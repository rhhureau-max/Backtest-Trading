#!/usr/bin/env python3
"""
Analyse des données de trading pour la stratégie de bougie 8h30 (ouverture New York)
Trouve tous les trades où la bougie de 8h30 dépasse les mèches des 5 dernières bougies précédentes.

Critères:
1. BULLISH: le HIGH de la bougie 8h30 dépasse le HIGH maximum des 5 bougies précédentes
2. BEARISH: le LOW de la bougie 8h30 est inférieur au LOW minimum des 5 bougies précédentes
"""

import pandas as pd
import zipfile
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Répertoire de base des données (utilise le répertoire du script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_csv_file(filepath):
    """Charge un fichier CSV avec le format approprié"""
    df = pd.read_csv(filepath, sep=';', 
                     names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                     skiprows=1)  # Skip header row
    
    # Combiner Date et Time en datetime
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    
    # Convertir les colonnes numériques
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df.dropna()


def load_zip_file(filepath):
    """Charge un fichier CSV zippé"""
    with zipfile.ZipFile(filepath, 'r') as z:
        # Obtenir le nom du fichier CSV dans le zip
        csv_files = [f for f in z.namelist() if f.endswith('.csv')]
        if csv_files:
            with z.open(csv_files[0]) as f:
                df = pd.read_csv(f, sep=';',
                               names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                               skiprows=1)
                
                # Combiner Date et Time en datetime
                df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
                
                # Convertir les colonnes numériques
                for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                return df.dropna()
    return pd.DataFrame()


def load_all_data(timeframe):
    """Charge toutes les données pour un timeframe donné (1m, 5m, 15m)"""
    all_data = []
    
    # Déterminer les années disponibles à partir des fichiers existants
    pattern = f"*{timeframe}.csv"
    years = set()
    for filename in os.listdir(BASE_DIR):
        if timeframe in filename and (filename.endswith('.csv') or filename.endswith('.csv.zip')):
            try:
                year = int(filename.split()[0])
                years.add(year)
            except (ValueError, IndexError):
                continue
    
    for year in sorted(years):
        # Chercher d'abord le fichier CSV, puis le zip
        csv_path = os.path.join(BASE_DIR, f"{year} {timeframe}.csv")
        zip_path = os.path.join(BASE_DIR, f"{year} {timeframe}.csv.zip")
        
        if os.path.exists(csv_path):
            print(f"  Loading {csv_path}...")
            df = load_csv_file(csv_path)
            all_data.append(df)
        elif os.path.exists(zip_path):
            print(f"  Loading {zip_path}...")
            df = load_zip_file(zip_path)
            if not df.empty:
                all_data.append(df)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.sort_values('DateTime').reset_index(drop=True)
        return combined
    return pd.DataFrame()


def get_830_candle_time(timeframe):
    """Retourne l'heure de la bougie 8h30 selon le timeframe"""
    # Pour tous les timeframes analysés, l'heure cible est 8h30
    return '08:30:00'


def find_previous_candles(df, idx, n_candles, timeframe):
    """
    Trouve les n bougies précédentes pour un index donné.
    Pour les timeframes 5m et 15m, on prend les n bougies immédiatement précédentes.
    Pour le timeframe 1m, on prend les n bougies précédentes (8:25, 8:26, 8:27, 8:28, 8:29).
    """
    if idx < n_candles:
        return None
    
    return df.iloc[idx - n_candles:idx]


def analyze_trades(df, timeframe):
    """
    Analyse les trades pour un DataFrame et timeframe donnés.
    Trouve les bougies de 8h30 qui dépassent les mèches des 5 bougies précédentes.
    """
    trades = []
    target_time = get_830_candle_time(timeframe)
    
    # Extraire l'heure de chaque bougie
    df['TimeOnly'] = df['DateTime'].dt.strftime('%H:%M:%S')
    
    # Filtrer les bougies de 8h30
    candles_830 = df[df['TimeOnly'] == target_time].copy()
    
    print(f"  Found {len(candles_830)} candles at {target_time}")
    
    for idx_830 in candles_830.index:
        # Obtenir la position dans le DataFrame original
        pos = df.index.get_loc(idx_830)
        
        # Obtenir les 5 bougies précédentes
        prev_candles = find_previous_candles(df, pos, 5, timeframe)
        
        if prev_candles is None or len(prev_candles) < 5:
            continue
        
        # Calculer le max High et min Low des 5 bougies précédentes
        max_high_prev = prev_candles['High'].max()
        min_low_prev = prev_candles['Low'].min()
        
        # Bougie actuelle (8h30)
        current_candle = df.loc[idx_830]
        current_high = current_candle['High']
        current_low = current_candle['Low']
        current_open = current_candle['Open']
        current_close = current_candle['Close']
        current_datetime = current_candle['DateTime']
        
        # Déterminer si la bougie est bullish ou bearish
        is_bullish = current_close > current_open
        is_bearish = current_close < current_open
        
        trade = None
        
        # Critère BULLISH: HIGH dépasse le HIGH max des 5 bougies précédentes
        if is_bullish and current_high > max_high_prev:
            trade = {
                'Date': current_datetime.strftime('%Y-%m-%d'),
                'Time': current_datetime.strftime('%H:%M:%S'),
                'Type': 'Bullish',
                'Entry_Price': current_close,  # Entrée sur le close pour bullish
                'Open_830': current_open,
                'High_830': current_high,
                'Low_830': current_low,
                'Close_830': current_close,
                'Max_High_Prev5': max_high_prev,
                'Min_Low_Prev5': min_low_prev,
                'Prev_Candles_Start': prev_candles.iloc[0]['DateTime'].strftime('%H:%M:%S'),
                'Prev_Candles_End': prev_candles.iloc[-1]['DateTime'].strftime('%H:%M:%S')
            }
        
        # Critère BEARISH: LOW inférieur au LOW min des 5 bougies précédentes
        elif is_bearish and current_low < min_low_prev:
            trade = {
                'Date': current_datetime.strftime('%Y-%m-%d'),
                'Time': current_datetime.strftime('%H:%M:%S'),
                'Type': 'Bearish',
                'Entry_Price': current_close,  # Entrée sur le close pour bearish
                'Open_830': current_open,
                'High_830': current_high,
                'Low_830': current_low,
                'Close_830': current_close,
                'Max_High_Prev5': max_high_prev,
                'Min_Low_Prev5': min_low_prev,
                'Prev_Candles_Start': prev_candles.iloc[0]['DateTime'].strftime('%H:%M:%S'),
                'Prev_Candles_End': prev_candles.iloc[-1]['DateTime'].strftime('%H:%M:%S')
            }
        
        if trade:
            trades.append(trade)
    
    return trades


def generate_report(trades_1m, trades_5m, trades_15m):
    """Génère le rapport complet"""
    report = []
    report.append("=" * 100)
    report.append("RAPPORT D'ANALYSE - STRATÉGIE BOUGIE 8H30 (OUVERTURE NEW YORK)")
    report.append("=" * 100)
    report.append("")
    report.append("Critères de la stratégie:")
    report.append("  - BULLISH: le HIGH de la bougie 8h30 dépasse le HIGH maximum des 5 bougies précédentes")
    report.append("  - BEARISH: le LOW de la bougie 8h30 est inférieur au LOW minimum des 5 bougies précédentes")
    report.append("")
    report.append("Période analysée: 2018-2025")
    report.append("")
    
    # Résumé
    report.append("-" * 100)
    report.append("RÉSUMÉ")
    report.append("-" * 100)
    report.append(f"  Trades identifiés sur 1 minute:  {len(trades_1m)} trades")
    report.append(f"  Trades identifiés sur 5 minutes: {len(trades_5m)} trades")
    report.append(f"  Trades identifiés sur 15 minutes: {len(trades_15m)} trades")
    report.append("")
    
    # Statistiques par type pour chaque timeframe
    for name, trades in [('1 minute', trades_1m), ('5 minutes', trades_5m), ('15 minutes', trades_15m)]:
        bullish = len([t for t in trades if t['Type'] == 'Bullish'])
        bearish = len([t for t in trades if t['Type'] == 'Bearish'])
        report.append(f"  {name}: {bullish} Bullish, {bearish} Bearish")
    
    report.append("")
    
    # Détails des trades pour chaque timeframe
    for name, trades, tf in [('1 MINUTE', trades_1m, '1m'), 
                              ('5 MINUTES', trades_5m, '5m'), 
                              ('15 MINUTES', trades_15m, '15m')]:
        report.append("=" * 100)
        report.append(f"TRADES IDENTIFIÉS - BOUGIES {name}")
        report.append("=" * 100)
        report.append("")
        
        if not trades:
            report.append("  Aucun trade identifié pour ce timeframe.")
            report.append("")
            continue
        
        # Statistiques par année
        trades_by_year = {}
        for t in trades:
            year = t['Date'][:4]
            if year not in trades_by_year:
                trades_by_year[year] = {'Bullish': 0, 'Bearish': 0}
            trades_by_year[year][t['Type']] += 1
        
        report.append("Statistiques par année:")
        for year in sorted(trades_by_year.keys()):
            stats = trades_by_year[year]
            report.append(f"  {year}: {stats['Bullish']} Bullish, {stats['Bearish']} Bearish (Total: {stats['Bullish'] + stats['Bearish']})")
        report.append("")
        
        report.append("-" * 100)
        report.append("Liste détaillée des trades:")
        report.append("-" * 100)
        report.append("")
        
        # En-tête du tableau
        header = f"{'Date':<12} {'Type':<8} {'Entry Price':<14} {'High 8h30':<14} {'Low 8h30':<14} {'Max High Prev5':<16} {'Min Low Prev5':<16}"
        report.append(header)
        report.append("-" * len(header))
        
        for trade in trades:
            line = f"{trade['Date']:<12} {trade['Type']:<8} {trade['Entry_Price']:<14.2f} {trade['High_830']:<14.2f} {trade['Low_830']:<14.2f} {trade['Max_High_Prev5']:<16.2f} {trade['Min_Low_Prev5']:<16.2f}"
            report.append(line)
        
        report.append("")
    
    return "\n".join(report)


def main():
    print("=" * 80)
    print("ANALYSE DE LA STRATÉGIE BOUGIE 8H30 (OUVERTURE NEW YORK)")
    print("=" * 80)
    print()
    
    trades_1m = []
    trades_5m = []
    trades_15m = []
    
    # Analyse des bougies 1 minute
    print("=" * 50)
    print("1. ANALYSE DES BOUGIES 1 MINUTE")
    print("=" * 50)
    df_1m = load_all_data('1m')
    if not df_1m.empty:
        print(f"  Total records loaded: {len(df_1m)}")
        trades_1m = analyze_trades(df_1m, '1m')
        print(f"  Trades identified: {len(trades_1m)}")
    else:
        print("  No data found for 1m timeframe")
    print()
    
    # Analyse des bougies 5 minutes
    print("=" * 50)
    print("2. ANALYSE DES BOUGIES 5 MINUTES")
    print("=" * 50)
    df_5m = load_all_data('5m')
    if not df_5m.empty:
        print(f"  Total records loaded: {len(df_5m)}")
        trades_5m = analyze_trades(df_5m, '5m')
        print(f"  Trades identified: {len(trades_5m)}")
    else:
        print("  No data found for 5m timeframe")
    print()
    
    # Analyse des bougies 15 minutes
    print("=" * 50)
    print("3. ANALYSE DES BOUGIES 15 MINUTES")
    print("=" * 50)
    df_15m = load_all_data('15m')
    if not df_15m.empty:
        print(f"  Total records loaded: {len(df_15m)}")
        trades_15m = analyze_trades(df_15m, '15m')
        print(f"  Trades identified: {len(trades_15m)}")
    else:
        print("  No data found for 15m timeframe")
    print()
    
    # Générer le rapport
    print("=" * 50)
    print("GÉNÉRATION DU RAPPORT")
    print("=" * 50)
    
    report = generate_report(trades_1m, trades_5m, trades_15m)
    
    # Sauvegarder le rapport
    report_path = os.path.join(BASE_DIR, "trading_analysis_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"  Report saved to: {report_path}")
    
    # Sauvegarder les trades en CSV pour chaque timeframe
    for name, trades in [('1m', trades_1m), 
                         ('5m', trades_5m), 
                         ('15m', trades_15m)]:
        if trades:
            csv_path = os.path.join(BASE_DIR, f"trades_{name}.csv")
            df_trades = pd.DataFrame(trades)
            df_trades.to_csv(csv_path, index=False)
            print(f"  Trades CSV saved to: {csv_path}")
    
    print()
    print("=" * 80)
    print("ANALYSE TERMINÉE")
    print("=" * 80)
    
    # Afficher le rapport
    print()
    print(report)


if __name__ == "__main__":
    main()
