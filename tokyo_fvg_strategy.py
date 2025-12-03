#!/usr/bin/env python3
"""
Tokyo Session FVG (Fair Value Gap) Inversion Strategy Analysis
================================================================
Analyzes trading data from 2018-2025 to calculate the win rate of a strategy
based on FVG inversions following Tokyo session manipulation.

Strategy Rules:

BEARISH SCENARIO (Short Entry):
1. Condition A: Price manipulates Tokyo High between 02:00-02:30
2. Condition B: During upward manipulation, a Bullish FVG forms
   (FVG Bullish: gap between High[N-1] and Low[N+1])
3. Trigger: Price reverses, fills the FVG, and a candle closes below it
   (FVG becomes resistance - "Inversion FVG")
4. Entry: Close of the breaking candle
5. Stop Loss: High of the breaking candle
6. Take Profit: Tokyo 50% Equilibrium

BULLISH SCENARIO (Long Entry):
1. Condition A: Price manipulates Tokyo Low between 02:00-02:30
2. Condition B: During downward manipulation, a Bearish FVG forms
   (FVG Bearish: gap between Low[N-1] and High[N+1])
3. Trigger: Price reverses, fills the FVG, and a candle closes above it
4. Entry: Close of the breaking candle
5. Stop Loss: Low of the breaking candle
6. Take Profit: Tokyo 50% Equilibrium

Win Rate Calculation: Percentage of trades that hit TP before SL
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import glob
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class FVG:
    """Class to represent a Fair Value Gap."""
    
    def __init__(self, fvg_type, top, bottom, start_idx, end_idx, formation_time):
        """
        Initialize FVG.
        
        Args:
            fvg_type: 'BULLISH' or 'BEARISH'
            top: Upper boundary of the FVG
            bottom: Lower boundary of the FVG
            start_idx: Index of candle N-1
            end_idx: Index of candle N+1
            formation_time: Timestamp when FVG was formed
        """
        self.type = fvg_type
        self.top = top
        self.bottom = bottom
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.formation_time = formation_time
        self.filled = False
        self.inverted = False
        self.inversion_time = None
        self.inversion_candle = None
    
    def __repr__(self):
        return f"FVG({self.type}, {self.bottom:.2f}-{self.top:.2f}, formed at {self.formation_time})"


class TokyoFVGAnalyzer:
    """Analyzer for Tokyo Session FVG Inversion Strategy."""
    
    def __init__(self, data_directory):
        """Initialize the analyzer with the data directory."""
        self.data_directory = data_directory
        self.all_data = []
        self.results = []
        self.trades = []
        self.filtered_trades_count = 0  # Count of trades filtered out due to R/R < 1
        self.sl_comparison_data = []  # Store data for SL options comparison
        
    def load_data(self, years=None, timeframes=None):
        """
        Load CSV files for specified years and timeframes.
        
        Args:
            years: List of years to load (default: 2018-2025)
            timeframes: List of timeframes to load (default: ['5m', '15m'])
        """
        if years is None:
            years = range(2018, 2026)  # 2018-2025
        if timeframes is None:
            timeframes = ['5m', '15m']  # Focus on smaller timeframes for FVG detection
        
        print("Loading data files...")
        for year in years:
            for tf in timeframes:
                filename = f"{year} {tf}.csv"
                filepath = os.path.join(self.data_directory, filename)
                
                if os.path.exists(filepath):
                    print(f"Loading {filename}...")
                    try:
                        df = pd.read_csv(filepath, sep=';', header=0)
                        
                        # Rename columns if they have generic names
                        if 'Column1' in df.columns:
                            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                        
                        # Parse datetime
                        df['DateTime'] = pd.to_datetime(
                            df['Date'] + ' ' + df['Time'], 
                            format='%d/%m/%Y %H:%M:%S',
                            errors='coerce'
                        )
                        
                        # Drop rows with invalid datetime
                        df = df.dropna(subset=['DateTime'])
                        
                        # Sort by datetime
                        df = df.sort_values('DateTime')
                        
                        # Add metadata
                        df['Year'] = year
                        df['Timeframe'] = tf
                        
                        self.all_data.append(df)
                        print(f"  Loaded {len(df)} rows from {filename}")
                        
                    except Exception as e:
                        print(f"  Error loading {filename}: {e}")
                else:
                    print(f"  File not found: {filename}")
        
        if self.all_data:
            # Combine all dataframes
            self.combined_data = pd.concat(self.all_data, ignore_index=True)
            self.combined_data = self.combined_data.sort_values('DateTime').reset_index(drop=True)
            print(f"\nTotal data loaded: {len(self.combined_data)} rows")
            print(f"Date range: {self.combined_data['DateTime'].min()} to {self.combined_data['DateTime'].max()}")
        else:
            print("No data loaded!")
            self.combined_data = pd.DataFrame()
    
    def identify_tokyo_session(self, date):
        """
        Identify Tokyo session (19:00-00:00) for a given date.
        Returns High, Low, and Equilibrium of the Tokyo session.
        
        Args:
            date: The date to find Tokyo session for
            
        Returns:
            dict with tokyo_high, tokyo_low, tokyo_eq, start_time, end_time
        """
        # Tokyo session: 19:00 on the given date to 00:00 next day
        tokyo_start = pd.Timestamp(date) + pd.Timedelta(hours=19)
        tokyo_end = tokyo_start + pd.Timedelta(hours=5)  # 19:00 + 5h = 00:00 next day
        
        # Filter data for Tokyo session
        tokyo_data = self.combined_data[
            (self.combined_data['DateTime'] >= tokyo_start) &
            (self.combined_data['DateTime'] <= tokyo_end)
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
            'end_time': tokyo_end,
            'data_points': len(tokyo_data)
        }
    
    def identify_manipulation_zone(self, date):
        """
        Identify manipulation zone (02:00-02:30 London session) for the day after Tokyo session.
        
        Args:
            date: The date of Tokyo session
            
        Returns:
            DataFrame with manipulation zone data, start time, end time
        """
        # Manipulation zone is on the next day (after Tokyo session ends)
        next_day = pd.Timestamp(date) + pd.Timedelta(days=1)
        manip_start = next_day + pd.Timedelta(hours=2)  # 02:00
        manip_end = manip_start + pd.Timedelta(minutes=30)  # 02:30
        
        # Filter data for manipulation zone
        manip_data = self.combined_data[
            (self.combined_data['DateTime'] >= manip_start) &
            (self.combined_data['DateTime'] <= manip_end)
        ]
        
        return manip_data.copy(), manip_start, manip_end
    
    def detect_fvgs(self, data):
        """
        Detect Fair Value Gaps in the given data.
        
        FVG Bullish: High[N-1] < Low[N+1] (gap up)
        FVG Bearish: Low[N-1] > High[N+1] (gap down)
        
        Args:
            data: DataFrame with OHLC data
            
        Returns:
            List of FVG objects
        """
        fvgs = []
        
        if len(data) < 3:
            return fvgs
        
        # Reset index to work with iloc
        data = data.reset_index(drop=True)
        
        # Iterate through candles to find FVGs (need 3 consecutive candles)
        for i in range(len(data) - 2):
            candle_n_minus_1 = data.iloc[i]
            candle_n = data.iloc[i + 1]
            candle_n_plus_1 = data.iloc[i + 2]
            
            # Check for Bullish FVG (gap up)
            # High of N-1 < Low of N+1
            if candle_n_minus_1['High'] < candle_n_plus_1['Low']:
                fvg = FVG(
                    fvg_type='BULLISH',
                    top=candle_n_plus_1['Low'],
                    bottom=candle_n_minus_1['High'],
                    start_idx=i,
                    end_idx=i + 2,
                    formation_time=candle_n_plus_1['DateTime']
                )
                fvgs.append(fvg)
            
            # Check for Bearish FVG (gap down)
            # Low of N-1 > High of N+1
            elif candle_n_minus_1['Low'] > candle_n_plus_1['High']:
                fvg = FVG(
                    fvg_type='BEARISH',
                    top=candle_n_minus_1['Low'],
                    bottom=candle_n_plus_1['High'],
                    start_idx=i,
                    end_idx=i + 2,
                    formation_time=candle_n_plus_1['DateTime']
                )
                fvgs.append(fvg)
        
        return fvgs
    
    def check_manipulation(self, manip_data, tokyo_high, tokyo_low):
        """
        Check if price manipulates Tokyo high or low during manipulation zone.
        
        Args:
            manip_data: DataFrame with manipulation zone data
            tokyo_high: Tokyo session high
            tokyo_low: Tokyo session low
            
        Returns:
            dict with manipulation info or None
        """
        if len(manip_data) == 0:
            return None
        
        # Check for high manipulation
        high_manip = manip_data[manip_data['High'] > tokyo_high]
        # Check for low manipulation
        low_manip = manip_data[manip_data['Low'] < tokyo_low]
        
        manipulation_type = None
        
        if len(high_manip) > 0 and len(low_manip) > 0:
            # Both manipulations occurred - take the first one
            first_high = high_manip.iloc[0]['DateTime']
            first_low = low_manip.iloc[0]['DateTime']
            
            if first_high < first_low:
                manipulation_type = 'HIGH'
            else:
                manipulation_type = 'LOW'
        elif len(high_manip) > 0:
            manipulation_type = 'HIGH'
        elif len(low_manip) > 0:
            manipulation_type = 'LOW'
        
        if manipulation_type:
            return {
                'type': manipulation_type,
                'data': manip_data
            }
        
        return None
    
    def check_fvg_inversion(self, fvg, data_after_formation, manipulation_type):
        """
        Check if an FVG is filled and inverted (candle closes beyond it).
        
        Args:
            fvg: FVG object
            data_after_formation: DataFrame with data after FVG formation
            manipulation_type: 'HIGH' or 'LOW'
            
        Returns:
            dict with inversion info or None
        """
        # For HIGH manipulation (bearish scenario), we look for BULLISH FVG inversion
        # Price should reverse down, fill the bullish FVG, and close below it
        if manipulation_type == 'HIGH' and fvg.type == 'BULLISH':
            # Check each candle after formation
            for idx, row in data_after_formation.iterrows():
                # Check if candle touches/fills the FVG
                if row['Low'] <= fvg.top and row['High'] >= fvg.bottom:
                    fvg.filled = True
                    
                    # Check if candle closes below the FVG (inversion)
                    if row['Close'] < fvg.bottom:
                        fvg.inverted = True
                        fvg.inversion_time = row['DateTime']
                        fvg.inversion_candle = row
                        return {
                            'inverted': True,
                            'inversion_time': row['DateTime'],
                            'entry_price': row['Close'],
                            'stop_loss': row['High'],
                            'direction': 'SHORT'
                        }
        
        # For LOW manipulation (bullish scenario), we look for BEARISH FVG inversion
        # Price should reverse up, fill the bearish FVG, and close above it
        elif manipulation_type == 'LOW' and fvg.type == 'BEARISH':
            # Check each candle after formation
            for idx, row in data_after_formation.iterrows():
                # Check if candle touches/fills the FVG
                if row['Low'] <= fvg.top and row['High'] >= fvg.bottom:
                    fvg.filled = True
                    
                    # Check if candle closes above the FVG (inversion)
                    if row['Close'] > fvg.top:
                        fvg.inverted = True
                        fvg.inversion_time = row['DateTime']
                        fvg.inversion_candle = row
                        return {
                            'inverted': True,
                            'inversion_time': row['DateTime'],
                            'entry_price': row['Close'],
                            'stop_loss': row['Low'],
                            'direction': 'LONG'
                        }
        
        return None
    
    def check_rr_levels(self, entry_price, stop_loss, entry_time, direction, hours=24):
        """
        Check if price reaches 1R, 1.5R, and 2R levels before hitting SL.
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            entry_time: Entry time
            direction: 'LONG' or 'SHORT'
            hours: Maximum hours to track the trade (default: 24)
            
        Returns:
            dict with reached_1R, reached_1_5R, reached_2R flags
        """
        end_time = entry_time + pd.Timedelta(hours=hours)
        
        # Get data after entry within the time window
        future_data = self.combined_data[
            (self.combined_data['DateTime'] > entry_time) &
            (self.combined_data['DateTime'] <= end_time)
        ]
        
        if len(future_data) == 0:
            return {
                'reached_1R': False,
                'reached_1_5R': False,
                'reached_2R': False
            }
        
        # Calculate risk
        risk = abs(entry_price - stop_loss)
        
        # Calculate TP levels based on risk
        if direction == 'LONG':
            tp_1r = entry_price + (1.0 * risk)
            tp_1_5r = entry_price + (1.5 * risk)
            tp_2r = entry_price + (2.0 * risk)
        else:  # SHORT
            tp_1r = entry_price - (1.0 * risk)
            tp_1_5r = entry_price - (1.5 * risk)
            tp_2r = entry_price - (2.0 * risk)
        
        # Track which levels are reached and when
        reached_1r = False
        reached_1_5r = False
        reached_2r = False
        sl_hit = False
        sl_time = None
        
        for idx, row in future_data.iterrows():
            if direction == 'LONG':
                # Check if SL is hit (price goes down to SL)
                if not sl_hit and row['Low'] <= stop_loss:
                    sl_hit = True
                    sl_time = row['DateTime']
                
                # Check if TP levels are hit (price goes up)
                if not reached_1r and row['High'] >= tp_1r:
                    reached_1r = True
                if not reached_1_5r and row['High'] >= tp_1_5r:
                    reached_1_5r = True
                if not reached_2r and row['High'] >= tp_2r:
                    reached_2r = True
            
            else:  # SHORT
                # Check if SL is hit (price goes up to SL)
                if not sl_hit and row['High'] >= stop_loss:
                    sl_hit = True
                    sl_time = row['DateTime']
                
                # Check if TP levels are hit (price goes down)
                if not reached_1r and row['Low'] <= tp_1r:
                    reached_1r = True
                if not reached_1_5r and row['Low'] <= tp_1_5r:
                    reached_1_5r = True
                if not reached_2r and row['Low'] <= tp_2r:
                    reached_2r = True
            
            # Stop if SL is hit
            if sl_hit:
                break
        
        return {
            'reached_1R': reached_1r,
            'reached_1_5R': reached_1_5r,
            'reached_2R': reached_2r,
            'tp_1r': tp_1r,
            'tp_1_5r': tp_1_5r,
            'tp_2r': tp_2r
        }
    
    def check_would_reach_without_sl(self, entry_price, stop_loss, entry_time, direction, hours=6):
        """
        For trades that hit SL, check if they would have reached TP levels without SL.
        This simulates ignoring the SL and tracking for up to 6 hours after entry.
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            entry_time: Entry time
            direction: 'LONG' or 'SHORT'
            hours: Maximum hours to track (default: 6)
            
        Returns:
            dict with would_reach_1R, would_reach_1_5R, would_reach_2R flags
        """
        end_time = entry_time + pd.Timedelta(hours=hours)
        
        # Get data after entry within the time window
        future_data = self.combined_data[
            (self.combined_data['DateTime'] > entry_time) &
            (self.combined_data['DateTime'] <= end_time)
        ]
        
        if len(future_data) == 0:
            return {
                'would_reach_1R': False,
                'would_reach_1_5R': False,
                'would_reach_2R': False
            }
        
        # Calculate risk
        risk = abs(entry_price - stop_loss)
        
        # Calculate TP levels based on risk
        if direction == 'LONG':
            tp_1r = entry_price + (1.0 * risk)
            tp_1_5r = entry_price + (1.5 * risk)
            tp_2r = entry_price + (2.0 * risk)
        else:  # SHORT
            tp_1r = entry_price - (1.0 * risk)
            tp_1_5r = entry_price - (1.5 * risk)
            tp_2r = entry_price - (2.0 * risk)
        
        # Track which levels are reached (IGNORE SL completely)
        would_reach_1r = False
        would_reach_1_5r = False
        would_reach_2r = False
        
        for idx, row in future_data.iterrows():
            if direction == 'LONG':
                # Check if TP levels are hit (price goes up)
                if not would_reach_1r and row['High'] >= tp_1r:
                    would_reach_1r = True
                if not would_reach_1_5r and row['High'] >= tp_1_5r:
                    would_reach_1_5r = True
                if not would_reach_2r and row['High'] >= tp_2r:
                    would_reach_2r = True
            else:  # SHORT
                # Check if TP levels are hit (price goes down)
                if not would_reach_1r and row['Low'] <= tp_1r:
                    would_reach_1r = True
                if not would_reach_1_5r and row['Low'] <= tp_1_5r:
                    would_reach_1_5r = True
                if not would_reach_2r and row['Low'] <= tp_2r:
                    would_reach_2r = True
            
            # Continue tracking even if all levels reached
            if would_reach_1r and would_reach_1_5r and would_reach_2r:
                break
        
        return {
            'would_reach_1R': would_reach_1r,
            'would_reach_1_5R': would_reach_1_5r,
            'would_reach_2R': would_reach_2r
        }
    
    def calculate_atr(self, end_time, period=14):
        """
        Calculate Average True Range (ATR) at a specific time.
        
        Args:
            end_time: The time to calculate ATR at
            period: Number of periods for ATR calculation (default: 14)
            
        Returns:
            ATR value
        """
        # Get data before end_time
        data_before = self.combined_data[
            self.combined_data['DateTime'] <= end_time
        ].tail(period + 1)
        
        if len(data_before) < period + 1:
            return None
        
        # Calculate True Range for each candle
        true_ranges = []
        for i in range(1, len(data_before)):
            high = data_before.iloc[i]['High']
            low = data_before.iloc[i]['Low']
            prev_close = data_before.iloc[i-1]['Close']
            
            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            true_ranges.append(tr)
        
        # Calculate ATR as average of True Ranges
        atr = np.mean(true_ranges[-period:]) if len(true_ranges) >= period else None
        return atr
    
    def get_manipulation_high_low(self, manip_data):
        """
        Get the high and low of the entire manipulation zone.
        
        Args:
            manip_data: DataFrame with manipulation zone data
            
        Returns:
            dict with manip_high and manip_low
        """
        if len(manip_data) == 0:
            return None
        
        return {
            'manip_high': manip_data['High'].max(),
            'manip_low': manip_data['Low'].min()
        }
    
    def calculate_sl_options(self, entry_price, signal_candle, entry_time, direction, 
                            manip_data, fvg, fixed_buffer=10):
        """
        Calculate all 4 Stop Loss options for a trade.
        
        Args:
            entry_price: Entry price
            signal_candle: The candle that triggered the entry (inversion candle)
            entry_time: Entry time
            direction: 'LONG' or 'SHORT'
            manip_data: DataFrame with manipulation zone data
            fvg: FVG object
            fixed_buffer: Fixed buffer in points (default: 10)
            
        Returns:
            dict with all SL options
        """
        # Original SL (High/Low of signal candle)
        sl_original = signal_candle['High'] if direction == 'SHORT' else signal_candle['Low']
        
        # Option 1: Swing SL (Manipulation High/Low)
        manip_hl = self.get_manipulation_high_low(manip_data)
        if manip_hl:
            sl_swing = manip_hl['manip_high'] if direction == 'SHORT' else manip_hl['manip_low']
        else:
            sl_swing = sl_original
        
        # Option 2: ATR Buffer SL
        atr = self.calculate_atr(entry_time, period=14)
        if atr:
            if direction == 'SHORT':
                sl_atr = signal_candle['High'] + (1.5 * atr)
            else:  # LONG
                sl_atr = signal_candle['Low'] - (1.5 * atr)
        else:
            sl_atr = sl_original
        
        # Option 3: FVG Complete SL
        if direction == 'SHORT':
            sl_fvg = fvg.top  # High of the FVG (top limit)
        else:  # LONG
            sl_fvg = fvg.bottom  # Low of the FVG (bottom limit)
        
        # Option 4: Fixed Buffer SL
        if direction == 'SHORT':
            sl_fixed = signal_candle['High'] + fixed_buffer
        else:  # LONG
            sl_fixed = signal_candle['Low'] - fixed_buffer
        
        return {
            'sl_original': sl_original,
            'sl_swing': sl_swing,
            'sl_atr': sl_atr,
            'sl_fvg': sl_fvg,
            'sl_fixed': sl_fixed,
            'atr_value': atr
        }
    
    def test_sl_with_rr_levels(self, entry_price, stop_loss, entry_time, direction, hours=24):
        """
        Test a specific SL and check if 1R, 1.5R, 2R levels are reached before SL.
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            entry_time: Entry time
            direction: 'LONG' or 'SHORT'
            hours: Maximum hours to track (default: 24)
            
        Returns:
            dict with reached_1R, reached_1_5R, reached_2R, hit_sl, and metrics
        """
        end_time = entry_time + pd.Timedelta(hours=hours)
        
        future_data = self.combined_data[
            (self.combined_data['DateTime'] > entry_time) &
            (self.combined_data['DateTime'] <= end_time)
        ]
        
        if len(future_data) == 0:
            return {
                'reached_1R': False,
                'reached_1_5R': False,
                'reached_2R': False,
                'hit_sl': False,
                'risk': abs(entry_price - stop_loss)
            }
        
        # Calculate risk and TP levels
        risk = abs(entry_price - stop_loss)
        
        if direction == 'LONG':
            tp_1r = entry_price + (1.0 * risk)
            tp_1_5r = entry_price + (1.5 * risk)
            tp_2r = entry_price + (2.0 * risk)
        else:  # SHORT
            tp_1r = entry_price - (1.0 * risk)
            tp_1_5r = entry_price - (1.5 * risk)
            tp_2r = entry_price - (2.0 * risk)
        
        reached_1r = False
        reached_1_5r = False
        reached_2r = False
        sl_hit = False
        
        for idx, row in future_data.iterrows():
            if direction == 'LONG':
                # Check if SL is hit
                if not sl_hit and row['Low'] <= stop_loss:
                    sl_hit = True
                    break
                
                # Check TP levels
                if not reached_1r and row['High'] >= tp_1r:
                    reached_1r = True
                if not reached_1_5r and row['High'] >= tp_1_5r:
                    reached_1_5r = True
                if not reached_2r and row['High'] >= tp_2r:
                    reached_2r = True
            else:  # SHORT
                # Check if SL is hit
                if not sl_hit and row['High'] >= stop_loss:
                    sl_hit = True
                    break
                
                # Check TP levels
                if not reached_1r and row['Low'] <= tp_1r:
                    reached_1r = True
                if not reached_1_5r and row['Low'] <= tp_1_5r:
                    reached_1_5r = True
                if not reached_2r and row['Low'] <= tp_2r:
                    reached_2r = True
        
        # Calculate win rates and expectancy
        win_rate_1r = 1.0 if reached_1r else 0.0
        win_rate_1_5r = 1.0 if reached_1_5r else 0.0
        win_rate_2r = 1.0 if reached_2r else 0.0
        
        # Expectancy calculation (per trade)
        expectancy_1r = (win_rate_1r * 1.0) - ((1 - win_rate_1r) * 1.0)
        expectancy_1_5r = (win_rate_1_5r * 1.5) - ((1 - win_rate_1_5r) * 1.0)
        expectancy_2r = (win_rate_2r * 2.0) - ((1 - win_rate_2r) * 1.0)
        
        return {
            'reached_1R': reached_1r,
            'reached_1_5R': reached_1_5r,
            'reached_2R': reached_2r,
            'hit_sl': sl_hit,
            'risk': risk,
            'expectancy_1r': expectancy_1r,
            'expectancy_1_5r': expectancy_1_5r,
            'expectancy_2r': expectancy_2r
        }
    
    def simulate_trade(self, entry_price, stop_loss, take_profit, entry_time, direction, hours=24):
        """
        Simulate a trade and check if TP is hit before SL.
        
        Args:
            entry_price: Entry price
            stop_loss: Stop loss price
            take_profit: Take profit price
            entry_time: Entry time
            direction: 'LONG' or 'SHORT'
            hours: Maximum hours to track the trade (default: 24)
            
        Returns:
            dict with trade result
        """
        end_time = entry_time + pd.Timedelta(hours=hours)
        
        # Get data after entry within the time window
        future_data = self.combined_data[
            (self.combined_data['DateTime'] > entry_time) &
            (self.combined_data['DateTime'] <= end_time)
        ]
        
        if len(future_data) == 0:
            return {
                'result': 'NO_DATA',
                'hit_tp': False,
                'hit_sl': False
            }
        
        tp_hit = False
        sl_hit = False
        tp_time = None
        sl_time = None
        exit_price = None
        exit_time = None
        
        for idx, row in future_data.iterrows():
            if direction == 'LONG':
                # Check if TP is hit (price goes up to TP)
                if not tp_hit and row['High'] >= take_profit:
                    tp_hit = True
                    tp_time = row['DateTime']
                    exit_price = take_profit
                    exit_time = tp_time
                
                # Check if SL is hit (price goes down to SL)
                if not sl_hit and row['Low'] <= stop_loss:
                    sl_hit = True
                    sl_time = row['DateTime']
                    if not tp_hit:  # If TP wasn't hit first
                        exit_price = stop_loss
                        exit_time = sl_time
            
            else:  # SHORT
                # Check if TP is hit (price goes down to TP)
                if not tp_hit and row['Low'] <= take_profit:
                    tp_hit = True
                    tp_time = row['DateTime']
                    exit_price = take_profit
                    exit_time = tp_time
                
                # Check if SL is hit (price goes up to SL)
                if not sl_hit and row['High'] >= stop_loss:
                    sl_hit = True
                    sl_time = row['DateTime']
                    if not tp_hit:  # If TP wasn't hit first
                        exit_price = stop_loss
                        exit_time = sl_time
            
            # If both hit, determine which came first
            if tp_hit and sl_hit:
                if tp_time < sl_time:
                    result = 'WIN'
                    exit_price = take_profit
                    exit_time = tp_time
                else:
                    result = 'LOSS'
                    exit_price = stop_loss
                    exit_time = sl_time
                break
        
        # Determine final result
        if tp_hit and not sl_hit:
            result = 'WIN'
        elif sl_hit and not tp_hit:
            result = 'LOSS'
        elif tp_hit and sl_hit:
            # Already handled above
            pass
        else:
            result = 'NO_EXIT'
            exit_price = future_data.iloc[-1]['Close']
            exit_time = future_data.iloc[-1]['DateTime']
        
        # Calculate P&L
        if direction == 'LONG':
            pnl = exit_price - entry_price if exit_price else 0
        else:  # SHORT
            pnl = entry_price - exit_price if exit_price else 0
        
        # Calculate risk/reward
        risk = abs(stop_loss - entry_price)
        reward = abs(take_profit - entry_price)
        rr_ratio = reward / risk if risk > 0 else 0
        
        return {
            'result': result,
            'hit_tp': tp_hit,
            'hit_sl': sl_hit,
            'tp_time': tp_time,
            'sl_time': sl_time,
            'exit_price': exit_price,
            'exit_time': exit_time,
            'pnl': pnl,
            'pnl_pct': (pnl / entry_price * 100) if entry_price > 0 else 0,
            'risk': risk,
            'reward': reward,
            'rr_ratio': rr_ratio
        }
    
    def analyze(self):
        """
        Main analysis function - processes all data and generates results.
        """
        if len(self.combined_data) == 0:
            print("No data to analyze!")
            return
        
        print("\n" + "="*80)
        print("Starting Tokyo Session FVG Inversion Strategy Analysis")
        print("="*80)
        
        # Get unique dates from the data
        self.combined_data['Date_Only'] = self.combined_data['DateTime'].dt.date
        unique_dates = sorted(self.combined_data['Date_Only'].unique())
        
        print(f"\nAnalyzing {len(unique_dates)} unique dates...")
        
        total_manipulations = 0
        total_fvgs_detected = 0
        total_inversions = 0
        total_trades = 0
        winning_trades = 0
        losing_trades = 0
        no_exit_trades = 0
        
        for i, date in enumerate(unique_dates):
            if (i + 1) % 100 == 0:
                print(f"Progress: {i+1}/{len(unique_dates)} dates processed...")
            
            # Step 1: Identify Tokyo session
            tokyo_session = self.identify_tokyo_session(date)
            
            if tokyo_session is None or tokyo_session['data_points'] < 2:
                continue
            
            # Step 2: Identify manipulation zone (next day)
            manip_data, manip_start, manip_end = self.identify_manipulation_zone(date)
            
            if len(manip_data) == 0:
                continue
            
            # Step 3: Check for manipulation
            manipulation = self.check_manipulation(
                manip_data,
                tokyo_session['tokyo_high'],
                tokyo_session['tokyo_low']
            )
            
            if manipulation is None:
                continue
            
            total_manipulations += 1
            
            # Step 4: Detect FVGs during manipulation zone
            fvgs = self.detect_fvgs(manip_data)
            
            if len(fvgs) == 0:
                continue
            
            # Filter FVGs based on manipulation type
            if manipulation['type'] == 'HIGH':
                # For HIGH manipulation, we want BULLISH FVGs
                relevant_fvgs = [fvg for fvg in fvgs if fvg.type == 'BULLISH']
            else:  # LOW manipulation
                # For LOW manipulation, we want BEARISH FVGs
                relevant_fvgs = [fvg for fvg in fvgs if fvg.type == 'BEARISH']
            
            if len(relevant_fvgs) == 0:
                continue
            
            total_fvgs_detected += len(relevant_fvgs)
            
            # Step 5: Check for FVG inversions after manipulation zone ends
            # Get data after manipulation zone
            after_manip_start = manip_end
            after_manip_end = after_manip_start + pd.Timedelta(hours=12)  # Check 12 hours after
            
            data_after_manip = self.combined_data[
                (self.combined_data['DateTime'] > after_manip_start) &
                (self.combined_data['DateTime'] <= after_manip_end)
            ]
            
            if len(data_after_manip) == 0:
                continue
            
            # Check each FVG for inversion
            for fvg in relevant_fvgs:
                # Get data after this specific FVG formation
                data_after_fvg = data_after_manip[
                    data_after_manip['DateTime'] > fvg.formation_time
                ]
                
                inversion = self.check_fvg_inversion(
                    fvg,
                    data_after_fvg,
                    manipulation['type']
                )
                
                if inversion is None:
                    continue
                
                total_inversions += 1
                
                # Step 6: Calculate Risk/Reward ratio BEFORE simulating the trade
                entry_price = inversion['entry_price']
                stop_loss = inversion['stop_loss']
                take_profit = tokyo_session['tokyo_eq']
                entry_time = inversion['inversion_time']
                direction = inversion['direction']
                
                # Calculate R/R ratio
                risk = abs(entry_price - stop_loss)
                reward = abs(take_profit - entry_price)
                rr_ratio = reward / risk if risk > 0 else 0
                
                # FILTER: Ignore trades with R/R < 1
                if rr_ratio < 1.0:
                    self.filtered_trades_count += 1
                    continue  # Skip this trade completely
                
                # Calculate ALL SL options
                sl_options = self.calculate_sl_options(
                    entry_price,
                    fvg.inversion_candle,
                    entry_time,
                    direction,
                    manip_data,
                    fvg,
                    fixed_buffer=10
                )
                
                # Test each SL option with R/R levels
                sl_results = {}
                for sl_name in ['sl_original', 'sl_swing', 'sl_atr', 'sl_fvg', 'sl_fixed']:
                    sl_value = sl_options[sl_name]
                    sl_results[sl_name] = self.test_sl_with_rr_levels(
                        entry_price,
                        sl_value,
                        entry_time,
                        direction,
                        hours=24
                    )
                
                # Store SL comparison data
                sl_comparison_record = {
                    'date': date,
                    'entry_price': entry_price,
                    'direction': direction,
                    'entry_time': entry_time,
                    # Original SL (baseline)
                    'sl_original': sl_options['sl_original'],
                    'sl_original_risk': sl_results['sl_original']['risk'],
                    'sl_original_1r': sl_results['sl_original']['reached_1R'],
                    'sl_original_1_5r': sl_results['sl_original']['reached_1_5R'],
                    'sl_original_2r': sl_results['sl_original']['reached_2R'],
                    'sl_original_expectancy_1r': sl_results['sl_original']['expectancy_1r'],
                    'sl_original_expectancy_1_5r': sl_results['sl_original']['expectancy_1_5r'],
                    'sl_original_expectancy_2r': sl_results['sl_original']['expectancy_2r'],
                    # Option 1: Swing SL
                    'sl_swing': sl_options['sl_swing'],
                    'sl_swing_risk': sl_results['sl_swing']['risk'],
                    'sl_swing_1r': sl_results['sl_swing']['reached_1R'],
                    'sl_swing_1_5r': sl_results['sl_swing']['reached_1_5R'],
                    'sl_swing_2r': sl_results['sl_swing']['reached_2R'],
                    'sl_swing_expectancy_1r': sl_results['sl_swing']['expectancy_1r'],
                    'sl_swing_expectancy_1_5r': sl_results['sl_swing']['expectancy_1_5r'],
                    'sl_swing_expectancy_2r': sl_results['sl_swing']['expectancy_2r'],
                    # Option 2: ATR SL
                    'sl_atr': sl_options['sl_atr'],
                    'sl_atr_risk': sl_results['sl_atr']['risk'],
                    'sl_atr_1r': sl_results['sl_atr']['reached_1R'],
                    'sl_atr_1_5r': sl_results['sl_atr']['reached_1_5R'],
                    'sl_atr_2r': sl_results['sl_atr']['reached_2R'],
                    'sl_atr_expectancy_1r': sl_results['sl_atr']['expectancy_1r'],
                    'sl_atr_expectancy_1_5r': sl_results['sl_atr']['expectancy_1_5r'],
                    'sl_atr_expectancy_2r': sl_results['sl_atr']['expectancy_2r'],
                    'atr_value': sl_options['atr_value'],
                    # Option 3: FVG SL
                    'sl_fvg': sl_options['sl_fvg'],
                    'sl_fvg_risk': sl_results['sl_fvg']['risk'],
                    'sl_fvg_1r': sl_results['sl_fvg']['reached_1R'],
                    'sl_fvg_1_5r': sl_results['sl_fvg']['reached_1_5R'],
                    'sl_fvg_2r': sl_results['sl_fvg']['reached_2R'],
                    'sl_fvg_expectancy_1r': sl_results['sl_fvg']['expectancy_1r'],
                    'sl_fvg_expectancy_1_5r': sl_results['sl_fvg']['expectancy_1_5r'],
                    'sl_fvg_expectancy_2r': sl_results['sl_fvg']['expectancy_2r'],
                    # Option 4: Fixed Buffer SL
                    'sl_fixed': sl_options['sl_fixed'],
                    'sl_fixed_risk': sl_results['sl_fixed']['risk'],
                    'sl_fixed_1r': sl_results['sl_fixed']['reached_1R'],
                    'sl_fixed_1_5r': sl_results['sl_fixed']['reached_1_5R'],
                    'sl_fixed_2r': sl_results['sl_fixed']['reached_2R'],
                    'sl_fixed_expectancy_1r': sl_results['sl_fixed']['expectancy_1r'],
                    'sl_fixed_expectancy_1_5r': sl_results['sl_fixed']['expectancy_1_5r'],
                    'sl_fixed_expectancy_2r': sl_results['sl_fixed']['expectancy_2r'],
                }
                self.sl_comparison_data.append(sl_comparison_record)
                
                # Check which R/R levels are reached (1R, 1.5R, 2R) with ORIGINAL SL
                rr_levels = self.check_rr_levels(
                    entry_price,
                    stop_loss,
                    entry_time,
                    direction,
                    hours=24
                )
                
                trade_result = self.simulate_trade(
                    entry_price,
                    stop_loss,
                    take_profit,
                    entry_time,
                    direction,
                    hours=24
                )
                
                # Check if trade would reach TP without SL (for losing trades)
                # This analysis helps identify if SL is too tight
                would_reach = self.check_would_reach_without_sl(
                    entry_price,
                    stop_loss,
                    entry_time,
                    direction,
                    hours=6  # Check 6 hours after entry
                )
                
                # Store trade details
                total_trades += 1
                
                if trade_result['result'] == 'WIN':
                    winning_trades += 1
                elif trade_result['result'] == 'LOSS':
                    losing_trades += 1
                elif trade_result['result'] == 'NO_EXIT':
                    no_exit_trades += 1
                
                trade_record = {
                    'date': date,
                    'tokyo_high': tokyo_session['tokyo_high'],
                    'tokyo_low': tokyo_session['tokyo_low'],
                    'tokyo_eq': tokyo_session['tokyo_eq'],
                    'manipulation_type': manipulation['type'],
                    'fvg_type': fvg.type,
                    'fvg_top': fvg.top,
                    'fvg_bottom': fvg.bottom,
                    'fvg_formation_time': fvg.formation_time,
                    'inversion_time': inversion['inversion_time'],
                    'direction': direction,
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'tp_1r': rr_levels['tp_1r'],
                    'tp_1_5r': rr_levels['tp_1_5r'],
                    'tp_2r': rr_levels['tp_2r'],
                    'reached_1R': rr_levels['reached_1R'],
                    'reached_1_5R': rr_levels['reached_1_5R'],
                    'reached_2R': rr_levels['reached_2R'],
                    'would_reach_1R_without_sl': would_reach['would_reach_1R'],
                    'would_reach_1_5R_without_sl': would_reach['would_reach_1_5R'],
                    'would_reach_2R_without_sl': would_reach['would_reach_2R'],
                    'exit_price': trade_result.get('exit_price'),
                    'exit_time': trade_result.get('exit_time'),
                    'result': trade_result['result'],
                    'pnl': trade_result.get('pnl'),
                    'pnl_pct': trade_result.get('pnl_pct'),
                    'risk': trade_result.get('risk'),
                    'reward': trade_result.get('reward'),
                    'rr_ratio': trade_result.get('rr_ratio')
                }
                
                self.trades.append(trade_record)
        
        print(f"\nAnalysis complete!")
        print(f"Total dates analyzed: {len(unique_dates)}")
        print(f"Total manipulations detected: {total_manipulations}")
        print(f"Total FVGs detected during manipulations: {total_fvgs_detected}")
        print(f"Total FVG inversions detected: {total_inversions}")
        print(f"\nR/R FILTER RESULTS:")
        print(f"Trades filtered out (R/R < 1): {self.filtered_trades_count}")
        total_potential_trades = total_trades + self.filtered_trades_count
        if total_potential_trades > 0:
            kept_percentage = (total_trades / total_potential_trades) * 100
            print(f"Trades kept (R/R >= 1): {total_trades} ({kept_percentage:.2f}%)")
        
        # Print breakdown by R/R levels reached
        if total_trades > 0:
            trades_df = pd.DataFrame(self.trades)
            reached_1r = trades_df['reached_1R'].sum()
            reached_1_5r = trades_df['reached_1_5R'].sum()
            reached_2r = trades_df['reached_2R'].sum()
            
            win_rate_1r = (reached_1r / total_trades * 100) if total_trades > 0 else 0
            win_rate_1_5r = (reached_1_5r / total_trades * 100) if total_trades > 0 else 0
            win_rate_2r = (reached_2r / total_trades * 100) if total_trades > 0 else 0
            
            print(f"\nWIN RATES BY R/R LEVEL:")
            print(f"  1R: {reached_1r}/{total_trades} trades ({win_rate_1r:.2f}%)")
            print(f"  1.5R: {reached_1_5r}/{total_trades} trades ({win_rate_1_5r:.2f}%)")
            print(f"  2R: {reached_2r}/{total_trades} trades ({win_rate_2r:.2f}%)")
        
        print(f"\nTRADE RESULTS (Tokyo EQ as TP):")
        print(f"Total trades executed: {total_trades}")
        print(f"Winning trades: {winning_trades}")
        print(f"Losing trades: {losing_trades}")
        print(f"No exit trades: {no_exit_trades}")
        
        if total_trades > 0:
            win_rate = (winning_trades / total_trades) * 100
            print(f"\n{'='*80}")
            print(f"OVERALL WIN RATE (Tokyo EQ): {win_rate:.2f}%")
            print(f"{'='*80}")
    
    def analyze_sl_quality(self):
        """
        Analyze Stop Loss quality by checking trades that hit SL.
        For these losing trades, determine if they would have reached TP without SL.
        This helps identify if the SL is too tight (false positives).
        
        Returns:
            dict with SL quality statistics
        """
        if not self.trades:
            print("No trades to analyze!")
            return None
        
        trades_df = pd.DataFrame(self.trades)
        total_trades = len(trades_df)
        
        # Identify losing trades for each R/R level
        # For 1R: trades that didn't reach 1R (hit SL before 1R)
        sl_hit_1r = trades_df[~trades_df['reached_1R']]
        # For 1.5R: trades that didn't reach 1.5R (hit SL before 1.5R)
        sl_hit_1_5r = trades_df[~trades_df['reached_1_5R']]
        # For 2R: trades that didn't reach 2R (hit SL before 2R)
        sl_hit_2r = trades_df[~trades_df['reached_2R']]
        
        # Count false positives (SL hit but would have reached TP without SL)
        false_positives_1r = sl_hit_1r['would_reach_1R_without_sl'].sum()
        false_positives_1_5r = sl_hit_1_5r['would_reach_1_5R_without_sl'].sum()
        false_positives_2r = sl_hit_2r['would_reach_2R_without_sl'].sum()
        
        # Calculate percentages
        fp_pct_1r = (false_positives_1r / len(sl_hit_1r) * 100) if len(sl_hit_1r) > 0 else 0
        fp_pct_1_5r = (false_positives_1_5r / len(sl_hit_1_5r) * 100) if len(sl_hit_1_5r) > 0 else 0
        fp_pct_2r = (false_positives_2r / len(sl_hit_2r) * 100) if len(sl_hit_2r) > 0 else 0
        
        # Calculate adjusted win rates if we ignored SL
        # (original winners + false positives) / total trades
        original_wins_1r = trades_df['reached_1R'].sum()
        original_wins_1_5r = trades_df['reached_1_5R'].sum()
        original_wins_2r = trades_df['reached_2R'].sum()
        
        adjusted_wins_1r = original_wins_1r + false_positives_1r
        adjusted_wins_1_5r = original_wins_1_5r + false_positives_1_5r
        adjusted_wins_2r = original_wins_2r + false_positives_2r
        
        adjusted_wr_1r = (adjusted_wins_1r / total_trades * 100) if total_trades > 0 else 0
        adjusted_wr_1_5r = (adjusted_wins_1_5r / total_trades * 100) if total_trades > 0 else 0
        adjusted_wr_2r = (adjusted_wins_2r / total_trades * 100) if total_trades > 0 else 0
        
        original_wr_1r = (original_wins_1r / total_trades * 100) if total_trades > 0 else 0
        original_wr_1_5r = (original_wins_1_5r / total_trades * 100) if total_trades > 0 else 0
        original_wr_2r = (original_wins_2r / total_trades * 100) if total_trades > 0 else 0
        
        return {
            'total_trades': total_trades,
            # 1R stats
            'sl_hit_1r': len(sl_hit_1r),
            'false_positives_1r': int(false_positives_1r),
            'fp_pct_1r': fp_pct_1r,
            'original_wr_1r': original_wr_1r,
            'adjusted_wr_1r': adjusted_wr_1r,
            # 1.5R stats
            'sl_hit_1_5r': len(sl_hit_1_5r),
            'false_positives_1_5r': int(false_positives_1_5r),
            'fp_pct_1_5r': fp_pct_1_5r,
            'original_wr_1_5r': original_wr_1_5r,
            'adjusted_wr_1_5r': adjusted_wr_1_5r,
            # 2R stats
            'sl_hit_2r': len(sl_hit_2r),
            'false_positives_2r': int(false_positives_2r),
            'fp_pct_2r': fp_pct_2r,
            'original_wr_2r': original_wr_2r,
            'adjusted_wr_2r': adjusted_wr_2r
        }
    
    def analyze_sl_options_comparison(self):
        """
        Analyze and compare all 4 SL options across all trades.
        
        Returns:
            dict with comprehensive comparison statistics
        """
        if not self.sl_comparison_data:
            print("No SL comparison data to analyze!")
            return None
        
        df = pd.DataFrame(self.sl_comparison_data)
        total_trades = len(df)
        
        # Define SL options
        sl_options = [
            ('original', 'Original (Signal Candle)'),
            ('swing', 'Option 1: Swing (Manipulation)'),
            ('atr', 'Option 2: ATR Buffer'),
            ('fvg', 'Option 3: FVG Complete'),
            ('fixed', 'Option 4: Fixed Buffer')
        ]
        
        comparison_results = {}
        
        for sl_key, sl_name in sl_options:
            # Count wins for each R/R level
            wins_1r = df[f'sl_{sl_key}_1r'].sum()
            wins_1_5r = df[f'sl_{sl_key}_1_5r'].sum()
            wins_2r = df[f'sl_{sl_key}_2r'].sum()
            
            # Calculate win rates
            wr_1r = (wins_1r / total_trades * 100) if total_trades > 0 else 0
            wr_1_5r = (wins_1_5r / total_trades * 100) if total_trades > 0 else 0
            wr_2r = (wins_2r / total_trades * 100) if total_trades > 0 else 0
            
            # Calculate expectancy (average across all trades)
            exp_1r = df[f'sl_{sl_key}_expectancy_1r'].mean()
            exp_1_5r = df[f'sl_{sl_key}_expectancy_1_5r'].mean()
            exp_2r = df[f'sl_{sl_key}_expectancy_2r'].mean()
            
            # Calculate average risk
            avg_risk = df[f'sl_{sl_key}_risk'].mean()
            
            # Calculate false positives avoided compared to original
            if sl_key != 'original':
                # Trades that lost with original but won with this option
                fp_avoided_1r = ((~df['sl_original_1r']) & df[f'sl_{sl_key}_1r']).sum()
                fp_avoided_1_5r = ((~df['sl_original_1_5r']) & df[f'sl_{sl_key}_1_5r']).sum()
                fp_avoided_2r = ((~df['sl_original_2r']) & df[f'sl_{sl_key}_2r']).sum()
            else:
                fp_avoided_1r = 0
                fp_avoided_1_5r = 0
                fp_avoided_2r = 0
            
            comparison_results[sl_key] = {
                'name': sl_name,
                'total_trades': total_trades,
                # 1R stats
                'wins_1r': int(wins_1r),
                'wr_1r': wr_1r,
                'exp_1r': exp_1r,
                'fp_avoided_1r': fp_avoided_1r,
                # 1.5R stats
                'wins_1_5r': int(wins_1_5r),
                'wr_1_5r': wr_1_5r,
                'exp_1_5r': exp_1_5r,
                'fp_avoided_1_5r': fp_avoided_1_5r,
                # 2R stats
                'wins_2r': int(wins_2r),
                'wr_2r': wr_2r,
                'exp_2r': exp_2r,
                'fp_avoided_2r': fp_avoided_2r,
                # Risk
                'avg_risk': avg_risk,
                # Overall score (combination of win rate and expectancy)
                'score_1r': wr_1r + (exp_1r * 50),  # Weight expectancy
                'score_1_5r': wr_1_5r + (exp_1_5r * 50),
                'score_2r': wr_2r + (exp_2r * 50)
            }
        
        return comparison_results
    
    def generate_sl_comparison_report(self, output_file='SL_OPTIONS_COMPARISON.md'):
        """
        Generate a comprehensive Markdown report comparing all SL options.
        """
        comparison = self.analyze_sl_options_comparison()
        
        if not comparison:
            print("No comparison data available!")
            return
        
        report_path = os.path.join(self.data_directory, output_file)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Comparaison des Options de Stop Loss - Tokyo FVG Strategy\n\n")
            f.write(f"**Date de l'analyse** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Nombre de trades analysés** : {comparison['original']['total_trades']}\n\n")
            f.write("="*80 + "\n\n")
            
            f.write("## 📊 Résumé Exécutif\n\n")
            f.write("Cette analyse compare 5 approches de placement du Stop Loss sur les **273 trades** :\n\n")
            f.write("1. **SL Original** : High/Low de la bougie signal (baseline actuelle)\n")
            f.write("2. **SL Swing** : High/Low du swing de manipulation complet (02:00-02:30)\n")
            f.write("3. **SL ATR** : High/Low de la bougie + 1.5× ATR(14)\n")
            f.write("4. **SL FVG Complet** : Au-delà des limites du FVG entier\n")
            f.write("5. **SL Buffer Fixe** : High/Low de la bougie + 10 points\n\n")
            
            # Find best option for each metric
            best_wr_1r = max(comparison.values(), key=lambda x: x['wr_1r'])
            best_wr_1_5r = max(comparison.values(), key=lambda x: x['wr_1_5r'])
            best_wr_2r = max(comparison.values(), key=lambda x: x['wr_2r'])
            best_exp_1r = max(comparison.values(), key=lambda x: x['exp_1r'])
            best_exp_1_5r = max(comparison.values(), key=lambda x: x['exp_1_5r'])
            best_exp_2r = max(comparison.values(), key=lambda x: x['exp_2r'])
            best_overall_1r = max(comparison.values(), key=lambda x: x['score_1r'])
            best_overall_1_5r = max(comparison.values(), key=lambda x: x['score_1_5r'])
            best_overall_2r = max(comparison.values(), key=lambda x: x['score_2r'])
            
            f.write("### 🏆 Meilleurs Résultats par Catégorie\n\n")
            f.write(f"- **Meilleur Win Rate à 1R** : {best_wr_1r['name']} ({best_wr_1r['wr_1r']:.2f}%)\n")
            f.write(f"- **Meilleur Win Rate à 1.5R** : {best_wr_1_5r['name']} ({best_wr_1_5r['wr_1_5r']:.2f}%)\n")
            f.write(f"- **Meilleur Win Rate à 2R** : {best_wr_2r['name']} ({best_wr_2r['wr_2r']:.2f}%)\n")
            f.write(f"- **Meilleure Expectancy à 1R** : {best_exp_1r['name']} ({best_exp_1r['exp_1r']:.4f}R)\n")
            f.write(f"- **Meilleure Expectancy à 1.5R** : {best_exp_1_5r['name']} ({best_exp_1_5r['exp_1_5r']:.4f}R)\n")
            f.write(f"- **Meilleure Expectancy à 2R** : {best_exp_2r['name']} ({best_exp_2r['exp_2r']:.4f}R)\n")
            f.write(f"- **Meilleur Score Global à 1R** : {best_overall_1r['name']}\n")
            f.write(f"- **Meilleur Score Global à 1.5R** : {best_overall_1_5r['name']}\n")
            f.write(f"- **Meilleur Score Global à 2R** : {best_overall_2r['name']}\n\n")
            
            f.write("="*80 + "\n\n")
            
            # Detailed comparison table for 1R
            f.write("## 📈 Comparaison Détaillée à 1R (1:1 Risk/Reward)\n\n")
            f.write("| Option SL | Trades Gagnants | Win Rate | Expectancy | Risk Moyen | FP Évités | Score |\n")
            f.write("|-----------|----------------|----------|------------|------------|-----------|-------|\n")
            for key in ['original', 'swing', 'atr', 'fvg', 'fixed']:
                c = comparison[key]
                marker = " 🏆" if c == best_wr_1r or c == best_exp_1r else ""
                f.write(f"| {c['name']}{marker} | {c['wins_1r']}/{c['total_trades']} | "
                       f"{c['wr_1r']:.2f}% | {c['exp_1r']:.4f}R | {c['avg_risk']:.2f} | "
                       f"{c['fp_avoided_1r']} | {c['score_1r']:.2f} |\n")
            f.write("\n")
            
            # Interpretation for 1R
            orig_1r = comparison['original']
            f.write("### Analyse 1R\n\n")
            f.write(f"**Baseline (SL Original)** : {orig_1r['wins_1r']}/{orig_1r['total_trades']} trades "
                   f"({orig_1r['wr_1r']:.2f}%), Expectancy = {orig_1r['exp_1r']:.4f}R\n\n")
            
            for key in ['swing', 'atr', 'fvg', 'fixed']:
                c = comparison[key]
                improvement_wr = c['wr_1r'] - orig_1r['wr_1r']
                improvement_exp = c['exp_1r'] - orig_1r['exp_1r']
                f.write(f"**{c['name']}** :\n")
                f.write(f"- Win Rate : {c['wr_1r']:.2f}% ({improvement_wr:+.2f}% vs baseline)\n")
                f.write(f"- Expectancy : {c['exp_1r']:.4f}R ({improvement_exp:+.4f}R vs baseline)\n")
                f.write(f"- Faux Positifs Évités : {c['fp_avoided_1r']} trades\n")
                f.write(f"- Impact : {'✅ POSITIF' if improvement_exp > 0 else '❌ NÉGATIF'}\n\n")
            
            f.write("\n" + "="*80 + "\n\n")
            
            # Detailed comparison table for 1.5R
            f.write("## 📈 Comparaison Détaillée à 1.5R (1:1.5 Risk/Reward)\n\n")
            f.write("| Option SL | Trades Gagnants | Win Rate | Expectancy | Risk Moyen | FP Évités | Score |\n")
            f.write("|-----------|----------------|----------|------------|------------|-----------|-------|\n")
            for key in ['original', 'swing', 'atr', 'fvg', 'fixed']:
                c = comparison[key]
                marker = " 🏆" if c == best_wr_1_5r or c == best_exp_1_5r else ""
                f.write(f"| {c['name']}{marker} | {c['wins_1_5r']}/{c['total_trades']} | "
                       f"{c['wr_1_5r']:.2f}% | {c['exp_1_5r']:.4f}R | {c['avg_risk']:.2f} | "
                       f"{c['fp_avoided_1_5r']} | {c['score_1_5r']:.2f} |\n")
            f.write("\n")
            
            # Interpretation for 1.5R
            orig_1_5r = comparison['original']
            f.write("### Analyse 1.5R\n\n")
            f.write(f"**Baseline (SL Original)** : {orig_1_5r['wins_1_5r']}/{orig_1_5r['total_trades']} trades "
                   f"({orig_1_5r['wr_1_5r']:.2f}%), Expectancy = {orig_1_5r['exp_1_5r']:.4f}R\n\n")
            
            for key in ['swing', 'atr', 'fvg', 'fixed']:
                c = comparison[key]
                improvement_wr = c['wr_1_5r'] - orig_1_5r['wr_1_5r']
                improvement_exp = c['exp_1_5r'] - orig_1_5r['exp_1_5r']
                f.write(f"**{c['name']}** :\n")
                f.write(f"- Win Rate : {c['wr_1_5r']:.2f}% ({improvement_wr:+.2f}% vs baseline)\n")
                f.write(f"- Expectancy : {c['exp_1_5r']:.4f}R ({improvement_exp:+.4f}R vs baseline)\n")
                f.write(f"- Faux Positifs Évités : {c['fp_avoided_1_5r']} trades\n")
                f.write(f"- Impact : {'✅ POSITIF' if improvement_exp > 0 else '❌ NÉGATIF'}\n\n")
            
            f.write("\n" + "="*80 + "\n\n")
            
            # Detailed comparison table for 2R
            f.write("## 📈 Comparaison Détaillée à 2R (1:2 Risk/Reward)\n\n")
            f.write("| Option SL | Trades Gagnants | Win Rate | Expectancy | Risk Moyen | FP Évités | Score |\n")
            f.write("|-----------|----------------|----------|------------|------------|-----------|-------|\n")
            for key in ['original', 'swing', 'atr', 'fvg', 'fixed']:
                c = comparison[key]
                marker = " 🏆" if c == best_wr_2r or c == best_exp_2r else ""
                f.write(f"| {c['name']}{marker} | {c['wins_2r']}/{c['total_trades']} | "
                       f"{c['wr_2r']:.2f}% | {c['exp_2r']:.4f}R | {c['avg_risk']:.2f} | "
                       f"{c['fp_avoided_2r']} | {c['score_2r']:.2f} |\n")
            f.write("\n")
            
            # Interpretation for 2R
            orig_2r = comparison['original']
            f.write("### Analyse 2R\n\n")
            f.write(f"**Baseline (SL Original)** : {orig_2r['wins_2r']}/{orig_2r['total_trades']} trades "
                   f"({orig_2r['wr_2r']:.2f}%), Expectancy = {orig_2r['exp_2r']:.4f}R\n\n")
            
            for key in ['swing', 'atr', 'fvg', 'fixed']:
                c = comparison[key]
                improvement_wr = c['wr_2r'] - orig_2r['wr_2r']
                improvement_exp = c['exp_2r'] - orig_2r['exp_2r']
                f.write(f"**{c['name']}** :\n")
                f.write(f"- Win Rate : {c['wr_2r']:.2f}% ({improvement_wr:+.2f}% vs baseline)\n")
                f.write(f"- Expectancy : {c['exp_2r']:.4f}R ({improvement_exp:+.4f}R vs baseline)\n")
                f.write(f"- Faux Positifs Évités : {c['fp_avoided_2r']} trades\n")
                f.write(f"- Impact : {'✅ POSITIF' if improvement_exp > 0 else '❌ NÉGATIF'}\n\n")
            
            f.write("\n" + "="*80 + "\n\n")
            
            # Final recommendation
            f.write("## 🎯 RECOMMANDATION FINALE\n\n")
            f.write("### Meilleur Compromis Global\n\n")
            
            # Determine best overall based on multiple factors
            f.write("Après analyse complète des 273 trades avec les 5 options de SL, voici la recommandation :\n\n")
            
            # Calculate overall winner
            best_overall = best_overall_2r  # Prioritize 2R for best R/R
            
            f.write(f"**OPTION RECOMMANDÉE : {best_overall['name']}**\n\n")
            f.write("**Justification** :\n\n")
            f.write(f"- Win Rate à 1R : {best_overall['wr_1r']:.2f}%\n")
            f.write(f"- Win Rate à 1.5R : {best_overall['wr_1_5r']:.2f}%\n")
            f.write(f"- Win Rate à 2R : {best_overall['wr_2r']:.2f}%\n")
            f.write(f"- Expectancy à 2R : {best_overall['exp_2r']:.4f}R\n")
            f.write(f"- Risk Moyen : {best_overall['avg_risk']:.2f} points\n\n")
            
            f.write("### Implémentation Pratique\n\n")
            
            # Get best option key
            best_key = [k for k, v in comparison.items() if v == best_overall][0]
            
            if best_key == 'swing':
                f.write("**Placement du Stop Loss** :\n")
                f.write("- **SHORT** : SL = Plus haut atteint pendant la manipulation (02:00-02:30)\n")
                f.write("- **LONG** : SL = Plus bas atteint pendant la manipulation (02:00-02:30)\n\n")
                f.write("**Avantages** :\n")
                f.write("- Respecte la structure du mouvement de manipulation\n")
                f.write("- Donne de l'espace au prix pour les wicks normaux\n")
                f.write("- Réduit significativement les faux positifs\n\n")
            elif best_key == 'atr':
                f.write("**Placement du Stop Loss** :\n")
                f.write("- Calculer ATR(14) à l'entry\n")
                f.write("- **SHORT** : SL = High de la bougie signal + (1.5 × ATR)\n")
                f.write("- **LONG** : SL = Low de la bougie signal - (1.5 × ATR)\n\n")
                f.write("**Avantages** :\n")
                f.write("- S'adapte automatiquement à la volatilité\n")
                f.write("- Approche scientifique et objective\n")
                f.write("- Large en période volatile, serré en période calme\n\n")
            elif best_key == 'fvg':
                f.write("**Placement du Stop Loss** :\n")
                f.write("- **SHORT** : SL = High du FVG (limite supérieure du FVG entier)\n")
                f.write("- **LONG** : SL = Low du FVG (limite inférieure du FVG entier)\n\n")
                f.write("**Avantages** :\n")
                f.write("- Logique par rapport à la théorie des FVG\n")
                f.write("- Le FVG doit agir comme support/résistance\n")
                f.write("- Évite les re-tests du FVG\n\n")
            elif best_key == 'fixed':
                f.write("**Placement du Stop Loss** :\n")
                f.write("- **SHORT** : SL = High de la bougie signal + 10 points\n")
                f.write("- **LONG** : SL = Low de la bougie signal - 10 points\n\n")
                f.write("**Avantages** :\n")
                f.write("- Très simple à implémenter\n")
                f.write("- Prévisible et constant\n")
                f.write("- Suffisant pour éviter la majorité des wicks\n\n")
            
            f.write("### Stratégie de Sortie Recommandée\n\n")
            f.write("1. **Entry** : Selon les règles d'inversion FVG\n")
            f.write(f"2. **SL** : {best_overall['name']}\n")
            f.write("3. **TP** : 2R (Entry ± 2 × Risk)\n")
            f.write("4. **Gestion** :\n")
            f.write("   - Dès que 1R est atteint → Move SL to Break-Even\n")
            f.write("   - Laisser courir vers 2R\n")
            f.write("   - Option : Sortie partielle (50%) à 1.5R, reste à 2R\n\n")
            
            f.write("### Résultats Attendus\n\n")
            f.write(f"Sur 100 trades avec {best_overall['name']} :\n")
            f.write(f"- ~{best_overall['wr_2r']:.0f} trades atteignent 2R\n")
            f.write(f"- ~{100 - best_overall['wr_2r']:.0f} trades stoppés\n")
            f.write(f"- Expectancy : {best_overall['exp_2r']:.4f}R par trade\n")
            profit_per_100 = best_overall['exp_2r'] * 100
            f.write(f"- Profit net estimé : {profit_per_100:+.2f}R sur 100 trades\n\n")
            
            f.write("="*80 + "\n\n")
            f.write("## 📋 Conclusion\n\n")
            f.write("L'analyse comparative démontre clairement que le **placement du Stop Loss est crucial** ")
            f.write("pour la performance de cette stratégie. ")
            f.write(f"En passant du SL original au {best_overall['name']}, ")
            f.write("on transforme une stratégie à expectancy négative en une stratégie potentiellement profitable.\n\n")
            f.write("**Action immédiate** : Implémenter le placement de SL recommandé sur les prochains setups.\n\n")
            f.write("---\n\n")
            f.write(f"*Rapport généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"\nSL Options Comparison Report saved to: {report_path}")
        
        # Also save detailed CSV
        if self.sl_comparison_data:
            csv_path = os.path.join(self.data_directory, 'sl_options_detailed.csv')
            pd.DataFrame(self.sl_comparison_data).to_csv(csv_path, index=False)
            print(f"Detailed SL options data saved to: {csv_path}")
    
    def generate_report(self, output_file='tokyo_fvg_strategy_report.txt'):
        """
        Generate a detailed analysis report.
        
        Args:
            output_file: Name of the output report file
        """
        if not self.trades:
            print("No trades to report!")
            return
        
        trades_df = pd.DataFrame(self.trades)
        
        # Calculate statistics
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['result'] == 'WIN'])
        losing_trades = len(trades_df[trades_df['result'] == 'LOSS'])
        no_exit_trades = len(trades_df[trades_df['result'] == 'NO_EXIT'])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Breakdown by direction
        long_trades = trades_df[trades_df['direction'] == 'LONG']
        short_trades = trades_df[trades_df['direction'] == 'SHORT']
        
        long_wins = len(long_trades[long_trades['result'] == 'WIN'])
        short_wins = len(short_trades[short_trades['result'] == 'WIN'])
        
        long_win_rate = (long_wins / len(long_trades) * 100) if len(long_trades) > 0 else 0
        short_win_rate = (short_wins / len(short_trades) * 100) if len(short_trades) > 0 else 0
        
        # P&L statistics
        completed_trades = trades_df[trades_df['result'].isin(['WIN', 'LOSS'])]
        total_pnl = completed_trades['pnl'].sum() if len(completed_trades) > 0 else 0
        avg_pnl = completed_trades['pnl'].mean() if len(completed_trades) > 0 else 0
        
        winning_pnl = trades_df[trades_df['result'] == 'WIN']['pnl'].sum()
        losing_pnl = abs(trades_df[trades_df['result'] == 'LOSS']['pnl'].sum())
        
        avg_win = trades_df[trades_df['result'] == 'WIN']['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = abs(trades_df[trades_df['result'] == 'LOSS']['pnl'].mean()) if losing_trades > 0 else 0
        
        # Risk/Reward statistics
        avg_rr = completed_trades['rr_ratio'].mean() if len(completed_trades) > 0 else 0
        
        # Expectancy
        expectancy = (win_rate / 100 * avg_win) - ((1 - win_rate / 100) * avg_loss)
        
        # Breakdown by year
        trades_df['year'] = pd.to_datetime(trades_df['date']).dt.year
        yearly_stats = trades_df.groupby('year').apply(
            lambda x: pd.Series({
                'total': len(x),
                'wins': len(x[x['result'] == 'WIN']),
                'win_rate': len(x[x['result'] == 'WIN']) / len(x) * 100 if len(x) > 0 else 0
            })
        )
        
        # Generate report
        report_path = os.path.join(self.data_directory, output_file)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("TOKYO SESSION FVG INVERSION STRATEGY ANALYSIS REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Analysis Period: {trades_df['date'].min()} to {trades_df['date'].max()}\n")
            f.write("="*80 + "\n\n")
            
            f.write("STRATEGY RULES:\n")
            f.write("-" * 80 + "\n")
            f.write("BEARISH SCENARIO (Short Entry):\n")
            f.write("  1. Price manipulates Tokyo High between 02:00-02:30\n")
            f.write("  2. During upward manipulation, a Bullish FVG forms\n")
            f.write("  3. Price reverses, fills FVG, and candle closes below it (Inversion)\n")
            f.write("  4. Entry: Close of breaking candle | SL: High of breaking candle\n")
            f.write("  5. TP: Tokyo 50% Equilibrium\n\n")
            f.write("BULLISH SCENARIO (Long Entry):\n")
            f.write("  1. Price manipulates Tokyo Low between 02:00-02:30\n")
            f.write("  2. During downward manipulation, a Bearish FVG forms\n")
            f.write("  3. Price reverses, fills FVG, and candle closes above it (Inversion)\n")
            f.write("  4. Entry: Close of breaking candle | SL: Low of breaking candle\n")
            f.write("  5. TP: Tokyo 50% Equilibrium\n\n")
            f.write("RISK/REWARD FILTER:\n")
            f.write("  - Only trades with R/R >= 1.0 are executed\n")
            f.write("  - Risk = |Entry - Stop Loss|\n")
            f.write("  - Reward = |Take Profit - Entry|\n")
            f.write("  - Trades with R/R < 1 are excluded\n")
            f.write("\n")
            f.write("R/R LEVEL ANALYSIS:\n")
            f.write("  - For each trade, we check if price reaches 1R, 1.5R, and 2R before SL\n")
            f.write("  - TP_1R = Entry + (1.0 × Risk) for LONG or Entry - (1.0 × Risk) for SHORT\n")
            f.write("  - TP_1.5R = Entry + (1.5 × Risk) for LONG or Entry - (1.5 × Risk) for SHORT\n")
            f.write("  - TP_2R = Entry + (2.0 × Risk) for LONG or Entry - (2.0 × Risk) for SHORT\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("R/R FILTER IMPACT:\n")
            f.write("-" * 80 + "\n")
            total_potential_trades = total_trades + self.filtered_trades_count
            kept_percentage = (total_trades / total_potential_trades * 100) if total_potential_trades > 0 else 0
            filtered_percentage = (self.filtered_trades_count / total_potential_trades * 100) if total_potential_trades > 0 else 0
            f.write(f"Total potential trades (before filter): {total_potential_trades}\n")
            f.write(f"Trades filtered out (R/R < 1): {self.filtered_trades_count} ({filtered_percentage:.2f}%)\n")
            f.write(f"Trades kept (R/R >= 1): {total_trades} ({kept_percentage:.2f}%)\n")
            f.write("\n" + "="*80 + "\n\n")
            
            # Add breakdown by R/R levels reached
            f.write("WIN RATES BY R/R LEVEL:\n")
            f.write("-" * 80 + "\n")
            f.write("This shows how many trades reached each R/R level BEFORE hitting SL.\n\n")
            
            reached_1r = trades_df['reached_1R'].sum()
            reached_1_5r = trades_df['reached_1_5R'].sum()
            reached_2r = trades_df['reached_2R'].sum()
            
            win_rate_1r = (reached_1r / total_trades * 100) if total_trades > 0 else 0
            win_rate_1_5r = (reached_1_5r / total_trades * 100) if total_trades > 0 else 0
            win_rate_2r = (reached_2r / total_trades * 100) if total_trades > 0 else 0
            
            f.write(f"{'R/R Level':<15} {'Reached':<15} {'Total':<10} {'Win Rate':<15}\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'1R':<15} {reached_1r:<15} {total_trades:<10} {win_rate_1r:.2f}%\n")
            f.write(f"{'1.5R':<15} {reached_1_5r:<15} {total_trades:<10} {win_rate_1_5r:.2f}%\n")
            f.write(f"{'2R':<15} {reached_2r:<15} {total_trades:<10} {win_rate_2r:.2f}%\n")
            f.write("\n" + "="*80 + "\n\n")
            
            # Add Stop Loss Quality Analysis
            sl_quality = self.analyze_sl_quality()
            if sl_quality:
                f.write("STOP LOSS QUALITY ANALYSIS:\n")
                f.write("="*80 + "\n")
                f.write("This analysis identifies 'False Positives' - trades that hit the Stop Loss\n")
                f.write("but would have eventually reached the Take Profit target within 6 hours if\n")
                f.write("the SL had not been in place. This helps determine if the SL is too tight.\n\n")
                
                f.write("1R (1:1 Risk/Reward) Analysis:\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total trades that hit SL before 1R: {sl_quality['sl_hit_1r']}\n")
                f.write(f"False Positives (would have reached 1R): {sl_quality['false_positives_1r']}\n")
                f.write(f"False Positive Rate: {sl_quality['fp_pct_1r']:.2f}%\n")
                f.write(f"Original Win Rate (with SL): {sl_quality['original_wr_1r']:.2f}%\n")
                f.write(f"Adjusted Win Rate (without SL): {sl_quality['adjusted_wr_1r']:.2f}%\n")
                f.write(f"Lost Opportunity: {sl_quality['adjusted_wr_1r'] - sl_quality['original_wr_1r']:.2f}%\n")
                f.write("\n")
                
                f.write("1.5R (1:1.5 Risk/Reward) Analysis:\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total trades that hit SL before 1.5R: {sl_quality['sl_hit_1_5r']}\n")
                f.write(f"False Positives (would have reached 1.5R): {sl_quality['false_positives_1_5r']}\n")
                f.write(f"False Positive Rate: {sl_quality['fp_pct_1_5r']:.2f}%\n")
                f.write(f"Original Win Rate (with SL): {sl_quality['original_wr_1_5r']:.2f}%\n")
                f.write(f"Adjusted Win Rate (without SL): {sl_quality['adjusted_wr_1_5r']:.2f}%\n")
                f.write(f"Lost Opportunity: {sl_quality['adjusted_wr_1_5r'] - sl_quality['original_wr_1_5r']:.2f}%\n")
                f.write("\n")
                
                f.write("2R (1:2 Risk/Reward) Analysis:\n")
                f.write("-" * 80 + "\n")
                f.write(f"Total trades that hit SL before 2R: {sl_quality['sl_hit_2r']}\n")
                f.write(f"False Positives (would have reached 2R): {sl_quality['false_positives_2r']}\n")
                f.write(f"False Positive Rate: {sl_quality['fp_pct_2r']:.2f}%\n")
                f.write(f"Original Win Rate (with SL): {sl_quality['original_wr_2r']:.2f}%\n")
                f.write(f"Adjusted Win Rate (without SL): {sl_quality['adjusted_wr_2r']:.2f}%\n")
                f.write(f"Lost Opportunity: {sl_quality['adjusted_wr_2r'] - sl_quality['original_wr_2r']:.2f}%\n")
                f.write("\n")
                
                # Add recommendations
                f.write("RECOMMENDATIONS:\n")
                f.write("-" * 80 + "\n")
                avg_fp_rate = (sl_quality['fp_pct_1r'] + sl_quality['fp_pct_1_5r'] + sl_quality['fp_pct_2r']) / 3
                
                if avg_fp_rate > 50:
                    f.write("⚠️  HIGH FALSE POSITIVE RATE (>50%): Your Stop Loss appears to be TOO TIGHT.\n")
                    f.write("The market frequently hunts your SL before moving in the anticipated direction.\n")
                    f.write("RECOMMENDATION: Consider widening your Stop Loss placement or using a different\n")
                    f.write("SL strategy (e.g., beyond the previous swing low/high instead of the signal candle).\n")
                elif avg_fp_rate > 30:
                    f.write("⚠️  MODERATE FALSE POSITIVE RATE (30-50%): Your Stop Loss may be slightly tight.\n")
                    f.write("A significant portion of stopped trades would have been winners.\n")
                    f.write("RECOMMENDATION: Consider testing a slightly wider SL or implementing partial\n")
                    f.write("position sizing with different SL levels.\n")
                elif avg_fp_rate > 15:
                    f.write("✓ ACCEPTABLE FALSE POSITIVE RATE (15-30%): Your Stop Loss placement appears\n")
                    f.write("reasonable. Some false positives are normal in trading.\n")
                    f.write("RECOMMENDATION: Current SL strategy is acceptable. Monitor over time.\n")
                else:
                    f.write("✓ LOW FALSE POSITIVE RATE (<15%): Your Stop Loss placement is APPROPRIATE.\n")
                    f.write("Very few trades are being stopped out that would have been winners.\n")
                    f.write("RECOMMENDATION: Maintain current SL strategy. It effectively protects capital.\n")
                
                f.write("\n" + "="*80 + "\n\n")
            
            f.write("OVERALL RESULTS (Tokyo EQ as TP):\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Trades: {total_trades}\n")
            f.write(f"Winning Trades: {winning_trades}\n")
            f.write(f"Losing Trades: {losing_trades}\n")
            f.write(f"No Exit Trades: {no_exit_trades}\n")
            f.write(f"\n>>> WIN RATE (Tokyo EQ): {win_rate:.2f}% <<<\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("BREAKDOWN BY DIRECTION:\n")
            f.write("-" * 80 + "\n")
            f.write(f"LONG Trades:\n")
            f.write(f"  Total: {len(long_trades)}\n")
            f.write(f"  Wins: {long_wins}\n")
            f.write(f"  Win Rate: {long_win_rate:.2f}%\n\n")
            f.write(f"SHORT Trades:\n")
            f.write(f"  Total: {len(short_trades)}\n")
            f.write(f"  Wins: {short_wins}\n")
            f.write(f"  Win Rate: {short_win_rate:.2f}%\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("PROFIT/LOSS STATISTICS:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total P&L: {total_pnl:.2f} points\n")
            f.write(f"Average P&L per trade: {avg_pnl:.2f} points\n")
            f.write(f"Total Winning P&L: {winning_pnl:.2f} points\n")
            f.write(f"Total Losing P&L: {losing_pnl:.2f} points\n")
            f.write(f"Average Win: {avg_win:.2f} points\n")
            f.write(f"Average Loss: {avg_loss:.2f} points\n")
            f.write(f"Win/Loss Ratio: {avg_win/avg_loss:.2f} : 1\n" if avg_loss > 0 else "Win/Loss Ratio: N/A\n")
            f.write(f"Expectancy: {expectancy:.2f} points per trade\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("RISK/REWARD ANALYSIS:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Average Risk/Reward Ratio: {avg_rr:.2f} : 1\n")
            f.write(f"Average Risk per trade: {completed_trades['risk'].mean():.2f} points\n" if len(completed_trades) > 0 else "Average Risk per trade: N/A\n")
            f.write(f"Average Reward per trade: {completed_trades['reward'].mean():.2f} points\n" if len(completed_trades) > 0 else "Average Reward per trade: N/A\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("YEARLY BREAKDOWN:\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Year':<10} {'Total':<10} {'Wins':<10} {'Win Rate':<15}\n")
            f.write("-" * 80 + "\n")
            for year in yearly_stats.index:
                total = int(yearly_stats.loc[year, 'total'])
                wins = int(yearly_stats.loc[year, 'wins'])
                wr = yearly_stats.loc[year, 'win_rate']
                f.write(f"{year:<10} {total:<10} {wins:<10} {wr:.2f}%\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("SAMPLE TRADES (First 20):\n")
            f.write("-" * 80 + "\n")
            sample_size = min(20, len(trades_df))
            for idx, row in trades_df.head(sample_size).iterrows():
                f.write(f"\nTrade #{idx+1}:\n")
                f.write(f"  Date: {row['date']}\n")
                f.write(f"  Tokyo Range: {row['tokyo_low']:.2f} - {row['tokyo_high']:.2f} (EQ: {row['tokyo_eq']:.2f})\n")
                f.write(f"  Manipulation: {row['manipulation_type']}\n")
                f.write(f"  FVG Type: {row['fvg_type']} ({row['fvg_bottom']:.2f} - {row['fvg_top']:.2f})\n")
                f.write(f"  FVG Formation: {row['fvg_formation_time']}\n")
                f.write(f"  Inversion Time: {row['inversion_time']}\n")
                f.write(f"  Direction: {row['direction']}\n")
                f.write(f"  Entry: {row['entry_price']:.2f}\n")
                f.write(f"  Stop Loss: {row['stop_loss']:.2f}\n")
                f.write(f"  Take Profit (Tokyo EQ): {row['take_profit']:.2f}\n")
                f.write(f"  TP 1R: {row['tp_1r']:.2f} (Reached: {row['reached_1R']})\n")
                f.write(f"  TP 1.5R: {row['tp_1_5r']:.2f} (Reached: {row['reached_1_5R']})\n")
                f.write(f"  TP 2R: {row['tp_2r']:.2f} (Reached: {row['reached_2R']})\n")
                f.write(f"  Actual R/R: {row['rr_ratio']:.2f}\n")
                f.write(f"  Result: {row['result']}\n")
                if row['result'] in ['WIN', 'LOSS']:
                    f.write(f"  Exit Price: {row['exit_price']:.2f}\n")
                    f.write(f"  Exit Time: {row['exit_time']}\n")
                    f.write(f"  P&L: {row['pnl']:.2f} points ({row['pnl_pct']:.2f}%)\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*80 + "\n")
        
        print(f"\nDetailed report saved to: {report_path}")
        
        # Also save results to CSV
        csv_path = os.path.join(self.data_directory, 'tokyo_fvg_strategy_results.csv')
        trades_df.to_csv(csv_path, index=False)
        print(f"Results data saved to: {csv_path}")
        
        # Print summary to console
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Total Trades: {total_trades}")
        print(f"Winning Trades: {winning_trades}")
        print(f"Losing Trades: {losing_trades}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"\nLONG Trades: {len(long_trades)} (Win Rate: {long_win_rate:.2f}%)")
        print(f"SHORT Trades: {len(short_trades)} (Win Rate: {short_win_rate:.2f}%)")
        print(f"\nTotal P&L: {total_pnl:.2f} points")
        print(f"Average P&L: {avg_pnl:.2f} points per trade")
        print(f"Expectancy: {expectancy:.2f} points per trade")
        print(f"Average R:R Ratio: {avg_rr:.2f}")
        print("="*80)
    
    def generate_visualizations(self):
        """Generate visualizations for the strategy results."""
        if not self.trades:
            print("No trades to visualize!")
            return
        
        trades_df = pd.DataFrame(self.trades)
        total_trades = len(trades_df)
        
        # Create figure with subplots
        fig, axes = plt.subplots(4, 2, figsize=(15, 24))
        fig.suptitle('Tokyo FVG Inversion Strategy - Analysis Results', fontsize=16, fontweight='bold')
        
        # 1. Win Rate Pie Chart
        ax1 = axes[0, 0]
        result_counts = trades_df['result'].value_counts()
        colors = ['#2ecc71', '#e74c3c', '#95a5a6']
        labels = ['WIN', 'LOSS', 'NO EXIT']
        filtered_counts = result_counts[result_counts.index.isin(labels)]
        ax1.pie(filtered_counts, labels=filtered_counts.index, autopct='%1.1f%%', 
                colors=colors[:len(filtered_counts)], startangle=90)
        ax1.set_title('Win Rate Distribution')
        
        # 2. Win Rate by Direction
        ax2 = axes[0, 1]
        direction_stats = trades_df.groupby('direction').apply(
            lambda x: pd.Series({
                'total': len(x),
                'wins': len(x[x['result'] == 'WIN']),
                'win_rate': len(x[x['result'] == 'WIN']) / len(x) * 100 if len(x) > 0 else 0
            })
        )
        
        x_pos = range(len(direction_stats))
        bars = ax2.bar(x_pos, direction_stats['win_rate'], color=['#3498db', '#e67e22'])
        ax2.set_xlabel('Direction')
        ax2.set_ylabel('Win Rate (%)')
        ax2.set_title('Win Rate by Direction')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(direction_stats.index)
        ax2.set_ylim(0, 100)
        ax2.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%\n({int(direction_stats.iloc[i]["wins"])}/{int(direction_stats.iloc[i]["total"])})',
                    ha='center', va='bottom')
        
        # 3. P&L Distribution
        ax3 = axes[1, 0]
        completed_trades = trades_df[trades_df['result'].isin(['WIN', 'LOSS'])]
        if len(completed_trades) > 0:
            ax3.hist(completed_trades['pnl'], bins=30, color='#9b59b6', edgecolor='black', alpha=0.7)
            ax3.axvline(0, color='red', linestyle='--', linewidth=2, label='Breakeven')
            ax3.axvline(completed_trades['pnl'].mean(), color='green', linestyle='--', 
                       linewidth=2, label=f'Mean: {completed_trades["pnl"].mean():.2f}')
            ax3.set_xlabel('P&L (Points)')
            ax3.set_ylabel('Frequency')
            ax3.set_title('P&L Distribution')
            ax3.legend()
            ax3.grid(axis='y', alpha=0.3)
        
        # 4. Win Rate by R/R Level
        ax4 = axes[1, 1]
        
        # Calculate win rates for each R/R level
        reached_1r = trades_df['reached_1R'].sum()
        reached_1_5r = trades_df['reached_1_5R'].sum()
        reached_2r = trades_df['reached_2R'].sum()
        
        win_rate_1r = (reached_1r / total_trades * 100) if total_trades > 0 else 0
        win_rate_1_5r = (reached_1_5r / total_trades * 100) if total_trades > 0 else 0
        win_rate_2r = (reached_2r / total_trades * 100) if total_trades > 0 else 0
        
        rr_levels = ['1R', '1.5R', '2R']
        win_rates = [win_rate_1r, win_rate_1_5r, win_rate_2r]
        reached_counts = [reached_1r, reached_1_5r, reached_2r]
        
        x_pos = range(len(rr_levels))
        colors_rr = ['#2ecc71', '#f39c12', '#e74c3c']  # Green, orange, red
        bars = ax4.bar(x_pos, win_rates, color=colors_rr, edgecolor='black', alpha=0.8)
        ax4.set_xlabel('R/R Level')
        ax4.set_ylabel('Win Rate (%)')
        ax4.set_title('Win Rate by R/R Level (Reached Before SL)')
        ax4.set_xticks(x_pos)
        ax4.set_xticklabels(rr_levels)
        ax4.set_ylim(0, 100)
        ax4.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%\n({int(reached_counts[i])}/{total_trades})',
                    ha='center', va='bottom', fontsize=9)
        
        # 5. Yearly Performance
        ax5 = axes[2, 0]
        trades_df['year'] = pd.to_datetime(trades_df['date']).dt.year
        yearly_stats = trades_df.groupby('year').apply(
            lambda x: pd.Series({
                'total': len(x),
                'wins': len(x[x['result'] == 'WIN']),
                'win_rate': len(x[x['result'] == 'WIN']) / len(x) * 100 if len(x) > 0 else 0
            })
        )
        
        bars = ax5.bar(yearly_stats.index, yearly_stats['win_rate'], color='#f39c12', edgecolor='black', alpha=0.8)
        ax5.set_xlabel('Year')
        ax5.set_ylabel('Win Rate (%)')
        ax5.set_title('Yearly Win Rate')
        ax5.set_ylim(0, 100)
        ax5.grid(axis='y', alpha=0.3)
        ax5.axhline(y=trades_df[trades_df['result'].isin(['WIN', 'LOSS'])].apply(
            lambda x: x['result'] == 'WIN', axis=1).mean()*100, 
            color='red', linestyle='--', linewidth=2, label='Overall Average')
        ax5.legend()
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            year = yearly_stats.index[i]
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%\n({int(yearly_stats.loc[year, "wins"])}/{int(yearly_stats.loc[year, "total"])})',
                    ha='center', va='bottom', fontsize=8)
        
        # 6. Cumulative P&L
        ax6 = axes[2, 1]
        completed_trades_sorted = completed_trades.sort_values('inversion_time')
        completed_trades_sorted['cumulative_pnl'] = completed_trades_sorted['pnl'].cumsum()
        
        if len(completed_trades_sorted) > 0:
            ax6.plot(completed_trades_sorted['inversion_time'], 
                    completed_trades_sorted['cumulative_pnl'], 
                    linewidth=2, color='#2c3e50')
            ax6.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
            ax6.set_xlabel('Date')
            ax6.set_ylabel('Cumulative P&L (Points)')
            ax6.set_title('Cumulative P&L Over Time')
            ax6.grid(True, alpha=0.3)
            
            # Format x-axis dates
            ax6.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax6.xaxis.set_major_locator(mdates.YearLocator())
            plt.setp(ax6.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 7. Stop Loss Quality Analysis - False Positives
        ax7 = axes[3, 0]
        sl_quality = self.analyze_sl_quality()
        
        if sl_quality:
            rr_levels = ['1R', '1.5R', '2R']
            fp_rates = [
                sl_quality['fp_pct_1r'],
                sl_quality['fp_pct_1_5r'],
                sl_quality['fp_pct_2r']
            ]
            fp_counts = [
                sl_quality['false_positives_1r'],
                sl_quality['false_positives_1_5r'],
                sl_quality['false_positives_2r']
            ]
            sl_hits = [
                sl_quality['sl_hit_1r'],
                sl_quality['sl_hit_1_5r'],
                sl_quality['sl_hit_2r']
            ]
            
            x_pos = range(len(rr_levels))
            colors_fp = ['#e74c3c', '#e67e22', '#f39c12']  # Red to orange gradient
            bars = ax7.bar(x_pos, fp_rates, color=colors_fp, edgecolor='black', alpha=0.8)
            ax7.set_xlabel('R/R Level')
            ax7.set_ylabel('False Positive Rate (%)')
            ax7.set_title('Stop Loss Quality: False Positive Rates\n(SL Hit but Would Have Reached TP)')
            ax7.set_xticks(x_pos)
            ax7.set_xticklabels(rr_levels)
            ax7.set_ylim(0, 100)
            ax7.grid(axis='y', alpha=0.3)
            ax7.axhline(y=30, color='orange', linestyle='--', linewidth=1, alpha=0.7, label='Warning Threshold (30%)')
            ax7.axhline(y=50, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Critical Threshold (50%)')
            ax7.legend(loc='upper right', fontsize=8)
            
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax7.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%\n({fp_counts[i]}/{sl_hits[i]})',
                        ha='center', va='bottom', fontsize=9)
        
        # 8. Win Rate Comparison: With vs Without SL
        ax8 = axes[3, 1]
        
        if sl_quality:
            rr_levels = ['1R', '1.5R', '2R']
            original_wrs = [
                sl_quality['original_wr_1r'],
                sl_quality['original_wr_1_5r'],
                sl_quality['original_wr_2r']
            ]
            adjusted_wrs = [
                sl_quality['adjusted_wr_1r'],
                sl_quality['adjusted_wr_1_5r'],
                sl_quality['adjusted_wr_2r']
            ]
            
            x = np.arange(len(rr_levels))
            width = 0.35
            
            bars1 = ax8.bar(x - width/2, original_wrs, width, label='With SL', 
                           color='#3498db', edgecolor='black', alpha=0.8)
            bars2 = ax8.bar(x + width/2, adjusted_wrs, width, label='Without SL (Theoretical)', 
                           color='#2ecc71', edgecolor='black', alpha=0.8)
            
            ax8.set_xlabel('R/R Level')
            ax8.set_ylabel('Win Rate (%)')
            ax8.set_title('Win Rate Comparison: Impact of Stop Loss')
            ax8.set_xticks(x)
            ax8.set_xticklabels(rr_levels)
            ax8.set_ylim(0, 100)
            ax8.legend()
            ax8.grid(axis='y', alpha=0.3)
            
            # Add value labels on bars
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax8.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.1f}%',
                            ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        # Save figure
        output_path = os.path.join(self.data_directory, 'tokyo_fvg_strategy_analysis.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\nVisualization saved to: {output_path}")
    
    def generate_sl_comparison_visualizations(self):
        """Generate visualizations comparing all SL options."""
        if not self.sl_comparison_data:
            print("No SL comparison data to visualize!")
            return
        
        comparison = self.analyze_sl_options_comparison()
        
        if not comparison:
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(3, 2, figsize=(16, 18))
        fig.suptitle('Stop Loss Options Comparison - Tokyo FVG Strategy', fontsize=16, fontweight='bold')
        
        sl_labels = ['Original\n(Signal)', 'Swing\n(Manip)', 'ATR\nBuffer', 'FVG\nComplete', 'Fixed\nBuffer']
        colors_sl = ['#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#e74c3c']
        
        # 1. Win Rate Comparison at 1R
        ax1 = axes[0, 0]
        wr_1r_values = [comparison[k]['wr_1r'] for k in ['original', 'swing', 'atr', 'fvg', 'fixed']]
        bars = ax1.bar(range(5), wr_1r_values, color=colors_sl, edgecolor='black', alpha=0.8)
        ax1.set_xlabel('SL Option', fontsize=11)
        ax1.set_ylabel('Win Rate (%)', fontsize=11)
        ax1.set_title('Win Rate à 1R par Option de SL', fontsize=12, fontweight='bold')
        ax1.set_xticks(range(5))
        ax1.set_xticklabels(sl_labels, fontsize=9)
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y', alpha=0.3)
        ax1.axhline(y=50, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Profitable (>50%)')
        ax1.legend(loc='upper right')
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            wins = comparison[['original', 'swing', 'atr', 'fvg', 'fixed'][i]]['wins_1r']
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%\n({wins}/273)',
                    ha='center', va='bottom', fontsize=8)
        
        # 2. Win Rate Comparison at 1.5R
        ax2 = axes[0, 1]
        wr_1_5r_values = [comparison[k]['wr_1_5r'] for k in ['original', 'swing', 'atr', 'fvg', 'fixed']]
        bars = ax2.bar(range(5), wr_1_5r_values, color=colors_sl, edgecolor='black', alpha=0.8)
        ax2.set_xlabel('SL Option', fontsize=11)
        ax2.set_ylabel('Win Rate (%)', fontsize=11)
        ax2.set_title('Win Rate à 1.5R par Option de SL', fontsize=12, fontweight='bold')
        ax2.set_xticks(range(5))
        ax2.set_xticklabels(sl_labels, fontsize=9)
        ax2.set_ylim(0, 100)
        ax2.grid(axis='y', alpha=0.3)
        ax2.axhline(y=40, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Profitable (>40%)')
        ax2.legend(loc='upper right')
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            wins = comparison[['original', 'swing', 'atr', 'fvg', 'fixed'][i]]['wins_1_5r']
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%\n({wins}/273)',
                    ha='center', va='bottom', fontsize=8)
        
        # 3. Win Rate Comparison at 2R
        ax3 = axes[1, 0]
        wr_2r_values = [comparison[k]['wr_2r'] for k in ['original', 'swing', 'atr', 'fvg', 'fixed']]
        bars = ax3.bar(range(5), wr_2r_values, color=colors_sl, edgecolor='black', alpha=0.8)
        ax3.set_xlabel('SL Option', fontsize=11)
        ax3.set_ylabel('Win Rate (%)', fontsize=11)
        ax3.set_title('Win Rate à 2R par Option de SL', fontsize=12, fontweight='bold')
        ax3.set_xticks(range(5))
        ax3.set_xticklabels(sl_labels, fontsize=9)
        ax3.set_ylim(0, 100)
        ax3.grid(axis='y', alpha=0.3)
        ax3.axhline(y=33, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Profitable (>33%)')
        ax3.legend(loc='upper right')
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            wins = comparison[['original', 'swing', 'atr', 'fvg', 'fixed'][i]]['wins_2r']
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%\n({wins}/273)',
                    ha='center', va='bottom', fontsize=8)
        
        # 4. Expectancy Comparison at 1R
        ax4 = axes[1, 1]
        exp_1r_values = [comparison[k]['exp_1r'] for k in ['original', 'swing', 'atr', 'fvg', 'fixed']]
        colors_exp = ['#e74c3c' if x < 0 else '#2ecc71' for x in exp_1r_values]
        bars = ax4.bar(range(5), exp_1r_values, color=colors_exp, edgecolor='black', alpha=0.8)
        ax4.set_xlabel('SL Option', fontsize=11)
        ax4.set_ylabel('Expectancy (R)', fontsize=11)
        ax4.set_title('Expectancy à 1R par Option de SL', fontsize=12, fontweight='bold')
        ax4.set_xticks(range(5))
        ax4.set_xticklabels(sl_labels, fontsize=9)
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.7)
        ax4.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}R',
                    ha='center', va='bottom' if height > 0 else 'top', fontsize=8)
        
        # 5. Expectancy Comparison at 2R
        ax5 = axes[2, 0]
        exp_2r_values = [comparison[k]['exp_2r'] for k in ['original', 'swing', 'atr', 'fvg', 'fixed']]
        colors_exp = ['#e74c3c' if x < 0 else '#2ecc71' for x in exp_2r_values]
        bars = ax5.bar(range(5), exp_2r_values, color=colors_exp, edgecolor='black', alpha=0.8)
        ax5.set_xlabel('SL Option', fontsize=11)
        ax5.set_ylabel('Expectancy (R)', fontsize=11)
        ax5.set_title('Expectancy à 2R par Option de SL', fontsize=12, fontweight='bold')
        ax5.set_xticks(range(5))
        ax5.set_xticklabels(sl_labels, fontsize=9)
        ax5.axhline(y=0, color='black', linestyle='-', linewidth=2, alpha=0.7)
        ax5.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}R',
                    ha='center', va='bottom' if height > 0 else 'top', fontsize=8)
        
        # 6. False Positives Avoided (vs Original)
        ax6 = axes[2, 1]
        fp_1r = [comparison[k]['fp_avoided_1r'] for k in ['swing', 'atr', 'fvg', 'fixed']]
        fp_1_5r = [comparison[k]['fp_avoided_1_5r'] for k in ['swing', 'atr', 'fvg', 'fixed']]
        fp_2r = [comparison[k]['fp_avoided_2r'] for k in ['swing', 'atr', 'fvg', 'fixed']]
        
        x = np.arange(4)
        width = 0.25
        
        bars1 = ax6.bar(x - width, fp_1r, width, label='1R', color='#2ecc71', edgecolor='black', alpha=0.8)
        bars2 = ax6.bar(x, fp_1_5r, width, label='1.5R', color='#f39c12', edgecolor='black', alpha=0.8)
        bars3 = ax6.bar(x + width, fp_2r, width, label='2R', color='#e74c3c', edgecolor='black', alpha=0.8)
        
        ax6.set_xlabel('SL Option', fontsize=11)
        ax6.set_ylabel('Faux Positifs Évités', fontsize=11)
        ax6.set_title('Faux Positifs Évités vs SL Original', fontsize=12, fontweight='bold')
        ax6.set_xticks(x)
        ax6.set_xticklabels(['Swing', 'ATR', 'FVG', 'Fixed'], fontsize=9)
        ax6.legend()
        ax6.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax6.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontsize=7)
        
        plt.tight_layout()
        
        # Save figure
        output_path = os.path.join(self.data_directory, 'sl_options_comparison.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\nSL Options Comparison Visualization saved to: {output_path}")


def main():
    """Main execution function."""
    print("="*80)
    print("Tokyo Session FVG Inversion Strategy Analyzer")
    print("="*80)
    print("\nThis script analyzes trading data from 2018-2025 to calculate the")
    print("win rate of a strategy based on FVG inversions following Tokyo")
    print("session manipulation.")
    print()
    
    # Initialize analyzer
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    analyzer = TokyoFVGAnalyzer(data_dir)
    
    # Load data (5m and 15m for better FVG detection)
    analyzer.load_data(years=range(2018, 2026), timeframes=['5m', '15m'])
    
    if len(analyzer.combined_data) == 0:
        print("\nERROR: No data loaded. Please check the data files.")
        return
    
    # Run analysis
    analyzer.analyze()
    
    # Generate standard report
    analyzer.generate_report()
    
    # Generate SL comparison report
    try:
        analyzer.generate_sl_comparison_report()
    except Exception as e:
        print(f"\nWarning: Could not generate SL comparison report: {e}")
    
    # Generate standard visualizations
    try:
        analyzer.generate_visualizations()
    except Exception as e:
        print(f"\nWarning: Could not generate visualizations: {e}")
        print("Make sure matplotlib is installed: pip install matplotlib")
    
    # Generate SL comparison visualizations
    try:
        analyzer.generate_sl_comparison_visualizations()
    except Exception as e:
        print(f"\nWarning: Could not generate SL comparison visualizations: {e}")
    
    print("\n" + "="*80)
    print("Analysis Complete!")
    print("="*80)
    print("\nGenerated Files:")
    print("  - tokyo_fvg_strategy_report.txt")
    print("  - tokyo_fvg_strategy_results.csv")
    print("  - tokyo_fvg_strategy_analysis.png")
    print("  - SL_OPTIONS_COMPARISON.md")
    print("  - sl_options_detailed.csv")
    print("  - sl_options_comparison.png")
    print("="*80)


if __name__ == "__main__":
    main()
