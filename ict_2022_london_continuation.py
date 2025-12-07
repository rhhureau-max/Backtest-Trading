#!/usr/bin/env python3
"""
ICT 2022 Model - London Continuation Strategy Backtest
=======================================================

This script implements a complete backtesting system for the ICT 2022 Model
applied to London continuation trading on NQ 5-minute data.

Strategy Logic:
1. Tokyo Session (19:00-23:00 previous day): Identify range (High, Low, EQ)
2. Midnight Open (00:00): Record open price
3. Event 1 - Liquidity Sweep (01:00-04:00): Price sweeps below Tokyo_Low while below Midnight_Open
4. Event 2 - Market Structure Shift: Internal structure break confirmation
5. Event 3 - FVG Entry: Enter at Fair Value Gap after displacement
6. Exit: Stop at Sweep_Low, Targets at Tokyo_EQ, Tokyo_High, Tokyo_High+10

Author: ICT Trading System
Date: 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import os
import glob

class ICT2022Model:
    """Main class for ICT 2022 Model backtesting"""
    
    def __init__(self, data_dir="/home/runner/work/Backtest-Trading/Backtest-Trading"):
        self.data_dir = data_dir
        self.df = None
        self.trades = []
        
    def load_data(self):
        """Load all 5-minute NQ data files from 2018-2025"""
        print("Loading data files...")
        
        all_data = []
        for year in range(2018, 2026):
            filepath = os.path.join(self.data_dir, f"{year} 5m.csv")
            if os.path.exists(filepath):
                print(f"  Loading {year} 5m.csv...")
                df_year = pd.read_csv(filepath, sep=';', skiprows=0)
                
                # Rename columns properly
                df_year.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                
                all_data.append(df_year)
        
        # Combine all years
        self.df = pd.concat(all_data, ignore_index=True)
        
        # Parse datetime - data is already in Chicago time
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'], 
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Sort by datetime
        self.df = self.df.sort_values('DateTime').reset_index(drop=True)
        
        # Extract time components
        self.df['Hour'] = self.df['DateTime'].dt.hour
        self.df['Minute'] = self.df['DateTime'].dt.minute
        self.df['DayOfWeek'] = self.df['DateTime'].dt.dayofweek  # 0=Monday
        
        print(f"Loaded {len(self.df)} candles from {self.df['DateTime'].min()} to {self.df['DateTime'].max()}")
        
        return self.df
    
    def calculate_ema(self, period=20):
        """Calculate EMA for MSS detection (Method 2)"""
        self.df['EMA_20'] = self.df['Close'].ewm(span=period, adjust=False).mean()
        self.df['Body_Size'] = abs(self.df['Close'] - self.df['Open'])
        self.df['Avg_Body_20'] = self.df['Body_Size'].rolling(window=20).mean()
    
    def get_tokyo_session_data(self, current_idx):
        """
        Get Tokyo session data for the PREVIOUS day (N-1)
        Tokyo Session: 19:00 - 23:00 (previous day)
        """
        current_dt = self.df.loc[current_idx, 'DateTime']
        
        # Tokyo session is on the previous calendar day
        tokyo_date = current_dt.date() - timedelta(days=1)
        
        # Define Tokyo session time range (19:00-23:00)
        tokyo_start = datetime.combine(tokyo_date, time(19, 0))
        tokyo_end = datetime.combine(tokyo_date, time(23, 0))
        
        # Find candles in Tokyo session
        tokyo_mask = (self.df['DateTime'] >= tokyo_start) & (self.df['DateTime'] <= tokyo_end)
        tokyo_candles = self.df[tokyo_mask]
        
        if len(tokyo_candles) == 0:
            return None, None, None
        
        tokyo_high = tokyo_candles['High'].max()
        tokyo_low = tokyo_candles['Low'].min()
        tokyo_eq = (tokyo_high + tokyo_low) / 2
        
        return tokyo_high, tokyo_low, tokyo_eq
    
    def get_midnight_open(self, current_idx):
        """
        Get the open price at midnight (00:00) on day N
        """
        current_dt = self.df.loc[current_idx, 'DateTime']
        midnight_date = current_dt.date()
        
        # Look for the candle at exactly 00:00
        midnight_dt = datetime.combine(midnight_date, time(0, 0))
        
        midnight_mask = (self.df['DateTime'] == midnight_dt)
        midnight_candles = self.df[midnight_mask]
        
        if len(midnight_candles) > 0:
            return midnight_candles.iloc[0]['Open']
        
        # If exact midnight not found, look for nearest candle after midnight
        after_midnight = self.df[self.df['DateTime'] >= midnight_dt]
        if len(after_midnight) > 0:
            return after_midnight.iloc[0]['Open']
        
        return None
    
    def detect_liquidity_sweep(self, current_idx, tokyo_low, midnight_open):
        """
        Event 1: Detect liquidity sweep below Tokyo_Low
        Time window: 01:00 - 04:00 (London Killzone)
        Condition: Price must go BELOW Tokyo_Low while below Midnight_Open
        Returns: (sweep_occurred, sweep_low, sweep_idx)
        """
        current_dt = self.df.loc[current_idx, 'DateTime']
        current_date = current_dt.date()
        
        # Define London Killzone (01:00-04:00)
        london_start = datetime.combine(current_date, time(1, 0))
        london_end = datetime.combine(current_date, time(4, 0))
        
        # Find candles in London Killzone
        london_mask = (
            (self.df['DateTime'] >= london_start) & 
            (self.df['DateTime'] <= london_end)
        )
        london_candles = self.df[london_mask]
        
        if len(london_candles) == 0:
            return False, None, None
        
        # Check for sweep: Low goes below Tokyo_Low AND price is below Midnight_Open
        for idx in london_candles.index:
            candle_low = self.df.loc[idx, 'Low']
            candle_close = self.df.loc[idx, 'Close']
            
            # Sweep condition: low breaks Tokyo_Low while trading below Midnight_Open (discount)
            if candle_low < tokyo_low and candle_close < midnight_open:
                # Find the lowest point during the sweep period
                sweep_low = london_candles['Low'].min()
                sweep_idx = london_candles['Low'].idxmin()
                return True, sweep_low, sweep_idx
        
        return False, None, None
    
    def detect_mss_method1(self, sweep_idx):
        """
        Method 1 (Primary - Simplified): MSS Detection
        - Look at 3 M5 candles immediately BEFORE the sweep low
        - Find highest high among these 3 candles (Pre-Sweep High)
        - MSS confirmed when price CLOSES above Pre-Sweep High
        Returns: (mss_occurred, mss_idx)
        """
        if sweep_idx < 3:
            return False, None
        
        # Get 3 candles before the sweep low
        pre_sweep_candles = self.df.loc[sweep_idx-3:sweep_idx-1]
        pre_sweep_high = pre_sweep_candles['High'].max()
        
        # Look for close above pre-sweep high AFTER the sweep
        # Search for next 20 candles (100 minutes) for MSS
        search_end = min(sweep_idx + 20, len(self.df) - 1)
        
        for idx in range(sweep_idx + 1, search_end + 1):
            if self.df.loc[idx, 'Close'] > pre_sweep_high:
                return True, idx
        
        return False, None
    
    def detect_mss_method2(self, sweep_idx):
        """
        Method 2 (Alternative - EMA based): MSS Detection
        - After sweep, MSS confirmed when:
          - Price closes above EMA 20
          - AND candle body size > average body size of last 20 candles
        Returns: (mss_occurred, mss_idx)
        """
        # Search for next 20 candles after sweep
        search_end = min(sweep_idx + 20, len(self.df) - 1)
        
        for idx in range(sweep_idx + 1, search_end + 1):
            candle_close = self.df.loc[idx, 'Close']
            ema_20 = self.df.loc[idx, 'EMA_20']
            body_size = self.df.loc[idx, 'Body_Size']
            avg_body = self.df.loc[idx, 'Avg_Body_20']
            
            # MSS condition: Close above EMA and strong body
            if candle_close > ema_20 and body_size > avg_body:
                return True, idx
        
        return False, None
    
    def detect_fvg(self, mss_idx):
        """
        Event 3: Detect Fair Value Gap after MSS
        Bullish FVG: Candle[i].Low > Candle[i-2].High
        Returns: (fvg_found, fvg_top, fvg_bottom, fvg_idx)
        """
        # Search for FVG in next 20 candles after MSS
        search_end = min(mss_idx + 20, len(self.df) - 1)
        
        for idx in range(mss_idx + 2, search_end + 1):
            # Check for bullish FVG
            current_low = self.df.loc[idx, 'Low']
            two_candles_back_high = self.df.loc[idx - 2, 'High']
            
            if current_low > two_candles_back_high:
                # FVG detected
                fvg_top = current_low
                fvg_bottom = two_candles_back_high
                return True, fvg_top, fvg_bottom, idx
        
        return False, None, None, None
    
    def simulate_trade(self, entry_price, stop_loss, tp1, tp2, tp3, entry_idx):
        """
        Simulate a trade from entry to exit
        Returns: Trade result dictionary
        """
        trade = {
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'tp1': tp1,
            'tp2': tp2,
            'tp3': tp3,
            'entry_time': self.df.loc[entry_idx, 'DateTime'],
            'exit_time': None,
            'exit_price': None,
            'exit_type': None,  # 'SL', 'TP1', 'TP2', 'TP3', 'EOD'
            'points': 0,
            'rr_ratio': 0,
            'duration_minutes': 0
        }
        
        risk = entry_price - stop_loss
        
        # Get next Tokyo session start (19:00) as cutoff
        entry_date = self.df.loc[entry_idx, 'DateTime'].date()
        eod_cutoff = datetime.combine(entry_date, time(19, 0))
        
        # Simulate tick-by-tick from entry
        for idx in range(entry_idx + 1, len(self.df)):
            candle = self.df.loc[idx]
            candle_dt = candle['DateTime']
            
            # Check if we've reached next Tokyo session (end of day)
            if candle_dt >= eod_cutoff:
                trade['exit_time'] = candle_dt
                trade['exit_price'] = candle['Close']
                trade['exit_type'] = 'EOD'
                trade['points'] = trade['exit_price'] - entry_price
                trade['duration_minutes'] = (trade['exit_time'] - trade['entry_time']).total_seconds() / 60
                break
            
            # Check stop loss hit
            if candle['Low'] <= stop_loss:
                trade['exit_time'] = candle_dt
                trade['exit_price'] = stop_loss
                trade['exit_type'] = 'SL'
                trade['points'] = stop_loss - entry_price
                trade['rr_ratio'] = -1
                trade['duration_minutes'] = (trade['exit_time'] - trade['entry_time']).total_seconds() / 60
                break
            
            # Check TP3 hit (highest target)
            if candle['High'] >= tp3:
                trade['exit_time'] = candle_dt
                trade['exit_price'] = tp3
                trade['exit_type'] = 'TP3'
                trade['points'] = tp3 - entry_price
                trade['rr_ratio'] = (tp3 - entry_price) / risk
                trade['duration_minutes'] = (trade['exit_time'] - trade['entry_time']).total_seconds() / 60
                break
            
            # Check TP2 hit (Tokyo_High - KEY TARGET)
            if candle['High'] >= tp2:
                trade['exit_time'] = candle_dt
                trade['exit_price'] = tp2
                trade['exit_type'] = 'TP2'
                trade['points'] = tp2 - entry_price
                trade['rr_ratio'] = (tp2 - entry_price) / risk
                trade['duration_minutes'] = (trade['exit_time'] - trade['entry_time']).total_seconds() / 60
                break
            
            # Check TP1 hit
            if candle['High'] >= tp1:
                trade['exit_time'] = candle_dt
                trade['exit_price'] = tp1
                trade['exit_type'] = 'TP1'
                trade['points'] = tp1 - entry_price
                trade['rr_ratio'] = (tp1 - entry_price) / risk
                trade['duration_minutes'] = (trade['exit_time'] - trade['entry_time']).total_seconds() / 60
                break
        
        return trade
    
    def check_entry_filled(self, fvg_top, fvg_idx, eod_cutoff):
        """
        Check if entry at FVG_Top gets filled before end of day
        Returns: (filled, fill_idx)
        """
        for idx in range(fvg_idx + 1, len(self.df)):
            candle_dt = self.df.loc[idx, 'DateTime']
            
            # Check if we've reached next Tokyo session
            if candle_dt >= eod_cutoff:
                return False, None
            
            # Check if price touches FVG top
            if self.df.loc[idx, 'Low'] <= fvg_top:
                return True, idx
        
        return False, None
    
    def run_backtest_mss_method(self, use_method1=True):
        """
        Run complete backtest using specified MSS method
        """
        print(f"\n{'='*60}")
        print(f"Running backtest with MSS Method {'1 (Simplified)' if use_method1 else '2 (EMA-based)'}")
        print(f"{'='*60}\n")
        
        setups_found = 0
        entries_filled = 0
        trades = []
        
        # Process day by day
        unique_dates = self.df['DateTime'].dt.date.unique()
        
        for date in unique_dates:
            # Skip weekends
            day_of_week = pd.to_datetime(date).dayofweek
            if day_of_week >= 5:  # Saturday or Sunday
                continue
            
            # Get a candle from current day (use 02:00 as reference)
            reference_time = datetime.combine(date, time(2, 0))
            reference_mask = self.df['DateTime'] == reference_time
            
            if reference_mask.sum() == 0:
                continue
            
            reference_idx = self.df[reference_mask].index[0]
            
            # Phase 1: Get Tokyo session data (previous day N-1)
            tokyo_high, tokyo_low, tokyo_eq = self.get_tokyo_session_data(reference_idx)
            
            if tokyo_high is None:
                continue
            
            # Get Midnight Open (day N)
            midnight_open = self.get_midnight_open(reference_idx)
            
            if midnight_open is None:
                continue
            
            # Phase 2: Detect liquidity sweep (01:00-04:00)
            sweep_occurred, sweep_low, sweep_idx = self.detect_liquidity_sweep(
                reference_idx, tokyo_low, midnight_open
            )
            
            if not sweep_occurred:
                continue
            
            setups_found += 1
            
            # Phase 3: Detect Market Structure Shift
            if use_method1:
                mss_occurred, mss_idx = self.detect_mss_method1(sweep_idx)
            else:
                mss_occurred, mss_idx = self.detect_mss_method2(sweep_idx)
            
            if not mss_occurred:
                continue
            
            # Phase 4: Detect FVG
            fvg_found, fvg_top, fvg_bottom, fvg_idx = self.detect_fvg(mss_idx)
            
            if not fvg_found:
                continue
            
            # Define targets
            # TP1: Tokyo_EQ or Midnight_Open (whichever is closer but above entry)
            tp1_candidates = [tokyo_eq, midnight_open]
            tp1_candidates = [t for t in tp1_candidates if t > fvg_top]
            tp1 = min(tp1_candidates) if tp1_candidates else tokyo_eq
            
            tp2 = tokyo_high  # KEY TARGET
            tp3 = tokyo_high + 10  # Expansion target
            
            # Check if entry gets filled
            eod_cutoff = datetime.combine(date, time(19, 0))
            entry_filled, entry_idx = self.check_entry_filled(fvg_top, fvg_idx, eod_cutoff)
            
            if not entry_filled:
                continue
            
            entries_filled += 1
            
            # Simulate trade
            trade = self.simulate_trade(
                entry_price=fvg_top,
                stop_loss=sweep_low,
                tp1=tp1,
                tp2=tp2,
                tp3=tp3,
                entry_idx=entry_idx
            )
            
            # Add context to trade
            trade['date'] = date
            trade['tokyo_high'] = tokyo_high
            trade['tokyo_low'] = tokyo_low
            trade['tokyo_eq'] = tokyo_eq
            trade['midnight_open'] = midnight_open
            trade['sweep_low'] = sweep_low
            
            trades.append(trade)
        
        return setups_found, entries_filled, trades
    
    def run_backtest_full_range_breakout(self):
        """
        Alternative strategy: Wait for full range breakout above Tokyo_High,
        then enter on pullback
        """
        print(f"\n{'='*60}")
        print(f"Running backtest with Full Range Breakout Method")
        print(f"{'='*60}\n")
        
        setups_found = 0
        entries_filled = 0
        trades = []
        
        unique_dates = self.df['DateTime'].dt.date.unique()
        
        for date in unique_dates:
            day_of_week = pd.to_datetime(date).dayofweek
            if day_of_week >= 5:
                continue
            
            reference_time = datetime.combine(date, time(2, 0))
            reference_mask = self.df['DateTime'] == reference_time
            
            if reference_mask.sum() == 0:
                continue
            
            reference_idx = self.df[reference_mask].index[0]
            
            # Get Tokyo session data
            tokyo_high, tokyo_low, tokyo_eq = self.get_tokyo_session_data(reference_idx)
            
            if tokyo_high is None:
                continue
            
            midnight_open = self.get_midnight_open(reference_idx)
            
            if midnight_open is None:
                continue
            
            # Detect sweep
            sweep_occurred, sweep_low, sweep_idx = self.detect_liquidity_sweep(
                reference_idx, tokyo_low, midnight_open
            )
            
            if not sweep_occurred:
                continue
            
            setups_found += 1
            
            # Wait for breakout above Tokyo_High
            eod_cutoff = datetime.combine(date, time(19, 0))
            breakout_idx = None
            
            for idx in range(sweep_idx + 1, len(self.df)):
                if self.df.loc[idx, 'DateTime'] >= eod_cutoff:
                    break
                
                if self.df.loc[idx, 'Close'] > tokyo_high:
                    breakout_idx = idx
                    break
            
            if breakout_idx is None:
                continue
            
            # Look for pullback entry (price returns to Tokyo_High)
            entry_price = tokyo_high
            entry_filled = False
            entry_idx = None
            
            for idx in range(breakout_idx + 1, len(self.df)):
                if self.df.loc[idx, 'DateTime'] >= eod_cutoff:
                    break
                
                if self.df.loc[idx, 'Low'] <= tokyo_high:
                    entry_filled = True
                    entry_idx = idx
                    break
            
            if not entry_filled:
                continue
            
            entries_filled += 1
            
            # Define targets for breakout method
            tp1 = tokyo_high + 10
            tp2 = tokyo_high + 20
            tp3 = tokyo_high + 30
            
            # Simulate trade
            trade = self.simulate_trade(
                entry_price=entry_price,
                stop_loss=sweep_low,
                tp1=tp1,
                tp2=tp2,
                tp3=tp3,
                entry_idx=entry_idx
            )
            
            trade['date'] = date
            trade['tokyo_high'] = tokyo_high
            trade['tokyo_low'] = tokyo_low
            trade['sweep_low'] = sweep_low
            
            trades.append(trade)
        
        return setups_found, entries_filled, trades
    
    def calculate_metrics(self, trades):
        """Calculate performance metrics for a list of trades"""
        if len(trades) == 0:
            return None
        
        total_trades = len(trades)
        
        # Win rates
        winners = [t for t in trades if t['points'] > 0]
        losers = [t for t in trades if t['points'] < 0]
        
        win_rate_overall = len(winners) / total_trades * 100
        
        # Win rate to each TP level
        tp1_hits = len([t for t in trades if t['exit_type'] in ['TP1', 'TP2', 'TP3']])
        tp2_hits = len([t for t in trades if t['exit_type'] in ['TP2', 'TP3']])
        tp3_hits = len([t for t in trades if t['exit_type'] == 'TP3'])
        
        win_rate_tp1 = tp1_hits / total_trades * 100
        win_rate_tp2 = tp2_hits / total_trades * 100  # KEY METRIC
        win_rate_tp3 = tp3_hits / total_trades * 100
        
        # Risk/Reward
        avg_rr = np.mean([t['rr_ratio'] for t in trades if t['rr_ratio'] > 0])
        
        # Net points
        net_points = sum([t['points'] for t in trades])
        
        # Profit factor
        gross_profit = sum([t['points'] for t in winners])
        gross_loss = abs(sum([t['points'] for t in losers]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Max consecutive losses
        max_consecutive_losses = 0
        current_consecutive = 0
        for trade in trades:
            if trade['points'] < 0:
                current_consecutive += 1
                max_consecutive_losses = max(max_consecutive_losses, current_consecutive)
            else:
                current_consecutive = 0
        
        # Average trade duration
        avg_duration = np.mean([t['duration_minutes'] for t in trades])
        
        return {
            'total_trades': total_trades,
            'winners': len(winners),
            'losers': len(losers),
            'win_rate_overall': win_rate_overall,
            'win_rate_tp1': win_rate_tp1,
            'win_rate_tp2': win_rate_tp2,
            'win_rate_tp3': win_rate_tp3,
            'avg_rr': avg_rr,
            'net_points': net_points,
            'profit_factor': profit_factor,
            'max_consecutive_losses': max_consecutive_losses,
            'avg_duration_minutes': avg_duration,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss
        }
    
    def print_results(self, method_name, setups, entries, trades, metrics):
        """Print formatted results"""
        print(f"\n{'-'*60}")
        print(f"--- {method_name} ---")
        print(f"{'-'*60}")
        print(f"Total Setups: {setups}")
        print(f"Entries Filled: {entries} ({entries/setups*100:.1f}%)" if setups > 0 else "Entries Filled: 0")
        print(f"Trades: {len(trades)}")
        print()
        
        if metrics:
            print(f"Win Rate Overall: {metrics['win_rate_overall']:.1f}%")
            print(f"Win Rate to TP1: {metrics['win_rate_tp1']:.1f}%")
            print(f"Win Rate to TP2 (Tokyo_High): {metrics['win_rate_tp2']:.1f}% ← KEY METRIC")
            print(f"Win Rate to TP3 (Tokyo_High + 10): {metrics['win_rate_tp3']:.1f}%")
            print()
            print(f"Average RR: {metrics['avg_rr']:.2f}:1")
            print(f"Net Points: {metrics['net_points']:+.2f}")
            print(f"Profit Factor: {metrics['profit_factor']:.2f}")
            print(f"Max Consecutive Losses: {metrics['max_consecutive_losses']}")
            print(f"Average Trade Duration: {metrics['avg_duration_minutes']:.1f} minutes")
        else:
            print("No trades to analyze.")
    
    def run_complete_backtest(self):
        """Run the complete backtesting suite"""
        print("\n" + "="*60)
        print("ICT 2022 Model - London Continuation Backtest")
        print("="*60)
        print("Data: NQ 5-minute (2018-2025)")
        print("Strategy: Enter INSIDE range after sweep & MSS, target OUTSIDE (Tokyo_High)")
        print("="*60)
        
        # Load data
        self.load_data()
        
        # Calculate EMA for Method 2
        self.calculate_ema()
        
        # Method 1: MSS (Simplified) + FVG Entry
        setups1, entries1, trades1 = self.run_backtest_mss_method(use_method1=True)
        metrics1 = self.calculate_metrics(trades1)
        
        # Method 2: Full Range Breakout Entry
        setups2, entries2, trades2 = self.run_backtest_full_range_breakout()
        metrics2 = self.calculate_metrics(trades2)
        
        # Print results
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)
        
        self.print_results(
            "Entry Method 1: MSS (Internal Structure) + FVG Entry",
            setups1, entries1, trades1, metrics1
        )
        
        self.print_results(
            "Entry Method 2: Full Range Breakout Entry",
            setups2, entries2, trades2, metrics2
        )
        
        # Comparison
        if metrics1 and metrics2:
            print(f"\n{'-'*60}")
            print("--- Comparison ---")
            print(f"{'-'*60}")
            
            if metrics1['win_rate_tp2'] > metrics2['win_rate_tp2']:
                print(f"MSS Entry is MORE profitable than Full Range Entry")
            else:
                print(f"MSS Entry is LESS profitable than Full Range Entry")
            
            print(f"Difference in Win Rate to Tokyo_High: {metrics1['win_rate_tp2'] - metrics2['win_rate_tp2']:+.1f}%")
            print(f"Difference in Net Points: {metrics1['net_points'] - metrics2['net_points']:+.2f} points")
            print()
        
        # Save results to file
        self.save_results_to_file(setups1, entries1, trades1, metrics1, 
                                   setups2, entries2, trades2, metrics2)
        
        return trades1, trades2
    
    def save_results_to_file(self, setups1, entries1, trades1, metrics1,
                             setups2, entries2, trades2, metrics2):
        """Save results to ICT_2022_RESULTS.txt"""
        filepath = os.path.join(self.data_dir, "ICT_2022_RESULTS.txt")
        
        with open(filepath, 'w') as f:
            f.write("="*60 + "\n")
            f.write("ICT 2022 Model - London Continuation Backtest\n")
            f.write("="*60 + "\n")
            f.write("Data: NQ 5-minute (2018-2025)\n\n")
            f.write("Strategy: Enter INSIDE range after sweep & MSS, target OUTSIDE (Tokyo_High)\n\n")
            
            f.write("-"*60 + "\n")
            f.write("--- Entry Method 1: MSS (Internal Structure) + FVG Entry ---\n")
            f.write("-"*60 + "\n")
            f.write(f"Total Setups: {setups1}\n")
            if setups1 > 0:
                f.write(f"Entries Filled: {entries1} ({entries1/setups1*100:.1f}%)\n")
            f.write(f"Trades: {len(trades1)}\n\n")
            
            if metrics1:
                f.write(f"Win Rate Overall: {metrics1['win_rate_overall']:.1f}%\n")
                f.write(f"Win Rate to TP1 (Tokyo_EQ): {metrics1['win_rate_tp1']:.1f}%\n")
                f.write(f"Win Rate to TP2 (Tokyo_High): {metrics1['win_rate_tp2']:.1f}% ← KEY METRIC\n")
                f.write(f"Win Rate to TP3 (Tokyo_High + 10): {metrics1['win_rate_tp3']:.1f}%\n\n")
                f.write(f"Average RR: {metrics1['avg_rr']:.2f}:1\n")
                f.write(f"Net Points: {metrics1['net_points']:+.2f}\n")
                f.write(f"Profit Factor: {metrics1['profit_factor']:.2f}\n")
                f.write(f"Max Consecutive Losses: {metrics1['max_consecutive_losses']}\n")
                f.write(f"Average Trade Duration: {metrics1['avg_duration_minutes']:.1f} minutes\n\n")
            
            f.write("-"*60 + "\n")
            f.write("--- Entry Method 2: Full Range Breakout Entry ---\n")
            f.write("-"*60 + "\n")
            f.write(f"Total Setups: {setups2}\n")
            if setups2 > 0:
                f.write(f"Entries Filled: {entries2} ({entries2/setups2*100:.1f}%)\n")
            f.write(f"Trades: {len(trades2)}\n\n")
            
            if metrics2:
                f.write(f"Win Rate Overall: {metrics2['win_rate_overall']:.1f}%\n")
                f.write(f"Win Rate to TP1: {metrics2['win_rate_tp1']:.1f}%\n")
                f.write(f"Win Rate to TP2: {metrics2['win_rate_tp2']:.1f}%\n")
                f.write(f"Win Rate to TP3: {metrics2['win_rate_tp3']:.1f}%\n\n")
                f.write(f"Average RR: {metrics2['avg_rr']:.2f}:1\n")
                f.write(f"Net Points: {metrics2['net_points']:+.2f}\n")
                f.write(f"Profit Factor: {metrics2['profit_factor']:.2f}\n")
                f.write(f"Max Consecutive Losses: {metrics2['max_consecutive_losses']}\n")
                f.write(f"Average Trade Duration: {metrics2['avg_duration_minutes']:.1f} minutes\n\n")
            
            if metrics1 and metrics2:
                f.write("-"*60 + "\n")
                f.write("--- Comparison ---\n")
                f.write("-"*60 + "\n")
                if metrics1['win_rate_tp2'] > metrics2['win_rate_tp2']:
                    f.write("MSS Entry is MORE profitable than Full Range Entry\n")
                else:
                    f.write("MSS Entry is LESS profitable than Full Range Entry\n")
                f.write(f"Difference in Win Rate to Tokyo_High: {metrics1['win_rate_tp2'] - metrics2['win_rate_tp2']:+.1f}%\n")
                f.write(f"Difference in Net Points: {metrics1['net_points'] - metrics2['net_points']:+.2f} points\n")
        
        print(f"\nResults saved to: {filepath}")


def main():
    """Main execution function"""
    backtest = ICT2022Model()
    trades1, trades2 = backtest.run_complete_backtest()
    
    print("\n" + "="*60)
    print("BACKTEST COMPLETE")
    print("="*60)
    print(f"Method 1 trades: {len(trades1)}")
    print(f"Method 2 trades: {len(trades2)}")
    print("\nCheck ICT_2022_RESULTS.txt for detailed results.")


if __name__ == "__main__":
    main()
