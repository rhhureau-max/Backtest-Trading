#!/usr/bin/env python3
"""
Judas Swing + Inversion FVG - Multi-Timeframe Strategy Analysis
================================================================
Advanced backtesting strategy with multi-timeframe FVG analysis and A/B testing
for Stop Loss placement.

Strategy Rules:

1. Multi-Timeframe FVG Analysis (Hierarchy):
   - During manipulation (02:00-02:30), detect FVGs on both 5m and 1m timeframes
   - Priority Rule:
     * Case A (Priority): If 5m FVG exists → Use 5m FVG for entry signal
     * Case B (Secondary): If NO 5m FVG → Use 1m FVG for entry signal

2. Stop Loss A/B Testing:
   For each valid trade, simulate two SL placements based on "Manipulation Candle"
   (the candle that made the highest/lowest point during liquidity sweep):
   - SL-Body: Place SL just beyond the body (min(Open,Close) for LONG, max(Open,Close) for SHORT)
   - SL-Wick: Place SL at the absolute wick extreme (Low for LONG, High for SHORT)

3. Take Profit Objectives:
   For each SL version, calculate win rate for three objectives:
   - TP 1: Risk/Reward (RR) of 1:1
   - TP 2: Risk/Reward (RR) of 1:1.5
   - TP 3: Risk/Reward (RR) of 1:2

BEARISH SCENARIO (Short Entry):
1. Price manipulates Tokyo High between 02:00-02:30
2. During upward manipulation, a Bullish FVG forms
3. Price reverses, fills the FVG, and a candle closes below it
4. Entry: Close of the inversion candle
5. Two SL options tested: Body vs Wick
6. TP: Three levels (1R, 1.5R, 2R)

BULLISH SCENARIO (Long Entry):
1. Price manipulates Tokyo Low between 02:00-02:30
2. During downward manipulation, a Bearish FVG forms
3. Price reverses, fills the FVG, and a candle closes above it
4. Entry: Close of the inversion candle
5. Two SL options tested: Body vs Wick
6. TP: Three levels (1R, 1.5R, 2R)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import seaborn as sns


class FVG:
    """Class to represent a Fair Value Gap."""
    
    def __init__(self, fvg_type, top, bottom, start_idx, end_idx, formation_time, timeframe):
        """
        Initialize FVG.
        
        Args:
            fvg_type: 'BULLISH' or 'BEARISH'
            top: Upper boundary of the FVG
            bottom: Lower boundary of the FVG
            start_idx: Index of candle N-1
            end_idx: Index of candle N+1
            formation_time: Timestamp when FVG was formed
            timeframe: '5m' or '1m'
        """
        self.type = fvg_type
        self.top = top
        self.bottom = bottom
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.formation_time = formation_time
        self.timeframe = timeframe
        self.filled = False
        self.inverted = False
        self.inversion_time = None
        self.inversion_candle = None
    
    def __repr__(self):
        return f"FVG({self.type}, {self.bottom:.2f}-{self.top:.2f}, {self.timeframe}, formed at {self.formation_time})"


class JudasSwingMTFAnalyzer:
    """Analyzer for Multi-Timeframe Judas Swing FVG Strategy."""
    
    def __init__(self, data_directory):
        """Initialize the analyzer with the data directory."""
        self.data_directory = data_directory
        self.data_5m = None
        self.data_1m = None
        self.trades = []
        
    def load_data(self, years=None):
        """
        Load 5m and 1m data for specified years.
        
        Args:
            years: List of years to load (default: 2018-2025)
        """
        if years is None:
            years = range(2018, 2026)  # 2018-2025
        
        print("Loading 5-minute data...")
        data_5m_list = []
        for year in years:
            filename = f"{year} 5m.csv"
            filepath = os.path.join(self.data_directory, filename)
            
            if os.path.exists(filepath):
                print(f"  Loading {filename}...")
                try:
                    df = pd.read_csv(filepath, sep=';', header=0)
                    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                    df['DateTime'] = pd.to_datetime(
                        df['Date'] + ' ' + df['Time'], 
                        format='%d/%m/%Y %H:%M:%S',
                        errors='coerce'
                    )
                    df = df.dropna(subset=['DateTime'])
                    df = df.sort_values('DateTime')
                    df['Year'] = year
                    data_5m_list.append(df)
                    print(f"    Loaded {len(df)} rows")
                except Exception as e:
                    print(f"    Error loading {filename}: {e}")
        
        if data_5m_list:
            self.data_5m = pd.concat(data_5m_list, ignore_index=True)
            self.data_5m = self.data_5m.sort_values('DateTime').reset_index(drop=True)
            print(f"Total 5m data: {len(self.data_5m)} rows")
            print(f"Date range: {self.data_5m['DateTime'].min()} to {self.data_5m['DateTime'].max()}")
        
        # Load 1m data (from unzipped files or 2025 1m.csv)
        print("\nLoading 1-minute data...")
        data_1m_list = []
        for year in years:
            filename = f"{year} 1m.csv"
            filepath = os.path.join(self.data_directory, filename)
            
            if os.path.exists(filepath):
                print(f"  Loading {filename}...")
                try:
                    df = pd.read_csv(filepath, sep=';', header=0)
                    if 'Column1' in df.columns:
                        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                    df['DateTime'] = pd.to_datetime(
                        df['Date'] + ' ' + df['Time'], 
                        format='%d/%m/%Y %H:%M:%S',
                        errors='coerce'
                    )
                    df = df.dropna(subset=['DateTime'])
                    df = df.sort_values('DateTime')
                    df['Year'] = year
                    data_1m_list.append(df)
                    print(f"    Loaded {len(df)} rows")
                except Exception as e:
                    print(f"    Error loading {filename}: {e}")
        
        if data_1m_list:
            self.data_1m = pd.concat(data_1m_list, ignore_index=True)
            self.data_1m = self.data_1m.sort_values('DateTime').reset_index(drop=True)
            print(f"Total 1m data: {len(self.data_1m)} rows")
        else:
            print("No 1m data available - will interpolate from 5m if needed")
            self.data_1m = None
    
    def resample_5m_to_1m(self, data_5m):
        """
        Interpolate 1m data from 5m data (if 1m not available).
        This is a simplified approach - each 5m candle is split into 5 1m candles.
        
        Args:
            data_5m: DataFrame with 5m data
            
        Returns:
            DataFrame with interpolated 1m data
        """
        data_1m_list = []
        
        for idx, row in data_5m.iterrows():
            base_time = row['DateTime']
            open_price = row['Open']
            high_price = row['High']
            low_price = row['Low']
            close_price = row['Close']
            volume = row['Volume']
            
            # Simple interpolation: distribute price movement across 5 minutes
            price_range = close_price - open_price
            
            for i in range(5):
                minute_time = base_time + pd.Timedelta(minutes=i)
                # Linear interpolation
                minute_open = open_price + (price_range * i / 5)
                minute_close = open_price + (price_range * (i + 1) / 5)
                # Distribute high/low proportionally
                minute_high = max(minute_open, minute_close) + (high_price - max(open_price, close_price)) / 5
                minute_low = min(minute_open, minute_close) - (min(open_price, close_price) - low_price) / 5
                
                data_1m_list.append({
                    'DateTime': minute_time,
                    'Open': minute_open,
                    'High': minute_high,
                    'Low': minute_low,
                    'Close': minute_close,
                    'Volume': volume / 5,
                    'Interpolated': True
                })
        
        return pd.DataFrame(data_1m_list)
    
    def identify_tokyo_session(self, date, data):
        """
        Identify Tokyo session (19:00-00:00) for a given date.
        
        Args:
            date: The date to find Tokyo session for
            data: DataFrame to use (5m or 1m)
            
        Returns:
            dict with tokyo_high, tokyo_low, tokyo_eq, start_time, end_time
        """
        tokyo_start = pd.Timestamp(date) + pd.Timedelta(hours=19)
        tokyo_end = tokyo_start + pd.Timedelta(hours=5)
        
        tokyo_data = data[
            (data['DateTime'] >= tokyo_start) &
            (data['DateTime'] <= tokyo_end)
        ]
        
        if len(tokyo_data) == 0:
            return None
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        tokyo_eq = (tokyo_high + tokyo_low) / 2
        
        return {
            'tokyo_high': tokyo_high,
            'tokyo_low': tokyo_low,
            'tokyo_eq': tokyo_eq,
            'start_time': tokyo_start,
            'end_time': tokyo_end
        }
    
    def get_manipulation_data(self, date, data):
        """
        Get manipulation zone data (02:00-02:30) for the day after Tokyo session.
        
        Args:
            date: The date of Tokyo session
            data: DataFrame to use (5m or 1m)
            
        Returns:
            DataFrame with manipulation zone data
        """
        next_day = pd.Timestamp(date) + pd.Timedelta(days=1)
        manip_start = next_day + pd.Timedelta(hours=2)
        manip_end = manip_start + pd.Timedelta(minutes=30)
        
        manip_data = data[
            (data['DateTime'] >= manip_start) &
            (data['DateTime'] <= manip_end)
        ].copy()
        
        return manip_data.reset_index(drop=True), manip_start, manip_end
    
    def detect_fvgs(self, data, timeframe):
        """
        Detect Fair Value Gaps in the given data.
        
        Args:
            data: DataFrame with OHLC data
            timeframe: '5m' or '1m'
            
        Returns:
            List of FVG objects
        """
        fvgs = []
        
        if len(data) < 3:
            return fvgs
        
        data = data.reset_index(drop=True)
        
        for i in range(len(data) - 2):
            candle_n_minus_1 = data.iloc[i]
            candle_n = data.iloc[i + 1]
            candle_n_plus_1 = data.iloc[i + 2]
            
            # Bullish FVG (gap up)
            if candle_n_minus_1['High'] < candle_n_plus_1['Low']:
                fvg = FVG(
                    fvg_type='BULLISH',
                    top=candle_n_plus_1['Low'],
                    bottom=candle_n_minus_1['High'],
                    start_idx=i,
                    end_idx=i + 2,
                    formation_time=candle_n_plus_1['DateTime'],
                    timeframe=timeframe
                )
                fvgs.append(fvg)
            
            # Bearish FVG (gap down)
            elif candle_n_minus_1['Low'] > candle_n_plus_1['High']:
                fvg = FVG(
                    fvg_type='BEARISH',
                    top=candle_n_minus_1['Low'],
                    bottom=candle_n_plus_1['High'],
                    start_idx=i,
                    end_idx=i + 2,
                    formation_time=candle_n_plus_1['DateTime'],
                    timeframe=timeframe
                )
                fvgs.append(fvg)
        
        return fvgs
    
    def find_manipulation_candle(self, manip_data, manipulation_type):
        """
        Find the manipulation candle (the one that made the extreme high/low).
        
        Args:
            manip_data: DataFrame with manipulation zone data
            manipulation_type: 'HIGH' or 'LOW'
            
        Returns:
            Series with the manipulation candle data
        """
        if manipulation_type == 'HIGH':
            # Find candle with highest high
            max_high_idx = manip_data['High'].idxmax()
            return manip_data.loc[max_high_idx]
        else:  # LOW
            # Find candle with lowest low
            min_low_idx = manip_data['Low'].idxmin()
            return manip_data.loc[min_low_idx]
    
    def check_fvg_inversion(self, fvg, data_after_fvg, direction):
        """
        Check if FVG is inverted (price fills it and closes beyond).
        
        Args:
            fvg: FVG object
            data_after_fvg: DataFrame with data after FVG formation
            direction: 'SHORT' or 'LONG'
            
        Returns:
            Inversion candle or None
        """
        for idx, candle in data_after_fvg.iterrows():
            if direction == 'SHORT':
                # For SHORT: need Bullish FVG to be filled and close below
                if fvg.type == 'BULLISH':
                    # Check if price entered FVG zone
                    if candle['Low'] <= fvg.top and candle['High'] >= fvg.bottom:
                        # Check if close is below FVG
                        if candle['Close'] < fvg.bottom:
                            return candle
            else:  # LONG
                # For LONG: need Bearish FVG to be filled and close above
                if fvg.type == 'BEARISH':
                    # Check if price entered FVG zone
                    if candle['Low'] <= fvg.top and candle['High'] >= fvg.bottom:
                        # Check if close is above FVG
                        if candle['Close'] > fvg.top:
                            return candle
        
        return None
    
    def simulate_trade(self, entry_price, sl_price, tp_price, entry_time, data_after_entry, direction):
        """
        Simulate a trade to see if TP or SL is hit first.
        
        Args:
            entry_price: Entry price
            sl_price: Stop loss price
            tp_price: Take profit price
            entry_time: Entry timestamp
            data_after_entry: DataFrame with data after entry
            direction: 'LONG' or 'SHORT'
            
        Returns:
            dict with result, exit_price, exit_time, pnl_r
        """
        for idx, candle in data_after_entry.iterrows():
            if direction == 'LONG':
                # Check if SL hit first
                if candle['Low'] <= sl_price:
                    return {
                        'result': 'LOSS',
                        'exit_price': sl_price,
                        'exit_time': candle['DateTime'],
                        'pnl_r': -1.0
                    }
                # Check if TP hit
                if candle['High'] >= tp_price:
                    risk = entry_price - sl_price
                    reward = tp_price - entry_price
                    return {
                        'result': 'WIN',
                        'exit_price': tp_price,
                        'exit_time': candle['DateTime'],
                        'pnl_r': reward / risk if risk > 0 else 0
                    }
            else:  # SHORT
                # Check if SL hit first
                if candle['High'] >= sl_price:
                    return {
                        'result': 'LOSS',
                        'exit_price': sl_price,
                        'exit_time': candle['DateTime'],
                        'pnl_r': -1.0
                    }
                # Check if TP hit
                if candle['Low'] <= tp_price:
                    risk = sl_price - entry_price
                    reward = entry_price - tp_price
                    return {
                        'result': 'WIN',
                        'exit_price': tp_price,
                        'exit_time': candle['DateTime'],
                        'pnl_r': reward / risk if risk > 0 else 0
                    }
        
        # Trade still open (no result within data range)
        return {
            'result': 'OPEN',
            'exit_price': None,
            'exit_time': None,
            'pnl_r': 0
        }
    
    def analyze_day(self, date):
        """
        Analyze a single day for trading opportunities.
        
        Args:
            date: Date to analyze
            
        Returns:
            List of trade dictionaries
        """
        day_trades = []
        
        # Get Tokyo session
        tokyo_info = self.identify_tokyo_session(date, self.data_5m)
        if not tokyo_info:
            return day_trades
        
        tokyo_high = tokyo_info['tokyo_high']
        tokyo_low = tokyo_info['tokyo_low']
        tokyo_eq = tokyo_info['tokyo_eq']
        
        # Get manipulation data for 5m
        manip_data_5m, manip_start, manip_end = self.get_manipulation_data(date, self.data_5m)
        
        if len(manip_data_5m) == 0:
            return day_trades
        
        # Check if manipulation occurred
        manip_high = manip_data_5m['High'].max()
        manip_low = manip_data_5m['Low'].min()
        
        manipulation_type = None
        if manip_high > tokyo_high and manip_low < tokyo_low:
            # Both sides hit - take first one
            high_candle = manip_data_5m[manip_data_5m['High'] == manip_high].iloc[0]
            low_candle = manip_data_5m[manip_data_5m['Low'] == manip_low].iloc[0]
            if high_candle['DateTime'] < low_candle['DateTime']:
                manipulation_type = 'HIGH'
            else:
                manipulation_type = 'LOW'
        elif manip_high > tokyo_high:
            manipulation_type = 'HIGH'
        elif manip_low < tokyo_low:
            manipulation_type = 'LOW'
        
        if not manipulation_type:
            return day_trades
        
        direction = 'SHORT' if manipulation_type == 'HIGH' else 'LONG'
        
        # Detect FVGs on 5m
        fvgs_5m = self.detect_fvgs(manip_data_5m, '5m')
        
        # Filter FVGs by type (Bullish for SHORT, Bearish for LONG)
        if direction == 'SHORT':
            fvgs_5m = [fvg for fvg in fvgs_5m if fvg.type == 'BULLISH']
        else:
            fvgs_5m = [fvg for fvg in fvgs_5m if fvg.type == 'BEARISH']
        
        # Get 1m data for manipulation zone
        if self.data_1m is not None:
            manip_data_1m, _, _ = self.get_manipulation_data(date, self.data_1m)
        else:
            # Interpolate from 5m
            manip_data_1m = self.resample_5m_to_1m(manip_data_5m)
        
        # Detect FVGs on 1m
        fvgs_1m = self.detect_fvgs(manip_data_1m, '1m')
        
        # Filter FVGs by type
        if direction == 'SHORT':
            fvgs_1m = [fvg for fvg in fvgs_1m if fvg.type == 'BULLISH']
        else:
            fvgs_1m = [fvg for fvg in fvgs_1m if fvg.type == 'BEARISH']
        
        # Apply priority rule: 5m > 1m
        selected_fvg = None
        used_timeframe = None
        
        if len(fvgs_5m) > 0:
            # Use first 5m FVG
            selected_fvg = fvgs_5m[0]
            used_timeframe = '5m'
        elif len(fvgs_1m) > 0:
            # Use first 1m FVG
            selected_fvg = fvgs_1m[0]
            used_timeframe = '1m'
        
        if not selected_fvg:
            return day_trades
        
        # Get data after manipulation for checking inversion
        # Use appropriate timeframe data
        if used_timeframe == '5m':
            data_after_manip = self.data_5m[self.data_5m['DateTime'] > manip_end].head(100)
        else:
            if self.data_1m is not None:
                data_after_manip = self.data_1m[self.data_1m['DateTime'] > manip_end].head(300)
            else:
                # Use 5m data as fallback
                data_after_manip = self.data_5m[self.data_5m['DateTime'] > manip_end].head(100)
        
        # Check for FVG inversion
        inversion_candle = self.check_fvg_inversion(selected_fvg, data_after_manip, direction)
        
        if inversion_candle is None:
            return day_trades
        
        # Entry price
        entry_price = inversion_candle['Close']
        entry_time = inversion_candle['DateTime']
        
        # Find manipulation candle for SL calculation
        manip_candle = self.find_manipulation_candle(manip_data_5m, manipulation_type)
        
        # Calculate two SL options
        if direction == 'SHORT':
            sl_body = max(manip_candle['Open'], manip_candle['Close'])
            sl_wick = manip_candle['High']
        else:  # LONG
            sl_body = min(manip_candle['Open'], manip_candle['Close'])
            sl_wick = manip_candle['Low']
        
        # Get data after entry for simulation (use 5m data for all simulations)
        data_after_entry = self.data_5m[self.data_5m['DateTime'] > entry_time].head(200)
        
        if len(data_after_entry) == 0:
            return day_trades
        
        # Test both SL options with 3 TP levels each
        for sl_type, sl_price in [('SL-Body', sl_body), ('SL-Wick', sl_wick)]:
            # Calculate risk
            if direction == 'SHORT':
                risk = sl_price - entry_price
            else:
                risk = entry_price - sl_price
            
            if risk <= 0:
                continue  # Invalid trade setup
            
            # Test 3 R:R ratios
            for rr_ratio, rr_name in [(1.0, '1R'), (1.5, '1.5R'), (2.0, '2R')]:
                # Calculate TP
                if direction == 'SHORT':
                    tp_price = entry_price - (risk * rr_ratio)
                else:
                    tp_price = entry_price + (risk * rr_ratio)
                
                # Simulate trade
                trade_result = self.simulate_trade(
                    entry_price, sl_price, tp_price, entry_time, 
                    data_after_entry, direction
                )
                
                # Store trade
                trade = {
                    'date': date,
                    'tokyo_high': tokyo_high,
                    'tokyo_low': tokyo_low,
                    'tokyo_eq': tokyo_eq,
                    'manipulation_type': manipulation_type,
                    'direction': direction,
                    'fvg_timeframe': used_timeframe,
                    'fvg_top': selected_fvg.top,
                    'fvg_bottom': selected_fvg.bottom,
                    'fvg_formation_time': selected_fvg.formation_time,
                    'inversion_time': entry_time,
                    'entry_price': entry_price,
                    'manip_candle_high': manip_candle['High'],
                    'manip_candle_low': manip_candle['Low'],
                    'manip_candle_open': manip_candle['Open'],
                    'manip_candle_close': manip_candle['Close'],
                    'sl_type': sl_type,
                    'sl_price': sl_price,
                    'tp_level': rr_name,
                    'tp_price': tp_price,
                    'risk': risk,
                    'reward_target': risk * rr_ratio,
                    'rr_ratio': rr_ratio,
                    'result': trade_result['result'],
                    'exit_price': trade_result['exit_price'],
                    'exit_time': trade_result['exit_time'],
                    'pnl_r': trade_result['pnl_r']
                }
                
                day_trades.append(trade)
        
        return day_trades
    
    def run_backtest(self):
        """
        Run the complete backtest analysis.
        """
        print("\n" + "="*80)
        print("JUDAS SWING MULTI-TIMEFRAME STRATEGY BACKTEST")
        print("="*80 + "\n")
        
        # Get unique dates from 5m data
        self.data_5m['Date'] = self.data_5m['DateTime'].dt.date
        unique_dates = sorted(self.data_5m['Date'].unique())
        
        print(f"Analyzing {len(unique_dates)} unique days...\n")
        
        all_trades = []
        processed = 0
        
        for date in unique_dates:
            processed += 1
            if processed % 100 == 0:
                print(f"Processed {processed}/{len(unique_dates)} days... ({processed/len(unique_dates)*100:.1f}%)")
            
            day_trades = self.analyze_day(date)
            all_trades.extend(day_trades)
        
        print(f"\nCompleted analysis of {len(unique_dates)} days")
        print(f"Total trade setups detected: {len(all_trades)}")
        
        self.trades = all_trades
        
        return all_trades
    
    def generate_statistics(self):
        """
        Generate comprehensive statistics from trades.
        
        Returns:
            DataFrame with statistics by SL type, timeframe, and TP level
        """
        if len(self.trades) == 0:
            print("No trades to analyze")
            return None
        
        df = pd.DataFrame(self.trades)
        
        # Filter only completed trades (not OPEN)
        df = df[df['result'] != 'OPEN']
        
        print(f"\nAnalyzing {len(df)} completed trades...")
        
        # Group by SL type, timeframe, and TP level
        stats = []
        
        for sl_type in df['sl_type'].unique():
            for tf in df['fvg_timeframe'].unique():
                for tp_level in df['tp_level'].unique():
                    subset = df[
                        (df['sl_type'] == sl_type) & 
                        (df['fvg_timeframe'] == tf) & 
                        (df['tp_level'] == tp_level)
                    ]
                    
                    if len(subset) == 0:
                        continue
                    
                    wins = len(subset[subset['result'] == 'WIN'])
                    losses = len(subset[subset['result'] == 'LOSS'])
                    total = len(subset)
                    win_rate = (wins / total * 100) if total > 0 else 0
                    
                    # Calculate expectancy
                    avg_win = subset[subset['result'] == 'WIN']['pnl_r'].mean() if wins > 0 else 0
                    avg_loss = subset[subset['result'] == 'LOSS']['pnl_r'].mean() if losses > 0 else 0
                    expectancy = (win_rate / 100 * avg_win) + ((1 - win_rate / 100) * avg_loss)
                    
                    stats.append({
                        'SL_Type': sl_type,
                        'Timeframe': tf,
                        'TP_Level': tp_level,
                        'Total_Trades': total,
                        'Wins': wins,
                        'Losses': losses,
                        'Win_Rate_%': win_rate,
                        'Avg_Win_R': avg_win,
                        'Avg_Loss_R': avg_loss,
                        'Expectancy_R': expectancy
                    })
        
        stats_df = pd.DataFrame(stats)
        stats_df = stats_df.sort_values(['SL_Type', 'Timeframe', 'TP_Level'])
        
        return stats_df
    
    def create_comparison_table(self, stats_df):
        """
        Create comparison table as specified in requirements.
        
        Returns:
            DataFrame formatted for display
        """
        if stats_df is None or len(stats_df) == 0:
            return None
        
        # Pivot to get the desired format
        comparison_data = []
        
        for sl_type in stats_df['SL_Type'].unique():
            sl_subset = stats_df[stats_df['SL_Type'] == sl_type]
            
            for tf in sl_subset['Timeframe'].unique():
                tf_subset = sl_subset[sl_subset['Timeframe'] == tf]
                
                # Get win rates for each TP level
                wr_1r = tf_subset[tf_subset['TP_Level'] == '1R']['Win_Rate_%'].values
                wr_1r = wr_1r[0] if len(wr_1r) > 0 else 0
                
                wr_15r = tf_subset[tf_subset['TP_Level'] == '1.5R']['Win_Rate_%'].values
                wr_15r = wr_15r[0] if len(wr_15r) > 0 else 0
                
                wr_2r = tf_subset[tf_subset['TP_Level'] == '2R']['Win_Rate_%'].values
                wr_2r = wr_2r[0] if len(wr_2r) > 0 else 0
                
                # Get total trades
                total = tf_subset['Total_Trades'].sum() // 3  # Divide by 3 since each trade is tested with 3 TPs
                
                # Get expectancy for 1R
                exp_1r = tf_subset[tf_subset['TP_Level'] == '1R']['Expectancy_R'].values
                exp_1r = exp_1r[0] if len(exp_1r) > 0 else 0
                
                comparison_data.append({
                    'SL_Type': sl_type,
                    'TF_Used': tf,
                    'WR_1R_%': f"{wr_1r:.1f}%",
                    'WR_1.5R_%': f"{wr_15r:.1f}%",
                    'WR_2R_%': f"{wr_2r:.1f}%",
                    'Trades': int(total),
                    'Expectancy_1R': f"{exp_1r:+.3f}R"
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        return comparison_df
    
    def save_results(self, stats_df, comparison_df, filename='judas_swing_mtf_results.csv'):
        """
        Save detailed results to CSV.
        """
        # Save all trades
        if len(self.trades) > 0:
            trades_df = pd.DataFrame(self.trades)
            trades_df.to_csv(filename, index=False)
            print(f"\nDetailed trades saved to: {filename}")
        
        # Save statistics
        if stats_df is not None:
            stats_filename = filename.replace('.csv', '_statistics.csv')
            stats_df.to_csv(stats_filename, index=False)
            print(f"Statistics saved to: {stats_filename}")
        
        # Save comparison table
        if comparison_df is not None:
            comp_filename = filename.replace('.csv', '_comparison.csv')
            comparison_df.to_csv(comp_filename, index=False)
            print(f"Comparison table saved to: {comp_filename}")
    
    def create_visualizations(self, stats_df, comparison_df, filename='judas_swing_mtf_comparison.png'):
        """
        Create comprehensive visualizations.
        """
        if stats_df is None or len(stats_df) == 0:
            print("No data to visualize")
            return
        
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Win Rate Comparison by SL Type and TP Level
        ax1 = fig.add_subplot(gs[0, :2])
        for sl_type in stats_df['SL_Type'].unique():
            subset = stats_df[stats_df['SL_Type'] == sl_type]
            tp_levels = ['1R', '1.5R', '2R']
            win_rates = []
            for tp in tp_levels:
                wr = subset[subset['TP_Level'] == tp]['Win_Rate_%'].mean()
                win_rates.append(wr)
            ax1.plot(tp_levels, win_rates, marker='o', label=sl_type, linewidth=2, markersize=8)
        ax1.set_xlabel('TP Level', fontsize=12)
        ax1.set_ylabel('Win Rate (%)', fontsize=12)
        ax1.set_title('Win Rate by SL Type and TP Level', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Win Rate by Timeframe
        ax2 = fig.add_subplot(gs[0, 2])
        tf_stats = stats_df.groupby('Timeframe')['Win_Rate_%'].mean()
        colors = ['#2ecc71' if x > 50 else '#e74c3c' for x in tf_stats.values]
        tf_stats.plot(kind='bar', ax=ax2, color=colors)
        ax2.set_xlabel('Timeframe', fontsize=12)
        ax2.set_ylabel('Avg Win Rate (%)', fontsize=12)
        ax2.set_title('Win Rate by Timeframe', fontsize=14, fontweight='bold')
        ax2.axhline(y=50, color='black', linestyle='--', alpha=0.5)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Expectancy Comparison
        ax3 = fig.add_subplot(gs[1, :2])
        exp_data = stats_df[stats_df['TP_Level'] == '1R'].groupby(['SL_Type', 'Timeframe'])['Expectancy_R'].mean().unstack()
        exp_data.plot(kind='bar', ax=ax3, width=0.8)
        ax3.set_xlabel('SL Type', fontsize=12)
        ax3.set_ylabel('Expectancy (R)', fontsize=12)
        ax3.set_title('Expectancy Comparison (1R Target)', fontsize=14, fontweight='bold')
        ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax3.legend(title='Timeframe')
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Number of Trades Distribution
        ax4 = fig.add_subplot(gs[1, 2])
        trade_counts = stats_df.groupby('Timeframe')['Total_Trades'].sum() / 3  # Divide by 3 TPs
        trade_counts.plot(kind='pie', ax=ax4, autopct='%1.1f%%', startangle=90)
        ax4.set_ylabel('')
        ax4.set_title('Trade Distribution by Timeframe', fontsize=14, fontweight='bold')
        
        # 5. Heatmap: Win Rate by SL Type and TP Level
        ax5 = fig.add_subplot(gs[2, :])
        pivot_data = stats_df.pivot_table(
            values='Win_Rate_%', 
            index='SL_Type', 
            columns=['Timeframe', 'TP_Level'],
            aggfunc='mean'
        )
        sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='RdYlGn', center=50, 
                    ax=ax5, cbar_kws={'label': 'Win Rate (%)'})
        ax5.set_title('Win Rate Heatmap: SL Type vs (Timeframe, TP Level)', 
                      fontsize=14, fontweight='bold')
        ax5.set_xlabel('Timeframe & TP Level', fontsize=12)
        ax5.set_ylabel('SL Type', fontsize=12)
        
        plt.suptitle('Judas Swing Multi-Timeframe Strategy - Complete Analysis', 
                     fontsize=16, fontweight='bold', y=0.995)
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\nVisualizations saved to: {filename}")
        plt.close()
    
    def generate_report(self, stats_df, comparison_df, filename='JUDAS_SWING_MTF_ANALYSIS.md'):
        """
        Generate comprehensive markdown report.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Judas Swing + Inversion FVG - Multi-Timeframe Strategy Analysis\n\n")
            f.write("## Executive Summary\n\n")
            f.write("This report presents the results of an advanced backtesting strategy combining:\n")
            f.write("- Multi-timeframe Fair Value Gap (FVG) analysis (5m and 1m)\n")
            f.write("- Hierarchical timeframe priority (5m > 1m)\n")
            f.write("- A/B testing of Stop Loss placement (Body vs Wick)\n")
            f.write("- Multiple Take Profit levels (1R, 1.5R, 2R)\n\n")
            
            f.write("## Strategy Rules\n\n")
            f.write("### 1. Tokyo Session Identification\n")
            f.write("- Tokyo Session: 19:00 - 00:00\n")
            f.write("- Record High, Low, and 50% Equilibrium\n\n")
            
            f.write("### 2. Manipulation Detection\n")
            f.write("- Manipulation Zone: 02:00 - 02:30 (London session)\n")
            f.write("- Condition: Price breaks Tokyo High (SHORT) or Low (LONG)\n\n")
            
            f.write("### 3. Multi-Timeframe FVG Detection\n")
            f.write("**Priority Rule:**\n")
            f.write("- **Case A (Priority)**: If 5m FVG exists → Use 5m FVG for entry\n")
            f.write("- **Case B (Secondary)**: If NO 5m FVG → Use 1m FVG for entry\n\n")
            
            f.write("### 4. Entry Trigger\n")
            f.write("- Wait for price to reverse and fill the FVG\n")
            f.write("- Entry: Close of candle that closes beyond FVG\n\n")
            
            f.write("### 5. Stop Loss A/B Testing\n")
            f.write("**Two SL options tested:**\n")
            f.write("- **SL-Body**: Placed beyond body of manipulation candle\n")
            f.write("- **SL-Wick**: Placed at absolute wick extreme of manipulation candle\n\n")
            
            f.write("### 6. Take Profit Levels\n")
            f.write("- **TP 1R**: Risk/Reward ratio of 1:1\n")
            f.write("- **TP 1.5R**: Risk/Reward ratio of 1:1.5\n")
            f.write("- **TP 2R**: Risk/Reward ratio of 1:2\n\n")
            
            f.write("## Data Analysis Period\n\n")
            if len(self.trades) > 0:
                df = pd.DataFrame(self.trades)
                f.write(f"- **Start Date**: {df['date'].min()}\n")
                f.write(f"- **End Date**: {df['date'].max()}\n")
                f.write(f"- **Total Days Analyzed**: {df['date'].nunique()}\n")
                f.write(f"- **Total Trade Setups**: {len(df) // 6} (tested with 6 configurations each)\n\n")
            
            f.write("## Results Summary\n\n")
            f.write("### Comparison Table\n\n")
            if comparison_df is not None:
                f.write(comparison_df.to_markdown(index=False))
                f.write("\n\n")
            
            f.write("### Detailed Statistics\n\n")
            if stats_df is not None:
                f.write(stats_df.to_markdown(index=False))
                f.write("\n\n")
            
            f.write("## Key Findings\n\n")
            if stats_df is not None and len(stats_df) > 0:
                # Find best configuration
                best_row = stats_df.loc[stats_df['Expectancy_R'].idxmax()]
                f.write(f"### Best Configuration\n")
                f.write(f"- **SL Type**: {best_row['SL_Type']}\n")
                f.write(f"- **Timeframe**: {best_row['Timeframe']}\n")
                f.write(f"- **TP Level**: {best_row['TP_Level']}\n")
                f.write(f"- **Win Rate**: {best_row['Win_Rate_%']:.1f}%\n")
                f.write(f"- **Expectancy**: {best_row['Expectancy_R']:+.3f}R\n")
                f.write(f"- **Total Trades**: {best_row['Total_Trades']}\n\n")
                
                # Timeframe usage
                tf_usage = stats_df.groupby('Timeframe')['Total_Trades'].sum()
                f.write(f"### Timeframe Usage\n")
                for tf, count in tf_usage.items():
                    pct = count / tf_usage.sum() * 100 / 3  # Divide by 3 for TP levels
                    f.write(f"- **{tf}**: {int(count/3)} trades ({pct:.1f}%)\n")
                f.write("\n")
                
                # SL Type comparison
                f.write(f"### SL Type Performance (1R Target)\n")
                sl_comp = stats_df[stats_df['TP_Level'] == '1R'].groupby('SL_Type').agg({
                    'Win_Rate_%': 'mean',
                    'Expectancy_R': 'mean'
                })
                for sl_type, row in sl_comp.iterrows():
                    f.write(f"- **{sl_type}**: WR={row['Win_Rate_%']:.1f}%, Exp={row['Expectancy_R']:+.3f}R\n")
                f.write("\n")
            
            f.write("## Recommendations\n\n")
            if stats_df is not None and len(stats_df) > 0:
                best = stats_df.loc[stats_df['Expectancy_R'].idxmax()]
                f.write(f"Based on the backtest results, the optimal configuration is:\n\n")
                f.write(f"1. **Use {best['SL_Type']}** for stop loss placement\n")
                f.write(f"2. **Prioritize {best['Timeframe']} timeframe** for FVG detection\n")
                f.write(f"3. **Target {best['TP_Level']}** for best risk/reward balance\n\n")
                
                f.write("This configuration provides:\n")
                f.write(f"- Win Rate: {best['Win_Rate_%']:.1f}%\n")
                f.write(f"- Positive Expectancy: {best['Expectancy_R']:+.3f}R per trade\n\n")
            
            f.write("## Notes and Limitations\n\n")
            f.write("- This backtest uses historical data and past performance does not guarantee future results\n")
            f.write("- Slippage, commissions, and spreads are not included in this analysis\n")
            f.write("- Market conditions may vary significantly from the backtest period\n")
            f.write("- The strategy assumes perfect execution at specified price levels\n\n")
            
            f.write("## Methodology\n\n")
            f.write("1. Load 5m and 1m historical data (2018-2025)\n")
            f.write("2. For each trading day:\n")
            f.write("   - Identify Tokyo session High/Low\n")
            f.write("   - Check for manipulation in 02:00-02:30 window\n")
            f.write("   - Detect FVGs on both 5m and 1m timeframes\n")
            f.write("   - Apply priority rule (5m > 1m)\n")
            f.write("   - Wait for FVG inversion signal\n")
            f.write("   - Test both SL options with 3 TP levels\n")
            f.write("3. Simulate each trade to determine outcome (WIN/LOSS)\n")
            f.write("4. Calculate statistics and generate comparison tables\n\n")
            
            f.write("---\n\n")
            f.write(f"*Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"\nMarkdown report saved to: {filename}")


def main():
    """Main execution function."""
    # Set working directory
    data_dir = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    
    # Initialize analyzer
    print("Initializing Multi-Timeframe Analyzer...")
    analyzer = JudasSwingMTFAnalyzer(data_dir)
    
    # Load data
    analyzer.load_data(years=range(2018, 2026))
    
    if analyzer.data_5m is None or len(analyzer.data_5m) == 0:
        print("ERROR: No 5m data loaded. Cannot proceed.")
        return
    
    # Run backtest
    trades = analyzer.run_backtest()
    
    if len(trades) == 0:
        print("\nNo trades detected. Analysis complete.")
        return
    
    # Generate statistics
    stats_df = analyzer.generate_statistics()
    
    # Create comparison table
    comparison_df = analyzer.create_comparison_table(stats_df)
    
    # Display results
    print("\n" + "="*80)
    print("COMPARISON TABLE")
    print("="*80 + "\n")
    if comparison_df is not None:
        print(comparison_df.to_string(index=False))
    
    print("\n" + "="*80)
    print("DETAILED STATISTICS")
    print("="*80 + "\n")
    if stats_df is not None:
        print(stats_df.to_string(index=False))
    
    # Save results
    analyzer.save_results(stats_df, comparison_df)
    
    # Create visualizations
    analyzer.create_visualizations(stats_df, comparison_df)
    
    # Generate report
    analyzer.generate_report(stats_df, comparison_df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  - judas_swing_mtf_results.csv (all trades)")
    print("  - judas_swing_mtf_results_statistics.csv (detailed stats)")
    print("  - judas_swing_mtf_results_comparison.csv (comparison table)")
    print("  - judas_swing_mtf_comparison.png (visualizations)")
    print("  - JUDAS_SWING_MTF_ANALYSIS.md (comprehensive report)")


if __name__ == "__main__":
    main()
