"""
ICT Fair Value Gap (FVG) Backtest Strategy
============================================

This script backtests an ICT-based trading strategy on NASDAQ 100 (NQ) 1-minute data
from 2018 to 2025, focusing on Fair Value Gaps with specific reversal patterns.

Strategy Components:
1. FVG Identification with Displacement
2. Killzone Time Filter (NY Session: 08:30-11:00)
3. Reversal Pattern Entry (Hammer/Shooting Star)
4. Multiple R:R Take Profit Targets (1R, 1.5R, 2R)

Author: Expert Quant Developer
Date: 2025
"""

import pandas as pd
import numpy as np
import zipfile
import os
from datetime import datetime, time
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')


class ICTFVGBacktest:
    """
    ICT Fair Value Gap backtesting engine with advanced price action filtering.
    """
    
    def __init__(self, data_folder: str = '.', use_ema_filter: bool = False, 
                 use_atr_filter: bool = False, use_breakeven: bool = False):
        """
        Initialize the backtest engine.
        
        Args:
            data_folder: Path to folder containing CSV/ZIP data files
            use_ema_filter: Enable EMA 200 trend filter
            use_atr_filter: Enable ATR threshold filter
            use_breakeven: Enable breakeven stop loss management
        """
        self.data_folder = data_folder
        self.killzone_start = time(8, 30)
        self.killzone_end = time(11, 0)
        self.stop_buffer = 0.5  # points to add to stop loss
        self.rr_targets = [1.0, 1.5, 2.0]  # Risk:Reward ratios
        
        # Optimization filters
        self.use_ema_filter = use_ema_filter
        self.use_atr_filter = use_atr_filter
        self.use_breakeven = use_breakeven
        self.ema_period = 200
        self.atr_period = 14
        self.atr_threshold = 2.0  # minimum ATR in points
        
    def load_data(self, year: int) -> pd.DataFrame:
        """
        Load 1-minute data for a specific year from CSV or ZIP file.
        
        Args:
            year: Year to load data for
            
        Returns:
            DataFrame with OHLCV data
        """
        filename_zip = os.path.join(self.data_folder, f"{year} 1m.csv.zip")
        filename_csv = os.path.join(self.data_folder, f"{year} 1m.csv")
        
        df = None
        
        # Try loading from ZIP first
        if os.path.exists(filename_zip):
            print(f"Loading {year} data from ZIP file...")
            with zipfile.ZipFile(filename_zip, 'r') as zip_ref:
                csv_name = zip_ref.namelist()[0]
                with zip_ref.open(csv_name) as csv_file:
                    df = pd.read_csv(csv_file, sep=';')
        # Try loading from CSV
        elif os.path.exists(filename_csv):
            print(f"Loading {year} data from CSV file...")
            df = pd.read_csv(filename_csv, sep=';')
        else:
            print(f"Warning: No data file found for {year}")
            return pd.DataFrame()
        
        # Rename columns to standard names
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Parse datetime
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                        format='%d/%m/%Y %H:%M:%S')
        
        # Extract time for killzone filtering
        df['TimeOnly'] = df['DateTime'].dt.time
        
        # Set DateTime as index
        df.set_index('DateTime', inplace=True)
        
        # Convert OHLCV to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop any rows with NaN values
        df.dropna(inplace=True)
        
        print(f"Loaded {len(df)} rows for {year}")
        return df
    
    def load_all_data(self, start_year: int = 2018, end_year: int = 2025) -> pd.DataFrame:
        """
        Load and concatenate data from multiple years.
        
        Args:
            start_year: First year to load
            end_year: Last year to load (inclusive)
            
        Returns:
            Combined DataFrame with all data
        """
        all_data = []
        
        for year in range(start_year, end_year + 1):
            df_year = self.load_data(year)
            if not df_year.empty:
                all_data.append(df_year)
        
        if not all_data:
            raise ValueError("No data loaded!")
        
        df = pd.concat(all_data, axis=0)
        df.sort_index(inplace=True)
        
        print(f"\nTotal data loaded: {len(df)} rows")
        print(f"Date range: {df.index[0]} to {df.index[-1]}")
        
        return df
    
    def is_in_killzone(self, time_val: time) -> bool:
        """
        Check if time is within the NY killzone (08:30-11:00).
        
        Args:
            time_val: Time to check
            
        Returns:
            True if in killzone, False otherwise
        """
        return self.killzone_start <= time_val <= self.killzone_end
    
    def get_time_segment(self, time_val: time) -> str:
        """
        Determine which time segment a trade belongs to.
        
        Args:
            time_val: Time to check
            
        Returns:
            'Opening_Chaos' (08:30-10:00) or 'Silver_Bullet' (10:00-11:00)
        """
        if time(8, 30) <= time_val < time(10, 0):
            return 'Opening_Chaos'
        elif time(10, 0) <= time_val <= time(11, 0):
            return 'Silver_Bullet'
        return 'Unknown'
    
    def calculate_ema(self, df: pd.DataFrame, period: int = 200) -> pd.Series:
        """
        Calculate Exponential Moving Average.
        
        Args:
            df: DataFrame with price data
            period: EMA period
            
        Returns:
            Series with EMA values
        """
        return df['Close'].ewm(span=period, adjust=False).mean()
    
    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range.
        
        Args:
            df: DataFrame with OHLC data
            period: ATR period
            
        Returns:
            Series with ATR values
        """
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period, min_periods=1).mean()
        
        return atr
    
    def identify_displacement(self, open_price: float, close_price: float, 
                             high: float, low: float, avg_range: float) -> bool:
        """
        Identify if a candle shows displacement (large body).
        
        Args:
            open_price: Open price
            close_price: Close price
            high: High price
            low: Low price
            avg_range: Average range for reference
            
        Returns:
            True if displacement candle, False otherwise
        """
        body = abs(close_price - open_price)
        candle_range = high - low
        
        # Displacement: body is at least 60% of range and larger than 1.5x avg range
        if candle_range == 0:
            return False
        
        body_ratio = body / candle_range
        is_large = candle_range > (1.5 * avg_range)
        
        return body_ratio >= 0.6 and is_large
    
    def identify_fvg(self, df: pd.DataFrame, idx: int, avg_range: float) -> Tuple[str, float, float]:
        """
        Identify Fair Value Gap at given index.
        
        Args:
            df: DataFrame with OHLC data
            idx: Current index (candle i)
            avg_range: Average range for displacement check
            
        Returns:
            Tuple of (fvg_type, fvg_top, fvg_bottom)
            fvg_type: 'bearish', 'bullish', or None
        """
        # Need at least 2 previous candles
        if idx < 2:
            return None, 0, 0
        
        # Get candles i-2, i-1, i
        candle_i_minus_2 = df.iloc[idx - 2]
        candle_i_minus_1 = df.iloc[idx - 1]
        candle_i = df.iloc[idx]
        
        # Check for displacement in candle i-1
        is_displacement = self.identify_displacement(
            candle_i_minus_1['Open'], 
            candle_i_minus_1['Close'],
            candle_i_minus_1['High'],
            candle_i_minus_1['Low'],
            avg_range
        )
        
        if not is_displacement:
            return None, 0, 0
        
        # Bearish FVG: Low[i-2] > High[i]
        if candle_i_minus_2['Low'] > candle_i['High']:
            fvg_top = candle_i_minus_2['Low']
            fvg_bottom = candle_i['High']
            return 'bearish', fvg_top, fvg_bottom
        
        # Bullish FVG: High[i-2] < Low[i]
        if candle_i_minus_2['High'] < candle_i['Low']:
            fvg_top = candle_i['Low']
            fvg_bottom = candle_i_minus_2['High']
            return 'bullish', fvg_top, fvg_bottom
        
        return None, 0, 0
    
    def is_shooting_star(self, open_price: float, high: float, low: float, 
                         close_price: float) -> bool:
        """
        Identify Shooting Star pattern.
        
        Criteria:
        - Upper wick at least 2x the body
        - Small body in lower third of range
        
        Args:
            open_price, high, low, close_price: OHLC values
            
        Returns:
            True if shooting star, False otherwise
        """
        body = abs(close_price - open_price)
        upper_wick = high - max(open_price, close_price)
        lower_wick = min(open_price, close_price) - low
        total_range = high - low
        
        if total_range == 0 or body == 0:
            return False
        
        # Upper wick at least 2x body
        if upper_wick < 2 * body:
            return False
        
        # Body in lower third (lower wick should be small)
        body_position = (max(open_price, close_price) - low) / total_range
        
        return body_position <= 0.4  # Body in lower 40%
    
    def is_hammer(self, open_price: float, high: float, low: float, 
                  close_price: float) -> bool:
        """
        Identify Hammer pattern.
        
        Criteria:
        - Lower wick at least 2x the body
        - Small body in upper third of range
        
        Args:
            open_price, high, low, close_price: OHLC values
            
        Returns:
            True if hammer, False otherwise
        """
        body = abs(close_price - open_price)
        upper_wick = high - max(open_price, close_price)
        lower_wick = min(open_price, close_price) - low
        total_range = high - low
        
        if total_range == 0 or body == 0:
            return False
        
        # Lower wick at least 2x body
        if lower_wick < 2 * body:
            return False
        
        # Body in upper third (upper wick should be small)
        body_position = (high - min(open_price, close_price)) / total_range
        
        return body_position <= 0.4  # Body in upper 40%
    
    def check_fvg_mitigation(self, candle_high: float, candle_low: float,
                            fvg_type: str, fvg_top: float, fvg_bottom: float) -> bool:
        """
        Check if candle mitigates (tests) the FVG.
        
        Args:
            candle_high, candle_low: Candle's high and low
            fvg_type: 'bearish' or 'bullish'
            fvg_top, fvg_bottom: FVG boundaries
            
        Returns:
            True if FVG is mitigated, False otherwise
        """
        if fvg_type == 'bearish':
            # For bearish FVG, price should reach up into the gap
            return candle_high >= fvg_bottom and candle_high <= fvg_top
        elif fvg_type == 'bullish':
            # For bullish FVG, price should reach down into the gap
            return candle_low <= fvg_top and candle_low >= fvg_bottom
        
        return False
    
    def simulate_trade(self, df: pd.DataFrame, entry_idx: int, direction: str,
                      entry_price: float, stop_loss: float, 
                      rr_ratio: float) -> Dict:
        """
        Simulate a single trade with given parameters.
        
        Args:
            df: DataFrame with price data
            entry_idx: Index where trade is entered
            direction: 'long' or 'short'
            entry_price: Entry price
            stop_loss: Stop loss price
            rr_ratio: Risk:Reward ratio for take profit
            
        Returns:
            Dictionary with trade results
        """
        risk = abs(entry_price - stop_loss)
        take_profit = entry_price + (risk * rr_ratio) if direction == 'long' else entry_price - (risk * rr_ratio)
        
        # Track if breakeven has been activated
        breakeven_activated = False
        current_stop = stop_loss
        
        # Iterate through subsequent candles
        for i in range(entry_idx + 1, len(df)):
            candle = df.iloc[i]
            
            # Check for breakeven trigger (if enabled)
            if self.use_breakeven and not breakeven_activated:
                if direction == 'long':
                    # If price moved 1R in our favor, move SL to breakeven
                    if candle['High'] >= entry_price + risk:
                        current_stop = entry_price
                        breakeven_activated = True
                else:  # short
                    if candle['Low'] <= entry_price - risk:
                        current_stop = entry_price
                        breakeven_activated = True
            
            if direction == 'long':
                # Check if stop loss hit
                if candle['Low'] <= current_stop:
                    pnl = current_stop - entry_price if breakeven_activated else -risk
                    return {
                        'result': 'breakeven' if breakeven_activated and pnl == 0 else ('loss' if pnl < 0 else 'win'),
                        'pnl': pnl,
                        'exit_price': current_stop,
                        'exit_idx': i,
                        'bars_in_trade': i - entry_idx,
                        'breakeven_hit': breakeven_activated
                    }
                # Check if take profit hit
                if candle['High'] >= take_profit:
                    return {
                        'result': 'win',
                        'pnl': risk * rr_ratio,
                        'exit_price': take_profit,
                        'exit_idx': i,
                        'bars_in_trade': i - entry_idx,
                        'breakeven_hit': breakeven_activated
                    }
            else:  # short
                # Check if stop loss hit
                if candle['High'] >= current_stop:
                    pnl = entry_price - current_stop if breakeven_activated else -risk
                    return {
                        'result': 'breakeven' if breakeven_activated and pnl == 0 else ('loss' if pnl < 0 else 'win'),
                        'pnl': pnl,
                        'exit_price': current_stop,
                        'exit_idx': i,
                        'bars_in_trade': i - entry_idx,
                        'breakeven_hit': breakeven_activated
                    }
                # Check if take profit hit
                if candle['Low'] <= take_profit:
                    return {
                        'result': 'win',
                        'pnl': risk * rr_ratio,
                        'exit_price': take_profit,
                        'exit_idx': i,
                        'bars_in_trade': i - entry_idx,
                        'breakeven_hit': breakeven_activated
                    }
        
        # No exit found (end of data)
        return {
            'result': 'no_exit',
            'pnl': 0,
            'exit_price': df.iloc[-1]['Close'],
            'exit_idx': len(df) - 1,
            'bars_in_trade': len(df) - entry_idx,
            'breakeven_hit': breakeven_activated
        }
    
    def run_backtest(self, df: pd.DataFrame) -> Dict:
        """
        Run the complete backtest on the provided data.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            Dictionary with backtest results for each R:R ratio
        """
        print("\n" + "="*80)
        print("Starting ICT FVG Backtest...")
        if self.use_ema_filter:
            print("✓ EMA Filter ENABLED")
        if self.use_atr_filter:
            print("✓ ATR Filter ENABLED")
        if self.use_breakeven:
            print("✓ Breakeven ENABLED")
        print("="*80)
        
        # Calculate average range for displacement detection (20-period)
        df['Range'] = df['High'] - df['Low']
        df['AvgRange'] = df['Range'].rolling(window=20, min_periods=1).mean()
        
        # Calculate technical indicators
        if self.use_ema_filter:
            print("Calculating EMA 200...")
            df['EMA200'] = self.calculate_ema(df, self.ema_period)
        
        if self.use_atr_filter:
            print("Calculating ATR 14...")
            df['ATR'] = self.calculate_atr(df, self.atr_period)
        
        # Store active FVGs
        active_fvgs = []
        
        # Store trades for each R:R ratio
        trades_by_rr = {rr: [] for rr in self.rr_targets}
        
        # Track last exit to avoid overlapping trades
        last_exit_idx = -1
        
        print(f"Analyzing {len(df)} candles...")
        
        for i in range(2, len(df)):
            if i % 50000 == 0:
                print(f"Progress: {i}/{len(df)} candles processed...")
            
            current_candle = df.iloc[i]
            current_time = current_candle['TimeOnly']
            
            # Only look for FVGs during killzone
            if self.is_in_killzone(current_time):
                # Identify new FVG
                fvg_type, fvg_top, fvg_bottom = self.identify_fvg(
                    df, i, df.iloc[i]['AvgRange']
                )
                
                if fvg_type:
                    # Store FVG with creation index
                    active_fvgs.append({
                        'type': fvg_type,
                        'top': fvg_top,
                        'bottom': fvg_bottom,
                        'created_idx': i,
                        'created_time': df.index[i]
                    })
            
            # Check for mitigation of active FVGs
            fvgs_to_remove = []
            
            for fvg_idx, fvg in enumerate(active_fvgs):
                # Skip if we're still in a trade
                if i <= last_exit_idx:
                    continue
                
                # Only check mitigation during killzone
                if not self.is_in_killzone(current_time):
                    continue
                
                # Check if FVG is too old (expire after 50 candles)
                if i - fvg['created_idx'] > 50:
                    fvgs_to_remove.append(fvg_idx)
                    continue
                
                # Check if current candle mitigates the FVG
                if self.check_fvg_mitigation(
                    current_candle['High'], 
                    current_candle['Low'],
                    fvg['type'], 
                    fvg['top'], 
                    fvg['bottom']
                ):
                    # Check for reversal pattern
                    entry_signal = False
                    direction = None
                    
                    if fvg['type'] == 'bearish':
                        # Look for Shooting Star
                        if self.is_shooting_star(
                            current_candle['Open'],
                            current_candle['High'],
                            current_candle['Low'],
                            current_candle['Close']
                        ):
                            # Check that upper wick penetrates FVG
                            if current_candle['High'] >= fvg['bottom']:
                                entry_signal = True
                                direction = 'short'
                    
                    elif fvg['type'] == 'bullish':
                        # Look for Hammer
                        if self.is_hammer(
                            current_candle['Open'],
                            current_candle['High'],
                            current_candle['Low'],
                            current_candle['Close']
                        ):
                            # Check that lower wick penetrates FVG
                            if current_candle['Low'] <= fvg['top']:
                                entry_signal = True
                                direction = 'long'
                    
                    if entry_signal:
                        # Apply optimization filters before entering trade
                        filter_passed = True
                        
                        # EMA Filter: Long only above EMA, Short only below EMA
                        if self.use_ema_filter:
                            ema_value = df.iloc[i]['EMA200']
                            if direction == 'long' and current_candle['Close'] <= ema_value:
                                filter_passed = False
                            elif direction == 'short' and current_candle['Close'] >= ema_value:
                                filter_passed = False
                        
                        # ATR Filter: Only trade when ATR > threshold
                        if self.use_atr_filter and filter_passed:
                            atr_value = df.iloc[i]['ATR']
                            if atr_value < self.atr_threshold:
                                filter_passed = False
                        
                        # Skip this trade if filters not passed
                        if not filter_passed:
                            continue
                        
                        # Entry at close of signal candle
                        entry_price = current_candle['Close']
                        
                        # Get time segment for analysis
                        time_segment = self.get_time_segment(current_time)
                        
                        # Calculate stop loss
                        if direction == 'short':
                            stop_loss = current_candle['High'] + self.stop_buffer
                        else:  # long
                            stop_loss = current_candle['Low'] - self.stop_buffer
                        
                        # Simulate trade for each R:R ratio
                        for rr in self.rr_targets:
                            trade_result = self.simulate_trade(
                                df, i, direction, entry_price, stop_loss, rr
                            )
                            
                            if trade_result['result'] != 'no_exit':
                                trade_result.update({
                                    'entry_time': df.index[i],
                                    'entry_price': entry_price,
                                    'stop_loss': stop_loss,
                                    'direction': direction,
                                    'fvg_type': fvg['type'],
                                    'rr_ratio': rr,
                                    'risk': abs(entry_price - stop_loss),
                                    'time_segment': time_segment
                                })
                                
                                trades_by_rr[rr].append(trade_result)
                        
                        # Update last exit index (use the longest trade duration)
                        max_exit_idx = max(
                            self.simulate_trade(df, i, direction, entry_price, stop_loss, rr)['exit_idx']
                            for rr in self.rr_targets
                        )
                        last_exit_idx = max_exit_idx
                        
                        # Remove this FVG after trade entry
                        fvgs_to_remove.append(fvg_idx)
                        break  # Only one trade per candle
            
            # Remove processed FVGs
            for idx in sorted(fvgs_to_remove, reverse=True):
                active_fvgs.pop(idx)
        
        print(f"\nBacktest completed!")
        print(f"Total candles analyzed: {len(df)}")
        
        # Calculate statistics for each R:R ratio
        results = {}
        
        for rr in self.rr_targets:
            trades = trades_by_rr[rr]
            
            if not trades:
                print(f"\nNo trades found for {rr}R")
                results[rr] = None
                continue
            
            # Calculate metrics
            total_trades = len(trades)
            winning_trades = [t for t in trades if t['result'] == 'win']
            losing_trades = [t for t in trades if t['result'] == 'loss']
            breakeven_trades = [t for t in trades if t['result'] == 'breakeven']
            
            num_wins = len(winning_trades)
            num_losses = len(losing_trades)
            num_breakeven = len(breakeven_trades)
            
            win_rate = (num_wins / total_trades * 100) if total_trades > 0 else 0
            
            total_profit = sum(t['pnl'] for t in winning_trades)
            total_loss = abs(sum(t['pnl'] for t in losing_trades))
            
            profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')
            
            net_pnl = sum(t['pnl'] for t in trades)
            
            # Calculate time segment statistics
            opening_chaos_trades = [t for t in trades if t.get('time_segment') == 'Opening_Chaos']
            silver_bullet_trades = [t for t in trades if t.get('time_segment') == 'Silver_Bullet']
            
            # Calculate drawdown
            cumulative_pnl = []
            running_pnl = 0
            for trade in trades:
                running_pnl += trade['pnl']
                cumulative_pnl.append(running_pnl)
            
            if cumulative_pnl:
                peak = cumulative_pnl[0]
                max_dd = 0
                for pnl in cumulative_pnl:
                    if pnl > peak:
                        peak = pnl
                    dd = peak - pnl
                    if dd > max_dd:
                        max_dd = dd
            else:
                max_dd = 0
            
            # Average bars in trade
            avg_bars = np.mean([t['bars_in_trade'] for t in trades])
            
            results[rr] = {
                'total_trades': total_trades,
                'winning_trades': num_wins,
                'losing_trades': num_losses,
                'breakeven_trades': num_breakeven,
                'win_rate': win_rate,
                'profit_factor': profit_factor,
                'total_profit': total_profit,
                'total_loss': total_loss,
                'net_pnl': net_pnl,
                'max_drawdown': max_dd,
                'avg_bars_in_trade': avg_bars,
                'trades': trades,
                'opening_chaos_trades': opening_chaos_trades,
                'silver_bullet_trades': silver_bullet_trades
            }
        
        return results
    
    def print_results(self, results: Dict):
        """
        Print formatted backtest results.
        
        Args:
            results: Dictionary with results for each R:R ratio
        """
        print("\n" + "="*80)
        print("BACKTEST RESULTS SUMMARY")
        print("="*80)
        
        for rr in self.rr_targets:
            res = results.get(rr)
            
            if res is None:
                print(f"\n{rr}R Target: No trades")
                continue
            
            print(f"\n{'='*80}")
            print(f"TAKE PROFIT: {rr}R (Risk:Reward)")
            print(f"{'='*80}")
            print(f"Total Trades:        {res['total_trades']}")
            print(f"Winning Trades:      {res['winning_trades']}")
            print(f"Losing Trades:       {res['losing_trades']}")
            print(f"Win Rate:            {res['win_rate']:.2f}%")
            print(f"Profit Factor:       {res['profit_factor']:.3f}")
            print(f"Total Profit:        ${res['total_profit']:.2f}")
            print(f"Total Loss:          ${res['total_loss']:.2f}")
            print(f"Net P&L:             ${res['net_pnl']:.2f}")
            print(f"Max Drawdown:        ${res['max_drawdown']:.2f}")
            print(f"Avg Bars in Trade:   {res['avg_bars_in_trade']:.1f}")
        
        print("\n" + "="*80)
    
    def export_trades_to_csv(self, results: Dict, output_file: str = 'trade_log.csv'):
        """
        Export all trades to CSV file.
        
        Args:
            results: Dictionary with results for each R:R ratio
            output_file: Output CSV filename
        """
        all_trades = []
        
        for rr in self.rr_targets:
            res = results.get(rr)
            if res and res['trades']:
                all_trades.extend(res['trades'])
        
        if all_trades:
            df_trades = pd.DataFrame(all_trades)
            output_path = os.path.join(self.data_folder, output_file)
            df_trades.to_csv(output_path, index=False)
            print(f"\nTrade log exported to: {output_path}")


def calculate_time_segment_stats(trades):
    """Calculate statistics for time segments."""
    opening_trades = [t for t in trades if t.get('time_segment') == 'Opening_Chaos']
    silver_trades = [t for t in trades if t.get('time_segment') == 'Silver_Bullet']
    
    def calc_stats(trade_list):
        if not trade_list:
            return {'count': 0, 'winrate': 0, 'pnl': 0}
        wins = sum(1 for t in trade_list if t['result'] == 'win')
        pnl = sum(t['pnl'] for t in trade_list)
        return {
            'count': len(trade_list),
            'winrate': (wins / len(trade_list) * 100) if trade_list else 0,
            'pnl': pnl
        }
    
    return {
        'opening_chaos': calc_stats(opening_trades),
        'silver_bullet': calc_stats(silver_trades)
    }


def main():
    """
    Main execution function with optimization filter comparison.
    """
    print("="*80)
    print("ICT FVG BACKTEST WITH OPTIMIZATION FILTERS")
    print("NASDAQ 100 (NQ) 1-Minute Data")
    print("Period: 2018-2025")
    print("="*80)
    
    data_folder = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    # Load data once for all backtests
    print("\nLoading data...")
    backtest_temp = ICTFVGBacktest(data_folder=data_folder)
    df = backtest_temp.load_all_data(start_year=2018, end_year=2025)
    
    # Define strategy configurations to test
    strategies = {
        'Base': {'use_ema_filter': False, 'use_atr_filter': False, 'use_breakeven': False},
        'With_EMA': {'use_ema_filter': True, 'use_atr_filter': False, 'use_breakeven': False},
        'With_ATR': {'use_ema_filter': False, 'use_atr_filter': True, 'use_breakeven': False},
        'With_Breakeven': {'use_ema_filter': False, 'use_atr_filter': False, 'use_breakeven': True},
        'With_All_Filters': {'use_ema_filter': True, 'use_atr_filter': True, 'use_breakeven': True},
    }
    
    # Store results for comparison
    all_results = {}
    
    # Run backtest for each strategy configuration
    for strategy_name, config in strategies.items():
        print("\n" + "="*80)
        print(f"RUNNING: {strategy_name}")
        print("="*80)
        
        backtest = ICTFVGBacktest(
            data_folder=data_folder,
            use_ema_filter=config['use_ema_filter'],
            use_atr_filter=config['use_atr_filter'],
            use_breakeven=config['use_breakeven']
        )
        
        results = backtest.run_backtest(df.copy())
        all_results[strategy_name] = results
    
    # Print comparison table for 1.5R target (best performer from original)
    print("\n" + "="*100)
    print("STRATEGY COMPARISON TABLE - TARGET 1.5R (Risk:Reward)")
    print("="*100)
    print(f"{'Strategy':<20} {'Total Trades':<15} {'Win Rate':<12} {'Profit Factor':<15} {'Net P&L':<12} {'Max DD':<12}")
    print("-"*100)
    
    for strategy_name in strategies.keys():
        results = all_results[strategy_name]
        res_1_5r = results.get(1.5)
        
        if res_1_5r:
            print(f"{strategy_name:<20} {res_1_5r['total_trades']:<15} "
                  f"{res_1_5r['win_rate']:>10.2f}% "
                  f"{res_1_5r['profit_factor']:>14.3f} "
                  f"${res_1_5r['net_pnl']:>10.2f} "
                  f"${res_1_5r['max_drawdown']:>10.2f}")
        else:
            print(f"{strategy_name:<20} {'N/A':<15} {'N/A':<12} {'N/A':<15} {'N/A':<12} {'N/A':<12}")
    
    print("="*100)
    
    # Print time segmentation analysis for Base and With_All_Filters
    print("\n" + "="*100)
    print("TIME SEGMENTATION ANALYSIS - 1.5R Target")
    print("="*100)
    
    for strategy_name in ['Base', 'With_All_Filters']:
        results = all_results[strategy_name]
        res_1_5r = results.get(1.5)
        
        if res_1_5r:
            print(f"\n{strategy_name}:")
            time_stats = calculate_time_segment_stats(res_1_5r['trades'])
            
            print(f"  Opening Chaos (08:30-10:00):")
            print(f"    Trades: {time_stats['opening_chaos']['count']}")
            print(f"    Win Rate: {time_stats['opening_chaos']['winrate']:.2f}%")
            print(f"    Net P&L: ${time_stats['opening_chaos']['pnl']:.2f}")
            
            print(f"  Silver Bullet (10:00-11:00):")
            print(f"    Trades: {time_stats['silver_bullet']['count']}")
            print(f"    Win Rate: {time_stats['silver_bullet']['winrate']:.2f}%")
            print(f"    Net P&L: ${time_stats['silver_bullet']['pnl']:.2f}")
    
    print("\n" + "="*100)
    
    # Print detailed results for best performing strategy
    print("\n" + "="*100)
    print("DETAILED RESULTS - ALL R:R TARGETS")
    print("="*100)
    
    # Find best strategy based on profit factor at 1.5R
    best_strategy = max(strategies.keys(), 
                       key=lambda s: all_results[s].get(1.5, {}).get('profit_factor', 0) 
                       if all_results[s].get(1.5) else 0)
    
    print(f"\nBest Strategy: {best_strategy}")
    print("-"*100)
    
    for rr in [1.0, 1.5, 2.0]:
        res = all_results[best_strategy].get(rr)
        if res:
            print(f"\n{rr}R Target:")
            print(f"  Total Trades:    {res['total_trades']}")
            print(f"  Winning Trades:  {res['winning_trades']}")
            print(f"  Losing Trades:   {res['losing_trades']}")
            if 'breakeven_trades' in res and res['breakeven_trades'] > 0:
                print(f"  Breakeven Trades: {res['breakeven_trades']}")
            print(f"  Win Rate:        {res['win_rate']:.2f}%")
            print(f"  Profit Factor:   {res['profit_factor']:.3f}")
            print(f"  Net P&L:         ${res['net_pnl']:.2f}")
            print(f"  Max Drawdown:    ${res['max_drawdown']:.2f}")
    
    print("\n" + "="*100)
    print("Backtest Complete!")
    print("="*100)


if __name__ == "__main__":
    main()
