"""
Résultats Réels des Stratégies London Killzone sur NQ
Backtest complet sur données 2018-2025
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
    BacktestEngine
)


def run_fast_backtest():
    """Run backtest with progress indicators."""
    
    print("="*100)
    print("RÉSULTATS RÉELS - STRATÉGIES LONDON KILLZONE SUR NQ (2018-2025)")
    print("="*100)
    print()
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
    files_5m = [os.path.join(base_path, f"{year} 5m.csv") for year in years if os.path.exists(os.path.join(base_path, f"{year} 5m.csv"))]
    files_4h = [os.path.join(base_path, f"{year} 4H.csv") for year in years if os.path.exists(os.path.join(base_path, f"{year} 4H.csv"))]
    
    print("📁 CHARGEMENT DES DONNÉES...")
    df_5m = DataLoader.load_multiple_files(files_5m)
    df_4h = DataLoader.load_multiple_files(files_4h) if files_4h else None
    
    print(f"✓ {len(df_5m):,} bougies 5m chargées ({pd.Series(df_5m.index.date).nunique():,} jours)")
    print(f"  Période: {df_5m.index.min()} → {df_5m.index.max()}")
    
    df_5m = TimeManager.convert_to_paris_time(df_5m)
    if df_4h is not None:
        df_4h = TimeManager.convert_to_paris_time(df_4h)
    
    engine = BacktestEngine(df_5m, df_4h)
    results = {}
    
    # =========================================================================
    # STRATEGY A
    # =========================================================================
    print("\n" + "="*100)
    print("STRATÉGIE A: JUDAS SWING (Chasse aux Liquidités)")
    print("="*100)
    
    strategy_a = StrategyA_JudasSwing(points_offset=5.0, risk_reward=3.0)
    trades_a = engine.run_strategy(strategy_a)
    perf_a = engine.generate_performance_report(trades_a, "Judas Swing")
    results['A'] = (perf_a, trades_a)
    
    print(f"\n💰 P&L Total: {perf_a['total_pnl']:.2f} points")
    print(f"📊 Win Rate: {perf_a['win_rate']:.2f}%")
    print(f"📈 Profit Factor: {perf_a['profit_factor']:.2f}")
    print(f"🎯 Trades: {perf_a['total_trades']} ({perf_a['winning_trades']} wins, {perf_a['losing_trades']} pertes)")
    
    if trades_a:
        df_a = pd.DataFrame(trades_a)
        df_a['year'] = pd.to_datetime(df_a['date']).dt.year
        print("\nPar année:")
        for year in sorted(df_a['year'].unique()):
            year_data = df_a[df_a['year'] == year]
            wins = (year_data['result'] == 'WIN').sum()
            pnl = year_data['pnl_points'].sum()
            print(f"  {year}: {len(year_data)} trades, {wins} wins ({wins/len(year_data)*100:.1f}%), P&L: {pnl:+.2f} pts")
    
    # =========================================================================
    # STRATEGY B
    # =========================================================================
    print("\n" + "="*100)
    print("STRATÉGIE B: ORB RETEST (Opening Range Breakout)")
    print("="*100)
    
    strategy_b = StrategyB_ORBRetest()
    trades_b = engine.run_strategy(strategy_b)
    perf_b = engine.generate_performance_report(trades_b, "ORB Retest")
    results['B'] = (perf_b, trades_b)
    
    print(f"\n💰 P&L Total: {perf_b['total_pnl']:.2f} points")
    print(f"📊 Win Rate: {perf_b['win_rate']:.2f}%")
    print(f"📈 Profit Factor: {perf_b['profit_factor']:.2f}")
    print(f"🎯 Trades: {perf_b['total_trades']} ({perf_b['winning_trades']} wins, {perf_b['losing_trades']} pertes)")
    
    if trades_b:
        df_b = pd.DataFrame(trades_b)
        df_b['year'] = pd.to_datetime(df_b['date']).dt.year
        print("\nPar année:")
        for year in sorted(df_b['year'].unique()):
            year_data = df_b[df_b['year'] == year]
            wins = (year_data['result'] == 'WIN').sum()
            pnl = year_data['pnl_points'].sum()
            print(f"  {year}: {len(year_data)} trades, {wins} wins ({wins/len(year_data)*100:.1f}%), P&L: {pnl:+.2f} pts")
    
    # =========================================================================
    # STRATEGY C - Optimized (every other year for speed)
    # =========================================================================
    print("\n" + "="*100)
    print("STRATÉGIE C: HTF CONTINUATION (Fibonacci OTE) - Sample")
    print("="*100)
    print("Note: Testée sur échantillon pour optimiser le temps de calcul")
    
    strategy_c = StrategyC_HTFContinuation()
    # Run on sample (2020, 2022, 2024)
    sample_years = ['2020', '2022', '2024']
    trades_c_sample = []
    
    for year in sample_years:
        trades_year = engine.run_strategy(strategy_c, f"{year}-01-01", f"{year}-12-31")
        trades_c_sample.extend(trades_year)
    
    if trades_c_sample:
        perf_c = engine.generate_performance_report(trades_c_sample, "HTF Continuation")
        results['C'] = (perf_c, trades_c_sample)
        
        print(f"\n💰 P&L Total (sample): {perf_c['total_pnl']:.2f} points")
        print(f"📊 Win Rate: {perf_c['win_rate']:.2f}%")
        print(f"📈 Profit Factor: {perf_c['profit_factor']:.2f}")
        print(f"🎯 Trades: {perf_c['total_trades']} ({perf_c['winning_trades']} wins, {perf_c['losing_trades']} pertes)")
        
        df_c = pd.DataFrame(trades_c_sample)
        df_c['year'] = pd.to_datetime(df_c['date']).dt.year
        print("\nPar année (sample):")
        for year in sorted(df_c['year'].unique()):
            year_data = df_c[df_c['year'] == int(year)]
            wins = (year_data['result'] == 'WIN').sum()
            pnl = year_data['pnl_points'].sum()
            print(f"  {year}: {len(year_data)} trades, {wins} wins ({wins/len(year_data)*100:.1f}%), P&L: {pnl:+.2f} pts")
    
    # =========================================================================
    # COMPARAISON
    # =========================================================================
    print("\n" + "="*100)
    print("COMPARAISON GLOBALE")
    print("="*100)
    
    comparison = []
    for name, (perf, _) in results.items():
        comparison.append({
            'Stratégie': f"Strategy {name}",
            'Trades': perf['total_trades'],
            'Win Rate (%)': f"{perf['win_rate']:.1f}",
            'Profit Factor': f"{perf['profit_factor']:.2f}",
            'P&L Total (pts)': f"{perf['total_pnl']:.2f}",
            'Avg R:R': f"{perf['avg_risk_reward']:.2f}"
        })
    
    df_comp = pd.DataFrame(comparison)
    print("\n" + df_comp.to_string(index=False))
    
    # =========================================================================
    # RECOMMANDATIONS
    # =========================================================================
    print("\n" + "="*100)
    print("ANALYSE & RECOMMANDATIONS")
    print("="*100)
    
    best_strategy = max(results.items(), key=lambda x: x[1][0]['total_pnl'])
    print(f"\n🏆 Meilleure stratégie (P&L): Strategy {best_strategy[0]}")
    print(f"   P&L Total: {best_strategy[1][0]['total_pnl']:.2f} points")
    print(f"   Win Rate: {best_strategy[1][0]['win_rate']:.2f}%")
    print(f"   Profit Factor: {best_strategy[1][0]['profit_factor']:.2f}")
    
    print("\n⚠️  NOTES IMPORTANTES:")
    print("   • Ces résultats sont basés sur des données historiques (backtest)")
    print("   • Aucun slippage ni commission inclus")
    print("   • Performance passée ≠ performance future")
    print("   • Toujours tester en paper trading d'abord")
    print("   • Adapter la taille de position à votre capital et risque")
    
    # Save results
    print("\n" + "="*100)
    print("SAUVEGARDE DES RÉSULTATS")
    print("="*100)
    
    for name, (perf, trades) in results.items():
        if trades:
            filename = f"real_results_strategy_{name.lower()}.csv"
            pd.DataFrame(trades).to_csv(filename, index=False)
            print(f"✓ {filename}")
    
    df_comp.to_csv('real_results_comparison.csv', index=False)
    print("✓ real_results_comparison.csv")
    
    print("\n" + "="*100)
    print("BACKTEST TERMINÉ ✓")
    print("="*100)
    
    return results


if __name__ == "__main__":
    results = run_fast_backtest()
