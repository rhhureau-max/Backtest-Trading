#!/usr/bin/env python3
"""
Inverse FVG (Fair Value Gap) Trading Strategy Backtest
Backtests an inverse FVG strategy on NQ futures data for 5m and 15m timeframes.
"""

import pandas as pd
from datetime import datetime, time
from typing import List, Dict, Tuple, Optional


class FVG:
    """Represents a Fair Value Gap zone"""
    def __init__(self, fvg_type: str, high_zone: float, low_zone: float, creation_time: datetime,
                 structure_high: float = None, structure_low: float = None):
        self.type = fvg_type  # 'bullish' or 'bearish'
        self.high_zone = high_zone
        self.low_zone = low_zone
        self.creation_time = creation_time
        self.used = False
        # Store structure levels for structure-based SL
        self.structure_high = structure_high if structure_high is not None else high_zone
        self.structure_low = structure_low if structure_low is not None else low_zone


class Position:
    """Represents an open trading position"""
    def __init__(self, position_type: str, entry_price: float, stop_loss: float, 
                 take_profit: float, entry_time: datetime, entry_bar: int):
        self.type = position_type  # 'LONG' or 'SHORT'
        self.entry_price = entry_price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.entry_time = entry_time
        self.entry_bar = entry_bar
        self.exit_price: Optional[float] = None
        self.exit_time: Optional[datetime] = None
        self.exit_reason: Optional[str] = None
        self.pnl: Optional[float] = None


class FVGBacktest:
    """Backtester for Inverse FVG Strategy"""
    
    def __init__(self, data: pd.DataFrame, timeframe: str, sl_type: str = 'candle', tp_ratio: float = 2.0):
        self.data = data.copy()
        self.timeframe = timeframe
        self.sl_type = sl_type  # 'candle', 'structure', or 'fixed'
        self.tp_ratio = tp_ratio  # TP ratio (1.5, 2.0, or 3.0)
        self.fvgs: List[FVG] = []
        self.position: Optional[Position] = None
        self.closed_trades: List[Position] = []
        
        # Trading session times
        self.session_start = time(1, 0)  # 01:00
        self.session_end = time(5, 0)    # 05:00
        
        # Fixed SL for NQ (in points)
        self.fixed_sl_points = 20.0
        
    def parse_datetime(self, date_str: str, time_str: str) -> datetime:
        """Parse date and time strings into datetime object"""
        return datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")
    
    def is_in_session(self, dt: datetime) -> bool:
        """Check if datetime is within trading session (01:00-05:00)"""
        current_time = dt.time()
        return self.session_start <= current_time < self.session_end
    
    def is_session_start(self, dt: datetime) -> bool:
        """Check if this is the start of a new session (01:00)"""
        return dt.time() == self.session_start
    
    def is_session_end(self, dt: datetime) -> bool:
        """Check if this is the end of session (05:00)"""
        return dt.time() == self.session_end
    
    def detect_fvg(self, i: int) -> Optional[FVG]:
        """
        Detect FVG at current bar i (requires bars i-2, i-1, i)
        Returns FVG object if detected, None otherwise
        """
        if i < 2:
            return None
        
        high_t2 = self.data.loc[i-2, 'High']
        low_t2 = self.data.loc[i-2, 'Low']
        high_t = self.data.loc[i, 'High']
        low_t = self.data.loc[i, 'Low']
        dt = self.data.loc[i, 'DateTime']
        
        # Bearish FVG: Low[t-2] > High[t]
        # For structure SL: structure_high = low_t2, structure_low = high_t
        if low_t2 > high_t:
            return FVG('bearish', low_t2, high_t, dt, structure_high=low_t2, structure_low=high_t)
        
        # Bullish FVG: High[t-2] < Low[t]
        # For structure SL: structure_high = low_t, structure_low = high_t2
        if high_t2 < low_t:
            return FVG('bullish', low_t, high_t2, dt, structure_high=low_t, structure_low=high_t2)
        
        return None
    
    def check_entry_signal(self, i: int) -> Optional[Tuple[str, float, float, float, FVG]]:
        """
        Check for entry signals based on FVGs
        Returns (signal_type, entry_price, stop_loss, take_profit, fvg) or None
        """
        if self.position is not None:
            return None  # Already in position
        
        close = self.data.loc[i, 'Close']
        high = self.data.loc[i, 'High']
        low = self.data.loc[i, 'Low']
        
        if i == 0:
            return None
        
        prev_close = self.data.loc[i-1, 'Close']
        
        # Check each FVG for inverse entry signals
        for fvg in self.fvgs:
            if fvg.used:
                continue
            
            if fvg.type == 'bearish':
                # INVERSE: LONG when close crosses ABOVE High_Zone of Bearish FVG
                if prev_close <= fvg.high_zone and close > fvg.high_zone:
                    entry_price = close
                    
                    # Calculate stop loss based on sl_type
                    if self.sl_type == 'candle':
                        # SL at lowest low of signal candle
                        stop_loss = low
                    elif self.sl_type == 'structure':
                        # SL below the bottom of FVG zone (High[t] from bearish FVG)
                        stop_loss = fvg.structure_low
                    elif self.sl_type == 'fixed':
                        # Fixed 20 points SL
                        stop_loss = entry_price - self.fixed_sl_points
                    else:
                        stop_loss = low  # Default to candle
                    
                    risk = entry_price - stop_loss
                    take_profit = entry_price + (self.tp_ratio * risk)
                    fvg.used = True
                    return ('LONG', entry_price, stop_loss, take_profit, fvg)
            
            elif fvg.type == 'bullish':
                # INVERSE: SHORT when close crosses BELOW Low_Zone of Bullish FVG
                if prev_close >= fvg.low_zone and close < fvg.low_zone:
                    entry_price = close
                    
                    # Calculate stop loss based on sl_type
                    if self.sl_type == 'candle':
                        # SL at highest high of signal candle
                        stop_loss = high
                    elif self.sl_type == 'structure':
                        # SL above the top of FVG zone (Low[t] from bullish FVG)
                        stop_loss = fvg.structure_high
                    elif self.sl_type == 'fixed':
                        # Fixed 20 points SL
                        stop_loss = entry_price + self.fixed_sl_points
                    else:
                        stop_loss = high  # Default to candle
                    
                    risk = stop_loss - entry_price
                    take_profit = entry_price - (self.tp_ratio * risk)
                    fvg.used = True
                    return ('SHORT', entry_price, stop_loss, take_profit, fvg)
        
        return None
    
    def check_exit(self, i: int) -> Optional[Tuple[float, str]]:
        """
        Check if position should be exited
        Returns (exit_price, exit_reason) or None
        """
        if self.position is None:
            return None
        
        high = self.data.loc[i, 'High']
        low = self.data.loc[i, 'Low']
        close = self.data.loc[i, 'Close']
        dt = self.data.loc[i, 'DateTime']
        
        # Check for session end
        if self.is_session_end(dt):
            return (close, 'SESSION_END')
        
        if self.position.type == 'LONG':
            # Check stop loss
            if low <= self.position.stop_loss:
                return (self.position.stop_loss, 'STOP_LOSS')
            # Check take profit
            if high >= self.position.take_profit:
                return (self.position.take_profit, 'TAKE_PROFIT')
        
        elif self.position.type == 'SHORT':
            # Check stop loss
            if high >= self.position.stop_loss:
                return (self.position.stop_loss, 'STOP_LOSS')
            # Check take profit
            if low <= self.position.take_profit:
                return (self.position.take_profit, 'TAKE_PROFIT')
        
        return None
    
    def close_position(self, exit_price: float, exit_reason: str, exit_time: datetime):
        """Close current position and calculate P&L"""
        if self.position is None:
            return
        
        self.position.exit_price = exit_price
        self.position.exit_reason = exit_reason
        self.position.exit_time = exit_time
        
        # Calculate P&L in points
        if self.position.type == 'LONG':
            self.position.pnl = exit_price - self.position.entry_price
        else:  # SHORT
            self.position.pnl = self.position.entry_price - exit_price
        
        self.closed_trades.append(self.position)
        self.position = None
    
    def run(self) -> Dict:
        """Run the backtest and return results"""
        # Parse datetime
        self.data['DateTime'] = self.data.apply(
            lambda row: self.parse_datetime(row['Date'], row['Time']), axis=1
        )
        
        current_day = None
        
        # Process bars sequentially
        for i in range(len(self.data)):
            dt = self.data.loc[i, 'DateTime']
            
            # Check for new day (session start at 01:00)
            if self.is_session_start(dt):
                day = dt.date()
                if current_day != day:
                    current_day = day
                    # Reset FVGs at start of new session
                    self.fvgs = []
            
            # Only process bars during trading session (01:00-05:00)
            if not self.is_in_session(dt):
                # If we're outside session and have open position, skip
                # (position should have been closed at session end)
                continue
            
            # Check for exit first (before new entries)
            if self.position is not None:
                exit_result = self.check_exit(i)
                if exit_result:
                    exit_price, exit_reason = exit_result
                    self.close_position(exit_price, exit_reason, dt)
            
            # Detect new FVG (only during session)
            new_fvg = self.detect_fvg(i)
            if new_fvg:
                self.fvgs.append(new_fvg)
            
            # Check for entry signal (only if no position)
            if self.position is None:
                entry_signal = self.check_entry_signal(i)
                if entry_signal:
                    signal_type, entry_price, stop_loss, take_profit, fvg = entry_signal
                    self.position = Position(
                        signal_type, entry_price, stop_loss, take_profit, dt, i
                    )
        
        # Close any remaining open position at end of data
        if self.position is not None:
            last_close = self.data.loc[len(self.data)-1, 'Close']
            last_time = self.data.loc[len(self.data)-1, 'DateTime']
            self.close_position(last_close, 'END_OF_DATA', last_time)
        
        # Calculate statistics
        results = self.calculate_statistics()
        return results
    
    def calculate_statistics(self) -> Dict:
        """Calculate backtest statistics including max drawdown"""
        total_trades = len(self.closed_trades)
        
        if total_trades == 0:
            return {
                'timeframe': self.timeframe,
                'sl_type': self.sl_type,
                'tp_ratio': self.tp_ratio,
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'winrate': 0.0,
                'total_pnl': 0.0,
                'gross_profit': 0.0,
                'gross_loss': 0.0,
                'profit_factor': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'max_drawdown': 0.0,
                'max_drawdown_pct': 0.0
            }
        
        winning_trades = [t for t in self.closed_trades if t.pnl > 0]
        losing_trades = [t for t in self.closed_trades if t.pnl <= 0]
        
        num_wins = len(winning_trades)
        num_losses = len(losing_trades)
        
        winrate = (num_wins / total_trades * 100) if total_trades > 0 else 0.0
        
        gross_profit = sum(t.pnl for t in winning_trades)
        gross_loss = abs(sum(t.pnl for t in losing_trades))
        
        total_pnl = sum(t.pnl for t in self.closed_trades)
        
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')
        
        avg_win = (gross_profit / num_wins) if num_wins > 0 else 0.0
        avg_loss = (gross_loss / num_losses) if num_losses > 0 else 0.0
        
        # Calculate max drawdown
        cumulative_pnl = 0.0
        peak = 0.0
        max_drawdown = 0.0
        
        for trade in self.closed_trades:
            cumulative_pnl += trade.pnl
            if cumulative_pnl > peak:
                peak = cumulative_pnl
            drawdown = peak - cumulative_pnl
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # Calculate max drawdown percentage (relative to peak)
        max_drawdown_pct = (max_drawdown / peak * 100) if peak > 0 else 0.0
        
        return {
            'timeframe': self.timeframe,
            'sl_type': self.sl_type,
            'tp_ratio': self.tp_ratio,
            'total_trades': total_trades,
            'winning_trades': num_wins,
            'losing_trades': num_losses,
            'winrate': winrate,
            'total_pnl': total_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'max_drawdown': max_drawdown,
            'max_drawdown_pct': max_drawdown_pct
        }


def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV data with proper column names"""
    df = pd.read_csv(filepath, sep=';')
    df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    return df


def print_results(results: Dict):
    """Print detailed results for a timeframe"""
    print(f"\nResults for {results['timeframe']} timeframe:")
    print(f"  Total Trades: {results['total_trades']}")
    print(f"  Winning Trades: {results['winning_trades']}")
    print(f"  Losing Trades: {results['losing_trades']}")
    print(f"  Win Rate: {results['winrate']:.2f}%")
    print(f"  Total P&L: {results['total_pnl']:.2f} points")
    print(f"  Gross Profit: {results['gross_profit']:.2f} points")
    print(f"  Gross Loss: {results['gross_loss']:.2f} points")
    if results['profit_factor'] == float('inf'):
        print(f"  Profit Factor: ∞ (no losses)")
    else:
        print(f"  Profit Factor: {results['profit_factor']:.2f}")
    print(f"  Average Win: {results['avg_win']:.2f} points")
    print(f"  Average Loss: {results['avg_loss']:.2f} points")


def print_comparison_table(results_5m: Dict, results_15m: Dict):
    """Print comparison table for both timeframes"""
    print("\n" + "="*80)
    print("INVERSE FVG STRATEGY BACKTEST RESULTS - COMPARISON TABLE")
    print("="*80)
    print(f"{'Metric':<25} {'5-Minute':<25} {'15-Minute':<25}")
    print("-"*80)
    print(f"{'Win Rate':<25} {results_5m['winrate']:>20.2f}% {results_15m['winrate']:>20.2f}%")
    print(f"{'Total Trades':<25} {results_5m['total_trades']:>24} {results_15m['total_trades']:>24}")
    print(f"{'Cumulative P&L (pts)':<25} {results_5m['total_pnl']:>20.2f} {results_15m['total_pnl']:>20.2f}")
    
    pf_5m = f"{results_5m['profit_factor']:.2f}" if results_5m['profit_factor'] != float('inf') else "∞"
    pf_15m = f"{results_15m['profit_factor']:.2f}" if results_15m['profit_factor'] != float('inf') else "∞"
    print(f"{'Profit Factor':<25} {pf_5m:>24} {pf_15m:>24}")
    print("-"*80)
    print(f"{'Winning Trades':<25} {results_5m['winning_trades']:>24} {results_15m['winning_trades']:>24}")
    print(f"{'Losing Trades':<25} {results_5m['losing_trades']:>24} {results_15m['losing_trades']:>24}")
    print(f"{'Gross Profit (pts)':<25} {results_5m['gross_profit']:>20.2f} {results_15m['gross_profit']:>20.2f}")
    print(f"{'Gross Loss (pts)':<25} {results_5m['gross_loss']:>20.2f} {results_15m['gross_loss']:>20.2f}")
    print(f"{'Average Win (pts)':<25} {results_5m['avg_win']:>20.2f} {results_15m['avg_win']:>20.2f}")
    print(f"{'Average Loss (pts)':<25} {results_5m['avg_loss']:>20.2f} {results_15m['avg_loss']:>20.2f}")
    print("="*80)


def run_parameter_optimization():
    """Run backtest with all SL and TP combinations"""
    print("\n" + "="*100)
    print("INVERSE FVG STRATEGY - PARAMETER OPTIMIZATION")
    print("="*100)
    print("\nStrategy Rules:")
    print("  - Trading Session: 01:00 - 05:00 only")
    print("  - FVG Detection: During session hours only")
    print("  - LONG Entry: Close crosses ABOVE High_Zone of Bearish FVG (INVERSE)")
    print("  - SHORT Entry: Close crosses BELOW Low_Zone of Bullish FVG (INVERSE)")
    print("\nTesting 3 Stop Loss Types:")
    print("  1. Candle: SL at signal candle's low (LONG) or high (SHORT)")
    print("  2. Structure: SL at FVG zone boundary")
    print("  3. Fixed: 20 points fixed SL")
    print("\nTesting 3 Take Profit Ratios:")
    print("  1. 1:1.5 (Scalping)")
    print("  2. 1:2.0 (Classic)")
    print("  3. 1:3.0 (Trend Following)")
    
    # File paths
    file_5m = "/home/runner/work/Backtest-Trading/Backtest-Trading/2025 5m.csv"
    file_15m = "/home/runner/work/Backtest-Trading/Backtest-Trading/2025 15m.csv"
    
    # Load data
    print("\nLoading data files...")
    data_5m = load_data(file_5m)
    data_15m = load_data(file_15m)
    print(f"  5m data: {len(data_5m)} bars")
    print(f"  15m data: {len(data_15m)} bars")
    
    # Define parameters to test
    sl_types = ['candle', 'structure', 'fixed']
    sl_names = {'candle': 'Candle', 'structure': 'Structure', 'fixed': 'Fixe'}
    tp_ratios = [1.5, 2.0, 3.0]
    timeframes = [('5m', data_5m), ('15m', data_15m)]
    
    all_results = []
    total_tests = len(sl_types) * len(tp_ratios) * len(timeframes)
    current_test = 0
    
    print(f"\n{'='*100}")
    print(f"Running {total_tests} backtest combinations...")
    print(f"{'='*100}\n")
    
    # Run all combinations
    for tf_name, data in timeframes:
        for sl_type in sl_types:
            for tp_ratio in tp_ratios:
                current_test += 1
                print(f"[{current_test}/{total_tests}] Testing {tf_name} - SL: {sl_names[sl_type]} - TP Ratio: 1:{tp_ratio}")
                
                backtest = FVGBacktest(data, tf_name, sl_type=sl_type, tp_ratio=tp_ratio)
                results = backtest.run()
                
                # Add readable SL name for display
                results['sl_name'] = sl_names[sl_type]
                all_results.append(results)
    
    # Create DataFrame from results
    df_results = pd.DataFrame(all_results)
    
    # Sort by Total P&L descending (using the numeric value)
    df_results = df_results.sort_values('total_pnl', ascending=False).reset_index(drop=True)
    
    # Format columns for display
    df_display = pd.DataFrame({
        'Timeframe': df_results['timeframe'],
        'Type de SL': df_results['sl_name'],
        'Ratio TP': df_results['tp_ratio'].apply(lambda x: f"1:{x}"),
        'Winrate (%)': df_results['winrate'].apply(lambda x: f"{x:.2f}"),
        'Nombre de Trades': df_results['total_trades'],
        'Total P&L (Points)': df_results['total_pnl'].apply(lambda x: f"{x:.2f}"),
        'Max Drawdown (Points)': df_results['max_drawdown'].apply(lambda x: f"{x:.2f}"),
        'Max Drawdown (%)': df_results['max_drawdown_pct'].apply(lambda x: f"{x:.2f}"),
        'Profit Factor': df_results['profit_factor'].apply(lambda x: f"{x:.2f}" if x != float('inf') else "∞")
    })
    
    # Print results table
    print("\n" + "="*100)
    print("RÉSULTATS - TABLEAU RÉCAPITULATIF (Trié par Total P&L décroissant)")
    print("="*100)
    print(df_display.to_string(index=False))
    print("="*100)
    
    # Print best configuration
    best_idx = df_results['total_pnl'].idxmax()
    best = df_results.loc[best_idx]
    print("\n🏆 MEILLEURE CONFIGURATION:")
    print(f"   Timeframe: {best['timeframe']}")
    print(f"   Type de SL: {best['sl_name']}")
    print(f"   Ratio TP: 1:{best['tp_ratio']}")
    print(f"   Total P&L: {best['total_pnl']:.2f} points")
    print(f"   Winrate: {best['winrate']:.2f}%")
    print(f"   Nombre de Trades: {best['total_trades']}")
    print(f"   Max Drawdown: {best['max_drawdown']:.2f} points ({best['max_drawdown_pct']:.2f}%)")
    print(f"   Profit Factor: {best['profit_factor']:.2f}" if best['profit_factor'] != float('inf') else "   Profit Factor: ∞")
    
    print("\nOptimisation terminée avec succès!")
    
    return df_display


def main():
    """Main function to run parameter optimization"""
    run_parameter_optimization()


if __name__ == "__main__":
    main()
