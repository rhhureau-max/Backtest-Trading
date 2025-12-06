"""
NQ London Continuation + Inversion FVG Strategy Backtest

This strategy captures trend continuation during London Open (02:00-05:00 Chicago)
using Inversion FVG entries after Asian session narrative setup.

Strategy Logic:
1. Asian Session (19:00-00:00): Identify trend and Asian FVG
2. London Open (02:00-03:30): Wait for retracement into Asian FVG
3. Inversion FVG: Enter when price closes through bearish FVG (in uptrend)
4. SMT Divergence: Check NQ vs ES divergence for confirmation

Stop Loss Options:
- SL A (Aggressive): 2-4 ticks below Inversion FVG
- SL B (Structural): 1 point below swing low

Target Options:
- Asian High: Liquidity at session high
- Fixed: 10-20 point scalp targets
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta, date
from typing import Dict, List, Tuple, Optional
import json

class FVG:
    """Fair Value Gap representation"""
    def __init__(self, idx: int, top: float, bottom: float, is_bullish: bool):
        self.idx = idx
        self.top = top
        self.bottom = bottom
        self.is_bullish = is_bullish
        self.filled = False
        
    def is_filled(self, high: float, low: float) -> bool:
        """Check if price has entered the FVG"""
        if self.is_bullish:
            return low <= self.top
        else:
            return high >= self.bottom

class SessionManager:
    """Manages trading sessions in Chicago time"""
    
    @staticmethod
    def is_asian_session(dt: datetime) -> bool:
        """Asian session: 19:00-00:00 Chicago"""
        t = dt.time()
        return time(19, 0) <= t or t < time(0, 0)
    
    @staticmethod
    def is_london_killzone(dt: datetime) -> bool:
        """London killzone: 02:00-05:00 Chicago"""
        t = dt.time()
        return time(2, 0) <= t < time(5, 0)
    
    @staticmethod
    def is_london_entry_window(dt: datetime) -> bool:
        """London entry window: 02:00-03:30 Chicago"""
        t = dt.time()
        return time(2, 0) <= t < time(3, 30)
    
    @staticmethod
    def get_session_label(dt: datetime) -> str:
        """Get session label for a datetime"""
        t = dt.time()
        if time(19, 0) <= t or t < time(0, 0):
            return "Asian"
        elif time(2, 0) <= t < time(5, 0):
            return "London"
        elif time(8, 30) <= t < time(15, 0):
            return "NY"
        else:
            return "Other"

class NQLondonContinuationStrategy:
    """
    NQ London Continuation + Inversion FVG Strategy
    """
    
    def __init__(self, nq_data: pd.DataFrame, es_data: pd.DataFrame = None):
        """
        Initialize strategy
        
        Args:
            nq_data: NQ 5-minute data
            es_data: ES 5-minute data for SMT divergence (optional)
        """
        self.nq_data = nq_data.copy()
        self.es_data = es_data.copy() if es_data is not None else None
        self.tick_size = 0.25  # NQ tick size
        
    def detect_fvg(self, data: pd.DataFrame, start_idx: int, end_idx: int) -> List[FVG]:
        """
        Detect Fair Value Gaps in a range
        
        Bullish FVG: Low[i] > High[i-2] (gap up)
        Bearish FVG: High[i] < Low[i-2] (gap down)
        """
        fvgs = []
        
        for i in range(start_idx + 2, end_idx):
            # Bullish FVG
            if data['Low'].iloc[i] > data['High'].iloc[i-2]:
                fvg = FVG(
                    idx=i,
                    top=data['Low'].iloc[i],
                    bottom=data['High'].iloc[i-2],
                    is_bullish=True
                )
                fvgs.append(fvg)
            
            # Bearish FVG
            elif data['High'].iloc[i] < data['Low'].iloc[i-2]:
                fvg = FVG(
                    idx=i,
                    top=data['Low'].iloc[i-2],
                    bottom=data['High'].iloc[i],
                    is_bullish=False
                )
                fvgs.append(fvg)
        
        return fvgs
    
    def detect_asian_narrative(self, data: pd.DataFrame, date: datetime.date) -> Dict:
        """
        Detect Asian session narrative (19:00-00:00)
        
        Returns:
            Dict with:
            - trend: 'bullish', 'bearish', or 'neutral'
            - asian_high: highest point
            - asian_low: lowest point
            - asian_fvgs: list of FVGs created during Asian session
        """
        # Get Asian session data
        asian_mask = (data['Date'] == date) & data['DateTime'].apply(SessionManager.is_asian_session)
        asian_data = data[asian_mask].copy()
        
        if len(asian_data) < 10:
            return None
        
        asian_high = asian_data['High'].max()
        asian_low = asian_data['Low'].min()
        
        # Determine trend: compare first half vs second half
        mid_idx = len(asian_data) // 2
        first_half_close = asian_data['Close'].iloc[:mid_idx].mean()
        second_half_close = asian_data['Close'].iloc[mid_idx:].mean()
        
        if second_half_close > first_half_close * 1.001:  # 0.1% threshold
            trend = 'bullish'
        elif second_half_close < first_half_close * 0.999:
            trend = 'bearish'
        else:
            trend = 'neutral'
        
        # Detect FVGs during Asian session
        start_idx = asian_data.index[0]
        end_idx = asian_data.index[-1] + 1
        asian_fvgs = self.detect_fvg(data, start_idx, end_idx)
        
        return {
            'trend': trend,
            'asian_high': asian_high,
            'asian_low': asian_low,
            'asian_fvgs': asian_fvgs,
            'asian_close': asian_data['Close'].iloc[-1],
            'asian_start_idx': start_idx,
            'asian_end_idx': end_idx
        }
    
    def check_smt_divergence(self, nq_data: pd.DataFrame, es_data: pd.DataFrame, 
                            nq_low_idx: int, lookback: int = 20) -> bool:
        """
        Check for SMT divergence between NQ and ES
        
        SMT: NQ makes lower low, but ES makes higher low (bullish divergence)
        or NQ makes higher high, but ES makes lower high (bearish divergence)
        
        Args:
            nq_data: NQ dataframe
            es_data: ES dataframe
            nq_low_idx: Index of NQ low to check
            lookback: Number of bars to look back
            
        Returns:
            True if bullish SMT divergence detected
        """
        if es_data is None:
            return False  # No ES data, can't check SMT
        
        # Get NQ current low and previous low
        current_nq_low = nq_data['Low'].iloc[nq_low_idx]
        start_idx = max(0, nq_low_idx - lookback)
        prev_nq_low = nq_data['Low'].iloc[start_idx:nq_low_idx].min()
        
        # Get corresponding ES data by timestamp
        nq_time = nq_data['DateTime'].iloc[nq_low_idx]
        
        # Find ES data around same time (within 5 minutes)
        time_window = timedelta(minutes=5)
        es_mask = (es_data['DateTime'] >= nq_time - time_window) & \
                  (es_data['DateTime'] <= nq_time + time_window)
        es_current = es_data[es_mask]
        
        if len(es_current) == 0:
            return False
        
        current_es_low = es_current['Low'].min()
        
        # Get previous ES low
        es_prev_mask = (es_data['DateTime'] >= nq_time - timedelta(minutes=lookback*5)) & \
                       (es_data['DateTime'] < nq_time - time_window)
        es_prev = es_data[es_prev_mask]
        
        if len(es_prev) == 0:
            return False
        
        prev_es_low = es_prev['Low'].min()
        
        # Bullish SMT: NQ lower low, ES higher low
        nq_lower_low = current_nq_low < prev_nq_low
        es_higher_low = current_es_low > prev_es_low
        
        return nq_lower_low and es_higher_low
    
    def detect_inversion_fvg(self, data: pd.DataFrame, london_start_idx: int, 
                            london_end_idx: int, asian_fvg: FVG, trend: str) -> Optional[Dict]:
        """
        Detect Inversion FVG during London session
        
        For bullish setup:
        1. Price retraces into Asian bullish FVG
        2. Price creates bearish FVG during retracement
        3. Price closes above the bearish FVG (inversion)
        
        Returns:
            Dict with entry details or None
        """
        if trend not in ['bullish', 'bearish']:
            return None
        
        # Detect FVGs during London session
        london_fvgs = self.detect_fvg(data, london_start_idx, london_end_idx)
        
        # Filter for opposite-direction FVGs (bearish FVG in bullish trend)
        target_bullish = (trend == 'bearish')
        opposite_fvgs = [fvg for fvg in london_fvgs if fvg.is_bullish == target_bullish]
        
        # Check for price retracing into Asian FVG
        for i in range(london_start_idx, london_end_idx):
            high = data['High'].iloc[i]
            low = data['Low'].iloc[i]
            
            # Check if price touched Asian FVG
            if asian_fvg.is_filled(high, low):
                asian_fvg.filled = True
                
                # Now look for inversion FVG after the touch
                for fvg in opposite_fvgs:
                    if fvg.idx <= i:
                        continue  # FVG before touch, skip
                    
                    # Check if price has closed through the FVG (inversion)
                    for j in range(fvg.idx + 1, min(fvg.idx + 5, london_end_idx)):
                        close = data['Close'].iloc[j]
                        
                        # Bullish setup: close above bearish FVG
                        if trend == 'bullish' and close > fvg.top:
                            return {
                                'entry_idx': j + 1,  # Enter next candle
                                'entry_price': data['Open'].iloc[j + 1] if j + 1 < len(data) else None,
                                'inversion_fvg': fvg,
                                'asian_fvg_touch_idx': i,
                                'setup_type': 'long'
                            }
                        
                        # Bearish setup: close below bullish FVG
                        elif trend == 'bearish' and close < fvg.bottom:
                            return {
                                'entry_idx': j + 1,
                                'entry_price': data['Open'].iloc[j + 1] if j + 1 < len(data) else None,
                                'inversion_fvg': fvg,
                                'asian_fvg_touch_idx': i,
                                'setup_type': 'short'
                            }
        
        return None
    
    def calculate_trade_outcome(self, data: pd.DataFrame, entry: Dict, 
                               asian_narrative: Dict, sl_type: str, 
                               target_type: str, rr_ratio: float = 1.0,
                               wait_for_retest: bool = False) -> Dict:
        """
        Calculate trade outcome with specified stop loss and target
        
        Args:
            data: Price data
            entry: Entry details from detect_inversion_fvg
            asian_narrative: Asian session info
            sl_type: 'A' (aggressive) or 'B' (structural)
            target_type: 'asian_high', 'fixed_10', 'fixed_15', 'fixed_20'
            rr_ratio: Risk-reward ratio
            wait_for_retest: If True, wait for price to retest inversion FVG before entry
            
        Returns:
            Dict with trade results
        """
        entry_idx = entry['entry_idx']
        if entry_idx >= len(data):
            return None
        
        entry_price = entry['entry_price']
        if entry_price is None:
            return None
        
        setup_type = entry['setup_type']
        inversion_fvg = entry['inversion_fvg']
        
        # Handle retest entry
        actual_entry_price = entry_price
        actual_entry_idx = entry_idx
        
        if wait_for_retest:
            # Wait for price to pull back to top of inversion FVG
            retest_found = False
            for i in range(entry_idx, min(entry_idx + 10, len(data))):
                if setup_type == 'long':
                    # Long: wait for pullback to FVG top
                    if data['Low'].iloc[i] <= inversion_fvg.top:
                        actual_entry_price = inversion_fvg.top
                        actual_entry_idx = i + 1
                        retest_found = True
                        break
                else:
                    # Short: wait for pullback to FVG bottom
                    if data['High'].iloc[i] >= inversion_fvg.bottom:
                        actual_entry_price = inversion_fvg.bottom
                        actual_entry_idx = i + 1
                        retest_found = True
                        break
            
            if not retest_found:
                return None  # No retest, skip trade
        
        # Calculate stop loss
        if sl_type == 'A':
            # SL A: 2-4 ticks below/above inversion FVG
            sl_distance_ticks = 3  # Using 3 ticks (0.75 points)
            if setup_type == 'long':
                stop_loss = inversion_fvg.bottom - (sl_distance_ticks * self.tick_size)
            else:
                stop_loss = inversion_fvg.top + (sl_distance_ticks * self.tick_size)
        else:  # SL B
            # SL B: 1 point below/above swing low/high
            touch_idx = entry['asian_fvg_touch_idx']
            if setup_type == 'long':
                # Find swing low in retracement
                swing_low = data['Low'].iloc[touch_idx:entry_idx].min()
                stop_loss = swing_low - 1.0
            else:
                # Find swing high in retracement
                swing_high = data['High'].iloc[touch_idx:entry_idx].max()
                stop_loss = swing_high + 1.0
        
        # Calculate risk
        if setup_type == 'long':
            risk = actual_entry_price - stop_loss
        else:
            risk = stop_loss - actual_entry_price
        
        if risk <= 0:
            return None
        
        # Calculate target
        if target_type == 'asian_high':
            if setup_type == 'long':
                target = asian_narrative['asian_high']
            else:
                target = asian_narrative['asian_low']
        elif target_type == 'fixed_10':
            if setup_type == 'long':
                target = actual_entry_price + 10.0
            else:
                target = actual_entry_price - 10.0
        elif target_type == 'fixed_15':
            if setup_type == 'long':
                target = actual_entry_price + 15.0
            else:
                target = actual_entry_price - 15.0
        elif target_type == 'fixed_20':
            if setup_type == 'long':
                target = actual_entry_price + 20.0
            else:
                target = actual_entry_price - 20.0
        else:  # RR-based
            reward = risk * rr_ratio
            if setup_type == 'long':
                target = actual_entry_price + reward
            else:
                target = actual_entry_price - reward
        
        # Simulate trade
        max_bars = 100  # Maximum bars to hold trade
        for i in range(actual_entry_idx, min(actual_entry_idx + max_bars, len(data))):
            high = data['High'].iloc[i]
            low = data['Low'].iloc[i]
            
            if setup_type == 'long':
                # Check stop loss
                if low <= stop_loss:
                    return {
                        'outcome': 'loss',
                        'entry_price': actual_entry_price,
                        'exit_price': stop_loss,
                        'entry_idx': actual_entry_idx,
                        'exit_idx': i,
                        'pnl': stop_loss - actual_entry_price,
                        'risk': risk,
                        'bars_held': i - actual_entry_idx,
                        'entry_type': 'retest' if wait_for_retest else 'immediate'
                    }
                # Check target
                if high >= target:
                    return {
                        'outcome': 'win',
                        'entry_price': actual_entry_price,
                        'exit_price': target,
                        'entry_idx': actual_entry_idx,
                        'exit_idx': i,
                        'pnl': target - actual_entry_price,
                        'risk': risk,
                        'bars_held': i - actual_entry_idx,
                        'entry_type': 'retest' if wait_for_retest else 'immediate'
                    }
            else:  # short
                # Check stop loss
                if high >= stop_loss:
                    return {
                        'outcome': 'loss',
                        'entry_price': actual_entry_price,
                        'exit_price': stop_loss,
                        'entry_idx': actual_entry_idx,
                        'exit_idx': i,
                        'pnl': actual_entry_price - stop_loss,
                        'risk': risk,
                        'bars_held': i - actual_entry_idx,
                        'entry_type': 'retest' if wait_for_retest else 'immediate'
                    }
                # Check target
                if low <= target:
                    return {
                        'outcome': 'win',
                        'entry_price': actual_entry_price,
                        'exit_price': target,
                        'entry_idx': actual_entry_idx,
                        'exit_idx': i,
                        'pnl': actual_entry_price - target,
                        'risk': risk,
                        'bars_held': i - actual_entry_idx,
                        'entry_type': 'retest' if wait_for_retest else 'immediate'
                    }
        
        # Trade timed out
        return None
    
    def run_backtest(self) -> Dict:
        """
        Run complete backtest on NQ data
        
        Returns:
            Dict with all trade results and statistics
        """
        data = self.nq_data
        trades = []
        
        # Get unique dates
        dates = data['Date'].unique()
        
        print(f"Starting backtest on {len(dates)} trading days...")
        
        for date in dates:
            # Get Asian narrative
            asian_narrative = self.detect_asian_narrative(data, date)
            if asian_narrative is None or asian_narrative['trend'] == 'neutral':
                continue
            
            # Get London session data
            next_day = date + timedelta(days=1)
            london_mask = (data['Date'] == next_day) & \
                         data['DateTime'].apply(SessionManager.is_london_entry_window)
            london_data = data[london_mask]
            
            if len(london_data) < 5:
                continue
            
            london_start_idx = london_data.index[0]
            london_end_idx = london_data.index[-1] + 1
            
            # Find valid Asian FVG to trade from
            asian_fvgs = asian_narrative['asian_fvgs']
            if len(asian_fvgs) == 0:
                continue
            
            # Use the last Asian FVG that matches trend
            target_bullish = (asian_narrative['trend'] == 'bullish')
            valid_fvgs = [fvg for fvg in asian_fvgs if fvg.is_bullish == target_bullish]
            
            if len(valid_fvgs) == 0:
                continue
            
            asian_fvg = valid_fvgs[-1]  # Use last FVG
            
            # Detect inversion FVG
            inversion_entry = self.detect_inversion_fvg(
                data, london_start_idx, london_end_idx, 
                asian_fvg, asian_narrative['trend']
            )
            
            if inversion_entry is None:
                continue
            
            # Check SMT if ES data available
            smt_divergence = False
            if self.es_data is not None:
                touch_idx = inversion_entry['asian_fvg_touch_idx']
                smt_divergence = self.check_smt_divergence(
                    data, self.es_data, touch_idx
                )
            
            # Test different configurations
            configurations = [
                # SL Type, Target Type, RR, Wait for Retest
                ('A', 'asian_high', 1.0, False),
                ('A', 'asian_high', 1.0, True),
                ('B', 'asian_high', 1.0, False),
                ('B', 'asian_high', 1.0, True),
                ('A', 'fixed_10', 1.0, False),
                ('A', 'fixed_10', 1.0, True),
                ('A', 'fixed_15', 1.0, False),
                ('A', 'fixed_15', 1.0, True),
                ('A', 'fixed_20', 1.0, False),
                ('A', 'fixed_20', 1.0, True),
                ('B', 'fixed_10', 1.0, False),
                ('B', 'fixed_15', 1.0, False),
                ('B', 'fixed_20', 1.0, False),
            ]
            
            for sl_type, target_type, rr, wait_retest in configurations:
                trade_result = self.calculate_trade_outcome(
                    data, inversion_entry, asian_narrative,
                    sl_type, target_type, rr, wait_retest
                )
                
                if trade_result is not None:
                    trade_result.update({
                        'date': date,
                        'sl_type': sl_type,
                        'target_type': target_type,
                        'rr_ratio': rr,
                        'wait_retest': wait_retest,
                        'asian_trend': asian_narrative['trend'],
                        'smt_divergence': smt_divergence,
                        'setup_type': inversion_entry['setup_type']
                    })
                    trades.append(trade_result)
        
        print(f"Backtest complete. Found {len(trades)} trades.")
        
        return {
            'trades': trades,
            'total_days': len(dates)
        }
    
    def analyze_results(self, backtest_results: Dict) -> Dict:
        """
        Analyze backtest results and generate statistics
        
        Returns:
            Dict with detailed statistics
        """
        trades = backtest_results['trades']
        
        if len(trades) == 0:
            return {'error': 'No trades found'}
        
        df = pd.DataFrame(trades)
        
        # Group by configuration
        configs = df.groupby(['sl_type', 'target_type', 'wait_retest'])
        
        results = {}
        
        for config, group in configs:
            sl_type, target_type, wait_retest = config
            
            config_name = f"SL_{sl_type}_{target_type}_{'retest' if wait_retest else 'immediate'}"
            
            wins = group[group['outcome'] == 'win']
            losses = group[group['outcome'] == 'loss']
            
            total_trades = len(group)
            win_count = len(wins)
            loss_count = len(losses)
            win_rate = win_count / total_trades if total_trades > 0 else 0
            
            total_pnl = group['pnl'].sum()
            avg_win = wins['pnl'].mean() if len(wins) > 0 else 0
            avg_loss = losses['pnl'].mean() if len(losses) > 0 else 0
            avg_pnl = group['pnl'].mean()
            
            gross_profit = wins['pnl'].sum() if len(wins) > 0 else 0
            gross_loss = abs(losses['pnl'].sum()) if len(losses) > 0 else 0
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
            
            expectancy = avg_pnl
            
            avg_bars_held = group['bars_held'].mean()
            
            # Calculate max drawdown
            cumulative_pnl = group.sort_values('entry_idx')['pnl'].cumsum()
            running_max = cumulative_pnl.expanding().max()
            drawdown = cumulative_pnl - running_max
            max_drawdown = drawdown.min()
            
            results[config_name] = {
                'total_trades': total_trades,
                'wins': win_count,
                'losses': loss_count,
                'win_rate': win_rate,
                'total_pnl': total_pnl,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'avg_pnl': avg_pnl,
                'expectancy': expectancy,
                'profit_factor': profit_factor,
                'max_drawdown': max_drawdown,
                'avg_bars_held': avg_bars_held,
                'avg_risk': group['risk'].mean()
            }
        
        return results


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV data in the format: Column1;Column2;Column3;Column4;Column5;Column6;Column7
    where Column1=Date, Column2=Time, Column3=Open, Column4=High, Column5=Low, Column6=Close, Column7=Volume
    """
    df = pd.read_csv(filepath, sep=';')
    
    # Parse datetime
    df['DateTime'] = pd.to_datetime(df['Column1'] + ' ' + df['Column2'], format='%d/%m/%Y %H:%M:%S')
    df['Date'] = df['DateTime'].dt.date
    df['Time'] = df['DateTime'].dt.time
    
    # Rename columns
    df['Open'] = df['Column3'].astype(float)
    df['High'] = df['Column4'].astype(float)
    df['Low'] = df['Column5'].astype(float)
    df['Close'] = df['Column6'].astype(float)
    df['Volume'] = df['Column7'].astype(float)
    
    # Keep only needed columns
    df = df[['DateTime', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    return df


def main():
    """Main execution function"""
    
    print("=" * 80)
    print("NQ LONDON CONTINUATION + INVERSION FVG BACKTEST")
    print("=" * 80)
    print()
    
    # Load NQ data
    print("Loading NQ data...")
    nq_2024 = load_data('/home/runner/work/Backtest-Trading/Backtest-Trading/2024 5m.csv')
    nq_2025 = load_data('/home/runner/work/Backtest-Trading/Backtest-Trading/2025 5m.csv')
    nq_data = pd.concat([nq_2024, nq_2025], ignore_index=True)
    print(f"Loaded {len(nq_data)} NQ 5m bars from 2024-2025")
    
    # Load ES data for SMT
    print("Loading ES data for SMT divergence...")
    es_data = load_data('/home/runner/work/Backtest-Trading/Backtest-Trading/ES 5m (2024-2025).csv')
    print(f"Loaded {len(es_data)} ES 5m bars")
    
    print()
    
    # Create strategy
    strategy = NQLondonContinuationStrategy(nq_data, es_data)
    
    # Run backtest
    print("Running backtest...")
    print()
    backtest_results = strategy.run_backtest()
    
    # Analyze results
    print()
    print("Analyzing results...")
    analysis = strategy.analyze_results(backtest_results)
    
    # Print results
    print()
    print("=" * 80)
    print("BACKTEST RESULTS")
    print("=" * 80)
    print()
    
    for config_name, stats in sorted(analysis.items()):
        print(f"\n{config_name}:")
        print("-" * 60)
        print(f"  Total Trades:    {stats['total_trades']}")
        print(f"  Wins:            {stats['wins']} ({stats['win_rate']*100:.1f}%)")
        print(f"  Losses:          {stats['losses']}")
        print(f"  Total P&L:       {stats['total_pnl']:.2f} pts")
        print(f"  Avg Win:         {stats['avg_win']:.2f} pts")
        print(f"  Avg Loss:        {stats['avg_loss']:.2f} pts")
        print(f"  Expectancy:      {stats['expectancy']:.2f} pts")
        print(f"  Profit Factor:   {stats['profit_factor']:.2f}")
        print(f"  Max Drawdown:    {stats['max_drawdown']:.2f} pts")
        print(f"  Avg Risk:        {stats['avg_risk']:.2f} pts")
        print(f"  Avg Bars Held:   {stats['avg_bars_held']:.1f}")
    
    # Save detailed results
    output_file = '/home/runner/work/Backtest-Trading/Backtest-Trading/nq_london_continuation_results.json'
    with open(output_file, 'w') as f:
        # Convert dates and booleans to strings for JSON serialization
        trades_serializable = []
        for trade in backtest_results['trades']:
            trade_copy = {}
            for key, value in trade.items():
                if isinstance(value, (date, datetime)):
                    trade_copy[key] = str(value)
                elif isinstance(value, bool):
                    trade_copy[key] = value  # JSON supports booleans
                elif isinstance(value, np.bool_):
                    trade_copy[key] = bool(value)
                elif isinstance(value, (np.integer, np.floating)):
                    trade_copy[key] = float(value)
                else:
                    trade_copy[key] = value
            trades_serializable.append(trade_copy)
        
        json.dump({
            'backtest_results': {
                'trades': trades_serializable,
                'total_days': backtest_results['total_days']
            },
            'analysis': analysis
        }, f, indent=2)
    
    print()
    print(f"Detailed results saved to: {output_file}")
    
    # Generate analysis report
    generate_analysis_report(backtest_results, analysis)


def generate_analysis_report(backtest_results: Dict, analysis: Dict):
    """Generate detailed analysis report answering the three key questions"""
    
    report = []
    report.append("=" * 80)
    report.append("NQ LONDON CONTINUATION + INVERSION FVG - ANALYSIS REPORT")
    report.append("=" * 80)
    report.append("")
    
    # Question 1: Retest vs Immediate Entry
    report.append("QUESTION 1: Retest Entry vs Immediate Entry")
    report.append("-" * 80)
    report.append("Does waiting for a retest of the Inversion FVG reduce drawdown?")
    report.append("")
    
    # Compare immediate vs retest for same SL and target
    retest_comparison = []
    for sl_type in ['A', 'B']:
        for target_type in ['asian_high', 'fixed_10', 'fixed_15', 'fixed_20']:
            immediate_key = f"SL_{sl_type}_{target_type}_immediate"
            retest_key = f"SL_{sl_type}_{target_type}_retest"
            
            if immediate_key in analysis and retest_key in analysis:
                imm = analysis[immediate_key]
                ret = analysis[retest_key]
                
                retest_comparison.append({
                    'config': f"SL_{sl_type}_{target_type}",
                    'immediate_trades': imm['total_trades'],
                    'retest_trades': ret['total_trades'],
                    'immediate_wr': imm['win_rate'],
                    'retest_wr': ret['win_rate'],
                    'immediate_exp': imm['expectancy'],
                    'retest_exp': ret['expectancy'],
                    'immediate_dd': imm['max_drawdown'],
                    'retest_dd': ret['max_drawdown']
                })
    
    for comp in retest_comparison:
        report.append(f"Configuration: {comp['config']}")
        report.append(f"  Immediate Entry:")
        report.append(f"    Trades: {comp['immediate_trades']}, Win Rate: {comp['immediate_wr']*100:.1f}%")
        report.append(f"    Expectancy: {comp['immediate_exp']:.2f} pts, Max DD: {comp['immediate_dd']:.2f} pts")
        report.append(f"  Retest Entry:")
        report.append(f"    Trades: {comp['retest_trades']}, Win Rate: {comp['retest_wr']*100:.1f}%")
        report.append(f"    Expectancy: {comp['retest_exp']:.2f} pts, Max DD: {comp['retest_dd']:.2f} pts")
        report.append(f"  Difference:")
        report.append(f"    Win Rate: {(comp['retest_wr'] - comp['immediate_wr'])*100:+.1f}%")
        report.append(f"    Expectancy: {(comp['retest_exp'] - comp['immediate_exp']):+.2f} pts")
        report.append(f"    Max DD: {(comp['retest_dd'] - comp['immediate_dd']):+.2f} pts")
        report.append("")
    
    # Question 2: SL A vs SL B
    report.append("")
    report.append("QUESTION 2: SL A (Aggressive) vs SL B (Structural)")
    report.append("-" * 80)
    report.append("Is the aggressive stop loss viable on NQ, or is structural better?")
    report.append("")
    
    sl_comparison = []
    for target_type in ['asian_high', 'fixed_10', 'fixed_15', 'fixed_20']:
        for entry_type in ['immediate', 'retest']:
            sl_a_key = f"SL_A_{target_type}_{entry_type}"
            sl_b_key = f"SL_B_{target_type}_{entry_type}"
            
            if sl_a_key in analysis and sl_b_key in analysis:
                sl_a = analysis[sl_a_key]
                sl_b = analysis[sl_b_key]
                
                sl_comparison.append({
                    'config': f"{target_type}_{entry_type}",
                    'sl_a_wr': sl_a['win_rate'],
                    'sl_b_wr': sl_b['win_rate'],
                    'sl_a_exp': sl_a['expectancy'],
                    'sl_b_exp': sl_b['expectancy'],
                    'sl_a_pf': sl_a['profit_factor'],
                    'sl_b_pf': sl_b['profit_factor'],
                    'sl_a_risk': sl_a['avg_risk'],
                    'sl_b_risk': sl_b['avg_risk']
                })
    
    for comp in sl_comparison:
        report.append(f"Configuration: {comp['config']}")
        report.append(f"  SL A (Aggressive):")
        report.append(f"    Win Rate: {comp['sl_a_wr']*100:.1f}%, Expectancy: {comp['sl_a_exp']:.2f} pts")
        report.append(f"    Profit Factor: {comp['sl_a_pf']:.2f}, Avg Risk: {comp['sl_a_risk']:.2f} pts")
        report.append(f"  SL B (Structural):")
        report.append(f"    Win Rate: {comp['sl_b_wr']*100:.1f}%, Expectancy: {comp['sl_b_exp']:.2f} pts")
        report.append(f"    Profit Factor: {comp['sl_b_pf']:.2f}, Avg Risk: {comp['sl_b_risk']:.2f} pts")
        report.append(f"  Winner: {'SL A' if comp['sl_a_exp'] > comp['sl_b_exp'] else 'SL B'} " +
                     f"(+{abs(comp['sl_a_exp'] - comp['sl_b_exp']):.2f} pts expectancy)")
        report.append("")
    
    # Question 3: Target Optimization
    report.append("")
    report.append("QUESTION 3: Target Optimization")
    report.append("-" * 80)
    report.append("Asian High vs Fixed Targets (10/15/20 pts)")
    report.append("")
    
    target_comparison = []
    for sl_type in ['A', 'B']:
        for entry_type in ['immediate', 'retest']:
            targets = {}
            for target_type in ['asian_high', 'fixed_10', 'fixed_15', 'fixed_20']:
                key = f"SL_{sl_type}_{target_type}_{entry_type}"
                if key in analysis:
                    targets[target_type] = analysis[key]
            
            if len(targets) > 0:
                target_comparison.append({
                    'config': f"SL_{sl_type}_{entry_type}",
                    'targets': targets
                })
    
    for comp in target_comparison:
        report.append(f"Configuration: {comp['config']}")
        best_target = None
        best_exp = -999
        for target_type, stats in comp['targets'].items():
            report.append(f"  {target_type}:")
            report.append(f"    Win Rate: {stats['win_rate']*100:.1f}%, Expectancy: {stats['expectancy']:.2f} pts")
            report.append(f"    Profit Factor: {stats['profit_factor']:.2f}")
            if stats['expectancy'] > best_exp:
                best_exp = stats['expectancy']
                best_target = target_type
        report.append(f"  Best Target: {best_target} ({best_exp:.2f} pts expectancy)")
        report.append("")
    
    # Summary and Recommendations
    report.append("")
    report.append("=" * 80)
    report.append("SUMMARY AND RECOMMENDATIONS")
    report.append("=" * 80)
    report.append("")
    
    # Find best overall configuration
    best_config = None
    best_expectancy = -999
    for config_name, stats in analysis.items():
        if stats['expectancy'] > best_expectancy and stats['total_trades'] >= 5:
            best_expectancy = stats['expectancy']
            best_config = config_name
    
    if best_config:
        best_stats = analysis[best_config]
        report.append(f"BEST CONFIGURATION: {best_config}")
        report.append(f"  Win Rate: {best_stats['win_rate']*100:.1f}%")
        report.append(f"  Expectancy: {best_stats['expectancy']:.2f} pts")
        report.append(f"  Profit Factor: {best_stats['profit_factor']:.2f}")
        report.append(f"  Total Trades: {best_stats['total_trades']}")
        report.append(f"  Total P&L: {best_stats['total_pnl']:.2f} pts")
    
    report.append("")
    report.append("=" * 80)
    
    # Save report
    report_file = '/home/runner/work/Backtest-Trading/Backtest-Trading/NQ_LONDON_CONTINUATION_ANALYSIS.md'
    with open(report_file, 'w') as f:
        f.write('\n'.join(report))
    
    print()
    print(f"Analysis report saved to: {report_file}")


if __name__ == '__main__':
    main()
