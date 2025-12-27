"""
Comprehensive Backtest Results for London Killzone Strategies
Running on all available NQ data from 2018 to 2025
"""

import os
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from london_killzone_strategies import (
    DataLoader,
    TimeManager,
    StrategyA_JudasSwing,
    StrategyB_ORBRetest,
    StrategyC_HTFContinuation,
    BacktestEngine,
    create_comparison_table
)


def run_comprehensive_backtest():
    """Run complete backtest on all available NQ data."""
    
    print("="*100)
    print("RÉSULTATS RÉELS - STRATÉGIES LONDON KILLZONE SUR NQ")
    print("="*100)
    print()
    
    # Define all data files
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
    files_5m = [os.path.join(base_path, f"{year} 5m.csv") for year in years]
    files_4h = [os.path.join(base_path, f"{year} 4H.csv") for year in years]
    
    # Filter only existing files
    files_5m = [f for f in files_5m if os.path.exists(f)]
    files_4h = [f for f in files_4h if os.path.exists(f)]
    
    print("CHARGEMENT DES DONNÉES")
    print("-" * 100)
    print(f"Fichiers 5m à charger: {len(files_5m)}")
    print(f"Fichiers 4H à charger: {len(files_4h)}")
    print()
    
    # Load 5-minute data
    print("Chargement des données 5 minutes...")
    df_5m = DataLoader.load_multiple_files(files_5m)
    
    if len(df_5m) == 0:
        print("ERREUR: Aucune donnée 5m chargée")
        return
    
    print(f"\n✓ Total données 5m: {len(df_5m):,} bougies")
    print(f"  Période: {df_5m.index.min()} à {df_5m.index.max()}")
    print(f"  Jours de trading: {pd.Series(df_5m.index.date).nunique():,}")
    
    # Load 4H data
    print("\nChargement des données 4 heures...")
    df_4h = DataLoader.load_multiple_files(files_4h)
    
    if len(df_4h) > 0:
        print(f"✓ Total données 4H: {len(df_4h):,} bougies")
    else:
        print("⚠️  Aucune donnée 4H - Strategy C utilisera une méthode alternative")
        df_4h = None
    
    # Convert to Paris time
    print("\nConversion en heure de Paris...")
    try:
        df_5m = TimeManager.convert_to_paris_time(df_5m)
        if df_4h is not None:
            df_4h = TimeManager.convert_to_paris_time(df_4h)
        print("✓ Conversion réussie")
    except Exception as e:
        print(f"Note: {e}")
    
    # Initialize backtest engine
    engine = BacktestEngine(df_5m, df_4h)
    
    # Store all results
    all_results = {}
    all_trades = {}
    
    # =========================================================================
    # STRATEGY A: JUDAS SWING
    # =========================================================================
    print("\n" + "="*100)
    print("STRATÉGIE A: JUDAS SWING (Chasse aux Liquidités)")
    print("="*100)
    
    strategy_a = StrategyA_JudasSwing(points_offset=5.0, risk_reward=3.0)
    trades_a = engine.run_strategy(strategy_a)
    perf_a = engine.generate_performance_report(trades_a, "Judas Swing")
    
    all_results['Strategy A'] = perf_a
    all_trades['Strategy A'] = trades_a
    
    print("\n📊 RÉSULTATS DÉTAILLÉS:")
    print(f"  Trades totaux: {perf_a['total_trades']}")
    print(f"  Trades gagnants: {perf_a['winning_trades']}")
    print(f"  Trades perdants: {perf_a['losing_trades']}")
    print(f"  Win Rate: {perf_a['win_rate']:.2f}%")
    print(f"  Gain moyen: {perf_a['avg_win']:.2f} points")
    print(f"  Perte moyenne: {perf_a['avg_loss']:.2f} points")
    print(f"  Profit Factor: {perf_a['profit_factor']:.2f}")
    print(f"  P&L Total: {perf_a['total_pnl']:.2f} points")
    print(f"  R:R Moyen Réalisé: {perf_a['avg_risk_reward']:.2f}")
    print(f"  Max pertes consécutives: {perf_a['max_consecutive_losses']}")
    
    if trades_a:
        df_trades_a = pd.DataFrame(trades_a)
        print(f"\n📈 STATISTIQUES PAR ANNÉE:")
        df_trades_a['year'] = pd.to_datetime(df_trades_a['date']).dt.year
        yearly_stats = df_trades_a.groupby('year').agg({
            'result': lambda x: (x == 'WIN').sum(),
            'pnl_points': ['count', 'sum']
        })
        for year in yearly_stats.index:
            wins = yearly_stats.loc[year, ('result', '<lambda>')]
            total = yearly_stats.loc[year, ('pnl_points', 'count')]
            pnl = yearly_stats.loc[year, ('pnl_points', 'sum')]
            wr = (wins/total*100) if total > 0 else 0
            print(f"  {year}: {total} trades, {wins} wins ({wr:.1f}%), P&L: {pnl:.2f} pts")
    
    # =========================================================================
    # STRATEGY B: ORB RETEST
    # =========================================================================
    print("\n" + "="*100)
    print("STRATÉGIE B: ORB RETEST (Opening Range Breakout)")
    print("="*100)
    
    strategy_b = StrategyB_ORBRetest(retest_window_hours=2)
    trades_b = engine.run_strategy(strategy_b)
    perf_b = engine.generate_performance_report(trades_b, "ORB Retest")
    
    all_results['Strategy B'] = perf_b
    all_trades['Strategy B'] = trades_b
    
    print("\n📊 RÉSULTATS DÉTAILLÉS:")
    print(f"  Trades totaux: {perf_b['total_trades']}")
    print(f"  Trades gagnants: {perf_b['winning_trades']}")
    print(f"  Trades perdants: {perf_b['losing_trades']}")
    print(f"  Win Rate: {perf_b['win_rate']:.2f}%")
    print(f"  Gain moyen: {perf_b['avg_win']:.2f} points")
    print(f"  Perte moyenne: {perf_b['avg_loss']:.2f} points")
    print(f"  Profit Factor: {perf_b['profit_factor']:.2f}")
    print(f"  P&L Total: {perf_b['total_pnl']:.2f} points")
    print(f"  R:R Moyen Réalisé: {perf_b['avg_risk_reward']:.2f}")
    print(f"  Max pertes consécutives: {perf_b['max_consecutive_losses']}")
    
    if trades_b:
        df_trades_b = pd.DataFrame(trades_b)
        print(f"\n📈 STATISTIQUES PAR ANNÉE:")
        df_trades_b['year'] = pd.to_datetime(df_trades_b['date']).dt.year
        yearly_stats = df_trades_b.groupby('year').agg({
            'result': lambda x: (x == 'WIN').sum(),
            'pnl_points': ['count', 'sum']
        })
        for year in yearly_stats.index:
            wins = yearly_stats.loc[year, ('result', '<lambda>')]
            total = yearly_stats.loc[year, ('pnl_points', 'count')]
            pnl = yearly_stats.loc[year, ('pnl_points', 'sum')]
            wr = (wins/total*100) if total > 0 else 0
            print(f"  {year}: {total} trades, {wins} wins ({wr:.1f}%), P&L: {pnl:.2f} pts")
    
    # =========================================================================
    # STRATEGY C: HTF CONTINUATION
    # =========================================================================
    print("\n" + "="*100)
    print("STRATÉGIE C: HTF CONTINUATION (Fibonacci OTE)")
    print("="*100)
    
    strategy_c = StrategyC_HTFContinuation(ote_low=0.618, ote_high=0.79)
    trades_c = engine.run_strategy(strategy_c)
    perf_c = engine.generate_performance_report(trades_c, "HTF Continuation")
    
    all_results['Strategy C'] = perf_c
    all_trades['Strategy C'] = trades_c
    
    print("\n📊 RÉSULTATS DÉTAILLÉS:")
    print(f"  Trades totaux: {perf_c['total_trades']}")
    print(f"  Trades gagnants: {perf_c['winning_trades']}")
    print(f"  Trades perdants: {perf_c['losing_trades']}")
    print(f"  Win Rate: {perf_c['win_rate']:.2f}%")
    print(f"  Gain moyen: {perf_c['avg_win']:.2f} points")
    print(f"  Perte moyenne: {perf_c['avg_loss']:.2f} points")
    print(f"  Profit Factor: {perf_c['profit_factor']:.2f}")
    print(f"  P&L Total: {perf_c['total_pnl']:.2f} points")
    print(f"  R:R Moyen Réalisé: {perf_c['avg_risk_reward']:.2f}")
    print(f"  Max pertes consécutives: {perf_c['max_consecutive_losses']}")
    
    if trades_c:
        df_trades_c = pd.DataFrame(trades_c)
        print(f"\n📈 STATISTIQUES PAR ANNÉE:")
        df_trades_c['year'] = pd.to_datetime(df_trades_c['date']).dt.year
        yearly_stats = df_trades_c.groupby('year').agg({
            'result': lambda x: (x == 'WIN').sum(),
            'pnl_points': ['count', 'sum']
        })
        for year in yearly_stats.index:
            wins = yearly_stats.loc[year, ('result', '<lambda>')]
            total = yearly_stats.loc[year, ('pnl_points', 'count')]
            pnl = yearly_stats.loc[year, ('pnl_points', 'sum')]
            wr = (wins/total*100) if total > 0 else 0
            print(f"  {year}: {total} trades, {wins} wins ({wr:.1f}%), P&L: {pnl:.2f} pts")
    
    # =========================================================================
    # COMPARAISON GLOBALE
    # =========================================================================
    print("\n" + "="*100)
    print("COMPARAISON GLOBALE DES TROIS STRATÉGIES")
    print("="*100 + "\n")
    
    comparison_df = pd.DataFrame([perf_a, perf_b, perf_c])
    comparison_df.index = ['Strategy A: Judas Swing', 'Strategy B: ORB Retest', 'Strategy C: HTF Continuation']
    
    print(comparison_df[['total_trades', 'win_rate', 'profit_factor', 'total_pnl', 'avg_risk_reward']].to_string())
    
    # =========================================================================
    # MEILLEURE STRATÉGIE
    # =========================================================================
    print("\n" + "="*100)
    print("ANALYSE & RECOMMANDATIONS")
    print("="*100)
    
    best_wr = max(perf_a['win_rate'], perf_b['win_rate'], perf_c['win_rate'])
    best_pf = max(perf_a['profit_factor'], perf_b['profit_factor'], perf_c['profit_factor'])
    best_pnl = max(perf_a['total_pnl'], perf_b['total_pnl'], perf_c['total_pnl'])
    
    print(f"\n🏆 MEILLEURES PERFORMANCES:")
    
    if perf_a['win_rate'] == best_wr:
        print(f"  Win Rate: Strategy A (Judas Swing) - {best_wr:.2f}%")
    elif perf_b['win_rate'] == best_wr:
        print(f"  Win Rate: Strategy B (ORB Retest) - {best_wr:.2f}%")
    else:
        print(f"  Win Rate: Strategy C (HTF Continuation) - {best_wr:.2f}%")
    
    if perf_a['profit_factor'] == best_pf:
        print(f"  Profit Factor: Strategy A (Judas Swing) - {best_pf:.2f}")
    elif perf_b['profit_factor'] == best_pf:
        print(f"  Profit Factor: Strategy B (ORB Retest) - {best_pf:.2f}")
    else:
        print(f"  Profit Factor: Strategy C (HTF Continuation) - {best_pf:.2f}")
    
    if perf_a['total_pnl'] == best_pnl:
        print(f"  P&L Total: Strategy A (Judas Swing) - {best_pnl:.2f} points")
    elif perf_b['total_pnl'] == best_pnl:
        print(f"  P&L Total: Strategy B (ORB Retest) - {best_pnl:.2f} points")
    else:
        print(f"  P&L Total: Strategy C (HTF Continuation) - {best_pnl:.2f} points")
    
    print("\n💡 RECOMMANDATIONS:")
    print("  1. Les résultats sont basés sur des données historiques (2018-2025)")
    print("  2. Aucun slippage ni commission n'est inclus dans ces résultats")
    print("  3. Testez toujours en paper trading avant d'utiliser de l'argent réel")
    print("  4. Adaptez la taille de position selon votre capital et tolérance au risque")
    print("  5. Considérez utiliser plusieurs stratégies en parallèle pour diversifier")
    
    # Save detailed results
    print("\n" + "="*100)
    print("SAUVEGARDE DES RÉSULTATS")
    print("="*100)
    
    # Save trades
    for name, trades in all_trades.items():
        if trades:
            filename = f"real_results_{name.replace(' ', '_').lower()}.csv"
            pd.DataFrame(trades).to_csv(filename, index=False)
            print(f"✓ {filename}")
    
    # Save summary
    comparison_df.to_csv('real_results_summary.csv')
    print("✓ real_results_summary.csv")
    
    print("\n" + "="*100)
    print("BACKTEST COMPLET TERMINÉ")
    print("="*100)
    
    return all_results, all_trades


if __name__ == "__main__":
    results, trades = run_comprehensive_backtest()
