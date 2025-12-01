#!/usr/bin/env python3
"""
SMC Reversal Strategy Backtester
================================
A complete backtesting system for Smart Money Concepts (SMC) based reversal strategy.

Strategy Logic:
- Long: Price retraces into bullish Major FVG, forms bullish Entry FVG, 
        entry on Entry FVG retest
- Short: Inverse logic with bearish FVGs
"""

import os
import zipfile
from io import StringIO
from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numba import njit

# Configuration
SWING_LOOKBACK = 5  # Bars to look back/forward for swing detection
FVG_LOOKBACK = 100  # Max bars to keep Major FVGs active
ENTRY_FVG_LOOKBACK = 10  # Bars to keep Entry FVGs active for retest


@dataclass
class FVG:
    """Fair Value Gap representation"""
    index: int          # Bar index where FVG was created
    top: float          # Top of the FVG zone
    bottom: float       # Bottom of the FVG zone
    is_bullish: bool    # True for bullish, False for bearish
    filled: bool = False


@dataclass 
class Trade:
    """Trade representation"""
    entry_index: int
    entry_price: float
    stop_loss: float
    take_profit: float
    is_long: bool
    exit_index: Optional[int] = None
    exit_price: Optional[float] = None
    pnl: float = 0.0
    is_win: bool = False


def load_data(data_dir: str) -> pd.DataFrame:
    """
    Load all 1-minute data from CSV files (plain and zipped).
    
    Args:
        data_dir: Directory containing the data files
        
    Returns:
        DataFrame with OHLCV data sorted by datetime
    """
    all_data = []
    
    # Find all relevant files
    files = os.listdir(data_dir)
    m1_files = [f for f in files if '1m' in f and (f.endswith('.csv') or f.endswith('.zip'))]
    
    print(f"Found {len(m1_files)} 1-minute data files")
    
    for filename in sorted(m1_files):
        filepath = os.path.join(data_dir, filename)
        print(f"Loading {filename}...")
        
        try:
            if filename.endswith('.zip'):
                # Extract CSV from zip
                with zipfile.ZipFile(filepath, 'r') as zf:
                    csv_name = zf.namelist()[0]
                    with zf.open(csv_name) as f:
                        content = f.read().decode('utf-8')
                        df = pd.read_csv(
                            StringIO(content),
                            sep=';',
                            names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                            skiprows=1
                        )
            else:
                df = pd.read_csv(
                    filepath,
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )
            
            # Parse datetime
            df['Datetime'] = pd.to_datetime(
                df['Date'] + ' ' + df['Time'], 
                format='%d/%m/%Y %H:%M:%S'
            )
            df = df.drop(columns=['Date', 'Time'])
            
            # Convert numeric columns
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            all_data.append(df)
            print(f"  Loaded {len(df):,} rows")
            
        except Exception as e:
            print(f"  Error loading {filename}: {e}")
    
    if not all_data:
        raise ValueError("No data files loaded!")
    
    # Combine and sort
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values('Datetime').reset_index(drop=True)
    combined = combined.dropna()
    
    print(f"\nTotal: {len(combined):,} rows from {combined['Datetime'].min()} to {combined['Datetime'].max()}")
    
    return combined


@njit
def detect_swings_numba(highs: np.ndarray, lows: np.ndarray, lookback: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Detect swing highs and lows using numba for performance.
    
    Returns:
        swing_highs: Array where values > 0 indicate swing high price
        swing_lows: Array where values > 0 indicate swing low price
    """
    n = len(highs)
    swing_highs = np.zeros(n)
    swing_lows = np.zeros(n)
    
    for i in range(lookback, n - lookback):
        # Check for swing high
        is_swing_high = True
        for j in range(i - lookback, i + lookback + 1):
            if j != i and highs[j] > highs[i]:
                is_swing_high = False
                break
        if is_swing_high:
            swing_highs[i] = highs[i]
        
        # Check for swing low
        is_swing_low = True
        for j in range(i - lookback, i + lookback + 1):
            if j != i and lows[j] < lows[i]:
                is_swing_low = False
                break
        if is_swing_low:
            swing_lows[i] = lows[i]
    
    return swing_highs, swing_lows


@njit
def detect_fvgs_numba(highs: np.ndarray, lows: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Detect Fair Value Gaps using numba for performance.
    
    Bullish FVG: Low[i-1] > High[i+1] (gap up)
    Bearish FVG: High[i-1] < Low[i+1] (gap down)
    
    Returns:
        bull_fvg_top, bull_fvg_bottom, bear_fvg_top, bear_fvg_bottom
    """
    n = len(highs)
    bull_fvg_top = np.zeros(n)
    bull_fvg_bottom = np.zeros(n)
    bear_fvg_top = np.zeros(n)
    bear_fvg_bottom = np.zeros(n)
    
    for i in range(1, n - 1):
        # Bullish FVG: Gap between candle i-1 low and candle i+1 high
        if lows[i - 1] > highs[i + 1]:
            bull_fvg_top[i] = lows[i - 1]
            bull_fvg_bottom[i] = highs[i + 1]
        
        # Bearish FVG: Gap between candle i-1 high and candle i+1 low
        if highs[i - 1] < lows[i + 1]:
            bear_fvg_top[i] = lows[i + 1]
            bear_fvg_bottom[i] = highs[i - 1]
    
    return bull_fvg_top, bull_fvg_bottom, bear_fvg_top, bear_fvg_bottom


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add swing points and FVG detection to the dataframe."""
    
    print("Detecting swing points...")
    highs = df['High'].values
    lows = df['Low'].values
    
    swing_highs, swing_lows = detect_swings_numba(highs, lows, SWING_LOOKBACK)
    df['SwingHigh'] = swing_highs
    df['SwingLow'] = swing_lows
    
    print("Detecting Fair Value Gaps...")
    bull_top, bull_bottom, bear_top, bear_bottom = detect_fvgs_numba(highs, lows)
    df['BullFVG_Top'] = bull_top
    df['BullFVG_Bottom'] = bull_bottom
    df['BearFVG_Top'] = bear_top
    df['BearFVG_Bottom'] = bear_bottom
    
    return df


class SMCBacktester:
    """
    Smart Money Concepts Reversal Strategy Backtester
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.trades: List[Trade] = []
        self.equity_curve: List[float] = [100000.0]  # Start with 100k
        self.initial_capital = 100000.0
        
        # Active FVG zones
        self.major_bull_fvgs: List[FVG] = []
        self.major_bear_fvgs: List[FVG] = []
        self.entry_bull_fvgs: List[FVG] = []
        self.entry_bear_fvgs: List[FVG] = []
        
        # Track last significant swing points
        self.last_swing_high = 0.0
        self.last_swing_high_idx = 0
        self.last_swing_low = float('inf')
        self.last_swing_low_idx = 0
        
    def _cleanup_old_fvgs(self, current_idx: int, fvg_list: List[FVG], lookback: int):
        """Remove old or filled FVGs."""
        fvg_list[:] = [
            fvg for fvg in fvg_list 
            if not fvg.filled and (current_idx - fvg.index) < lookback
        ]
    
    def _find_deepest_fvg(self, fvgs: List[FVG], is_bullish: bool) -> Optional[FVG]:
        """Find the furthest/deepest FVG (best discount)."""
        if not fvgs:
            return None
        if is_bullish:
            # For bullish, deepest = lowest bottom
            return min(fvgs, key=lambda f: f.bottom)
        else:
            # For bearish, deepest = highest top
            return max(fvgs, key=lambda f: f.top)
    
    def _get_local_swing_low(self, start_idx: int, end_idx: int) -> Tuple[float, int]:
        """Find the lowest swing low in a range."""
        subset = self.df.iloc[max(0, start_idx):end_idx + 1]
        swing_lows = subset[subset['SwingLow'] > 0]['SwingLow']
        if len(swing_lows) > 0:
            min_idx = swing_lows.idxmin()
            return swing_lows[min_idx], min_idx
        # Fallback to absolute low
        min_idx = subset['Low'].idxmin()
        return subset.loc[min_idx, 'Low'], min_idx
    
    def _get_local_swing_high(self, start_idx: int, end_idx: int) -> Tuple[float, int]:
        """Find the highest swing high in a range."""
        subset = self.df.iloc[max(0, start_idx):end_idx + 1]
        swing_highs = subset[subset['SwingHigh'] > 0]['SwingHigh']
        if len(swing_highs) > 0:
            max_idx = swing_highs.idxmax()
            return swing_highs[max_idx], max_idx
        # Fallback to absolute high
        max_idx = subset['High'].idxmax()
        return subset.loc[max_idx, 'High'], max_idx
    
    def run_backtest(self):
        """Execute the backtest."""
        print("\nRunning backtest...")
        
        n = len(self.df)
        position_open = False
        current_trade: Optional[Trade] = None
        
        # Risk per trade (2% of equity)
        risk_pct = 0.02
        
        for i in range(FVG_LOOKBACK, n - 1):
            if i % 100000 == 0:
                print(f"  Processing bar {i:,}/{n:,} ({100*i/n:.1f}%)")
            
            row = self.df.iloc[i]
            close = row['Close']
            high = row['High']
            low = row['Low']
            
            # Update swing points tracking
            if row['SwingHigh'] > 0:
                self.last_swing_high = row['SwingHigh']
                self.last_swing_high_idx = i
            if row['SwingLow'] > 0:
                self.last_swing_low = row['SwingLow']
                self.last_swing_low_idx = i
            
            # Collect new Major FVGs
            if row['BullFVG_Top'] > 0:
                self.major_bull_fvgs.append(FVG(
                    index=i, 
                    top=row['BullFVG_Top'], 
                    bottom=row['BullFVG_Bottom'],
                    is_bullish=True
                ))
            if row['BearFVG_Top'] > 0:
                self.major_bear_fvgs.append(FVG(
                    index=i, 
                    top=row['BearFVG_Top'], 
                    bottom=row['BearFVG_Bottom'],
                    is_bullish=False
                ))
            
            # Cleanup old FVGs
            self._cleanup_old_fvgs(i, self.major_bull_fvgs, FVG_LOOKBACK)
            self._cleanup_old_fvgs(i, self.major_bear_fvgs, FVG_LOOKBACK)
            self._cleanup_old_fvgs(i, self.entry_bull_fvgs, ENTRY_FVG_LOOKBACK)
            self._cleanup_old_fvgs(i, self.entry_bear_fvgs, ENTRY_FVG_LOOKBACK)
            
            # Manage open position
            if position_open and current_trade:
                if current_trade.is_long:
                    # Check stop loss
                    if low <= current_trade.stop_loss:
                        current_trade.exit_price = current_trade.stop_loss
                        current_trade.exit_index = i
                        current_trade.is_win = False
                        position_open = False
                    # Check take profit
                    elif high >= current_trade.take_profit:
                        current_trade.exit_price = current_trade.take_profit
                        current_trade.exit_index = i
                        current_trade.is_win = True
                        position_open = False
                else:
                    # Short position
                    if high >= current_trade.stop_loss:
                        current_trade.exit_price = current_trade.stop_loss
                        current_trade.exit_index = i
                        current_trade.is_win = False
                        position_open = False
                    elif low <= current_trade.take_profit:
                        current_trade.exit_price = current_trade.take_profit
                        current_trade.exit_index = i
                        current_trade.is_win = True
                        position_open = False
                
                if not position_open:
                    # Calculate PnL
                    if current_trade.is_long:
                        current_trade.pnl = current_trade.exit_price - current_trade.entry_price
                    else:
                        current_trade.pnl = current_trade.entry_price - current_trade.exit_price
                    
                    # Update equity (using 1 contract for simplicity)
                    pnl_dollars = current_trade.pnl * 20  # NQ point value = $20
                    new_equity = self.equity_curve[-1] + pnl_dollars
                    self.equity_curve.append(new_equity)
                    self.trades.append(current_trade)
                    current_trade = None
                    continue
            
            # Look for new trade setups (only if no position)
            if not position_open:
                # ===== LONG SETUP =====
                # Step 1: Check if price is in a Major Bullish FVG zone
                deepest_bull_fvg = self._find_deepest_fvg(self.major_bull_fvgs, is_bullish=True)
                
                if deepest_bull_fvg and low <= deepest_bull_fvg.top:
                    # Price is touching/in the Major FVG zone
                    # Step 2: Look for a new Entry FVG (bullish) as sign of strength
                    if row['BullFVG_Top'] > 0:
                        # New bullish Entry FVG created
                        entry_fvg = FVG(
                            index=i,
                            top=row['BullFVG_Top'],
                            bottom=row['BullFVG_Bottom'],
                            is_bullish=True
                        )
                        self.entry_bull_fvgs.append(entry_fvg)
                
                # Step 3: Check for Entry FVG retest
                for entry_fvg in self.entry_bull_fvgs:
                    if entry_fvg.index != i and not entry_fvg.filled:
                        # Check if current candle retests the Entry FVG
                        if low <= entry_fvg.top and low >= entry_fvg.bottom:
                            entry_fvg.filled = True
                            
                            # Get SL (local swing low)
                            local_low, _ = self._get_local_swing_low(
                                deepest_bull_fvg.index if deepest_bull_fvg else i - 20, i
                            )
                            sl = local_low - 2  # Small buffer below swing low
                            
                            # Get TP (last swing high before retracement)
                            tp = self.last_swing_high if self.last_swing_high > close else close + (close - sl)
                            
                            # Validate R:R
                            risk = close - sl
                            reward = tp - close
                            if risk > 0 and reward / risk >= 1.0:
                                current_trade = Trade(
                                    entry_index=i,
                                    entry_price=close,
                                    stop_loss=sl,
                                    take_profit=tp,
                                    is_long=True
                                )
                                position_open = True
                                if deepest_bull_fvg:
                                    deepest_bull_fvg.filled = True
                                break
                
                # ===== SHORT SETUP =====
                if not position_open:
                    deepest_bear_fvg = self._find_deepest_fvg(self.major_bear_fvgs, is_bullish=False)
                    
                    if deepest_bear_fvg and high >= deepest_bear_fvg.bottom:
                        # Price is touching/in the Major Bearish FVG zone
                        if row['BearFVG_Top'] > 0:
                            entry_fvg = FVG(
                                index=i,
                                top=row['BearFVG_Top'],
                                bottom=row['BearFVG_Bottom'],
                                is_bullish=False
                            )
                            self.entry_bear_fvgs.append(entry_fvg)
                    
                    # Check for Entry FVG retest (bearish)
                    for entry_fvg in self.entry_bear_fvgs:
                        if entry_fvg.index != i and not entry_fvg.filled:
                            if high >= entry_fvg.bottom and high <= entry_fvg.top:
                                entry_fvg.filled = True
                                
                                # Get SL (local swing high)
                                local_high, _ = self._get_local_swing_high(
                                    deepest_bear_fvg.index if deepest_bear_fvg else i - 20, i
                                )
                                sl = local_high + 2
                                
                                # Get TP (last swing low)
                                tp = self.last_swing_low if self.last_swing_low < close else close - (sl - close)
                                
                                # Validate R:R
                                risk = sl - close
                                reward = close - tp
                                if risk > 0 and reward / risk >= 1.0:
                                    current_trade = Trade(
                                        entry_index=i,
                                        entry_price=close,
                                        stop_loss=sl,
                                        take_profit=tp,
                                        is_long=False
                                    )
                                    position_open = True
                                    if deepest_bear_fvg:
                                        deepest_bear_fvg.filled = True
                                    break
        
        # Close any remaining position at last bar
        if position_open and current_trade:
            last_close = self.df.iloc[-1]['Close']
            current_trade.exit_price = last_close
            current_trade.exit_index = n - 1
            if current_trade.is_long:
                current_trade.pnl = last_close - current_trade.entry_price
                current_trade.is_win = current_trade.pnl > 0
            else:
                current_trade.pnl = current_trade.entry_price - last_close
                current_trade.is_win = current_trade.pnl > 0
            
            pnl_dollars = current_trade.pnl * 20
            self.equity_curve.append(self.equity_curve[-1] + pnl_dollars)
            self.trades.append(current_trade)
        
        print(f"\nBacktest complete. Total trades: {len(self.trades)}")
    
    def generate_report(self, output_dir: str):
        """Generate performance report and equity curve."""
        
        if not self.trades:
            print("No trades to report!")
            # Generate empty report
            report = """# SMC Reversal Strategy Backtest Report

## Summary
**No trades were executed during the backtest period.**

This could indicate:
- The strategy conditions are too strict
- Parameters may need adjustment
- Market conditions did not match strategy requirements

## Configuration
- Swing Lookback: {}
- Major FVG Lookback: {}
- Entry FVG Lookback: {}
""".format(SWING_LOOKBACK, FVG_LOOKBACK, ENTRY_FVG_LOOKBACK)
            
            with open(os.path.join(output_dir, 'backtest_report.md'), 'w') as f:
                f.write(report)
            
            # Generate flat equity curve
            plt.figure(figsize=(12, 6))
            plt.plot([self.initial_capital], 'b-', linewidth=2)
            plt.title('Equity Curve - No Trades')
            plt.xlabel('Trade Number')
            plt.ylabel('Equity ($)')
            plt.grid(True, alpha=0.3)
            plt.savefig(os.path.join(output_dir, 'equity_curve.png'), dpi=150, bbox_inches='tight')
            plt.close()
            return
        
        # Calculate metrics
        total_trades = len(self.trades)
        winning_trades = sum(1 for t in self.trades if t.is_win)
        losing_trades = total_trades - winning_trades
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        gross_profit = sum(t.pnl for t in self.trades if t.pnl > 0)
        gross_loss = abs(sum(t.pnl for t in self.trades if t.pnl < 0))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Calculate Risk/Reward ratios
        rr_ratios = []
        for t in self.trades:
            if t.is_long:
                risk = t.entry_price - t.stop_loss
                reward = t.take_profit - t.entry_price
            else:
                risk = t.stop_loss - t.entry_price
                reward = t.entry_price - t.take_profit
            if risk > 0:
                rr_ratios.append(reward / risk)
        avg_rr = np.mean(rr_ratios) if rr_ratios else 0
        
        # Net PnL
        net_pnl = sum(t.pnl for t in self.trades)
        net_pnl_dollars = net_pnl * 20  # NQ point value
        
        final_equity = self.equity_curve[-1]
        total_return = ((final_equity - self.initial_capital) / self.initial_capital) * 100
        
        # Long vs Short breakdown
        long_trades = [t for t in self.trades if t.is_long]
        short_trades = [t for t in self.trades if not t.is_long]
        long_wins = sum(1 for t in long_trades if t.is_win)
        short_wins = sum(1 for t in short_trades if t.is_win)
        
        # Max drawdown
        peak = self.initial_capital
        max_dd = 0
        for eq in self.equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak * 100
            if dd > max_dd:
                max_dd = dd
        
        # Generate report
        report = f"""# SMC Reversal Strategy Backtest Report

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Trades** | {total_trades} |
| **Win Rate** | {win_rate:.2f}% |
| **Profit Factor** | {profit_factor:.2f} |
| **Avg Risk/Reward** | {avg_rr:.2f} |
| **Net P&L (points)** | {net_pnl:.2f} |
| **Net P&L ($)** | ${net_pnl_dollars:,.2f} |
| **Total Return** | {total_return:.2f}% |
| **Max Drawdown** | {max_dd:.2f}% |

## Trade Breakdown

### By Direction
| Type | Trades | Wins | Win Rate |
|------|--------|------|----------|
| Long | {len(long_trades)} | {long_wins} | {100*long_wins/len(long_trades) if long_trades else 0:.1f}% |
| Short | {len(short_trades)} | {short_wins} | {100*short_wins/len(short_trades) if short_trades else 0:.1f}% |

### Win/Loss Distribution
- **Winning Trades**: {winning_trades} ({win_rate:.1f}%)
- **Losing Trades**: {losing_trades} ({100-win_rate:.1f}%)
- **Gross Profit**: {gross_profit:.2f} points
- **Gross Loss**: {gross_loss:.2f} points

## Strategy Configuration
| Parameter | Value |
|-----------|-------|
| Swing Lookback | {SWING_LOOKBACK} bars |
| Major FVG Lookback | {FVG_LOOKBACK} bars |
| Entry FVG Lookback | {ENTRY_FVG_LOOKBACK} bars |
| Initial Capital | ${self.initial_capital:,.2f} |
| Contract Point Value | $20 (NQ) |

## Data Period
- **Start**: {self.df['Datetime'].iloc[0]}
- **End**: {self.df['Datetime'].iloc[-1]}
- **Total Bars**: {len(self.df):,}

## Equity Curve
![Equity Curve](equity_curve.png)

---
*Report generated by SMC Reversal Strategy Backtester*
"""
        
        # Save report
        report_path = os.path.join(output_dir, 'backtest_report.md')
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"Report saved to: {report_path}")
        
        # Generate equity curve chart
        plt.figure(figsize=(14, 7))
        plt.subplot(1, 1, 1)
        plt.plot(self.equity_curve, 'b-', linewidth=1.5, label='Equity')
        plt.axhline(y=self.initial_capital, color='gray', linestyle='--', alpha=0.7, label='Initial Capital')
        plt.fill_between(range(len(self.equity_curve)), self.initial_capital, self.equity_curve, 
                         where=[e >= self.initial_capital for e in self.equity_curve], 
                         alpha=0.3, color='green', label='Profit')
        plt.fill_between(range(len(self.equity_curve)), self.initial_capital, self.equity_curve,
                         where=[e < self.initial_capital for e in self.equity_curve],
                         alpha=0.3, color='red', label='Drawdown')
        plt.title('SMC Reversal Strategy - Equity Curve', fontsize=14, fontweight='bold')
        plt.xlabel('Trade Number', fontsize=12)
        plt.ylabel('Equity ($)', fontsize=12)
        plt.legend(loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        chart_path = os.path.join(output_dir, 'equity_curve.png')
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Equity curve saved to: {chart_path}")


def main():
    """Main entry point."""
    # Get data directory
    data_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("SMC REVERSAL STRATEGY BACKTESTER")
    print("=" * 60)
    
    # Load data
    df = load_data(data_dir)
    
    # Add technical indicators
    df = add_technical_indicators(df)
    
    # Run backtest
    backtester = SMCBacktester(df)
    backtester.run_backtest()
    
    # Generate report
    backtester.generate_report(data_dir)
    
    print("\n" + "=" * 60)
    print("BACKTEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
