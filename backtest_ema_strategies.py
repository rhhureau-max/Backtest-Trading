#!/usr/bin/env python3
"""
Backtesting de 3 stratégies EMA sur NQ et ES (2018-2025)
Stratégies:
1. EMA Crossover Court Terme (9/21)
2. EMA Crossover Moyen Terme (20/50)
3. Triple EMA (8/21/55)

Analyse détaillée par actif, année et stratégie avec PnL et Win Rate
"""

import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple

import pandas as pd
import numpy as np

# Configuration
DATA_DIR = Path(__file__).parent
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 150)
pd.set_option('display.float_format', '{:.2f}'.format)


@dataclass
class Trade:
    """Représente un trade"""
    entry_date: datetime
    exit_date: datetime
    entry_price: float
    exit_price: float
    direction: str  # 'LONG' ou 'SHORT'
    pnl_points: float
    pnl_percent: float

    @property
    def is_winner(self) -> bool:
        return self.pnl_points > 0


@dataclass
class StrategyResult:
    """Résultats d'une stratégie"""
    strategy_name: str
    symbol: str
    year: int
    trades: List[Trade]

    @property
    def total_trades(self) -> int:
        return len(self.trades)

    @property
    def winning_trades(self) -> int:
        return sum(1 for t in self.trades if t.is_winner)

    @property
    def losing_trades(self) -> int:
        return self.total_trades - self.winning_trades

    @property
    def win_rate(self) -> float:
        if self.total_trades == 0:
            return 0.0
        return (self.winning_trades / self.total_trades) * 100

    @property
    def total_pnl_points(self) -> float:
        return sum(t.pnl_points for t in self.trades)

    @property
    def total_pnl_percent(self) -> float:
        return sum(t.pnl_percent for t in self.trades)

    @property
    def avg_win(self) -> float:
        winners = [t.pnl_points for t in self.trades if t.is_winner]
        return np.mean(winners) if winners else 0.0

    @property
    def avg_loss(self) -> float:
        losers = [t.pnl_points for t in self.trades if not t.is_winner]
        return np.mean(losers) if losers else 0.0

    @property
    def profit_factor(self) -> float:
        gross_profit = sum(t.pnl_points for t in self.trades if t.is_winner)
        gross_loss = abs(sum(t.pnl_points for t in self.trades if not t.is_winner))
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0.0
        return gross_profit / gross_loss

    @property
    def max_drawdown(self) -> float:
        if not self.trades:
            return 0.0
        cumulative = np.cumsum([t.pnl_points for t in self.trades])
        running_max = np.maximum.accumulate(cumulative)
        drawdown = cumulative - running_max
        return drawdown.min() if len(drawdown) > 0 else 0.0


def load_csv_data(filepath: Path) -> pd.DataFrame:
    """Charge un fichier CSV"""
    try:
        df = pd.read_csv(
            filepath,
            sep=';',
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1,
            encoding='utf-8-sig'
        )

        datetime_str = df['Date'] + ' ' + df['Time']
        try:
            df['Datetime'] = pd.to_datetime(datetime_str, format='%d/%m/%Y %H:%M:%S')
        except:
            try:
                df['Datetime'] = pd.to_datetime(datetime_str, format='%m/%d/%Y %H:%M:%S')
            except:
                df['Datetime'] = pd.to_datetime(datetime_str, format='mixed', dayfirst=True)

        df = df.set_index('Datetime')
        df = df.drop(columns=['Date', 'Time'])

        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df.dropna()
    except Exception as e:
        print(f"Erreur lecture {filepath.name}: {e}")
        return pd.DataFrame()


def load_all_daily_data(symbol: str) -> pd.DataFrame:
    """Charge toutes les données journalières pour un symbole"""
    all_data = []

    if symbol == 'NQ':
        for year in range(2018, 2026):
            filepath = DATA_DIR / f"{year} 1D.csv"
            if filepath.exists():
                df = load_csv_data(filepath)
                if not df.empty:
                    all_data.append(df)
    elif symbol == 'ES':
        filepath = DATA_DIR / "ES 1D (2018-2025).csv"
        if filepath.exists():
            df = load_csv_data(filepath)
            if not df.empty:
                all_data.append(df)

    if all_data:
        return pd.concat(all_data).sort_index()
    return pd.DataFrame()


def calculate_ema(data: pd.Series, period: int) -> pd.Series:
    """Calcule l'EMA"""
    return data.ewm(span=period, adjust=False).mean()


def strategy_ema_crossover(df: pd.DataFrame, fast_period: int, slow_period: int,
                           strategy_name: str) -> List[Trade]:
    """
    Stratégie EMA Crossover
    - LONG quand EMA rapide croise au-dessus de EMA lente
    - SHORT quand EMA rapide croise en-dessous de EMA lente
    """
    df = df.copy()
    df['EMA_Fast'] = calculate_ema(df['Close'], fast_period)
    df['EMA_Slow'] = calculate_ema(df['Close'], slow_period)

    # Signaux
    df['Signal'] = 0
    df.loc[df['EMA_Fast'] > df['EMA_Slow'], 'Signal'] = 1   # Long
    df.loc[df['EMA_Fast'] < df['EMA_Slow'], 'Signal'] = -1  # Short

    # Changements de position
    df['Position_Change'] = df['Signal'].diff()

    trades = []
    position = None
    entry_date = None
    entry_price = None

    for idx, row in df.iterrows():
        if pd.isna(row['Position_Change']):
            continue

        # Entrée Long
        if row['Position_Change'] == 2 or (row['Position_Change'] == 1 and position is None):
            if position == 'SHORT':
                # Fermer short
                pnl_points = entry_price - row['Close']
                pnl_percent = (pnl_points / entry_price) * 100
                trades.append(Trade(
                    entry_date=entry_date,
                    exit_date=idx,
                    entry_price=entry_price,
                    exit_price=row['Close'],
                    direction='SHORT',
                    pnl_points=pnl_points,
                    pnl_percent=pnl_percent
                ))
            # Ouvrir long
            position = 'LONG'
            entry_date = idx
            entry_price = row['Close']

        # Entrée Short
        elif row['Position_Change'] == -2 or (row['Position_Change'] == -1 and position is None):
            if position == 'LONG':
                # Fermer long
                pnl_points = row['Close'] - entry_price
                pnl_percent = (pnl_points / entry_price) * 100
                trades.append(Trade(
                    entry_date=entry_date,
                    exit_date=idx,
                    entry_price=entry_price,
                    exit_price=row['Close'],
                    direction='LONG',
                    pnl_points=pnl_points,
                    pnl_percent=pnl_percent
                ))
            # Ouvrir short
            position = 'SHORT'
            entry_date = idx
            entry_price = row['Close']

    return trades


def strategy_triple_ema(df: pd.DataFrame, fast: int, medium: int, slow: int,
                        strategy_name: str) -> List[Trade]:
    """
    Stratégie Triple EMA
    - LONG quand EMA fast > EMA medium > EMA slow (tendance haussière confirmée)
    - SHORT quand EMA fast < EMA medium < EMA slow (tendance baissière confirmée)
    - Sortie quand la configuration se casse
    """
    df = df.copy()
    df['EMA_Fast'] = calculate_ema(df['Close'], fast)
    df['EMA_Medium'] = calculate_ema(df['Close'], medium)
    df['EMA_Slow'] = calculate_ema(df['Close'], slow)

    # Signaux
    df['Signal'] = 0
    # Long: Fast > Medium > Slow
    df.loc[(df['EMA_Fast'] > df['EMA_Medium']) &
           (df['EMA_Medium'] > df['EMA_Slow']), 'Signal'] = 1
    # Short: Fast < Medium < Slow
    df.loc[(df['EMA_Fast'] < df['EMA_Medium']) &
           (df['EMA_Medium'] < df['EMA_Slow']), 'Signal'] = -1

    # Changements de position
    df['Position_Change'] = df['Signal'].diff()

    trades = []
    position = None
    entry_date = None
    entry_price = None

    for idx, row in df.iterrows():
        if pd.isna(row['Position_Change']):
            continue

        current_signal = row['Signal']

        # Fermer position si signal neutre ou inversé
        if position == 'LONG' and current_signal != 1:
            pnl_points = row['Close'] - entry_price
            pnl_percent = (pnl_points / entry_price) * 100
            trades.append(Trade(
                entry_date=entry_date,
                exit_date=idx,
                entry_price=entry_price,
                exit_price=row['Close'],
                direction='LONG',
                pnl_points=pnl_points,
                pnl_percent=pnl_percent
            ))
            position = None

        elif position == 'SHORT' and current_signal != -1:
            pnl_points = entry_price - row['Close']
            pnl_percent = (pnl_points / entry_price) * 100
            trades.append(Trade(
                entry_date=entry_date,
                exit_date=idx,
                entry_price=entry_price,
                exit_price=row['Close'],
                direction='SHORT',
                pnl_points=pnl_points,
                pnl_percent=pnl_percent
            ))
            position = None

        # Ouvrir nouvelle position
        if position is None:
            if current_signal == 1:
                position = 'LONG'
                entry_date = idx
                entry_price = row['Close']
            elif current_signal == -1:
                position = 'SHORT'
                entry_date = idx
                entry_price = row['Close']

    return trades


def run_backtest(symbol: str, strategy_func, strategy_name: str, **params) -> List[StrategyResult]:
    """Exécute le backtest pour un symbole et une stratégie"""
    df = load_all_daily_data(symbol)
    if df.empty:
        return []

    results = []

    # Backtest par année
    for year in df.index.year.unique():
        year_df = df[df.index.year == year].copy()
        if len(year_df) < 50:  # Minimum de données
            continue

        trades = strategy_func(year_df, **params, strategy_name=strategy_name)

        result = StrategyResult(
            strategy_name=strategy_name,
            symbol=symbol,
            year=year,
            trades=trades
        )
        results.append(result)

    # Backtest global (toutes années)
    all_trades = strategy_func(df, **params, strategy_name=strategy_name)
    global_result = StrategyResult(
        strategy_name=strategy_name,
        symbol=symbol,
        year=0,  # 0 = toutes les années
        trades=all_trades
    )
    results.append(global_result)

    return results


def print_results_table(results: List[StrategyResult], title: str):
    """Affiche les résultats sous forme de tableau"""
    print(f"\n{'='*120}")
    print(f"{title}")
    print(f"{'='*120}")

    data = []
    for r in results:
        year_label = "TOTAL" if r.year == 0 else str(r.year)
        data.append({
            'Stratégie': r.strategy_name,
            'Actif': r.symbol,
            'Année': year_label,
            'Trades': r.total_trades,
            'Gagnants': r.winning_trades,
            'Perdants': r.losing_trades,
            'Win Rate %': f"{r.win_rate:.1f}",
            'PnL Points': f"{r.total_pnl_points:.2f}",
            'PnL %': f"{r.total_pnl_percent:.2f}",
            'Avg Win': f"{r.avg_win:.2f}",
            'Avg Loss': f"{r.avg_loss:.2f}",
            'Profit Factor': f"{r.profit_factor:.2f}" if r.profit_factor != float('inf') else "∞",
            'Max DD': f"{r.max_drawdown:.2f}"
        })

    df = pd.DataFrame(data)
    print(df.to_string(index=False))


def print_comparison_summary(all_results: Dict[str, List[StrategyResult]]):
    """Affiche un résumé comparatif des stratégies"""
    print("\n" + "="*120)
    print("COMPARAISON DES STRATEGIES - RESULTATS GLOBAUX")
    print("="*120)

    comparison_data = []

    for strategy_name, results in all_results.items():
        # Filtrer les résultats globaux (year=0)
        global_results = [r for r in results if r.year == 0]

        for r in global_results:
            comparison_data.append({
                'Stratégie': strategy_name,
                'Actif': r.symbol,
                'Total Trades': r.total_trades,
                'Win Rate %': r.win_rate,
                'PnL Total (pts)': r.total_pnl_points,
                'PnL Total %': r.total_pnl_percent,
                'Profit Factor': r.profit_factor if r.profit_factor != float('inf') else 999,
                'Max Drawdown': r.max_drawdown,
                'Avg Trade (pts)': r.total_pnl_points / r.total_trades if r.total_trades > 0 else 0
            })

    df = pd.DataFrame(comparison_data)

    # Trier par PnL
    df = df.sort_values('PnL Total (pts)', ascending=False)

    # Formater pour affichage
    df['Win Rate %'] = df['Win Rate %'].apply(lambda x: f"{x:.1f}")
    df['PnL Total (pts)'] = df['PnL Total (pts)'].apply(lambda x: f"{x:.2f}")
    df['PnL Total %'] = df['PnL Total %'].apply(lambda x: f"{x:.2f}")
    df['Profit Factor'] = df['Profit Factor'].apply(lambda x: f"{x:.2f}" if x < 999 else "∞")
    df['Max Drawdown'] = df['Max Drawdown'].apply(lambda x: f"{x:.2f}")
    df['Avg Trade (pts)'] = df['Avg Trade (pts)'].apply(lambda x: f"{x:.2f}")

    print(df.to_string(index=False))


def print_yearly_comparison(all_results: Dict[str, List[StrategyResult]]):
    """Affiche la comparaison par année"""
    print("\n" + "="*120)
    print("COMPARAISON PAR ANNEE - PnL EN POINTS")
    print("="*120)

    # Créer un pivot table
    yearly_data = []

    for strategy_name, results in all_results.items():
        for r in results:
            if r.year != 0:  # Exclure les totaux
                yearly_data.append({
                    'Stratégie': f"{strategy_name} ({r.symbol})",
                    'Année': r.year,
                    'PnL': r.total_pnl_points,
                    'Win Rate': r.win_rate,
                    'Trades': r.total_trades
                })

    df = pd.DataFrame(yearly_data)

    # Pivot pour PnL
    pivot_pnl = df.pivot_table(index='Stratégie', columns='Année', values='PnL', aggfunc='first')
    pivot_pnl = pivot_pnl.round(2)

    print("\nPnL par année (en points):")
    print(pivot_pnl.to_string())

    # Pivot pour Win Rate
    pivot_wr = df.pivot_table(index='Stratégie', columns='Année', values='Win Rate', aggfunc='first')
    pivot_wr = pivot_wr.round(1)

    print("\n\nWin Rate par année (%):")
    print(pivot_wr.to_string())


def print_best_worst_trades(all_results: Dict[str, List[StrategyResult]], n: int = 5):
    """Affiche les meilleurs et pires trades"""
    print("\n" + "="*120)
    print(f"TOP {n} MEILLEURS ET PIRES TRADES")
    print("="*120)

    all_trades = []
    for strategy_name, results in all_results.items():
        for r in results:
            if r.year == 0:  # Uniquement résultats globaux
                for t in r.trades:
                    all_trades.append({
                        'Stratégie': strategy_name,
                        'Actif': r.symbol,
                        'Direction': t.direction,
                        'Entrée': t.entry_date.strftime('%Y-%m-%d'),
                        'Sortie': t.exit_date.strftime('%Y-%m-%d'),
                        'Prix Entrée': t.entry_price,
                        'Prix Sortie': t.exit_price,
                        'PnL (pts)': t.pnl_points,
                        'PnL %': t.pnl_percent
                    })

    df = pd.DataFrame(all_trades)

    print(f"\n{n} MEILLEURS TRADES:")
    best = df.nlargest(n, 'PnL (pts)')
    best['PnL (pts)'] = best['PnL (pts)'].apply(lambda x: f"{x:.2f}")
    best['PnL %'] = best['PnL %'].apply(lambda x: f"{x:.2f}")
    best['Prix Entrée'] = best['Prix Entrée'].apply(lambda x: f"{x:.2f}")
    best['Prix Sortie'] = best['Prix Sortie'].apply(lambda x: f"{x:.2f}")
    print(best.to_string(index=False))

    print(f"\n{n} PIRES TRADES:")
    worst = df.nsmallest(n, 'PnL (pts)')
    worst['PnL (pts)'] = worst['PnL (pts)'].apply(lambda x: f"{x:.2f}")
    worst['PnL %'] = worst['PnL %'].apply(lambda x: f"{x:.2f}")
    worst['Prix Entrée'] = worst['Prix Entrée'].apply(lambda x: f"{x:.2f}")
    worst['Prix Sortie'] = worst['Prix Sortie'].apply(lambda x: f"{x:.2f}")
    print(worst.to_string(index=False))


def main():
    """Point d'entrée principal"""
    print("="*120)
    print("BACKTESTING DE STRATEGIES EMA - NQ ET ES (2018-2025)")
    print("="*120)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Définition des stratégies
    strategies = {
        'EMA Crossover 9/21 (Court Terme)': {
            'func': strategy_ema_crossover,
            'params': {'fast_period': 9, 'slow_period': 21}
        },
        'EMA Crossover 20/50 (Moyen Terme)': {
            'func': strategy_ema_crossover,
            'params': {'fast_period': 20, 'slow_period': 50}
        },
        'Triple EMA 8/21/55': {
            'func': strategy_triple_ema,
            'params': {'fast': 8, 'medium': 21, 'slow': 55}
        }
    }

    symbols = ['NQ', 'ES']
    all_results = {}

    # Exécuter les backtests
    for strategy_name, strategy_config in strategies.items():
        print(f"\nBacktesting: {strategy_name}...")
        strategy_results = []

        for symbol in symbols:
            print(f"  - {symbol}...")
            results = run_backtest(
                symbol=symbol,
                strategy_func=strategy_config['func'],
                strategy_name=strategy_name,
                **strategy_config['params']
            )
            strategy_results.extend(results)

        all_results[strategy_name] = strategy_results

    print("\n" + "="*120)
    print("RESULTATS DETAILLES")
    print("="*120)

    # Afficher les résultats détaillés par stratégie
    for strategy_name, results in all_results.items():
        # Résultats NQ
        nq_results = [r for r in results if r.symbol == 'NQ']
        print_results_table(nq_results, f"{strategy_name} - NQ (Nasdaq-100 Futures)")

        # Résultats ES
        es_results = [r for r in results if r.symbol == 'ES']
        print_results_table(es_results, f"{strategy_name} - ES (S&P 500 Futures)")

    # Comparaisons
    print_comparison_summary(all_results)
    print_yearly_comparison(all_results)
    print_best_worst_trades(all_results, n=5)

    # Résumé final
    print("\n" + "="*120)
    print("RESUME ET CONCLUSIONS")
    print("="*120)

    # Trouver la meilleure stratégie par PnL
    best_by_pnl = {}
    for strategy_name, results in all_results.items():
        for r in results:
            if r.year == 0:
                key = f"{strategy_name} ({r.symbol})"
                best_by_pnl[key] = {
                    'pnl': r.total_pnl_points,
                    'pnl_pct': r.total_pnl_percent,
                    'win_rate': r.win_rate,
                    'trades': r.total_trades,
                    'pf': r.profit_factor
                }

    # Trier par PnL
    sorted_strategies = sorted(best_by_pnl.items(), key=lambda x: x[1]['pnl'], reverse=True)

    print("\nCLASSEMENT PAR PnL TOTAL (Points):")
    print("-" * 80)
    for i, (name, stats) in enumerate(sorted_strategies, 1):
        pf_str = f"{stats['pf']:.2f}" if stats['pf'] != float('inf') else "∞"
        print(f"{i}. {name}")
        print(f"   PnL: {stats['pnl']:.2f} pts ({stats['pnl_pct']:.2f}%) | "
              f"Win Rate: {stats['win_rate']:.1f}% | "
              f"Trades: {stats['trades']} | "
              f"Profit Factor: {pf_str}")

    print("\n" + "="*120)
    print("OBSERVATIONS CLES:")
    print("="*120)
    print("""
1. STRATEGIE EMA CROSSOVER 9/21 (Court Terme):
   - Plus de trades, plus réactive aux mouvements de marché
   - Win rate généralement plus bas (plus de faux signaux)
   - Meilleure pour les marchés volatils

2. STRATEGIE EMA CROSSOVER 20/50 (Moyen Terme):
   - Moins de trades, filtre le bruit du marché
   - Win rate potentiellement meilleur
   - Capture les tendances plus établies

3. STRATEGIE TRIPLE EMA 8/21/55:
   - Confirmation plus forte des tendances
   - Moins de faux signaux mais entrées tardives
   - Meilleure en marchés directionnels forts

NOTES:
- Les résultats ne prennent pas en compte les frais de transaction
- Les backtests utilisent les prix de clôture pour les entrées/sorties
- Le PnL est calculé en points (pas en dollars)
- Performance passée ne garantit pas les résultats futurs
""")

    print("="*120)
    print("FIN DU RAPPORT")
    print("="*120)


if __name__ == "__main__":
    main()
