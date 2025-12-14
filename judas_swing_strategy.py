#!/usr/bin/env python3
"""
Judas Swing (London Opening Reversal) Backtesting Strategy

This strategy exploits false breakouts during the London opening session by:
1. Identifying Tokyo session range (19:00-00:00 previous day)
2. Detecting liquidity sweeps during London opening (02:00-03:30)
3. Finding Fair Value Gaps (FVGs) created during the sweep
4. Identifying reversal patterns (Hammer/Shooting Star)
5. Entering on FVG inversion with proper risk management
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class JudasSwingStrategy:
    """
    Implements the Judas Swing strategy for backtesting on 5-minute data.
    """
    
    def __init__(self, csv_path: str):
        """
        Initialize the strategy with CSV data.
        
        Args:
            csv_path: Path to the CSV file with 5-minute data
        """
        self.csv_path = csv_path
        self.df = None
        self.trades = []
        self.load_data()
        
    def load_data(self):
        """Load and parse CSV data with semicolon delimiter."""
        print(f"Loading data from {self.csv_path}...")
        
        # Load CSV with semicolon delimiter
        self.df = pd.read_csv(
            self.csv_path,
            sep=';',
            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
            skiprows=1
        )
        
        # Parse datetime (data is already in Chicago time UTC-6)
        self.df['Datetime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Set datetime as index
        self.df.set_index('Datetime', inplace=True)
        self.df.sort_index(inplace=True)
        
        # Extract time components
        self.df['Hour'] = self.df.index.hour
        self.df['Minute'] = self.df.index.minute
        self.df['Date_Only'] = self.df.index.date
        
        print(f"Loaded {len(self.df)} candles from {self.df.index[0]} to {self.df.index[-1]}")
        
    def identify_tokyo_session(self, date) -> Optional[Dict]:
        """
        Identify Tokyo session range (19:00 to 00:00 previous day).
        
        Args:
            date: The current date for which to find the previous day's Tokyo session
            
        Returns:
            Dictionary with Tokyo session high, low, and datetime range
        """
        # Tokyo session is on the previous day (n-1)
        prev_date = date - timedelta(days=1)
        
        # Get candles between 19:00 and 23:59:59 on previous day
        tokyo_candles = self.df[
            (self.df['Date_Only'] == prev_date) &
            (self.df['Hour'] >= 19)
        ]
        
        if len(tokyo_candles) == 0:
            return None
            
        tokyo_high = tokyo_candles['High'].max()
        tokyo_low = tokyo_candles['Low'].min()
        
        return {
            'high': tokyo_high,
            'low': tokyo_low,
            'start': tokyo_candles.index[0],
            'end': tokyo_candles.index[-1],
            'range': tokyo_high - tokyo_low
        }
    
    def detect_fvg(self, idx: int, direction: str) -> Optional[Dict]:
        """
        Detect Fair Value Gap at given index.
        
        Bullish FVG: Low[i] > High[i-2]
        Bearish FVG: High[i] < Low[i-2]
        
        Args:
            idx: Current index
            direction: 'bullish' or 'bearish'
            
        Returns:
            Dictionary with FVG details or None
        """
        if idx < 2:
            return None
            
        if direction == 'bullish':
            # Bullish FVG: gap between current low and high 2 candles ago
            if self.df.iloc[idx]['Low'] > self.df.iloc[idx-2]['High']:
                return {
                    'type': 'bullish',
                    'top': self.df.iloc[idx]['Low'],
                    'bottom': self.df.iloc[idx-2]['High'],
                    'index': idx,
                    'datetime': self.df.index[idx]
                }
        elif direction == 'bearish':
            # Bearish FVG: gap between current high and low 2 candles ago
            if self.df.iloc[idx]['High'] < self.df.iloc[idx-2]['Low']:
                return {
                    'type': 'bearish',
                    'top': self.df.iloc[idx-2]['Low'],
                    'bottom': self.df.iloc[idx]['High'],
                    'index': idx,
                    'datetime': self.df.index[idx]
                }
        
        return None
    
    def detect_liquidity_sweep(self, date, tokyo_session: Dict) -> Optional[Dict]:
        """
        Detect liquidity sweep during London opening (02:00-03:30).
        
        Args:
            date: Current date
            tokyo_session: Tokyo session data with high/low
            
        Returns:
            Dictionary with sweep details or None
        """
        # Get candles between 02:00 and 03:30 on current day
        london_candles = self.df[
            (self.df['Date_Only'] == date) &
            (self.df['Hour'] >= 2) &
            ((self.df['Hour'] < 3) | ((self.df['Hour'] == 3) & (self.df['Minute'] <= 30)))
        ]
        
        if len(london_candles) == 0:
            return None
        
        london_high = london_candles['High'].max()
        london_low = london_candles['Low'].min()
        
        # Check for sweep of Tokyo high (bearish sweep)
        if london_high > tokyo_session['high']:
            # Find FVGs created during the sweep (bearish FVGs)
            fvgs = []
            for i in range(2, len(london_candles)):
                idx = london_candles.index[i]
                loc_result = self.df.index.get_loc(idx)
                # Handle case where get_loc returns a slice
                if isinstance(loc_result, slice):
                    actual_idx = loc_result.start
                else:
                    actual_idx = loc_result
                fvg = self.detect_fvg(actual_idx, 'bearish')
                if fvg:
                    fvgs.append(fvg)
            
            if fvgs:
                return {
                    'direction': 'bearish',
                    'swept_level': tokyo_session['high'],
                    'sweep_high': london_high,
                    'fvgs': fvgs,
                    'candles': london_candles
                }
        
        # Check for sweep of Tokyo low (bullish sweep)
        if london_low < tokyo_session['low']:
            # Find FVGs created during the sweep (bullish FVGs)
            fvgs = []
            for i in range(2, len(london_candles)):
                idx = london_candles.index[i]
                loc_result = self.df.index.get_loc(idx)
                # Handle case where get_loc returns a slice
                if isinstance(loc_result, slice):
                    actual_idx = loc_result.start
                else:
                    actual_idx = loc_result
                fvg = self.detect_fvg(actual_idx, 'bullish')
                if fvg:
                    fvgs.append(fvg)
            
            if fvgs:
                return {
                    'direction': 'bullish',
                    'swept_level': tokyo_session['low'],
                    'sweep_low': london_low,
                    'fvgs': fvgs,
                    'candles': london_candles
                }
        
        return None
    
    def detect_reversal_pattern(self, candle: pd.Series, direction: str) -> bool:
        """
        Detect Hammer (bullish) or Shooting Star (bearish) pattern.
        
        Criteria:
        - Body in top/bottom 30% of range
        - Wick at least 2x body size
        - Opposite wick < 10% of range
        
        Args:
            candle: Candle data
            direction: 'bullish' (hammer) or 'bearish' (shooting star)
            
        Returns:
            True if pattern detected
        """
        open_price = candle['Open']
        high = candle['High']
        low = candle['Low']
        close = candle['Close']
        
        body_size = abs(close - open_price)
        total_range = high - low
        
        if total_range == 0:
            return False
        
        if direction == 'bullish':
            # Hammer: body at top, long lower wick
            body_top = max(open_price, close)
            body_bottom = min(open_price, close)
            
            lower_wick = body_bottom - low
            upper_wick = high - body_top
            
            # Body in top 30% of range
            if body_bottom < low + 0.7 * total_range:
                return False
            
            # Lower wick at least 2x body size
            if body_size > 0 and lower_wick < 2 * body_size:
                return False
            
            # Upper wick < 10% of range
            if upper_wick > 0.1 * total_range:
                return False
            
            return True
            
        elif direction == 'bearish':
            # Shooting Star: body at bottom, long upper wick
            body_top = max(open_price, close)
            body_bottom = min(open_price, close)
            
            lower_wick = body_bottom - low
            upper_wick = high - body_top
            
            # Body in bottom 30% of range
            if body_top > low + 0.3 * total_range:
                return False
            
            # Upper wick at least 2x body size
            if body_size > 0 and upper_wick < 2 * body_size:
                return False
            
            # Lower wick < 10% of range
            if lower_wick > 0.1 * total_range:
                return False
            
            return True
        
        return False
    
    def detect_fvg_inversion(self, start_idx: int, fvg: Dict, direction: str, 
                            max_candles: int = 20) -> Optional[Dict]:
        """
        Detect FVG inversion (candle fills and closes beyond FVG).
        
        Args:
            start_idx: Index to start looking from
            fvg: FVG dictionary with top/bottom
            direction: 'bullish' or 'bearish' for trade direction
            max_candles: Maximum candles to look ahead
            
        Returns:
            Dictionary with inversion details or None
        """
        for i in range(start_idx, min(start_idx + max_candles, len(self.df))):
            candle = self.df.iloc[i]
            
            if direction == 'bullish':
                # For long: need to fill bearish FVG and close above it
                # Candle should have low <= fvg bottom and close > fvg top
                if candle['Low'] <= fvg['bottom'] and candle['Close'] > fvg['top']:
                    return {
                        'index': i,
                        'datetime': self.df.index[i],
                        'close': candle['Close'],
                        'fvg_filled': fvg
                    }
            
            elif direction == 'bearish':
                # For short: need to fill bullish FVG and close below it
                # Candle should have high >= fvg top and close < fvg bottom
                if candle['High'] >= fvg['top'] and candle['Close'] < fvg['bottom']:
                    return {
                        'index': i,
                        'datetime': self.df.index[i],
                        'close': candle['Close'],
                        'fvg_filled': fvg
                    }
        
        return None
    
    def find_reversal_candle(self, sweep_data: Dict, tokyo_session: Dict) -> Optional[Dict]:
        """
        Find reversal candle (Hammer or Shooting Star) after sweep.
        
        Args:
            sweep_data: Sweep detection data
            tokyo_session: Tokyo session data
            
        Returns:
            Dictionary with reversal candle details or None
        """
        direction = sweep_data['direction']
        candles = sweep_data['candles']
        
        # Look for reversal pattern in the sweep candles and shortly after
        last_sweep_idx = self.df.index.get_loc(candles.index[-1])
        
        # Check up to 10 candles after the sweep window
        for i in range(last_sweep_idx - len(candles), last_sweep_idx + 10):
            if i < 0 or i >= len(self.df):
                continue
            
            candle = self.df.iloc[i]
            
            # For bullish reversal (swept low), look for hammer
            if direction == 'bullish' and self.detect_reversal_pattern(candle, 'bullish'):
                # Hammer should be near the swept low
                if candle['Low'] <= tokyo_session['low'] + (tokyo_session['range'] * 0.2):
                    loc_result = self.df.index.get_loc(self.df.index[i])
                    actual_idx = loc_result.start if isinstance(loc_result, slice) else loc_result
                    return {
                        'index': actual_idx,
                        'datetime': self.df.index[i],
                        'type': 'hammer',
                        'high': candle['High'],
                        'low': candle['Low'],
                        'open': candle['Open'],
                        'close': candle['Close']
                    }
            
            # For bearish reversal (swept high), look for shooting star
            elif direction == 'bearish' and self.detect_reversal_pattern(candle, 'bearish'):
                # Shooting star should be near the swept high
                if candle['High'] >= tokyo_session['high'] - (tokyo_session['range'] * 0.2):
                    loc_result = self.df.index.get_loc(self.df.index[i])
                    actual_idx = loc_result.start if isinstance(loc_result, slice) else loc_result
                    return {
                        'index': actual_idx,
                        'datetime': self.df.index[i],
                        'type': 'shooting_star',
                        'high': candle['High'],
                        'low': candle['Low'],
                        'open': candle['Open'],
                        'close': candle['Close']
                    }
        
        return None
    
    def calculate_stop_loss(self, reversal_candle: Dict, fvg: Dict, 
                           direction: str) -> Tuple[float, float]:
        """
        Calculate both stop loss strategies.
        
        Args:
            reversal_candle: Reversal candle data
            fvg: FVG that was inverted
            direction: Trade direction
            
        Returns:
            Tuple of (SL1_aggressive, SL2_conservative)
        """
        if direction == 'bullish':
            # SL1: 1 point below inverted FVG bottom
            sl1 = fvg['bottom'] - 1.0
            
            # SL2: 1 point below hammer's low wick
            sl2 = reversal_candle['low'] - 1.0
            
        else:  # bearish
            # SL1: 1 point above inverted FVG top
            sl1 = fvg['top'] + 1.0
            
            # SL2: 1 point above shooting star's high wick
            sl2 = reversal_candle['high'] + 1.0
        
        return sl1, sl2
    
    def simulate_trade(self, entry_idx: int, entry_price: float, direction: str,
                      sl1: float, sl2: float, tokyo_session: Dict,
                      reversal_candle: Dict, sweep_data: Dict, fvg: Dict,
                      rr_ratios: List[float] = [2.0, 3.0, 3.5]) -> Dict:
        """
        Simulate trade execution and track multiple outcomes.
        
        Args:
            entry_idx: Entry candle index
            entry_price: Entry price
            direction: Trade direction
            sl1: Aggressive stop loss
            sl2: Conservative stop loss
            tokyo_session: Tokyo session data
            reversal_candle: Reversal candle data
            sweep_data: Sweep data
            fvg: FVG data
            rr_ratios: Risk-reward ratios to test
            
        Returns:
            Dictionary with trade results
        """
        if direction == 'bullish':
            target = tokyo_session['high']
        else:
            target = tokyo_session['low']
        
        # Calculate risks for both SLs
        if direction == 'bullish':
            risk1 = entry_price - sl1
            risk2 = entry_price - sl2
            potential_reward = target - entry_price
        else:
            risk1 = sl1 - entry_price
            risk2 = sl2 - entry_price
            potential_reward = entry_price - target
        
        # Initialize results
        result = {
            'entry_datetime': self.df.index[entry_idx],
            'entry_price': entry_price,
            'direction': direction,
            'sl1': sl1,
            'sl2': sl2,
            'target': target,
            'risk1': risk1,
            'risk2': risk2,
            'potential_reward': potential_reward,
            'tokyo_high': tokyo_session['high'],
            'tokyo_low': tokyo_session['low'],
            'tokyo_range': tokyo_session['range'],
            'swept_level': sweep_data['swept_level'],
            'reversal_type': reversal_candle['type'],
            'fvg_top': fvg['top'],
            'fvg_bottom': fvg['bottom'],
            'sl1_hit': False,
            'sl2_hit': False,
            'target_hit': False,
            'sl1_exit_datetime': None,
            'sl2_exit_datetime': None,
            'target_exit_datetime': None,
            'sl1_pnl': 0,
            'sl2_pnl': 0,
            'max_favorable_excursion': 0,
            'max_adverse_excursion': 0,
            'candles_to_resolution': 0,
            'reversal_speed': 0
        }
        
        # Add RR-based targets
        for rr in rr_ratios:
            result[f'tp_rr{rr}'] = None
            result[f'tp_rr{rr}_hit_sl1'] = False
            result[f'tp_rr{rr}_hit_sl2'] = False
            result[f'tp_rr{rr}_datetime_sl1'] = None
            result[f'tp_rr{rr}_datetime_sl2'] = None
        
        # Simulate forward from entry
        max_forward_candles = 100
        sl1_active = True
        sl2_active = True
        
        for i in range(entry_idx + 1, min(entry_idx + max_forward_candles, len(self.df))):
            candle = self.df.iloc[i]
            result['candles_to_resolution'] += 1
            
            # Track excursions
            if direction == 'bullish':
                favorable = candle['High'] - entry_price
                adverse = entry_price - candle['Low']
                
                # Check SL1 hit
                if sl1_active and candle['Low'] <= sl1:
                    result['sl1_hit'] = True
                    result['sl1_exit_datetime'] = self.df.index[i]
                    result['sl1_pnl'] = -risk1
                    sl1_active = False
                
                # Check SL2 hit
                if sl2_active and candle['Low'] <= sl2:
                    result['sl2_hit'] = True
                    result['sl2_exit_datetime'] = self.df.index[i]
                    result['sl2_pnl'] = -risk2
                    sl2_active = False
                
                # Check target hit
                if candle['High'] >= target:
                    if not result['target_hit']:
                        result['target_hit'] = True
                        result['target_exit_datetime'] = self.df.index[i]
                        if sl1_active:
                            result['sl1_pnl'] = potential_reward
                        if sl2_active:
                            result['sl2_pnl'] = potential_reward
                
                # Check RR targets
                for rr in rr_ratios:
                    tp1 = entry_price + (risk1 * rr)
                    tp2 = entry_price + (risk2 * rr)
                    
                    if sl1_active and not result[f'tp_rr{rr}_hit_sl1'] and candle['High'] >= tp1:
                        result[f'tp_rr{rr}_hit_sl1'] = True
                        result[f'tp_rr{rr}_datetime_sl1'] = self.df.index[i]
                    
                    if sl2_active and not result[f'tp_rr{rr}_hit_sl2'] and candle['High'] >= tp2:
                        result[f'tp_rr{rr}_hit_sl2'] = True
                        result[f'tp_rr{rr}_datetime_sl2'] = self.df.index[i]
                
            else:  # bearish
                favorable = entry_price - candle['Low']
                adverse = candle['High'] - entry_price
                
                # Check SL1 hit
                if sl1_active and candle['High'] >= sl1:
                    result['sl1_hit'] = True
                    result['sl1_exit_datetime'] = self.df.index[i]
                    result['sl1_pnl'] = -risk1
                    sl1_active = False
                
                # Check SL2 hit
                if sl2_active and candle['High'] >= sl2:
                    result['sl2_hit'] = True
                    result['sl2_exit_datetime'] = self.df.index[i]
                    result['sl2_pnl'] = -risk2
                    sl2_active = False
                
                # Check target hit
                if candle['Low'] <= target:
                    if not result['target_hit']:
                        result['target_hit'] = True
                        result['target_exit_datetime'] = self.df.index[i]
                        if sl1_active:
                            result['sl1_pnl'] = potential_reward
                        if sl2_active:
                            result['sl2_pnl'] = potential_reward
                
                # Check RR targets
                for rr in rr_ratios:
                    tp1 = entry_price - (risk1 * rr)
                    tp2 = entry_price - (risk2 * rr)
                    
                    if sl1_active and not result[f'tp_rr{rr}_hit_sl1'] and candle['Low'] <= tp1:
                        result[f'tp_rr{rr}_hit_sl1'] = True
                        result[f'tp_rr{rr}_datetime_sl1'] = self.df.index[i]
                    
                    if sl2_active and not result[f'tp_rr{rr}_hit_sl2'] and candle['Low'] <= tp2:
                        result[f'tp_rr{rr}_hit_sl2'] = True
                        result[f'tp_rr{rr}_datetime_sl2'] = self.df.index[i]
            
            result['max_favorable_excursion'] = max(result['max_favorable_excursion'], favorable)
            result['max_adverse_excursion'] = max(result['max_adverse_excursion'], adverse)
            
            # If both SLs hit, stop simulation
            if not sl1_active and not sl2_active:
                break
        
        # Calculate reversal speed (favorable excursion per candle)
        if result['candles_to_resolution'] > 0:
            result['reversal_speed'] = result['max_favorable_excursion'] / result['candles_to_resolution']
        
        return result
    
    def run_backtest(self):
        """
        Run the complete backtest on the loaded data.
        """
        print("\n" + "="*80)
        print("STARTING JUDAS SWING BACKTEST")
        print("="*80 + "\n")
        
        # Get unique dates
        unique_dates = sorted(self.df['Date_Only'].unique())
        
        setups_found = 0
        trades_executed = 0
        
        for i, date in enumerate(unique_dates):
            # Skip first day (need previous day for Tokyo session)
            if i == 0:
                continue
            
            # Get Tokyo session from previous day
            tokyo_session = self.identify_tokyo_session(date)
            if not tokyo_session:
                continue
            
            # Check for liquidity sweep during London opening
            sweep = self.detect_liquidity_sweep(date, tokyo_session)
            if not sweep or not sweep['fvgs']:
                continue
            
            setups_found += 1
            
            # Find reversal candle
            reversal_candle = self.find_reversal_candle(sweep, tokyo_session)
            if not reversal_candle:
                continue
            
            # For each FVG created during sweep, check for inversion
            for fvg in sweep['fvgs']:
                # Start looking after reversal candle
                start_idx = reversal_candle['index'] + 1
                
                # Detect FVG inversion
                inversion = self.detect_fvg_inversion(
                    start_idx, 
                    fvg, 
                    sweep['direction']
                )
                
                if not inversion:
                    continue
                
                # Calculate stop losses
                sl1, sl2 = self.calculate_stop_loss(
                    reversal_candle,
                    fvg,
                    sweep['direction']
                )
                
                # Entry at close of inversion candle
                entry_idx = inversion['index']
                entry_price = inversion['close']
                
                # Simulate trade
                trade_result = self.simulate_trade(
                    entry_idx=entry_idx,
                    entry_price=entry_price,
                    direction=sweep['direction'],
                    sl1=sl1,
                    sl2=sl2,
                    tokyo_session=tokyo_session,
                    reversal_candle=reversal_candle,
                    sweep_data=sweep,
                    fvg=fvg
                )
                
                self.trades.append(trade_result)
                trades_executed += 1
                
                # Only take first valid FVG inversion per setup
                break
        
        print(f"\nBacktest Complete!")
        print(f"Setups found (sweep + FVG): {setups_found}")
        print(f"Trades executed (with reversal + inversion): {trades_executed}")
    
    def analyze_results(self) -> Dict:
        """
        Analyze backtest results and generate comprehensive statistics.
        
        Returns:
            Dictionary with detailed analysis
        """
        if not self.trades:
            return {"error": "No trades to analyze"}
        
        analysis = {
            'total_trades': len(self.trades),
            'long_trades': sum(1 for t in self.trades if t['direction'] == 'bullish'),
            'short_trades': sum(1 for t in self.trades if t['direction'] == 'bearish'),
        }
        
        # Analyze SL1 (Aggressive)
        sl1_wins = [t for t in self.trades if t['sl1_pnl'] > 0]
        sl1_losses = [t for t in self.trades if t['sl1_pnl'] < 0]
        
        analysis['sl1_aggressive'] = {
            'wins': len(sl1_wins),
            'losses': len(sl1_losses),
            'win_rate': len(sl1_wins) / len(self.trades) * 100 if self.trades else 0,
            'avg_win': np.mean([t['sl1_pnl'] for t in sl1_wins]) if sl1_wins else 0,
            'avg_loss': np.mean([t['sl1_pnl'] for t in sl1_losses]) if sl1_losses else 0,
            'total_pnl': sum(t['sl1_pnl'] for t in self.trades),
            'avg_risk': np.mean([t['risk1'] for t in self.trades]),
            'premature_stops': sum(1 for t in self.trades if t['sl1_hit'] and t['target_hit'])
        }
        
        if analysis['sl1_aggressive']['avg_loss'] != 0:
            analysis['sl1_aggressive']['profit_factor'] = (
                abs(analysis['sl1_aggressive']['avg_win'] * len(sl1_wins)) /
                abs(analysis['sl1_aggressive']['avg_loss'] * len(sl1_losses))
                if sl1_losses else float('inf')
            )
            analysis['sl1_aggressive']['expectancy'] = (
                analysis['sl1_aggressive']['win_rate'] / 100 * analysis['sl1_aggressive']['avg_win'] +
                (1 - analysis['sl1_aggressive']['win_rate'] / 100) * analysis['sl1_aggressive']['avg_loss']
            )
        else:
            analysis['sl1_aggressive']['profit_factor'] = float('inf')
            analysis['sl1_aggressive']['expectancy'] = analysis['sl1_aggressive']['avg_win']
        
        # Analyze SL2 (Conservative)
        sl2_wins = [t for t in self.trades if t['sl2_pnl'] > 0]
        sl2_losses = [t for t in self.trades if t['sl2_pnl'] < 0]
        
        analysis['sl2_conservative'] = {
            'wins': len(sl2_wins),
            'losses': len(sl2_losses),
            'win_rate': len(sl2_wins) / len(self.trades) * 100 if self.trades else 0,
            'avg_win': np.mean([t['sl2_pnl'] for t in sl2_wins]) if sl2_wins else 0,
            'avg_loss': np.mean([t['sl2_pnl'] for t in sl2_losses]) if sl2_losses else 0,
            'total_pnl': sum(t['sl2_pnl'] for t in self.trades),
            'avg_risk': np.mean([t['risk2'] for t in self.trades]),
            'premature_stops': sum(1 for t in self.trades if t['sl2_hit'] and t['target_hit'])
        }
        
        if analysis['sl2_conservative']['avg_loss'] != 0:
            analysis['sl2_conservative']['profit_factor'] = (
                abs(analysis['sl2_conservative']['avg_win'] * len(sl2_wins)) /
                abs(analysis['sl2_conservative']['avg_loss'] * len(sl2_losses))
                if sl2_losses else float('inf')
            )
            analysis['sl2_conservative']['expectancy'] = (
                analysis['sl2_conservative']['win_rate'] / 100 * analysis['sl2_conservative']['avg_win'] +
                (1 - analysis['sl2_conservative']['win_rate'] / 100) * analysis['sl2_conservative']['avg_loss']
            )
        else:
            analysis['sl2_conservative']['profit_factor'] = float('inf')
            analysis['sl2_conservative']['expectancy'] = analysis['sl2_conservative']['avg_win']
        
        # Analyze RR ratios
        rr_ratios = [2.0, 3.0, 3.5]
        analysis['rr_analysis'] = {}
        
        for rr in rr_ratios:
            sl1_hits = sum(1 for t in self.trades if t[f'tp_rr{rr}_hit_sl1'])
            sl2_hits = sum(1 for t in self.trades if t[f'tp_rr{rr}_hit_sl2'])
            
            analysis['rr_analysis'][f'rr_{rr}'] = {
                'sl1_success_rate': sl1_hits / len(self.trades) * 100 if self.trades else 0,
                'sl2_success_rate': sl2_hits / len(self.trades) * 100 if self.trades else 0,
                'sl1_hits': sl1_hits,
                'sl2_hits': sl2_hits
            }
        
        # Target analysis
        analysis['target_analysis'] = {
            'target_hit_rate': sum(1 for t in self.trades if t['target_hit']) / len(self.trades) * 100,
            'avg_candles_to_resolution': np.mean([t['candles_to_resolution'] for t in self.trades]),
            'avg_reversal_speed': np.mean([t['reversal_speed'] for t in self.trades]),
            'avg_favorable_excursion': np.mean([t['max_favorable_excursion'] for t in self.trades]),
            'avg_adverse_excursion': np.mean([t['max_adverse_excursion'] for t in self.trades])
        }
        
        # Psychology insights
        analysis['psychology_insights'] = {
            'fvg_inversion_benefit': (
                "FVG inversion entry waits for price to confirm the reversal by filling "
                "the gap created during the sweep. This reduces false entries compared to "
                "entering directly on the reversal pattern, as it requires price to show "
                "actual commitment to the reversal direction."
            ),
            'premature_sl1_stops': analysis['sl1_aggressive']['premature_stops'],
            'premature_sl2_stops': analysis['sl2_conservative']['premature_stops'],
            'stop_loss_recommendation': (
                "SL2 (conservative)" if analysis['sl2_conservative']['win_rate'] > 
                analysis['sl1_aggressive']['win_rate'] else "SL1 (aggressive)"
            )
        }
        
        return analysis
    
    def save_results(self, output_file: str = 'judas_swing_results.json'):
        """
        Save backtest results and analysis to file.
        
        Args:
            output_file: Path to output file
        """
        analysis = self.analyze_results()
        
        # Convert datetime objects to strings for JSON serialization
        trades_serializable = []
        for trade in self.trades:
            trade_copy = trade.copy()
            for key, value in trade_copy.items():
                if isinstance(value, (pd.Timestamp, datetime)):
                    trade_copy[key] = str(value)
                elif isinstance(value, (np.integer, np.floating)):
                    trade_copy[key] = float(value)
            trades_serializable.append(trade_copy)
        
        output = {
            'strategy': 'Judas Swing (London Opening Reversal)',
            'data_file': self.csv_path,
            'backtest_period': {
                'start': str(self.df.index[0]),
                'end': str(self.df.index[-1])
            },
            'analysis': analysis,
            'trades': trades_serializable
        }
        
        # Save to JSON
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2, default=str)
        
        print(f"\nResults saved to {output_file}")
        
        # Also create a human-readable report
        report_file = output_file.replace('.json', '_report.txt')
        self.generate_report(analysis, report_file)
    
    def generate_report(self, analysis: Dict, report_file: str):
        """
        Generate human-readable report.
        
        Args:
            analysis: Analysis dictionary
            report_file: Path to report file
        """
        with open(report_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("JUDAS SWING (LONDON OPENING REVERSAL) BACKTEST REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Data File: {self.csv_path}\n")
            f.write(f"Period: {self.df.index[0]} to {self.df.index[-1]}\n")
            f.write(f"Total Trades: {analysis['total_trades']}\n")
            f.write(f"Long Trades: {analysis['long_trades']}\n")
            f.write(f"Short Trades: {analysis['short_trades']}\n\n")
            
            # SL1 Analysis
            f.write("-"*80 + "\n")
            f.write("SL1 (AGGRESSIVE - FVG Based)\n")
            f.write("-"*80 + "\n")
            sl1 = analysis['sl1_aggressive']
            f.write(f"Win Rate: {sl1['win_rate']:.2f}%\n")
            f.write(f"Wins: {sl1['wins']} | Losses: {sl1['losses']}\n")
            f.write(f"Average Win: {sl1['avg_win']:.2f} points\n")
            f.write(f"Average Loss: {sl1['avg_loss']:.2f} points\n")
            f.write(f"Total P&L: {sl1['total_pnl']:.2f} points\n")
            f.write(f"Profit Factor: {sl1['profit_factor']:.2f}\n")
            f.write(f"Expectancy: {sl1['expectancy']:.2f} points\n")
            f.write(f"Average Risk: {sl1['avg_risk']:.2f} points\n")
            f.write(f"Premature Stops (hit SL then target): {sl1['premature_stops']}\n\n")
            
            # SL2 Analysis
            f.write("-"*80 + "\n")
            f.write("SL2 (CONSERVATIVE - Pattern Wick Based)\n")
            f.write("-"*80 + "\n")
            sl2 = analysis['sl2_conservative']
            f.write(f"Win Rate: {sl2['win_rate']:.2f}%\n")
            f.write(f"Wins: {sl2['wins']} | Losses: {sl2['losses']}\n")
            f.write(f"Average Win: {sl2['avg_win']:.2f} points\n")
            f.write(f"Average Loss: {sl2['avg_loss']:.2f} points\n")
            f.write(f"Total P&L: {sl2['total_pnl']:.2f} points\n")
            f.write(f"Profit Factor: {sl2['profit_factor']:.2f}\n")
            f.write(f"Expectancy: {sl2['expectancy']:.2f} points\n")
            f.write(f"Average Risk: {sl2['avg_risk']:.2f} points\n")
            f.write(f"Premature Stops (hit SL then target): {sl2['premature_stops']}\n\n")
            
            # RR Analysis
            f.write("-"*80 + "\n")
            f.write("RISK:REWARD RATIO ANALYSIS\n")
            f.write("-"*80 + "\n")
            for rr_key, rr_data in analysis['rr_analysis'].items():
                rr = rr_key.replace('rr_', '')
                f.write(f"\n{rr}:1 Risk Reward Ratio:\n")
                f.write(f"  SL1 Success Rate: {rr_data['sl1_success_rate']:.2f}% ({rr_data['sl1_hits']} hits)\n")
                f.write(f"  SL2 Success Rate: {rr_data['sl2_success_rate']:.2f}% ({rr_data['sl2_hits']} hits)\n")
            
            # Target Analysis
            f.write("\n" + "-"*80 + "\n")
            f.write("TARGET ANALYSIS\n")
            f.write("-"*80 + "\n")
            target = analysis['target_analysis']
            f.write(f"Target Hit Rate: {target['target_hit_rate']:.2f}%\n")
            f.write(f"Average Candles to Resolution: {target['avg_candles_to_resolution']:.1f}\n")
            f.write(f"Average Reversal Speed: {target['avg_reversal_speed']:.2f} points/candle\n")
            f.write(f"Average Favorable Excursion: {target['avg_favorable_excursion']:.2f} points\n")
            f.write(f"Average Adverse Excursion: {target['avg_adverse_excursion']:.2f} points\n\n")
            
            # Psychology Insights
            f.write("-"*80 + "\n")
            f.write("PSYCHOLOGY & STRATEGY INSIGHTS\n")
            f.write("-"*80 + "\n")
            psych = analysis['psychology_insights']
            f.write(f"\nFVG Inversion Entry Benefit:\n{psych['fvg_inversion_benefit']}\n\n")
            f.write(f"Premature SL1 Stops: {psych['premature_sl1_stops']}\n")
            f.write(f"Premature SL2 Stops: {psych['premature_sl2_stops']}\n\n")
            f.write(f"Recommended Stop Loss: {psych['stop_loss_recommendation']}\n\n")
            
            # Key Findings
            f.write("-"*80 + "\n")
            f.write("KEY FINDINGS & ANSWERS\n")
            f.write("-"*80 + "\n\n")
            
            f.write("1. Win Rate Comparison:\n")
            f.write(f"   SL1 (Aggressive): {sl1['win_rate']:.2f}%\n")
            f.write(f"   SL2 (Conservative): {sl2['win_rate']:.2f}%\n")
            f.write(f"   Difference: {abs(sl1['win_rate'] - sl2['win_rate']):.2f}%\n\n")
            
            f.write("2. Premature Stop-Out Analysis:\n")
            f.write(f"   SL1 stopped out before real move: {sl1['premature_stops']} times ")
            f.write(f"({sl1['premature_stops']/analysis['total_trades']*100:.1f}%)\n")
            f.write(f"   SL2 stopped out before real move: {sl2['premature_stops']} times ")
            f.write(f"({sl2['premature_stops']/analysis['total_trades']*100:.1f}%)\n\n")
            
            f.write("3. Reversal Speed/Violence:\n")
            f.write(f"   Average: {target['avg_reversal_speed']:.2f} points per 5-minute candle\n")
            f.write(f"   Average time to resolution: {target['avg_candles_to_resolution']:.1f} candles ")
            f.write(f"({target['avg_candles_to_resolution']*5:.0f} minutes)\n\n")
            
            f.write("4. Tokyo Extreme Target Success:\n")
            f.write(f"   Target hit rate: {target['target_hit_rate']:.2f}%\n\n")
            
            f.write("5. Optimal RR Ratio:\n")
            best_rr_sl1 = max(analysis['rr_analysis'].items(), 
                             key=lambda x: x[1]['sl1_success_rate'])
            best_rr_sl2 = max(analysis['rr_analysis'].items(), 
                             key=lambda x: x[1]['sl2_success_rate'])
            f.write(f"   For SL1: {best_rr_sl1[0].replace('rr_', '')}:1 ")
            f.write(f"({best_rr_sl1[1]['sl1_success_rate']:.2f}% success)\n")
            f.write(f"   For SL2: {best_rr_sl2[0].replace('rr_', '')}:1 ")
            f.write(f"({best_rr_sl2[1]['sl2_success_rate']:.2f}% success)\n\n")
            
            f.write("-"*80 + "\n")
            f.write("CONCLUSION\n")
            f.write("-"*80 + "\n\n")
            
            if sl2['win_rate'] > sl1['win_rate']:
                f.write("The CONSERVATIVE stop loss (SL2) based on the reversal pattern's extreme wick\n")
                f.write("performs better than the aggressive FVG-based stop (SL1). This suggests that\n")
                f.write("the tight stops get hit prematurely during volatility before the real move.\n\n")
            else:
                f.write("The AGGRESSIVE stop loss (SL1) based on the FVG performs better, suggesting\n")
                f.write("that the tighter risk management is viable for this setup.\n\n")
            
            f.write(f"Overall expectancy with recommended SL: ")
            f.write(f"{max(sl1['expectancy'], sl2['expectancy']):.2f} points per trade\n")
        
        print(f"Report saved to {report_file}")


def main():
    """Main execution function."""
    import sys
    
    # Default files
    nq_file = '/home/runner/work/Backtest-Trading/Backtest-Trading/2024 5m.csv'
    es_file = '/home/runner/work/Backtest-Trading/Backtest-Trading/ES 5m (2024-2025).csv'
    
    print("\n" + "="*80)
    print("JUDAS SWING STRATEGY BACKTESTER")
    print("="*80)
    
    # Backtest NQ
    print(f"\n{'='*80}")
    print("BACKTESTING NQ (2024)")
    print(f"{'='*80}\n")
    
    nq_strategy = JudasSwingStrategy(nq_file)
    nq_strategy.run_backtest()
    nq_strategy.save_results('judas_swing_nq_2024_results.json')
    
    # Backtest ES
    print(f"\n\n{'='*80}")
    print("BACKTESTING ES (2024-2025)")
    print(f"{'='*80}\n")
    
    es_strategy = JudasSwingStrategy(es_file)
    es_strategy.run_backtest()
    es_strategy.save_results('judas_swing_es_2024_2025_results.json')
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE")
    print("="*80)
    print("\nResults saved:")
    print("  - judas_swing_nq_2024_results.json")
    print("  - judas_swing_nq_2024_results_report.txt")
    print("  - judas_swing_es_2024_2025_results.json")
    print("  - judas_swing_es_2024_2025_results_report.txt")
    print("\n")


if __name__ == "__main__":
    main()
