#!/usr/bin/env python3
"""
Comparison Script: 38.2% vs 50% Fibonacci Entry
================================================
Compares the London Reversal strategy with two different entry levels:
- Current: 50% Fibonacci retracement
- Alternative: 38.2% Fibonacci retracement

This will show the impact on:
- Execution rate (missed trades)
- Win rate
- Average Risk/Reward
- Net profit
- Max drawdown
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import zipfile
import os
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Import the original backtest class
import sys
sys.path.insert(0, '/home/runner/work/Backtest-Trading/Backtest-Trading')
from london_reversal_backtest import LondonReversalBacktest


class LondonReversalBacktest382(LondonReversalBacktest):
    """
    Modified version with 38.2% Fibonacci entry instead of 50%
    """
    
    def __init__(self, data_dir: str = "/home/runner/work/Backtest-Trading/Backtest-Trading"):
        super().__init__(data_dir)
        self.fib_level = 0.382  # 38.2% Fibonacci level
    
    def calculate_entry_and_targets(self, manipulation: Dict, mss: Dict,
                                   direction: str) -> Dict:
        """
        Calculate entry price (38.2% Fib) and target levels.
        """
        if direction == 'short':
            # Fib from manipulation peak to MSS low
            fib_high = manipulation['peak']
            fib_low = mss['close']
            
            # Entry at 38.2% retracement (more aggressive)
            entry = fib_low + (fib_high - fib_low) * self.fib_level
            
            # Stop loss: 0.5 points above manipulation peak
            stop_loss = manipulation['peak'] + 0.5
            
            # Risk
            risk = stop_loss - entry
            
            # Take profits
            tp1 = entry - (risk * 1.0)  # 1R
            tp2 = entry - (risk * 1.5)  # 1.5R
            tp3 = entry - (risk * 2.0)  # 2R
            
        else:  # long
            # Fib from manipulation peak to MSS high
            fib_low = manipulation['peak']
            fib_high = mss['close']
            
            # Entry at 38.2% retracement (more aggressive)
            entry = fib_low + (fib_high - fib_low) * self.fib_level
            
            # Stop loss: 0.5 points below manipulation peak
            stop_loss = manipulation['peak'] - 0.5
            
            # Risk
            risk = entry - stop_loss
            
            # Take profits
            tp1 = entry + (risk * 1.0)  # 1R
            tp2 = entry + (risk * 1.5)  # 1.5R
            tp3 = entry + (risk * 2.0)  # 2R
        
        return {
            'direction': direction,
            'entry': entry,
            'stop_loss': stop_loss,
            'risk': risk,
            'tp1': tp1,
            'tp2': tp2,
            'tp3': tp3
        }


def run_comparison():
    """
    Run both backtests and compare results
    """
    print("=" * 80)
    print("FIBONACCI ENTRY COMPARISON: 38.2% vs 50%")
    print("=" * 80)
    print()
    
    # Run 50% backtest (original)
    print("Running backtest with 50% Fibonacci entry...")
    print("-" * 80)
    backtest_50 = LondonReversalBacktest()
    backtest_50.run_backtest(
        scan_timeframe='5m',
        tokyo_timeframe='15m',
        years=list(range(2018, 2026))
    )
    
    print("\n" + "=" * 80)
    print()
    
    # Run 38.2% backtest
    print("Running backtest with 38.2% Fibonacci entry...")
    print("-" * 80)
    backtest_382 = LondonReversalBacktest382()
    backtest_382.run_backtest(
        scan_timeframe='5m',
        tokyo_timeframe='15m',
        years=list(range(2018, 2026))
    )
    
    print("\n" + "=" * 80)
    print("COMPARISON RESULTS")
    print("=" * 80)
    
    # Extract key metrics
    total_setups_50 = len(backtest_50.trade_log)
    missed_50 = backtest_50.missed_trades
    executed_50 = total_setups_50 - missed_50
    
    total_setups_382 = len(backtest_382.trade_log)
    missed_382 = backtest_382.missed_trades
    executed_382 = total_setups_382 - missed_382
    
    print(f"\n{'Metric':<40} | {'50% Fib':<20} | {'38.2% Fib':<20} | Difference")
    print("-" * 100)
    
    # Setup statistics
    print(f"{'Total Setups Detected':<40} | {total_setups_50:<20} | {total_setups_382:<20} | {total_setups_382 - total_setups_50:+d}")
    print(f"{'Trades Executed':<40} | {executed_50:<20} | {executed_382:<20} | {executed_382 - executed_50:+d}")
    print(f"{'Trades Missed':<40} | {missed_50:<20} | {missed_382:<20} | {missed_382 - missed_50:+d}")
    
    exec_rate_50 = (executed_50 / total_setups_50 * 100) if total_setups_50 > 0 else 0
    exec_rate_382 = (executed_382 / total_setups_382 * 100) if total_setups_382 > 0 else 0
    print(f"{'Execution Rate (%)':<40} | {exec_rate_50:<20.2f} | {exec_rate_382:<20.2f} | {exec_rate_382 - exec_rate_50:+.2f}%")
    
    print("\n" + "=" * 100)
    
    # Compare TP2 results (recommended level)
    for fib_level, backtest, label in [(50, backtest_50, '50% Fib'), (38.2, backtest_382, '38.2% Fib')]:
        df = backtest.trade_log[backtest.trade_log['Outcome'] != 'Missed'].copy()
        
        if len(df) == 0:
            continue
        
        wins = len(df[df['TP2_Outcome'] == 'Win'])
        losses = len(df[df['TP2_Outcome'] == 'Loss'])
        total = wins + losses
        
        if total == 0:
            continue
        
        wr = (wins / total) * 100
        
        # Calculate metrics
        winning_trades = df[df['TP2_Outcome'] == 'Win']
        losing_trades = df[df['TP2_Outcome'] == 'Loss']
        
        avg_win = winning_trades['TP2_PnL'].mean() if len(winning_trades) > 0 else 0
        avg_loss = abs(losing_trades['TP2_PnL'].mean()) if len(losing_trades) > 0 else 0
        
        rr_ratio = avg_win / avg_loss if avg_loss > 0 else 0
        
        net_profit = df['TP2_PnL'].sum()
        
        total_wins = winning_trades['TP2_PnL'].sum() if len(winning_trades) > 0 else 0
        total_losses = abs(losing_trades['TP2_PnL'].sum()) if len(losing_trades) > 0 else 0
        pf = total_wins / total_losses if total_losses > 0 else 0
        
        # Calculate drawdown
        df_sorted = df.sort_values('Entry_Datetime')
        df_sorted['Cumulative_PnL'] = df_sorted['TP2_PnL'].cumsum()
        df_sorted['Running_Max'] = df_sorted['Cumulative_PnL'].cummax()
        df_sorted['Drawdown'] = df_sorted['Cumulative_PnL'] - df_sorted['Running_Max']
        max_dd = df_sorted['Drawdown'].min()
        max_dd_pct = (max_dd / df_sorted['Running_Max'].max() * 100) if df_sorted['Running_Max'].max() > 0 else 0
        
        print(f"\n{label} - TP2 (1.5R) RESULTS:")
        print("-" * 100)
        print(f"  Trades Executed:      {total}")
        print(f"  Win Rate:             {wr:.2f}%")
        print(f"  Avg Win:              ${avg_win:.2f}")
        print(f"  Avg Loss:             ${avg_loss:.2f}")
        print(f"  RR Ratio:             {rr_ratio:.2f}:1")
        print(f"  Net Profit:           ${net_profit:.2f}")
        print(f"  Profit Factor:        {pf:.2f}")
        print(f"  Max Drawdown:         ${max_dd:.2f} ({max_dd_pct:.2f}%)")
    
    print("\n" + "=" * 100)
    print("KEY INSIGHTS")
    print("=" * 100)
    
    # Calculate improvement percentages
    if executed_50 > 0:
        exec_increase = ((executed_382 - executed_50) / executed_50) * 100
        print(f"\n✓ Execution rate increased by {exec_increase:+.1f}% with 38.2% Fib entry")
    
    print(f"\n✓ More aggressive entry at 38.2% captures more setups")
    print(f"  but with different risk/reward characteristics")
    
    # Save comparison to file
    comparison_data = {
        'Entry_Level': ['50% Fib', '38.2% Fib'],
        'Total_Setups': [total_setups_50, total_setups_382],
        'Executed': [executed_50, executed_382],
        'Missed': [missed_50, missed_382],
        'Execution_Rate_%': [exec_rate_50, exec_rate_382]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.to_csv('fib_entry_comparison.csv', index=False)
    print(f"\n✓ Detailed comparison saved to: fib_entry_comparison.csv")
    
    print("\n" + "=" * 100)


if __name__ == "__main__":
    run_comparison()
