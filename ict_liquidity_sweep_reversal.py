#!/usr/bin/env python3
"""
ICT Liquidity Sweep Reversal Strategy
======================================

Analyzes NQ (Nasdaq Futures) and ES (S&P 500 Futures) for high-probability 
reversal setups based on ICT (Inner Circle Trader) methodology.

Strategy focuses on:
1. Time & Killzones (London Open 2am-5am, NY Open 9:30am-11am NY time)
2. Liquidity Sweeps (price exceeds Swing High/Low)
3. Sweep Quality Analysis (wick rejection vs full body)
4. SMT Divergence (Smart Money Tool - NQ vs ES divergence)
5. Displacement & Market Structure Shift
6. Fair Value Gap (FVG) detection

Author: ICT Strategy Implementation
Date: December 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
from typing import Dict, List, Tuple, Optional
import pytz


class ICTLiquiditySweepAnalyzer:
    """
    Analyzes price data for ICT Liquidity Sweep Reversal setups.
    """
    
    def __init__(self):
        """Initialize the analyzer with configuration parameters."""
        self.nq_data = {}  # Store multiple timeframes for NQ
        self.es_data = {}  # Store multiple timeframes for ES
        
        # ICT Configuration
        self.london_killzone = (time(2, 0), time(5, 0))  # 2am-5am NY time
        self.ny_killzone = (time(9, 30), time(11, 0))    # 9:30am-11am NY time
        
        # Swing detection parameters
        self.swing_lookback_15m = 20  # bars to look back for 15m swings
        self.swing_lookback_1h = 10   # bars to look back for 1h swings
        
        # SMT divergence tolerance
        self.smt_tolerance = 0.002  # 0.2% for double top/bottom detection
        
        # Displacement parameters
        self.min_displacement_pct = 0.003  # 0.3% minimum body size for displacement
        
        # FVG parameters
        self.fvg_lookback = 60  # bars to look back for FVG zones
        
    def load_data(self, year: int = 2024) -> None:
        """
        Load NQ and ES data for multiple timeframes.
        
        Args:
            year: Year to load data for (default 2024)
        """
        print(f"\n{'='*80}")
        print(f"Loading data for year {year}...")
        print(f"{'='*80}\n")
        
        # Load NQ data (Nasdaq Futures)
        timeframes = ['1m', '5m', '15m', '1h']
        
        for tf in timeframes:
            try:
                if tf == '1h':
                    filename = f"{year} 1H.csv"
                else:
                    filename = f"{year} {tf}.csv"
                
                df = pd.read_csv(
                    filename,
                    sep=';',
                    names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'],
                    skiprows=1
                )
                
                # Combine date and time into datetime
                df['datetime'] = pd.to_datetime(
                    df['date'] + ' ' + df['time'],
                    format='%d/%m/%Y %H:%M:%S'
                )
                
                # Convert to NY timezone
                df['datetime'] = df['datetime'].dt.tz_localize('America/New_York', ambiguous='infer')
                
                # Convert price columns to float
                for col in ['open', 'high', 'low', 'close']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                df = df.dropna()
                df = df.sort_values('datetime').reset_index(drop=True)
                
                self.nq_data[tf] = df
                print(f"✓ Loaded NQ {tf}: {len(df)} candles")
                
            except FileNotFoundError:
                print(f"✗ File not found: {filename}")
            except Exception as e:
                print(f"✗ Error loading NQ {tf}: {e}")
        
        # Load ES data (S&P 500 Futures)
        try:
            # ES uses different file naming
            if year >= 2024:
                es_filename = f"ES 5m (2024-2025).csv"
            elif year >= 2021:
                es_filename = f"ES 5m (2021-2023).csv"
            else:
                es_filename = f"ES 5m (2018-2020).csv"
            
            df_es = pd.read_csv(
                es_filename,
                sep=';',
                names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'],
                skiprows=1
            )
            
            df_es['datetime'] = pd.to_datetime(
                df_es['date'] + ' ' + df_es['time'],
                format='%d/%m/%Y %H:%M:%S'
            )
            
            df_es['datetime'] = df_es['datetime'].dt.tz_localize('America/New_York', ambiguous='infer')
            
            for col in ['open', 'high', 'low', 'close']:
                df_es[col] = pd.to_numeric(df_es[col], errors='coerce')
            
            df_es = df_es.dropna()
            df_es = df_es.sort_values('datetime').reset_index(drop=True)
            
            # Filter to the specific year
            df_es = df_es[df_es['datetime'].dt.year == year].reset_index(drop=True)
            
            self.es_data['5m'] = df_es
            print(f"✓ Loaded ES 5m: {len(df_es)} candles")
            
        except Exception as e:
            print(f"✗ Error loading ES data: {e}")
        
        print(f"\n{'='*80}\n")
    
    def is_in_killzone(self, dt: datetime) -> Tuple[bool, str]:
        """
        Check if datetime is within London or NY killzone.
        
        Args:
            dt: Datetime to check
            
        Returns:
            Tuple of (is_in_killzone, killzone_name)
        """
        t = dt.time()
        
        # London Killzone: 2am-5am NY time
        if self.london_killzone[0] <= t <= self.london_killzone[1]:
            return True, "London Open"
        
        # NY Killzone: 9:30am-11am NY time
        if self.ny_killzone[0] <= t <= self.ny_killzone[1]:
            return True, "NY Open"
        
        return False, ""
    
    def detect_swing_points(self, df: pd.DataFrame, lookback: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect swing highs and swing lows using vectorized operations.
        
        Args:
            df: DataFrame with OHLC data
            lookback: Number of bars to look back/forward
            
        Returns:
            Tuple of (swing_highs, swing_lows) as boolean arrays
        """
        highs = df['high'].values
        lows = df['low'].values
        n = len(df)
        
        swing_highs = np.zeros(n, dtype=bool)
        swing_lows = np.zeros(n, dtype=bool)
        
        # Detect swing highs (local maxima)
        for i in range(lookback, n - lookback):
            if highs[i] == np.max(highs[i-lookback:i+lookback+1]):
                swing_highs[i] = True
        
        # Detect swing lows (local minima)
        for i in range(lookback, n - lookback):
            if lows[i] == np.min(lows[i-lookback:i+lookback+1]):
                swing_lows[i] = True
        
        return swing_highs, swing_lows
    
    def detect_liquidity_sweep(self, df: pd.DataFrame, idx: int, 
                               swing_highs: np.ndarray, swing_lows: np.ndarray) -> Optional[Dict]:
        """
        Detect if current candle sweeps liquidity (exceeds previous swing high/low).
        
        Args:
            df: DataFrame with OHLC data
            idx: Current candle index
            swing_highs: Boolean array of swing high locations
            swing_lows: Boolean array of swing low locations
            
        Returns:
            Dictionary with sweep details or None
        """
        if idx < 20:  # Need history
            return None
        
        current_high = df.loc[idx, 'high']
        current_low = df.loc[idx, 'low']
        
        # Find previous swing highs and lows
        prev_swing_highs = df.loc[:idx-1][swing_highs[:idx]]['high'].values
        prev_swing_lows = df.loc[:idx-1][swing_lows[:idx]]['low'].values
        
        if len(prev_swing_highs) == 0 and len(prev_swing_lows) == 0:
            return None
        
        # Check for Buy Side Liquidity Sweep (sweep above previous swing high)
        if len(prev_swing_highs) > 0:
            recent_swing_high = prev_swing_highs[-1]
            if current_high > recent_swing_high:
                return {
                    'type': 'Buy Side Liquidity',
                    'sweep_level': recent_swing_high,
                    'sweep_high': current_high,
                    'sweep_low': current_low,
                    'direction': 'bearish_reversal'  # Expecting price to reverse down
                }
        
        # Check for Sell Side Liquidity Sweep (sweep below previous swing low)
        if len(prev_swing_lows) > 0:
            recent_swing_low = prev_swing_lows[-1]
            if current_low < recent_swing_low:
                return {
                    'type': 'Sell Side Liquidity',
                    'sweep_level': recent_swing_low,
                    'sweep_high': current_high,
                    'sweep_low': current_low,
                    'direction': 'bullish_reversal'  # Expecting price to reverse up
                }
        
        return None
    
    def analyze_sweep_quality(self, row: pd.Series, sweep_info: Dict) -> Dict:
        """
        Analyze the quality of the liquidity sweep candle.
        
        Args:
            row: Candle that performed the sweep
            sweep_info: Sweep information dictionary
            
        Returns:
            Dictionary with quality metrics
        """
        open_price = row['open']
        close_price = row['close']
        high = row['high']
        low = row['low']
        
        body_size = abs(close_price - open_price)
        total_range = high - low
        
        if total_range == 0:
            return {'quality': 'Poor', 'type': 'Doji', 'score': 0}
        
        body_ratio = body_size / total_range
        
        if sweep_info['type'] == 'Buy Side Liquidity':
            # For bearish reversal, we want upper wick (rejection)
            upper_wick = high - max(open_price, close_price)
            wick_ratio = upper_wick / total_range
            
            if wick_ratio > 0.6:
                return {
                    'quality': 'Excellent',
                    'type': 'Strong Rejection Wick',
                    'score': 3,
                    'wick_ratio': wick_ratio,
                    'body_ratio': body_ratio
                }
            elif wick_ratio > 0.4:
                return {
                    'quality': 'Good',
                    'type': 'Rejection Wick',
                    'score': 2,
                    'wick_ratio': wick_ratio,
                    'body_ratio': body_ratio
                }
            else:
                return {
                    'quality': 'Poor',
                    'type': 'Full Body Breakout',
                    'score': 1,
                    'wick_ratio': wick_ratio,
                    'body_ratio': body_ratio
                }
        
        else:  # Sell Side Liquidity
            # For bullish reversal, we want lower wick (rejection)
            lower_wick = min(open_price, close_price) - low
            wick_ratio = lower_wick / total_range
            
            if wick_ratio > 0.6:
                return {
                    'quality': 'Excellent',
                    'type': 'Strong Rejection Wick',
                    'score': 3,
                    'wick_ratio': wick_ratio,
                    'body_ratio': body_ratio
                }
            elif wick_ratio > 0.4:
                return {
                    'quality': 'Good',
                    'type': 'Rejection Wick',
                    'score': 2,
                    'wick_ratio': wick_ratio,
                    'body_ratio': body_ratio
                }
            else:
                return {
                    'quality': 'Poor',
                    'type': 'Full Body Breakout',
                    'score': 1,
                    'wick_ratio': wick_ratio,
                    'body_ratio': body_ratio
                }
    
    def check_smt_divergence(self, nq_dt: datetime, nq_price: float, 
                            sweep_type: str) -> Dict:
        """
        Check for SMT (Smart Money Tool) divergence between NQ and ES.
        
        Args:
            nq_dt: Datetime of NQ sweep
            nq_price: Price level of NQ
            sweep_type: 'Buy Side Liquidity' or 'Sell Side Liquidity'
            
        Returns:
            Dictionary with SMT analysis
        """
        if '5m' not in self.es_data:
            return {'has_smt': False, 'reason': 'ES data not available'}
        
        df_es = self.es_data['5m']
        
        # Find ES data around the same time (within 10 minutes)
        time_window = timedelta(minutes=10)
        es_window = df_es[
            (df_es['datetime'] >= nq_dt - time_window) &
            (df_es['datetime'] <= nq_dt + time_window)
        ]
        
        if len(es_window) == 0:
            return {'has_smt': False, 'reason': 'No ES data in time window'}
        
        # Get ES price at similar time
        es_idx = (es_window['datetime'] - nq_dt).abs().argmin()
        es_current = es_window.iloc[es_idx]
        
        # Look back 60 minutes to find previous high/low
        lookback_time = nq_dt - timedelta(minutes=60)
        es_history = df_es[
            (df_es['datetime'] >= lookback_time) &
            (df_es['datetime'] < nq_dt)
        ]
        
        if len(es_history) < 5:
            return {'has_smt': False, 'reason': 'Insufficient ES history'}
        
        if sweep_type == 'Buy Side Liquidity':
            # NQ made Higher High, check if ES made Lower High or Double Top
            nq_direction = "Higher High"
            es_prev_high = es_history['high'].max()
            es_current_high = es_current['high']
            
            # Check for Lower High in ES
            if es_current_high < es_prev_high * (1 - self.smt_tolerance):
                return {
                    'has_smt': True,
                    'type': 'Bearish SMT Divergence',
                    'nq_direction': nq_direction,
                    'es_direction': 'Lower High',
                    'es_prev_high': es_prev_high,
                    'es_current_high': es_current_high,
                    'probability': 'High'
                }
            
            # Check for Double Top in ES
            elif abs(es_current_high - es_prev_high) / es_prev_high < self.smt_tolerance:
                return {
                    'has_smt': True,
                    'type': 'Bearish SMT Divergence (Double Top)',
                    'nq_direction': nq_direction,
                    'es_direction': 'Double Top',
                    'es_prev_high': es_prev_high,
                    'es_current_high': es_current_high,
                    'probability': 'Medium'
                }
        
        else:  # Sell Side Liquidity
            # NQ made Lower Low, check if ES made Higher Low or Double Bottom
            nq_direction = "Lower Low"
            es_prev_low = es_history['low'].min()
            es_current_low = es_current['low']
            
            # Check for Higher Low in ES
            if es_current_low > es_prev_low * (1 + self.smt_tolerance):
                return {
                    'has_smt': True,
                    'type': 'Bullish SMT Divergence',
                    'nq_direction': nq_direction,
                    'es_direction': 'Higher Low',
                    'es_prev_low': es_prev_low,
                    'es_current_low': es_current_low,
                    'probability': 'High'
                }
            
            # Check for Double Bottom in ES
            elif abs(es_current_low - es_prev_low) / es_prev_low < self.smt_tolerance:
                return {
                    'has_smt': True,
                    'type': 'Bullish SMT Divergence (Double Bottom)',
                    'nq_direction': nq_direction,
                    'es_direction': 'Double Bottom',
                    'es_prev_low': es_prev_low,
                    'es_current_low': es_current_low,
                    'probability': 'Medium'
                }
        
        return {'has_smt': False, 'reason': 'No divergence detected'}
    
    def detect_displacement_and_mss(self, df: pd.DataFrame, idx: int, 
                                    sweep_direction: str) -> Dict:
        """
        Detect displacement (impulsive move) and Market Structure Shift after sweep.
        
        Args:
            df: DataFrame with OHLC data
            idx: Index of sweep candle
            sweep_direction: 'bearish_reversal' or 'bullish_reversal'
            
        Returns:
            Dictionary with displacement and MSS analysis
        """
        if idx >= len(df) - 3:
            return {'has_displacement': False, 'reason': 'Not enough forward data'}
        
        # Look at next 3 candles for displacement
        displacement_found = False
        displacement_candle = None
        
        for i in range(1, 4):
            if idx + i >= len(df):
                break
            
            candle = df.iloc[idx + i]
            body_size = abs(candle['close'] - candle['open'])
            total_range = candle['high'] - candle['low']
            
            if total_range == 0:
                continue
            
            body_ratio = body_size / total_range
            price_change_pct = body_size / candle['open']
            
            # Check if this is an impulsive candle
            if body_ratio > 0.7 and price_change_pct > self.min_displacement_pct:
                # Check if direction matches expected reversal
                is_bearish = candle['close'] < candle['open']
                
                if sweep_direction == 'bearish_reversal' and is_bearish:
                    displacement_found = True
                    displacement_candle = i
                    break
                elif sweep_direction == 'bullish_reversal' and not is_bearish:
                    displacement_found = True
                    displacement_candle = i
                    break
        
        if not displacement_found:
            return {'has_displacement': False, 'reason': 'No impulsive move detected'}
        
        # Check for Market Structure Shift (break of previous structure)
        disp_idx = idx + displacement_candle
        disp_row = df.iloc[disp_idx]
        
        # Look at previous 10 candles to find structure
        lookback_start = max(0, idx - 10)
        previous_structure = df.iloc[lookback_start:idx]
        
        mss_detected = False
        
        if sweep_direction == 'bearish_reversal':
            # For bearish MSS, need to break below recent swing low
            if len(previous_structure) > 0:
                recent_low = previous_structure['low'].min()
                if disp_row['close'] < recent_low:
                    mss_detected = True
        else:  # bullish_reversal
            # For bullish MSS, need to break above recent swing high
            if len(previous_structure) > 0:
                recent_high = previous_structure['high'].max()
                if disp_row['close'] > recent_high:
                    mss_detected = True
        
        return {
            'has_displacement': True,
            'displacement_candle': displacement_candle,
            'has_mss': mss_detected,
            'strength': 'Strong' if mss_detected else 'Moderate'
        }
    
    def detect_fvg(self, df: pd.DataFrame, idx: int, sweep_direction: str) -> Dict:
        """
        Detect Fair Value Gap (FVG) left by the displacement move.
        
        Args:
            df: DataFrame with OHLC data
            idx: Index of sweep candle
            sweep_direction: 'bearish_reversal' or 'bullish_reversal'
            
        Returns:
            Dictionary with FVG analysis
        """
        if idx >= len(df) - 3:
            return {'has_fvg': False, 'reason': 'Not enough forward data'}
        
        # Look for FVG in next 5 candles
        for i in range(1, 6):
            if idx + i + 1 >= len(df):
                break
            
            # FVG pattern: gap between candle[i-1] and candle[i+1]
            # with candle[i] being the impulsive move
            
            if sweep_direction == 'bearish_reversal':
                # Bearish FVG: Low[i-1] > High[i+1]
                low_before = df.iloc[idx + i - 1]['low']
                high_after = df.iloc[idx + i + 1]['high']
                
                if low_before > high_after:
                    gap_size = low_before - high_after
                    gap_size_pct = gap_size / df.iloc[idx + i]['close'] * 100
                    
                    return {
                        'has_fvg': True,
                        'type': 'Bearish FVG',
                        'gap_top': low_before,
                        'gap_bottom': high_after,
                        'gap_size': gap_size,
                        'gap_size_pct': gap_size_pct,
                        'candles_after_sweep': i
                    }
            
            else:  # bullish_reversal
                # Bullish FVG: High[i-1] < Low[i+1]
                high_before = df.iloc[idx + i - 1]['high']
                low_after = df.iloc[idx + i + 1]['low']
                
                if high_before < low_after:
                    gap_size = low_after - high_before
                    gap_size_pct = gap_size / df.iloc[idx + i]['close'] * 100
                    
                    return {
                        'has_fvg': True,
                        'type': 'Bullish FVG',
                        'gap_bottom': high_before,
                        'gap_top': low_after,
                        'gap_size': gap_size,
                        'gap_size_pct': gap_size_pct,
                        'candles_after_sweep': i
                    }
        
        return {'has_fvg': False, 'reason': 'No FVG detected'}
    
    def analyze_session(self, timeframe: str = '15m', 
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> List[Dict]:
        """
        Analyze trading sessions for liquidity sweep reversal setups.
        
        Args:
            timeframe: Timeframe to analyze ('5m', '15m', '1h')
            start_date: Optional start date (YYYY-MM-DD)
            end_date: Optional end date (YYYY-MM-DD)
            
        Returns:
            List of valid setups found
        """
        if timeframe not in self.nq_data:
            print(f"Error: {timeframe} data not loaded")
            return []
        
        df = self.nq_data[timeframe].copy()
        
        # Filter by date range if provided
        if start_date:
            df = df[df['datetime'] >= pd.Timestamp(start_date, tz='America/New_York')]
        if end_date:
            df = df[df['datetime'] <= pd.Timestamp(end_date, tz='America/New_York')]
        
        # Reset index after filtering to avoid KeyError
        df = df.reset_index(drop=True)
        
        if len(df) == 0:
            print("No data in specified date range")
            return []
        
        print(f"\n{'='*80}")
        print(f"Analyzing {timeframe} data: {len(df)} candles")
        print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")
        print(f"{'='*80}\n")
        
        # Detect swing points
        lookback = self.swing_lookback_15m if timeframe == '15m' else self.swing_lookback_1h
        swing_highs, swing_lows = self.detect_swing_points(df, lookback)
        
        print(f"Detected {swing_highs.sum()} swing highs and {swing_lows.sum()} swing lows\n")
        
        valid_setups = []
        
        # Scan each candle for potential setup
        for idx in range(lookback, len(df) - 5):
            row = df.iloc[idx]
            dt = row['datetime']
            
            # Step 1: Check if in killzone
            in_killzone, killzone_name = self.is_in_killzone(dt)
            if not in_killzone:
                continue
            
            # Step 2: Check for liquidity sweep
            sweep_info = self.detect_liquidity_sweep(df, idx, swing_highs, swing_lows)
            if sweep_info is None:
                continue
            
            # Step 3: Analyze sweep quality
            quality_info = self.analyze_sweep_quality(row, sweep_info)
            
            # Step 4: Check SMT divergence
            smt_info = self.check_smt_divergence(
                dt,
                row['close'],
                sweep_info['type']
            )
            
            # Step 5: Check for displacement and MSS
            displacement_info = self.detect_displacement_and_mss(
                df, idx, sweep_info['direction']
            )
            
            # Step 6: Check for FVG
            fvg_info = self.detect_fvg(df, idx, sweep_info['direction'])
            
            # Calculate setup probability
            probability_score = 0
            probability_factors = []
            
            # Quality score (0-3 points)
            probability_score += quality_info['score']
            probability_factors.append(f"Quality: {quality_info['quality']}")
            
            # SMT score (0-3 points)
            if smt_info['has_smt']:
                if smt_info.get('probability') == 'High':
                    probability_score += 3
                    probability_factors.append("SMT: High Probability")
                else:
                    probability_score += 2
                    probability_factors.append("SMT: Medium Probability")
            else:
                probability_factors.append("SMT: None")
            
            # Displacement score (0-2 points)
            if displacement_info.get('has_displacement'):
                if displacement_info.get('has_mss'):
                    probability_score += 2
                    probability_factors.append("Displacement: Strong + MSS")
                else:
                    probability_score += 1
                    probability_factors.append("Displacement: Moderate")
            
            # FVG score (0-1 point)
            if fvg_info.get('has_fvg'):
                probability_score += 1
                probability_factors.append("FVG: Present")
            
            # Determine overall probability
            if probability_score >= 7:
                overall_probability = "Very High"
            elif probability_score >= 5:
                overall_probability = "High"
            elif probability_score >= 3:
                overall_probability = "Medium"
            else:
                overall_probability = "Low"
            
            # Store the setup
            setup = {
                'datetime': dt,
                'timeframe': timeframe,
                'killzone': killzone_name,
                'sweep_info': sweep_info,
                'quality_info': quality_info,
                'smt_info': smt_info,
                'displacement_info': displacement_info,
                'fvg_info': fvg_info,
                'probability_score': probability_score,
                'probability_factors': probability_factors,
                'overall_probability': overall_probability,
                'price': row['close']
            }
            
            # Only keep Medium probability or higher
            if probability_score >= 3:
                valid_setups.append(setup)
        
        return valid_setups
    
    def generate_report(self, setups: List[Dict]) -> str:
        """
        Generate a detailed report of found setups.
        
        Args:
            setups: List of setup dictionaries
            
        Returns:
            Formatted report string
        """
        if len(setups) == 0:
            return "\n⚠️  No valid setups found in the analyzed period.\n"
        
        report = []
        report.append("\n" + "="*80)
        report.append("ICT LIQUIDITY SWEEP REVERSAL SETUPS - ANALYSIS REPORT")
        report.append("="*80 + "\n")
        
        report.append(f"Total Valid Setups Found: {len(setups)}\n")
        
        # Group by probability
        probability_groups = {}
        for setup in setups:
            prob = setup['overall_probability']
            if prob not in probability_groups:
                probability_groups[prob] = []
            probability_groups[prob].append(setup)
        
        report.append("Setup Distribution:")
        for prob in ['Very High', 'High', 'Medium', 'Low']:
            count = len(probability_groups.get(prob, []))
            if count > 0:
                report.append(f"  {prob} Probability: {count} setups")
        
        report.append("\n" + "="*80 + "\n")
        
        # Detail each setup
        for i, setup in enumerate(setups, 1):
            report.append(f"SETUP #{i}")
            report.append("-" * 80)
            
            # Basic info
            report.append(f"📅 Date/Time: {setup['datetime'].strftime('%Y-%m-%d %H:%M:%S %Z')}")
            report.append(f"⏱️  Timeframe: {setup['timeframe']}")
            report.append(f"🎯 Killzone: {setup['killzone']}")
            report.append(f"💰 Price: {setup['price']:.2f}")
            
            # Liquidity Sweep
            sweep = setup['sweep_info']
            report.append(f"\n🔄 LIQUIDITY SWEEP:")
            report.append(f"   Type: {sweep['type']}")
            report.append(f"   Sweep Level: {sweep['sweep_level']:.2f}")
            report.append(f"   Expected Direction: {sweep['direction'].replace('_', ' ').title()}")
            
            # Quality Analysis
            quality = setup['quality_info']
            report.append(f"\n✨ SWEEP QUALITY:")
            report.append(f"   Quality: {quality['quality']}")
            report.append(f"   Type: {quality['type']}")
            if 'wick_ratio' in quality:
                report.append(f"   Wick Ratio: {quality['wick_ratio']:.1%}")
                report.append(f"   Body Ratio: {quality['body_ratio']:.1%}")
            
            # SMT Divergence
            smt = setup['smt_info']
            report.append(f"\n📊 SMT DIVERGENCE:")
            if smt['has_smt']:
                report.append(f"   ✓ Confirmed: {smt['type']}")
                report.append(f"   NQ: {smt['nq_direction']}")
                report.append(f"   ES: {smt['es_direction']}")
                report.append(f"   Probability: {smt['probability']}")
            else:
                report.append(f"   ✗ Not Detected: {smt['reason']}")
            
            # Displacement & MSS
            disp = setup['displacement_info']
            report.append(f"\n⚡ DISPLACEMENT & MSS:")
            if disp.get('has_displacement'):
                report.append(f"   ✓ Displacement: Detected (candle +{disp['displacement_candle']})")
                report.append(f"   MSS: {'✓ Yes' if disp.get('has_mss') else '✗ No'}")
                report.append(f"   Strength: {disp['strength']}")
            else:
                report.append(f"   ✗ Not Detected: {disp.get('reason', 'Unknown')}")
            
            # FVG
            fvg = setup['fvg_info']
            report.append(f"\n📍 FAIR VALUE GAP (FVG):")
            if fvg.get('has_fvg'):
                report.append(f"   ✓ Detected: {fvg['type']}")
                report.append(f"   Gap Range: {fvg['gap_bottom']:.2f} - {fvg['gap_top']:.2f}")
                report.append(f"   Gap Size: {fvg['gap_size']:.2f} ({fvg['gap_size_pct']:.2f}%)")
            else:
                report.append(f"   ✗ Not Detected: {fvg.get('reason', 'Unknown')}")
            
            # Overall Assessment
            report.append(f"\n🎲 OVERALL ASSESSMENT:")
            report.append(f"   Probability: {setup['overall_probability']}")
            report.append(f"   Score: {setup['probability_score']}/9")
            report.append(f"   Factors:")
            for factor in setup['probability_factors']:
                report.append(f"     • {factor}")
            
            report.append("\n" + "="*80 + "\n")
        
        return "\n".join(report)


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("ICT LIQUIDITY SWEEP REVERSAL ANALYZER")
    print("="*80)
    
    # Initialize analyzer
    analyzer = ICTLiquiditySweepAnalyzer()
    
    # Load data for 2024 (most recent complete year)
    analyzer.load_data(year=2024)
    
    # Analyze 15m timeframe (recommended for ICT setups)
    print("\n🔍 Scanning for reversal setups on 15m timeframe...")
    setups_15m = analyzer.analyze_session(
        timeframe='15m',
        start_date='2024-01-01',
        end_date='2024-12-31'
    )
    
    # Generate and print report
    report = analyzer.generate_report(setups_15m)
    print(report)
    
    # Save report to file
    report_filename = "ICT_Liquidity_Sweep_Reversal_Report_2024.txt"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {report_filename}\n")
    
    # Also analyze 5m for more granular setups
    print("\n🔍 Scanning for reversal setups on 5m timeframe...")
    setups_5m = analyzer.analyze_session(
        timeframe='5m',
        start_date='2024-12-01',  # Last month only for 5m (too much data otherwise)
        end_date='2024-12-31'
    )
    
    if len(setups_5m) > 0:
        report_5m = analyzer.generate_report(setups_5m)
        print(report_5m)
        
        report_filename_5m = "ICT_Liquidity_Sweep_Reversal_Report_5m_Dec2024.txt"
        with open(report_filename_5m, 'w', encoding='utf-8') as f:
            f.write(report_5m)
        
        print(f"\n✅ 5m Report saved to: {report_filename_5m}\n")


if __name__ == "__main__":
    main()
