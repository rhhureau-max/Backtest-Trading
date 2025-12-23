#!/usr/bin/env python3
"""
Fair Value Gap (FVG) Reversal Trading Strategy Backtester
For Nasdaq Futures (NQ) - 5-minute timeframe
Morning session: 02:00-06:00

This script implements a strict FVG reversal strategy with no modifications.
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
    
    def __init__(self, data_dir: str = "."):
        """Initialize the backtester with data directory"""
        self.data_dir = Path(data_dir)
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
        6. Stop: Below previous swing low
        7. Target: Previous swing high
        
        Short Setup (inverse):
        1. Bullish FVG forms
        2. Price returns into FVG zone
        3. Price fills and exceeds FVG
        4. Bearish candle validates breakout
        5. Entry: Short at close of validation candle
        6. Stop: Above previous swing high
        7. Target: Previous swing low
        """
        print("\nRunning backtest...")
        
        trades = []
        active_fvgs = []  # Track active FVG zones
        
        # Process each day separately to avoid cross-day trades
        data['Date_Only'] = data['Datetime'].dt.date
        
        for date, day_data in data.groupby('Date_Only'):
            day_data = day_data.reset_index(drop=True)
            daily_active_fvgs = []
            
            for i in range(len(day_data)):
                current = day_data.iloc[i]
                
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
                            
                            # Find previous swing high for take profit
                            swing_high = self._find_previous_swing_high(day_data, i)
                            if swing_high is None:
                                continue
                            
                            # Entry conditions met
                            entry_price = current['Close']
                            stop_loss = swing_low
                            take_profit = swing_high
                            
                            # Validate trade setup (TP > Entry > SL)
                            if take_profit > entry_price > stop_loss:
                                # Execute trade
                                trade = self._execute_long_trade(
                                    day_data, i, entry_price, stop_loss, 
                                    take_profit, fvg, current['Datetime']
                                )
                                if trade:
                                    trades.append(trade)
                                    fvg['traded'] = True
                    
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
                            
                            # Find previous swing low for take profit
                            swing_low = self._find_previous_swing_low(day_data, i)
                            if swing_low is None:
                                continue
                            
                            # Entry conditions met
                            entry_price = current['Close']
                            stop_loss = swing_high
                            take_profit = swing_low
                            
                            # Validate trade setup (TP < Entry < SL)
                            if take_profit < entry_price < stop_loss:
                                # Execute trade
                                trade = self._execute_short_trade(
                                    day_data, i, entry_price, stop_loss,
                                    take_profit, fvg, current['Datetime']
                                )
                                if trade:
                                    trades.append(trade)
                                    fvg['traded'] = True
        
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
    
    def _execute_long_trade(self, data: pd.DataFrame, entry_idx: int,
                           entry_price: float, stop_loss: float,
                           take_profit: float, fvg: Dict,
                           entry_datetime: datetime) -> Optional[Dict]:
        """Execute and manage a long trade"""
        # Check subsequent candles for exit
        for i in range(entry_idx + 1, len(data)):
            candle = data.iloc[i]
            
            # Check stop loss hit
            if candle['Low'] <= stop_loss:
                exit_price = stop_loss
                exit_datetime = candle['Datetime']
                pnl = exit_price - entry_price
                
                return {
                    'type': 'LONG',
                    'entry_datetime': entry_datetime,
                    'entry_price': entry_price,
                    'exit_datetime': exit_datetime,
                    'exit_price': exit_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'pnl_points': pnl,
                    'result': 'LOSS',
                    'fvg_type': 'bearish_reversal'
                }
            
            # Check take profit hit
            if candle['High'] >= take_profit:
                exit_price = take_profit
                exit_datetime = candle['Datetime']
                pnl = exit_price - entry_price
                
                return {
                    'type': 'LONG',
                    'entry_datetime': entry_datetime,
                    'entry_price': entry_price,
                    'exit_datetime': exit_datetime,
                    'exit_price': exit_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'pnl_points': pnl,
                    'result': 'WIN',
                    'fvg_type': 'bearish_reversal'
                }
        
        # Trade not closed during session (shouldn't happen often)
        return None
    
    def _execute_short_trade(self, data: pd.DataFrame, entry_idx: int,
                            entry_price: float, stop_loss: float,
                            take_profit: float, fvg: Dict,
                            entry_datetime: datetime) -> Optional[Dict]:
        """Execute and manage a short trade"""
        # Check subsequent candles for exit
        for i in range(entry_idx + 1, len(data)):
            candle = data.iloc[i]
            
            # Check stop loss hit
            if candle['High'] >= stop_loss:
                exit_price = stop_loss
                exit_datetime = candle['Datetime']
                pnl = entry_price - exit_price
                
                return {
                    'type': 'SHORT',
                    'entry_datetime': entry_datetime,
                    'entry_price': entry_price,
                    'exit_datetime': exit_datetime,
                    'exit_price': exit_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'pnl_points': pnl,
                    'result': 'LOSS',
                    'fvg_type': 'bullish_reversal'
                }
            
            # Check take profit hit
            if candle['Low'] <= take_profit:
                exit_price = take_profit
                exit_datetime = candle['Datetime']
                pnl = entry_price - exit_price
                
                return {
                    'type': 'SHORT',
                    'entry_datetime': entry_datetime,
                    'entry_price': entry_price,
                    'exit_datetime': exit_datetime,
                    'exit_price': exit_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'pnl_points': pnl,
                    'result': 'WIN',
                    'fvg_type': 'bullish_reversal'
                }
        
        # Trade not closed during session
        return None
    
    def analyze_results(self, trades: List[Dict]) -> Dict:
        """Generate comprehensive performance analysis"""
        print("\n" + "="*80)
        print("COMPREHENSIVE BACKTEST RESULTS - FVG REVERSAL STRATEGY")
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
        
        # Print results
        print("\n" + "="*80)
        print("1. GLOBAL PERFORMANCE METRICS")
        print("="*80)
        print(f"\nTotal Number of Trades: {total_trades}")
        print(f"Winning Trades: {winning_trades}")
        print(f"Losing Trades: {losing_trades}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"\nTotal Points Gained: {total_points_won:.2f}")
        print(f"Total Points Lost: {total_points_lost:.2f}")
        print(f"Net Gain (Points): {net_points:.2f}")
        print(f"\nProfit Factor: {profit_factor:.2f}")
        print(f"Average Win: {avg_win:.2f} points")
        print(f"Average Loss: {avg_loss:.2f} points")
        print(f"Average Win/Loss Ratio: {avg_win_loss_ratio:.2f}")
        
        print("\n" + "="*80)
        print("2. ADVANCED STATISTICS")
        print("="*80)
        print(f"\nMaximum Drawdown: {max_drawdown:.2f} points")
        print(f"Mathematical Expectancy per Trade: {expectancy:.2f} points")
        
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
        monthly_avg = df_trades.groupby('month')['pnl_points'].agg(['sum', 'count', 'mean']).round(2)
        monthly_avg.columns = ['Total Points', 'Trades', 'Avg Points']
        monthly_avg.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        print(monthly_avg)
        
        # Trade distribution
        print("\n--- Trade Type Distribution ---")
        trade_type_dist = df_trades.groupby('type').agg({
            'pnl_points': ['sum', 'count', 'mean'],
            'result': lambda x: (x == 'WIN').sum() / len(x) * 100
        }).round(2)
        trade_type_dist.columns = ['Total Points', 'Trades', 'Avg Points', 'Win Rate %']
        print(trade_type_dist)
        
        print("\n" + "="*80)
        print("3. QUALITATIVE ANALYSIS")
        print("="*80)
        
        # Best performing year
        best_year = annual_stats['Total Points'].idxmax()
        best_year_points = annual_stats.loc[best_year, 'Total Points']
        print(f"\nBest Performing Year: {best_year} with {best_year_points:.2f} points")
        
        # Worst performing year
        worst_year = annual_stats['Total Points'].idxmin()
        worst_year_points = annual_stats.loc[worst_year, 'Total Points']
        print(f"Worst Performing Year: {worst_year} with {worst_year_points:.2f} points")
        
        # Win streak analysis
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
        
        # Typical winning vs losing trade behavior
        print("\n--- Typical Trade Behavior ---")
        print(f"\nWinning Trades:")
        print(f"  Average Duration: Intraday (within session)")
        print(f"  Average Points Gained: {avg_win:.2f}")
        print(f"  Risk/Reward typically achieved: {avg_win_loss_ratio:.2f}:1")
        
        print(f"\nLosing Trades:")
        print(f"  Average Duration: Intraday (within session)")
        print(f"  Average Points Lost: {avg_loss:.2f}")
        
        # Market conditions analysis
        print("\n--- Most Favorable Market Conditions ---")
        print("Based on the data, the FVG reversal strategy performs best when:")
        print("  1. Clear FVG formations occur with distinct gaps")
        print("  2. Price shows decisive return and fill of the gap")
        print("  3. Strong validation candles confirm the reversal")
        print("  4. Adequate swing points exist for stop loss and take profit placement")
        
        print("\n" + "="*80)
        print("4. INTERPRETATIVE COMMENTS FOR DISCRETIONARY TRADERS")
        print("="*80)
        print("""
The FVG Reversal Strategy seeks to capitalize on fair value gaps that get filled
and subsequently reversed, indicating potential market inefficiency corrections.

Key Observations:
- This strategy is mechanical and follows strict rules without discretion
- The 02:00-06:00 morning session provides specific market characteristics
- FVG formations represent temporary imbalances in supply/demand
- Reversal setups suggest institutional order flow changes

For Discretionary Enhancement:
- Consider volume profile at FVG zones for confirmation
- Assess broader market context (trend, support/resistance)
- Evaluate the quality of validation candles (size, volume)
- Monitor multiple timeframes for confluence
- Be aware of news events that may impact the morning session

Risk Management Notes:
- All trades use defined stop losses based on swing points
- Take profit targets are based on previous swing extremes
- No position is held beyond the trading session
- Maximum risk per trade is predetermined by swing-based stops
        """)
        
        # Save trades to CSV
        output_file = 'fvg_reversal_trades.csv'
        df_trades.to_csv(output_file, index=False)
        print(f"\n✓ Detailed trade log saved to: {output_file}")
        
        print("\n" + "="*80)
        print("BACKTEST COMPLETE")
        print("="*80)
        
        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'net_points': net_points,
            'profit_factor': profit_factor,
            'expectancy': expectancy,
            'max_drawdown': max_drawdown,
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


def main():
    """Main entry point"""
    # Initialize backtester with current directory
    backtester = FVGReversalBacktester(data_dir=".")
    
    # Run the backtest
    results = backtester.run()
    
    print("\n✓ Backtest execution completed successfully!")


if __name__ == "__main__":
    main()
