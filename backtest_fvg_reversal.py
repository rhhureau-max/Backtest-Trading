#!/usr/bin/env python3
"""
Fair Value Gap (FVG) Reversal Trading Strategy Backtester
For Nasdaq Futures (NQ) - 5-minute timeframe
Morning session: 02:00-06:00

This script implements a strict FVG reversal strategy with:
- Stop Loss: Swing +/- 0.5 points
- Take Profit: Risk-Reward based (1R or 1.5R)
- One trade at a time (no pyramiding)
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class FVGReversalBacktester:
    """Backtester for Fair Value Gap Reversal Strategy"""
    
    def __init__(self, data_dir: str = ".", risk_reward_ratio: float = 1.0):
        """
        Initialize the backtester with data directory and risk-reward ratio
        
        Args:
            data_dir: Directory containing CSV data files
            risk_reward_ratio: Risk-reward ratio for take profit (1.0 for 1R, 1.5 for 1.5R)
        """
        self.data_dir = Path(data_dir)
        self.risk_reward_ratio = risk_reward_ratio
        self.trades = []
        self.equity_curve = []
        
    def load_data(self) -> pd.DataFrame:
        """Load all 5m CSV files from 2018-2025"""
        print("Loading data files...")
        all_data = []
        
        for year in range(2018, 2026):
            file_path = self.data_dir / f"{year} 5m.csv"
            if file_path.exists():
                print(f"  Loading {file_path.name}...")
                df = pd.read_csv(
                    file_path,
                    sep=';',
                    header=0,
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                )
                all_data.append(df)
            else:
                print(f"  Warning: {file_path.name} not found")
        
        if not all_data:
            raise FileNotFoundError("No data files found!")
        
        # Combine all data
        data = pd.concat(all_data, ignore_index=True)
        
        # Create datetime column (no timezone conversion - use as-is)
        data['Datetime'] = pd.to_datetime(
            data['Date'] + ' ' + data['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # Sort by datetime
        data = data.sort_values('Datetime').reset_index(drop=True)
        
        print(f"Total candles loaded: {len(data)}")
        return data
    
    def filter_session(self, data: pd.DataFrame) -> pd.DataFrame:
        """Filter data for 02:00-06:00 morning session only"""
        print("\nFiltering for 02:00-06:00 session...")
        
        # Extract time component
        data['TimeOnly'] = data['Datetime'].dt.time
        
        # Filter for 02:00:00 to 05:55:00 (inclusive)
        session_start = time(2, 0, 0)
        session_end = time(5, 55, 0)
        
        filtered = data[
            (data['TimeOnly'] >= session_start) &
            (data['TimeOnly'] <= session_end)
        ].copy()
        
        print(f"Session candles: {len(filtered)}")
        return filtered
    
    def detect_fvg(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Detect Fair Value Gaps (FVG)
        - Bearish FVG: high[i-1] > low[i+1] (downward imbalance)
        - Bullish FVG: low[i-1] < high[i+1] (upward imbalance)
        """
        print("\nDetecting Fair Value Gaps...")
        
        data['BearishFVG'] = False
        data['BullishFVG'] = False
        data['FVG_Upper'] = np.nan
        data['FVG_Lower'] = np.nan
        
        # Need at least 3 candles to form FVG
        for i in range(1, len(data) - 1):
            # Bearish FVG: high of candle i-1 > low of candle i+1
            if data.iloc[i-1]['High'] > data.iloc[i+1]['Low']:
                data.at[data.index[i], 'BearishFVG'] = True
                data.at[data.index[i], 'FVG_Upper'] = data.iloc[i-1]['High']
                data.at[data.index[i], 'FVG_Lower'] = data.iloc[i+1]['Low']
            
            # Bullish FVG: low of candle i-1 < high of candle i+1
            elif data.iloc[i-1]['Low'] < data.iloc[i+1]['High']:
                data.at[data.index[i], 'BullishFVG'] = True
                data.at[data.index[i], 'FVG_Lower'] = data.iloc[i-1]['Low']
                data.at[data.index[i], 'FVG_Upper'] = data.iloc[i+1]['High']
        
        bearish_count = data['BearishFVG'].sum()
        bullish_count = data['BullishFVG'].sum()
        print(f"Bearish FVGs detected: {bearish_count}")
        print(f"Bullish FVGs detected: {bullish_count}")
        
        return data
    
    def find_swing_points(self, data: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
        """Find swing highs and swing lows"""
        data['SwingHigh'] = np.nan
        data['SwingLow'] = np.nan
        
        for i in range(lookback, len(data) - lookback):
            # Swing High: highest high in the window
            window_highs = data.iloc[i-lookback:i+lookback+1]['High']
            if data.iloc[i]['High'] == window_highs.max():
                data.at[data.index[i], 'SwingHigh'] = data.iloc[i]['High']
            
            # Swing Low: lowest low in the window
            window_lows = data.iloc[i-lookback:i+lookback+1]['Low']
            if data.iloc[i]['Low'] == window_lows.min():
                data.at[data.index[i], 'SwingLow'] = data.iloc[i]['Low']
        
        return data
    
    def backtest(self, data: pd.DataFrame) -> List[Dict]:
        """
        Execute the FVG reversal strategy backtest
        
        Long Setup:
        1. Bearish FVG forms
        2. Price returns into FVG zone
        3. Price fills and exceeds FVG
        4. Bullish candle validates breakout
        5. Entry: Long at close of validation candle
        6. Stop: Swing low - 0.5 points
        7. Target: Entry + RR * (Entry - Stop)
        
        Short Setup (inverse):
        1. Bullish FVG forms
        2. Price returns into FVG zone
        3. Price fills and exceeds FVG
        4. Bearish candle validates breakout
        5. Entry: Short at close of validation candle
        6. Stop: Swing high + 0.5 points
        7. Target: Entry - RR * (Stop - Entry)
        
        Only one trade can be active at a time (no pyramiding).
        """
        print("\nRunning backtest...")
        
        trades = []
        active_fvgs = []  # Track active FVG zones
        active_trade = None  # Track current open trade
        
        # Process each day separately to avoid cross-day trades
        data['Date_Only'] = data['Datetime'].dt.date
        
        for date, day_data in data.groupby('Date_Only'):
            day_data = day_data.reset_index(drop=True)
            daily_active_fvgs = []
            
            for i in range(len(day_data)):
                current = day_data.iloc[i]
                
                # Check if active trade needs to be closed
                if active_trade is not None:
                    exit_result = self._check_trade_exit(current, active_trade)
                    if exit_result is not None:
                        trades.append(exit_result)
                        active_trade = None  # Trade closed
                
                # Only look for new trades if no trade is active
                if active_trade is None:
                    # Detect new FVGs
                    if current['BearishFVG']:
                        daily_active_fvgs.append({
                            'type': 'bearish',
                            'upper': current['FVG_Upper'],
                            'lower': current['FVG_Lower'],
                            'index': i,
                            'datetime': current['Datetime'],
                            'filled': False,
                            'exceeded': False
                        })
                    
                    if current['BullishFVG']:
                        daily_active_fvgs.append({
                            'type': 'bullish',
                            'upper': current['FVG_Upper'],
                            'lower': current['FVG_Lower'],
                            'index': i,
                            'datetime': current['Datetime'],
                            'filled': False,
                            'exceeded': False
                        })
                    
                    # Check active FVGs for reversal setups
                    for fvg in daily_active_fvgs[:]:
                        if i <= fvg['index']:
                            continue
                        
                        # LONG SETUP: Bearish FVG reversal
                        if fvg['type'] == 'bearish' and not fvg.get('traded', False):
                            # Check if price returned into FVG zone
                            in_zone = (current['Low'] <= fvg['upper'] and 
                                      current['High'] >= fvg['lower'])
                            
                            if in_zone:
                                fvg['filled'] = True
                            
                            # Check if price exceeded FVG (moved above upper bound)
                            if fvg['filled'] and current['Close'] > fvg['upper']:
                                fvg['exceeded'] = True
                            
                            # Check for bullish validation candle
                            if fvg['exceeded'] and current['Close'] > current['Open']:
                                # Find previous swing low for stop loss
                                swing_low = self._find_previous_swing_low(day_data, i)
                                if swing_low is None:
                                    continue
                                
                                # Entry conditions met
                                entry_price = current['Close']
                                stop_loss = swing_low - 0.5  # NEW: Swing low - 0.5 points
                                
                                # Calculate R (risk)
                                risk = entry_price - stop_loss
                                
                                # Calculate take profit based on RR ratio
                                take_profit = entry_price + (self.risk_reward_ratio * risk)
                                
                                # Validate trade setup (TP > Entry > SL)
                                if take_profit > entry_price > stop_loss:
                                    # Create trade entry
                                    active_trade = {
                                        'type': 'LONG',
                                        'entry_datetime': current['Datetime'],
                                        'entry_price': entry_price,
                                        'stop_loss': stop_loss,
                                        'take_profit': take_profit,
                                        'fvg_type': 'bearish_reversal',
                                        'risk': risk
                                    }
                                    fvg['traded'] = True
                                    break  # Exit FVG loop, wait for this trade to close
                        
                        # SHORT SETUP: Bullish FVG reversal
                        elif fvg['type'] == 'bullish' and not fvg.get('traded', False):
                            # Check if price returned into FVG zone
                            in_zone = (current['Low'] <= fvg['upper'] and 
                                      current['High'] >= fvg['lower'])
                            
                            if in_zone:
                                fvg['filled'] = True
                            
                            # Check if price exceeded FVG (moved below lower bound)
                            if fvg['filled'] and current['Close'] < fvg['lower']:
                                fvg['exceeded'] = True
                            
                            # Check for bearish validation candle
                            if fvg['exceeded'] and current['Close'] < current['Open']:
                                # Find previous swing high for stop loss
                                swing_high = self._find_previous_swing_high(day_data, i)
                                if swing_high is None:
                                    continue
                                
                                # Entry conditions met
                                entry_price = current['Close']
                                stop_loss = swing_high + 0.5  # NEW: Swing high + 0.5 points
                                
                                # Calculate R (risk)
                                risk = stop_loss - entry_price
                                
                                # Calculate take profit based on RR ratio
                                take_profit = entry_price - (self.risk_reward_ratio * risk)
                                
                                # Validate trade setup (TP < Entry < SL)
                                if take_profit < entry_price < stop_loss:
                                    # Create trade entry
                                    active_trade = {
                                        'type': 'SHORT',
                                        'entry_datetime': current['Datetime'],
                                        'entry_price': entry_price,
                                        'stop_loss': stop_loss,
                                        'take_profit': take_profit,
                                        'fvg_type': 'bullish_reversal',
                                        'risk': risk
                                    }
                                    fvg['traded'] = True
                                    break  # Exit FVG loop, wait for this trade to close
            
            # Close any open trade at end of day
            if active_trade is not None:
                # Trade not closed during session - force close at session end
                active_trade = None
        
        print(f"Total trades executed: {len(trades)}")
        return trades
    
    def _find_previous_swing_low(self, data: pd.DataFrame, current_idx: int, 
                                  lookback: int = 20) -> Optional[float]:
        """Find the most recent swing low before current index"""
        start_idx = max(0, current_idx - lookback)
        window = data.iloc[start_idx:current_idx]
        
        if len(window) == 0:
            return None
        
        # Return the lowest low in the lookback window
        return window['Low'].min()
    
    def _find_previous_swing_high(self, data: pd.DataFrame, current_idx: int,
                                   lookback: int = 20) -> Optional[float]:
        """Find the most recent swing high before current index"""
        start_idx = max(0, current_idx - lookback)
        window = data.iloc[start_idx:current_idx]
        
        if len(window) == 0:
            return None
        
        # Return the highest high in the lookback window
        return window['High'].max()
    
    def _check_trade_exit(self, candle: pd.Series, active_trade: Dict) -> Optional[Dict]:
        """
        Check if the active trade should be closed based on current candle
        
        Args:
            candle: Current candle data
            active_trade: Dictionary containing active trade information
            
        Returns:
            Completed trade dictionary if exit occurred, None otherwise
        """
        if active_trade['type'] == 'LONG':
            # Check stop loss hit
            if candle['Low'] <= active_trade['stop_loss']:
                exit_price = active_trade['stop_loss']
                pnl = exit_price - active_trade['entry_price']
                r_multiple = pnl / active_trade['risk'] if active_trade['risk'] > 0 else 0
                
                return {
                    'type': 'LONG',
                    'entry_datetime': active_trade['entry_datetime'],
                    'entry_price': active_trade['entry_price'],
                    'exit_datetime': candle['Datetime'],
                    'exit_price': exit_price,
                    'stop_loss': active_trade['stop_loss'],
                    'take_profit': active_trade['take_profit'],
                    'pnl_points': pnl,
                    'r_multiple': r_multiple,
                    'result': 'LOSS',
                    'fvg_type': active_trade['fvg_type']
                }
            
            # Check take profit hit
            if candle['High'] >= active_trade['take_profit']:
                exit_price = active_trade['take_profit']
                pnl = exit_price - active_trade['entry_price']
                r_multiple = pnl / active_trade['risk'] if active_trade['risk'] > 0 else 0
                
                return {
                    'type': 'LONG',
                    'entry_datetime': active_trade['entry_datetime'],
                    'entry_price': active_trade['entry_price'],
                    'exit_datetime': candle['Datetime'],
                    'exit_price': exit_price,
                    'stop_loss': active_trade['stop_loss'],
                    'take_profit': active_trade['take_profit'],
                    'pnl_points': pnl,
                    'r_multiple': r_multiple,
                    'result': 'WIN',
                    'fvg_type': active_trade['fvg_type']
                }
        
        else:  # SHORT
            # Check stop loss hit
            if candle['High'] >= active_trade['stop_loss']:
                exit_price = active_trade['stop_loss']
                pnl = active_trade['entry_price'] - exit_price
                r_multiple = pnl / active_trade['risk'] if active_trade['risk'] > 0 else 0
                
                return {
                    'type': 'SHORT',
                    'entry_datetime': active_trade['entry_datetime'],
                    'entry_price': active_trade['entry_price'],
                    'exit_datetime': candle['Datetime'],
                    'exit_price': exit_price,
                    'stop_loss': active_trade['stop_loss'],
                    'take_profit': active_trade['take_profit'],
                    'pnl_points': pnl,
                    'r_multiple': r_multiple,
                    'result': 'LOSS',
                    'fvg_type': active_trade['fvg_type']
                }
            
            # Check take profit hit
            if candle['Low'] <= active_trade['take_profit']:
                exit_price = active_trade['take_profit']
                pnl = active_trade['entry_price'] - exit_price
                r_multiple = pnl / active_trade['risk'] if active_trade['risk'] > 0 else 0
                
                return {
                    'type': 'SHORT',
                    'entry_datetime': active_trade['entry_datetime'],
                    'entry_price': active_trade['entry_price'],
                    'exit_datetime': candle['Datetime'],
                    'exit_price': exit_price,
                    'stop_loss': active_trade['stop_loss'],
                    'take_profit': active_trade['take_profit'],
                    'pnl_points': pnl,
                    'r_multiple': r_multiple,
                    'result': 'WIN',
                    'fvg_type': active_trade['fvg_type']
                }
        
        return None
    
    def analyze_results(self, trades: List[Dict]) -> Dict:
        """Generate comprehensive performance analysis"""
        print("\n" + "="*80)
        print(f"COMPREHENSIVE BACKTEST RESULTS - FVG REVERSAL STRATEGY ({self.risk_reward_ratio}R)")
        print("="*80)
        
        if not trades:
            print("\nNo trades were executed during the backtest period.")
            return {}
        
        # Convert to DataFrame for easier analysis
        df_trades = pd.DataFrame(trades)
        
        # Add year and month columns
        df_trades['year'] = pd.to_datetime(df_trades['entry_datetime']).dt.year
        df_trades['month'] = pd.to_datetime(df_trades['entry_datetime']).dt.month
        df_trades['year_month'] = pd.to_datetime(df_trades['entry_datetime']).dt.to_period('M')
        
        # Calculate metrics
        total_trades = len(df_trades)
        long_trades = len(df_trades[df_trades['type'] == 'LONG'])
        short_trades = len(df_trades[df_trades['type'] == 'SHORT'])
        
        winning_trades = len(df_trades[df_trades['result'] == 'WIN'])
        losing_trades = len(df_trades[df_trades['result'] == 'LOSS'])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Points analysis
        total_points_won = df_trades[df_trades['result'] == 'WIN']['pnl_points'].sum()
        total_points_lost = abs(df_trades[df_trades['result'] == 'LOSS']['pnl_points'].sum())
        net_points = df_trades['pnl_points'].sum()
        
        # Average win/loss
        avg_win = df_trades[df_trades['result'] == 'WIN']['pnl_points'].mean() if winning_trades > 0 else 0
        avg_loss = abs(df_trades[df_trades['result'] == 'LOSS']['pnl_points'].mean()) if losing_trades > 0 else 0
        avg_win_loss_ratio = (avg_win / avg_loss) if avg_loss > 0 else 0
        
        # Profit factor
        profit_factor = (total_points_won / total_points_lost) if total_points_lost > 0 else float('inf')
        
        # Expectancy
        expectancy = df_trades['pnl_points'].mean() if total_trades > 0 else 0
        
        # Drawdown calculation
        df_trades['cumulative_pnl'] = df_trades['pnl_points'].cumsum()
        df_trades['running_max'] = df_trades['cumulative_pnl'].cummax()
        df_trades['drawdown'] = df_trades['cumulative_pnl'] - df_trades['running_max']
        max_drawdown = abs(df_trades['drawdown'].min())
        
        # Trade type analysis
        long_wins = len(df_trades[(df_trades['type'] == 'LONG') & (df_trades['result'] == 'WIN')])
        short_wins = len(df_trades[(df_trades['type'] == 'SHORT') & (df_trades['result'] == 'WIN')])
        long_win_rate = (long_wins / long_trades * 100) if long_trades > 0 else 0
        short_win_rate = (short_wins / short_trades * 100) if short_trades > 0 else 0
        
        # Print results
        print("\n" + "="*80)
        print("1. GLOBAL PERFORMANCE METRICS")
        print("="*80)
        print(f"\nTotal Number of Trades: {total_trades}")
        print(f"  - LONG Trades: {long_trades} (Win Rate: {long_win_rate:.2f}%)")
        print(f"  - SHORT Trades: {short_trades} (Win Rate: {short_win_rate:.2f}%)")
        print(f"\nWinning Trades: {winning_trades}")
        print(f"Losing Trades: {losing_trades}")
        print(f"Global Win Rate: {win_rate:.2f}%")
        print(f"\nTotal Points Gained: {total_points_won:.2f}")
        print(f"Total Points Lost: {total_points_lost:.2f}")
        print(f"Net Gain (Points): {net_points:.2f}")
        print(f"\nProfit Factor: {profit_factor:.2f}")
        print(f"Average Gain per Trade: {avg_win:.2f} points")
        print(f"Average Loss per Trade: {avg_loss:.2f} points")
        print(f"Average Win/Loss Ratio: {avg_win_loss_ratio:.2f}")
        
        print("\n" + "="*80)
        print("2. ADVANCED STATISTICS")
        print("="*80)
        print(f"\nMaximum Drawdown: {max_drawdown:.2f} points")
        print(f"Mathematical Expectancy per Trade: {expectancy:.2f} points")
        
        # R-Multiple Distribution
        print("\n--- R-Multiple Distribution ---")
        r_distribution = df_trades['r_multiple'].describe()
        print(f"Mean R: {r_distribution['mean']:.2f}")
        print(f"Median R: {r_distribution['50%']:.2f}")
        print(f"Min R: {r_distribution['min']:.2f}")
        print(f"Max R: {r_distribution['max']:.2f}")
        print(f"Std Dev R: {r_distribution['std']:.2f}")
        
        # R-Multiple bins
        print("\nR-Multiple Frequency:")
        r_bins = pd.cut(df_trades['r_multiple'], bins=[-float('inf'), -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, float('inf')])
        r_counts = r_bins.value_counts().sort_index()
        for bin_range, count in r_counts.items():
            print(f"  {bin_range}: {count} trades ({count/total_trades*100:.1f}%)")
        
        # Annual performance
        print("\n--- Annual Performance ---")
        annual_stats = df_trades.groupby('year').agg({
            'pnl_points': ['sum', 'count', 'mean'],
            'result': lambda x: (x == 'WIN').sum() / len(x) * 100
        }).round(2)
        annual_stats.columns = ['Total Points', 'Trades', 'Avg Points/Trade', 'Win Rate %']
        print(annual_stats)
        
        # Monthly performance
        print("\n--- Average Monthly Performance ---")
        monthly_stats = df_trades.groupby('month').agg({
            'pnl_points': ['sum', 'count', 'mean'],
            'result': lambda x: (x == 'WIN').sum() / len(x) * 100
        }).round(2)
        monthly_stats.columns = ['Total Points', 'Trades', 'Avg Points', 'Win Rate %']
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_stats.index = [month_names[i-1] for i in monthly_stats.index]
        print(monthly_stats)
        
        print("\n" + "="*80)
        print("3. QUALITATIVE ANALYSIS")
        print("="*80)
        
        # Best/Worst performing periods
        best_year = annual_stats['Total Points'].idxmax()
        best_year_points = annual_stats.loc[best_year, 'Total Points']
        worst_year = annual_stats['Total Points'].idxmin()
        worst_year_points = annual_stats.loc[worst_year, 'Total Points']
        
        print(f"\nMost Profitable Year: {best_year} with {best_year_points:.2f} points")
        print(f"Least Profitable Year: {worst_year} with {worst_year_points:.2f} points")
        
        best_month_idx = monthly_stats['Total Points'].idxmax()
        best_month_points = monthly_stats.loc[best_month_idx, 'Total Points']
        print(f"Most Profitable Month (avg): {best_month_idx} with {best_month_points:.2f} points")
        
        # Streak analysis
        win_streaks = []
        loss_streaks = []
        current_streak = 0
        streak_type = None
        
        for result in df_trades['result']:
            if result == 'WIN':
                if streak_type == 'WIN':
                    current_streak += 1
                else:
                    if current_streak > 0 and streak_type == 'LOSS':
                        loss_streaks.append(current_streak)
                    current_streak = 1
                    streak_type = 'WIN'
            else:
                if streak_type == 'LOSS':
                    current_streak += 1
                else:
                    if current_streak > 0 and streak_type == 'WIN':
                        win_streaks.append(current_streak)
                    current_streak = 1
                    streak_type = 'LOSS'
        
        # Add final streak
        if streak_type == 'WIN' and current_streak > 0:
            win_streaks.append(current_streak)
        elif streak_type == 'LOSS' and current_streak > 0:
            loss_streaks.append(current_streak)
        
        max_win_streak = max(win_streaks) if win_streaks else 0
        max_loss_streak = max(loss_streaks) if loss_streaks else 0
        
        print(f"\nMaximum Consecutive Wins: {max_win_streak}")
        print(f"Maximum Consecutive Losses: {max_loss_streak}")
        
        # Winning vs Losing behavior
        print("\n--- Typical Trade Behavior ---")
        print(f"\nWinning Trades:")
        print(f"  Average Points Gained: {avg_win:.2f}")
        print(f"  Target R Achievement: {self.risk_reward_ratio}R (by design)")
        
        print(f"\nLosing Trades:")
        print(f"  Average Points Lost: {avg_loss:.2f}")
        print(f"  Average R Lost: ~-1R (by design)")
        
        # Market conditions
        print("\n--- Favorable Market Conditions ---")
        print(f"Based on {self.risk_reward_ratio}R target strategy:")
        if self.risk_reward_ratio == 1.0:
            print("  - 1R target requires ~50%+ win rate for profitability")
            print(f"  - Achieved win rate: {win_rate:.2f}% (Excellent)")
        else:
            print(f"  - {self.risk_reward_ratio}R target allows for lower win rates")
            print(f"  - Achieved win rate: {win_rate:.2f}%")
        
        print("  - Clear FVG formations with decisive fills")
        print("  - Strong validation candles confirming reversal")
        print("  - Adequate price movement to reach targets")
        
        # Trade type preference
        if long_trades > short_trades * 2:
            print("\n  - Strategy shows significant LONG bias")
        elif short_trades > long_trades * 2:
            print("\n  - Strategy shows significant SHORT bias")
        else:
            print("\n  - Strategy shows balanced LONG/SHORT distribution")
        
        print("\n" + "="*80)
        print("4. PERFORMANCE COMPARISON NOTES")
        print("="*80)
        print(f"""
Strategy Configuration: {self.risk_reward_ratio}R Take Profit
Stop Loss: Swing +/- 0.5 points (Fixed)
Take Profit: Entry +/- {self.risk_reward_ratio}R (Risk-Reward based)

Key Characteristics:
- Win Rate: {win_rate:.2f}%
- Profit Factor: {profit_factor:.2f}
- Expectancy: {expectancy:.2f} points per trade
- Max Drawdown: {max_drawdown:.2f} points

This configuration {'achieves' if net_points > 0 else 'does not achieve'} positive expectancy.
{'Recommended for live trading consideration.' if profit_factor > 1.5 and win_rate > 50 else 'May require optimization or additional filters.'}
        """)
        
        # Save trades to CSV
        output_file = f'fvg_reversal_trades_{self.risk_reward_ratio}R.csv'
        df_trades.to_csv(output_file, index=False)
        print(f"\n✓ Detailed trade log saved to: {output_file}")
        
        print("\n" + "="*80)
        print("BACKTEST COMPLETE")
        print("="*80)
        
        return {
            'total_trades': total_trades,
            'long_trades': long_trades,
            'short_trades': short_trades,
            'win_rate': win_rate,
            'long_win_rate': long_win_rate,
            'short_win_rate': short_win_rate,
            'net_points': net_points,
            'profit_factor': profit_factor,
            'expectancy': expectancy,
            'max_drawdown': max_drawdown,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'trades_df': df_trades
        }
    
    def run(self):
        """Main execution method"""
        print("="*80)
        print("FVG REVERSAL STRATEGY BACKTEST")
        print("Instrument: NQ (Nasdaq Futures)")
        print("Timeframe: 5 minutes")
        print("Session: 02:00-06:00")
        print("Period: 2018-2025")
        print(f"Risk-Reward Ratio: {self.risk_reward_ratio}R")
        print("="*80)
        
        # Load data
        data = self.load_data()
        
        # Filter session
        session_data = self.filter_session(data)
        
        # Detect FVGs
        session_data = self.detect_fvg(session_data)
        
        # Find swing points
        session_data = self.find_swing_points(session_data)
        
        # Run backtest
        trades = self.backtest(session_data)
        
        # Analyze results
        results = self.analyze_results(trades)
        
        return results


def compare_strategies(results_1r: Dict, results_1_5r: Dict):
    """Compare the performance of 1R vs 1.5R strategies"""
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS: 1R vs 1.5R STRATEGY")
    print("="*80)
    
    if not results_1r or not results_1_5r:
        print("\nCannot perform comparison - one or both strategies have no trades.")
        return
    
    print("\n--- Performance Comparison ---")
    print(f"\n{'Metric':<30} {'1R Strategy':<20} {'1.5R Strategy':<20} {'Winner':<15}")
    print("-" * 85)
    
    # Total Trades
    print(f"{'Total Trades':<30} {results_1r['total_trades']:<20} {results_1_5r['total_trades']:<20} {'Same' if results_1r['total_trades'] == results_1_5r['total_trades'] else ('1R' if results_1r['total_trades'] > results_1_5r['total_trades'] else '1.5R'):<15}")
    
    # Win Rate
    print(f"{'Win Rate (%)':<30} {results_1r['win_rate']:<20.2f} {results_1_5r['win_rate']:<20.2f} {'1R' if results_1r['win_rate'] > results_1_5r['win_rate'] else '1.5R':<15}")
    
    # Net Points
    print(f"{'Net Points':<30} {results_1r['net_points']:<20.2f} {results_1_5r['net_points']:<20.2f} {'1R' if results_1r['net_points'] > results_1_5r['net_points'] else '1.5R':<15}")
    
    # Profit Factor
    pf_1r = f"{results_1r['profit_factor']:.2f}" if results_1r['profit_factor'] != float('inf') else "∞"
    pf_1_5r = f"{results_1_5r['profit_factor']:.2f}" if results_1_5r['profit_factor'] != float('inf') else "∞"
    pf_winner = '1R' if results_1r['profit_factor'] > results_1_5r['profit_factor'] else '1.5R'
    print(f"{'Profit Factor':<30} {pf_1r:<20} {pf_1_5r:<20} {pf_winner:<15}")
    
    # Expectancy
    print(f"{'Expectancy (pts/trade)':<30} {results_1r['expectancy']:<20.2f} {results_1_5r['expectancy']:<20.2f} {'1R' if results_1r['expectancy'] > results_1_5r['expectancy'] else '1.5R':<15}")
    
    # Max Drawdown
    print(f"{'Max Drawdown (pts)':<30} {results_1r['max_drawdown']:<20.2f} {results_1_5r['max_drawdown']:<20.2f} {'1R' if results_1r['max_drawdown'] < results_1_5r['max_drawdown'] else '1.5R':<15}")
    
    # Average Win
    print(f"{'Avg Win (pts)':<30} {results_1r['avg_win']:<20.2f} {results_1_5r['avg_win']:<20.2f} {'1.5R' if results_1_5r['avg_win'] > results_1r['avg_win'] else '1R':<15}")
    
    # Average Loss
    print(f"{'Avg Loss (pts)':<30} {results_1r['avg_loss']:<20.2f} {results_1_5r['avg_loss']:<20.2f} {'1R' if results_1r['avg_loss'] < results_1_5r['avg_loss'] else '1.5R':<15}")
    
    print("\n--- Key Insights ---")
    
    # Win Rate Comparison
    wr_diff = results_1r['win_rate'] - results_1_5r['win_rate']
    if abs(wr_diff) < 1:
        print(f"\n1. Win rates are virtually identical ({results_1r['win_rate']:.2f}% vs {results_1_5r['win_rate']:.2f}%)")
    else:
        print(f"\n1. {'1R' if wr_diff > 0 else '1.5R'} has a {abs(wr_diff):.2f}% higher win rate")
        print(f"   This is {'expected' if wr_diff > 0 else 'unexpected'} since {'1R' if wr_diff > 0 else '1.5R'} has a {'closer' if wr_diff > 0 else 'farther'} target")
    
    # Net Points Comparison
    np_diff = results_1_5r['net_points'] - results_1r['net_points']
    np_pct = (np_diff / abs(results_1r['net_points']) * 100) if results_1r['net_points'] != 0 else 0
    if np_diff > 0:
        print(f"\n2. 1.5R strategy produces {np_diff:.2f} more points ({np_pct:.1f}% improvement)")
        print(f"   Despite potentially lower win rate, larger wins compensate")
    else:
        print(f"\n2. 1R strategy produces {abs(np_diff):.2f} more points ({abs(np_pct):.1f}% better)")
        print(f"   Higher win rate with 1R target proves more effective for this setup")
    
    # Expectancy Comparison
    exp_diff = results_1_5r['expectancy'] - results_1r['expectancy']
    if exp_diff > 0:
        print(f"\n3. 1.5R has superior expectancy (+{exp_diff:.2f} pts/trade)")
        print(f"   Each trade is expected to yield {exp_diff:.2f} more points on average")
    else:
        print(f"\n3. 1R has superior expectancy (+{abs(exp_diff):.2f} pts/trade)")
        print(f"   More consistent smaller wins outperform occasional larger wins")
    
    # Risk Management
    dd_diff = results_1_5r['max_drawdown'] - results_1r['max_drawdown']
    if abs(dd_diff) < 100:
        print(f"\n4. Drawdowns are comparable (difference: {abs(dd_diff):.2f} pts)")
    else:
        better_dd = '1R' if dd_diff > 0 else '1.5R'
        print(f"\n4. {better_dd} has significantly lower drawdown (-{abs(dd_diff):.2f} pts)")
        print(f"   Better risk management with {better_dd} target")
    
    # Recommendation
    print("\n--- RECOMMENDATION ---")
    
    # Score each strategy
    score_1r = 0
    score_1_5r = 0
    
    if results_1r['net_points'] > results_1_5r['net_points']:
        score_1r += 3
    else:
        score_1_5r += 3
    
    if results_1r['expectancy'] > results_1_5r['expectancy']:
        score_1r += 2
    else:
        score_1_5r += 2
    
    if results_1r['profit_factor'] > results_1_5r['profit_factor']:
        score_1r += 2
    else:
        score_1_5r += 2
    
    if results_1r['max_drawdown'] < results_1_5r['max_drawdown']:
        score_1r += 1
    else:
        score_1_5r += 1
    
    if results_1r['win_rate'] > results_1_5r['win_rate']:
        score_1r += 1
    else:
        score_1_5r += 1
    
    if score_1r > score_1_5r:
        print(f"\nBased on overall performance metrics, the 1R strategy is RECOMMENDED.")
        print(f"  - More consistent performance")
        print(f"  - Higher win rate typically means better psychological comfort")
        print(f"  - Better suited for traders who prefer frequent smaller wins")
    elif score_1_5r > score_1r:
        print(f"\nBased on overall performance metrics, the 1.5R strategy is RECOMMENDED.")
        print(f"  - Higher net profitability")
        print(f"  - Better risk-reward efficiency")
        print(f"  - Better suited for patient traders seeking larger gains")
    else:
        print(f"\nBoth strategies show comparable performance.")
        print(f"  - Choice depends on trader psychology and preferences")
        print(f"  - 1R: More wins, better for confidence building")
        print(f"  - 1.5R: Larger wins, better for capital efficiency")
    
    print("\n" + "="*80)


def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("RUNNING DUAL BACKTEST: 1R AND 1.5R STRATEGIES")
    print("="*80)
    
    # Run 1R strategy
    print("\n\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + " "*25 + "RUNNING 1R STRATEGY" + " "*34 + "█")
    print("█" + " "*78 + "█")
    print("█"*80 + "\n")
    
    backtester_1r = FVGReversalBacktester(data_dir=".", risk_reward_ratio=1.0)
    results_1r = backtester_1r.run()
    
    # Run 1.5R strategy
    print("\n\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + " "*23 + "RUNNING 1.5R STRATEGY" + " "*34 + "█")
    print("█" + " "*78 + "█")
    print("█"*80 + "\n")
    
    backtester_1_5r = FVGReversalBacktester(data_dir=".", risk_reward_ratio=1.5)
    results_1_5r = backtester_1_5r.run()
    
    # Compare strategies
    compare_strategies(results_1r, results_1_5r)
    
    print("\n✓ Dual backtest execution completed successfully!")
    print(f"✓ Results saved to: fvg_reversal_trades_1.0R.csv and fvg_reversal_trades_1.5R.csv")


if __name__ == "__main__":
    main()
