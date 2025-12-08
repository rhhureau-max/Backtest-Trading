"""
ICT London Open Backtesting Strategy for Nasdaq (NQ) Futures
============================================================

This script implements a comprehensive backtesting system for the ICT London Open strategy.

Strategy Rules:
1. Determine directional bias from H1/4H market structure
2. Identify Tokyo session range (19:00-00:00 NY time)
3. Detect FVG before manipulation move (Condition A)
4. Detect Judas Swing - aggressive move through FVG sweeping liquidity (Condition B)
5. Detect Inversion - violent reversal back through FVG (Condition C)
6. Detect Market Structure Shift (Condition D)
7. Enter on pullback to Inversion FVG with stop at Judas wick

Data Format: CSV with semicolon delimiter
Columns: Date;Time;Open;High;Low;Close;Volume

Usage:
    python ict_london_open_backtest.py [--data-dir PATH] [--start-year YEAR] [--end-year YEAR]
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import argparse
import warnings
warnings.filterwarnings('ignore')

class ICTLondonOpenBacktest:
    """
    Comprehensive ICT London Open backtesting system
    """
    
    def __init__(self, data_dir, start_year=2018, end_year=2025):
        """
        Initialize the backtesting system
        
        Parameters:
        -----------
        data_dir : str
            Directory containing CSV data files
        start_year : int
            Starting year for backtest
        end_year : int
            Ending year for backtest
        """
        self.data_dir = Path(data_dir)
        self.start_year = start_year
        self.end_year = end_year
        
        # Trading parameters
        self.slippage = 0.5  # NQ futures slippage/spread in points
        self.contract_value = 20  # $20 per point for NQ
        
        # Strategy parameters
        self.tokyo_start_hour = 19  # 19:00 NY time
        self.tokyo_end_hour = 0  # 00:00 NY time (midnight)
        self.london_start_hour = 1  # 01:00 NY time
        self.london_end_hour = 5  # 05:00 NY time
        
        # FVG parameters
        self.fvg_min_size = 2.0  # Minimum FVG size in points
        self.liquidity_sweep_tolerance = 0.5  # Tolerance for liquidity sweep detection in points
        
        # Data storage
        self.data = {}
        self.trades = []
        
    def load_data(self):
        """
        Load and parse multi-timeframe data from CSV files
        """
        print("Loading multi-timeframe data...")
        timeframes = ['1m', '5m', '15m', '1H', '4H']
        
        for tf in timeframes:
            print(f"  Loading {tf} data...")
            self.data[tf] = self._load_timeframe_data(tf)
            
        print(f"Data loaded successfully: {len(self.data)} timeframes")
        
    def _load_timeframe_data(self, timeframe):
        """
        Load data for a specific timeframe across all years
        
        Parameters:
        -----------
        timeframe : str
            Timeframe to load (1m, 5m, 15m, 1H, 4H)
            
        Returns:
        --------
        pd.DataFrame
            Combined dataframe for all years
        """
        all_data = []
        
        for year in range(self.start_year, self.end_year + 1):
            filepath = self.data_dir / f"{year} {timeframe}.csv"
            
            if filepath.exists():
                try:
                    df = pd.read_csv(
                        filepath,
                        sep=';',
                        skiprows=1,  # Skip header row
                        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                    )
                    
                    # Parse datetime
                    df['Datetime'] = pd.to_datetime(
                        df['Date'] + ' ' + df['Time'],
                        format='%d/%m/%Y %H:%M:%S'
                    )
                    
                    # Set index and keep only OHLCV
                    df = df.set_index('Datetime')
                    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
                    
                    # Convert to numeric
                    for col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    
                    # Remove any NaN rows
                    df = df.dropna()
                    
                    all_data.append(df)
                    print(f"    {year}: {len(df)} bars")
                    
                except Exception as e:
                    print(f"    Error loading {filepath}: {e}")
        
        if all_data:
            combined = pd.concat(all_data).sort_index()
            # Remove duplicates
            combined = combined[~combined.index.duplicated(keep='first')]
            return combined
        else:
            return pd.DataFrame()
    
    def detect_fvg(self, df, direction='bullish'):
        """
        Detect Fair Value Gaps (FVG) in price data using 3-candle pattern
        
        A Fair Value Gap (FVG) represents a price inefficiency where:
        - The middle candle (candle[1]) creates an impulse move
        - Leaving a gap between candle[0] and candle[2] with no overlap
        
        Pattern Details:
        - Bullish FVG: candle[0].high < candle[2].low 
          Example: [1] moves up so fast that [0]'s high never touches [2]'s low
          Gap zone = [candle[0].high, candle[2].low]
          
        - Bearish FVG: candle[0].low > candle[2].high
          Example: [1] moves down so fast that [0]'s low never touches [2]'s high
          Gap zone = [candle[2].high, candle[0].low]
        
        Only gaps larger than fvg_min_size are considered valid.
        
        Parameters:
        -----------
        df : pd.DataFrame
            OHLC data with datetime index
        direction : str
            'bullish' or 'bearish' - type of FVG to detect
            
        Returns:
        --------
        list of dict
            List of FVGs with keys: timestamp, end_timestamp, top, bottom, 
            size, direction, filled
        """
        fvgs = []
        
        for i in range(len(df) - 2):
            candle0 = df.iloc[i]
            candle1 = df.iloc[i + 1]
            candle2 = df.iloc[i + 2]
            
            if direction == 'bullish':
                # Bullish FVG: gap up
                if candle0['High'] < candle2['Low']:
                    gap_bottom = candle0['High']
                    gap_top = candle2['Low']
                    gap_size = gap_top - gap_bottom
                    
                    if gap_size >= self.fvg_min_size:
                        fvgs.append({
                            'timestamp': df.index[i + 1],
                            'end_timestamp': df.index[i + 2],
                            'top': gap_top,
                            'bottom': gap_bottom,
                            'size': gap_size,
                            'direction': 'bullish',
                            'filled': False
                        })
            
            elif direction == 'bearish':
                # Bearish FVG: gap down
                if candle0['Low'] > candle2['High']:
                    gap_top = candle0['Low']
                    gap_bottom = candle2['High']
                    gap_size = gap_top - gap_bottom
                    
                    if gap_size >= self.fvg_min_size:
                        fvgs.append({
                            'timestamp': df.index[i + 1],
                            'end_timestamp': df.index[i + 2],
                            'top': gap_top,
                            'bottom': gap_bottom,
                            'size': gap_size,
                            'direction': 'bearish',
                            'filled': False
                        })
        
        return fvgs
    
    def identify_tokyo_session(self, date):
        """
        Get Tokyo session high/low for a given date
        
        Tokyo session: 19:00 previous day to 00:00 current day (NY time)
        
        Parameters:
        -----------
        date : datetime
            The date to find Tokyo session for
            
        Returns:
        --------
        dict or None
            Dictionary with tokyo_high, tokyo_low, start_time, end_time
        """
        # Tokyo session runs from 19:00 previous day to 00:00 current day
        tokyo_start = pd.Timestamp(date) - pd.Timedelta(days=1) + pd.Timedelta(hours=19)
        tokyo_end = pd.Timestamp(date) + pd.Timedelta(hours=0)
        
        # Get 5m data for Tokyo session
        df_5m = self.data['5m']
        tokyo_data = df_5m[(df_5m.index >= tokyo_start) & (df_5m.index < tokyo_end)]
        
        if len(tokyo_data) == 0:
            return None
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        
        return {
            'tokyo_high': tokyo_high,
            'tokyo_low': tokyo_low,
            'start_time': tokyo_start,
            'end_time': tokyo_end
        }
    
    def detect_market_structure_shift(self, df, start_idx, direction='bullish', lookback=20):
        """
        Detect Market Structure Shift (MSS) - confirmation of trend change
        
        A Market Structure Shift occurs when price decisively breaks the most recent
        swing point in the new direction, confirming a change in trend.
        
        MSS Criteria:
        - Bullish MSS: After inversion, price breaks above the prior swing high
          (highest high in lookback period before the reversal point)
        - Bearish MSS: After inversion, price breaks below the prior swing low
          (lowest low in lookback period before the reversal point)
        
        This implementation uses a simplified approach:
        - Looks back N bars to find the range before the reversal
        - Confirms MSS when price breaks the opposite extreme of that range
        - This validates that structure has genuinely shifted
        
        Parameters:
        -----------
        df : pd.DataFrame
            OHLC data with datetime index
        start_idx : int
            Index position to start looking for MSS (typically after inversion)
        direction : str
            'bullish' or 'bearish' - direction of expected MSS
        lookback : int
            Number of bars to look back for swing point identification (default: 20)
            
        Returns:
        --------
        dict or None
            MSS information with keys: timestamp, price, direction
            Returns None if no MSS detected within 50 bars
        """
        if start_idx < lookback:
            return None
        
        # Get data before start point
        lookback_data = df.iloc[start_idx - lookback:start_idx]
        
        if len(lookback_data) < 3:
            return None
        
        if direction == 'bullish':
            # Find the most recent swing low
            swing_low = lookback_data['Low'].min()
            
            # Check if price breaks above the high after that swing low
            for i in range(start_idx, min(start_idx + 50, len(df))):
                if df.iloc[i]['High'] > lookback_data['High'].max():
                    return {
                        'timestamp': df.index[i],
                        'price': df.iloc[i]['High'],
                        'direction': 'bullish'
                    }
        
        elif direction == 'bearish':
            # Find the most recent swing high
            swing_high = lookback_data['High'].max()
            
            # Check if price breaks below the low after that swing high
            for i in range(start_idx, min(start_idx + 50, len(df))):
                if df.iloc[i]['Low'] < lookback_data['Low'].min():
                    return {
                        'timestamp': df.index[i],
                        'price': df.iloc[i]['Low'],
                        'direction': 'bearish'
                    }
        
        return None
    
    def detect_ict_setup(self, date):
        """
        Detect ICT London Open setup for a specific date
        
        The setup must follow this sequence:
        1. Condition A: FVG formed before manipulation
        2. Condition B: Judas Swing - aggressive move through FVG sweeping liquidity
        3. Condition C: Inversion - reversal back through FVG with close beyond
        4. Condition D: Market Structure Shift
        
        Parameters:
        -----------
        date : datetime
            The date to analyze
            
        Returns:
        --------
        dict or None
            Setup information if detected
        """
        # Get Tokyo session for this date
        tokyo = self.identify_tokyo_session(date)
        if tokyo is None:
            return None
        
        # Define London session window
        london_start = pd.Timestamp(date) + pd.Timedelta(hours=self.london_start_hour)
        london_end = pd.Timestamp(date) + pd.Timedelta(hours=self.london_end_hour)
        
        # Get M5 and M15 data for analysis
        df_5m = self.data['5m']
        df_15m = self.data['15m']
        
        # Get data from Tokyo end to London end
        analysis_start = tokyo['end_time']
        analysis_data_5m = df_5m[(df_5m.index >= analysis_start) & (df_5m.index <= london_end)]
        
        if len(analysis_data_5m) < 10:
            return None
        
        # CONDITION A: Detect FVGs on M5 before London open
        pre_london_5m = df_5m[(df_5m.index >= analysis_start) & (df_5m.index < london_start)]
        
        if len(pre_london_5m) < 3:
            return None
        
        # Detect both bullish and bearish FVGs
        bullish_fvgs = self.detect_fvg(pre_london_5m, 'bullish')
        bearish_fvgs = self.detect_fvg(pre_london_5m, 'bearish')
        
        # Try to find complete setup for both directions
        setups = []
        
        # Try bearish setup (Judas swing up, then reversal down)
        for fvg in bearish_fvgs:
            setup = self._check_setup_sequence(
                fvg, analysis_data_5m, tokyo, 'bearish', london_start, london_end
            )
            if setup:
                setups.append(setup)
        
        # Try bullish setup (Judas swing down, then reversal up)
        for fvg in bullish_fvgs:
            setup = self._check_setup_sequence(
                fvg, analysis_data_5m, tokyo, 'bullish', london_start, london_end
            )
            if setup:
                setups.append(setup)
        
        # Return the first valid setup found
        if setups:
            return setups[0]
        
        return None
    
    def _check_setup_sequence(self, fvg, df, tokyo, direction, london_start, london_end):
        """
        Check if the full ICT setup sequence is present
        
        Parameters:
        -----------
        fvg : dict
            The FVG (Condition A)
        df : pd.DataFrame
            Price data during analysis period
        tokyo : dict
            Tokyo session high/low
        direction : str
            'bullish' or 'bearish'
        london_start : Timestamp
            London session start
        london_end : Timestamp
            London session end
            
        Returns:
        --------
        dict or None
            Complete setup if found
        """
        # Get data after FVG formation
        data_after_fvg = df[df.index > fvg['end_timestamp']]
        
        if len(data_after_fvg) < 5:
            return None
        
        # CONDITION B: Look for Judas Swing
        # Price must cross through FVG and sweep Tokyo liquidity
        judas_swing = None
        
        if direction == 'bearish':
            # For bearish setup, Judas swing goes UP
            # Must cross through bearish FVG (upward) and sweep Tokyo high
            for i in range(len(data_after_fvg)):
                bar = data_after_fvg.iloc[i]
                
                # Check if price swept Tokyo high
                if bar['High'] >= tokyo['tokyo_high'] - self.liquidity_sweep_tolerance:
                    # Check if this move crossed through the FVG
                    # Price should have been below FVG and then moved above
                    lookback = max(0, i - 5)
                    prior_bars = data_after_fvg.iloc[lookback:i]
                    
                    if len(prior_bars) > 0:
                        was_below = prior_bars['Low'].min() < fvg['bottom']
                        crossed_through = bar['High'] > fvg['top']
                        
                        if was_below and crossed_through:
                            judas_swing = {
                                'timestamp': data_after_fvg.index[i],
                                'high': bar['High'],
                                'low': bar['Low'],
                                'direction': 'up'
                            }
                            break
        
        elif direction == 'bullish':
            # For bullish setup, Judas swing goes DOWN
            # Must cross through bullish FVG (downward) and sweep Tokyo low
            for i in range(len(data_after_fvg)):
                bar = data_after_fvg.iloc[i]
                
                # Check if price swept Tokyo low
                if bar['Low'] <= tokyo['tokyo_low'] + self.liquidity_sweep_tolerance:
                    # Check if this move crossed through the FVG
                    lookback = max(0, i - 5)
                    prior_bars = data_after_fvg.iloc[lookback:i]
                    
                    if len(prior_bars) > 0:
                        was_above = prior_bars['High'].max() > fvg['top']
                        crossed_through = bar['Low'] < fvg['bottom']
                        
                        if was_above and crossed_through:
                            judas_swing = {
                                'timestamp': data_after_fvg.index[i],
                                'high': bar['High'],
                                'low': bar['Low'],
                                'direction': 'down'
                            }
                            break
        
        if judas_swing is None:
            return None
        
        # CONDITION C: Look for Inversion
        # Price must reverse violently and close beyond the FVG in opposite direction
        data_after_judas = data_after_fvg[data_after_fvg.index > judas_swing['timestamp']]
        
        if len(data_after_judas) < 3:
            return None
        
        inversion = None
        
        if direction == 'bearish':
            # After upward Judas, look for downward reversal
            for i in range(len(data_after_judas)):
                bar = data_after_judas.iloc[i]
                
                # Check if price closed below the FVG
                if bar['Close'] < fvg['bottom']:
                    inversion = {
                        'timestamp': data_after_judas.index[i],
                        'price': bar['Close'],
                        'inversion_fvg_top': fvg['top'],
                        'inversion_fvg_bottom': fvg['bottom']
                    }
                    break
        
        elif direction == 'bullish':
            # After downward Judas, look for upward reversal
            for i in range(len(data_after_judas)):
                bar = data_after_judas.iloc[i]
                
                # Check if price closed above the FVG
                if bar['Close'] > fvg['top']:
                    inversion = {
                        'timestamp': data_after_judas.index[i],
                        'price': bar['Close'],
                        'inversion_fvg_top': fvg['top'],
                        'inversion_fvg_bottom': fvg['bottom']
                    }
                    break
        
        if inversion is None:
            return None
        
        # CONDITION D: Check for Market Structure Shift
        # Get index of inversion in the main dataframe
        try:
            inversion_idx = df.index.get_loc(inversion['timestamp'])
        except KeyError:
            return None
        
        mss = self.detect_market_structure_shift(df, inversion_idx, direction)
        
        if mss is None:
            return None
        
        # All conditions met! Return the complete setup
        return {
            'date': london_start.date(),
            'direction': direction,
            'fvg': fvg,
            'tokyo': tokyo,
            'judas_swing': judas_swing,
            'inversion': inversion,
            'mss': mss,
            'london_start': london_start,
            'london_end': london_end
        }
    
    def simulate_trade(self, setup):
        """
        Simulate a trade based on the setup
        
        Entry: Limit order on pullback to Inversion FVG
        Stop: Just above/below Judas Swing wick
        Target: Opposite Tokyo liquidity
        
        Parameters:
        -----------
        setup : dict
            Complete ICT setup
            
        Returns:
        --------
        dict or None
            Trade result
        """
        direction = setup['direction']
        inversion_fvg_top = setup['inversion']['inversion_fvg_top']
        inversion_fvg_bottom = setup['inversion']['inversion_fvg_bottom']
        
        # Entry price: middle of Inversion FVG
        entry_price = (inversion_fvg_top + inversion_fvg_bottom) / 2
        
        # Stop loss
        if direction == 'bearish':
            # Stop above Judas swing high
            stop_loss = setup['judas_swing']['high'] + 2.0  # Add buffer
            target = setup['tokyo']['tokyo_low']  # Target opposite liquidity
        else:
            # Stop below Judas swing low
            stop_loss = setup['judas_swing']['low'] - 2.0  # Add buffer
            target = setup['tokyo']['tokyo_high']  # Target opposite liquidity
        
        # Get data after inversion for trade simulation
        df_5m = self.data['5m']
        trade_start = setup['inversion']['timestamp']
        trade_end = trade_start + pd.Timedelta(hours=12)  # Look 12 hours forward
        
        trade_data = df_5m[(df_5m.index > trade_start) & (df_5m.index <= trade_end)]
        
        if len(trade_data) == 0:
            return None
        
        # Check if entry gets filled
        entry_filled = False
        entry_time = None
        
        for i in range(len(trade_data)):
            bar = trade_data.iloc[i]
            
            # Check if price pulls back into Inversion FVG
            # For bearish: price should pullback UP into the FVG zone (from below)
            # For bullish: price should pullback DOWN into the FVG zone (from above)
            if bar['High'] >= inversion_fvg_bottom and bar['Low'] <= inversion_fvg_top:
                entry_filled = True
                entry_time = trade_data.index[i]
                break
        
        # Missed trade logic: if target hit before entry, cancel
        if not entry_filled:
            # Check if target was hit before entry opportunity
            if direction == 'bearish':
                if trade_data['Low'].min() <= target:
                    return None  # Missed trade
            else:
                if trade_data['High'].max() >= target:
                    return None  # Missed trade
            
            return None  # Entry never filled
        
        # Entry filled, now simulate trade outcome
        trade_data_after_entry = trade_data[trade_data.index > entry_time]
        
        outcome = None
        exit_time = None
        exit_price = None
        
        for i in range(len(trade_data_after_entry)):
            bar = trade_data_after_entry.iloc[i]
            
            if direction == 'bearish':
                # Check stop loss first (more conservative)
                if bar['High'] >= stop_loss:
                    outcome = 'loss'
                    exit_time = trade_data_after_entry.index[i]
                    exit_price = stop_loss - self.slippage
                    break
                # Then check target
                if bar['Low'] <= target:
                    outcome = 'win'
                    exit_time = trade_data_after_entry.index[i]
                    exit_price = target + self.slippage
                    break
            else:
                # Check stop loss first
                if bar['Low'] <= stop_loss:
                    outcome = 'loss'
                    exit_time = trade_data_after_entry.index[i]
                    exit_price = stop_loss + self.slippage
                    break
                # Then check target
                if bar['High'] >= target:
                    outcome = 'win'
                    exit_time = trade_data_after_entry.index[i]
                    exit_price = target - self.slippage
                    break
        
        # If no outcome after 12 hours, close at market (scratch trade)
        if outcome is None:
            exit_time = trade_data_after_entry.index[-1]
            exit_price = trade_data_after_entry.iloc[-1]['Close']
            
            if direction == 'bearish':
                if exit_price < entry_price:
                    outcome = 'win'
                else:
                    outcome = 'loss'
            else:
                if exit_price > entry_price:
                    outcome = 'win'
                else:
                    outcome = 'loss'
        
        # Calculate P&L
        if direction == 'bearish':
            points_pnl = entry_price - exit_price
        else:
            points_pnl = exit_price - entry_price
        
        dollar_pnl = points_pnl * self.contract_value
        
        return {
            'date': setup['date'],
            'direction': direction,
            'entry_time': entry_time,
            'entry_price': entry_price,
            'exit_time': exit_time,
            'exit_price': exit_price,
            'stop_loss': stop_loss,
            'target': target,
            'outcome': outcome,
            'points_pnl': points_pnl,
            'dollar_pnl': dollar_pnl,
            'tokyo_high': setup['tokyo']['tokyo_high'],
            'tokyo_low': setup['tokyo']['tokyo_low']
        }
    
    def run_backtest(self):
        """
        Run the complete backtest from start_year to end_year
        """
        print("\n" + "="*70)
        print("ICT LONDON OPEN BACKTEST - NASDAQ FUTURES")
        print("="*70)
        
        # Load data
        self.load_data()
        
        print("\nScanning for ICT setups...")
        
        # Get all unique dates from 5m data
        df_5m = self.data['5m']
        all_dates = df_5m.index.date
        unique_dates = sorted(set(all_dates))
        
        print(f"Analyzing {len(unique_dates)} trading days...\n")
        
        # Scan each date for setups
        setup_count = 0
        
        for i, date in enumerate(unique_dates):
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{len(unique_dates)} days analyzed...")
            
            setup = self.detect_ict_setup(date)
            
            if setup:
                setup_count += 1
                trade = self.simulate_trade(setup)
                
                if trade:
                    self.trades.append(trade)
        
        print(f"\nSetups found: {setup_count}")
        print(f"Trades executed: {len(self.trades)}")
        
        # Calculate and display results
        self.calculate_results()
    
    def calculate_results(self):
        """
        Calculate comprehensive backtest results and generate reports
        """
        if len(self.trades) == 0:
            print("\nNo trades to analyze.")
            return
        
        # Convert trades to DataFrame
        df_trades = pd.DataFrame(self.trades)
        
        # Add datetime features
        df_trades['entry_time'] = pd.to_datetime(df_trades['entry_time'])
        df_trades['year'] = df_trades['entry_time'].dt.year
        df_trades['month'] = df_trades['entry_time'].dt.month
        df_trades['weekday'] = df_trades['entry_time'].dt.day_name()
        df_trades['hour'] = df_trades['entry_time'].dt.hour
        
        # Calculate metrics
        total_trades = len(df_trades)
        winning_trades = len(df_trades[df_trades['outcome'] == 'win'])
        losing_trades = len(df_trades[df_trades['outcome'] == 'loss'])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = df_trades['dollar_pnl'].sum()
        gross_profit = df_trades[df_trades['dollar_pnl'] > 0]['dollar_pnl'].sum()
        gross_loss = abs(df_trades[df_trades['dollar_pnl'] < 0]['dollar_pnl'].sum())
        
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        
        avg_win = df_trades[df_trades['outcome'] == 'win']['dollar_pnl'].mean() if winning_trades > 0 else 0
        avg_loss = df_trades[df_trades['outcome'] == 'loss']['dollar_pnl'].mean() if losing_trades > 0 else 0
        
        expectancy = (win_rate / 100 * avg_win) + ((1 - win_rate / 100) * avg_loss)
        
        # Calculate drawdown
        df_trades['cumulative_pnl'] = df_trades['dollar_pnl'].cumsum()
        df_trades['cumulative_max'] = df_trades['cumulative_pnl'].cummax()
        df_trades['drawdown'] = df_trades['cumulative_pnl'] - df_trades['cumulative_max']
        
        max_drawdown_dollar = df_trades['drawdown'].min()
        peak_balance = df_trades['cumulative_max'].max()
        max_drawdown_pct = (max_drawdown_dollar / peak_balance * 100) if peak_balance > 0 else 0
        
        # Print results
        print("\n" + "="*70)
        print("BACKTEST RESULTS")
        print("="*70)
        print(f"\nTotal Trades: {total_trades}")
        print(f"Winning Trades: {winning_trades}")
        print(f"Losing Trades: {losing_trades}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"\nTotal P&L: ${total_pnl:,.2f}")
        print(f"Gross Profit: ${gross_profit:,.2f}")
        print(f"Gross Loss: ${gross_loss:,.2f}")
        print(f"Profit Factor: {profit_factor:.2f}")
        print(f"\nAverage Win: ${avg_win:,.2f}")
        print(f"Average Loss: ${avg_loss:,.2f}")
        print(f"Expectancy: ${expectancy:,.2f}")
        print(f"\nMax Drawdown: ${max_drawdown_dollar:,.2f} ({max_drawdown_pct:.2f}%)")
        
        # Analysis by year
        print("\n" + "-"*70)
        print("PERFORMANCE BY YEAR")
        print("-"*70)
        yearly = df_trades.groupby('year').agg({
            'dollar_pnl': ['sum', 'count'],
            'outcome': lambda x: (x == 'win').sum() / len(x) * 100
        })
        yearly.columns = ['Total P&L', 'Trades', 'Win Rate %']
        print(yearly.to_string())
        
        # Analysis by weekday
        print("\n" + "-"*70)
        print("PERFORMANCE BY WEEKDAY")
        print("-"*70)
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        weekday = df_trades.groupby('weekday').agg({
            'dollar_pnl': ['sum', 'count'],
            'outcome': lambda x: (x == 'win').sum() / len(x) * 100
        })
        weekday.columns = ['Total P&L', 'Trades', 'Win Rate %']
        weekday = weekday.reindex(weekday_order, fill_value=0)
        print(weekday.to_string())
        
        # Analysis by hour
        print("\n" + "-"*70)
        print("PERFORMANCE BY HOUR")
        print("-"*70)
        hourly = df_trades.groupby('hour').agg({
            'dollar_pnl': ['sum', 'count'],
            'outcome': lambda x: (x == 'win').sum() / len(x) * 100
        })
        hourly.columns = ['Total P&L', 'Trades', 'Win Rate %']
        print(hourly.to_string())
        
        # Save trade log
        trade_log_path = self.data_dir / 'ict_london_open_trades.csv'
        df_trades.to_csv(trade_log_path, index=False)
        print(f"\nTrade log saved to: {trade_log_path}")
        
        # Generate visualizations
        self.generate_visualizations(df_trades)
    
    def generate_visualizations(self, df_trades):
        """
        Generate visualization charts
        
        Parameters:
        -----------
        df_trades : pd.DataFrame
            Trade results dataframe
        """
        print("\nGenerating visualizations...")
        
        # Set style
        sns.set_style("darkgrid")
        plt.rcParams['figure.figsize'] = (15, 10)
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('ICT London Open Backtest Results - NQ Futures', fontsize=16, fontweight='bold')
        
        # 1. Equity Curve
        ax1 = axes[0, 0]
        df_trades['cumulative_pnl'].plot(ax=ax1, linewidth=2, color='blue')
        ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        ax1.set_title('Equity Curve', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Trade Number')
        ax1.set_ylabel('Cumulative P&L ($)')
        ax1.grid(True, alpha=0.3)
        
        # 2. Drawdown
        ax2 = axes[0, 1]
        df_trades['drawdown'].plot(ax=ax2, linewidth=2, color='red')
        ax2.fill_between(range(len(df_trades)), df_trades['drawdown'], 0, alpha=0.3, color='red')
        ax2.set_title('Drawdown', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Trade Number')
        ax2.set_ylabel('Drawdown ($)')
        ax2.grid(True, alpha=0.3)
        
        # 3. Win/Loss Distribution
        ax3 = axes[1, 0]
        win_loss_data = df_trades['outcome'].value_counts()
        colors = ['green' if x == 'win' else 'red' for x in win_loss_data.index]
        win_loss_data.plot(kind='bar', ax=ax3, color=colors, alpha=0.7)
        ax3.set_title('Win/Loss Distribution', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Outcome')
        ax3.set_ylabel('Count')
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0)
        ax3.grid(True, alpha=0.3)
        
        # 4. P&L Distribution
        ax4 = axes[1, 1]
        df_trades['dollar_pnl'].hist(ax=ax4, bins=30, color='blue', alpha=0.7, edgecolor='black')
        ax4.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax4.set_title('P&L Distribution', fontsize=12, fontweight='bold')
        ax4.set_xlabel('P&L ($)')
        ax4.set_ylabel('Frequency')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save figure
        chart_path = self.data_dir / 'ict_london_open_results.png'
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"Charts saved to: {chart_path}")
        
        plt.close()
        
        # Additional chart: Performance by Year
        fig2, ax = plt.subplots(figsize=(12, 6))
        yearly_pnl = df_trades.groupby('year')['dollar_pnl'].sum()
        yearly_pnl.plot(kind='bar', ax=ax, color='blue', alpha=0.7, edgecolor='black')
        ax.axhline(y=0, color='red', linestyle='--')
        ax.set_title('Annual Performance', fontsize=14, fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Total P&L ($)')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        chart_path_2 = self.data_dir / 'ict_london_open_annual.png'
        plt.savefig(chart_path_2, dpi=300, bbox_inches='tight')
        print(f"Annual performance chart saved to: {chart_path_2}")
        
        plt.close()


def main():
    """
    Main execution function
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='ICT London Open Backtesting Strategy for NQ Futures'
    )
    parser.add_argument(
        '--data-dir',
        type=str,
        default='/home/runner/work/Backtest-Trading/Backtest-Trading',
        help='Directory containing CSV data files (default: current directory)'
    )
    parser.add_argument(
        '--start-year',
        type=int,
        default=2018,
        help='Starting year for backtest (default: 2018)'
    )
    parser.add_argument(
        '--end-year',
        type=int,
        default=2025,
        help='Ending year for backtest (default: 2025)'
    )
    
    args = parser.parse_args()
    
    # Initialize backtesting system
    backtest = ICTLondonOpenBacktest(
        data_dir=args.data_dir,
        start_year=args.start_year,
        end_year=args.end_year
    )
    
    # Run backtest
    backtest.run_backtest()
    
    print("\n" + "="*70)
    print("BACKTEST COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()
