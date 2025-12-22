#!/usr/bin/env python3
"""
FVG Inversion Strategy Backtesting Script
Backtests 3 variants of the FVG Inversion strategy on NQ 5-minute data (2018-2025)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')


class FVGBacktester:
    """Backtest FVG Inversion Strategy with multiple variants"""
    
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.df = None
        
    def load_data(self):
        """Load all 5-minute CSV files from 2018 to 2025"""
        print("Loading data files...")
        all_data = []
        
        for year in range(2018, 2026):
            file_path = self.data_dir / f"{year} 5m.csv"
            if file_path.exists():
                print(f"  Loading {file_path.name}...")
                df_year = pd.read_csv(
                    file_path, 
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )
                all_data.append(df_year)
        
        # Combine all years
        self.df = pd.concat(all_data, ignore_index=True)
        
        # Create datetime column
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'], 
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Convert OHLC to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Sort by datetime
        self.df = self.df.sort_values('DateTime').reset_index(drop=True)
        
        # Extract hour for filtering
        self.df['Hour'] = self.df['DateTime'].dt.hour
        
        print(f"Total candles loaded: {len(self.df)}")
        print(f"Date range: {self.df['DateTime'].min()} to {self.df['DateTime'].max()}")
        
    def detect_fvg(self):
        """
        Detect Fair Value Gaps (FVG)
        Only validate FVGs created by a candle with opening hour between 02:00 and 06:00 (inclusive)
        
        Bearish FVG: Low[i-1] > High[i+1] → resistance zone [High[i+1], Low[i-1]]
        Bullish FVG: High[i-1] < Low[i+1] → support zone [High[i-1], Low[i+1]]
        """
        print("\nDetecting FVGs...")
        
        fvg_list = []
        
        # Need at least 3 candles for FVG detection
        for i in range(1, len(self.df) - 1):
            # Check if candle i (middle candle) opens between 02:00 and 06:00
            if not (2 <= self.df.loc[i, 'Hour'] <= 6):
                continue
            
            # Bearish FVG: Low[i-1] > High[i+1]
            if self.df.loc[i-1, 'Low'] > self.df.loc[i+1, 'High']:
                fvg_list.append({
                    'index': i,
                    'type': 'bearish',
                    'top': self.df.loc[i-1, 'Low'],
                    'bottom': self.df.loc[i+1, 'High'],
                    'datetime': self.df.loc[i, 'DateTime']
                })
            
            # Bullish FVG: High[i-1] < Low[i+1]
            elif self.df.loc[i-1, 'High'] < self.df.loc[i+1, 'Low']:
                fvg_list.append({
                    'index': i,
                    'type': 'bullish',
                    'top': self.df.loc[i+1, 'Low'],
                    'bottom': self.df.loc[i-1, 'High'],
                    'datetime': self.df.loc[i, 'DateTime']
                })
        
        print(f"Total FVGs detected: {len(fvg_list)}")
        print(f"  Bearish FVGs: {sum(1 for fvg in fvg_list if fvg['type'] == 'bearish')}")
        print(f"  Bullish FVGs: {sum(1 for fvg in fvg_list if fvg['type'] == 'bullish')}")
        
        return fvg_list
    
    def get_swing_high_low(self, idx, lookback):
        """Get swing high/low for the last N candles before idx"""
        start_idx = max(0, idx - lookback)
        candles = self.df.iloc[start_idx:idx]
        
        swing_high = candles['High'].max()
        swing_low = candles['Low'].min()
        
        return swing_high, swing_low
    
    def backtest_strategy(self, fvg_list, strategy_name, sl_lookback, tp_multiplier):
        """
        Backtest a specific strategy variant
        
        Args:
            fvg_list: List of detected FVGs
            strategy_name: Name of the strategy
            sl_lookback: Number of candles to look back for SL
            tp_multiplier: Risk/reward multiplier for TP
        """
        print(f"\n{'='*60}")
        print(f"Backtesting: {strategy_name}")
        print(f"{'='*60}")
        
        trades = []
        active_trade = None
        
        for i in range(len(self.df)):
            current_candle = self.df.iloc[i]
            
            # Check if active trade hits SL or TP
            if active_trade:
                trade_hit = False
                
                if active_trade['direction'] == 'LONG':
                    # Check SL (Low hits SL)
                    if current_candle['Low'] <= active_trade['sl']:
                        active_trade['exit_price'] = active_trade['sl']
                        active_trade['exit_datetime'] = current_candle['DateTime']
                        active_trade['exit_reason'] = 'SL'
                        active_trade['pnl'] = active_trade['sl'] - active_trade['entry_price']
                        trade_hit = True
                    # Check TP (High hits TP)
                    elif current_candle['High'] >= active_trade['tp']:
                        active_trade['exit_price'] = active_trade['tp']
                        active_trade['exit_datetime'] = current_candle['DateTime']
                        active_trade['exit_reason'] = 'TP'
                        active_trade['pnl'] = active_trade['tp'] - active_trade['entry_price']
                        trade_hit = True
                
                elif active_trade['direction'] == 'SHORT':
                    # Check SL (High hits SL)
                    if current_candle['High'] >= active_trade['sl']:
                        active_trade['exit_price'] = active_trade['sl']
                        active_trade['exit_datetime'] = current_candle['DateTime']
                        active_trade['exit_reason'] = 'SL'
                        active_trade['pnl'] = active_trade['entry_price'] - active_trade['sl']
                        trade_hit = True
                    # Check TP (Low hits TP)
                    elif current_candle['Low'] <= active_trade['tp']:
                        active_trade['exit_price'] = active_trade['tp']
                        active_trade['exit_datetime'] = current_candle['DateTime']
                        active_trade['exit_reason'] = 'TP'
                        active_trade['pnl'] = active_trade['entry_price'] - active_trade['tp']
                        trade_hit = True
                
                if trade_hit:
                    trades.append(active_trade)
                    active_trade = None
            
            # Look for entry signals (only if no active trade)
            if not active_trade:
                for fvg in fvg_list:
                    # Only consider FVGs that occurred before current candle
                    if fvg['index'] >= i:
                        continue
                    
                    # LONG Entry: Close strictly above top of Bearish FVG
                    if fvg['type'] == 'bearish' and current_candle['Close'] > fvg['top']:
                        # Calculate SL (lowest low of last N candles)
                        _, swing_low = self.get_swing_high_low(i, sl_lookback)
                        sl = swing_low
                        
                        # Calculate TP using fixed RR multiplier
                        risk = current_candle['Close'] - sl
                        tp = current_candle['Close'] + (tp_multiplier * risk)
                        
                        active_trade = {
                            'direction': 'LONG',
                            'entry_price': current_candle['Close'],
                            'entry_datetime': current_candle['DateTime'],
                            'sl': sl,
                            'tp': tp,
                            'risk': risk,
                            'rr': tp_multiplier,
                            'fvg_type': fvg['type'],
                            'fvg_top': fvg['top'],
                            'fvg_bottom': fvg['bottom']
                        }
                        break  # One trade at a time
                    
                    # SHORT Entry: Close strictly below bottom of Bullish FVG
                    elif fvg['type'] == 'bullish' and current_candle['Close'] < fvg['bottom']:
                        # Calculate SL (highest high of last N candles)
                        swing_high, _ = self.get_swing_high_low(i, sl_lookback)
                        sl = swing_high
                        
                        # Calculate TP using fixed RR multiplier
                        risk = sl - current_candle['Close']
                        tp = current_candle['Close'] - (tp_multiplier * risk)
                        
                        active_trade = {
                            'direction': 'SHORT',
                            'entry_price': current_candle['Close'],
                            'entry_datetime': current_candle['DateTime'],
                            'sl': sl,
                            'tp': tp,
                            'risk': risk,
                            'rr': tp_multiplier,
                            'fvg_type': fvg['type'],
                            'fvg_top': fvg['top'],
                            'fvg_bottom': fvg['bottom']
                        }
                        break  # One trade at a time
        
        # Calculate statistics
        if not trades:
            print(f"No trades executed for {strategy_name}")
            return None
        
        trades_df = pd.DataFrame(trades)
        
        num_trades = len(trades_df)
        winning_trades = trades_df[trades_df['pnl'] > 0]
        losing_trades = trades_df[trades_df['pnl'] < 0]
        
        win_rate = (len(winning_trades) / num_trades * 100) if num_trades > 0 else 0
        
        total_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
        total_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0
        profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')
        
        total_pnl = trades_df['pnl'].sum()
        
        # Calculate max drawdown
        cumulative_pnl = trades_df['pnl'].cumsum()
        running_max = cumulative_pnl.cummax()
        drawdown = running_max - cumulative_pnl
        max_drawdown = drawdown.max()
        
        results = {
            'Strategy': strategy_name,
            'Trades': num_trades,
            'Win Rate (%)': round(win_rate, 2),
            'Profit Factor': round(profit_factor, 2) if profit_factor != float('inf') else 'Inf',
            'Total PnL (pts)': round(total_pnl, 2),
            'Max Drawdown (pts)': round(max_drawdown, 2),
            'Avg Win (pts)': round(winning_trades['pnl'].mean(), 2) if len(winning_trades) > 0 else 0,
            'Avg Loss (pts)': round(losing_trades['pnl'].mean(), 2) if len(losing_trades) > 0 else 0,
            'Wins': len(winning_trades),
            'Losses': len(losing_trades)
        }
        
        print(f"\nResults for {strategy_name}:")
        print(f"  Total Trades: {num_trades}")
        print(f"  Wins: {len(winning_trades)} | Losses: {len(losing_trades)}")
        print(f"  Win Rate: {win_rate:.2f}%")
        print(f"  Profit Factor: {results['Profit Factor']}")
        print(f"  Total PnL: {total_pnl:.2f} points")
        print(f"  Max Drawdown: {max_drawdown:.2f} points")
        print(f"  Avg Win: {results['Avg Win (pts)']:.2f} pts | Avg Loss: {results['Avg Loss (pts)']:.2f} pts")
        
        return results
    
    def run_all_strategies(self):
        """Run all three strategy variants with multiple TP ratios"""
        # Load data
        self.load_data()
        
        # Detect FVGs
        fvg_list = self.detect_fvg()
        
        if not fvg_list:
            print("\nNo FVGs detected. Cannot proceed with backtesting.")
            return
        
        # Define TP ratios to test
        tp_ratios = [1.0, 1.5, 2.0, 2.5]
        
        # Define strategy configurations
        strategies = [
            {'name': 'Strategy A (Scalping)', 'sl_lookback': 5},
            {'name': 'Strategy B (Intraday)', 'sl_lookback': 12},
            {'name': 'Strategy C (Swing)', 'sl_lookback': 20}
        ]
        
        # Backtest all combinations
        results = []
        
        for strategy in strategies:
            for tp_ratio in tp_ratios:
                strategy_name = f"{strategy['name']} - {tp_ratio} RR"
                result = self.backtest_strategy(
                    fvg_list, 
                    strategy_name,
                    sl_lookback=strategy['sl_lookback'],
                    tp_multiplier=tp_ratio
                )
                if result:
                    results.append(result)
        
        # Display comparison table
        if results:
            print(f"\n{'='*100}")
            print("COMPARATIVE RESULTS - FVG INVERSION STRATEGY (ALL TP RATIOS)")
            print(f"{'='*100}\n")
            
            results_df = pd.DataFrame(results)
            print(results_df.to_string(index=False))
            print(f"\n{'='*80}")
        else:
            print("\nNo results to display.")


def main():
    """Main execution function"""
    print("="*80)
    print("FVG INVERSION STRATEGY BACKTESTING")
    print("NQ 5-minute data (2018-2025)")
    print("="*80)
    
    # Initialize backtester
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    backtester = FVGBacktester(data_dir)
    
    # Run all strategies
    backtester.run_all_strategies()
    
    print("\nBacktesting complete!")


if __name__ == "__main__":
    main()
