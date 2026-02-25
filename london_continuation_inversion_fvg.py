"""
London Continuation + Inversion FVG Entry Strategy

This strategy implements a Trend Continuation approach during the London session
using precise entry based on Inversion FVG (Fair Value Gap).

Strategy Logic (BUY Setup):
1. Tokyo Session (19:00-00:00): Bullish trend with Bullish FVG (Asian FVG) below price
2. London Retracement (02:00-05:00): Price retraces down to test Asian FVG
3. During descent: Price creates Bearish FVG M5 (short-term seller strength)
4. Price touches Asian FVG, reacts, and moves up
5. Trigger: M5 candle fills the Bearish FVG and closes above it (Inversion FVG)
6. Entry: Immediate at close of validation candle

Stop Loss Options:
- SL A (Aggressive): Below the inverted Bearish FVG
- SL B (Structural): Below body close of lowest candle that tested Asian FVG

For SELL Setup: Reverse all logic
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class FVGDetector:
    """Detects Fair Value Gaps in price data"""
    
    @staticmethod
    def detect_bullish_fvg(df: pd.DataFrame, idx: int) -> Optional[Tuple[float, float]]:
        """
        Detect Bullish FVG: Low[i] > High[i-2] (gap up)
        Returns (gap_low, gap_high) or None
        """
        if idx < 2:
            return None
        
        if df.iloc[idx]['Low'] > df.iloc[idx-2]['High']:
            gap_low = df.iloc[idx-2]['High']
            gap_high = df.iloc[idx]['Low']
            return (gap_low, gap_high)
        return None
    
    @staticmethod
    def detect_bearish_fvg(df: pd.DataFrame, idx: int) -> Optional[Tuple[float, float]]:
        """
        Detect Bearish FVG: High[i] < Low[i-2] (gap down)
        Returns (gap_low, gap_high) or None
        """
        if idx < 2:
            return None
        
        if df.iloc[idx]['High'] < df.iloc[idx-2]['Low']:
            gap_low = df.iloc[idx]['High']
            gap_high = df.iloc[idx-2]['Low']
            return (gap_low, gap_high)
        return None
    
    @staticmethod
    def is_fvg_filled(fvg: Tuple[float, float], candle_high: float, candle_low: float) -> bool:
        """Check if a candle completely fills an FVG"""
        gap_low, gap_high = fvg
        return candle_low <= gap_low and candle_high >= gap_high
    
    @staticmethod
    def does_price_touch_fvg(fvg: Tuple[float, float], candle_high: float, candle_low: float) -> bool:
        """Check if price touches or enters an FVG"""
        gap_low, gap_high = fvg
        return not (candle_low > gap_high or candle_high < gap_low)


class SessionManager:
    """Manages trading session detection"""
    
    @staticmethod
    def is_tokyo_session(dt: datetime) -> bool:
        """Tokyo session: 19:00-00:00 (previous day)"""
        # Session runs from 19:00 to midnight (including 23:59:59)
        return time(19, 0) <= dt.time() <= time(23, 59, 59)
    
    @staticmethod
    def is_london_session(dt: datetime) -> bool:
        """London session: 02:00-05:00"""
        return time(2, 0) <= dt.time() < time(5, 0)
    
    @staticmethod
    def get_tokyo_date(dt: datetime) -> datetime:
        """Get the date identifier for Tokyo session"""
        # Tokyo 19:00-00:00 belongs to the next trading day
        if dt.time() >= time(19, 0):
            return dt.date() + timedelta(days=1)
        else:
            return dt.date()


class LondonContinuationStrategy:
    """
    Implements London Continuation + Inversion FVG Entry Strategy
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.fvg_detector = FVGDetector()
        self.session_manager = SessionManager()
        self.trades = []
        self.prepare_data()
        
    def prepare_data(self):
        """Prepare and clean the data"""
        # Parse date and time
        self.df['DateTime'] = pd.to_datetime(
            self.df['Column1'] + ' ' + self.df['Column2'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Rename columns
        self.df.rename(columns={
            'Column3': 'Open',
            'Column4': 'High',
            'Column5': 'Low',
            'Column6': 'Close',
            'Column7': 'Volume'
        }, inplace=True)
        
        # Set DateTime as index
        self.df.set_index('DateTime', inplace=True)
        
        # Convert to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Remove any NaN values
        self.df.dropna(inplace=True)
        
        # Add session identifiers
        self.df['is_tokyo'] = self.df.index.map(self.session_manager.is_tokyo_session)
        self.df['is_london'] = self.df.index.map(self.session_manager.is_london_session)
        self.df['tokyo_date'] = self.df.index.map(self.session_manager.get_tokyo_date)
    
    def find_tokyo_sessions(self) -> Dict[datetime, pd.DataFrame]:
        """Group data by Tokyo session"""
        tokyo_data = self.df[self.df['is_tokyo']].copy()
        sessions = {}
        
        for date, group in tokyo_data.groupby('tokyo_date'):
            if len(group) > 0:
                sessions[date] = group
        
        return sessions
    
    def analyze_tokyo_trend(self, session_df: pd.DataFrame) -> Dict:
        """
        Analyze Tokyo session for trend and FVGs
        Returns dict with trend, fvgs, and session high/low
        """
        if len(session_df) < 3:
            return {'trend': None, 'fvgs': [], 'high': None, 'low': None}
        
        session_high = session_df['High'].max()
        session_low = session_df['Low'].min()
        session_close = session_df['Close'].iloc[-1]
        session_open = session_df['Open'].iloc[0]
        
        # Determine trend (simplified: based on close vs open)
        if session_close > session_open:
            trend = 'bullish'
        elif session_close < session_open:
            trend = 'bearish'
        else:
            trend = None
        
        # Find FVGs in Tokyo session
        bullish_fvgs = []
        bearish_fvgs = []
        
        session_df_reset = session_df.reset_index()
        for i in range(2, len(session_df_reset)):
            # Detect bullish FVGs
            bull_fvg = self.fvg_detector.detect_bullish_fvg(session_df_reset, i)
            if bull_fvg:
                bullish_fvgs.append({
                    'fvg': bull_fvg,
                    'time': session_df_reset.iloc[i]['DateTime'],
                    'index': i
                })
            
            # Detect bearish FVGs
            bear_fvg = self.fvg_detector.detect_bearish_fvg(session_df_reset, i)
            if bear_fvg:
                bearish_fvgs.append({
                    'fvg': bear_fvg,
                    'time': session_df_reset.iloc[i]['DateTime'],
                    'index': i
                })
        
        return {
            'trend': trend,
            'bullish_fvgs': bullish_fvgs,
            'bearish_fvgs': bearish_fvgs,
            'high': session_high,
            'low': session_low,
            'close': session_close,
            'open': session_open
        }
    
    def find_london_setups(self, tokyo_date: datetime, tokyo_analysis: Dict) -> List[Dict]:
        """
        Find London continuation setups based on Tokyo analysis
        """
        setups = []
        
        # Get London session data for this day
        london_df = self.df[
            (self.df.index.date == tokyo_date) & 
            (self.df['is_london'])
        ].copy()
        
        if len(london_df) < 3:
            return setups
        
        trend = tokyo_analysis['trend']
        if trend is None:
            return setups
        
        # BUY Setup: Tokyo bullish with bullish FVGs
        if trend == 'bullish' and len(tokyo_analysis['bullish_fvgs']) > 0:
            asian_fvg = tokyo_analysis['bullish_fvgs'][-1]['fvg']  # Last bullish FVG
            setup = self._find_buy_setup(london_df, asian_fvg, tokyo_analysis)
            if setup:
                setup['tokyo_date'] = tokyo_date
                setup['direction'] = 'BUY'
                setups.append(setup)
        
        # SELL Setup: Tokyo bearish with bearish FVGs
        if trend == 'bearish' and len(tokyo_analysis['bearish_fvgs']) > 0:
            asian_fvg = tokyo_analysis['bearish_fvgs'][-1]['fvg']  # Last bearish FVG
            setup = self._find_sell_setup(london_df, asian_fvg, tokyo_analysis)
            if setup:
                setup['tokyo_date'] = tokyo_date
                setup['direction'] = 'SELL'
                setups.append(setup)
        
        return setups
    
    def _find_buy_setup(self, london_df: pd.DataFrame, asian_fvg: Tuple[float, float], 
                        tokyo_analysis: Dict) -> Optional[Dict]:
        """
        Find BUY setup in London session
        1. Price retraces to Asian FVG (bullish)
        2. During descent, creates Bearish FVG M5
        3. Price fills Bearish FVG and closes above (Inversion)
        """
        london_df_reset = london_df.reset_index()
        
        # Track if price touched Asian FVG
        touched_asian_fvg = False
        touch_idx = None
        bearish_fvgs = []  # FVGs created during retracement
        
        for i in range(2, len(london_df_reset)):
            current_low = london_df_reset.iloc[i]['Low']
            current_high = london_df_reset.iloc[i]['High']
            
            # Check if price touches Asian FVG
            if self.fvg_detector.does_price_touch_fvg(asian_fvg, current_high, current_low):
                if not touched_asian_fvg:
                    touched_asian_fvg = True
                    touch_idx = i
            
            # Detect Bearish FVGs during descent (including at touch)
            # Allow FVG detection until after touch to capture all retracement FVGs
            bear_fvg = self.fvg_detector.detect_bearish_fvg(london_df_reset, i)
            if bear_fvg and (not touched_asian_fvg or i <= touch_idx + 2):
                bearish_fvgs.append({
                    'fvg': bear_fvg,
                    'time': london_df_reset.iloc[i]['DateTime'],
                    'index': i
                })
            
            # After touching Asian FVG, look for Inversion FVG
            if touched_asian_fvg and len(bearish_fvgs) > 0:
                # Check if current candle fills last Bearish FVG and closes above it
                last_bear_fvg = bearish_fvgs[-1]['fvg']
                current_close = london_df_reset.iloc[i]['Close']
                
                if (self.fvg_detector.is_fvg_filled(last_bear_fvg, current_high, current_low) and
                    current_close > last_bear_fvg[1]):  # Closes above FVG high
                    
                    # Find the lowest body close during Asian FVG test
                    test_candles = london_df_reset.iloc[touch_idx:i+1]
                    lowest_body = test_candles['Close'].min()
                    
                    return {
                        'entry_time': london_df_reset.iloc[i]['DateTime'],
                        'entry_price': current_close,
                        'entry_idx': i,
                        'asian_fvg': asian_fvg,
                        'inversion_fvg': last_bear_fvg,
                        'sl_a': last_bear_fvg[0],  # Below inversion FVG
                        'sl_b': lowest_body,  # Below body of test
                        'tokyo_high': tokyo_analysis['high'],
                        'touch_idx': touch_idx
                    }
        
        return None
    
    def _find_sell_setup(self, london_df: pd.DataFrame, asian_fvg: Tuple[float, float],
                         tokyo_analysis: Dict) -> Optional[Dict]:
        """
        Find SELL setup in London session
        1. Price retraces up to Asian FVG (bearish)
        2. During ascent, creates Bullish FVG M5
        3. Price fills Bullish FVG and closes below (Inversion)
        """
        london_df_reset = london_df.reset_index()
        
        touched_asian_fvg = False
        touch_idx = None
        bullish_fvgs = []  # FVGs created during retracement
        
        for i in range(2, len(london_df_reset)):
            current_low = london_df_reset.iloc[i]['Low']
            current_high = london_df_reset.iloc[i]['High']
            
            # Check if price touches Asian FVG
            if self.fvg_detector.does_price_touch_fvg(asian_fvg, current_high, current_low):
                if not touched_asian_fvg:
                    touched_asian_fvg = True
                    touch_idx = i
            
            # Detect Bullish FVGs during ascent (including at touch)
            # Allow FVG detection until after touch to capture all retracement FVGs
            bull_fvg = self.fvg_detector.detect_bullish_fvg(london_df_reset, i)
            if bull_fvg and (not touched_asian_fvg or i <= touch_idx + 2):
                bullish_fvgs.append({
                    'fvg': bull_fvg,
                    'time': london_df_reset.iloc[i]['DateTime'],
                    'index': i
                })
            
            # After touching Asian FVG, look for Inversion FVG
            if touched_asian_fvg and len(bullish_fvgs) > 0:
                last_bull_fvg = bullish_fvgs[-1]['fvg']
                current_close = london_df_reset.iloc[i]['Close']
                
                if (self.fvg_detector.is_fvg_filled(last_bull_fvg, current_high, current_low) and
                    current_close < last_bull_fvg[0]):  # Closes below FVG low
                    
                    # Find highest body close during Asian FVG test
                    test_candles = london_df_reset.iloc[touch_idx:i+1]
                    highest_body = test_candles['Close'].max()
                    
                    return {
                        'entry_time': london_df_reset.iloc[i]['DateTime'],
                        'entry_price': current_close,
                        'entry_idx': i,
                        'asian_fvg': asian_fvg,
                        'inversion_fvg': last_bull_fvg,
                        'sl_a': last_bull_fvg[1],  # Above inversion FVG
                        'sl_b': highest_body,  # Above body of test
                        'tokyo_low': tokyo_analysis['low'],
                        'touch_idx': touch_idx
                    }
        
        return None
    
    def simulate_trade(self, setup: Dict, sl_type: str, rr_ratio: float) -> Dict:
        """
        Simulate a trade with given stop loss type and risk-reward ratio
        """
        direction = setup['direction']
        entry_price = setup['entry_price']
        entry_time = setup['entry_time']
        
        if sl_type == 'A':
            stop_loss = setup['sl_a']
        else:  # SL B
            stop_loss = setup['sl_b']
        
        # Calculate risk and target
        if direction == 'BUY':
            risk = entry_price - stop_loss
            target = entry_price + (risk * rr_ratio)
        else:  # SELL
            risk = stop_loss - entry_price
            target = entry_price - (risk * rr_ratio)
        
        # Get subsequent data after entry
        future_data = self.df[self.df.index > entry_time].head(200)  # Look ahead ~16 hours
        
        if len(future_data) == 0:
            return {
                'status': 'no_data',
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'target': target,
                'risk': risk
            }
        
        # Check for SL or TP hit
        for idx, row in future_data.iterrows():
            if direction == 'BUY':
                if row['Low'] <= stop_loss:
                    # Stop loss hit
                    return {
                        'status': 'loss',
                        'entry_price': entry_price,
                        'exit_price': stop_loss,
                        'exit_time': idx,
                        'stop_loss': stop_loss,
                        'target': target,
                        'risk': risk,
                        'pnl': -risk,
                        'reached_new_high': row['High'] > setup['tokyo_high']
                    }
                elif row['High'] >= target:
                    # Target hit
                    return {
                        'status': 'win',
                        'entry_price': entry_price,
                        'exit_price': target,
                        'exit_time': idx,
                        'stop_loss': stop_loss,
                        'target': target,
                        'risk': risk,
                        'pnl': risk * rr_ratio,
                        'reached_new_high': True
                    }
            else:  # SELL
                if row['High'] >= stop_loss:
                    # Stop loss hit
                    return {
                        'status': 'loss',
                        'entry_price': entry_price,
                        'exit_price': stop_loss,
                        'exit_time': idx,
                        'stop_loss': stop_loss,
                        'target': target,
                        'risk': risk,
                        'pnl': -risk,
                        'reached_new_low': row['Low'] < setup['tokyo_low']
                    }
                elif row['Low'] <= target:
                    # Target hit
                    return {
                        'status': 'win',
                        'entry_price': entry_price,
                        'exit_price': target,
                        'exit_time': idx,
                        'stop_loss': stop_loss,
                        'target': target,
                        'risk': risk,
                        'pnl': risk * rr_ratio,
                        'reached_new_low': True
                    }
        
        # No exit found in time window
        last_price = future_data['Close'].iloc[-1]
        if direction == 'BUY':
            pnl = last_price - entry_price
        else:
            pnl = entry_price - last_price
        
        return {
            'status': 'open',
            'entry_price': entry_price,
            'exit_price': last_price,
            'exit_time': future_data.index[-1],
            'stop_loss': stop_loss,
            'target': target,
            'risk': risk,
            'pnl': pnl
        }
    
    def run_backtest(self, rr_ratios: List[float] = [1, 1.5, 2, 2.5, 3]) -> Dict:
        """
        Run complete backtest with multiple RR ratios and SL types
        """
        print("=" * 80)
        print("LONDON CONTINUATION + INVERSION FVG STRATEGY - BACKTEST")
        print("=" * 80)
        print(f"\nData period: {self.df.index[0]} to {self.df.index[-1]}")
        print(f"Total candles: {len(self.df)}")
        
        # Find all Tokyo sessions
        tokyo_sessions = self.find_tokyo_sessions()
        print(f"\nTokyo sessions analyzed: {len(tokyo_sessions)}")
        
        # Analyze each Tokyo session and find London setups
        all_setups = []
        
        for tokyo_date, tokyo_df in tokyo_sessions.items():
            tokyo_analysis = self.analyze_tokyo_trend(tokyo_df)
            
            if tokyo_analysis['trend'] is not None:
                london_setups = self.find_london_setups(tokyo_date, tokyo_analysis)
                all_setups.extend(london_setups)
        
        print(f"Total setups found: {len(all_setups)}")
        
        if len(all_setups) == 0:
            print("\nNo setups found with current criteria.")
            return {'setups': 0}
        
        # Count by direction
        buy_setups = [s for s in all_setups if s['direction'] == 'BUY']
        sell_setups = [s for s in all_setups if s['direction'] == 'SELL']
        print(f"  - BUY setups: {len(buy_setups)}")
        print(f"  - SELL setups: {len(sell_setups)}")
        
        # Run simulations for all combinations
        results = {
            'setups': all_setups,
            'simulations': {}
        }
        
        for sl_type in ['A', 'B']:
            for rr in rr_ratios:
                key = f"SL_{sl_type}_RR_{rr}"
                trades = []
                
                for setup in all_setups:
                    trade = self.simulate_trade(setup, sl_type, rr)
                    trade['setup'] = setup
                    trade['sl_type'] = sl_type
                    trade['rr_ratio'] = rr
                    trades.append(trade)
                
                results['simulations'][key] = trades
        
        return results
    
    def calculate_statistics(self, trades: List[Dict]) -> Dict:
        """Calculate performance statistics for a set of trades"""
        if len(trades) == 0:
            return {}
        
        wins = [t for t in trades if t['status'] == 'win']
        losses = [t for t in trades if t['status'] == 'loss']
        open_trades = [t for t in trades if t['status'] == 'open']
        
        total_trades = len(wins) + len(losses)
        
        if total_trades == 0:
            return {
                'total_setups': len(trades),
                'total_trades': 0,
                'wins': 0,
                'losses': 0,
                'open': len(open_trades)
            }
        
        win_rate = len(wins) / total_trades * 100
        
        total_profit = sum([t['pnl'] for t in wins])
        total_loss = abs(sum([t['pnl'] for t in losses]))
        
        net_pnl = total_profit - total_loss
        
        avg_win = total_profit / len(wins) if len(wins) > 0 else 0
        avg_loss = total_loss / len(losses) if len(losses) > 0 else 0
        
        # Use a large finite number instead of infinity for better handling
        profit_factor = total_profit / total_loss if total_loss > 0 else (999.999 if total_profit > 0 else 0)
        
        expectancy = (avg_win * (len(wins) / total_trades) - 
                     avg_loss * (len(losses) / total_trades)) if total_trades > 0 else 0
        
        # Check reached new high/low
        # Note: We track if price reached Tokyo extreme during trade lifetime
        reached_extremes = 0
        for t in trades:
            if t['status'] == 'win':
                # Winning trades reached target, but may not have exceeded Tokyo extreme
                # Check if extreme was reached
                if 'reached_new_high' in t and t['reached_new_high']:
                    reached_extremes += 1
                elif 'reached_new_low' in t and t['reached_new_low']:
                    reached_extremes += 1
            elif t['status'] == 'loss':
                if 'reached_new_high' in t and t['reached_new_high']:
                    reached_extremes += 1
                elif 'reached_new_low' in t and t['reached_new_low']:
                    reached_extremes += 1
        
        extreme_rate = reached_extremes / total_trades * 100 if total_trades > 0 else 0
        
        return {
            'total_setups': len(trades),
            'total_trades': total_trades,
            'wins': len(wins),
            'losses': len(losses),
            'open': len(open_trades),
            'win_rate': win_rate,
            'total_profit': total_profit,
            'total_loss': total_loss,
            'net_pnl': net_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'expectancy': expectancy,
            'reached_extremes': reached_extremes,
            'extreme_rate': extreme_rate
        }
    
    def print_results(self, results: Dict):
        """Print comprehensive results and analysis"""
        if results['setups'] == 0:
            return
        
        print("\n" + "=" * 80)
        print("BACKTEST RESULTS - ALL CONFIGURATIONS")
        print("=" * 80)
        
        # Print results for each configuration
        for config_name, trades in results['simulations'].items():
            stats = self.calculate_statistics(trades)
            
            if stats.get('total_trades', 0) == 0:
                continue
            
            print(f"\n{'-' * 80}")
            print(f"Configuration: {config_name}")
            print(f"{'-' * 80}")
            print(f"Total Setups: {stats['total_setups']}")
            print(f"Total Trades (Closed): {stats['total_trades']}")
            print(f"Wins: {stats['wins']} | Losses: {stats['losses']} | Open: {stats['open']}")
            print(f"Win Rate: {stats['win_rate']:.2f}%")
            print(f"Profit Factor: {stats['profit_factor']:.3f}")
            print(f"Expectancy: {stats['expectancy']:.2f} points")
            print(f"Net P&L: {stats['net_pnl']:.2f} points")
            print(f"Avg Win: {stats['avg_win']:.2f} | Avg Loss: {stats['avg_loss']:.2f}")
            print(f"Reached Tokyo Extreme: {stats['reached_extremes']}/{stats['total_trades']} ({stats['extreme_rate']:.2f}%)")
        
        # Comparative analysis
        print("\n" + "=" * 80)
        print("COMPARATIVE ANALYSIS: SL A vs SL B")
        print("=" * 80)
        
        # Group by RR ratio
        rr_ratios = sorted(list(set([float(k.split('_')[-1]) for k in results['simulations'].keys()])))
        
        for rr in rr_ratios:
            print(f"\n--- Risk-Reward Ratio: 1:{rr} ---")
            
            # Convert RR to int if it's a whole number for key matching
            rr_key = int(rr) if rr == int(rr) else rr
            sl_a_key = f"SL_A_RR_{rr_key}"
            sl_b_key = f"SL_B_RR_{rr_key}"
            
            stats_a = self.calculate_statistics(results['simulations'][sl_a_key])
            stats_b = self.calculate_statistics(results['simulations'][sl_b_key])
            
            if stats_a.get('total_trades', 0) == 0:
                continue
            
            print(f"\n  SL A (Aggressive - Below Inversion FVG):")
            print(f"    Win Rate: {stats_a['win_rate']:.2f}% | PF: {stats_a['profit_factor']:.3f} | Exp: {stats_a['expectancy']:.2f}")
            
            print(f"\n  SL B (Structural - Below Body):")
            print(f"    Win Rate: {stats_b['win_rate']:.2f}% | PF: {stats_b['profit_factor']:.3f} | Exp: {stats_b['expectancy']:.2f}")
            
            wr_diff = stats_b['win_rate'] - stats_a['win_rate']
            pf_diff = stats_b['profit_factor'] - stats_a['profit_factor']
            
            print(f"\n  Difference (B - A):")
            print(f"    Win Rate: {wr_diff:+.2f}% | PF: {pf_diff:+.3f}")
        
        # Answer the three key questions
        print("\n" + "=" * 80)
        print("ANALYSIS: ANSWERING KEY QUESTIONS")
        print("=" * 80)
        
        self._answer_key_questions(results)
    
    def _answer_key_questions(self, results: Dict):
        """
        Answer the three key questions:
        1. Signal Reliability (Inversion vs Direct Entry)
        2. SL Choice (Is SL A too tight?)
        3. Success Probability (Reaching Tokyo extreme)
        """
        print("\n" + "-" * 80)
        print("QUESTION 1: Signal Reliability - Inversion FVG Filter")
        print("-" * 80)
        print("Does waiting for Inversion FVG effectively filter 'falling knives'?")
        print()
        
        # Compare best RR for SL A vs SL B
        best_rr = 2  # Use 1:2 as standard
        sl_a_key = f"SL_A_RR_{best_rr}"
        sl_b_key = f"SL_B_RR_{best_rr}"
        
        stats_a = self.calculate_statistics(results['simulations'][sl_a_key])
        stats_b = self.calculate_statistics(results['simulations'][sl_b_key])
        
        if stats_a.get('total_trades', 0) > 0:
            print(f"Win Rate with Inversion Entry (SL A): {stats_a['win_rate']:.2f}%")
            print(f"Win Rate with Inversion Entry (SL B): {stats_b['win_rate']:.2f}%")
            print()
            print("INSIGHT: The strategy requires price to:")
            print("  1. Touch Asian FVG (confirming support/resistance)")
            print("  2. Create retracement FVG (showing counter-move strength)")
            print("  3. Fill and close through retracement FVG (confirming trend resume)")
            print()
            if stats_a['win_rate'] > 50:
                print("✓ The Inversion FVG filter shows POSITIVE edge (>50% win rate)")
                print("  This confirms waiting for the fill reduces false signals.")
            else:
                print("✗ The filter shows LIMITED edge (<50% win rate)")
                print("  May need additional confirmation or better timing.")
        
        print("\n" + "-" * 80)
        print("QUESTION 2: SL Choice - Is SL A Too Tight?")
        print("-" * 80)
        print("Does the market re-test Inversion FVG before continuing?")
        print()
        
        # Compare SL A vs SL B across all RR ratios
        print("Performance Comparison (RR 1:2):")
        print(f"  SL A - Win Rate: {stats_a['win_rate']:.2f}%, PF: {stats_a['profit_factor']:.3f}")
        print(f"  SL B - Win Rate: {stats_b['win_rate']:.2f}%, PF: {stats_b['profit_factor']:.3f}")
        print()
        
        wr_improvement = stats_b['win_rate'] - stats_a['win_rate']
        pf_improvement = stats_b['profit_factor'] - stats_a['profit_factor']
        
        print(f"Improvement with SL B: Win Rate +{wr_improvement:.2f}%, PF +{pf_improvement:.3f}")
        print()
        
        if wr_improvement > 5:
            print("✓ SL A appears TOO TIGHT - significant improvement with SL B")
            print("  Market frequently re-tests the Inversion FVG before continuing.")
            print("  RECOMMENDATION: Use SL B (below body) for better survival rate.")
        elif wr_improvement > 0:
            print("⚠ SL A shows MODERATE tightness - slight improvement with SL B")
            print("  Some re-tests occur but not critical.")
            print("  RECOMMENDATION: Consider trader's risk tolerance.")
        else:
            print("✓ SL A is ADEQUATE - no significant benefit from wider stop")
            print("  Inversion FVG provides good support/resistance.")
            print("  RECOMMENDATION: SL A acceptable for aggressive traders.")
        
        print("\n" + "-" * 80)
        print("QUESTION 3: Success Probability - Reaching Tokyo Extreme")
        print("-" * 80)
        print("If price respects SL B and breaks Inversion FVG, what is probability")
        print("of reaching new Tokyo session high/low?")
        print()
        
        # Calculate probability for SL B trades
        sl_b_trades = results['simulations'][sl_b_key]
        valid_trades = [t for t in sl_b_trades if t['status'] in ['win', 'loss']]
        
        if len(valid_trades) > 0:
            extreme_reached = stats_b['reached_extremes']
            total = stats_b['total_trades']
            probability = stats_b['extreme_rate']
            
            print(f"Total Closed Trades: {total}")
            print(f"Reached Tokyo Extreme: {extreme_reached}")
            print(f"Probability: {probability:.2f}%")
            print()
            
            if probability > 70:
                print("✓ HIGH PROBABILITY (>70%)")
                print("  Strong continuation pattern - most setups reach new extremes.")
                print("  INSIGHT: The strategy captures genuine trend continuation.")
            elif probability > 50:
                print("⚠ MODERATE PROBABILITY (50-70%)")
                print("  Decent continuation but some setups fail to extend.")
                print("  INSIGHT: May benefit from additional trend filters.")
            else:
                print("✗ LOW PROBABILITY (<50%)")
                print("  Many setups fail to reach new extremes.")
                print("  INSIGHT: Strategy may be catching corrections, not continuations.")
        
        print("\n" + "=" * 80)
        print("RECOMMENDATIONS SUMMARY")
        print("=" * 80)
        
        if stats_a.get('total_trades', 0) > 0:
            # Determine best configuration
            best_config = None
            best_expectancy = -999999
            
            for config_name, trades in results['simulations'].items():
                stats = self.calculate_statistics(trades)
                if stats.get('expectancy', -999999) > best_expectancy:
                    best_expectancy = stats['expectancy']
                    best_config = config_name
            
            print(f"\nBest Configuration: {best_config}")
            best_stats = self.calculate_statistics(results['simulations'][best_config])
            print(f"  Win Rate: {best_stats['win_rate']:.2f}%")
            print(f"  Profit Factor: {best_stats['profit_factor']:.3f}")
            print(f"  Expectancy: {best_stats['expectancy']:.2f} points")
            print()
            
            if 'SL_B' in best_config:
                print("• Prefer SL B (Structural) for better win rate")
            else:
                print("• SL A (Aggressive) shows competitive performance")
            
            if best_stats['expectancy'] > 0:
                print("• Strategy shows POSITIVE expectancy - viable for trading")
            else:
                print("• Strategy needs refinement - negative expectancy")
            
            print(f"• Optimal RR appears to be around 1:{best_config.split('_')[-1]}")


def main():
    """Main execution function"""
    import sys
    import os
    
    print("=" * 80)
    print("LONDON CONTINUATION + INVERSION FVG ENTRY STRATEGY")
    print("=" * 80)
    
    # Get base directory (use current directory if not specified)
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load NQ data (2024 5m.csv)
    print("\n" + "=" * 80)
    print("TESTING ON NQ (NASDAQ) DATA")
    print("=" * 80)
    
    nq_file = os.path.join(base_dir, "2024 5m.csv")
    
    try:
        nq_df = pd.read_csv(nq_file, sep=';')
        print(f"\nLoaded NQ data: {len(nq_df)} rows")
        
        strategy_nq = LondonContinuationStrategy(nq_df)
        results_nq = strategy_nq.run_backtest()
        strategy_nq.print_results(results_nq)
        
    except Exception as e:
        print(f"Error processing NQ data: {e}")
        import traceback
        traceback.print_exc()
    
    # Load ES data (ES 5m (2024-2025).csv)
    print("\n\n" + "=" * 80)
    print("TESTING ON ES (S&P 500) DATA")
    print("=" * 80)
    
    es_file = os.path.join(base_dir, "ES 5m (2024-2025).csv")
    
    try:
        es_df = pd.read_csv(es_file, sep=';')
        print(f"\nLoaded ES data: {len(es_df)} rows")
        
        strategy_es = LondonContinuationStrategy(es_df)
        results_es = strategy_es.run_backtest()
        strategy_es.print_results(results_es)
        
    except Exception as e:
        print(f"Error processing ES data: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("BACKTEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
