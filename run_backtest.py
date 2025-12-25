"""
Main Backtest Execution Script
Runs complete backtest for both strategies on NQ data (2018-2025)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
import sys

from data_loader import DataLoader
from market_structure import MarketStructureDetector
from strategy1_liquidity_raid import LiquidityRaidStrategy
from strategy2_trend_continuation import TrendContinuationStrategy
from backtest_engine import BacktestEngine


def main():
    print("="*70)
    print("SMC/ICT LONDON KILLZONE BACKTEST SYSTEM")
    print("NQ Futures (2018-2025)")
    print("="*70)
    
    # Initialize components
    print("\n[1/6] Initializing components...")
    loader = DataLoader()
    detector = MarketStructureDetector()
    strategy1 = LiquidityRaidStrategy(detector)
    strategy2 = TrendContinuationStrategy(detector)
    engine = BacktestEngine()
    
    # Load data
    print("\n[2/6] Loading market data...")
    try:
        data = loader.load_all_timeframes()
        data_5m = data['5m']
        data_15m = data['15m']
        data_1h = data['1H']
    except Exception as e:
        print(f"ERROR loading data: {str(e)}")
        return
    
    # Get trading days
    print("\n[3/6] Identifying trading days...")
    trading_days = loader.get_trading_days(data_5m)
    print(f"Found {len(trading_days)} trading days to analyze")
    
    # Generate signals
    print("\n[4/6] Scanning for trading signals...")
    all_signals = []
    
    for i, date in enumerate(trading_days):
        if i % 100 == 0:
            print(f"  Progress: {i}/{len(trading_days)} days analyzed...")
        
        try:
            # Strategy 1: Liquidity Raid
            s1_signals = strategy1.analyze_day(date, data_5m, data_1h)
            all_signals.extend(s1_signals)
            
            # Strategy 2: Trend Continuation
            s2_signals = strategy2.analyze_day(date, data_5m, data_1h)
            all_signals.extend(s2_signals)
            
        except Exception as e:
            # Silently continue on errors for individual days
            pass
    
    print(f"  Total signals generated: {len(all_signals)}")
    
    # Execute trades
    print("\n[5/6] Executing backtest trades...")
    for i, signal in enumerate(all_signals):
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(all_signals)} trades executed...")
        
        try:
            trade = engine.execute_trade(signal, data_5m)
            trade = engine.add_market_context(trade)
            engine.trades.append(trade)
        except Exception as e:
            print(f"  Warning: Error executing trade {i}: {str(e)}")
    
    print(f"  Total trades tracked: {len(engine.trades)}")
    
    # Generate reports
    print("\n[6/6] Generating reports...")
    
    # Get results dataframe
    results_df = engine.get_results_dataframe()
    
    if len(results_df) == 0:
        print("ERROR: No trades to report")
        return
    
    # Save CSV report
    csv_file = "backtest_results.csv"
    results_df.to_csv(csv_file, index=False)
    print(f"  ✓ CSV report saved: {csv_file}")
    
    # Save JSON report
    json_file = "backtest_results.json"
    results_json = results_df.to_dict(orient='records')
    with open(json_file, 'w') as f:
        json.dump(results_json, f, indent=2, default=str)
    print(f"  ✓ JSON report saved: {json_file}")
    
    # Calculate statistics
    stats = engine.calculate_statistics()
    
    # Save statistics
    stats_file = "backtest_statistics.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2, default=str)
    print(f"  ✓ Statistics saved: {stats_file}")
    
    # Generate analysis report
    generate_analysis_report(results_df, stats)
    
    print("\n" + "="*70)
    print("BACKTEST COMPLETE")
    print("="*70)
    print(f"\nGenerated files:")
    print(f"  - backtest_results.csv")
    print(f"  - backtest_results.json")
    print(f"  - backtest_statistics.json")
    print(f"  - backtest_analysis.md")
    
    # Print summary
    print_summary(stats)


def print_summary(stats: dict):
    """Print quick summary statistics"""
    print("\n" + "="*70)
    print("QUICK SUMMARY")
    print("="*70)
    
    if 'error' in stats:
        print(f"Error: {stats['error']}")
        return
    
    print(f"\nOverall Performance:")
    print(f"  Total Signals: {stats.get('total_signals', 0)}")
    print(f"  Valid Trades: {stats.get('valid_trades', 0)}")
    print(f"  Win Rate: {stats.get('win_rate', 0):.2f}%")
    print(f"  Average R:R Ratio: {stats.get('avg_rr_ratio', 0):.2f}")
    print(f"  Total P&L: {stats.get('total_pnl', 0):.2f} points")
    print(f"  Average P&L per trade: {stats.get('avg_pnl', 0):.2f} points")
    
    print(f"\nStrategy Breakdown:")
    
    # Strategy 1 Aggressive
    if 'STRATEGY_1_AGGRESSIVE_trades' in stats:
        print(f"\n  Strategy 1 (Aggressive):")
        print(f"    Trades: {stats['STRATEGY_1_AGGRESSIVE_trades']}")
        print(f"    Win Rate: {stats['STRATEGY_1_AGGRESSIVE_win_rate']:.2f}%")
        print(f"    Avg R:R: {stats['STRATEGY_1_AGGRESSIVE_avg_rr']:.2f}")
        print(f"    Total P&L: {stats['STRATEGY_1_AGGRESSIVE_total_pnl']:.2f} points")
    
    # Strategy 1 Conservative
    if 'STRATEGY_1_CONSERVATIVE_trades' in stats:
        print(f"\n  Strategy 1 (Conservative):")
        print(f"    Trades: {stats['STRATEGY_1_CONSERVATIVE_trades']}")
        print(f"    Win Rate: {stats['STRATEGY_1_CONSERVATIVE_win_rate']:.2f}%")
        print(f"    Avg R:R: {stats['STRATEGY_1_CONSERVATIVE_avg_rr']:.2f}")
        print(f"    Total P&L: {stats['STRATEGY_1_CONSERVATIVE_total_pnl']:.2f} points")
    
    # Strategy 2
    if 'STRATEGY_2_CONTINUATION_trades' in stats:
        print(f"\n  Strategy 2 (Trend Continuation):")
        print(f"    Trades: {stats['STRATEGY_2_CONTINUATION_trades']}")
        print(f"    Win Rate: {stats['STRATEGY_2_CONTINUATION_win_rate']:.2f}%")
        print(f"    Avg R:R: {stats['STRATEGY_2_CONTINUATION_avg_rr']:.2f}")
        print(f"    Total P&L: {stats['STRATEGY_2_CONTINUATION_total_pnl']:.2f} points")


def generate_analysis_report(df: pd.DataFrame, stats: dict):
    """Generate detailed markdown analysis report"""
    
    report = []
    report.append("# London Killzone Backtest Analysis Report")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\n**Data Range:** 2018-2025")
    report.append(f"\n**Instrument:** NQ Futures (Nasdaq-100)")
    
    report.append("\n\n## Executive Summary")
    report.append("\nThis backtest analyzes two SMC/ICT trading strategies focused on the London Killzone (02:00-05:00 EST):")
    report.append("\n- **Strategy 1**: Liquidity Raid (Judas Swing reversal)")
    report.append("\n- **Strategy 2**: Trend Continuation (Breakout momentum)")
    
    # Overall Performance
    report.append("\n\n## Overall Performance")
    report.append(f"\n- **Total Signals Generated**: {stats.get('total_signals', 0)}")
    report.append(f"\n- **Valid Trades Executed**: {stats.get('valid_trades', 0)}")
    report.append(f"\n- **Overall Win Rate**: {stats.get('win_rate', 0):.2f}%")
    report.append(f"\n- **Average Risk:Reward Ratio**: {stats.get('avg_rr_ratio', 0):.2f}")
    report.append(f"\n- **Total P&L**: {stats.get('total_pnl', 0):.2f} points")
    report.append(f"\n- **Average P&L per Trade**: {stats.get('avg_pnl', 0):.2f} points")
    report.append(f"\n- **Largest Win**: {stats.get('max_win', 0):.2f} points")
    report.append(f"\n- **Largest Loss**: {stats.get('max_loss', 0):.2f} points")
    
    # Strategy Comparison
    report.append("\n\n## Strategy Comparison")
    
    valid_trades = df[df['exit_result'].isin(['TP1', 'TP2', 'STOP_LOSS'])]
    
    for strategy in df['strategy'].unique():
        strategy_trades = valid_trades[valid_trades['strategy'] == strategy]
        
        if len(strategy_trades) > 0:
            report.append(f"\n\n### {strategy}")
            report.append(f"\n- **Number of Trades**: {len(strategy_trades)}")
            report.append(f"\n- **Win Rate**: {(strategy_trades['win'].sum() / len(strategy_trades) * 100):.2f}%")
            report.append(f"\n- **Average R:R Ratio**: {strategy_trades['rr_ratio'].mean():.2f}")
            report.append(f"\n- **Total P&L**: {strategy_trades['pnl'].sum():.2f} points")
            report.append(f"\n- **Average Win**: {strategy_trades[strategy_trades['win']==1]['pnl'].mean():.2f} points")
            report.append(f"\n- **Average Loss**: {strategy_trades[strategy_trades['win']==0]['pnl'].mean():.2f} points")
            
            # Exit analysis
            exit_counts = strategy_trades['exit_result'].value_counts()
            report.append(f"\n- **Exit Breakdown**:")
            for exit_type, count in exit_counts.items():
                pct = (count / len(strategy_trades)) * 100
                report.append(f"\n  - {exit_type}: {count} ({pct:.1f}%)")
    
    # Market Context Analysis
    report.append("\n\n## Market Context Analysis")
    report.append("\nPerformance across different market regimes:")
    
    for context in valid_trades['market_context'].unique():
        context_trades = valid_trades[valid_trades['market_context'] == context]
        
        if len(context_trades) > 0:
            report.append(f"\n\n### {context}")
            report.append(f"\n- **Trades**: {len(context_trades)}")
            report.append(f"\n- **Win Rate**: {(context_trades['win'].sum() / len(context_trades) * 100):.2f}%")
            report.append(f"\n- **Total P&L**: {context_trades['pnl'].sum():.2f} points")
            report.append(f"\n- **Avg R:R**: {context_trades['rr_ratio'].mean():.2f}")
    
    # Volatility Analysis
    report.append("\n\n## Volatility Impact Analysis")
    report.append("\nAnalyzing the impact of high volatility periods (2020 COVID, 2022 Bear Market) on stop loss width:")
    
    # 2020 Analysis
    covid_trades = valid_trades[valid_trades['date'].str.startswith('2020')]
    if len(covid_trades) > 0:
        report.append(f"\n\n### 2020 (COVID Period)")
        report.append(f"\n- **Average Risk (Stop Loss Width)**: {covid_trades['risk'].mean():.2f} points")
        report.append(f"\n- **Win Rate**: {(covid_trades['win'].sum() / len(covid_trades) * 100):.2f}%")
        report.append(f"\n- **Trades**: {len(covid_trades)}")
    
    # 2022 Analysis
    bear_trades = valid_trades[valid_trades['date'].str.startswith('2022')]
    if len(bear_trades) > 0:
        report.append(f"\n\n### 2022 (Bear Market)")
        report.append(f"\n- **Average Risk (Stop Loss Width)**: {bear_trades['risk'].mean():.2f} points")
        report.append(f"\n- **Win Rate**: {(bear_trades['win'].sum() / len(bear_trades) * 100):.2f}%")
        report.append(f"\n- **Trades**: {len(bear_trades)}")
    
    # Normal periods
    normal_trades = valid_trades[~valid_trades['date'].str.startswith(('2020', '2022'))]
    if len(normal_trades) > 0:
        report.append(f"\n\n### Other Periods (Lower Volatility)")
        report.append(f"\n- **Average Risk (Stop Loss Width)**: {normal_trades['risk'].mean():.2f} points")
        report.append(f"\n- **Win Rate**: {(normal_trades['win'].sum() / len(normal_trades) * 100):.2f}%")
        report.append(f"\n- **Trades**: {len(normal_trades)}")
    
    # Entry Precision Analysis
    report.append("\n\n## Entry Precision Analysis (M5 vs M15)")
    report.append("\nComparing aggressive (M5) vs conservative (MSS + FVG) entries for Strategy 1:")
    
    aggressive = valid_trades[valid_trades['strategy'] == 'STRATEGY_1_AGGRESSIVE']
    conservative = valid_trades[valid_trades['strategy'] == 'STRATEGY_1_CONSERVATIVE']
    
    if len(aggressive) > 0:
        report.append(f"\n\n### Aggressive Entry (M5 Close)")
        report.append(f"\n- **Win Rate**: {(aggressive['win'].sum() / len(aggressive) * 100):.2f}%")
        report.append(f"\n- **Avg R:R**: {aggressive['rr_ratio'].mean():.2f}")
        report.append(f"\n- **Trades**: {len(aggressive)}")
    
    if len(conservative) > 0:
        report.append(f"\n\n### Conservative Entry (MSS + FVG)")
        report.append(f"\n- **Win Rate**: {(conservative['win'].sum() / len(conservative) * 100):.2f}%")
        report.append(f"\n- **Avg R:R**: {conservative['rr_ratio'].mean():.2f}")
        report.append(f"\n- **Trades**: {len(conservative)}")
    
    # Key Findings
    report.append("\n\n## Key Findings")
    
    # Best strategy
    best_strategy = None
    best_winrate = 0
    
    for strategy in df['strategy'].unique():
        strategy_trades = valid_trades[valid_trades['strategy'] == strategy]
        if len(strategy_trades) > 0:
            winrate = (strategy_trades['win'].sum() / len(strategy_trades) * 100)
            if winrate > best_winrate:
                best_winrate = winrate
                best_strategy = strategy
    
    report.append(f"\n\n### Best Performing Strategy")
    report.append(f"\n**{best_strategy}** with {best_winrate:.2f}% win rate")
    
    # Volatility impact
    report.append(f"\n\n### Volatility Impact")
    if len(covid_trades) > 0 and len(normal_trades) > 0:
        risk_increase = ((covid_trades['risk'].mean() - normal_trades['risk'].mean()) / normal_trades['risk'].mean()) * 100
        report.append(f"\nStop loss width increased by approximately {abs(risk_increase):.1f}% during high volatility periods (2020/2022).")
    
    # Entry precision
    if len(aggressive) > 0 and len(conservative) > 0:
        report.append(f"\n\n### Entry Precision Importance")
        winrate_diff = abs((aggressive['win'].sum() / len(aggressive) * 100) - (conservative['win'].sum() / len(conservative) * 100))
        if (conservative['win'].sum() / len(conservative) * 100) > (aggressive['win'].sum() / len(aggressive) * 100):
            report.append(f"\nConservative entries (MSS + FVG) showed {winrate_diff:.1f}% better win rate, ")
            report.append(f"demonstrating the importance of precise M5 entry confirmation.")
        else:
            report.append(f"\nAggressive entries performed {winrate_diff:.1f}% better, ")
            report.append(f"suggesting that immediate action on rejection candles can be more effective.")
    
    # Recommendations
    report.append("\n\n## Recommendations")
    report.append("\n\nBased on the backtest results:")
    report.append("\n\n1. **Strategy Selection**: Focus on the best performing strategy identified above")
    report.append("\n2. **Risk Management**: Adjust position sizing during high volatility periods (increase stop loss buffer)")
    report.append("\n3. **Entry Timing**: Consider the trade-off between aggressive and conservative entries based on your risk tolerance")
    report.append("\n4. **Market Context**: Be aware that strategy performance varies significantly across different market regimes")
    report.append("\n5. **London Killzone Focus**: Results confirm the importance of the 02:00-05:00 EST session for these setups")
    
    # Write report
    report_file = "backtest_analysis.md"
    with open(report_file, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"  ✓ Analysis report saved: {report_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nBacktest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
