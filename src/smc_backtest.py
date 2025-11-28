"""
SMC Backtest Main Script

Smart Money Concepts (SMC) backtesting system for Nasdaq trading.
Uses 15-minute and 5-minute timeframes to identify:
- Accumulation phases
- Liquidity sweeps
- Fair Value Gaps (FVG)
- Entry signals based on FVG breaks

Author: Backtest-Trading System
"""

import os
import sys
import pandas as pd
import numpy as np
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from detectors import find_valid_entries, detect_fvg, detect_liquidity_sweep, filter_entries_by_session
from trade_manager import TradeManager, Trade, TradeStatus


def load_config(config_path: str = None) -> Dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file (default: config/settings.yaml)
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / 'config' / 'settings.yaml'
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def load_csv_data(filepath: str, separator: str = ';') -> pd.DataFrame:
    """
    Load CSV data file.
    
    Args:
        filepath: Path to CSV file
        separator: CSV separator (default: ';')
        
    Returns:
        DataFrame with OHLC data
    """
    # Read CSV
    df = pd.read_csv(filepath, sep=separator)
    
    # Rename columns
    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    # Create datetime index
    df['DateTime'] = pd.to_datetime(
        df['Date'] + ' ' + df['Time'],
        format='%d/%m/%Y %H:%M:%S'
    )
    df.set_index('DateTime', inplace=True)
    
    # Convert to numeric
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Sort by datetime
    df.sort_index(inplace=True)
    
    return df


def load_year_data(year: int, base_path: str = None) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Load 15m and 5m data for a specific year.
    
    Args:
        year: Year to load
        base_path: Base directory path (default: repository root)
        
    Returns:
        Tuple of (df_15m, df_5m)
    """
    if base_path is None:
        base_path = Path(__file__).parent.parent
    else:
        base_path = Path(base_path)
    
    path_15m = base_path / f'{year} 15m.csv'
    path_5m = base_path / f'{year} 5m.csv'
    
    df_15m = None
    df_5m = None
    
    if path_15m.exists():
        try:
            df_15m = load_csv_data(str(path_15m))
            print(f"  Loaded {year} 15m data: {len(df_15m)} candles")
        except Exception as e:
            print(f"  Error loading {year} 15m data: {e}")
    else:
        print(f"  Warning: {path_15m} not found")
    
    if path_5m.exists():
        try:
            df_5m = load_csv_data(str(path_5m))
            print(f"  Loaded {year} 5m data: {len(df_5m)} candles")
        except Exception as e:
            print(f"  Error loading {year} 5m data: {e}")
    else:
        print(f"  Warning: {path_5m} not found")
    
    return df_15m, df_5m


def run_backtest(config: Dict, base_path: str = None, verbose: bool = True) -> TradeManager:
    """
    Run the SMC backtest.
    
    Args:
        config: Configuration dictionary
        base_path: Base path for data files
        verbose: Print progress information
        
    Returns:
        TradeManager with all trades
    """
    trade_manager = TradeManager(config)
    years = config.get('data', {}).get('years', list(range(2018, 2026)))
    
    if verbose:
        print("=" * 60)
        print("SMC Backtesting System")
        print("=" * 60)
        print(f"\nProcessing years: {years}")
        print("-" * 60)
    
    total_entries = 0
    
    for year in years:
        if verbose:
            print(f"\n[{year}] Loading data...")
        
        df_15m, df_5m = load_year_data(year, base_path)
        
        if df_15m is None or df_5m is None:
            if verbose:
                print(f"[{year}] Skipping - missing data files")
            continue
        
        if verbose:
            print(f"[{year}] Finding entry signals...")
        
        # Find valid entries
        entries = find_valid_entries(df_15m, df_5m, config)
        
        # Filter entries by trading sessions (London 02:00-05:00, New York 08:30-11:00)
        entries = filter_entries_by_session(entries, config)
        
        if verbose:
            print(f"[{year}] Found {len(entries)} potential entries (filtered by session)")
        
        # Open trades for each entry
        trades_opened = 0
        for entry in entries:
            trade = trade_manager.open_trade(entry)
            if trade:
                trades_opened += 1
        
        if verbose:
            print(f"[{year}] Opened {trades_opened} trades (max per day limit applied)")
        
        total_entries += trades_opened
        
        # Process all 5m candles to update trades
        if verbose:
            print(f"[{year}] Processing candles for trade management...")
        
        for idx in range(len(df_5m)):
            candle = df_5m.iloc[idx]
            trade_manager.process_candle(candle)
    
    if verbose:
        print("\n" + "=" * 60)
        print(f"Total entries processed: {total_entries}")
        print("=" * 60)
    
    return trade_manager


def generate_report(trade_manager: TradeManager, config: Dict, output_path: str = None):
    """
    Generate the strategy report.
    
    Args:
        trade_manager: TradeManager with completed backtest
        config: Configuration dictionary
        output_path: Path to save report (default: analysis/STRATEGY_REPORT.md)
    """
    if output_path is None:
        output_path = Path(__file__).parent.parent / 'analysis' / 'STRATEGY_REPORT.md'
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(exist_ok=True)
    
    results = trade_manager.get_results()
    results_by_year = trade_manager.get_results_by_year()
    results_by_type = trade_manager.get_results_by_type()
    rr_ratios = config.get('risk_management', {}).get('risk_reward_ratios', [1.0, 1.5, 2.0])
    
    report = []
    report.append("# SMC Strategy Backtesting Report")
    report.append("")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append("---")
    report.append("")
    
    # Strategy Description
    report.append("## 1. Strategy Description")
    report.append("")
    report.append("### Timeframes")
    report.append("- **15 minutes**: Trend identification and liquidity sweep detection")
    report.append("- **5 minutes**: FVG detection and entry confirmation")
    report.append("")
    report.append("### Entry Conditions")
    report.append("1. **Accumulation Phase**: Price consolidation on 15m timeframe")
    report.append("2. **Liquidity Sweep**: Temporary breakout beyond key level (15m and 5m)")
    report.append("3. **Fair Value Gap (FVG)**: Gap formation on 5m after sweep")
    report.append("4. **Entry Confirmation**:")
    report.append("   - **BUY**: Price closes ABOVE a bearish FVG")
    report.append("   - **SELL**: Price closes BELOW a bullish FVG")
    report.append("")
    report.append("### Risk Management")
    report.append("- **Stop-Loss**: Below/above confirmation candle or FVG")
    report.append(f"- **Take Profits**: RR ratios of {', '.join(f'1:{rr}' for rr in rr_ratios)}")
    report.append("")
    report.append("---")
    report.append("")
    
    # Global Statistics
    report.append("## 2. Global Statistics")
    report.append("")
    report.append(f"| Metric | Value |")
    report.append("|--------|-------|")
    report.append(f"| Total Trades | {results['total_trades']} |")
    report.append(f"| Winning Trades | {results['winning_trades']} |")
    report.append(f"| Losing Trades | {results['losing_trades']} |")
    report.append(f"| Win Rate | {results['win_rate']:.2f}% |")
    report.append(f"| Profit Factor | {results['profit_factor']:.2f} |")
    report.append(f"| Total P&L (points) | {results['total_pnl']:.2f} |")
    report.append(f"| Average Win (points) | {results['avg_win']:.2f} |")
    report.append(f"| Average Loss (points) | {results['avg_loss']:.2f} |")
    report.append("")
    
    # TP/SL Distribution
    report.append("### Take Profit / Stop Loss Distribution")
    report.append("")
    report.append(f"| Level | Count | Percentage |")
    report.append("|-------|-------|------------|")
    
    total = results['total_trades'] if results['total_trades'] > 0 else 1
    report.append(f"| TP1 (RR 1:{rr_ratios[0]}) | {results['tp1_count']} | {results['tp1_count']/total*100:.1f}% |")
    if len(rr_ratios) > 1:
        report.append(f"| TP2 (RR 1:{rr_ratios[1]}) | {results['tp2_count']} | {results['tp2_count']/total*100:.1f}% |")
    if len(rr_ratios) > 2:
        report.append(f"| TP3 (RR 1:{rr_ratios[2]}) | {results['tp3_count']} | {results['tp3_count']/total*100:.1f}% |")
    if len(rr_ratios) > 3:
        report.append(f"| TP4 (RR 1:{rr_ratios[3]}) | {results['tp4_count']} | {results['tp4_count']/total*100:.1f}% |")
    report.append(f"| Stop Loss | {results['sl_count']} | {results['sl_count']/total*100:.1f}% |")
    report.append("")
    report.append("---")
    report.append("")
    
    # Statistics by Year
    report.append("## 3. Statistics by Year (2018-2025)")
    report.append("")
    report.append("| Year | Total Trades | Wins | Losses | Win Rate | TP1 | TP2 | TP3 | TP4 | SL |")
    report.append("|------|-------------|------|--------|----------|-----|-----|-----|-----|-----|")
    
    for year in sorted(results_by_year.keys()):
        data = results_by_year[year]
        report.append(
            f"| {year} | {data['total_trades']} | {data['winning_trades']} | "
            f"{data['losing_trades']} | {data['win_rate']:.1f}% | "
            f"{data['tp1_count']} | {data['tp2_count']} | {data['tp3_count']} | {data['tp4_count']} | {data['sl_count']} |"
        )
    report.append("")
    report.append("---")
    report.append("")
    
    # Statistics by Trade Type
    report.append("## 4. Statistics by Trade Type (Long vs Short)")
    report.append("")
    report.append("| Type | Total Trades | Wins | Losses | Win Rate |")
    report.append("|------|-------------|------|--------|----------|")
    
    for trade_type, data in results_by_type.items():
        report.append(
            f"| {trade_type} | {data['total_trades']} | {data['wins']} | "
            f"{data['losses']} | {data['win_rate']:.1f}% |"
        )
    report.append("")
    report.append("---")
    report.append("")
    
    # Best/Worst Analysis
    report.append("## 5. Performance Analysis")
    report.append("")
    
    if results_by_year:
        best_year = max(results_by_year.items(), key=lambda x: x[1]['win_rate'])
        worst_year = min(results_by_year.items(), key=lambda x: x[1]['win_rate'])
        
        report.append(f"### Best Performing Year")
        report.append(f"- **{best_year[0]}**: {best_year[1]['win_rate']:.1f}% win rate "
                     f"({best_year[1]['winning_trades']} wins / {best_year[1]['total_trades']} total)")
        report.append("")
        report.append(f"### Worst Performing Year")
        report.append(f"- **{worst_year[0]}**: {worst_year[1]['win_rate']:.1f}% win rate "
                     f"({worst_year[1]['winning_trades']} wins / {worst_year[1]['total_trades']} total)")
    report.append("")
    report.append("---")
    report.append("")
    
    # Conclusions
    report.append("## 6. Conclusions and Recommendations")
    report.append("")
    
    if results['total_trades'] > 0:
        if results['win_rate'] >= 50:
            report.append("### Positive Observations")
            report.append(f"- The strategy shows a positive win rate of {results['win_rate']:.1f}%")
            if results['profit_factor'] > 1:
                report.append(f"- Profit factor of {results['profit_factor']:.2f} indicates profitable trading")
        else:
            report.append("### Areas for Improvement")
            report.append(f"- Win rate of {results['win_rate']:.1f}% suggests room for optimization")
            
        report.append("")
        report.append("### Key Metrics Summary")
        report.append(f"- **TP/SL Ratio**: {results['winning_trades']}:{results['losing_trades']}")
        
        # Calculate expected value
        if results['winning_trades'] > 0 and results['losing_trades'] > 0:
            avg_rr_win = results['total_pnl'] / results['winning_trades'] if results['winning_trades'] > 0 else 0
            ev = (results['win_rate']/100 * results['avg_win']) - ((100-results['win_rate'])/100 * results['avg_loss'])
            report.append(f"- **Expected Value per Trade**: {ev:.2f} points")
    else:
        report.append("No trades were generated during the backtest period.")
        report.append("")
        report.append("### Recommendations")
        report.append("- Review and adjust strategy parameters in config/settings.yaml")
        report.append("- Consider relaxing FVG detection thresholds")
        report.append("- Check liquidity sweep detection sensitivity")
    
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Report generated by SMC Backtesting System*")
    
    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"\nReport saved to: {output_path}")


def save_trades_csv(trade_manager: TradeManager, output_path: str = None):
    """
    Save all trades to CSV file.
    
    Args:
        trade_manager: TradeManager with completed backtest
        output_path: Path to save CSV
    """
    if output_path is None:
        output_path = Path(__file__).parent.parent / 'analysis' / 'trades_results.csv'
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(exist_ok=True)
    
    df = trade_manager.export_trades_to_df()
    df.to_csv(output_path, index=False)
    
    print(f"Trades saved to: {output_path}")


def main():
    """Main entry point for the backtest."""
    # Get base path
    base_path = Path(__file__).parent.parent
    
    print("\n" + "=" * 60)
    print("  SMC BACKTESTING SYSTEM")
    print("  Smart Money Concepts Strategy for Nasdaq")
    print("=" * 60)
    
    # Load configuration
    print("\nLoading configuration...")
    config = load_config()
    
    # Run backtest
    trade_manager = run_backtest(config, str(base_path), verbose=True)
    
    # Get and display results
    results = trade_manager.get_results()
    
    print("\n" + "=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"\n  Total Trades: {results['total_trades']}")
    print(f"  Winning Trades: {results['winning_trades']}")
    print(f"  Losing Trades: {results['losing_trades']}")
    print(f"  Win Rate: {results['win_rate']:.2f}%")
    print(f"  Profit Factor: {results['profit_factor']:.2f}")
    print(f"\n  TP1 (RR 1:1): {results['tp1_count']}")
    print(f"  TP2 (RR 1:1.5): {results['tp2_count']}")
    print(f"  TP3 (RR 1:2): {results['tp3_count']}")
    print(f"  TP4 (RR 1:2.5): {results['tp4_count']}")
    print(f"  Stop Loss: {results['sl_count']}")
    
    # Generate report
    print("\nGenerating report...")
    generate_report(trade_manager, config)
    
    # Save trades
    if config.get('output', {}).get('save_trades_csv', True):
        save_trades_csv(trade_manager)
    
    print("\n" + "=" * 60)
    print("  Backtest Complete!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
