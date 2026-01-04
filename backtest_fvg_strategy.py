#!/usr/bin/env python3
"""
Backtest FVG Inversion Strategy for Nasdaq (NQ)
Période: 2018-Aujourd'hui
Timeframe: 3 minutes avec filtre de tendance H1
Fenêtre de trading: London Killzone (01:00-04:00 Chicago time)

Stratégie:
- LONG: Prix comble un FVG Baissier + H1 Close > EMA50
- SHORT: Prix comble un FVG Haussier + H1 Close < EMA50
- SL: High/Low de la bougie signal
- TP: Ratio 1:1
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


def load_data_1min(filepath, delimiter=';'):
    """
    Charge les données 1 minute depuis un fichier CSV.
    
    Parameters:
    -----------
    filepath : str
        Chemin vers le fichier CSV
    delimiter : str
        Délimiteur du CSV
    
    Returns:
    --------
    pd.DataFrame
        DataFrame avec colonnes DateTime, Open, High, Low, Close
    """
    print(f"Chargement des données 1m depuis {filepath}...")
    
    try:
        df = pd.read_csv(filepath, delimiter=delimiter, encoding='utf-8-sig')
        
        # Format: Date;Time;Open;High;Low;Close;Volume
        if len(df.columns) >= 7:
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            df = df[['DateTime', 'Open', 'High', 'Low', 'Close']]
        
        # Convertir en numérique
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df.sort_values('DateTime', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        print(f"✓ Données 1m chargées: {len(df)} lignes")
        print(f"  Plage: {df['DateTime'].min()} à {df['DateTime'].max()}")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement: {str(e)}")


def load_data_1h(filepath, delimiter=';'):
    """
    Charge les données 1 heure depuis un fichier CSV.
    
    Parameters:
    -----------
    filepath : str
        Chemin vers le fichier CSV
    delimiter : str
        Délimiteur du CSV
    
    Returns:
    --------
    pd.DataFrame
        DataFrame avec colonnes DateTime, Open, High, Low, Close
    """
    print(f"Chargement des données 1H depuis {filepath}...")
    
    try:
        df = pd.read_csv(filepath, delimiter=delimiter, encoding='utf-8-sig')
        
        # Format: Date;Time;Open;High;Low;Close;Volume
        if len(df.columns) >= 7:
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            df = df[['DateTime', 'Open', 'High', 'Low', 'Close']]
        
        # Convertir en numérique
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df.sort_values('DateTime', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        print(f"✓ Données 1H chargées: {len(df)} lignes")
        print(f"  Plage: {df['DateTime'].min()} à {df['DateTime'].max()}")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement: {str(e)}")


def resample_to_3min(df_1min):
    """
    Convertit les données 1 minute en bougies de 3 minutes.
    
    Parameters:
    -----------
    df_1min : pd.DataFrame
        DataFrame avec données 1 minute
    
    Returns:
    --------
    pd.DataFrame
        DataFrame avec données 3 minutes
    """
    print("Resampling 1m → 3m...")
    
    df = df_1min.copy()
    df.set_index('DateTime', inplace=True)
    
    # Resampling OHLC
    df_3min = df.resample('3T').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last'
    })
    
    df_3min.dropna(inplace=True)
    df_3min.reset_index(inplace=True)
    
    print(f"✓ Resampling terminé: {len(df_3min)} bougies 3m")
    
    return df_3min


def calculate_ema(df, period=50):
    """
    Calcule l'EMA (Exponential Moving Average).
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame avec colonne Close
    period : int
        Période de l'EMA
    
    Returns:
    --------
    pd.Series
        Série avec les valeurs EMA
    """
    return df['Close'].ewm(span=period, adjust=False).mean()


def detect_fvg_bearish(df):
    """
    Détecte les FVG Baissiers: Low[i-2] > High[i]
    
    Returns:
    --------
    pd.DataFrame avec colonnes FVG_Bearish_Top et FVG_Bearish_Bottom
    """
    df = df.copy()
    
    # Décaler les valeurs
    df['Low_i_minus_2'] = df['Low'].shift(2)
    
    # Condition: Low[i-2] > High[i]
    condition = df['Low_i_minus_2'] > df['High']
    
    df['FVG_Bearish'] = False
    df['FVG_Bearish_Top'] = np.nan
    df['FVG_Bearish_Bottom'] = np.nan
    
    df.loc[condition, 'FVG_Bearish'] = True
    df.loc[condition, 'FVG_Bearish_Top'] = df.loc[condition, 'Low_i_minus_2']
    df.loc[condition, 'FVG_Bearish_Bottom'] = df.loc[condition, 'High']
    
    df.drop('Low_i_minus_2', axis=1, inplace=True)
    
    return df


def detect_fvg_bullish(df):
    """
    Détecte les FVG Haussiers: High[i-2] < Low[i]
    
    Returns:
    --------
    pd.DataFrame avec colonnes FVG_Bullish_Top et FVG_Bullish_Bottom
    """
    df = df.copy()
    
    # Décaler les valeurs
    df['High_i_minus_2'] = df['High'].shift(2)
    
    # Condition: High[i-2] < Low[i]
    condition = df['High_i_minus_2'] < df['Low']
    
    df['FVG_Bullish'] = False
    df['FVG_Bullish_Top'] = np.nan
    df['FVG_Bullish_Bottom'] = np.nan
    
    df.loc[condition, 'FVG_Bullish'] = True
    df.loc[condition, 'FVG_Bullish_Top'] = df.loc[condition, 'Low']
    df.loc[condition, 'FVG_Bullish_Bottom'] = df.loc[condition, 'High_i_minus_2']
    
    df.drop('High_i_minus_2', axis=1, inplace=True)
    
    return df


def merge_h1_data_to_3min(df_3min, df_1h):
    """
    Mappe les données H1 (EMA50) aux timestamps 3m.
    Utilise merge_asof pour éviter le lookahead bias.
    
    Parameters:
    -----------
    df_3min : pd.DataFrame
        Données 3 minutes
    df_1h : pd.DataFrame
        Données 1 heure avec EMA50
    
    Returns:
    --------
    pd.DataFrame
        Données 3m avec colonne H1_EMA50
    """
    print("Mapping des données H1 vers 3m...")
    
    # Calculer l'EMA50 sur H1
    df_1h = df_1h.copy()
    df_1h['H1_EMA50'] = calculate_ema(df_1h, period=50)
    df_1h['H1_Close'] = df_1h['Close']
    
    # Préparer pour merge_asof (éviter lookahead bias)
    df_3min = df_3min.sort_values('DateTime')
    df_1h_merge = df_1h[['DateTime', 'H1_Close', 'H1_EMA50']].sort_values('DateTime')
    
    # Merge asof: utilise la dernière valeur H1 disponible avant chaque timestamp 3m
    df_merged = pd.merge_asof(
        df_3min,
        df_1h_merge,
        on='DateTime',
        direction='backward'
    )
    
    print(f"✓ Mapping terminé")
    
    return df_merged


def is_london_killzone(dt):
    """
    Vérifie si le timestamp est dans la London Killzone (01:00-04:00).
    
    Parameters:
    -----------
    dt : datetime
        Timestamp à vérifier
    
    Returns:
    --------
    bool
        True si dans la fenêtre de trading
    """
    hour = dt.hour
    return 1 <= hour < 4


def backtest_strategy(df_3min, initial_capital=100000):
    """
    Exécute le backtest de la stratégie FVG Inversion.
    
    Conditions d'entrée:
    - LONG: Prix comble FVG Baissier (Close > FVG_Bearish_Bottom) + H1_Close > H1_EMA50
    - SHORT: Prix comble FVG Haussier (Close < FVG_Bullish_Top) + H1_Close < H1_EMA50
    - Fenêtre: London Killzone (01:00-04:00)
    
    Gestion:
    - SL: High/Low de la bougie signal
    - TP: RR 1:1
    - Une seule position à la fois
    
    Parameters:
    -----------
    df_3min : pd.DataFrame
        Données 3 minutes avec FVG et H1_EMA50
    initial_capital : float
        Capital de départ
    
    Returns:
    --------
    dict
        Résultats du backtest
    """
    print("\n" + "="*80)
    print("BACKTEST EN COURS...")
    print("="*80)
    
    capital = initial_capital
    position = None  # None, 'LONG' ou 'SHORT'
    entry_price = 0
    stop_loss = 0
    take_profit = 0
    entry_time = None
    
    trades = []
    equity_curve = []
    
    # Stocker les FVG récents (lookback 20 bougies)
    recent_fvg_bearish = []
    recent_fvg_bullish = []
    
    for i in range(len(df_3min)):
        row = df_3min.iloc[i]
        dt = row['DateTime']
        open_price = row['Open']
        high = row['High']
        low = row['Low']
        close = row['Close']
        h1_close = row.get('H1_Close', np.nan)
        h1_ema50 = row.get('H1_EMA50', np.nan)
        
        # Vérifier que nous avons les données H1
        if pd.isna(h1_close) or pd.isna(h1_ema50):
            equity_curve.append(capital)
            continue
        
        # Mettre à jour les FVG récents
        if row.get('FVG_Bearish', False):
            recent_fvg_bearish.append({
                'index': i,
                'top': row['FVG_Bearish_Top'],
                'bottom': row['FVG_Bearish_Bottom'],
                'datetime': dt
            })
            # Garder seulement les 20 derniers
            if len(recent_fvg_bearish) > 20:
                recent_fvg_bearish.pop(0)
        
        if row.get('FVG_Bullish', False):
            recent_fvg_bullish.append({
                'index': i,
                'top': row['FVG_Bullish_Top'],
                'bottom': row['FVG_Bullish_Bottom'],
                'datetime': dt
            })
            if len(recent_fvg_bullish) > 20:
                recent_fvg_bullish.pop(0)
        
        # Gestion de position ouverte
        if position is not None:
            # Vérifier SL/TP
            if position == 'LONG':
                # Check SL
                if low <= stop_loss:
                    pnl = stop_loss - entry_price
                    capital += pnl
                    trades.append({
                        'entry_time': entry_time,
                        'exit_time': dt,
                        'type': 'LONG',
                        'entry_price': entry_price,
                        'exit_price': stop_loss,
                        'pnl': pnl,
                        'result': 'LOSS'
                    })
                    position = None
                # Check TP
                elif high >= take_profit:
                    pnl = take_profit - entry_price
                    capital += pnl
                    trades.append({
                        'entry_time': entry_time,
                        'exit_time': dt,
                        'type': 'LONG',
                        'entry_price': entry_price,
                        'exit_price': take_profit,
                        'pnl': pnl,
                        'result': 'WIN'
                    })
                    position = None
            
            elif position == 'SHORT':
                # Check SL
                if high >= stop_loss:
                    pnl = entry_price - stop_loss
                    capital += pnl
                    trades.append({
                        'entry_time': entry_time,
                        'exit_time': dt,
                        'type': 'SHORT',
                        'entry_price': entry_price,
                        'exit_price': stop_loss,
                        'pnl': pnl,
                        'result': 'LOSS'
                    })
                    position = None
                # Check TP
                elif low <= take_profit:
                    pnl = entry_price - take_profit
                    capital += pnl
                    trades.append({
                        'entry_time': entry_time,
                        'exit_time': dt,
                        'type': 'SHORT',
                        'entry_price': entry_price,
                        'exit_price': take_profit,
                        'pnl': pnl,
                        'result': 'WIN'
                    })
                    position = None
        
        # Vérifier les signaux d'entrée (seulement si pas de position)
        if position is None and is_london_killzone(dt):
            # Signal LONG: Prix comble un FVG Baissier récent + H1_Close > H1_EMA50
            if h1_close > h1_ema50:
                for fvg in recent_fvg_bearish:
                    # Vérifier si le prix comble le FVG (Close > Bottom du FVG)
                    if close > fvg['bottom'] and close < fvg['top']:
                        # Entrée à la clôture de la bougie
                        entry_price = close
                        stop_loss = low
                        risk = entry_price - stop_loss
                        take_profit = entry_price + risk  # RR 1:1
                        position = 'LONG'
                        entry_time = dt
                        break
            
            # Signal SHORT: Prix comble un FVG Haussier récent + H1_Close < H1_EMA50
            elif h1_close < h1_ema50:
                for fvg in recent_fvg_bullish:
                    # Vérifier si le prix comble le FVG (Close < Top du FVG)
                    if close < fvg['top'] and close > fvg['bottom']:
                        # Entrée à la clôture de la bougie
                        entry_price = close
                        stop_loss = high
                        risk = stop_loss - entry_price
                        take_profit = entry_price - risk  # RR 1:1
                        position = 'SHORT'
                        entry_time = dt
                        break
        
        equity_curve.append(capital)
    
    # Calculer les statistiques
    total_trades = len(trades)
    winning_trades = [t for t in trades if t['result'] == 'WIN']
    losing_trades = [t for t in trades if t['result'] == 'LOSS']
    
    winrate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0
    
    total_wins = sum([t['pnl'] for t in winning_trades])
    total_losses = abs(sum([t['pnl'] for t in losing_trades]))
    
    profit_factor = (total_wins / total_losses) if total_losses > 0 else 0
    
    # Calculer le drawdown maximum
    peak = initial_capital
    max_drawdown = 0
    for equity in equity_curve:
        if equity > peak:
            peak = equity
        drawdown = (peak - equity) / peak * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    final_capital = capital
    total_return = ((final_capital - initial_capital) / initial_capital * 100)
    
    results = {
        'initial_capital': initial_capital,
        'final_capital': final_capital,
        'total_return': total_return,
        'total_trades': total_trades,
        'winning_trades': len(winning_trades),
        'losing_trades': len(losing_trades),
        'winrate': winrate,
        'profit_factor': profit_factor,
        'max_drawdown': max_drawdown,
        'trades': trades,
        'equity_curve': equity_curve
    }
    
    return results


def print_results(results):
    """
    Affiche les résultats du backtest.
    """
    print("\n" + "="*80)
    print("RÉSULTATS DU BACKTEST")
    print("="*80)
    print(f"\nCapital Initial:       ${results['initial_capital']:,.2f}")
    print(f"Capital Final:         ${results['final_capital']:,.2f}")
    print(f"Rendement Total:       {results['total_return']:.2f}%")
    print(f"\nNombre de Trades:      {results['total_trades']}")
    print(f"Trades Gagnants:       {results['winning_trades']}")
    print(f"Trades Perdants:       {results['losing_trades']}")
    print(f"Winrate:               {results['winrate']:.2f}%")
    print(f"Profit Factor:         {results['profit_factor']:.2f}")
    print(f"Drawdown Maximum:      {results['max_drawdown']:.2f}%")
    print("="*80)
    
    # Afficher quelques trades
    if results['total_trades'] > 0:
        print("\nPremiers 5 trades:")
        print("-" * 80)
        for i, trade in enumerate(results['trades'][:5], 1):
            print(f"Trade {i}: {trade['type']}")
            print(f"  Entrée: {trade['entry_time']} @ {trade['entry_price']:.2f}")
            print(f"  Sortie: {trade['exit_time']} @ {trade['exit_price']:.2f}")
            print(f"  P&L: {trade['pnl']:.2f} ({trade['result']})")
            print("-" * 80)


def main():
    """
    Fonction principale pour exécuter le backtest.
    """
    print("="*80)
    print("BACKTEST FVG INVERSION STRATEGY - NASDAQ (NQ)")
    print("="*80)
    print()
    
    # Note: Utiliser un seul fichier pour la démo (2025 1m.csv)
    # Pour le backtest complet 2018-2025, charger et concaténer tous les fichiers
    
    # Charger les données 1 minute
    df_1min = load_data_1min('2025 1m.csv')
    
    # Limiter à un échantillon pour la démo (premières 50000 lignes)
    print("\n⚠️  Utilisation d'un échantillon de données pour la démo (50,000 bougies 1m)")
    df_1min = df_1min.head(50000)
    
    # Resampler en 3 minutes
    df_3min = resample_to_3min(df_1min)
    
    # Charger les données 1 heure
    df_1h = load_data_1h('2025 1H.csv')
    
    # Limiter les données H1 à la même plage que 3m
    df_1h = df_1h[df_1h['DateTime'] <= df_3min['DateTime'].max()]
    
    # Détecter les FVG
    print("\nDétection des FVG Baissiers...")
    df_3min = detect_fvg_bearish(df_3min)
    
    print("Détection des FVG Haussiers...")
    df_3min = detect_fvg_bullish(df_3min)
    
    # Merger les données H1
    df_3min = merge_h1_data_to_3min(df_3min, df_1h)
    
    # Exécuter le backtest
    results = backtest_strategy(df_3min, initial_capital=100000)
    
    # Afficher les résultats
    print_results(results)
    
    # Sauvegarder les trades dans un CSV
    if results['total_trades'] > 0:
        trades_df = pd.DataFrame(results['trades'])
        trades_df.to_csv('backtest_trades.csv', index=False)
        print(f"\n✓ Trades sauvegardés dans: backtest_trades.csv")
    
    print("\n" + "="*80)
    print("BACKTEST TERMINÉ")
    print("="*80)


if __name__ == "__main__":
    main()
