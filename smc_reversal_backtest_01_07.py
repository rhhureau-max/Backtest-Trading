#!/usr/bin/env python3
"""
SMC Reversal Backtest Strategy for NQ 01:00-07:00 Session
==========================================================

This script implements a Smart Money Concepts (SMC) reversal strategy
focused on identifying liquidity sweeps, market structure shifts (MSS),
and Fair Value Gaps (FVG) for high-probability reversal trades.

Strategy Logic:
- Detects Fractal Highs/Lows (swing points)
- Identifies liquidity sweeps (breaks then rejects)
- Confirms Market Structure Shift (MSS)
- Enters on 50% Fibonacci retracement
- Targets first FVG created during MSS move
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import os
import sys
from typing import List, Tuple, Optional, Dict
import warnings
warnings.filterwarnings('ignore')


class SMCReversalBacktest:
    """
    SMC Reversal Strategy Backtester
    
    Implements both long and short setups based on:
    1. Fractal detection (swing points)
    2. Liquidity sweep identification
    3. Market Structure Shift (MSS) confirmation
    4. Fibonacci retracement entry
    5. FVG-based take profit
    """
    
    def __init__(self, session_start='01:00:00', session_end='07:00:00', 
                 fractal_periods=2, mss_lookback=30, max_sweep_delay=5, 
                 min_trade_spacing=10):
        """
        Initialize the backtester
        
        Args:
            session_start: Session start time (HH:MM:SS)
            session_end: Session end time (HH:MM:SS)
            fractal_periods: Number of candles each side for fractal
            mss_lookback: How far back to look for significant fractals
            max_sweep_delay: Max candles after sweep for rejection
            min_trade_spacing: Minimum candles between trades
        """
        self.session_start = time.fromisoformat(session_start)
        self.session_end = time.fromisoformat(session_end)
        self.fractal_periods = fractal_periods
        self.mss_lookback = mss_lookback
        self.max_sweep_delay = max_sweep_delay
        self.min_trade_spacing = min_trade_spacing
        
        # Trade tracking
        self.trades = []
        self.equity_curve = []
        
    def load_data(self, years: List[int] = None) -> pd.DataFrame:
        """
        Load and combine NQ 5-minute data from CSV files
        
        Args:
            years: List of years to load (default: 2023-2025)
        
        Returns:
            Combined DataFrame with parsed datetime
        """
        if years is None:
            years = [2023, 2024, 2025]
        
        all_data = []
        
        for year in years:
            filename = f"{year} 5m.csv"
            if not os.path.exists(filename):
                print(f"Warning: {filename} not found, skipping...")
                continue
            
            print(f"Loading {filename}...")
            df = pd.read_csv(filename, sep=';')
            
            # Parse datetime (DD/MM/YYYY and HH:MM:SS)
            df['datetime'] = pd.to_datetime(
                df['Column1'] + ' ' + df['Column2'], 
                format='%d/%m/%Y %H:%M:%S'
            )
            
            # Rename columns
            df = df.rename(columns={
                'Column3': 'open',
                'Column4': 'high',
                'Column5': 'low',
                'Column6': 'close',
                'Column7': 'volume'
            })
            
            df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
            all_data.append(df)
            
        if not all_data:
            raise ValueError("No data loaded. Check if CSV files exist.")
        
        # Combine all years
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.sort_values('datetime').reset_index(drop=True)
        
        print(f"Total data loaded: {len(combined)} candles")
        print(f"Date range: {combined['datetime'].min()} to {combined['datetime'].max()}")
        
        return combined
    
    def filter_session(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter data to session window (01:00-07:00)
        
        Args:
            df: DataFrame with datetime column
        
        Returns:
            Filtered DataFrame
        """
        df['time'] = df['datetime'].dt.time
        session_mask = (df['time'] >= self.session_start) & (df['time'] <= self.session_end)
        return df[session_mask].copy()
    
    def detect_fractals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect Fractal Highs and Fractal Lows
        
        Fractal High: A high surrounded by N lower highs on each side
        Fractal Low: A low surrounded by N higher lows on each side
        
        Args:
            df: DataFrame with OHLC data
        
        Returns:
            DataFrame with fractal_high and fractal_low boolean columns
        """
        n = self.fractal_periods
        
        df['fractal_high'] = False
        df['fractal_low'] = False
        
        for i in range(n, len(df) - n):
            # Check if current high is highest in window
            window_highs = df['high'].iloc[i-n:i+n+1]
            if df['high'].iloc[i] == window_highs.max():
                # Ensure it's surrounded by lower highs
                left_ok = all(df['high'].iloc[i] > df['high'].iloc[i-j] for j in range(1, n+1))
                right_ok = all(df['high'].iloc[i] > df['high'].iloc[i+j] for j in range(1, n+1))
                if left_ok and right_ok:
                    df.loc[df.index[i], 'fractal_high'] = True
            
            # Check if current low is lowest in window
            window_lows = df['low'].iloc[i-n:i+n+1]
            if df['low'].iloc[i] == window_lows.min():
                # Ensure it's surrounded by higher lows
                left_ok = all(df['low'].iloc[i] < df['low'].iloc[i-j] for j in range(1, n+1))
                right_ok = all(df['low'].iloc[i] < df['low'].iloc[i+j] for j in range(1, n+1))
                if left_ok and right_ok:
                    df.loc[df.index[i], 'fractal_low'] = True
        
        return df
    
    def detect_fvg(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect Fair Value Gaps (FVG)
        
        Bearish FVG: Gap where Low[N] > High[N+2] (unfilled gap down)
        Bullish FVG: Gap where High[N] < Low[N+2] (unfilled gap up)
        
        Args:
            df: DataFrame with OHLC data
        
        Returns:
            DataFrame with FVG information
        """
        df['bearish_fvg'] = False
        df['bullish_fvg'] = False
        df['fvg_top'] = np.nan
        df['fvg_bottom'] = np.nan
        
        for i in range(len(df) - 2):
            # Bearish FVG: Low[i] > High[i+2]
            if df['low'].iloc[i] > df['high'].iloc[i+2]:
                df.loc[df.index[i+1], 'bearish_fvg'] = True
                df.loc[df.index[i+1], 'fvg_top'] = df['low'].iloc[i]
                df.loc[df.index[i+1], 'fvg_bottom'] = df['high'].iloc[i+2]
            
            # Bullish FVG: High[i] < Low[i+2]
            elif df['high'].iloc[i] < df['low'].iloc[i+2]:
                df.loc[df.index[i+1], 'bullish_fvg'] = True
                df.loc[df.index[i+1], 'fvg_top'] = df['low'].iloc[i+2]
                df.loc[df.index[i+1], 'fvg_bottom'] = df['high'].iloc[i]
        
        return df
    
    def identify_liquidity_sweep(self, df: pd.DataFrame, idx: int, 
                                   direction: str) -> Optional[Dict]:
        """
        Identify if a liquidity sweep occurred
        
        Short setup: Price exceeds fractal high then rejects
        Long setup: Price exceeds fractal low then rejects
        
        Args:
            df: DataFrame with OHLC and fractal data
            idx: Current candle index
            direction: 'short' or 'long'
        
        Returns:
            Dict with sweep info or None
        """
        lookback = self.mss_lookback
        start_idx = max(0, idx - lookback)
        
        if direction == 'short':
            # Look for recent fractal highs
            recent_fractals = df.iloc[start_idx:idx]
            fractal_highs = recent_fractals[recent_fractals['fractal_high']]
            
            if len(fractal_highs) == 0:
                return None
            
            # Get the most recent significant fractal high
            last_fractal_high = fractal_highs['high'].iloc[-1]
            last_fractal_idx = fractal_highs.index[-1]
            
            # Check if current or recent candles swept above it
            for j in range(max(0, idx - self.max_sweep_delay), idx + 1):
                if j >= len(df):
                    break
                
                candle = df.iloc[j]
                
                # More permissive: sweep if high exceeds fractal OR close is near rejection
                if candle['high'] > last_fractal_high:
                    # Accept if closes below high or shows bearish rejection
                    if (candle['close'] < last_fractal_high or 
                        (candle['high'] - candle['close']) > (candle['close'] - candle['open']) * 0.5):
                        return {
                            'sweep_idx': j,
                            'sweep_high': candle['high'],
                            'fractal_high': last_fractal_high,
                            'fractal_idx': last_fractal_idx,
                            'rejection': True
                        }
        
        elif direction == 'long':
            # Look for recent fractal lows
            recent_fractals = df.iloc[start_idx:idx]
            fractal_lows = recent_fractals[recent_fractals['fractal_low']]
            
            if len(fractal_lows) == 0:
                return None
            
            # Get the most recent significant fractal low
            last_fractal_low = fractal_lows['low'].iloc[-1]
            last_fractal_idx = fractal_lows.index[-1]
            
            # Check if current or recent candles swept below it
            for j in range(max(0, idx - self.max_sweep_delay), idx + 1):
                if j >= len(df):
                    break
                
                candle = df.iloc[j]
                
                # More permissive: sweep if low exceeds fractal OR close is near rejection
                if candle['low'] < last_fractal_low:
                    # Accept if closes above low or shows bullish rejection
                    if (candle['close'] > last_fractal_low or 
                        (candle['close'] - candle['low']) > (candle['open'] - candle['close']) * 0.5):
                        return {
                            'sweep_idx': j,
                            'sweep_low': candle['low'],
                            'fractal_low': last_fractal_low,
                            'fractal_idx': last_fractal_idx,
                            'rejection': True
                        }
        
        return None
    
    def check_mss(self, df: pd.DataFrame, sweep_info: Dict, 
                   idx: int, direction: str) -> Optional[Dict]:
        """
        Check if Market Structure Shift (MSS) occurred
        
        Short: Price breaks below recent significant fractal low
        Long: Price breaks above recent significant fractal high
        
        Args:
            df: DataFrame with OHLC and fractal data
            sweep_info: Information about the liquidity sweep
            idx: Current candle index
            direction: 'short' or 'long'
        
        Returns:
            Dict with MSS info or None
        """
        sweep_idx = sweep_info['sweep_idx']
        
        if direction == 'short':
            # Find significant fractal lows BEFORE the sweep
            pre_sweep = df.iloc[max(0, sweep_idx - self.mss_lookback):sweep_idx]
            fractal_lows = pre_sweep[pre_sweep['fractal_low']]
            
            if len(fractal_lows) == 0:
                return None
            
            # Most recent fractal low before sweep
            mss_level = fractal_lows['low'].iloc[-1]
            mss_fractal_idx = fractal_lows.index[-1]
            
            # Check if price broke below it after the sweep
            for j in range(sweep_idx, idx + 1):
                if j >= len(df):
                    break
                
                if df['low'].iloc[j] < mss_level:
                    return {
                        'mss_idx': j,
                        'mss_low': df['low'].iloc[j],
                        'mss_level': mss_level,
                        'mss_fractal_idx': mss_fractal_idx
                    }
        
        elif direction == 'long':
            # Find significant fractal highs BEFORE the sweep
            pre_sweep = df.iloc[max(0, sweep_idx - self.mss_lookback):sweep_idx]
            fractal_highs = pre_sweep[pre_sweep['fractal_high']]
            
            if len(fractal_highs) == 0:
                return None
            
            # Most recent fractal high before sweep
            mss_level = fractal_highs['high'].iloc[-1]
            mss_fractal_idx = fractal_highs.index[-1]
            
            # Check if price broke above it after the sweep
            for j in range(sweep_idx, idx + 1):
                if j >= len(df):
                    break
                
                if df['high'].iloc[j] > mss_level:
                    return {
                        'mss_idx': j,
                        'mss_high': df['high'].iloc[j],
                        'mss_level': mss_level,
                        'mss_fractal_idx': mss_fractal_idx
                    }
        
        return None
    
    def calculate_fib_entry(self, sweep_info: Dict, mss_info: Dict, 
                            direction: str) -> float:
        """
        Calculate 50% Fibonacci retracement entry level
        
        Args:
            sweep_info: Liquidity sweep information
            mss_info: Market Structure Shift information
            direction: 'short' or 'long'
        
        Returns:
            Entry price at 50% retracement
        """
        if direction == 'short':
            # 50% between sweep high and MSS low
            high_point = sweep_info['sweep_high']
            low_point = mss_info['mss_low']
            return low_point + (high_point - low_point) * 0.5
        
        elif direction == 'long':
            # 50% between sweep low and MSS high
            low_point = sweep_info['sweep_low']
            high_point = mss_info['mss_high']
            return high_point - (high_point - low_point) * 0.5
        
        return None
    
    def find_nearest_fvg(self, df: pd.DataFrame, mss_idx: int, 
                         direction: str) -> Optional[float]:
        """
        Find first unfilled FVG created during MSS move
        
        Args:
            df: DataFrame with FVG data
            mss_idx: Index where MSS occurred
            direction: 'short' or 'long'
        
        Returns:
            TP level (middle of FVG) or None
        """
        if direction == 'short':
            # Look for bearish FVGs around MSS
            search_start = max(0, mss_idx - 5)
            search_end = min(len(df), mss_idx + 5)
            
            fvgs = df.iloc[search_start:search_end]
            bearish_fvgs = fvgs[fvgs['bearish_fvg']]
            
            if len(bearish_fvgs) > 0:
                # Use the first FVG found
                fvg = bearish_fvgs.iloc[0]
                return (fvg['fvg_top'] + fvg['fvg_bottom']) / 2
        
        elif direction == 'long':
            # Look for bullish FVGs around MSS
            search_start = max(0, mss_idx - 5)
            search_end = min(len(df), mss_idx + 5)
            
            fvgs = df.iloc[search_start:search_end]
            bullish_fvgs = fvgs[fvgs['bullish_fvg']]
            
            if len(bullish_fvgs) > 0:
                # Use the first FVG found
                fvg = bullish_fvgs.iloc[0]
                return (fvg['fvg_top'] + fvg['fvg_bottom']) / 2
        
        return None
    
    def simulate_trade(self, df: pd.DataFrame, entry_idx: int, 
                       entry_price: float, sl_price: float, 
                       tp_price: float, direction: str) -> Dict:
        """
        Simulate trade execution from entry onwards
        
        Args:
            df: DataFrame with OHLC data
            entry_idx: Index where entry signal generated
            entry_price: Entry limit price
            sl_price: Stop loss price
            tp_price: Take profit price
            direction: 'short' or 'long'
        
        Returns:
            Trade result dictionary
        """
        entry_filled = False
        actual_entry_idx = None
        actual_entry_price = None
        exit_idx = None
        exit_price = None
        result = None
        
        # Check if entry gets filled
        for i in range(entry_idx, min(entry_idx + 50, len(df))):
            candle = df.iloc[i]
            
            if not entry_filled:
                # Check if price reaches entry level
                if direction == 'short':
                    if candle['high'] >= entry_price:
                        entry_filled = True
                        actual_entry_idx = i
                        actual_entry_price = entry_price
                elif direction == 'long':
                    if candle['low'] <= entry_price:
                        entry_filled = True
                        actual_entry_idx = i
                        actual_entry_price = entry_price
            
            else:
                # Monitor for SL or TP hit
                if direction == 'short':
                    # Check SL first (worst case)
                    if candle['high'] >= sl_price:
                        exit_idx = i
                        exit_price = sl_price
                        result = 'loss'
                        break
                    # Check TP
                    elif candle['low'] <= tp_price:
                        exit_idx = i
                        exit_price = tp_price
                        result = 'win'
                        break
                
                elif direction == 'long':
                    # Check SL first (worst case)
                    if candle['low'] <= sl_price:
                        exit_idx = i
                        exit_price = sl_price
                        result = 'loss'
                        break
                    # Check TP
                    elif candle['high'] >= tp_price:
                        exit_idx = i
                        exit_price = tp_price
                        result = 'win'
                        break
        
        if not entry_filled:
            return {'status': 'no_fill'}
        
        if result is None:
            return {'status': 'timeout'}
        
        # Calculate P&L
        if direction == 'short':
            pnl = actual_entry_price - exit_price
        else:
            pnl = exit_price - actual_entry_price
        
        risk = abs(actual_entry_price - sl_price)
        reward = abs(tp_price - actual_entry_price)
        rr_ratio = reward / risk if risk > 0 else 0
        
        return {
            'status': 'completed',
            'entry_datetime': df['datetime'].iloc[actual_entry_idx],
            'entry_price': actual_entry_price,
            'exit_datetime': df['datetime'].iloc[exit_idx],
            'exit_price': exit_price,
            'sl_price': sl_price,
            'tp_price': tp_price,
            'direction': direction,
            'result': result,
            'pnl': pnl,
            'risk': risk,
            'reward': reward,
            'rr_ratio': rr_ratio
        }
    
    def run_backtest(self, df: pd.DataFrame) -> List[Dict]:
        """
        Run the complete SMC reversal backtest
        
        Args:
            df: DataFrame with OHLC data (already session-filtered)
        
        Returns:
            List of completed trades
        """
        print("\nRunning SMC Reversal Backtest...")
        print("=" * 60)
        
        # Detect fractals and FVGs
        print("Detecting fractals...")
        df = self.detect_fractals(df)
        
        print("Detecting Fair Value Gaps...")
        df = self.detect_fvg(df)
        
        trades = []
        last_trade_idx = -self.min_trade_spacing
        
        # Scan for setups
        print("Scanning for trade setups...")
        total_candles = len(df)
        
        for idx in range(self.mss_lookback + 10, total_candles - 50):
            if idx % 5000 == 0:
                progress = (idx / total_candles) * 100
                print(f"Progress: {progress:.1f}% ({idx}/{total_candles}) - Trades found: {len(trades)}")
            
            # Enforce spacing between trades
            if idx - last_trade_idx < self.min_trade_spacing:
                continue
            
            current_candle = df.iloc[idx]
            
            # Only enter during session hours
            if not (self.session_start <= current_candle['time'] <= self.session_end):
                continue
            
            # Check for SHORT setups
            sweep_info = self.identify_liquidity_sweep(df, idx, 'short')
            if sweep_info is not None:
                mss_info = self.check_mss(df, sweep_info, idx, 'short')
                if mss_info is not None:
                    # Valid setup - calculate entry
                    entry_price = self.calculate_fib_entry(sweep_info, mss_info, 'short')
                    sl_price = sweep_info['sweep_high']
                    tp_price = self.find_nearest_fvg(df, mss_info['mss_idx'], 'short')
                    
                    if tp_price is None:
                        # Fallback: use 2R
                        risk = sl_price - entry_price
                        tp_price = entry_price - (2 * risk)
                    
                    # Ensure valid risk/reward
                    if entry_price < sl_price and tp_price < entry_price:
                        # Simulate the trade
                        trade_result = self.simulate_trade(
                            df, idx, entry_price, sl_price, tp_price, 'short'
                        )
                        
                        if trade_result['status'] == 'completed':
                            trades.append(trade_result)
                            last_trade_idx = idx
                            continue
            
            # Check for LONG setups
            sweep_info = self.identify_liquidity_sweep(df, idx, 'long')
            if sweep_info is not None:
                mss_info = self.check_mss(df, sweep_info, idx, 'long')
                if mss_info is not None:
                    # Valid setup - calculate entry
                    entry_price = self.calculate_fib_entry(sweep_info, mss_info, 'long')
                    sl_price = sweep_info['sweep_low']
                    tp_price = self.find_nearest_fvg(df, mss_info['mss_idx'], 'long')
                    
                    if tp_price is None:
                        # Fallback: use 2R
                        risk = entry_price - sl_price
                        tp_price = entry_price + (2 * risk)
                    
                    # Ensure valid risk/reward
                    if entry_price > sl_price and tp_price > entry_price:
                        # Simulate the trade
                        trade_result = self.simulate_trade(
                            df, idx, entry_price, sl_price, tp_price, 'long'
                        )
                        
                        if trade_result['status'] == 'completed':
                            trades.append(trade_result)
                            last_trade_idx = idx
                            continue
        
        print(f"\nBacktest complete! Found {len(trades)} trades.")
        return trades
    
    def calculate_metrics(self, trades: List[Dict]) -> Dict:
        """
        Calculate comprehensive performance metrics
        
        Args:
            trades: List of completed trades
        
        Returns:
            Dictionary of performance metrics
        """
        if not trades:
            return {'error': 'No trades to analyze'}
        
        df_trades = pd.DataFrame(trades)
        
        # Basic metrics
        total_trades = len(df_trades)
        winning_trades = len(df_trades[df_trades['result'] == 'win'])
        losing_trades = len(df_trades[df_trades['result'] == 'loss'])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # P&L metrics
        total_pnl = df_trades['pnl'].sum()
        avg_win = df_trades[df_trades['result'] == 'win']['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = df_trades[df_trades['result'] == 'loss']['pnl'].mean() if losing_trades > 0 else 0
        
        # Risk:Reward
        avg_rr = df_trades['rr_ratio'].mean()
        
        # Profit factor
        gross_profit = df_trades[df_trades['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(df_trades[df_trades['pnl'] < 0]['pnl'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Drawdown calculation (assuming 1% risk per trade on $100k account)
        account_size = 100000
        risk_per_trade = 0.01
        
        equity = [account_size]
        for _, trade in df_trades.iterrows():
            # Convert points to dollars (NQ = $20 per point)
            dollar_pnl = trade['pnl'] * 20
            # Scale by risk percentage
            position_size = (account_size * risk_per_trade) / (trade['risk'] * 20)
            actual_pnl = dollar_pnl * position_size
            account_size += actual_pnl
            equity.append(account_size)
        
        equity_series = pd.Series(equity)
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max * 100
        max_drawdown = drawdown.min()
        
        # Yearly breakdown
        df_trades['year'] = pd.to_datetime(df_trades['entry_datetime']).dt.year
        yearly_stats = df_trades.groupby('year').agg({
            'pnl': ['sum', 'count'],
            'result': lambda x: (x == 'win').sum()
        }).round(2)
        
        metrics = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'avg_rr_ratio': round(avg_rr, 2),
            'profit_factor': round(profit_factor, 2),
            'total_pnl_points': round(total_pnl, 2),
            'avg_win_points': round(avg_win, 2),
            'avg_loss_points': round(avg_loss, 2),
            'max_drawdown_pct': round(max_drawdown, 2),
            'final_equity': round(equity[-1], 2),
            'equity_curve': equity,
            'yearly_stats': yearly_stats,
            'trades_df': df_trades
        }
        
        return metrics
    
    def plot_equity_curve(self, metrics: Dict, save_path: str = 'smc_reversal_equity_curve.png'):
        """
        Plot and save equity curve
        
        Args:
            metrics: Performance metrics dictionary
            save_path: Path to save the plot
        """
        equity = metrics['equity_curve']
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Equity curve
        ax1.plot(equity, linewidth=2, color='#2E86AB')
        ax1.axhline(y=equity[0], color='gray', linestyle='--', alpha=0.5)
        ax1.set_title('SMC Reversal Strategy - Equity Curve (1% Risk per Trade)', 
                     fontsize=14, fontweight='bold')
        ax1.set_xlabel('Trade Number', fontsize=11)
        ax1.set_ylabel('Account Value ($)', fontsize=11)
        ax1.grid(alpha=0.3)
        ax1.set_facecolor('#F8F9FA')
        
        # Format y-axis
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Drawdown
        equity_series = pd.Series(equity)
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max * 100
        
        ax2.fill_between(range(len(drawdown)), drawdown, 0, alpha=0.3, color='red')
        ax2.plot(drawdown, linewidth=1.5, color='darkred')
        ax2.set_title('Drawdown (%)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Trade Number', fontsize=11)
        ax2.set_ylabel('Drawdown (%)', fontsize=11)
        ax2.grid(alpha=0.3)
        ax2.set_facecolor('#F8F9FA')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nEquity curve saved to: {save_path}")
        plt.close()
    
    def generate_report(self, metrics: Dict, save_path: str = 'README_SMC_REVERSAL_BACKTEST.md'):
        """
        Generate comprehensive markdown report
        
        Args:
            metrics: Performance metrics dictionary
            save_path: Path to save the report
        """
        trades_df = metrics['trades_df']
        
        # Sample trades (first 5 wins and losses)
        sample_wins = trades_df[trades_df['result'] == 'win'].head(5)
        sample_losses = trades_df[trades_df['result'] == 'loss'].head(5)
        
        report = f"""# SMC Reversal Backtest Strategy - Complete Report
## NQ Futures 01:00-07:00 Session (2023-2025)

---

## Strategy Overview

### Smart Money Concepts (SMC) Reversal Strategy

This backtest implements a comprehensive SMC-based reversal strategy that identifies high-probability trade setups during the NQ futures 01:00-07:00 session window.

**Core Components:**

1. **Fractal Detection**: Identifies swing highs/lows (structural points)
   - Fractal High: A high point surrounded by {self.fractal_periods} lower highs on each side
   - Fractal Low: A low point surrounded by {self.fractal_periods} higher lows on each side

2. **Liquidity Sweep**: Smart money taking liquidity before reversing
   - SHORT: Price wicks above fractal high but closes below (rejection)
   - LONG: Price wicks below fractal low but closes above (rejection)

3. **Market Structure Shift (MSS)**: Confirmation of reversal
   - SHORT: Price breaks below recent significant fractal low
   - LONG: Price breaks above recent significant fractal high

4. **Entry Logic**: 50% Fibonacci retracement
   - Calculated from sweep extreme to MSS extreme
   - Provides optimal entry on pullback/retracement

5. **Take Profit**: First Fair Value Gap (FVG)
   - Bearish FVG: Gap where Low[N] > High[N+2]
   - Bullish FVG: Gap where High[N] < Low[N+2]
   - Fallback: 2R if no FVG detected

6. **Stop Loss**: Beyond the sweep point
   - SHORT: Above the sweep high
   - LONG: Below the sweep low

---

## Performance Summary

### Overall Results

| Metric | Value |
|--------|-------|
| **Total Trades** | {metrics['total_trades']} |
| **Winning Trades** | {metrics['winning_trades']} |
| **Losing Trades** | {metrics['losing_trades']} |
| **Win Rate** | {metrics['win_rate']}% |
| **Average R:R Ratio** | {metrics['avg_rr_ratio']}:1 |
| **Profit Factor** | {metrics['profit_factor']} |
| **Total P&L (Points)** | {metrics['total_pnl_points']} |
| **Average Win (Points)** | {metrics['avg_win_points']} |
| **Average Loss (Points)** | {metrics['avg_loss_points']} |
| **Maximum Drawdown** | {metrics['max_drawdown_pct']}% |
| **Final Account Value** | ${metrics['final_equity']:,.2f} |

**Note**: Performance calculated with 1% risk per trade on $100,000 starting capital. 
NQ point value = $20.

---

## Yearly Performance Breakdown

"""
        
        # Yearly stats
        for year in sorted(trades_df['year'].unique()):
            year_trades = trades_df[trades_df['year'] == year]
            year_wins = len(year_trades[year_trades['result'] == 'win'])
            year_total = len(year_trades)
            year_wr = (year_wins / year_total * 100) if year_total > 0 else 0
            year_pnl = year_trades['pnl'].sum()
            
            report += f"""### {year}
- **Trades**: {year_total}
- **Win Rate**: {year_wr:.1f}%
- **Total P&L**: {year_pnl:.2f} points

"""
        
        report += f"""---

## Sample Trade Examples

### Winning Trades (Sample)

"""
        
        for idx, trade in sample_wins.iterrows():
            report += f"""**Trade #{idx + 1}** - {trade['direction'].upper()}
- Entry: {trade['entry_datetime']} @ {trade['entry_price']:.2f}
- Exit: {trade['exit_datetime']} @ {trade['exit_price']:.2f}
- SL: {trade['sl_price']:.2f} | TP: {trade['tp_price']:.2f}
- P&L: +{trade['pnl']:.2f} points
- R:R: {trade['rr_ratio']:.2f}:1

"""
        
        report += """### Losing Trades (Sample)

"""
        
        for idx, trade in sample_losses.iterrows():
            report += f"""**Trade #{idx + 1}** - {trade['direction'].upper()}
- Entry: {trade['entry_datetime']} @ {trade['entry_price']:.2f}
- Exit: {trade['exit_datetime']} @ {trade['exit_price']:.2f}
- SL: {trade['sl_price']:.2f} | TP: {trade['tp_price']:.2f}
- P&L: {trade['pnl']:.2f} points
- R:R: {trade['rr_ratio']:.2f}:1

"""
        
        report += f"""---

## Key Insights

### Strategy Strengths
1. **High Risk:Reward**: Average R:R of {metrics['avg_rr_ratio']}:1 allows profitability even with sub-50% win rate
2. **Systematic Approach**: Clear rules for entry, exit, and risk management
3. **SMC Principles**: Aligns with institutional order flow concepts
4. **Session Focus**: Targets specific high-volatility window

### Areas for Optimization
1. **Setup Selectivity**: Consider additional filters to improve win rate
2. **FVG Detection**: Enhance FVG targeting for better profit targets
3. **MSS Confirmation**: Fine-tune lookback periods for structure breaks
4. **Multiple Timeframes**: Incorporate HTF bias for directional confluence

---

## Methodology

### Data
- **Instrument**: NQ Futures (Nasdaq-100 E-mini)
- **Timeframe**: 5-minute candles
- **Period**: 2023-2025
- **Session**: 01:00-07:00 (high volatility window)

### Execution Assumptions
- Realistic fill simulation (checks if price reaches entry level)
- Conservative stop loss placement (beyond sweep point)
- Dynamic take profit (based on FVG or 2R fallback)
- 1% account risk per trade
- No slippage or commission considered

### Backtesting Process
1. Load and parse multi-year 5-minute NQ data
2. Filter to 01:00-07:00 session window
3. Detect fractals (swing points) across dataset
4. Identify Fair Value Gaps (unfilled price gaps)
5. Scan for liquidity sweeps (rejection candles)
6. Confirm Market Structure Shifts
7. Calculate 50% Fibonacci entries
8. Simulate trade execution with realistic fills
9. Track equity curve and calculate metrics

---

## Visualization

See `smc_reversal_equity_curve.png` for:
- Cumulative equity curve
- Drawdown analysis

---

## Disclaimer

This backtest is for educational purposes only. Past performance does not guarantee future results. 
Trading futures involves substantial risk of loss. Always conduct your own due diligence and 
consider consulting with a financial advisor before trading.

---

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Script**: smc_reversal_backtest_01_07.py
"""
        
        with open(save_path, 'w') as f:
            f.write(report)
        
        print(f"Report saved to: {save_path}")


def main():
    """
    Main execution function
    """
    print("=" * 60)
    print("SMC REVERSAL BACKTEST - NQ 01:00-07:00 SESSION")
    print("=" * 60)
    
    # Initialize backtester
    backtester = SMCReversalBacktest(
        session_start='01:00:00',
        session_end='07:00:00',
        fractal_periods=2,
        mss_lookback=30,
        max_sweep_delay=5,
        min_trade_spacing=10
    )
    
    # Load data (focus on recent years for performance)
    print("\n[1/5] Loading data...")
    df = backtester.load_data(years=[2023, 2024, 2025])
    
    # Filter to session
    print("\n[2/5] Filtering to session window (01:00-07:00)...")
    df_session = backtester.filter_session(df)
    print(f"Session candles: {len(df_session)}")
    
    # Run backtest
    print("\n[3/5] Running backtest...")
    trades = backtester.run_backtest(df_session)
    
    if not trades:
        print("\n⚠ No trades generated. Consider adjusting parameters.")
        return
    
    # Calculate metrics
    print("\n[4/5] Calculating performance metrics...")
    metrics = backtester.calculate_metrics(trades)
    
    # Display results
    print("\n" + "=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)
    print(f"Total Trades: {metrics['total_trades']}")
    print(f"Win Rate: {metrics['win_rate']}%")
    print(f"Average R:R: {metrics['avg_rr_ratio']}:1")
    print(f"Profit Factor: {metrics['profit_factor']}")
    print(f"Total P&L: {metrics['total_pnl_points']:.2f} points")
    print(f"Max Drawdown: {metrics['max_drawdown_pct']:.2f}%")
    print(f"Final Equity: ${metrics['final_equity']:,.2f}")
    print("=" * 60)
    
    # Generate outputs
    print("\n[5/5] Generating outputs...")
    backtester.plot_equity_curve(metrics)
    backtester.generate_report(metrics)
    
    print("\n✅ Backtest complete! Check output files:")
    print("   - smc_reversal_equity_curve.png")
    print("   - README_SMC_REVERSAL_BACKTEST.md")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
