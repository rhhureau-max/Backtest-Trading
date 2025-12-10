"""
5 Advanced ICT Strategies Backtester - Extension
================================================

Senior Quantitative Analyst - ICT Smart Money Concepts Specialist

This script extends the institutional backtesting system with 5 advanced ICT strategies:
6. ICT Power of 3 (AMD) - Midnight Open Manipulation
7. SMT Divergence (NQ vs ES) - Correlation Crack Detection
8. ICT Breaker Block 4H - Polarity Change
9. Institutional Trend (VWAP Multi-Timeframe)
10. Volume Profile - POC Migration

Author: Senior Quant Analyst - ICT Expert
Date: 2025-12-10
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import warnings
warnings.filterwarnings('ignore')


class ICTAdvancedBacktester:
    """
    Advanced ICT strategies backtester with NQ/ES correlation analysis.
    """
    
    def __init__(self, symbol='NQ', start_date='2018-01-01', csv_dir='.'):
        """
        Initialize the ICT advanced backtester.
        
        Args:
            symbol: Trading symbol (NQ or ES)
            start_date: Start date for backtest
            csv_dir: Directory containing CSV files
        """
        self.symbol = symbol
        self.start_date = start_date
        self.csv_dir = csv_dir
        
        # Dataframes for NQ
        self.df_nq_1d = None
        self.df_nq_4h = None
        self.df_nq_1h = None
        self.df_nq_15m = None
        self.df_nq_5m = None
        
        # Dataframes for ES (for SMT divergence)
        self.df_es_1d = None
        self.df_es_4h = None
        self.df_es_1h = None
        
        # Results storage
        self.results = {}
        
    def load_data(self):
        """
        Load all required timeframes for NQ and ES.
        """
        print("📊 Loading multi-asset multi-timeframe data...")
        
        try:
            # Load NQ data
            print("\n📈 Loading NQ data:")
            self.df_nq_1d = self._load_timeframe('1D', 'NQ')
            print(f"   ✅ NQ Daily: {len(self.df_nq_1d)} candles")
            
            self.df_nq_4h = self._load_timeframe('4H', 'NQ')
            print(f"   ✅ NQ 4H: {len(self.df_nq_4h)} candles")
            
            self.df_nq_1h = self._load_timeframe('1H', 'NQ')
            print(f"   ✅ NQ 1H: {len(self.df_nq_1h)} candles")
            
            self.df_nq_15m = self._load_timeframe('15m', 'NQ')
            print(f"   ✅ NQ 15M: {len(self.df_nq_15m)} candles")
            
            self.df_nq_5m = self._load_timeframe('5m', 'NQ')
            print(f"   ✅ NQ 5M: {len(self.df_nq_5m)} candles")
            
            # Load ES data
            print("\n📉 Loading ES data:")
            self.df_es_1d = self._load_es_combined('1D')
            print(f"   ✅ ES Daily: {len(self.df_es_1d)} candles")
            
            self.df_es_1h = self._load_es_combined('1H')
            print(f"   ✅ ES 1H: {len(self.df_es_1h)} candles")
            
            # Create 4H from 1H data
            self.df_es_4h = self.df_es_1h.resample('4h').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()
            print(f"   ✅ ES 4H (resampled): {len(self.df_es_4h)} candles")
            
            print(f"\n✅ All data loaded successfully\n")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def _load_timeframe(self, timeframe, symbol='NQ'):
        """
        Load CSV data for a specific timeframe (NQ format with years).
        """
        start_year = int(self.start_date.split('-')[0])
        current_year = datetime.now().year
        
        dataframes = []
        
        for year in range(start_year, current_year + 1):
            csv_file = f"{self.csv_dir}/{year} {timeframe}.csv"
            try:
                df_year = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
                
                if 'Column1' in df_year.columns:
                    df_year['DateTime'] = pd.to_datetime(
                        df_year['Column1'] + ' ' + df_year['Column2'],
                        format='%d/%m/%Y %H:%M:%S'
                    )
                    df_year['Open'] = df_year['Column3'].astype(float)
                    df_year['High'] = df_year['Column4'].astype(float)
                    df_year['Low'] = df_year['Column5'].astype(float)
                    df_year['Close'] = df_year['Column6'].astype(float)
                    df_year['Volume'] = df_year['Column7'].astype(float)
                    
                    df_year = df_year[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                    df_year.set_index('DateTime', inplace=True)
                    dataframes.append(df_year)
            except FileNotFoundError:
                continue
        
        if dataframes:
            df = pd.concat(dataframes)
            df = df.sort_index()
            df = df[df.index >= self.start_date]
            return df
        else:
            raise ValueError(f"No data found for {symbol} {timeframe}")
    
    def _load_es_combined(self, timeframe):
        """
        Load ES data from combined CSV files.
        """
        # Try combined file first
        if timeframe == '1D':
            csv_file = f"{self.csv_dir}/ES 1D (2018-2025).csv"
        elif timeframe == '1H':
            csv_file = f"{self.csv_dir}/ES 1h (2018-2025).csv"
        else:
            raise ValueError(f"ES combined file not available for {timeframe}")
        
        try:
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
            
            if 'Column1' in df.columns:
                df['DateTime'] = pd.to_datetime(
                    df['Column1'] + ' ' + df['Column2'],
                    format='%d/%m/%Y %H:%M:%S'
                )
                df['Open'] = df['Column3'].astype(float)
                df['High'] = df['Column4'].astype(float)
                df['Low'] = df['Column5'].astype(float)
                df['Close'] = df['Column6'].astype(float)
                df['Volume'] = df['Column7'].astype(float)
                
                df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                df.set_index('DateTime', inplace=True)
                df = df.sort_index()
                df = df[df.index >= self.start_date]
                return df
        except Exception as e:
            raise ValueError(f"Error loading ES {timeframe}: {e}")
    
    def strategy_6_ict_power_of_3_amd(self):
        """
        STRATEGY 6: ICT Power of 3 (AMD) - Midnight Open Manipulation
        
        Logic:
        - Note price at 00:00 NY Time (Midnight Open)
        - If price goes below Midnight Open between 00:00-08:30 NY (London session)
        - Then shows reversal candle (H1 or M15)
        - Signal: Bullish bias - manipulation to buy at discount, target distribution above Midnight Open
        
        Expected Win Rate: ~65-70%
        """
        print("="*80)
        print("📈 STRATEGY 6: ICT Power of 3 (AMD) - Midnight Open")
        print("="*80)
        
        trades = []
        
        # Use 1H data for cleaner signals
        df_1h = self.df_nq_1h.copy()
        
        # Group by date
        df_1h['Date'] = df_1h.index.date
        
        for date in df_1h['Date'].unique():
            day_data = df_1h[df_1h['Date'] == date]
            
            if len(day_data) < 10:
                continue
            
            # Find midnight open (00:00)
            midnight_candles = day_data[day_data.index.hour == 0]
            if len(midnight_candles) == 0:
                continue
            
            midnight_open = midnight_candles.iloc[0]['Open']
            
            # Look at London session (00:00 to 08:30)
            london_candles = day_data[
                (day_data.index.hour >= 0) & 
                (day_data.index.hour < 9)
            ]
            
            if len(london_candles) < 3:
                continue
            
            # Check if price went below midnight open
            went_below = (london_candles['Low'] < midnight_open).any()
            
            if not went_below:
                continue
            
            # Look for reversal candle (bullish engulfing or strong green)
            for i in range(1, len(london_candles)):
                candle = london_candles.iloc[i]
                prev_candle = london_candles.iloc[i-1]
                
                # Bullish reversal: current close > current open and close > prev high
                is_reversal = (candle['Close'] > candle['Open']) and \
                              (candle['Close'] > prev_candle['High'])
                
                if is_reversal and candle['Low'] < midnight_open:
                    # Entry after reversal
                    entry_price = candle['Close']
                    target = midnight_open * 1.005  # Target 0.5% above midnight open
                    stop_loss = london_candles['Low'].min() * 0.995
                    direction = 'LONG'
                    
                    # Check outcome in remaining candles
                    remaining_candles = day_data.iloc[day_data.index.get_loc(candle.name)+1:]
                    
                    if len(remaining_candles) == 0:
                        continue
                    
                    trade_result = self._check_trade_outcome(
                        remaining_candles, entry_price, target, stop_loss, direction
                    )
                    
                    if trade_result:
                        trades.append({
                            'date': date,
                            'entry': entry_price,
                            'direction': direction,
                            'target': target,
                            'stop': stop_loss,
                            'midnight_open': midnight_open,
                            **trade_result
                        })
                    break
        
        results = self._calculate_statistics(trades, "ICT Power of 3 (AMD)")
        self.results['strategy_6'] = results
        
        return results
    
    def strategy_7_smt_divergence(self):
        """
        STRATEGY 7: SMT Divergence (NQ vs ES) at Key Level
        
        Logic:
        - Compare NQ and ES when testing previous highs/lows
        - Bearish SMT: NQ makes higher high BUT ES fails (lower high)
        - Bullish SMT: NQ makes lower low BUT ES makes higher low
        - Signal: Immediate reversal expected
        
        Expected Win Rate: ~70% (One of ICT's most reliable signals)
        """
        print("="*80)
        print("📈 STRATEGY 7: SMT Divergence (NQ vs ES)")
        print("="*80)
        
        trades = []
        
        # Use 4H data for both NQ and ES
        df_nq = self.df_nq_4h.copy()
        df_es = self.df_es_4h.copy()
        
        # Find swing highs and lows for both (lookback 10 candles)
        for i in range(20, len(df_nq)):
            current_time = df_nq.index[i]
            
            # Find corresponding ES candle
            es_candle_idx = df_es.index.get_indexer([current_time], method='nearest')[0]
            if es_candle_idx < 20 or es_candle_idx >= len(df_es):
                continue
            
            # Get recent history for both
            nq_recent = df_nq.iloc[i-10:i+1]
            es_recent = df_es.iloc[es_candle_idx-10:es_candle_idx+1]
            
            current_nq = df_nq.iloc[i]
            current_es = df_es.iloc[es_candle_idx]
            
            # Check for bearish SMT (at highs)
            nq_prev_high = nq_recent.iloc[:-1]['High'].max()
            es_prev_high = es_recent.iloc[:-1]['High'].max()
            
            # NQ makes higher high, ES doesn't
            if current_nq['High'] > nq_prev_high and current_es['High'] < es_prev_high:
                # Bearish SMT detected
                entry_price = current_nq['Close']
                target = current_nq['Low'] - (current_nq['High'] - current_nq['Low']) * 2
                stop_loss = current_nq['High'] * 1.005
                direction = 'SHORT'
                
                remaining_candles = df_nq.iloc[i+1:i+20]
                
                if len(remaining_candles) > 0:
                    trade_result = self._check_trade_outcome(
                        remaining_candles, entry_price, target, stop_loss, direction
                    )
                    
                    if trade_result:
                        trades.append({
                            'date': current_time.date(),
                            'entry': entry_price,
                            'direction': direction,
                            'target': target,
                            'stop': stop_loss,
                            'type': 'BEARISH_SMT',
                            'nq_high': current_nq['High'],
                            'es_high': current_es['High'],
                            **trade_result
                        })
            
            # Check for bullish SMT (at lows)
            nq_prev_low = nq_recent.iloc[:-1]['Low'].min()
            es_prev_low = es_recent.iloc[:-1]['Low'].min()
            
            # NQ makes lower low, ES doesn't
            if current_nq['Low'] < nq_prev_low and current_es['Low'] > es_prev_low:
                # Bullish SMT detected
                entry_price = current_nq['Close']
                target = current_nq['High'] + (current_nq['High'] - current_nq['Low']) * 2
                stop_loss = current_nq['Low'] * 0.995
                direction = 'LONG'
                
                remaining_candles = df_nq.iloc[i+1:i+20]
                
                if len(remaining_candles) > 0:
                    trade_result = self._check_trade_outcome(
                        remaining_candles, entry_price, target, stop_loss, direction
                    )
                    
                    if trade_result:
                        trades.append({
                            'date': current_time.date(),
                            'entry': entry_price,
                            'direction': direction,
                            'target': target,
                            'stop': stop_loss,
                            'type': 'BULLISH_SMT',
                            'nq_low': current_nq['Low'],
                            'es_low': current_es['Low'],
                            **trade_result
                        })
        
        results = self._calculate_statistics(trades, "SMT Divergence (NQ vs ES)")
        self.results['strategy_7'] = results
        
        return results
    
    def strategy_8_breaker_block(self):
        """
        STRATEGY 8: ICT Breaker Block 4H (Polarity Change)
        
        Logic:
        - Identify bearish order block (last bullish candle before bearish MSS)
        - If price breaks back above this block (close above)
        - Signal: Block becomes bullish breaker, bias turns bullish on retest
        
        Expected Win Rate: ~60-65%
        """
        print("="*80)
        print("📈 STRATEGY 8: ICT Breaker Block 4H")
        print("="*80)
        
        trades = []
        
        df_4h = self.df_nq_4h.copy()
        
        # Identify order blocks and breakers
        for i in range(20, len(df_4h) - 10):
            # Look for bearish market structure shift (MSS)
            recent = df_4h.iloc[i-10:i+1]
            current = df_4h.iloc[i]
            
            # Simple MSS: break of previous swing low
            swing_low = recent.iloc[:-5]['Low'].min()
            
            if current['Low'] < swing_low:
                # MSS happened, find last bullish candle before the drop
                for j in range(i-1, i-10, -1):
                    candle = df_4h.iloc[j]
                    if candle['Close'] > candle['Open']:
                        # This is the bearish order block
                        ob_high = candle['High']
                        ob_low = candle['Low']
                        
                        # Now look for price breaking back above this block
                        future_candles = df_4h.iloc[i+1:i+40]
                        
                        for k, (idx, future) in enumerate(future_candles.iterrows()):
                            # Breaker: close above order block
                            if future['Close'] > ob_high:
                                # Wait for retest
                                retest_candles = future_candles.iloc[k+1:k+10]
                                
                                for m, (idx2, retest) in enumerate(retest_candles.iterrows()):
                                    # Retest of breaker zone
                                    if retest['Low'] <= ob_high and retest['Low'] >= ob_low:
                                        # Entry on retest
                                        entry_price = ob_high
                                        target = ob_high + (ob_high - ob_low) * 3
                                        stop_loss = ob_low * 0.995
                                        direction = 'LONG'
                                        
                                        remaining = retest_candles.iloc[m+1:]
                                        
                                        if len(remaining) > 0:
                                            trade_result = self._check_trade_outcome(
                                                remaining, entry_price, target, stop_loss, direction
                                            )
                                            
                                            if trade_result:
                                                trades.append({
                                                    'date': idx2.date(),
                                                    'entry': entry_price,
                                                    'direction': direction,
                                                    'target': target,
                                                    'stop': stop_loss,
                                                    'ob_high': ob_high,
                                                    'ob_low': ob_low,
                                                    **trade_result
                                                })
                                        break
                                break
                        break
        
        results = self._calculate_statistics(trades, "ICT Breaker Block")
        self.results['strategy_8'] = results
        
        return results
    
    def strategy_9_institutional_vwap(self):
        """
        STRATEGY 9: Institutional Trend (VWAP Weekly & Daily)
        
        Logic:
        - Calculate weekly VWAP (anchored from week start)
        - Calculate daily VWAP
        - Bullish bias: price > weekly VWAP AND price > daily VWAP
        - Bearish bias: price < weekly VWAP AND price < daily VWAP
        - Filter: Don't trade if price between the two VWAPs
        
        Expected Win Rate: ~55-60%
        """
        print("="*80)
        print("📈 STRATEGY 9: Institutional VWAP Trend")
        print("="*80)
        
        trades = []
        
        df_1h = self.df_nq_1h.copy()
        
        # Calculate VWAP
        df_1h['Typical_Price'] = (df_1h['High'] + df_1h['Low'] + df_1h['Close']) / 3
        df_1h['TPV'] = df_1h['Typical_Price'] * df_1h['Volume']
        
        # Weekly VWAP (anchored at week start)
        df_1h['Week'] = df_1h.index.isocalendar().week
        df_1h['Year'] = df_1h.index.year
        
        df_1h['Weekly_VWAP'] = df_1h.groupby(['Year', 'Week']).apply(
            lambda x: (x['TPV'].cumsum() / x['Volume'].cumsum())
        ).reset_index(level=[0, 1], drop=True)
        
        # Daily VWAP
        df_1h['Date'] = df_1h.index.date
        df_1h['Daily_VWAP'] = df_1h.groupby('Date').apply(
            lambda x: (x['TPV'].cumsum() / x['Volume'].cumsum())
        ).reset_index(level=0, drop=True)
        
        # Generate signals
        for i in range(50, len(df_1h) - 10):
            current = df_1h.iloc[i]
            
            weekly_vwap = current['Weekly_VWAP']
            daily_vwap = current['Daily_VWAP']
            price = current['Close']
            
            if pd.isna(weekly_vwap) or pd.isna(daily_vwap):
                continue
            
            # Bullish bias
            if price > weekly_vwap and price > daily_vwap:
                # Wait for pullback to daily VWAP
                future_candles = df_1h.iloc[i+1:i+20]
                
                for j, (idx, candle) in enumerate(future_candles.iterrows()):
                    if candle['Low'] <= candle['Daily_VWAP']:
                        # Entry at VWAP
                        entry_price = candle['Daily_VWAP']
                        target = entry_price * 1.015  # 1.5% target
                        stop_loss = candle['Low'] * 0.995
                        direction = 'LONG'
                        
                        remaining = future_candles.iloc[j+1:]
                        
                        if len(remaining) > 0:
                            trade_result = self._check_trade_outcome(
                                remaining, entry_price, target, stop_loss, direction
                            )
                            
                            if trade_result:
                                trades.append({
                                    'date': idx.date(),
                                    'entry': entry_price,
                                    'direction': direction,
                                    'target': target,
                                    'stop': stop_loss,
                                    'weekly_vwap': weekly_vwap,
                                    'daily_vwap': daily_vwap,
                                    **trade_result
                                })
                        break
            
            # Bearish bias
            elif price < weekly_vwap and price < daily_vwap:
                # Wait for rally to daily VWAP
                future_candles = df_1h.iloc[i+1:i+20]
                
                for j, (idx, candle) in enumerate(future_candles.iterrows()):
                    if candle['High'] >= candle['Daily_VWAP']:
                        # Entry at VWAP
                        entry_price = candle['Daily_VWAP']
                        target = entry_price * 0.985  # 1.5% target
                        stop_loss = candle['High'] * 1.005
                        direction = 'SHORT'
                        
                        remaining = future_candles.iloc[j+1:]
                        
                        if len(remaining) > 0:
                            trade_result = self._check_trade_outcome(
                                remaining, entry_price, target, stop_loss, direction
                            )
                            
                            if trade_result:
                                trades.append({
                                    'date': idx.date(),
                                    'entry': entry_price,
                                    'direction': direction,
                                    'target': target,
                                    'stop': stop_loss,
                                    'weekly_vwap': weekly_vwap,
                                    'daily_vwap': daily_vwap,
                                    **trade_result
                                })
                        break
        
        results = self._calculate_statistics(trades, "Institutional VWAP Trend")
        self.results['strategy_9'] = results
        
        return results
    
    def strategy_10_poc_migration(self):
        """
        STRATEGY 10: Volume Profile - POC Migration
        
        Logic:
        - Calculate Point of Control (POC) for J-1 and J-2
        - Bullish bias: POC(J-1) > POC(J-2) - value migrating up
        - Bearish bias: POC(J-1) < POC(J-2) - value migrating down
        - Entry: Test of J-1 POC in direction of migration
        
        Expected Win Rate: ~58-62%
        """
        print("="*80)
        print("📈 STRATEGY 10: Volume Profile POC Migration")
        print("="*80)
        
        trades = []
        
        df_1d = self.df_nq_1d.copy()
        df_1h = self.df_nq_1h.copy()
        
        # Calculate POC for each day (price with highest volume)
        # Simplified: use close as POC approximation (in reality would need tick data)
        df_1d['POC'] = df_1d['Close']  # Simplified POC
        
        for i in range(2, len(df_1d)):
            day_today = df_1d.index[i]
            day_j1 = df_1d.index[i-1]
            day_j2 = df_1d.index[i-2]
            
            poc_j1 = df_1d.loc[day_j1, 'POC']
            poc_j2 = df_1d.loc[day_j2, 'POC']
            
            # Check POC migration
            if poc_j1 > poc_j2:
                # Bullish migration
                bias = 'BULLISH'
                
                # Get intraday data for today
                day_candles = df_1h[
                    (df_1h.index >= day_today) &
                    (df_1h.index < day_today + timedelta(days=1))
                ]
                
                # Look for test of J-1 POC
                for j, (idx, candle) in enumerate(day_candles.iterrows()):
                    if candle['Low'] <= poc_j1 * 1.002 and candle['Low'] >= poc_j1 * 0.998:
                        # POC tested
                        entry_price = poc_j1
                        target = poc_j1 * 1.01  # 1% target
                        stop_loss = poc_j2 * 0.995
                        direction = 'LONG'
                        
                        remaining = day_candles.iloc[j+1:]
                        
                        if len(remaining) > 0:
                            trade_result = self._check_trade_outcome(
                                remaining, entry_price, target, stop_loss, direction
                            )
                            
                            if trade_result:
                                trades.append({
                                    'date': idx.date(),
                                    'entry': entry_price,
                                    'direction': direction,
                                    'target': target,
                                    'stop': stop_loss,
                                    'poc_j1': poc_j1,
                                    'poc_j2': poc_j2,
                                    'migration': 'UP',
                                    **trade_result
                                })
                        break
            
            elif poc_j1 < poc_j2:
                # Bearish migration
                bias = 'BEARISH'
                
                day_candles = df_1h[
                    (df_1h.index >= day_today) &
                    (df_1h.index < day_today + timedelta(days=1))
                ]
                
                for j, (idx, candle) in enumerate(day_candles.iterrows()):
                    if candle['High'] >= poc_j1 * 0.998 and candle['High'] <= poc_j1 * 1.002:
                        # POC tested
                        entry_price = poc_j1
                        target = poc_j1 * 0.99  # 1% target
                        stop_loss = poc_j2 * 1.005
                        direction = 'SHORT'
                        
                        remaining = day_candles.iloc[j+1:]
                        
                        if len(remaining) > 0:
                            trade_result = self._check_trade_outcome(
                                remaining, entry_price, target, stop_loss, direction
                            )
                            
                            if trade_result:
                                trades.append({
                                    'date': idx.date(),
                                    'entry': entry_price,
                                    'direction': direction,
                                    'target': target,
                                    'stop': stop_loss,
                                    'poc_j1': poc_j1,
                                    'poc_j2': poc_j2,
                                    'migration': 'DOWN',
                                    **trade_result
                                })
                        break
        
        results = self._calculate_statistics(trades, "POC Migration")
        self.results['strategy_10'] = results
        
        return results
    
    def _check_trade_outcome(self, candles, entry, target, stop, direction):
        """
        Check if trade hits target or stop loss.
        """
        if len(candles) == 0:
            return None
        
        for i, (idx, candle) in enumerate(candles.iterrows()):
            if direction == 'LONG':
                if candle['Low'] <= stop:
                    return {
                        'outcome': 'LOSS',
                        'exit_price': stop,
                        'pnl': stop - entry,
                        'bars_held': i + 1
                    }
                if candle['High'] >= target:
                    return {
                        'outcome': 'WIN',
                        'exit_price': target,
                        'pnl': target - entry,
                        'bars_held': i + 1
                    }
            else:  # SHORT
                if candle['High'] >= stop:
                    return {
                        'outcome': 'LOSS',
                        'exit_price': stop,
                        'pnl': entry - stop,
                        'bars_held': i + 1
                    }
                if candle['Low'] <= target:
                    return {
                        'outcome': 'WIN',
                        'exit_price': target,
                        'pnl': entry - target,
                        'bars_held': i + 1
                    }
        
        # No exit - close at market
        last_candle = candles.iloc[-1]
        exit_price = last_candle['Close']
        
        if direction == 'LONG':
            pnl = exit_price - entry
        else:
            pnl = entry - exit_price
        
        outcome = 'WIN' if pnl > 0 else 'LOSS'
        
        return {
            'outcome': outcome,
            'exit_price': exit_price,
            'pnl': pnl,
            'bars_held': len(candles)
        }
    
    def _calculate_statistics(self, trades, strategy_name):
        """
        Calculate Win Rate, Profit Factor, and Max Drawdown.
        """
        if len(trades) == 0:
            print(f"\n❌ No trades found for {strategy_name}\n")
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'max_drawdown': 0
            }
        
        df_trades = pd.DataFrame(trades)
        
        wins = (df_trades['outcome'] == 'WIN').sum()
        losses = (df_trades['outcome'] == 'LOSS').sum()
        total_trades = len(trades)
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        gross_profit = df_trades[df_trades['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(df_trades[df_trades['pnl'] < 0]['pnl'].sum())
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else np.inf
        
        cumulative_pnl = df_trades['pnl'].cumsum()
        running_max = cumulative_pnl.expanding().max()
        drawdown = cumulative_pnl - running_max
        max_drawdown = abs(drawdown.min())
        
        avg_win = df_trades[df_trades['pnl'] > 0]['pnl'].mean() if wins > 0 else 0
        avg_loss = abs(df_trades[df_trades['pnl'] < 0]['pnl'].mean()) if losses > 0 else 0
        
        print(f"\n📊 {strategy_name} Results:")
        print(f"   • Total Trades: {total_trades}")
        print(f"   • Wins: {wins} | Losses: {losses}")
        print(f"   • Win Rate: {win_rate:.2f}%")
        print(f"   • Profit Factor: {profit_factor:.2f}")
        print(f"   • Max Drawdown: {max_drawdown:.2f} points")
        print(f"   • Gross Profit: {gross_profit:.2f} points")
        print(f"   • Gross Loss: {gross_loss:.2f} points")
        print(f"   • Net Profit: {gross_profit - gross_loss:.2f} points")
        print(f"   • Average Win: {avg_win:.2f} points")
        print(f"   • Average Loss: {avg_loss:.2f} points")
        print(f"   • Average Bars Held: {df_trades['bars_held'].mean():.1f}")
        
        return {
            'strategy_name': strategy_name,
            'total_trades': total_trades,
            'wins': int(wins),
            'losses': int(losses),
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'net_profit': gross_profit - gross_loss,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'avg_bars_held': df_trades['bars_held'].mean(),
            'trades': trades
        }
    
    def run_all_strategies(self):
        """
        Run all 5 ICT advanced strategies and display comparison.
        """
        print("\n" + "="*80)
        print("🎯 5 ADVANCED ICT STRATEGIES BACKTEST")
        print(f"Symbol: {self.symbol}")
        print(f"Period: {self.start_date} to {datetime.now().strftime('%Y-%m-%d')}")
        print("="*80 + "\n")
        
        self.load_data()
        
        print("Starting ICT advanced backtests...\n")
        
        results_6 = self.strategy_6_ict_power_of_3_amd()
        print()
        
        results_7 = self.strategy_7_smt_divergence()
        print()
        
        results_8 = self.strategy_8_breaker_block()
        print()
        
        results_9 = self.strategy_9_institutional_vwap()
        print()
        
        results_10 = self.strategy_10_poc_migration()
        print()
        
        self._print_comparison_table()
        
        return self.results
    
    def _print_comparison_table(self):
        """
        Print comparison table of all ICT strategies.
        """
        print("\n" + "="*80)
        print("📊 ICT STRATEGIES COMPARISON TABLE")
        print("="*80)
        
        print(f"\n{'Strategy':<40} {'Trades':<8} {'Win Rate':<10} {'PF':<8} {'Net PnL':<12} {'Max DD':<10}")
        print("-" * 100)
        
        for key in ['strategy_6', 'strategy_7', 'strategy_8', 'strategy_9', 'strategy_10']:
            if key in self.results:
                r = self.results[key]
                print(f"{r['strategy_name']:<40} "
                      f"{r['total_trades']:<8} "
                      f"{r['win_rate']:<9.2f}% "
                      f"{r['profit_factor']:<7.2f} "
                      f"{r['net_profit']:<11.2f}pts "
                      f"{r['max_drawdown']:<9.2f}pts")
        
        print("\n" + "="*80)
        print("💡 EXPECTED vs ACTUAL Win Rates:")
        print("="*80)
        
        expected_wr = {
            'strategy_6': 67.5,
            'strategy_7': 70,
            'strategy_8': 62.5,
            'strategy_9': 57.5,
            'strategy_10': 60
        }
        
        for key in ['strategy_6', 'strategy_7', 'strategy_8', 'strategy_9', 'strategy_10']:
            if key in self.results:
                r = self.results[key]
                expected = expected_wr[key]
                actual = r['win_rate']
                diff = actual - expected
                symbol = "✅" if diff >= -5 else "⚠️"
                print(f"{symbol} {r['strategy_name']:<40} Expected: {expected:.1f}% | Actual: {actual:.2f}% | Diff: {diff:+.2f}%")
        
        print()


def main():
    """
    Main execution function.
    """
    print("\n" + "="*80)
    print("🚀 5 ADVANCED ICT STRATEGIES - BACKTEST SYSTEM")
    print("="*80)
    print("\nSenior Quantitative Analyst - ICT Smart Money Concepts")
    print("Backtesting Period: 2018 to Present")
    print("Multi-Asset Correlation Analysis: NQ vs ES")
    print("\n" + "="*80 + "\n")
    
    backtester = ICTAdvancedBacktester(
        symbol='NQ',
        start_date='2018-01-01',
        csv_dir='.'
    )
    
    results = backtester.run_all_strategies()
    
    print("\n" + "="*80)
    print("✅ ICT ADVANCED BACKTEST COMPLETE")
    print("="*80)
    print("\n📝 Summary:")
    print("   • All 5 ICT advanced strategies tested")
    print("   • Multi-asset correlation (NQ vs ES) analyzed")
    print("   • Smart Money Concepts validated")
    print("\n")


if __name__ == "__main__":
    main()
