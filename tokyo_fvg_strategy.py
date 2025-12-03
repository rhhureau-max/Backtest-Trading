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
                
                trade_result = self.simulate_trade(
                    entry_price,
                    stop_loss,
                    take_profit,
                    entry_time,
                    direction,
                    hours=24
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
        print(f"\nTRADE RESULTS:")
        print(f"Total trades executed: {total_trades}")
        print(f"Winning trades: {winning_trades}")
        print(f"Losing trades: {losing_trades}")
        print(f"No exit trades: {no_exit_trades}")
        
        if total_trades > 0:
            win_rate = (winning_trades / total_trades) * 100
            print(f"\n{'='*80}")
            print(f"WIN RATE: {win_rate:.2f}%")
            print(f"{'='*80}")
    
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
            f.write("  - Only trades with Risk/Reward ratio >= 1.0 are executed\n")
            f.write("  - Risk = |Entry - Stop Loss|\n")
            f.write("  - Reward = |Take Profit - Entry|\n")
            f.write("  - Trades with R/R < 1.0 are completely excluded from analysis\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("R/R FILTER IMPACT:\n")
            f.write("-" * 80 + "\n")
            total_potential_trades = total_trades + self.filtered_trades_count
            kept_percentage = (total_trades / total_potential_trades * 100) if total_potential_trades > 0 else 0
            filtered_percentage = (self.filtered_trades_count / total_potential_trades * 100) if total_potential_trades > 0 else 0
            f.write(f"Total potential trades (before filter): {total_potential_trades}\n")
            f.write(f"Trades filtered out (R/R < 1.0): {self.filtered_trades_count} ({filtered_percentage:.2f}%)\n")
            f.write(f"Trades kept (R/R >= 1.0): {total_trades} ({kept_percentage:.2f}%)\n")
            f.write("\n" + "="*80 + "\n\n")
            
            f.write("OVERALL RESULTS:\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Trades: {total_trades}\n")
            f.write(f"Winning Trades: {winning_trades}\n")
            f.write(f"Losing Trades: {losing_trades}\n")
            f.write(f"No Exit Trades: {no_exit_trades}\n")
            f.write(f"\n>>> WIN RATE: {win_rate:.2f}% <<<\n")
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
                f.write(f"  Take Profit: {row['take_profit']:.2f}\n")
                f.write(f"  Risk/Reward: {row['rr_ratio']:.2f}\n")
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
        
        # Create figure with subplots
        fig, axes = plt.subplots(3, 2, figsize=(15, 18))
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
        
        # 4. Risk/Reward Distribution
        ax4 = axes[1, 1]
        if len(completed_trades) > 0:
            ax4.hist(completed_trades['rr_ratio'], bins=20, color='#1abc9c', edgecolor='black', alpha=0.7)
            ax4.axvline(completed_trades['rr_ratio'].mean(), color='red', linestyle='--', 
                       linewidth=2, label=f'Mean: {completed_trades["rr_ratio"].mean():.2f}')
            ax4.set_xlabel('Risk/Reward Ratio')
            ax4.set_ylabel('Frequency')
            ax4.set_title('Risk/Reward Distribution')
            ax4.legend()
            ax4.grid(axis='y', alpha=0.3)
        
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
        
        plt.tight_layout()
        
        # Save figure
        output_path = os.path.join(self.data_directory, 'tokyo_fvg_strategy_analysis.png')
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"\nVisualization saved to: {output_path}")


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
    
    # Generate report
    analyzer.generate_report()
    
    # Generate visualizations
    try:
        analyzer.generate_visualizations()
    except Exception as e:
        print(f"\nWarning: Could not generate visualizations: {e}")
        print("Make sure matplotlib is installed: pip install matplotlib")
    
    print("\n" + "="*80)
    print("Analysis Complete!")
    print("="*80)


if __name__ == "__main__":
    main()
