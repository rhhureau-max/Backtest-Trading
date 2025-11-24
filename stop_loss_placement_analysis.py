"""
Stop Loss Placement Analysis for FVG Strategy
Tests 3 different SL placement strategies across all R/R ratios and timeframes
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

from data_loader import DataLoader
from fvg_detector import FVGDetector
from performance_metrics import PerformanceMetrics


class StopLossPlacementBacktest:
    """Backtest engine with configurable stop loss placement"""
    
    def __init__(self, initial_capital=10000, risk_reward_ratio=2.0, sl_placement='middle'):
        """
        Initialize backtest engine
        
        Parameters:
        -----------
        initial_capital : float
            Initial capital
        risk_reward_ratio : float
            Risk/reward ratio for TP calculation
        sl_placement : str
            Stop loss placement strategy:
            - 'middle': SL at middle of FVG (original)
            - 'top': SL at top of FVG for long, bottom for short
            - 'bottom': SL at bottom of FVG for long, top for short
            - 'first_candle': SL below/above first candle of FVG
        """
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.trades = []
        self.risk_reward_ratio = risk_reward_ratio
        self.sl_placement = sl_placement
    
    def calculate_stop_loss(self, entry_price, fvg_info, direction, data, fvg_idx):
        """
        Calculate stop loss based on placement strategy
        
        Parameters:
        -----------
        entry_price : float
            Entry price
        fvg_info : dict
            FVG information (upper, lower, middle)
        direction : int
            1 for long, -1 for short
        data : pd.DataFrame
            Price data
        fvg_idx : int
            Index of FVG candle
            
        Returns:
        --------
        float
            Stop loss level
        """
        if self.sl_placement == 'middle':
            return fvg_info['middle']
        
        elif self.sl_placement == 'top':
            # For long: SL at top of FVG, For short: SL at bottom of FVG
            if direction == 1:  # Long
                return fvg_info['upper']
            else:  # Short
                return fvg_info['lower']
        
        elif self.sl_placement == 'bottom':
            # For long: SL at bottom of FVG, For short: SL at top of FVG
            if direction == 1:  # Long
                return fvg_info['lower']
            else:  # Short
                return fvg_info['upper']
        
        elif self.sl_placement == 'first_candle':
            # SL below/above the first candle (candle before FVG at 8:30)
            pos = data.index.get_loc(fvg_idx)
            if pos < 1:
                # Fallback to middle if first candle not available
                return fvg_info['middle']
            
            first_candle_idx = data.index[pos - 1]
            first_candle = data.loc[first_candle_idx]
            
            if direction == 1:  # Long - SL below first candle
                return first_candle['Low']
            else:  # Short - SL above first candle
                return first_candle['High']
        
        else:
            raise ValueError(f"Unknown SL placement: {self.sl_placement}")
    
    def run_backtest(self, data, timeframe):
        """Run backtest with current SL placement strategy"""
        
        # Get FVG signals
        fvg_signals = data[data['FVG_Signal'] != 0].copy()
        
        print(f"Processing {len(fvg_signals)} FVG signals...")
        
        trades_list = []
        
        for idx, row in fvg_signals.iterrows():
            # Determine direction
            direction = 1 if row['FVG_Signal'] == 1 else -1
            
            # Get FVG info
            fvg_info = {
                'upper': row['FVG_Upper'],
                'lower': row['FVG_Lower'],
                'middle': row['FVG_Middle']
            }
            
            # Find entry candle
            entry_time = self._get_entry_time(idx, timeframe, data)
            if entry_time is None:
                continue
            
            # Get entry price
            try:
                entry_candle = data.loc[entry_time]
                entry_price = entry_candle['Close']
            except:
                continue
            
            # Calculate SL using the placement strategy
            stop_loss = self.calculate_stop_loss(entry_price, fvg_info, direction, data, idx)
            
            # Calculate risk and TP
            risk = abs(entry_price - stop_loss)
            
            if direction == 1:  # Long
                take_profit = entry_price + (self.risk_reward_ratio * risk)
            else:  # Short
                take_profit = entry_price - (self.risk_reward_ratio * risk)
            
            # Execute trade
            trade_result = self._execute_trade(data, entry_time, entry_price, 
                                              stop_loss, take_profit, direction, fvg_info)
            
            if trade_result:
                trades_list.append(trade_result)
        
        print(f"Completed {len(trades_list)} trades")
        
        if len(trades_list) == 0:
            return None
        
        return pd.DataFrame(trades_list)
    
    def _get_entry_time(self, fvg_idx, timeframe, data):
        """Get entry time based on timeframe"""
        # fvg_idx is already a datetime index
        fvg_time = fvg_idx
        
        if timeframe == '1m':
            minutes_delay = 1
        elif timeframe == '5m':
            minutes_delay = 5
        elif timeframe == '15m':
            minutes_delay = 15
        else:
            return None
        
        entry_time = fvg_time + pd.Timedelta(minutes=minutes_delay)
        
        if entry_time in data.index:
            return entry_time
        return None
    
    def _execute_trade(self, data, entry_time, entry_price, stop_loss, take_profit, 
                       direction, fvg_info):
        """Execute trade and find exit"""
        
        entry_date = entry_time.date()
        
        # Get candles after entry
        future_data = data[data.index > entry_time]
        
        # Filter same day
        same_day_data = future_data[future_data['Date_only'] == entry_date]
        
        if len(same_day_data) == 0:
            return None
        
        # Check for exit
        for check_time, candle in same_day_data.iterrows():
            if direction == 1:  # Long
                # Check SL
                if candle['Low'] <= stop_loss:
                    return {
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_time': check_time,
                        'exit_price': stop_loss,
                        'direction': 'Long',
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'exit_reason': 'SL',
                        'pnl': stop_loss - entry_price,
                        'return_pct': ((stop_loss - entry_price) / entry_price) * 100,
                        'fvg_lower': fvg_info['lower'],
                        'fvg_upper': fvg_info['upper'],
                        'fvg_middle': fvg_info['middle']
                    }
                # Check TP
                if candle['High'] >= take_profit:
                    return {
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_time': check_time,
                        'exit_price': take_profit,
                        'direction': 'Long',
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'exit_reason': 'TP',
                        'pnl': take_profit - entry_price,
                        'return_pct': ((take_profit - entry_price) / entry_price) * 100,
                        'fvg_lower': fvg_info['lower'],
                        'fvg_upper': fvg_info['upper'],
                        'fvg_middle': fvg_info['middle']
                    }
            else:  # Short
                # Check SL
                if candle['High'] >= stop_loss:
                    return {
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_time': check_time,
                        'exit_price': stop_loss,
                        'direction': 'Short',
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'exit_reason': 'SL',
                        'pnl': entry_price - stop_loss,
                        'return_pct': ((entry_price - stop_loss) / entry_price) * 100,
                        'fvg_lower': fvg_info['lower'],
                        'fvg_upper': fvg_info['upper'],
                        'fvg_middle': fvg_info['middle']
                    }
                # Check TP
                if candle['Low'] <= take_profit:
                    return {
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_time': check_time,
                        'exit_price': take_profit,
                        'direction': 'Short',
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'exit_reason': 'TP',
                        'pnl': entry_price - take_profit,
                        'return_pct': ((entry_price - take_profit) / entry_price) * 100,
                        'fvg_lower': fvg_info['lower'],
                        'fvg_upper': fvg_info['upper'],
                        'fvg_middle': fvg_info['middle']
                    }
        
        # End of day - close position at last candle close
        last_candle = same_day_data.iloc[-1]
        exit_price = last_candle['Close']
        
        if direction == 1:
            pnl = exit_price - entry_price
        else:
            pnl = entry_price - exit_price
        
        return {
            'entry_time': entry_time,
            'entry_price': entry_price,
            'exit_time': same_day_data.index[-1],
            'exit_price': exit_price,
            'direction': 'Long' if direction == 1 else 'Short',
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'exit_reason': 'EOD',
            'pnl': pnl,
            'return_pct': (pnl / entry_price) * 100,
            'fvg_lower': fvg_info['lower'],
            'fvg_upper': fvg_info['upper'],
            'fvg_middle': fvg_info['middle']
        }


def run_sl_placement_analysis():
    """Run complete stop loss placement analysis"""
    
    print("\n" + "="*80)
    print("STOP LOSS PLACEMENT ANALYSIS - FVG STRATEGY")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Configuration
    START_YEAR = 2018
    END_YEAR = 2024
    INITIAL_CAPITAL = 10000
    TIMEFRAMES = ['1m', '5m', '15m']
    RISK_REWARD_RATIOS = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    SL_PLACEMENTS = ['top', 'bottom', 'first_candle']
    SL_NAMES = {
        'top': 'SL at Top/Bottom of FVG',
        'bottom': 'SL at Bottom/Top of FVG',
        'first_candle': 'SL at First Candle'
    }
    OUTPUT_DIR = 'results_sl_placement'
    
    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}\n")
    
    # Store all results
    all_results = {}
    
    # Load and process data for each timeframe
    for timeframe in TIMEFRAMES:
        print(f"\n{'='*80}")
        print(f"PROCESSING {timeframe.upper()} TIMEFRAME")
        print(f"{'='*80}\n")
        
        # Load data once for this timeframe
        print(f"Loading {timeframe} data...")
        loader = DataLoader()
        data = loader.load_multiple_years(START_YEAR, END_YEAR, timeframe)
        data = loader.filter_trading_hours(data, start_hour=8, end_hour=17)
        print(f"Loaded {len(data)} rows\n")
        
        # Detect FVG signals once
        print(f"Detecting FVG signals...")
        detector = FVGDetector()
        data_with_fvg = detector.detect_fvg(data, target_time='08:30:00')
        print()
        
        # Test each SL placement strategy
        for sl_placement in SL_PLACEMENTS:
            print(f"\n{'-'*60}")
            print(f"Testing: {SL_NAMES[sl_placement]}")
            print(f"{'-'*60}\n")
            
            all_results[f"{timeframe}_{sl_placement}"] = {}
            
            # Test each R/R ratio
            for rr_ratio in RISK_REWARD_RATIOS:
                print(f"  R/R {rr_ratio}...", end=' ')
                
                # Run backtest
                engine = StopLossPlacementBacktest(
                    initial_capital=INITIAL_CAPITAL,
                    risk_reward_ratio=rr_ratio,
                    sl_placement=sl_placement
                )
                
                trades_df = engine.run_backtest(data_with_fvg, timeframe)
                
                if trades_df is None or len(trades_df) == 0:
                    print("No trades")
                    continue
                
                # Calculate metrics
                perf = PerformanceMetrics(trades_df, initial_capital=INITIAL_CAPITAL)
                metrics = perf.calculate_all_metrics()
                metrics['risk_reward_ratio'] = rr_ratio
                metrics['sl_placement'] = sl_placement
                
                all_results[f"{timeframe}_{sl_placement}"][rr_ratio] = {
                    'trades_df': trades_df,
                    'metrics': metrics
                }
                
                # Save trades CSV
                csv_filename = f"trades_{timeframe}_{sl_placement}_rr{rr_ratio}.csv"
                csv_path = os.path.join(OUTPUT_DIR, csv_filename)
                trades_df.to_csv(csv_path, index=False)
                
                print(f"Return: {metrics['total_return']:.2f}%, Win Rate: {metrics['win_rate']:.2f}%")
    
    # Generate comparison report
    print(f"\n{'='*80}")
    print("GENERATING COMPARISON REPORT")
    print(f"{'='*80}\n")
    
    generate_sl_comparison_report(all_results, OUTPUT_DIR)
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nResults saved to: {OUTPUT_DIR}/")


def generate_sl_comparison_report(all_results, output_dir):
    """Generate comprehensive comparison report"""
    
    report_path = os.path.join(output_dir, 'sl_placement_comparison_report.md')
    
    with open(report_path, 'w') as f:
        f.write("# FVG Strategy - Stop Loss Placement Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write("This report compares three different stop loss placement strategies across all risk/reward ratios and timeframes.\n\n")
        
        f.write("### Stop Loss Placement Strategies Tested:\n\n")
        f.write("1. **SL at Top/Bottom of FVG:**\n")
        f.write("   - Long trades: SL at top of FVG\n")
        f.write("   - Short trades: SL at bottom of FVG\n\n")
        
        f.write("2. **SL at Bottom/Top of FVG:**\n")
        f.write("   - Long trades: SL at bottom of FVG\n")
        f.write("   - Short trades: SL at top of FVG\n\n")
        
        f.write("3. **SL at First Candle:**\n")
        f.write("   - Long trades: SL below the first candle (8:29 candle)\n")
        f.write("   - Short trades: SL above the first candle (8:29 candle)\n\n")
        
        f.write("**Analysis Period:** 2018-2024 (7 years)\n\n")
        f.write("---\n\n")
        
        # Results for each timeframe
        for timeframe in ['1m', '5m', '15m']:
            f.write(f"\n## {timeframe.upper()} Timeframe Results\n\n")
            
            for sl_placement in ['top', 'bottom', 'first_candle']:
                key = f"{timeframe}_{sl_placement}"
                
                if key not in all_results or not all_results[key]:
                    continue
                
                sl_name = {
                    'top': 'Top/Bottom',
                    'bottom': 'Bottom/Top',
                    'first_candle': 'First Candle'
                }[sl_placement]
                
                f.write(f"\n### Strategy: SL at {sl_name}\n\n")
                
                # Create table
                f.write("| R/R | Trades | Win Rate (%) | Return (%) | Sharpe | Max DD (%) | Profit Factor | Avg Win ($) | Avg Loss ($) |\n")
                f.write("|-----|--------|--------------|------------|--------|------------|---------------|-------------|-------------|\n")
                
                results = all_results[key]
                for rr in sorted(results.keys()):
                    m = results[rr]['metrics']
                    f.write(f"| {rr:.1f} | {m['total_trades']} | {m['win_rate']:.2f} | ")
                    f.write(f"{m['total_return']:.2f} | {m['sharpe_ratio']:.2f} | ")
                    f.write(f"{m['max_drawdown']:.2f} | {m['profit_factor']:.2f} | ")
                    f.write(f"{m['avg_win']:.2f} | {m['avg_loss']:.2f} |\n")
                
                # Find best R/R for this strategy
                best_rr = max(results.items(), key=lambda x: x[1]['metrics']['total_return'])
                f.write(f"\n**Best R/R:** {best_rr[0]} with {best_rr[1]['metrics']['total_return']:.2f}% return\n\n")
        
        # Overall best configurations
        f.write("\n## Overall Best Configurations\n\n")
        
        best_configs = []
        for key, results in all_results.items():
            if not results:
                continue
            for rr, data in results.items():
                best_configs.append({
                    'key': key,
                    'timeframe': key.split('_')[0],
                    'sl_placement': '_'.join(key.split('_')[1:]),
                    'rr': rr,
                    'return': data['metrics']['total_return'],
                    'sharpe': data['metrics']['sharpe_ratio'],
                    'win_rate': data['metrics']['win_rate'],
                    'max_dd': data['metrics']['max_drawdown']
                })
        
        if best_configs:
            # Sort by return
            best_configs.sort(key=lambda x: x['return'], reverse=True)
            
            f.write("### Top 10 Configurations by Total Return\n\n")
            f.write("| Rank | Timeframe | SL Placement | R/R | Return (%) | Sharpe | Win Rate (%) | Max DD (%) |\n")
            f.write("|------|-----------|--------------|-----|------------|--------|--------------|------------|\n")
            
            for i, config in enumerate(best_configs[:10], 1):
                sl_name = {
                    'top': 'Top/Bottom',
                    'bottom': 'Bottom/Top',
                    'first_candle': 'First Candle'
                }.get(config['sl_placement'], config['sl_placement'])
                
                f.write(f"| {i} | {config['timeframe'].upper()} | {sl_name} | {config['rr']:.1f} | ")
                f.write(f"{config['return']:.2f} | {config['sharpe']:.2f} | ")
                f.write(f"{config['win_rate']:.2f} | {config['max_dd']:.2f} |\n")
            
            f.write("\n")
        
        f.write("\n## Key Insights\n\n")
        f.write("1. **SL Placement Impact:** Different stop loss placements significantly affect both win rates and total returns\n")
        f.write("2. **Risk Management:** Tighter stops (first candle) may preserve capital better but could reduce win rates\n")
        f.write("3. **Optimal Strategy:** The best configuration balances return, win rate, and risk-adjusted performance\n\n")
    
    print(f"Report saved to: {report_path}")
    
    # Also create CSV summary
    csv_path = os.path.join(output_dir, 'sl_placement_summary.csv')
    summary_data = []
    
    for key, results in all_results.items():
        if not results:
            continue
        
        timeframe = key.split('_')[0]
        sl_placement = '_'.join(key.split('_')[1:])
        
        for rr, data in results.items():
            m = data['metrics']
            summary_data.append({
                'Timeframe': timeframe,
                'SL_Placement': sl_placement,
                'Risk_Reward_Ratio': rr,
                'Total_Trades': m['total_trades'],
                'Win_Rate_Pct': m['win_rate'],
                'Total_Return_Pct': m['total_return'],
                'Sharpe_Ratio': m['sharpe_ratio'],
                'Max_Drawdown_Pct': m['max_drawdown'],
                'Profit_Factor': m['profit_factor'],
                'Avg_Win': m['avg_win'],
                'Avg_Loss': m['avg_loss']
            })
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df = summary_df.sort_values(['Timeframe', 'SL_Placement', 'Risk_Reward_Ratio'])
        summary_df.to_csv(csv_path, index=False)
        print(f"CSV summary saved to: {csv_path}")


if __name__ == "__main__":
    run_sl_placement_analysis()
