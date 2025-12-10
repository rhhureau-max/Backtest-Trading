"""
5 Institutional Daily Bias Strategies Backtester
=================================================

Senior Quantitative Analyst - NQ & ES Futures Specialist

This script backtests 5 institutional methodologies for determining daily bias:
1. Market Profile 80% Rule (Value Area)
2. Liquidity Sweep & Reclaim (ICT/Turtle Soup)
3. Opening Range Breakout with Trend Filter
4. Gap Fill (Mean Reversion)
5. Structural Alignment 4H/1D (Trend Following)

Author: Senior Quant Analyst
Date: 2025-12-10
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import warnings
warnings.filterwarnings('ignore')


class InstitutionalBiasBacktester:
    """
    Backtester for 5 institutional daily bias strategies on NQ/ES futures.
    """
    
    def __init__(self, symbol='NQ', start_date='2018-01-01', csv_dir='.'):
        """
        Initialize the backtester.
        
        Args:
            symbol: Trading symbol (NQ or ES)
            start_date: Start date for backtest
            csv_dir: Directory containing CSV files
        """
        self.symbol = symbol
        self.start_date = start_date
        self.csv_dir = csv_dir
        
        # Dataframes for different timeframes
        self.df_1d = None
        self.df_4h = None
        self.df_1h = None
        self.df_30m = None
        self.df_15m = None
        self.df_5m = None
        
        # Results storage
        self.results = {}
        
    def load_data(self):
        """
        Load all required timeframes from CSV files.
        """
        print("📊 Loading multi-timeframe data...")
        
        try:
            # Load 1D data
            self.df_1d = self._load_timeframe('1D')
            print(f"   ✅ Daily: {len(self.df_1d)} candles")
            
            # Load 4H data
            self.df_4h = self._load_timeframe('4H')
            print(f"   ✅ 4H: {len(self.df_4h)} candles")
            
            # Load 15M data (for ORB)
            self.df_15m = self._load_timeframe('15m')
            print(f"   ✅ 15M: {len(self.df_15m)} candles")
            
            # Load 5M data (for detailed analysis)
            self.df_5m = self._load_timeframe('5m')
            print(f"   ✅ 5M: {len(self.df_5m)} candles")
            
            print(f"✅ All data loaded successfully\n")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def _load_timeframe(self, timeframe):
        """
        Load CSV data for a specific timeframe.
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
            raise ValueError(f"No data found for {timeframe}")
    
    def strategy_1_market_profile_80_rule(self):
        """
        STRATEGY 1: Market Profile 80% Rule
        
        Logic:
        - Calculate Value Area (70% of volume range) from previous day
        - If price opens outside VA but returns inside with 2 consecutive 30m closes
        - Signal: Bias toward opposite end of VA
        
        Expected Win Rate: ~80%
        """
        print("="*80)
        print("📈 STRATEGY 1: Market Profile 80% Rule (Value Area)")
        print("="*80)
        
        trades = []
        
        # We need daily data and 30m data
        # For simplicity, we'll use 5m data to simulate 30m
        df_30m = self.df_5m.resample('30min').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()
        
        # Get daily data
        daily_data = self.df_1d.copy()
        
        # Calculate Value Area for each day (simplified: 70% volume range)
        daily_data['VA_High'] = daily_data['Close'] + (daily_data['High'] - daily_data['Low']) * 0.35
        daily_data['VA_Low'] = daily_data['Close'] - (daily_data['High'] - daily_data['Low']) * 0.35
        
        for i in range(1, len(daily_data)):
            prev_day = daily_data.index[i-1]
            current_day = daily_data.index[i]
            
            va_high = daily_data.loc[prev_day, 'VA_High']
            va_low = daily_data.loc[prev_day, 'VA_Low']
            
            # Get 30m candles for current day
            day_candles = df_30m[
                (df_30m.index >= current_day) &
                (df_30m.index < current_day + timedelta(days=1))
            ]
            
            if len(day_candles) < 3:
                continue
            
            # Check if opens outside VA
            open_price = day_candles.iloc[0]['Open']
            opened_above = open_price > va_high
            opened_below = open_price < va_low
            
            if not (opened_above or opened_below):
                continue
            
            # Look for 2 consecutive closes inside VA
            for j in range(1, len(day_candles) - 1):
                close1 = day_candles.iloc[j]['Close']
                close2 = day_candles.iloc[j+1]['Close']
                
                inside1 = va_low <= close1 <= va_high
                inside2 = va_low <= close2 <= va_high
                
                if inside1 and inside2:
                    # Signal detected
                    if opened_above:
                        # Short toward VA_Low
                        entry_price = day_candles.iloc[j+1]['Close']
                        target = va_low
                        stop_loss = va_high * 1.005  # 0.5% above VA high
                        direction = 'SHORT'
                    else:  # opened_below
                        # Long toward VA_High
                        entry_price = day_candles.iloc[j+1]['Close']
                        target = va_high
                        stop_loss = va_low * 0.995  # 0.5% below VA low
                        direction = 'LONG'
                    
                    # Check outcome
                    remaining_candles = day_candles.iloc[j+2:]
                    
                    if len(remaining_candles) == 0:
                        continue
                    
                    trade_result = self._check_trade_outcome(
                        remaining_candles, entry_price, target, stop_loss, direction
                    )
                    
                    if trade_result:
                        trades.append({
                            'date': current_day,
                            'entry': entry_price,
                            'direction': direction,
                            'target': target,
                            'stop': stop_loss,
                            **trade_result
                        })
                    
                    break  # Only one trade per day
        
        # Calculate statistics
        results = self._calculate_statistics(trades, "Market Profile 80% Rule")
        self.results['strategy_1'] = results
        
        return results
    
    def strategy_2_liquidity_sweep_reclaim(self):
        """
        STRATEGY 2: Liquidity Sweep & Reclaim (ICT/Turtle Soup)
        
        Logic:
        - Identify previous day high (PDH) and low (PDL)
        - If price sweeps PDH/PDL but closes back inside previous day range
        - Signal: Immediate reversal (false breakout)
        
        Expected Win Rate: 65-70%
        """
        print("="*80)
        print("📈 STRATEGY 2: Liquidity Sweep & Reclaim (ICT)")
        print("="*80)
        
        trades = []
        
        # Use 4H data for cleaner signals
        df_4h = self.df_4h.copy()
        daily_data = self.df_1d.copy()
        
        for i in range(1, len(daily_data)):
            prev_day = daily_data.index[i-1]
            current_day = daily_data.index[i]
            
            pdh = daily_data.loc[prev_day, 'High']
            pdl = daily_data.loc[prev_day, 'Low']
            
            # Get 4H candles for current day
            day_candles = df_4h[
                (df_4h.index >= current_day) &
                (df_4h.index < current_day + timedelta(days=1))
            ]
            
            if len(day_candles) == 0:
                continue
            
            # Check for PDH sweep
            for j in range(len(day_candles)):
                candle = day_candles.iloc[j]
                
                # PDH sweep: High > PDH but Close < PDH
                if candle['High'] > pdh and candle['Close'] < pdh:
                    # Bearish signal
                    entry_price = candle['Close']
                    target = pdl  # Target previous day low
                    stop_loss = pdh * 1.01  # 1% above PDH
                    direction = 'SHORT'
                    
                    remaining_candles = day_candles.iloc[j+1:]
                    if len(remaining_candles) == 0:
                        continue
                    
                    trade_result = self._check_trade_outcome(
                        remaining_candles, entry_price, target, stop_loss, direction
                    )
                    
                    if trade_result:
                        trades.append({
                            'date': current_day,
                            'entry': entry_price,
                            'direction': direction,
                            'target': target,
                            'stop': stop_loss,
                            'type': 'PDH_SWEEP',
                            **trade_result
                        })
                    break
                
                # PDL sweep: Low < PDL but Close > PDL
                elif candle['Low'] < pdl and candle['Close'] > pdl:
                    # Bullish signal
                    entry_price = candle['Close']
                    target = pdh  # Target previous day high
                    stop_loss = pdl * 0.99  # 1% below PDL
                    direction = 'LONG'
                    
                    remaining_candles = day_candles.iloc[j+1:]
                    if len(remaining_candles) == 0:
                        continue
                    
                    trade_result = self._check_trade_outcome(
                        remaining_candles, entry_price, target, stop_loss, direction
                    )
                    
                    if trade_result:
                        trades.append({
                            'date': current_day,
                            'entry': entry_price,
                            'direction': direction,
                            'target': target,
                            'stop': stop_loss,
                            'type': 'PDL_SWEEP',
                            **trade_result
                        })
                    break
        
        results = self._calculate_statistics(trades, "Liquidity Sweep & Reclaim")
        self.results['strategy_2'] = results
        
        return results
    
    def strategy_3_opening_range_breakout(self):
        """
        STRATEGY 3: Opening Range Breakout with Trend Filter
        
        Logic:
        - Define opening range: first 15 minutes of US session (09:30-09:45 EST)
        - Trend filter: Above SMA20 on daily = only long breakouts, below = only short
        - Entry on breakout of OR high/low, stop at opposite end
        
        Expected Win Rate: 60-65%
        """
        print("="*80)
        print("📈 STRATEGY 3: Opening Range Breakout (ORB)")
        print("="*80)
        
        trades = []
        
        # Calculate SMA20 on daily
        daily_data = self.df_1d.copy()
        daily_data['SMA20'] = daily_data['Close'].rolling(window=20).mean()
        
        # Use 5m data for precise ORB
        df_5m = self.df_5m.copy()
        
        for i in range(20, len(daily_data)):
            current_day = daily_data.index[i]
            sma20 = daily_data.loc[current_day, 'SMA20']
            current_price = daily_data.loc[current_day, 'Open']
            
            # Determine trend bias
            bullish_trend = current_price > sma20
            bearish_trend = current_price < sma20
            
            if pd.isna(sma20):
                continue
            
            # Get 5m candles for the day
            day_candles = df_5m[
                (df_5m.index >= current_day) &
                (df_5m.index < current_day + timedelta(days=1))
            ]
            
            if len(day_candles) < 10:
                continue
            
            # Find opening range (first 3 candles = 15 minutes)
            or_candles = day_candles.iloc[:3]
            or_high = or_candles['High'].max()
            or_low = or_candles['Low'].min()
            
            # Look for breakout
            remaining_candles = day_candles.iloc[3:]
            
            for j in range(len(remaining_candles)):
                candle = remaining_candles.iloc[j]
                
                # Bullish breakout (only if in uptrend)
                if bullish_trend and candle['High'] > or_high:
                    entry_price = or_high
                    target = or_high + (or_high - or_low) * 2  # 2:1 R:R
                    stop_loss = or_low
                    direction = 'LONG'
                    
                    trade_result = self._check_trade_outcome(
                        remaining_candles.iloc[j:], entry_price, target, stop_loss, direction
                    )
                    
                    if trade_result:
                        trades.append({
                            'date': current_day,
                            'entry': entry_price,
                            'direction': direction,
                            'target': target,
                            'stop': stop_loss,
                            'or_high': or_high,
                            'or_low': or_low,
                            **trade_result
                        })
                    break
                
                # Bearish breakout (only if in downtrend)
                elif bearish_trend and candle['Low'] < or_low:
                    entry_price = or_low
                    target = or_low - (or_high - or_low) * 2  # 2:1 R:R
                    stop_loss = or_high
                    direction = 'SHORT'
                    
                    trade_result = self._check_trade_outcome(
                        remaining_candles.iloc[j:], entry_price, target, stop_loss, direction
                    )
                    
                    if trade_result:
                        trades.append({
                            'date': current_day,
                            'entry': entry_price,
                            'direction': direction,
                            'target': target,
                            'stop': stop_loss,
                            'or_high': or_high,
                            'or_low': or_low,
                            **trade_result
                        })
                    break
        
        results = self._calculate_statistics(trades, "Opening Range Breakout")
        self.results['strategy_3'] = results
        
        return results
    
    def strategy_4_gap_fill(self):
        """
        STRATEGY 4: Gap Fill (Mean Reversion)
        
        Logic:
        - Identify gap > 0.5% from previous day close
        - If gap not filled in first 30 minutes
        - Signal: Fade the gap when reversal candle appears
        
        Expected Win Rate: ~62%
        """
        print("="*80)
        print("📈 STRATEGY 4: Gap Fill (Mean Reversion)")
        print("="*80)
        
        trades = []
        
        daily_data = self.df_1d.copy()
        df_5m = self.df_5m.copy()
        
        for i in range(1, len(daily_data)):
            prev_day = daily_data.index[i-1]
            current_day = daily_data.index[i]
            
            prev_close = daily_data.loc[prev_day, 'Close']
            current_open = daily_data.loc[current_day, 'Open']
            
            # Calculate gap percentage
            gap_pct = abs(current_open - prev_close) / prev_close * 100
            
            if gap_pct < 0.5:
                continue
            
            gap_up = current_open > prev_close
            gap_down = current_open < prev_close
            
            # Get 5m candles for the day
            day_candles = df_5m[
                (df_5m.index >= current_day) &
                (df_5m.index < current_day + timedelta(days=1))
            ]
            
            if len(day_candles) < 10:
                continue
            
            # Check first 30 minutes (6 candles of 5m)
            first_30min = day_candles.iloc[:6]
            
            # Check if gap filled in first 30 min
            if gap_up:
                gap_filled_early = (first_30min['Low'] <= prev_close).any()
            else:
                gap_filled_early = (first_30min['High'] >= prev_close).any()
            
            if gap_filled_early:
                continue  # Skip if gap filled too quickly
            
            # Look for reversal after 30 minutes
            remaining_candles = day_candles.iloc[6:]
            
            for j in range(len(remaining_candles)):
                candle = remaining_candles.iloc[j]
                
                # Gap up - look for bearish reversal
                if gap_up:
                    # Bearish engulfing or strong red candle
                    if candle['Close'] < candle['Open']:
                        entry_price = candle['Close']
                        target = prev_close
                        stop_loss = day_candles.iloc[:j+6]['High'].max() * 1.005
                        direction = 'SHORT'
                        
                        trade_result = self._check_trade_outcome(
                            remaining_candles.iloc[j:], entry_price, target, stop_loss, direction
                        )
                        
                        if trade_result:
                            trades.append({
                                'date': current_day,
                                'entry': entry_price,
                                'direction': direction,
                                'target': target,
                                'stop': stop_loss,
                                'gap_pct': gap_pct,
                                'gap_type': 'UP',
                                **trade_result
                            })
                        break
                
                # Gap down - look for bullish reversal
                elif gap_down:
                    # Bullish engulfing or strong green candle
                    if candle['Close'] > candle['Open']:
                        entry_price = candle['Close']
                        target = prev_close
                        stop_loss = day_candles.iloc[:j+6]['Low'].min() * 0.995
                        direction = 'LONG'
                        
                        trade_result = self._check_trade_outcome(
                            remaining_candles.iloc[j:], entry_price, target, stop_loss, direction
                        )
                        
                        if trade_result:
                            trades.append({
                                'date': current_day,
                                'entry': entry_price,
                                'direction': direction,
                                'target': target,
                                'stop': stop_loss,
                                'gap_pct': gap_pct,
                                'gap_type': 'DOWN',
                                **trade_result
                            })
                        break
        
        results = self._calculate_statistics(trades, "Gap Fill")
        self.results['strategy_4'] = results
        
        return results
    
    def strategy_5_structural_alignment(self):
        """
        STRATEGY 5: Structural Alignment 4H/1D (Trend Following)
        
        Logic:
        - 1D: Price must be above EMA20
        - 4H: Price must make Higher High (HH) and Higher Low (HL)
        - Entry: Buy pullback to EMA20 on 4H if 1D condition met
        
        Expected Win Rate: ~55% (but high R:R > 1:2)
        """
        print("="*80)
        print("📈 STRATEGY 5: Structural Alignment 4H/1D")
        print("="*80)
        
        trades = []
        
        # Calculate EMA20 on daily
        daily_data = self.df_1d.copy()
        daily_data['EMA20'] = daily_data['Close'].ewm(span=20, adjust=False).mean()
        
        # Calculate EMA20 on 4H
        df_4h = self.df_4h.copy()
        df_4h['EMA20'] = df_4h['Close'].ewm(span=20, adjust=False).mean()
        
        # Detect Higher Highs and Higher Lows on 4H
        df_4h['HH'] = False
        df_4h['HL'] = False
        
        for i in range(2, len(df_4h)):
            # Higher High: Current high > previous 2 highs
            if df_4h.iloc[i]['High'] > df_4h.iloc[i-1]['High'] and \
               df_4h.iloc[i]['High'] > df_4h.iloc[i-2]['High']:
                df_4h.iloc[i, df_4h.columns.get_loc('HH')] = True
            
            # Higher Low: Current low > previous 2 lows
            if df_4h.iloc[i]['Low'] > df_4h.iloc[i-1]['Low'] and \
               df_4h.iloc[i]['Low'] > df_4h.iloc[i-2]['Low']:
                df_4h.iloc[i, df_4h.columns.get_loc('HL')] = True
        
        for i in range(20, len(df_4h)):
            current_time = df_4h.index[i]
            current_date = current_time.date()
            
            # Get corresponding daily candle
            daily_candle = daily_data[daily_data.index.date == current_date]
            if len(daily_candle) == 0:
                continue
            
            daily_close = daily_candle['Close'].iloc[0]
            daily_ema20 = daily_candle['EMA20'].iloc[0]
            
            if pd.isna(daily_ema20):
                continue
            
            # Check 1D condition: Price above EMA20
            if daily_close <= daily_ema20:
                continue
            
            # Check 4H conditions: HH and HL in recent history
            recent_4h = df_4h.iloc[max(0, i-10):i]
            has_hh = recent_4h['HH'].any()
            has_hl = recent_4h['HL'].any()
            
            if not (has_hh and has_hl):
                continue
            
            # Look for pullback to EMA20 on 4H
            candle = df_4h.iloc[i]
            ema20_4h = candle['EMA20']
            
            if pd.isna(ema20_4h):
                continue
            
            # Entry when price pulls back to EMA20
            if candle['Low'] <= ema20_4h <= candle['High']:
                entry_price = ema20_4h
                
                # Target: 2x the risk (recent swing high)
                recent_high = recent_4h['High'].max()
                risk = entry_price - candle['Low']
                target = entry_price + (risk * 2)
                stop_loss = candle['Low'] * 0.995
                direction = 'LONG'
                
                # Check outcome
                remaining_candles = df_4h.iloc[i+1:i+20]  # Next 20 4H candles
                
                if len(remaining_candles) == 0:
                    continue
                
                trade_result = self._check_trade_outcome(
                    remaining_candles, entry_price, target, stop_loss, direction
                )
                
                if trade_result:
                    trades.append({
                        'date': current_date,
                        'entry': entry_price,
                        'direction': direction,
                        'target': target,
                        'stop': stop_loss,
                        'daily_ema': daily_ema20,
                        **trade_result
                    })
        
        results = self._calculate_statistics(trades, "Structural Alignment")
        self.results['strategy_5'] = results
        
        return results
    
    def _check_trade_outcome(self, candles, entry, target, stop, direction):
        """
        Check if trade hits target or stop loss.
        """
        if len(candles) == 0:
            return None
        
        for i, (idx, candle) in enumerate(candles.iterrows()):
            if direction == 'LONG':
                # Check stop first
                if candle['Low'] <= stop:
                    return {
                        'outcome': 'LOSS',
                        'exit_price': stop,
                        'pnl': stop - entry,
                        'bars_held': i + 1
                    }
                # Check target
                if candle['High'] >= target:
                    return {
                        'outcome': 'WIN',
                        'exit_price': target,
                        'pnl': target - entry,
                        'bars_held': i + 1
                    }
            else:  # SHORT
                # Check stop first
                if candle['High'] >= stop:
                    return {
                        'outcome': 'LOSS',
                        'exit_price': stop,
                        'pnl': entry - stop,
                        'bars_held': i + 1
                    }
                # Check target
                if candle['Low'] <= target:
                    return {
                        'outcome': 'WIN',
                        'exit_price': target,
                        'pnl': entry - target,
                        'bars_held': i + 1
                    }
        
        # No exit found - close at market
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
        
        # Win Rate
        wins = (df_trades['outcome'] == 'WIN').sum()
        losses = (df_trades['outcome'] == 'LOSS').sum()
        total_trades = len(trades)
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        # Profit Factor
        gross_profit = df_trades[df_trades['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(df_trades[df_trades['pnl'] < 0]['pnl'].sum())
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else np.inf
        
        # Max Drawdown
        cumulative_pnl = df_trades['pnl'].cumsum()
        running_max = cumulative_pnl.expanding().max()
        drawdown = cumulative_pnl - running_max
        max_drawdown = abs(drawdown.min())
        
        # Average metrics
        avg_win = df_trades[df_trades['pnl'] > 0]['pnl'].mean() if wins > 0 else 0
        avg_loss = abs(df_trades[df_trades['pnl'] < 0]['pnl'].mean()) if losses > 0 else 0
        
        # Print results
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
        Run all 5 strategies and display comparison.
        """
        print("\n" + "="*80)
        print("🎯 5 INSTITUTIONAL DAILY BIAS STRATEGIES BACKTEST")
        print(f"Symbol: {self.symbol}")
        print(f"Period: {self.start_date} to {datetime.now().strftime('%Y-%m-%d')}")
        print("="*80 + "\n")
        
        # Load data
        self.load_data()
        
        # Run all strategies
        print("Starting backtests...\n")
        
        results_1 = self.strategy_1_market_profile_80_rule()
        print()
        
        results_2 = self.strategy_2_liquidity_sweep_reclaim()
        print()
        
        results_3 = self.strategy_3_opening_range_breakout()
        print()
        
        results_4 = self.strategy_4_gap_fill()
        print()
        
        results_5 = self.strategy_5_structural_alignment()
        print()
        
        # Comparison table
        self._print_comparison_table()
        
        return self.results
    
    def _print_comparison_table(self):
        """
        Print comparison table of all strategies.
        """
        print("\n" + "="*80)
        print("📊 STRATEGY COMPARISON TABLE")
        print("="*80)
        
        print(f"\n{'Strategy':<35} {'Trades':<8} {'Win Rate':<10} {'PF':<8} {'Net PnL':<12} {'Max DD':<10}")
        print("-" * 95)
        
        for key in ['strategy_1', 'strategy_2', 'strategy_3', 'strategy_4', 'strategy_5']:
            if key in self.results:
                r = self.results[key]
                print(f"{r['strategy_name']:<35} "
                      f"{r['total_trades']:<8} "
                      f"{r['win_rate']:<9.2f}% "
                      f"{r['profit_factor']:<7.2f} "
                      f"{r['net_profit']:<11.2f}pts "
                      f"{r['max_drawdown']:<9.2f}pts")
        
        print("\n" + "="*80)
        print("💡 EXPECTED vs ACTUAL Win Rates:")
        print("="*80)
        
        expected_wr = {
            'strategy_1': 80,
            'strategy_2': 67.5,
            'strategy_3': 62.5,
            'strategy_4': 62,
            'strategy_5': 55
        }
        
        for key in ['strategy_1', 'strategy_2', 'strategy_3', 'strategy_4', 'strategy_5']:
            if key in self.results:
                r = self.results[key]
                expected = expected_wr[key]
                actual = r['win_rate']
                diff = actual - expected
                symbol = "✅" if diff >= -5 else "⚠️"
                print(f"{symbol} {r['strategy_name']:<35} Expected: {expected:.1f}% | Actual: {actual:.2f}% | Diff: {diff:+.2f}%")
        
        print()


def main():
    """
    Main execution function.
    """
    print("\n" + "="*80)
    print("🚀 5 INSTITUTIONAL DAILY BIAS STRATEGIES - BACKTEST SYSTEM")
    print("="*80)
    print("\nSenior Quantitative Analyst - NQ & ES Futures")
    print("Backtesting Period: 2018 to Present")
    print("\n" + "="*80 + "\n")
    
    # Initialize backtester with NQ data
    backtester = InstitutionalBiasBacktester(
        symbol='NQ',
        start_date='2018-01-01',
        csv_dir='.'
    )
    
    # Run all strategies
    results = backtester.run_all_strategies()
    
    print("\n" + "="*80)
    print("✅ BACKTEST COMPLETE")
    print("="*80)
    print("\n📝 Summary:")
    print("   • All 5 institutional strategies tested")
    print("   • Results show Win Rate, Profit Factor, Max Drawdown")
    print("   • Comparison with theoretical expected win rates")
    print("\n")


if __name__ == "__main__":
    main()
