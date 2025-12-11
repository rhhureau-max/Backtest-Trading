"""
ICT FVG Reversal Strategy - 4 Variants Comparison
==================================================

Compares 4 different execution strategies for FVG reversal trading:
1. The Conservative - Safe entry at proximal line, structural SL, liquidity target
2. The Sniper - 50% FVG entry, tight SL, 3R target
3. The Algo Run - Proximal entry, structural SL, 2.5 SD target
4. Silver Bullet Style - First valid FVG, fixed 25pt SL, fixed 50pt TP

All strategies share the same setup logic:
- Liquidity Sweep (20-bar low violated) on 15m
- Market Structure Shift (MSS) with displacement
- FVG formation in opposite direction
- Entry window: 01:00-04:00 only
"""

import pandas as pd
import numpy as np
from datetime import time
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class FVGReversalVariants:
    """
    Compare 4 execution variants of FVG reversal strategy
    """
    
    def __init__(self, capital: float = 100000, risk_per_trade: float = 0.01):
        """
        Initialize with capital and risk parameters
        
        Args:
            capital: Starting capital in USD
            risk_per_trade: Risk percentage per trade
        """
        self.capital = capital
        self.risk_per_trade = risk_per_trade
        self.point_value = 20  # NQ point value
        
        # Time window configuration
        self.entry_start = time(1, 0)   # 01:00
        self.entry_end = time(4, 0)     # 04:00
        
        # Variant configurations
        self.variants = {
            'Conservative': {
                'entry_type': 'proximal',
                'sl_type': 'structural',
                'tp_type': 'liquidity',
                'description': 'Safe entry, structural stop, liquidity target'
            },
            'Sniper': {
                'entry_type': 'ce_50',
                'sl_type': 'displacement',
                'tp_type': 'fixed_rr',
                'rr_ratio': 3.0,
                'description': 'CE 50% entry, tight stop, 3R target'
            },
            'Algo_Run': {
                'entry_type': 'proximal',
                'sl_type': 'structural',
                'tp_type': 'std_dev',
                'std_multiplier': 2.5,
                'description': 'Proximal entry, structural stop, 2.5 SD target'
            },
            'Silver_Bullet': {
                'entry_type': 'proximal',
                'sl_type': 'fixed',
                'sl_points': 25,
                'tp_type': 'fixed',
                'tp_points': 50,
                'description': 'First FVG, fixed 25pt SL, fixed 50pt TP'
            }
        }
        
        self.results = {}
    
    def load_data(self, timeframe: str, year: int) -> pd.DataFrame:
        """Load CSV data for specific timeframe and year"""
        filename = f"/home/runner/work/Backtest-Trading/Backtest-Trading/{year} {timeframe}.csv"
        
        df = pd.read_csv(filename, sep=';')
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        df.set_index('DateTime', inplace=True)
        df.drop(['Date', 'Time'], axis=1, inplace=True)
        
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df.sort_index(inplace=True)
        return df
    
    def detect_liquidity_sweep(self, df: pd.DataFrame, idx: int, lookback: int = 20) -> Tuple[bool, str, float]:
        """
        Detect liquidity sweep - 20-bar low/high violated
        
        Returns:
            (has_sweep, direction, swept_level)
        """
        if idx < lookback + 5:
            return False, '', 0.0
        
        lookback_data = df.iloc[max(0, idx-lookback-5):idx-2]
        
        # Check for low sweep (bullish setup)
        if len(lookback_data) >= lookback:
            swing_low = lookback_data['Low'].min()
            recent_low = df.iloc[idx-2:idx]['Low'].min()
            
            if recent_low < swing_low:
                # Price swept below the swing low
                return True, 'bullish', swing_low
        
        # Check for high sweep (bearish setup)
        if len(lookback_data) >= lookback:
            swing_high = lookback_data['High'].max()
            recent_high = df.iloc[idx-2:idx]['High'].max()
            
            if recent_high > swing_high:
                # Price swept above the swing high
                return True, 'bearish', swing_high
        
        return False, '', 0.0
    
    def detect_mss_with_displacement(self, df: pd.DataFrame, idx: int, direction: str) -> Tuple[bool, float, float]:
        """
        Detect Market Structure Shift with displacement
        
        Returns:
            (has_mss, mss_high, mss_low) - range of the MSS move
        """
        if idx < 30:
            return False, 0.0, 0.0
        
        # Look for structure break in last 10 bars
        recent_data = df.iloc[idx-10:idx]
        
        if direction == 'bullish':
            # Need to see price breaking above recent structure
            prev_data = df.iloc[max(0, idx-30):idx-10]
            if len(prev_data) > 0:
                resistance = prev_data['High'].quantile(0.75)
                if recent_data['High'].max() > resistance:
                    # MSS detected
                    mss_low = recent_data['Low'].min()
                    mss_high = recent_data['High'].max()
                    
                    # Check for displacement (strong move)
                    displacement_candle = recent_data.iloc[-1]
                    body_size = abs(displacement_candle['Close'] - displacement_candle['Open'])
                    avg_body = abs(df.iloc[idx-20:idx-1]['Close'] - df.iloc[idx-20:idx-1]['Open']).mean()
                    
                    if body_size > avg_body * 1.5:
                        return True, mss_high, mss_low
        
        elif direction == 'bearish':
            # Need to see price breaking below recent structure
            prev_data = df.iloc[max(0, idx-30):idx-10]
            if len(prev_data) > 0:
                support = prev_data['Low'].quantile(0.25)
                if recent_data['Low'].min() < support:
                    # MSS detected
                    mss_high = recent_data['High'].max()
                    mss_low = recent_data['Low'].min()
                    
                    # Check for displacement
                    displacement_candle = recent_data.iloc[-1]
                    body_size = abs(displacement_candle['Close'] - displacement_candle['Open'])
                    avg_body = abs(df.iloc[idx-20:idx-1]['Close'] - df.iloc[idx-20:idx-1]['Open']).mean()
                    
                    if body_size > avg_body * 1.5:
                        return True, mss_high, mss_low
        
        return False, 0.0, 0.0
    
    def detect_fvg(self, df: pd.DataFrame, idx: int, direction: str) -> Tuple[bool, float, float, float]:
        """
        Detect Fair Value Gap in specified direction
        
        Returns:
            (has_fvg, fvg_high, fvg_low, ce_price)
        """
        if idx < 3:
            return False, 0.0, 0.0, 0.0
        
        if direction == 'bullish':
            # Bullish FVG: Low[i] > High[i-2]
            if df['Low'].iloc[idx] > df['High'].iloc[idx-2]:
                fvg_low = df['High'].iloc[idx-2]
                fvg_high = df['Low'].iloc[idx]
                ce_price = (fvg_high + fvg_low) / 2
                return True, fvg_high, fvg_low, ce_price
        
        elif direction == 'bearish':
            # Bearish FVG: High[i] < Low[i-2]
            if df['High'].iloc[idx] < df['Low'].iloc[idx-2]:
                fvg_high = df['Low'].iloc[idx-2]
                fvg_low = df['High'].iloc[idx]
                ce_price = (fvg_high + fvg_low) / 2
                return True, fvg_high, fvg_low, ce_price
        
        return False, 0.0, 0.0, 0.0
    
    def calculate_entry_price(self, entry_type: str, direction: str, fvg_high: float, 
                             fvg_low: float, ce_price: float) -> float:
        """Calculate entry price based on variant"""
        if entry_type == 'proximal':
            # Enter at proximal line (entry boundary)
            return fvg_low if direction == 'bullish' else fvg_high
        
        elif entry_type == 'ce_50':
            # Enter at 50% CE
            return ce_price
        
        return 0.0
    
    def calculate_stop_loss(self, sl_type: str, direction: str, df: pd.DataFrame, 
                           idx: int, fvg_high: float, fvg_low: float, 
                           mss_high: float, mss_low: float, sl_points: float = None) -> float:
        """Calculate stop loss based on variant"""
        if sl_type == 'structural':
            # Place at structural swing
            lookback_data = df.iloc[max(0, idx-30):idx]
            if direction == 'bullish':
                return lookback_data['Low'].min() - 2.0
            else:
                return lookback_data['High'].max() + 2.0
        
        elif sl_type == 'displacement':
            # Tight stop behind displacement candle
            displacement_candle = df.iloc[idx-1]
            if direction == 'bullish':
                return displacement_candle['Low'] - 2.0
            else:
                return displacement_candle['High'] + 2.0
        
        elif sl_type == 'fixed' and sl_points:
            # Fixed points stop
            entry = fvg_low if direction == 'bullish' else fvg_high
            if direction == 'bullish':
                return entry - sl_points
            else:
                return entry + sl_points
        
        return 0.0
    
    def calculate_take_profit(self, tp_type: str, direction: str, entry_price: float,
                             stop_loss: float, df: pd.DataFrame, idx: int,
                             mss_high: float, mss_low: float, 
                             rr_ratio: float = None, std_multiplier: float = None,
                             tp_points: float = None) -> float:
        """Calculate take profit based on variant"""
        risk = abs(entry_price - stop_loss)
        
        if tp_type == 'liquidity':
            # Target next swing high/low or 1:2
            lookback_data = df.iloc[idx:min(idx+50, len(df))]
            
            if direction == 'bullish':
                if len(lookback_data) > 0:
                    next_high = lookback_data['High'].max()
                    liquidity_target = next_high
                    max_target = entry_price + (risk * 2)
                    return min(liquidity_target, max_target)
                return entry_price + (risk * 2)
            else:
                if len(lookback_data) > 0:
                    next_low = lookback_data['Low'].min()
                    liquidity_target = next_low
                    max_target = entry_price - (risk * 2)
                    return max(liquidity_target, max_target)
                return entry_price - (risk * 2)
        
        elif tp_type == 'fixed_rr' and rr_ratio:
            # Fixed R:R ratio
            if direction == 'bullish':
                return entry_price + (risk * rr_ratio)
            else:
                return entry_price - (risk * rr_ratio)
        
        elif tp_type == 'std_dev' and std_multiplier:
            # Standard deviation of manipulation range
            manipulation_range = df.iloc[max(0, idx-20):idx]['Close']
            std_dev = manipulation_range.std()
            
            if direction == 'bullish':
                return entry_price + (std_dev * std_multiplier)
            else:
                return entry_price - (std_dev * std_multiplier)
        
        elif tp_type == 'fixed' and tp_points:
            # Fixed points
            if direction == 'bullish':
                return entry_price + tp_points
            else:
                return entry_price - tp_points
        
        return 0.0
    
    def check_entry_filled(self, entry_type: str, entry_price: float, direction: str,
                          df: pd.DataFrame, entry_idx: int, scan_limit: int = 20) -> Tuple[bool, int]:
        """
        Check if entry order gets filled
        For CE_50, entry might not fill if price doesn't retrace enough
        
        Returns:
            (filled, fill_index)
        """
        if entry_type == 'proximal':
            # Proximal entry usually fills quickly
            return True, entry_idx
        
        elif entry_type == 'ce_50':
            # Check if price retraces to CE within next bars
            for i in range(entry_idx, min(entry_idx + scan_limit, len(df))):
                current_bar = df.iloc[i]
                
                if direction == 'bullish':
                    if current_bar['Low'] <= entry_price:
                        return True, i
                else:
                    if current_bar['High'] >= entry_price:
                        return True, i
            
            # Entry not filled
            return False, -1
        
        return True, entry_idx
    
    def simulate_trade(self, df: pd.DataFrame, entry_idx: int, variant_config: Dict,
                      direction: str, fvg_high: float, fvg_low: float, ce_price: float,
                      mss_high: float, mss_low: float) -> Optional[Dict]:
        """
        Simulate trade execution for specific variant
        """
        # Calculate entry, SL, TP
        entry_price = self.calculate_entry_price(
            variant_config['entry_type'], direction, fvg_high, fvg_low, ce_price
        )
        
        stop_loss = self.calculate_stop_loss(
            variant_config['sl_type'], direction, df, entry_idx,
            fvg_high, fvg_low, mss_high, mss_low,
            variant_config.get('sl_points')
        )
        
        take_profit = self.calculate_take_profit(
            variant_config['tp_type'], direction, entry_price, stop_loss,
            df, entry_idx, mss_high, mss_low,
            variant_config.get('rr_ratio'),
            variant_config.get('std_multiplier'),
            variant_config.get('tp_points')
        )
        
        # Check if entry fills
        entry_filled, fill_idx = self.check_entry_filled(
            variant_config['entry_type'], entry_price, direction, df, entry_idx
        )
        
        if not entry_filled:
            return None  # Trade not taken
        
        entry_time = df.index[fill_idx]
        
        # Calculate position size
        risk_points = abs(entry_price - stop_loss)
        risk_amount = self.capital * self.risk_per_trade
        position_size = max(1, int(risk_amount / (risk_points * self.point_value)))
        
        # Simulate trade management
        for i in range(fill_idx + 1, min(fill_idx + 200, len(df))):
            current_bar = df.iloc[i]
            
            # Check stop loss
            if direction == 'bullish':
                if current_bar['Low'] <= stop_loss:
                    pnl = (stop_loss - entry_price) * position_size * self.point_value
                    return {
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_price': stop_loss,
                        'exit_time': df.index[i],
                        'direction': direction,
                        'pnl': pnl,
                        'outcome': 'loss',
                        'r_multiple': -1.0
                    }
            else:
                if current_bar['High'] >= stop_loss:
                    pnl = (entry_price - stop_loss) * position_size * self.point_value
                    return {
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_price': stop_loss,
                        'exit_time': df.index[i],
                        'direction': direction,
                        'pnl': pnl,
                        'outcome': 'loss',
                        'r_multiple': -1.0
                    }
            
            # Check take profit
            if direction == 'bullish':
                if current_bar['High'] >= take_profit:
                    pnl = (take_profit - entry_price) * position_size * self.point_value
                    r_multiple = (take_profit - entry_price) / risk_points
                    return {
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_price': take_profit,
                        'exit_time': df.index[i],
                        'direction': direction,
                        'pnl': pnl,
                        'outcome': 'win',
                        'r_multiple': r_multiple
                    }
            else:
                if current_bar['Low'] <= take_profit:
                    pnl = (entry_price - take_profit) * position_size * self.point_value
                    r_multiple = (entry_price - take_profit) / risk_points
                    return {
                        'entry_time': entry_time,
                        'entry_price': entry_price,
                        'exit_price': take_profit,
                        'exit_time': df.index[i],
                        'direction': direction,
                        'pnl': pnl,
                        'outcome': 'win',
                        'r_multiple': r_multiple
                    }
        
        # Still open at end - close at market
        last_bar = df.iloc[-1]
        exit_price = last_bar['Close']
        
        if direction == 'bullish':
            pnl = (exit_price - entry_price) * position_size * self.point_value
        else:
            pnl = (entry_price - exit_price) * position_size * self.point_value
        
        r_multiple = pnl / (risk_points * position_size * self.point_value)
        
        return {
            'entry_time': entry_time,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'exit_time': df.index[-1],
            'direction': direction,
            'pnl': pnl,
            'outcome': 'win' if pnl > 0 else 'loss',
            'r_multiple': r_multiple
        }
    
    def run_backtest_variant(self, variant_name: str, years: List[int]) -> pd.DataFrame:
        """
        Run backtest for specific variant across multiple years
        """
        print(f"\n{'='*80}")
        print(f"BACKTESTING: {variant_name}")
        print(f"Description: {self.variants[variant_name]['description']}")
        print(f"{'='*80}")
        
        variant_config = self.variants[variant_name]
        all_trades = []
        
        for year in years:
            print(f"\nProcessing {year}...")
            
            # Load 15m data
            df_15m = self.load_data('15m', year)
            print(f"  Loaded {len(df_15m)} bars")
            
            # Scan for setups
            setups_found = 0
            trades_taken = 0
            
            for i in range(50, len(df_15m) - 50):
                current_time = df_15m.index[i].time()
                
                # Check time window
                if not (self.entry_start <= current_time < self.entry_end):
                    continue
                
                # 1. Check for liquidity sweep
                has_sweep, sweep_direction, swept_level = self.detect_liquidity_sweep(df_15m, i)
                
                if not has_sweep:
                    continue
                
                # 2. Check for MSS with displacement
                has_mss, mss_high, mss_low = self.detect_mss_with_displacement(df_15m, i, sweep_direction)
                
                if not has_mss:
                    continue
                
                # 3. Check for FVG in opposite direction
                has_fvg, fvg_high, fvg_low, ce_price = self.detect_fvg(df_15m, i, sweep_direction)
                
                if not has_fvg:
                    continue
                
                setups_found += 1
                
                # 4. Simulate trade for this variant
                trade = self.simulate_trade(
                    df_15m, i, variant_config, sweep_direction,
                    fvg_high, fvg_low, ce_price, mss_high, mss_low
                )
                
                if trade:
                    trade['variant'] = variant_name
                    trade['year'] = year
                    all_trades.append(trade)
                    trades_taken += 1
            
            print(f"  Setups found: {setups_found}")
            print(f"  Trades taken: {trades_taken} (Unfilled: {setups_found - trades_taken})")
        
        if len(all_trades) > 0:
            trades_df = pd.DataFrame(all_trades)
            print(f"\nTotal trades for {variant_name}: {len(trades_df)}")
            return trades_df
        else:
            print(f"\nNo trades for {variant_name}")
            return pd.DataFrame()
    
    def run_all_variants(self, years: List[int] = [2024]) -> pd.DataFrame:
        """
        Run backtest for all 4 variants and compare
        """
        print("="*80)
        print("ICT FVG REVERSAL - 4 VARIANTS COMPARISON")
        print("="*80)
        print(f"Years: {years}")
        print(f"Entry window: {self.entry_start} - {self.entry_end}")
        print(f"Capital: ${self.capital:,.2f}")
        print(f"Risk per trade: {self.risk_per_trade*100}%")
        
        all_results = []
        
        # Run each variant
        for variant_name in self.variants.keys():
            trades = self.run_backtest_variant(variant_name, years)
            
            if len(trades) > 0:
                # Calculate metrics
                total_trades = len(trades)
                winners = trades[trades['outcome'] == 'win']
                losers = trades[trades['outcome'] == 'loss']
                
                win_rate = (len(winners) / total_trades) * 100 if total_trades > 0 else 0
                avg_rr = trades['r_multiple'].mean()
                
                gross_profit = winners['pnl'].sum() if len(winners) > 0 else 0
                gross_loss = abs(losers['pnl'].sum()) if len(losers) > 0 else 0
                profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
                
                net_profit = trades['pnl'].sum()
                
                # Calculate drawdown
                cumulative_pnl = trades['pnl'].cumsum()
                running_max = cumulative_pnl.cummax()
                drawdown = running_max - cumulative_pnl
                max_drawdown = drawdown.max()
                
                all_results.append({
                    'Variant': variant_name,
                    'Total Trades': total_trades,
                    'Win Rate (%)': round(win_rate, 2),
                    'Avg R:R': round(avg_rr, 2),
                    'Profit Factor': round(profit_factor, 2),
                    'Max Drawdown ($)': round(max_drawdown, 2),
                    'Net Profit ($)': round(net_profit, 2)
                })
                
                # Store detailed trades
                self.results[variant_name] = trades
            else:
                all_results.append({
                    'Variant': variant_name,
                    'Total Trades': 0,
                    'Win Rate (%)': 0,
                    'Avg R:R': 0,
                    'Profit Factor': 0,
                    'Max Drawdown ($)': 0,
                    'Net Profit ($)': 0
                })
        
        # Create comparison DataFrame
        comparison_df = pd.DataFrame(all_results)
        
        print("\n" + "="*80)
        print("COMPARISON TABLE - ALL VARIANTS")
        print("="*80)
        print(comparison_df.to_string(index=False))
        print("="*80)
        
        return comparison_df
    
    def save_results(self, comparison_df: pd.DataFrame):
        """Save results to CSV files"""
        comparison_df.to_csv('fvg_variants_comparison.csv', index=False)
        print("\nComparison saved to: fvg_variants_comparison.csv")
        
        # Save detailed trades for each variant
        for variant_name, trades_df in self.results.items():
            if len(trades_df) > 0:
                filename = f'fvg_variant_{variant_name.lower()}_trades.csv'
                trades_df.to_csv(filename, index=False)
                print(f"Detailed trades for {variant_name} saved to: {filename}")


def main():
    """Main execution function"""
    
    # Initialize backtest
    backtest = FVGReversalVariants(capital=100000, risk_per_trade=0.01)
    
    # Run comparison for 2024
    comparison = backtest.run_all_variants(years=[2024])
    
    # Save results
    backtest.save_results(comparison)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    
    # Print winner
    if len(comparison) > 0:
        best_variant = comparison.loc[comparison['Net Profit ($)'].idxmax()]
        print(f"\nBest performing variant: {best_variant['Variant']}")
        print(f"  Net Profit: ${best_variant['Net Profit ($)']:,.2f}")
        print(f"  Win Rate: {best_variant['Win Rate (%)']}%")
        print(f"  Profit Factor: {best_variant['Profit Factor']}")
    
    return backtest, comparison


if __name__ == "__main__":
    backtest, comparison = main()
