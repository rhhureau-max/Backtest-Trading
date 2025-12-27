"""
London Killzone Trading Strategies Backtest Framework
=====================================================

This module implements three trading strategies specifically designed for the 
London Killzone session (08:00-12:00 Paris time) on Nasdaq 100 (NQ) futures.

Strategies:
- Strategy A: Judas Swing (Liquidity Hunt Reversal)
- Strategy B: ORB Retest (Opening Range Breakout)
- Strategy C: HTF Continuation (Fibonacci OTE)

Constraint: Maximum ONE trade per day during the specified time window.
"""

import pandas as pd
import numpy as np
import pytz
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict, List
import warnings
warnings.filterwarnings('ignore')


class DataLoader:
    """Handles loading and preprocessing of trading data."""
    
    @staticmethod
    def load_csv(filepath: str) -> pd.DataFrame:
        """
        Load CSV data with proper datetime parsing.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            DataFrame with datetime index and OHLCV columns
        """
        # Read CSV with semicolon separator
        df = pd.read_csv(filepath, sep=';')
        
        # Rename columns
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Combine Date and Time into datetime
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                        format='%d/%m/%Y %H:%M:%S')
        
        # Set datetime as index
        df.set_index('Datetime', inplace=True)
        df.drop(['Date', 'Time'], axis=1, inplace=True)
        
        # Convert to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    @staticmethod
    def load_multiple_files(filepaths: List[str]) -> pd.DataFrame:
        """
        Load and combine multiple CSV files.
        
        Args:
            filepaths: List of file paths to load
            
        Returns:
            Combined DataFrame sorted by datetime
        """
        dfs = []
        for filepath in filepaths:
            try:
                df = DataLoader.load_csv(filepath)
                dfs.append(df)
                print(f"Loaded {filepath}: {len(df)} rows")
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        if dfs:
            combined = pd.concat(dfs)
            combined = combined.sort_index()
            combined = combined[~combined.index.duplicated(keep='first')]
            return combined
        return pd.DataFrame()


class TimeManager:
    """Handles timezone and session time management."""
    
    @staticmethod
    def convert_to_paris_time(df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert datetime index to Paris timezone.
        Assumes input data is in UTC or exchange time.
        
        Args:
            df: DataFrame with datetime index
            
        Returns:
            DataFrame with Paris timezone
        """
        df_copy = df.copy()
        
        # Localize to UTC if naive
        if df_copy.index.tz is None:
            df_copy.index = df_copy.index.tz_localize('UTC')
        
        # Convert to Paris time (Europe/Paris)
        df_copy.index = df_copy.index.tz_convert('Europe/Paris')
        
        return df_copy
    
    @staticmethod
    def get_session_data(df: pd.DataFrame, date: pd.Timestamp, 
                        start_hour: int, end_hour: int) -> pd.DataFrame:
        """
        Extract data for a specific session on a given date.
        
        Args:
            df: DataFrame with datetime index
            date: Date to extract
            start_hour: Session start hour (0-23)
            end_hour: Session end hour (0-23)
            
        Returns:
            DataFrame containing only the specified session
        """
        date_str = date.strftime('%Y-%m-%d')
        start_time = f"{date_str} {start_hour:02d}:00:00"
        end_time = f"{date_str} {end_hour:02d}:00:00"
        
        mask = (df.index >= start_time) & (df.index < end_time)
        return df[mask]


class StrategyA_JudasSwing:
    """
    Strategy A: Judas Swing (Liquidity Hunt)
    
    Logic:
    1. Calculate Asian session range (00:00-08:00 Paris)
    2. Wait for breakout after 08:00
    3. Enter on reintegration into range
    4. SL: 5 points above/below false breakout wick
    5. TP: Opposite liquidity or 1:3 R:R
    """
    
    def __init__(self, points_offset: float = 5.0, risk_reward: float = 3.0):
        self.points_offset = points_offset
        self.risk_reward = risk_reward
        self.name = "Judas Swing"
    
    def calculate_asian_range(self, df: pd.DataFrame, date: pd.Timestamp) -> Tuple[float, float]:
        """
        Calculate Asian session range (00:00-08:00).
        
        Args:
            df: DataFrame with OHLC data
            date: Date to analyze
            
        Returns:
            Tuple of (asian_high, asian_low)
        """
        asian_data = TimeManager.get_session_data(df, date, 0, 8)
        
        if len(asian_data) == 0:
            return None, None
        
        asian_high = asian_data['High'].max()
        asian_low = asian_data['Low'].min()
        
        return asian_high, asian_low
    
    def find_signal(self, df: pd.DataFrame, date: pd.Timestamp) -> Optional[Dict]:
        """
        Find Judas Swing signal for a given date.
        
        Args:
            df: DataFrame with OHLC data
            date: Date to analyze
            
        Returns:
            Dictionary with trade details or None
        """
        # Get Asian range
        asian_high, asian_low = self.calculate_asian_range(df, date)
        
        if asian_high is None or asian_low is None:
            return None
        
        # Get London session data (08:00-12:00)
        london_data = TimeManager.get_session_data(df, date, 8, 12)
        
        if len(london_data) == 0:
            return None
        
        # Look for false breakout and reintegration
        signal = None
        breakout_high = None
        breakout_low = None
        
        for i in range(len(london_data)):
            current = london_data.iloc[i]
            
            # Check for bullish false breakout (break low, then reintegrate)
            if breakout_low is None and current['Low'] < asian_low:
                breakout_low = current['Low']
                continue
            
            if breakout_low is not None and current['Close'] > asian_low:
                # Reintegration detected - LONG signal
                entry_price = current['Close']
                stop_loss = breakout_low - self.points_offset
                risk = entry_price - stop_loss
                take_profit = entry_price + (risk * self.risk_reward)
                
                # Alternative TP: Asian high
                tp_alternative = asian_high
                take_profit = max(take_profit, tp_alternative)
                
                signal = {
                    'date': date,
                    'entry_time': current.name,
                    'direction': 'LONG',
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'asian_high': asian_high,
                    'asian_low': asian_low,
                    'breakout_level': breakout_low,
                    'risk': risk
                }
                break
            
            # Check for bearish false breakout (break high, then reintegrate)
            if breakout_high is None and current['High'] > asian_high:
                breakout_high = current['High']
                continue
            
            if breakout_high is not None and current['Close'] < asian_high:
                # Reintegration detected - SHORT signal
                entry_price = current['Close']
                stop_loss = breakout_high + self.points_offset
                risk = stop_loss - entry_price
                take_profit = entry_price - (risk * self.risk_reward)
                
                # Alternative TP: Asian low
                tp_alternative = asian_low
                take_profit = min(take_profit, tp_alternative)
                
                signal = {
                    'date': date,
                    'entry_time': current.name,
                    'direction': 'SHORT',
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'asian_high': asian_high,
                    'asian_low': asian_low,
                    'breakout_level': breakout_high,
                    'risk': risk
                }
                break
        
        return signal
    
    def execute_trade(self, df: pd.DataFrame, signal: Dict) -> Dict:
        """
        Execute trade based on signal and return result.
        
        Args:
            df: DataFrame with OHLC data
            signal: Trade signal dictionary
            
        Returns:
            Trade result dictionary
        """
        entry_time = signal['entry_time']
        direction = signal['direction']
        entry_price = signal['entry_price']
        stop_loss = signal['stop_loss']
        take_profit = signal['take_profit']
        
        # Get subsequent data after entry
        subsequent_data = df[df.index > entry_time]
        
        # Check each candle for SL or TP hit
        for idx, row in subsequent_data.iterrows():
            if direction == 'LONG':
                if row['Low'] <= stop_loss:
                    return {
                        'result': 'LOSS',
                        'exit_time': idx,
                        'exit_price': stop_loss,
                        'pnl': stop_loss - entry_price,
                        'pnl_points': stop_loss - entry_price
                    }
                elif row['High'] >= take_profit:
                    return {
                        'result': 'WIN',
                        'exit_time': idx,
                        'exit_price': take_profit,
                        'pnl': take_profit - entry_price,
                        'pnl_points': take_profit - entry_price
                    }
            else:  # SHORT
                if row['High'] >= stop_loss:
                    return {
                        'result': 'LOSS',
                        'exit_time': idx,
                        'exit_price': stop_loss,
                        'pnl': entry_price - stop_loss,
                        'pnl_points': entry_price - stop_loss
                    }
                elif row['Low'] <= take_profit:
                    return {
                        'result': 'WIN',
                        'exit_time': idx,
                        'exit_price': take_profit,
                        'pnl': entry_price - take_profit,
                        'pnl_points': entry_price - take_profit
                    }
        
        # Trade still open at end of data
        return {
            'result': 'OPEN',
            'exit_time': None,
            'exit_price': None,
            'pnl': 0,
            'pnl_points': 0
        }


class StrategyB_ORBRetest:
    """
    Strategy B: Opening Range Breakout (ORB) Retest
    
    Logic:
    1. Define opening box (08:00-09:00 Paris)
    2. Wait for breakout after 09:00
    3. Enter on retest of broken level (limit order)
    4. SL: Middle of box (50% range)
    5. TP: 200% extension of box range
    """
    
    def __init__(self, retest_window_hours: int = 2):
        self.retest_window_hours = retest_window_hours  # Valid until 11:00
        self.name = "ORB Retest"
    
    def calculate_opening_box(self, df: pd.DataFrame, date: pd.Timestamp) -> Tuple[float, float]:
        """
        Calculate opening box range (08:00-09:00).
        
        Args:
            df: DataFrame with OHLC data
            date: Date to analyze
            
        Returns:
            Tuple of (box_high, box_low)
        """
        box_data = TimeManager.get_session_data(df, date, 8, 9)
        
        if len(box_data) == 0:
            return None, None
        
        box_high = box_data['High'].max()
        box_low = box_data['Low'].min()
        
        return box_high, box_low
    
    def find_signal(self, df: pd.DataFrame, date: pd.Timestamp) -> Optional[Dict]:
        """
        Find ORB Retest signal for a given date.
        
        Args:
            df: DataFrame with OHLC data
            date: Date to analyze
            
        Returns:
            Dictionary with trade details or None
        """
        # Get opening box
        box_high, box_low = self.calculate_opening_box(df, date)
        
        if box_high is None or box_low is None:
            return None
        
        box_range = box_high - box_low
        box_mid = (box_high + box_low) / 2
        
        # Get data after 09:00 until 11:00
        date_str = date.strftime('%Y-%m-%d')
        start_time = f"{date_str} 09:00:00"
        end_time = f"{date_str} 11:00:00"
        
        mask = (df.index >= start_time) & (df.index < end_time)
        trading_data = df[mask]
        
        if len(trading_data) == 0:
            return None
        
        # Look for breakout
        signal = None
        breakout_detected = None
        
        for i in range(len(trading_data)):
            current = trading_data.iloc[i]
            
            # Check for bullish breakout
            if breakout_detected is None and current['Close'] > box_high:
                breakout_detected = 'BULLISH'
                continue
            
            # Check for bearish breakout
            if breakout_detected is None and current['Close'] < box_low:
                breakout_detected = 'BEARISH'
                continue
            
            # Check for retest after bullish breakout
            if breakout_detected == 'BULLISH' and current['Low'] <= box_high:
                # Retest detected - LONG signal
                entry_price = box_high
                stop_loss = box_mid
                risk = entry_price - stop_loss
                take_profit = entry_price + (box_range * 2)
                
                signal = {
                    'date': date,
                    'entry_time': current.name,
                    'direction': 'LONG',
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'box_high': box_high,
                    'box_low': box_low,
                    'box_range': box_range,
                    'risk': risk,
                    'order_type': 'LIMIT'
                }
                break
            
            # Check for retest after bearish breakout
            if breakout_detected == 'BEARISH' and current['High'] >= box_low:
                # Retest detected - SHORT signal
                entry_price = box_low
                stop_loss = box_mid
                risk = stop_loss - entry_price
                take_profit = entry_price - (box_range * 2)
                
                signal = {
                    'date': date,
                    'entry_time': current.name,
                    'direction': 'SHORT',
                    'entry_price': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'box_high': box_high,
                    'box_low': box_low,
                    'box_range': box_range,
                    'risk': risk,
                    'order_type': 'LIMIT'
                }
                break
        
        return signal
    
    def execute_trade(self, df: pd.DataFrame, signal: Dict) -> Dict:
        """
        Execute trade based on signal and return result.
        
        Args:
            df: DataFrame with OHLC data
            signal: Trade signal dictionary
            
        Returns:
            Trade result dictionary
        """
        entry_time = signal['entry_time']
        direction = signal['direction']
        entry_price = signal['entry_price']
        stop_loss = signal['stop_loss']
        take_profit = signal['take_profit']
        
        # Get subsequent data after entry
        subsequent_data = df[df.index > entry_time]
        
        # Check each candle for SL or TP hit
        for idx, row in subsequent_data.iterrows():
            if direction == 'LONG':
                if row['Low'] <= stop_loss:
                    return {
                        'result': 'LOSS',
                        'exit_time': idx,
                        'exit_price': stop_loss,
                        'pnl': stop_loss - entry_price,
                        'pnl_points': stop_loss - entry_price
                    }
                elif row['High'] >= take_profit:
                    return {
                        'result': 'WIN',
                        'exit_time': idx,
                        'exit_price': take_profit,
                        'pnl': take_profit - entry_price,
                        'pnl_points': take_profit - entry_price
                    }
            else:  # SHORT
                if row['High'] >= stop_loss:
                    return {
                        'result': 'LOSS',
                        'exit_time': idx,
                        'exit_price': stop_loss,
                        'pnl': entry_price - stop_loss,
                        'pnl_points': entry_price - stop_loss
                    }
                elif row['Low'] <= take_profit:
                    return {
                        'result': 'WIN',
                        'exit_time': idx,
                        'exit_price': take_profit,
                        'pnl': entry_price - take_profit,
                        'pnl_points': entry_price - take_profit
                    }
        
        # Trade still open at end of data
        return {
            'result': 'OPEN',
            'exit_time': None,
            'exit_price': None,
            'pnl': 0,
            'pnl_points': 0
        }


class StrategyC_HTFContinuation:
    """
    Strategy C: Higher Timeframe Continuation (Fibonacci OTE)
    
    Logic:
    1. Determine bias from D1 candle or H4 MA50
    2. Wait for pullback in London session
    3. Enter on Fibonacci OTE zone (61.8%-79% retracement)
    4. Look for reversal patterns (pinbar, engulfing)
    5. SL: Below swing low (Fib 0%)
    6. TP: Swing high (Fib 100%) or -0.27 extension
    """
    
    def __init__(self, ote_low: float = 0.618, ote_high: float = 0.79):
        self.ote_low = ote_low
        self.ote_high = ote_high
        self.name = "HTF Continuation (Fib OTE)"
    
    def determine_bias(self, df: pd.DataFrame, df_h4: pd.DataFrame, 
                      date: pd.Timestamp) -> Optional[str]:
        """
        Determine directional bias from D1 or H4 data.
        
        Args:
            df: Main DataFrame
            df_h4: H4 timeframe DataFrame
            date: Date to analyze
            
        Returns:
            'BULLISH' or 'BEARISH' or None
        """
        # Get previous day's candle
        prev_date = date - timedelta(days=1)
        date_str = prev_date.strftime('%Y-%m-%d')
        
        # Try to find D1 candle
        try:
            day_data = df[df.index.date == prev_date.date()]
            if len(day_data) > 0:
                day_open = day_data.iloc[0]['Open']
                day_close = day_data.iloc[-1]['Close']
                
                if day_close > day_open:
                    return 'BULLISH'
                else:
                    return 'BEARISH'
        except:
            pass
        
        # Fallback: Use H4 MA50 if available
        if df_h4 is not None and len(df_h4) >= 50:
            try:
                recent_h4 = df_h4[df_h4.index <= date].tail(50)
                if len(recent_h4) >= 50:
                    ma50 = recent_h4['Close'].mean()
                    current_price = recent_h4.iloc[-1]['Close']
                    
                    if current_price > ma50:
                        return 'BULLISH'
                    else:
                        return 'BEARISH'
            except:
                pass
        
        return None
    
    def calculate_fibonacci_levels(self, swing_low: float, swing_high: float) -> Dict:
        """
        Calculate Fibonacci retracement levels.
        
        Args:
            swing_low: Swing low price
            swing_high: Swing high price
            
        Returns:
            Dictionary with Fibonacci levels
        """
        diff = swing_high - swing_low
        
        return {
            '0.0': swing_low,
            '0.236': swing_low + (diff * 0.236),
            '0.382': swing_low + (diff * 0.382),
            '0.5': swing_low + (diff * 0.5),
            '0.618': swing_low + (diff * 0.618),
            '0.79': swing_low + (diff * 0.79),
            '1.0': swing_high,
            '-0.27': swing_high + (diff * 0.27)
        }
    
    def is_reversal_pattern(self, candle: pd.Series, prev_candle: pd.Series, 
                           direction: str) -> bool:
        """
        Detect reversal candlestick patterns.
        
        Args:
            candle: Current candle
            prev_candle: Previous candle
            direction: Expected direction ('BULLISH' or 'BEARISH')
            
        Returns:
            True if reversal pattern detected
        """
        body_current = abs(candle['Close'] - candle['Open'])
        body_prev = abs(prev_candle['Close'] - prev_candle['Open'])
        
        if direction == 'BULLISH':
            # Bullish pinbar: long lower wick, small body, close near high
            lower_wick = candle['Open'] - candle['Low'] if candle['Close'] > candle['Open'] else candle['Close'] - candle['Low']
            if lower_wick > body_current * 2 and candle['Close'] > candle['Open']:
                return True
            
            # Bullish engulfing
            if (candle['Close'] > candle['Open'] and 
                prev_candle['Close'] < prev_candle['Open'] and
                candle['Close'] > prev_candle['Open'] and
                candle['Open'] < prev_candle['Close']):
                return True
        
        else:  # BEARISH
            # Bearish pinbar: long upper wick, small body, close near low
            upper_wick = candle['High'] - candle['Open'] if candle['Close'] < candle['Open'] else candle['High'] - candle['Close']
            if upper_wick > body_current * 2 and candle['Close'] < candle['Open']:
                return True
            
            # Bearish engulfing
            if (candle['Close'] < candle['Open'] and 
                prev_candle['Close'] > prev_candle['Open'] and
                candle['Close'] < prev_candle['Open'] and
                candle['Open'] > prev_candle['Close']):
                return True
        
        return False
    
    def find_signal(self, df: pd.DataFrame, df_h4: pd.DataFrame, 
                   date: pd.Timestamp) -> Optional[Dict]:
        """
        Find HTF Continuation signal for a given date.
        
        Args:
            df: DataFrame with OHLC data (5m or 15m)
            df_h4: H4 timeframe DataFrame
            date: Date to analyze
            
        Returns:
            Dictionary with trade details or None
        """
        # Determine bias
        bias = self.determine_bias(df, df_h4, date)
        
        if bias is None:
            return None
        
        # Get London session data (08:00-12:00)
        london_data = TimeManager.get_session_data(df, date, 8, 12)
        
        if len(london_data) < 2:
            return None
        
        # Find swing points for Fibonacci
        if bias == 'BULLISH':
            # For bullish: swing low to current high
            swing_low = london_data['Low'].min()
            swing_high = london_data['High'].max()
        else:
            # For bearish: swing high to current low
            swing_high = london_data['High'].max()
            swing_low = london_data['Low'].min()
        
        fib_levels = self.calculate_fibonacci_levels(swing_low, swing_high)
        ote_low_level = fib_levels[str(self.ote_low)]
        ote_high_level = fib_levels[str(self.ote_high)]
        
        # Look for price in OTE zone with reversal pattern
        signal = None
        
        for i in range(1, len(london_data)):
            current = london_data.iloc[i]
            prev = london_data.iloc[i-1]
            
            if bias == 'BULLISH':
                # Check if price is in OTE zone
                if ote_low_level <= current['Low'] <= ote_high_level:
                    # Check for bullish reversal pattern
                    if self.is_reversal_pattern(current, prev, 'BULLISH'):
                        entry_price = current['Close']
                        stop_loss = swing_low - 5  # 5 points buffer
                        take_profit = fib_levels['-0.27']  # Extension target
                        risk = entry_price - stop_loss
                        
                        signal = {
                            'date': date,
                            'entry_time': current.name,
                            'direction': 'LONG',
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'bias': bias,
                            'swing_low': swing_low,
                            'swing_high': swing_high,
                            'ote_zone': (ote_low_level, ote_high_level),
                            'risk': risk
                        }
                        break
            
            else:  # BEARISH
                # Check if price is in OTE zone (for bearish, it's reversed)
                if ote_low_level <= current['High'] <= ote_high_level:
                    # Check for bearish reversal pattern
                    if self.is_reversal_pattern(current, prev, 'BEARISH'):
                        entry_price = current['Close']
                        stop_loss = swing_high + 5  # 5 points buffer
                        take_profit = swing_low - (swing_high - swing_low) * 0.27
                        risk = stop_loss - entry_price
                        
                        signal = {
                            'date': date,
                            'entry_time': current.name,
                            'direction': 'SHORT',
                            'entry_price': entry_price,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit,
                            'bias': bias,
                            'swing_low': swing_low,
                            'swing_high': swing_high,
                            'ote_zone': (ote_low_level, ote_high_level),
                            'risk': risk
                        }
                        break
        
        return signal
    
    def execute_trade(self, df: pd.DataFrame, signal: Dict) -> Dict:
        """
        Execute trade based on signal and return result.
        
        Args:
            df: DataFrame with OHLC data
            signal: Trade signal dictionary
            
        Returns:
            Trade result dictionary
        """
        entry_time = signal['entry_time']
        direction = signal['direction']
        entry_price = signal['entry_price']
        stop_loss = signal['stop_loss']
        take_profit = signal['take_profit']
        
        # Get subsequent data after entry
        subsequent_data = df[df.index > entry_time]
        
        # Check each candle for SL or TP hit
        for idx, row in subsequent_data.iterrows():
            if direction == 'LONG':
                if row['Low'] <= stop_loss:
                    return {
                        'result': 'LOSS',
                        'exit_time': idx,
                        'exit_price': stop_loss,
                        'pnl': stop_loss - entry_price,
                        'pnl_points': stop_loss - entry_price
                    }
                elif row['High'] >= take_profit:
                    return {
                        'result': 'WIN',
                        'exit_time': idx,
                        'exit_price': take_profit,
                        'pnl': take_profit - entry_price,
                        'pnl_points': take_profit - entry_price
                    }
            else:  # SHORT
                if row['High'] >= stop_loss:
                    return {
                        'result': 'LOSS',
                        'exit_time': idx,
                        'exit_price': stop_loss,
                        'pnl': entry_price - stop_loss,
                        'pnl_points': entry_price - stop_loss
                    }
                elif row['Low'] <= take_profit:
                    return {
                        'result': 'WIN',
                        'exit_time': idx,
                        'exit_price': take_profit,
                        'pnl': entry_price - take_profit,
                        'pnl_points': entry_price - take_profit
                    }
        
        # Trade still open at end of data
        return {
            'result': 'OPEN',
            'exit_time': None,
            'exit_price': None,
            'pnl': 0,
            'pnl_points': 0
        }


class BacktestEngine:
    """Main backtesting engine for running strategies."""
    
    def __init__(self, df: pd.DataFrame, df_h4: Optional[pd.DataFrame] = None):
        """
        Initialize backtest engine.
        
        Args:
            df: Main DataFrame with intraday data (5m or 15m)
            df_h4: Optional H4 DataFrame for HTF analysis
        """
        self.df = df
        self.df_h4 = df_h4
        self.results = []
    
    def run_strategy(self, strategy, start_date: str = None, end_date: str = None):
        """
        Run a strategy across all trading days.
        
        Args:
            strategy: Strategy instance to run
            start_date: Start date for backtest (YYYY-MM-DD)
            end_date: End date for backtest (YYYY-MM-DD)
            
        Returns:
            List of trade results
        """
        # Get unique dates
        dates = pd.Series(self.df.index.date).unique()
        
        if start_date:
            dates = dates[dates >= pd.to_datetime(start_date).date()]
        if end_date:
            dates = dates[dates <= pd.to_datetime(end_date).date()]
        
        trades = []
        
        print(f"\nRunning {strategy.name} strategy...")
        print(f"Analyzing {len(dates)} trading days...")
        
        for date in dates:
            date_ts = pd.Timestamp(date)
            
            # Find signal
            if isinstance(strategy, StrategyC_HTFContinuation):
                signal = strategy.find_signal(self.df, self.df_h4, date_ts)
            else:
                signal = strategy.find_signal(self.df, date_ts)
            
            if signal is not None:
                # Execute trade
                result = strategy.execute_trade(self.df, signal)
                
                # Combine signal and result
                trade = {**signal, **result}
                trades.append(trade)
        
        print(f"Found {len(trades)} trade signals")
        
        return trades
    
    def generate_performance_report(self, trades: List[Dict], strategy_name: str) -> Dict:
        """
        Generate performance statistics for trades.
        
        Args:
            trades: List of trade dictionaries
            strategy_name: Name of the strategy
            
        Returns:
            Dictionary with performance metrics
        """
        if not trades:
            return {
                'strategy': strategy_name,
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'profit_factor': 0,
                'total_pnl': 0,
                'max_consecutive_losses': 0
            }
        
        df_trades = pd.DataFrame(trades)
        
        wins = df_trades[df_trades['result'] == 'WIN']
        losses = df_trades[df_trades['result'] == 'LOSS']
        
        total_trades = len(df_trades)
        winning_trades = len(wins)
        losing_trades = len(losses)
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        avg_win = wins['pnl_points'].mean() if len(wins) > 0 else 0
        avg_loss = losses['pnl_points'].mean() if len(losses) > 0 else 0
        
        total_win_pnl = wins['pnl_points'].sum() if len(wins) > 0 else 0
        total_loss_pnl = abs(losses['pnl_points'].sum()) if len(losses) > 0 else 0
        
        profit_factor = (total_win_pnl / total_loss_pnl) if total_loss_pnl > 0 else 0
        total_pnl = df_trades['pnl_points'].sum()
        
        # Calculate max consecutive losses
        max_consecutive_losses = 0
        current_consecutive = 0
        for result in df_trades['result']:
            if result == 'LOSS':
                current_consecutive += 1
                max_consecutive_losses = max(max_consecutive_losses, current_consecutive)
            else:
                current_consecutive = 0
        
        return {
            'strategy': strategy_name,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'profit_factor': round(profit_factor, 2),
            'total_pnl': round(total_pnl, 2),
            'max_consecutive_losses': max_consecutive_losses,
            'avg_risk_reward': round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0
        }


def create_comparison_table():
    """
    Create a theoretical comparison table for the three strategies.
    
    Returns:
        DataFrame with strategy comparison
    """
    comparison = {
        'Strategy': [
            'A: Judas Swing',
            'B: ORB Retest', 
            'C: HTF Continuation'
        ],
        'Setup Type': [
            'Reversal (False Breakout)',
            'Continuation (Breakout + Retest)',
            'Trend Following (Fibonacci)'
        ],
        'Entry Style': [
            'Market Order',
            'Limit Order',
            'Market Order'
        ],
        'Risk/Reward': [
            '1:3 (Fixed)',
            '1:4 (Variable, based on box)',
            '1:2-1:3 (HTF dependent)'
        ],
        'Win Rate Expected': [
            '45-55%',
            '50-60%',
            '55-65%'
        ],
        'Best For NQ When': [
            'High volatility, choppy opens',
            'Trending days, clear direction',
            'Strong HTF trend alignment'
        ],
        'Weaknesses': [
            'Can miss if no false breakout',
            'Requires patience for retest',
            'Complex, needs HTF data'
        ],
        'Strengths': [
            'Catches reversals early',
            'Better R:R, clear levels',
            'High probability with trend'
        ],
        'Volatility Preference': [
            'High (whipsaw markets)',
            'Medium-High (momentum)',
            'Medium (trending markets)'
        ]
    }
    
    return pd.DataFrame(comparison)


if __name__ == "__main__":
    print("="*60)
    print("London Killzone Trading Strategies Backtest")
    print("="*60)
    print("\nThis module provides three trading strategies for NQ futures:")
    print("- Strategy A: Judas Swing (False Breakout Reversal)")
    print("- Strategy B: ORB Retest (Opening Range Breakout)")
    print("- Strategy C: HTF Continuation (Fibonacci OTE)")
    print("\nAll strategies trade only during 08:00-12:00 Paris time")
    print("Maximum one trade per day\n")
    
    # Display comparison table
    print("\n" + "="*60)
    print("STRATEGY COMPARISON TABLE")
    print("="*60 + "\n")
    
    comparison_df = create_comparison_table()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 40)
    
    print(comparison_df.to_string(index=False))
    print("\n" + "="*60)
