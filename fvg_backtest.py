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
        
        # Calculate ATR for alternative strategies
        self.df['TR'] = np.maximum(
            self.df['High'] - self.df['Low'],
            np.maximum(
                abs(self.df['High'] - self.df['Close'].shift(1)),
                abs(self.df['Low'] - self.df['Close'].shift(1))
            )
        )
        self.df['ATR'] = self.df['TR'].rolling(window=14).mean()
        
        print(f"Total candles loaded: {len(self.df)}")
        print(f"Date range: {self.df['DateTime'].min()} to {self.df['DateTime'].max()}")
        
    def detect_fvg(self, min_gap_size=0, max_gap_size=None):
        """
        Detect Fair Value Gaps (FVG)
        Only validate FVGs created by a candle with opening hour between 02:00 and 06:00 (inclusive)
        
        Bearish FVG: Low[i-1] > High[i+1] → resistance zone [High[i+1], Low[i-1]]
        Bullish FVG: High[i-1] < Low[i+1] → support zone [High[i-1], Low[i+1]]
        
        Args:
            min_gap_size: Minimum size of the gap in points to be considered valid (default: 0)
            max_gap_size: Maximum size of the gap in points (None = no max limit)
        """
        if max_gap_size is None:
            print(f"\nDetecting FVGs (min gap size: {min_gap_size} pts)...")
        else:
            print(f"\nDetecting FVGs (gap size range: {min_gap_size}-{max_gap_size} pts)...")
        
        fvg_list = []
        
        # Need at least 3 candles for FVG detection
        for i in range(1, len(self.df) - 1):
            # Check if candle i (middle candle) opens between 02:00 and 06:00
            if not (2 <= self.df.loc[i, 'Hour'] <= 6):
                continue
            
            # Bearish FVG: Low[i-1] > High[i+1]
            if self.df.loc[i-1, 'Low'] > self.df.loc[i+1, 'High']:
                gap_size = self.df.loc[i-1, 'Low'] - self.df.loc[i+1, 'High']
                if gap_size >= min_gap_size and (max_gap_size is None or gap_size < max_gap_size):
                    fvg_list.append({
                        'index': i,
                        'type': 'bearish',
                        'top': self.df.loc[i-1, 'Low'],
                        'bottom': self.df.loc[i+1, 'High'],
                        'gap_size': gap_size,
                        'datetime': self.df.loc[i, 'DateTime']
                    })
            
            # Bullish FVG: High[i-1] < Low[i+1]
            elif self.df.loc[i-1, 'High'] < self.df.loc[i+1, 'Low']:
                gap_size = self.df.loc[i+1, 'Low'] - self.df.loc[i-1, 'High']
                if gap_size >= min_gap_size and (max_gap_size is None or gap_size < max_gap_size):
                    fvg_list.append({
                        'index': i,
                        'type': 'bullish',
                        'top': self.df.loc[i+1, 'Low'],
                        'bottom': self.df.loc[i-1, 'High'],
                        'gap_size': gap_size,
                        'datetime': self.df.loc[i, 'DateTime']
                    })
        
        print(f"Total FVGs detected: {len(fvg_list)}")
        print(f"  Bearish FVGs: {sum(1 for fvg in fvg_list if fvg['type'] == 'bearish')}")
        print(f"  Bullish FVGs: {sum(1 for fvg in fvg_list if fvg['type'] == 'bullish')}")
        if fvg_list:
            avg_gap = sum(fvg['gap_size'] for fvg in fvg_list) / len(fvg_list)
            print(f"  Average gap size: {avg_gap:.2f} pts")
        
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
    
    def backtest_atr_strategy(self, fvg_list, strategy_name, atr_multiplier, tp_multiplier):
        """
        Backtest with ATR-based stop-loss
        
        Args:
            fvg_list: List of detected FVGs
            strategy_name: Name of the strategy
            atr_multiplier: Multiplier for ATR to set SL distance
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
            if not active_trade and not pd.isna(current_candle['ATR']):
                for fvg in fvg_list:
                    # Only consider FVGs that occurred before current candle
                    if fvg['index'] >= i:
                        continue
                    
                    # LONG Entry: Close strictly above top of Bearish FVG
                    if fvg['type'] == 'bearish' and current_candle['Close'] > fvg['top']:
                        # Calculate SL using ATR
                        atr_value = current_candle['ATR']
                        sl = current_candle['Close'] - (atr_multiplier * atr_value)
                        
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
                            'atr': atr_value,
                            'fvg_type': fvg['type'],
                            'fvg_top': fvg['top'],
                            'fvg_bottom': fvg['bottom']
                        }
                        break  # One trade at a time
                    
                    # SHORT Entry: Close strictly below bottom of Bullish FVG
                    elif fvg['type'] == 'bullish' and current_candle['Close'] < fvg['bottom']:
                        # Calculate SL using ATR
                        atr_value = current_candle['ATR']
                        sl = current_candle['Close'] + (atr_multiplier * atr_value)
                        
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
                            'atr': atr_value,
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
    
    def backtest_fvg_based_strategy(self, fvg_list, strategy_name, buffer_points, tp_multiplier):
        """
        Backtest with FVG-based stop-loss (beyond the FVG edge)
        
        Args:
            fvg_list: List of detected FVGs
            strategy_name: Name of the strategy
            buffer_points: Points beyond FVG edge for SL
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
                        # Calculate SL below FVG bottom with buffer
                        sl = fvg['bottom'] - buffer_points
                        
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
                        # Calculate SL above FVG top with buffer
                        sl = fvg['top'] + buffer_points
                        
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
    
    def run_strategy_a_alternatives(self):
        """Run Alternative Strategy A variants (ATR-based and FVG-based)"""
        # Load data
        self.load_data()
        
        # Detect FVGs
        fvg_list = self.detect_fvg()
        
        if not fvg_list:
            print("\nNo FVGs detected. Cannot proceed with backtesting.")
            return
        
        results = []
        
        print("\n" + "="*80)
        print("ALTERNATIVE STRATEGY A VARIANTS")
        print("="*80)
        
        # ATR-Based Strategies (Alternative 1)
        print("\n### ATR-BASED STRATEGIES ###")
        atr_configs = [
            {'multiplier': 1.5, 'tp': 1.5, 'name': 'A-ATR1: ATR(14)×1.5 SL, 1.5 RR TP'},
            {'multiplier': 2.0, 'tp': 2.0, 'name': 'A-ATR2: ATR(14)×2.0 SL, 2.0 RR TP'},
            {'multiplier': 2.5, 'tp': 2.5, 'name': 'A-ATR3: ATR(14)×2.5 SL, 2.5 RR TP'},
            {'multiplier': 3.0, 'tp': 2.5, 'name': 'A-ATR4: ATR(14)×3.0 SL, 2.5 RR TP'},
        ]
        
        for config in atr_configs:
            result = self.backtest_atr_strategy(
                fvg_list,
                config['name'],
                atr_multiplier=config['multiplier'],
                tp_multiplier=config['tp']
            )
            if result:
                results.append(result)
        
        # FVG-Based Strategies (Alternative 4)
        print("\n### FVG-BASED STRATEGIES ###")
        fvg_configs = [
            {'buffer': 5, 'tp': 1.5, 'name': 'A-FVG1: FVG edge + 5pts SL, 1.5 RR TP'},
            {'buffer': 10, 'tp': 2.0, 'name': 'A-FVG2: FVG edge + 10pts SL, 2.0 RR TP'},
            {'buffer': 15, 'tp': 2.5, 'name': 'A-FVG3: FVG edge + 15pts SL, 2.5 RR TP'},
            {'buffer': 20, 'tp': 3.0, 'name': 'A-FVG4: FVG edge + 20pts SL, 3.0 RR TP'},
        ]
        
        for config in fvg_configs:
            result = self.backtest_fvg_based_strategy(
                fvg_list,
                config['name'],
                buffer_points=config['buffer'],
                tp_multiplier=config['tp']
            )
            if result:
                results.append(result)
        
        # Display comparison table
        if results:
            print(f"\n{'='*100}")
            print("COMPARATIVE RESULTS - STRATEGY A ALTERNATIVES")
            print(f"{'='*100}\n")
            
            results_df = pd.DataFrame(results)
            print(results_df.to_string(index=False))
            print(f"\n{'='*100}")
            
            # Highlight best performers
            print("\n### BEST PERFORMERS ###")
            best_pnl = results_df.loc[results_df['Total PnL (pts)'].idxmax()]
            print(f"\nHighest Total PnL: {best_pnl['Strategy']}")
            print(f"  {best_pnl['Total PnL (pts)']} pts | {best_pnl['Trades']} trades | {best_pnl['Win Rate (%)']}% WR | PF: {best_pnl['Profit Factor']}")
            
            # Filter out 'Inf' values for profit factor comparison
            numeric_pf = results_df[results_df['Profit Factor'] != 'Inf']
            if not numeric_pf.empty:
                best_pf = numeric_pf.loc[numeric_pf['Profit Factor'].astype(float).idxmax()]
                print(f"\nBest Profit Factor: {best_pf['Strategy']}")
                print(f"  PF: {best_pf['Profit Factor']} | {best_pf['Total PnL (pts)']} pts | {best_pf['Trades']} trades | {best_pf['Win Rate (%)']}% WR")
            
            best_wr = results_df.loc[results_df['Win Rate (%)'].idxmax()]
            print(f"\nHighest Win Rate: {best_wr['Strategy']}")
            print(f"  {best_wr['Win Rate (%)']}% WR | {best_wr['Total PnL (pts)']} pts | {best_wr['Trades']} trades | PF: {best_wr['Profit Factor']}")
            
            print(f"\n{'='*100}")
        else:
            print("\nNo results to display.")
    
    def run_strategies_with_gap_filters(self):
        """Run all original strategies with different minimum gap size filters"""
        # Load data once
        self.load_data()
        
        # Define gap size filters to test
        gap_filters = [2, 5, 10, 20]
        
        # Define TP ratios to test
        tp_ratios = [1.0, 1.5, 2.0, 2.5]
        
        # Define strategy configurations
        strategies = [
            {'name': 'Strategy A (Scalping)', 'sl_lookback': 5},
            {'name': 'Strategy B (Intraday)', 'sl_lookback': 12},
            {'name': 'Strategy C (Swing)', 'sl_lookback': 20}
        ]
        
        all_results = {}
        
        for gap_size in gap_filters:
            print(f"\n{'='*80}")
            print(f"TESTING WITH MINIMUM GAP SIZE: {gap_size} POINTS")
            print(f"{'='*80}")
            
            # Detect FVGs with this gap filter
            fvg_list = self.detect_fvg(min_gap_size=gap_size)
            
            if not fvg_list:
                print(f"\nNo FVGs detected with min gap size {gap_size} pts. Skipping.")
                continue
            
            results = []
            
            # Backtest all combinations
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
                        result['Min Gap Size'] = gap_size
                        results.append(result)
            
            # Store results for this gap size
            all_results[gap_size] = results
            
            # Display comparison table for this gap size
            if results:
                print(f"\n{'='*100}")
                print(f"RESULTS FOR MINIMUM GAP SIZE: {gap_size} POINTS")
                print(f"{'='*100}\n")
                
                results_df = pd.DataFrame(results)
                print(results_df.to_string(index=False))
                print(f"\n{'='*100}")
        
        # Create comprehensive comparison across all gap sizes
        print(f"\n{'='*100}")
        print("COMPREHENSIVE COMPARISON - ALL GAP SIZES")
        print(f"{'='*100}\n")
        
        # Flatten all results
        all_results_flat = []
        for gap_size, results in all_results.items():
            all_results_flat.extend(results)
        
        if all_results_flat:
            all_df = pd.DataFrame(all_results_flat)
            
            # Group by strategy and gap size for analysis
            print("\nSummary by Strategy and Gap Size:")
            print("-" * 100)
            
            for strategy in strategies:
                print(f"\n### {strategy['name']} ###")
                strategy_data = all_df[all_df['Strategy'].str.contains(strategy['name'])]
                
                if not strategy_data.empty:
                    summary = strategy_data.groupby('Min Gap Size').agg({
                        'Trades': 'sum',
                        'Win Rate (%)': 'mean',
                        'Total PnL (pts)': 'sum',
                        'Max Drawdown (pts)': 'max'
                    }).round(2)
                    print(summary.to_string())
            
            print(f"\n{'='*100}")
        else:
            print("\nNo results to display.")
        
        return all_results
    
    def run_strategies_with_gap_ranges(self):
        """Run all original strategies with different gap size ranges"""
        # Load data once
        self.load_data()
        
        # Define gap size ranges to test
        gap_ranges = [
            (0.25, 2, "0.25-2 pts"),
            (2, 5, "2-5 pts"),
            (5, 10, "5-10 pts"),
            (10, 20, "10-20 pts")
        ]
        
        # Define TP ratios to test
        tp_ratios = [1.0, 1.5, 2.0, 2.5]
        
        # Define strategy configurations
        strategies = [
            {'name': 'Strategy A (Scalping)', 'sl_lookback': 5},
            {'name': 'Strategy B (Intraday)', 'sl_lookback': 12},
            {'name': 'Strategy C (Swing)', 'sl_lookback': 20}
        ]
        
        all_results = {}
        
        for min_gap, max_gap, gap_label in gap_ranges:
            print(f"\n{'='*80}")
            print(f"TESTING WITH GAP SIZE RANGE: {gap_label}")
            print(f"{'='*80}")
            
            # Detect FVGs with this gap range
            fvg_list = self.detect_fvg(min_gap_size=min_gap, max_gap_size=max_gap)
            
            if not fvg_list:
                print(f"\nNo FVGs detected in gap range {gap_label}. Skipping.")
                continue
            
            results = []
            
            # Backtest all combinations
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
                        result['Gap Range'] = gap_label
                        results.append(result)
            
            # Store results for this gap range
            all_results[gap_label] = results
            
            # Display comparison table for this gap range
            if results:
                print(f"\n{'='*100}")
                print(f"RESULTS FOR GAP SIZE RANGE: {gap_label}")
                print(f"{'='*100}\n")
                
                results_df = pd.DataFrame(results)
                # Select key columns for display
                display_cols = ['Strategy', 'Trades', 'Win Rate (%)', 'Profit Factor', 
                               'Total PnL (pts)', 'Max Drawdown (pts)', 'Wins', 'Losses']
                print(results_df[display_cols].to_string(index=False))
                print(f"\n{'='*100}")
        
        # Create comprehensive comparison across all gap ranges
        print(f"\n{'='*100}")
        print("COMPREHENSIVE COMPARISON - ALL GAP SIZE RANGES")
        print(f"{'='*100}\n")
        
        # Flatten all results
        all_results_flat = []
        for gap_label, results in all_results.items():
            all_results_flat.extend(results)
        
        if all_results_flat:
            all_df = pd.DataFrame(all_results_flat)
            
            # Display full results table
            print("\n=== COMPLETE RESULTS TABLE ===\n")
            display_cols = ['Strategy', 'Gap Range', 'Trades', 'Win Rate (%)', 'Profit Factor', 
                           'Total PnL (pts)', 'Max Drawdown (pts)']
            print(all_df[display_cols].to_string(index=False))
            
            # Group by strategy for summary
            print("\n\n=== SUMMARY BY STRATEGY ===")
            print("-" * 100)
            
            for strategy in strategies:
                print(f"\n### {strategy['name']} ###")
                strategy_data = all_df[all_df['Strategy'].str.contains(strategy['name'])]
                
                if not strategy_data.empty:
                    # Group by gap range and TP ratio
                    for tp in tp_ratios:
                        tp_data = strategy_data[strategy_data['Strategy'].str.contains(f"{tp} RR")]
                        if not tp_data.empty:
                            print(f"\n  {tp} RR:")
                            for _, row in tp_data.iterrows():
                                print(f"    {row['Gap Range']:12s}: {row['Trades']:6d} trades | "
                                      f"{row['Win Rate (%)']:5.2f}% WR | PF {row['Profit Factor']:4s} | "
                                      f"PnL {row['Total PnL (pts)']:10.2f} pts | DD {row['Max Drawdown (pts)']:8.2f} pts")
            
            print(f"\n{'='*100}")
        else:
            print("\nNo results to display.")
        
        return all_results


def main():
    """Main execution function"""
    print("="*80)
    print("FVG INVERSION STRATEGY BACKTESTING")
    print("NQ 5-minute data (2018-2025)")
    print("="*80)
    
    # Initialize backtester
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    backtester = FVGBacktester(data_dir)
    
    # Run all strategies with gap size ranges
    backtester.run_strategies_with_gap_ranges()
    
    print("\nBacktesting complete!")


if __name__ == "__main__":
    main()
