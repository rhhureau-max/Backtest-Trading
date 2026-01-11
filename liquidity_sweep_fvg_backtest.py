#!/usr/bin/env python3
"""
NQ Futures Liquidity Sweep + FVG Inversion Strategy Backtester
================================================================

Strategy: Liquidity Sweep followed by First FVG Inversion with One-Bullet Rule
Author: Senior Quantitative Trader
Date: 2026-01-11

This script implements an advanced backtesting engine that combines:
1. Liquidity Sweep detection (price sweeping swing highs/lows)
2. Fair Value Gap (FVG) formation after the sweep
3. FVG Inversion confirmation

The strategy requires ALL THREE steps to occur in sequence before entering a trade.

Key Features:
- Swing point detection using fractal logic
- Liquidity sweep validation (buy-side and sell-side)
- FVG detection following sweeps
- Strict session-based trading (London & New York killzones)
- One trade per session rule ("One Bullet")
- 1:1 Risk-to-Reward ratio
- Comprehensive performance reporting with sweep analytics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import time
from collections import deque
import os


class LiquiditySweepFVGBacktest:
    """
    Advanced backtesting engine for Liquidity Sweep + FVG Inversion strategy.
    
    This strategy requires a 3-step process:
    1. Identify swing points (liquidity pools)
    2. Detect liquidity sweeps
    3. Confirm with FVG formation and inversion
    """
    
    # Configuration constants
    MIN_RISK_THRESHOLD = 0.1  # Minimum risk for trade validity
    MAX_ACTIVE_FVGS = 100  # Maximum number of active FVGs to track
    MAX_SWING_CHECKS = 10  # Maximum recent swing points to check per bar
    SWEEP_VALIDITY_MULTIPLIER = 2  # Multiplier for sweep validity window
    
    def __init__(self, 
                 data_dir='/home/runner/work/Backtest-Trading/Backtest-Trading',
                 swing_lookback=5,
                 max_swing_history=50,
                 sweep_lookback=20):
        """
        Initialize the backtester.
        
        Args:
            data_dir (str): Directory containing the CSV files
            swing_lookback (int): Number of bars before/after to confirm swing point
            max_swing_history (int): Maximum number of swing points to track
            sweep_lookback (int): Maximum bars to look back for recent sweeps
        """
        self.data_dir = data_dir
        self.df = None
        self.trades = []
        
        # Swing point detection parameters
        self.swing_lookback = swing_lookback
        self.max_swing_history = max_swing_history
        self.sweep_lookback = sweep_lookback
        
        # Session definitions (Chicago Time)
        self.london_start = time(1, 0)   # 01:00
        self.london_end = time(4, 0)     # 04:00
        self.ny_start = time(8, 30)      # 08:30
        self.ny_end = time(11, 0)        # 11:00
        
    def load_data(self):
        """
        Load and combine all yearly 5-minute CSV files.
        
        Returns:
            pd.DataFrame: Combined and processed dataframe
        """
        print("Loading data from CSV files...")
        
        # Find all 5m CSV files for years 2018-2024
        csv_files = []
        for year in range(2018, 2025):  # 2018 to 2024
            file_pattern = os.path.join(self.data_dir, f"{year} 5m.csv")
            if os.path.exists(file_pattern):
                csv_files.append(file_pattern)
        
        if not csv_files:
            raise FileNotFoundError("No 5-minute CSV files found!")
        
        print(f"Found {len(csv_files)} files: {[os.path.basename(f) for f in csv_files]}")
        
        # Load and combine all CSV files
        dfs = []
        for file in csv_files:
            print(f"  Loading {os.path.basename(file)}...")
            df = pd.read_csv(file, sep=';', skiprows=1, 
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            dfs.append(df)
        
        # Combine all dataframes
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Total rows loaded: {len(combined_df)}")
        
        # Parse datetime
        combined_df['DateTime'] = pd.to_datetime(
            combined_df['Date'] + ' ' + combined_df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Sort by datetime
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        
        # Extract time for session filtering
        combined_df['TimeOnly'] = combined_df['DateTime'].dt.time
        combined_df['DateOnly'] = combined_df['DateTime'].dt.date
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        
        # Drop any rows with NaN values
        combined_df = combined_df.dropna().reset_index(drop=True)
        
        print(f"Data loaded successfully. Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
        
        self.df = combined_df
        return combined_df
    
    def identify_swing_points(self):
        """
        Identify swing highs and swing lows using fractal logic.
        
        A Swing High is a bar whose high is higher than N bars before AND after it.
        A Swing Low is a bar whose low is lower than N bars before AND after it.
        
        This method adds columns to the dataframe marking swing points.
        """
        print(f"\nIdentifying swing points (lookback={self.swing_lookback})...")
        
        df = self.df.copy()
        n = self.swing_lookback
        
        # Initialize swing point columns
        df['Swing_High'] = False
        df['Swing_High_Price'] = np.nan
        df['Swing_Low'] = False
        df['Swing_Low_Price'] = np.nan
        
        # Identify swing points (need at least n bars before and after)
        for i in range(n, len(df) - n):
            current_high = df.loc[i, 'High']
            current_low = df.loc[i, 'Low']
            
            # Check if this is a Swing High
            # High must be higher than all highs in the lookback window before and after
            is_swing_high = True
            for j in range(1, n + 1):
                if df.loc[i - j, 'High'] >= current_high or df.loc[i + j, 'High'] >= current_high:
                    is_swing_high = False
                    break
            
            if is_swing_high:
                df.loc[i, 'Swing_High'] = True
                df.loc[i, 'Swing_High_Price'] = current_high
            
            # Check if this is a Swing Low
            # Low must be lower than all lows in the lookback window before and after
            is_swing_low = True
            for j in range(1, n + 1):
                if df.loc[i - j, 'Low'] <= current_low or df.loc[i + j, 'Low'] <= current_low:
                    is_swing_low = False
                    break
            
            if is_swing_low:
                df.loc[i, 'Swing_Low'] = True
                df.loc[i, 'Swing_Low_Price'] = current_low
        
        swing_highs = df['Swing_High'].sum()
        swing_lows = df['Swing_Low'].sum()
        print(f"  Found {swing_highs} Swing Highs")
        print(f"  Found {swing_lows} Swing Lows")
        
        self.df = df
        return df
    
    def detect_fvgs(self):
        """
        Detect Fair Value Gaps (FVGs) in the data.
        
        A Bearish FVG occurs when: Low[i-2] > High[i]
        A Bullish FVG occurs when: High[i-2] < Low[i]
        """
        print("\nDetecting Fair Value Gaps...")
        
        df = self.df.copy()
        
        # Initialize FVG columns
        df['Bearish_FVG'] = False
        df['Bearish_FVG_Top'] = np.nan
        df['Bearish_FVG_Bottom'] = np.nan
        
        df['Bullish_FVG'] = False
        df['Bullish_FVG_Top'] = np.nan
        df['Bullish_FVG_Bottom'] = np.nan
        
        # Detect FVGs (starting from index 2)
        for i in range(2, len(df)):
            # Bearish FVG: Low[i-2] > High[i]
            if df.loc[i-2, 'Low'] > df.loc[i, 'High']:
                df.loc[i, 'Bearish_FVG'] = True
                df.loc[i, 'Bearish_FVG_Top'] = df.loc[i-2, 'Low']
                df.loc[i, 'Bearish_FVG_Bottom'] = df.loc[i, 'High']
            
            # Bullish FVG: High[i-2] < Low[i]
            if df.loc[i-2, 'High'] < df.loc[i, 'Low']:
                df.loc[i, 'Bullish_FVG'] = True
                df.loc[i, 'Bullish_FVG_Bottom'] = df.loc[i-2, 'High']
                df.loc[i, 'Bullish_FVG_Top'] = df.loc[i, 'Low']
        
        bearish_count = df['Bearish_FVG'].sum()
        bullish_count = df['Bullish_FVG'].sum()
        print(f"  Found {bearish_count} Bearish FVGs")
        print(f"  Found {bullish_count} Bullish FVGs")
        
        self.df = df
        return df
    
    def get_session(self, time_val):
        """
        Determine which trading session a time belongs to.
        
        Args:
            time_val (time): Time to check
            
        Returns:
            str: 'London', 'New York', or None
        """
        if self.london_start <= time_val < self.london_end:
            return 'London'
        elif self.ny_start <= time_val < self.ny_end:
            return 'New York'
        return None
    
    def run_backtest(self):
        """
        Execute the advanced backtesting logic with liquidity sweep detection.
        
        This implements the 3-step process:
        1. Track swing points (liquidity pools)
        2. Detect liquidity sweeps
        3. Confirm with FVG formation and inversion
        
        Implements the "One Bullet" rule: only the first valid signal per session is traded.
        """
        print("\n" + "="*70)
        print("Running Backtest with Liquidity Sweep + FVG Inversion Strategy...")
        print("="*70)
        
        df = self.df
        trades = []
        
        # Track recent swing points (FIFO with max history)
        # Format: (index, price, type) where type is 'high' or 'low'
        swing_highs = deque(maxlen=self.max_swing_history)
        swing_lows = deque(maxlen=self.max_swing_history)
        
        # Track recent sweeps
        # Format: (index, swept_price, type) where type is 'buy_side' or 'sell_side'
        recent_sweeps = deque(maxlen=self.sweep_lookback)
        
        # Track active FVGs that follow a sweep
        # Format: (fvg_index, top, bottom, sweep_index, sweep_type)
        # Use limited size deques to prevent memory/performance issues
        active_bearish_fvgs = deque(maxlen=self.MAX_ACTIVE_FVGS)  # For LONG setups (after sell-side sweep)
        active_bullish_fvgs = deque(maxlen=self.MAX_ACTIVE_FVGS)  # For SHORT setups (after buy-side sweep)
        
        # Track session state
        current_date = None
        london_traded = False
        ny_traded = False
        
        # Track active trade
        active_trade = None
        
        # Statistics tracking
        total_sweeps = 0
        buy_side_sweeps = 0
        sell_side_sweeps = 0
        
        print("\n🔍 Processing bars and detecting patterns...")
        
        # Progress tracking
        total_bars = len(df)
        progress_interval = total_bars // 10  # Report progress every 10%
        
        for i in range(len(df)):
            # Progress reporting
            if i > 0 and i % progress_interval == 0:
                progress_pct = (i / total_bars) * 100
                print(f"  Progress: {progress_pct:.1f}% ({i}/{total_bars} bars)")
            
            row = df.iloc[i]
            current_time = row['TimeOnly']
            current_session = self.get_session(current_time)
            
            # Reset session flags on new day
            if row['DateOnly'] != current_date:
                current_date = row['DateOnly']
                london_traded = False
                ny_traded = False
            
            # ===================================================================
            # STEP 1: Update swing point lists
            # ===================================================================
            if row['Swing_High']:
                swing_highs.append((i, row['Swing_High_Price']))
            
            if row['Swing_Low']:
                swing_lows.append((i, row['Swing_Low_Price']))
            
            # ===================================================================
            # STEP 2: Detect liquidity sweeps
            # ===================================================================
            # Buy-side sweep: Price goes ABOVE a previous Swing High
            # Only check the last few swing highs for efficiency
            buy_sweep_detected = False
            last_n_swing_highs = list(swing_highs)[-self.MAX_SWING_CHECKS:] if len(swing_highs) >= self.MAX_SWING_CHECKS else list(swing_highs)
            for swing_idx, swing_price in reversed(last_n_swing_highs):
                if swing_idx < i and row['High'] > swing_price:
                    # Sweep detected!
                    recent_sweeps.append((i, swing_price, 'buy_side'))
                    total_sweeps += 1
                    buy_side_sweeps += 1
                    buy_sweep_detected = True
                    break  # Only count once per bar
            
            # Sell-side sweep: Price goes BELOW a previous Swing Low
            # Only check the last few swing lows for efficiency
            sell_sweep_detected = False
            if not buy_sweep_detected:  # Only check one type per bar for clarity
                last_n_swing_lows = list(swing_lows)[-self.MAX_SWING_CHECKS:] if len(swing_lows) >= self.MAX_SWING_CHECKS else list(swing_lows)
                for swing_idx, swing_price in reversed(last_n_swing_lows):
                    if swing_idx < i and row['Low'] < swing_price:
                        # Sweep detected!
                        recent_sweeps.append((i, swing_price, 'sell_side'))
                        total_sweeps += 1
                        sell_side_sweeps += 1
                        sell_sweep_detected = True
                        break  # Only count once per bar
            
            # ===================================================================
            # STEP 3: Detect FVGs that follow recent sweeps
            # ===================================================================
            # Clean up old sweeps from the recent_sweeps deque
            # Filter to only keep sweeps within the lookback window
            recent_sweeps_list = list(recent_sweeps)
            recent_sweeps = deque(
                [(sweep_idx, swept_price, sweep_type) 
                 for sweep_idx, swept_price, sweep_type in recent_sweeps_list
                 if i - sweep_idx <= self.sweep_lookback],
                maxlen=self.sweep_lookback
            )
            
            # Check if there was a recent sell-side sweep (for LONG setup)
            recent_sell_side_sweeps = [
                (sweep_idx, swept_price) 
                for sweep_idx, swept_price, sweep_type in recent_sweeps
                if sweep_type == 'sell_side'
            ]
            
            # Check if there was a recent buy-side sweep (for SHORT setup)
            recent_buy_side_sweeps = [
                (sweep_idx, swept_price) 
                for sweep_idx, swept_price, sweep_type in recent_sweeps
                if sweep_type == 'buy_side'
            ]
            
            # Add Bearish FVG to active list ONLY if preceded by sell-side sweep
            if row['Bearish_FVG'] and recent_sell_side_sweeps:
                # Use the most recent sell-side sweep
                sweep_idx, swept_price = recent_sell_side_sweeps[-1]
                active_bearish_fvgs.append((
                    i, 
                    row['Bearish_FVG_Top'], 
                    row['Bearish_FVG_Bottom'],
                    sweep_idx,
                    'sell_side'
                ))
            
            # Add Bullish FVG to active list ONLY if preceded by buy-side sweep
            if row['Bullish_FVG'] and recent_buy_side_sweeps:
                # Use the most recent buy-side sweep
                sweep_idx, swept_price = recent_buy_side_sweeps[-1]
                active_bullish_fvgs.append((
                    i, 
                    row['Bullish_FVG_Top'], 
                    row['Bullish_FVG_Bottom'],
                    sweep_idx,
                    'buy_side'
                ))
            
            # ===================================================================
            # STEP 4: Check if active trade hits SL or TP
            # ===================================================================
            if active_trade is not None:
                trade = active_trade
                
                if trade['Direction'] == 'LONG':
                    # Check Stop Loss
                    if row['Low'] <= trade['Stop_Loss']:
                        trade['Exit_DateTime'] = row['DateTime']
                        trade['Exit_Price'] = trade['Stop_Loss']
                        trade['Exit_Reason'] = 'Stop Loss'
                        trade['PnL'] = trade['Exit_Price'] - trade['Entry_Price']
                        trade['Status'] = 'Loss'
                        trades.append(trade)
                        active_trade = None
                        continue
                    
                    # Check Take Profit
                    if row['High'] >= trade['Take_Profit']:
                        trade['Exit_DateTime'] = row['DateTime']
                        trade['Exit_Price'] = trade['Take_Profit']
                        trade['Exit_Reason'] = 'Take Profit'
                        trade['PnL'] = trade['Exit_Price'] - trade['Entry_Price']
                        trade['Status'] = 'Win'
                        trades.append(trade)
                        active_trade = None
                        continue
                
                else:  # SHORT
                    # Check Stop Loss
                    if row['High'] >= trade['Stop_Loss']:
                        trade['Exit_DateTime'] = row['DateTime']
                        trade['Exit_Price'] = trade['Stop_Loss']
                        trade['Exit_Reason'] = 'Stop Loss'
                        trade['PnL'] = trade['Entry_Price'] - trade['Exit_Price']
                        trade['Status'] = 'Loss'
                        trades.append(trade)
                        active_trade = None
                        continue
                    
                    # Check Take Profit
                    if row['Low'] <= trade['Take_Profit']:
                        trade['Exit_DateTime'] = row['DateTime']
                        trade['Exit_Price'] = trade['Take_Profit']
                        trade['Exit_Reason'] = 'Take Profit'
                        trade['PnL'] = trade['Entry_Price'] - trade['Exit_Price']
                        trade['Status'] = 'Win'
                        trades.append(trade)
                        active_trade = None
                        continue
            
            # ===================================================================
            # STEP 5: Look for new entry signals (FVG inversions)
            # ===================================================================
            # Only look for new entries if:
            # 1. We're in a valid session
            # 2. No active trade
            # 3. Haven't traded this session yet
            if current_session is None or active_trade is not None:
                continue
            
            if current_session == 'London' and london_traded:
                continue
            
            if current_session == 'New York' and ny_traded:
                continue
            
            # Check for LONG signals (Bearish FVG inversion after sell-side sweep)
            for fvg_idx, fvg_top, fvg_bottom, sweep_idx, sweep_type in list(active_bearish_fvgs):
                # Signal: Close ABOVE the top of Bearish FVG
                # Additional validation: Ensure the sweep is still reasonably recent
                bars_since_sweep = i - sweep_idx
                if row['Close'] > fvg_top and bars_since_sweep <= self.sweep_lookback * self.SWEEP_VALIDITY_MULTIPLIER:
                    # LONG ENTRY SIGNAL!
                    entry_price = row['Close']
                    stop_loss = row['Low']
                    risk = entry_price - stop_loss
                    
                    # Skip if risk is too small (avoid tiny trades)
                    if risk < self.MIN_RISK_THRESHOLD:
                        continue
                    
                    take_profit = entry_price + risk  # 1:1 RRR
                    
                    trade = {
                        'Entry_DateTime': row['DateTime'],
                        'Entry_Price': entry_price,
                        'Direction': 'LONG',
                        'Session': current_session,
                        'Stop_Loss': stop_loss,
                        'Take_Profit': take_profit,
                        'Risk': risk,
                        'FVG_Index': fvg_idx,
                        'Sweep_Index': sweep_idx,
                        'Sweep_Type': sweep_type,
                        'Signal_Candle_Index': i,
                        'Bars_Since_Sweep': bars_since_sweep
                    }
                    
                    active_trade = trade
                    
                    # Mark session as traded
                    if current_session == 'London':
                        london_traded = True
                    else:
                        ny_traded = True
                    
                    # Remove this FVG from active list (inverted)
                    active_bearish_fvgs.remove((fvg_idx, fvg_top, fvg_bottom, sweep_idx, sweep_type))
                    
                    break  # Take only first signal
            
            # If we already took a trade, skip SHORT check
            if active_trade is not None:
                continue
            
            # Check for SHORT signals (Bullish FVG inversion after buy-side sweep)
            for fvg_idx, fvg_top, fvg_bottom, sweep_idx, sweep_type in list(active_bullish_fvgs):
                # Signal: Close BELOW the bottom of Bullish FVG
                # Additional validation: Ensure the sweep is still reasonably recent
                bars_since_sweep = i - sweep_idx
                if row['Close'] < fvg_bottom and bars_since_sweep <= self.sweep_lookback * self.SWEEP_VALIDITY_MULTIPLIER:
                    # SHORT ENTRY SIGNAL!
                    entry_price = row['Close']
                    stop_loss = row['High']
                    risk = stop_loss - entry_price
                    
                    # Skip if risk is too small (avoid tiny trades)
                    if risk < self.MIN_RISK_THRESHOLD:
                        continue
                    
                    take_profit = entry_price - risk  # 1:1 RRR
                    
                    trade = {
                        'Entry_DateTime': row['DateTime'],
                        'Entry_Price': entry_price,
                        'Direction': 'SHORT',
                        'Session': current_session,
                        'Stop_Loss': stop_loss,
                        'Take_Profit': take_profit,
                        'Risk': risk,
                        'FVG_Index': fvg_idx,
                        'Sweep_Index': sweep_idx,
                        'Sweep_Type': sweep_type,
                        'Signal_Candle_Index': i,
                        'Bars_Since_Sweep': bars_since_sweep
                    }
                    
                    active_trade = trade
                    
                    # Mark session as traded
                    if current_session == 'London':
                        london_traded = True
                    else:
                        ny_traded = True
                    
                    # Remove this FVG from active list (inverted)
                    active_bullish_fvgs.remove((fvg_idx, fvg_top, fvg_bottom, sweep_idx, sweep_type))
                    
                    break  # Take only first signal
        
        # Close any remaining open trade at the end
        if active_trade is not None:
            last_row = df.iloc[-1]
            trade = active_trade
            trade['Exit_DateTime'] = last_row['DateTime']
            trade['Exit_Price'] = last_row['Close']
            trade['Exit_Reason'] = 'End of Data'
            
            if trade['Direction'] == 'LONG':
                trade['PnL'] = trade['Exit_Price'] - trade['Entry_Price']
            else:
                trade['PnL'] = trade['Entry_Price'] - trade['Exit_Price']
            
            trade['Status'] = 'Win' if trade['PnL'] > 0 else 'Loss'
            trades.append(trade)
        
        self.trades = trades
        
        print(f"\n📊 Sweep Detection Statistics:")
        print(f"  Total Sweeps Detected: {total_sweeps}")
        print(f"  Buy-side Sweeps: {buy_side_sweeps}")
        print(f"  Sell-side Sweeps: {sell_side_sweeps}")
        print(f"\n✅ Backtest complete. Total trades executed: {len(trades)}")
        
        return trades
    
    def calculate_performance(self):
        """
        Calculate performance metrics for the strategy.
        
        Returns:
            dict: Performance statistics overall and by session
        """
        print("\n" + "="*70)
        print("PERFORMANCE SUMMARY - LIQUIDITY SWEEP + FVG INVERSION STRATEGY")
        print("="*70)
        
        if not self.trades:
            print("No trades were executed.")
            return {}
        
        trades_df = pd.DataFrame(self.trades)
        
        # Overall statistics
        total_trades = len(trades_df)
        wins = len(trades_df[trades_df['Status'] == 'Win'])
        losses = len(trades_df[trades_df['Status'] == 'Loss'])
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = trades_df['PnL'].sum()
        winning_pnl = trades_df[trades_df['Status'] == 'Win']['PnL'].sum()
        losing_pnl = abs(trades_df[trades_df['Status'] == 'Loss']['PnL'].sum())
        
        profit_factor = (winning_pnl / losing_pnl) if losing_pnl > 0 else float('inf')
        
        # Calculate average time from sweep to entry
        avg_bars_since_sweep = trades_df['Bars_Since_Sweep'].mean()
        
        print("\n📊 OVERALL PERFORMANCE")
        print("-" * 70)
        print(f"Total Trades:              {total_trades}")
        print(f"Winning Trades:            {wins}")
        print(f"Losing Trades:             {losses}")
        print(f"Win Rate:                  {win_rate:.2f}%")
        print(f"Profit Factor:             {profit_factor:.2f}")
        print(f"Net Profit:                {total_pnl:.2f} points")
        print(f"Avg Win:                   {trades_df[trades_df['Status'] == 'Win']['PnL'].mean():.2f} points" if wins > 0 else "Avg Win:                   N/A")
        print(f"Avg Loss:                  {trades_df[trades_df['Status'] == 'Loss']['PnL'].mean():.2f} points" if losses > 0 else "Avg Loss:                  N/A")
        print(f"Avg Bars Since Sweep:      {avg_bars_since_sweep:.1f} bars")
        
        # Session-specific statistics
        print("\n📈 SESSION BREAKDOWN")
        print("-" * 70)
        
        session_stats = {}
        
        for session in ['London', 'New York']:
            session_trades = trades_df[trades_df['Session'] == session]
            
            if len(session_trades) == 0:
                print(f"\n{session} Session: No trades")
                continue
            
            s_total = len(session_trades)
            s_wins = len(session_trades[session_trades['Status'] == 'Win'])
            s_losses = len(session_trades[session_trades['Status'] == 'Loss'])
            s_win_rate = (s_wins / s_total * 100) if s_total > 0 else 0
            
            s_total_pnl = session_trades['PnL'].sum()
            s_winning_pnl = session_trades[session_trades['Status'] == 'Win']['PnL'].sum()
            s_losing_pnl = abs(session_trades[session_trades['Status'] == 'Loss']['PnL'].sum())
            
            s_profit_factor = (s_winning_pnl / s_losing_pnl) if s_losing_pnl > 0 else float('inf')
            
            print(f"\n{session} Session:")
            print(f"  Total Trades:   {s_total}")
            print(f"  Wins / Losses:  {s_wins} / {s_losses}")
            print(f"  Win Rate:       {s_win_rate:.2f}%")
            print(f"  Profit Factor:  {s_profit_factor:.2f}")
            print(f"  Net Profit:     {s_total_pnl:.2f} points")
            
            session_stats[session] = {
                'Total_Trades': s_total,
                'Wins': s_wins,
                'Losses': s_losses,
                'Win_Rate': s_win_rate,
                'Profit_Factor': s_profit_factor,
                'Net_Profit': s_total_pnl
            }
        
        # Direction breakdown
        print("\n📉 DIRECTION BREAKDOWN")
        print("-" * 70)
        
        for direction in ['LONG', 'SHORT']:
            dir_trades = trades_df[trades_df['Direction'] == direction]
            
            if len(dir_trades) == 0:
                print(f"\n{direction}: No trades")
                continue
            
            d_total = len(dir_trades)
            d_wins = len(dir_trades[dir_trades['Status'] == 'Win'])
            d_win_rate = (d_wins / d_total * 100) if d_total > 0 else 0
            d_total_pnl = dir_trades['PnL'].sum()
            
            print(f"\n{direction}:")
            print(f"  Total Trades:   {d_total}")
            print(f"  Win Rate:       {d_win_rate:.2f}%")
            print(f"  Net Profit:     {d_total_pnl:.2f} points")
        
        # Sweep type breakdown
        print("\n🌊 SWEEP TYPE BREAKDOWN")
        print("-" * 70)
        
        for sweep_type in ['sell_side', 'buy_side']:
            sweep_trades = trades_df[trades_df['Sweep_Type'] == sweep_type]
            
            if len(sweep_trades) == 0:
                continue
            
            st_total = len(sweep_trades)
            st_wins = len(sweep_trades[sweep_trades['Status'] == 'Win'])
            st_win_rate = (st_wins / st_total * 100) if st_total > 0 else 0
            st_total_pnl = sweep_trades['PnL'].sum()
            
            sweep_name = "Sell-side Sweep (LONG setups)" if sweep_type == 'sell_side' else "Buy-side Sweep (SHORT setups)"
            print(f"\n{sweep_name}:")
            print(f"  Total Trades:   {st_total}")
            print(f"  Win Rate:       {st_win_rate:.2f}%")
            print(f"  Net Profit:     {st_total_pnl:.2f} points")
        
        return {
            'overall': {
                'Total_Trades': total_trades,
                'Wins': wins,
                'Losses': losses,
                'Win_Rate': win_rate,
                'Profit_Factor': profit_factor,
                'Net_Profit': total_pnl,
                'Avg_Bars_Since_Sweep': avg_bars_since_sweep
            },
            'sessions': session_stats
        }
    
    def plot_equity_curve(self, output_file='liquidity_sweep_equity_curve.png'):
        """
        Generate and save equity curve visualization.
        
        Args:
            output_file (str): Output filename for the plot
        """
        print(f"\n📊 Generating equity curve: {output_file}")
        
        if not self.trades:
            print("No trades to plot.")
            return
        
        trades_df = pd.DataFrame(self.trades)
        trades_df['Cumulative_PnL'] = trades_df['PnL'].cumsum()
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Plot 1: Cumulative Equity Curve
        ax1.plot(range(len(trades_df)), trades_df['Cumulative_PnL'], 
                linewidth=2, color='#2E86AB', label='Cumulative P&L')
        ax1.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax1.fill_between(range(len(trades_df)), trades_df['Cumulative_PnL'], 0, 
                         where=(trades_df['Cumulative_PnL'] >= 0), 
                         alpha=0.3, color='green', label='Profit')
        ax1.fill_between(range(len(trades_df)), trades_df['Cumulative_PnL'], 0, 
                         where=(trades_df['Cumulative_PnL'] < 0), 
                         alpha=0.3, color='red', label='Loss')
        ax1.set_title('Liquidity Sweep + FVG Inversion Strategy - Cumulative Equity Curve', 
                     fontsize=16, fontweight='bold')
        ax1.set_xlabel('Trade Number', fontsize=12)
        ax1.set_ylabel('Cumulative P&L (Points)', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Individual Trade Results
        colors = ['green' if status == 'Win' else 'red' for status in trades_df['Status']]
        ax2.bar(range(len(trades_df)), trades_df['PnL'], color=colors, alpha=0.6)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax2.set_title('Individual Trade Results', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Trade Number', fontsize=12)
        ax2.set_ylabel('P&L (Points)', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        # Save to file
        output_path = os.path.join(self.data_dir, output_file)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ Equity curve saved to: {output_path}")
        
        plt.close()
    
    def export_trades(self, output_file='liquidity_sweep_trades_log.csv'):
        """
        Export all trades to a CSV file for further analysis.
        
        Args:
            output_file (str): Output filename for the trades log
        """
        if not self.trades:
            print("No trades to export.")
            return
        
        trades_df = pd.DataFrame(self.trades)
        output_path = os.path.join(self.data_dir, output_file)
        trades_df.to_csv(output_path, index=False)
        print(f"✅ Trades exported to: {output_path}")


def main():
    """
    Main execution function.
    """
    print("="*70)
    print("NQ FUTURES - LIQUIDITY SWEEP + FVG INVERSION STRATEGY BACKTESTER")
    print("="*70)
    print("Strategy: Liquidity Sweep → FVG Formation → FVG Inversion")
    print("Sessions: London (01:00-04:00) & New York (08:30-11:00)")
    print("Risk Management: 1:1 RRR | One Bullet Per Session")
    print("="*70)
    
    # Initialize backtester with configurable parameters
    bt = LiquiditySweepFVGBacktest(
        swing_lookback=5,        # Bars before/after for swing point confirmation
        max_swing_history=50,    # Maximum swing points to track
        sweep_lookback=20        # Maximum bars to look back for recent sweeps
    )
    
    # Execute backtest pipeline
    try:
        # Step 1: Load data
        bt.load_data()
        
        # Step 2: Identify swing points (liquidity pools)
        bt.identify_swing_points()
        
        # Step 3: Detect FVGs
        bt.detect_fvgs()
        
        # Step 4: Run backtest with sweep detection
        bt.run_backtest()
        
        # Step 5: Calculate and display performance
        bt.calculate_performance()
        
        # Step 6: Generate equity curve
        bt.plot_equity_curve('liquidity_sweep_equity_curve.png')
        
        # Step 7: Export trades
        bt.export_trades('liquidity_sweep_trades_log.csv')
        
        print("\n" + "="*70)
        print("✅ BACKTEST COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nOutput files:")
        print("  - liquidity_sweep_equity_curve.png: Cumulative P&L visualization")
        print("  - liquidity_sweep_trades_log.csv: Detailed trade log with sweep info")
        print("\nKey Features Implemented:")
        print("  ✓ Swing point detection using fractal logic")
        print("  ✓ Buy-side and sell-side liquidity sweep detection")
        print("  ✓ FVG formation validation after sweeps")
        print("  ✓ FVG inversion entry signals")
        print("  ✓ One-bullet rule per session")
        print("  ✓ 1:1 Risk-to-Reward ratio")
        print("  ✓ Comprehensive performance analytics")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
