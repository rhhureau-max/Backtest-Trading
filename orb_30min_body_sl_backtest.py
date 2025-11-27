"""
Opening Range Breakout (ORB) Backtesting Strategy for NQ Futures
30-MINUTE OPENING RANGE WITH BODY-BASED STOP LOSS VERSION

This script implements an ORB backtesting strategy with:
- Opening Range: High/Low of 08:30-09:00 CT (14:30-15:00 UTC) - 30 minutes
- Breakout: After 09:00 CT (15:00 UTC)
- Stop Loss: Under the BODY of breakout candle (not the wick)
  - Long: min(Open, Close) of breakout candle
  - Short: max(Open, Close) of breakout candle
- Take Profit: Variable R:R ratios (1:1 to 1:5)
- Filter: Skip days with range < 20 points
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, time
from dataclasses import dataclass, field
from typing import Optional, List, Dict
import warnings
warnings.filterwarnings('ignore')


@dataclass
class Trade:
    """Represents a single trade"""
    date: str
    direction: str  # 'LONG' or 'SHORT'
    entry_price: float
    entry_time: str
    stop_loss: float
    take_profits: Dict[int, float] = field(default_factory=dict)  # RR -> price
    exit_price: float = 0.0
    exit_time: str = ''
    exit_type: str = ''  # 'SL', 'TP1', 'TP2', ..., 'TP5', 'EOD'
    exit_rr: int = 0  # Which RR target was hit (1-5)
    pnl: float = 0.0
    risk: float = 0.0
    range_size: float = 0.0
    candle_body_bottom: float = 0.0
    candle_body_top: float = 0.0


class ORB30MinBodySLBacktester:
    """Opening Range Breakout Backtester with 30-min Range and Body-Based Stop Loss"""
    
    # Time constants (in UTC)
    RANGE_START = time(14, 30)  # 08:30 CT = 14:30 UTC
    RANGE_END = time(15, 0)     # 09:00 CT = 15:00 UTC (30-minute opening range)
    SESSION_END = time(21, 0)   # 15:00 CT = 21:00 UTC (end of regular session)
    
    # Strategy parameters
    MIN_RANGE = 20  # Minimum range size in points
    RR_RATIOS = [1, 2, 3, 4, 5]  # Test R:R from 1:1 to 1:5
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.trades: List[Trade] = []
        self.all_data: pd.DataFrame = pd.DataFrame()
        
    def load_data(self, years: List[int] = None) -> pd.DataFrame:
        """Load 5-minute data for specified years"""
        if years is None:
            # Dynamically detect available years from data files
            available_files = list(self.data_dir.glob("*5m.csv"))
            years = sorted(set(
                int(f.stem.split()[0]) for f in available_files 
                if f.stem.split()[0].isdigit()
            ))
        
        all_dfs = []
        for year in years:
            file_path = self.data_dir / f"{year} 5m.csv"
            if file_path.exists():
                df = pd.read_csv(
                    file_path,
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )
                df['Year'] = year
                all_dfs.append(df)
                print(f"Loaded {year}: {len(df)} rows")
            else:
                print(f"File not found: {file_path}")
        
        if not all_dfs:
            raise ValueError("No data files found")
        
        self.all_data = pd.concat(all_dfs, ignore_index=True)
        
        # Parse datetime
        self.all_data['DateTime'] = pd.to_datetime(
            self.all_data['Date'] + ' ' + self.all_data['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        self.all_data['TimeOnly'] = pd.to_datetime(self.all_data['Time'], format='%H:%M:%S').dt.time
        self.all_data['DateOnly'] = pd.to_datetime(self.all_data['Date'], format='%d/%m/%Y').dt.date
        
        # Convert price columns to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            self.all_data[col] = pd.to_numeric(self.all_data[col], errors='coerce')
        
        self.all_data.sort_values('DateTime', inplace=True)
        self.all_data.reset_index(drop=True, inplace=True)
        
        print(f"\nTotal rows loaded: {len(self.all_data)}")
        return self.all_data
    
    def calculate_opening_range(self, day_data: pd.DataFrame) -> Optional[dict]:
        """Calculate the opening range (High/Low) for 08:30-09:00 CT (14:30-15:00 UTC) - 30 min"""
        range_data = day_data[
            (day_data['TimeOnly'] >= self.RANGE_START) &
            (day_data['TimeOnly'] < self.RANGE_END)
        ]
        
        # Need 6 candles for 30-minute range (14:30, 14:35, 14:40, 14:45, 14:50, 14:55)
        if len(range_data) < 6:
            return None
        
        range_high = range_data['High'].max()
        range_low = range_data['Low'].min()
        range_size = range_high - range_low
        
        return {
            'high': range_high,
            'low': range_low,
            'size': range_size,
            'mid': (range_high + range_low) / 2
        }
    
    def find_breakout_with_candle(self, day_data: pd.DataFrame, range_info: dict) -> Optional[dict]:
        """Find the first breakout after 09:00 CT (15:00 UTC) and return candle info"""
        # Only look for breakouts AFTER 09:00 CT (15:00 UTC)
        post_range_data = day_data[
            (day_data['TimeOnly'] >= self.RANGE_END) &
            (day_data['TimeOnly'] < self.SESSION_END)
        ]
        
        for _, candle in post_range_data.iterrows():
            # Calculate body bounds
            candle_body_bottom = min(candle['Open'], candle['Close'])
            candle_body_top = max(candle['Open'], candle['Close'])
            
            # Long breakout: candle closes above range high
            if candle['Close'] > range_info['high']:
                return {
                    'direction': 'LONG',
                    'entry_price': candle['Close'],
                    'entry_time': candle['Time'],
                    'entry_idx': candle.name,
                    'candle_low': candle['Low'],
                    'candle_high': candle['High'],
                    'candle_open': candle['Open'],
                    'candle_close': candle['Close'],
                    'candle_body_bottom': candle_body_bottom,
                    'candle_body_top': candle_body_top
                }
            
            # Short breakout: candle closes below range low
            if candle['Close'] < range_info['low']:
                return {
                    'direction': 'SHORT',
                    'entry_price': candle['Close'],
                    'entry_time': candle['Time'],
                    'entry_idx': candle.name,
                    'candle_low': candle['Low'],
                    'candle_high': candle['High'],
                    'candle_open': candle['Open'],
                    'candle_close': candle['Close'],
                    'candle_body_bottom': candle_body_bottom,
                    'candle_body_top': candle_body_top
                }
        
        return None
    
    def calculate_body_stops_and_targets(self, direction: str, entry_price: float, 
                                          breakout: dict) -> Optional[dict]:
        """Calculate stop loss based on candle BODY and take profit levels for RR 1-5
        
        For LONG: Stop loss under the BODY bottom (min of open/close)
        For SHORT: Stop loss above the BODY top (max of open/close)
        """
        if direction == 'LONG':
            # Stop loss under the BODY of breakout candle (not the wick)
            stop_loss = breakout['candle_body_bottom']
            risk = entry_price - stop_loss
            
            # Validate risk is positive
            if risk <= 0:
                return None
            
            # Calculate take profits for each RR ratio
            take_profits = {}
            for rr in self.RR_RATIOS:
                take_profits[rr] = entry_price + (rr * risk)
                
        else:  # SHORT
            # Stop loss above the BODY of breakout candle (not the wick)
            stop_loss = breakout['candle_body_top']
            risk = stop_loss - entry_price
            
            # Validate risk is positive
            if risk <= 0:
                return None
            
            # Calculate take profits for each RR ratio
            take_profits = {}
            for rr in self.RR_RATIOS:
                take_profits[rr] = entry_price - (rr * risk)
        
        return {
            'stop_loss': stop_loss,
            'take_profits': take_profits,
            'risk': risk
        }
    
    def simulate_trade(self, day_data: pd.DataFrame, breakout: dict, 
                       levels: dict) -> dict:
        """Simulate the trade to find exit - checks all RR levels"""
        direction = breakout['direction']
        entry_price = breakout['entry_price']
        entry_idx = breakout['entry_idx']
        
        post_entry_data = day_data[
            (day_data.index > entry_idx) &
            (day_data['TimeOnly'] < self.SESSION_END)
        ]
        
        for _, candle in post_entry_data.iterrows():
            sl_hit = False
            tp_hits = {}  # RR -> hit or not
            
            if direction == 'LONG':
                sl_hit = candle['Low'] <= levels['stop_loss']
                for rr, tp_price in levels['take_profits'].items():
                    tp_hits[rr] = candle['High'] >= tp_price
                
                # Find highest TP hit without SL
                if not sl_hit:
                    for rr in sorted(tp_hits.keys(), reverse=True):
                        if tp_hits[rr]:
                            return self._create_exit(
                                breakout, levels, 
                                levels['take_profits'][rr],
                                candle['Time'], f'TP{rr}', rr
                            )
                
                # If SL hit
                if sl_hit:
                    # Check if any TP was also hit in same candle
                    highest_tp_hit = None
                    for rr in sorted(tp_hits.keys(), reverse=True):
                        if tp_hits[rr]:
                            highest_tp_hit = rr
                            break
                    
                    if highest_tp_hit:
                        # Use candle direction to determine order
                        candle_bullish = candle['Close'] >= candle['Open']
                        if candle_bullish:
                            # Bullish: went down first (SL), then up
                            return self._create_exit(
                                breakout, levels, 
                                levels['stop_loss'],
                                candle['Time'], 'SL', 0
                            )
                        else:
                            # Bearish: went up first (TP), then down
                            return self._create_exit(
                                breakout, levels, 
                                levels['take_profits'][highest_tp_hit],
                                candle['Time'], f'TP{highest_tp_hit}', highest_tp_hit
                            )
                    else:
                        return self._create_exit(
                            breakout, levels, 
                            levels['stop_loss'],
                            candle['Time'], 'SL', 0
                        )
                        
            else:  # SHORT
                sl_hit = candle['High'] >= levels['stop_loss']
                for rr, tp_price in levels['take_profits'].items():
                    tp_hits[rr] = candle['Low'] <= tp_price
                
                # Find highest TP hit without SL
                if not sl_hit:
                    for rr in sorted(tp_hits.keys(), reverse=True):
                        if tp_hits[rr]:
                            return self._create_exit(
                                breakout, levels, 
                                levels['take_profits'][rr],
                                candle['Time'], f'TP{rr}', rr
                            )
                
                # If SL hit
                if sl_hit:
                    highest_tp_hit = None
                    for rr in sorted(tp_hits.keys(), reverse=True):
                        if tp_hits[rr]:
                            highest_tp_hit = rr
                            break
                    
                    if highest_tp_hit:
                        candle_bearish = candle['Close'] <= candle['Open']
                        if candle_bearish:
                            # Bearish: went up first (SL), then down
                            return self._create_exit(
                                breakout, levels, 
                                levels['stop_loss'],
                                candle['Time'], 'SL', 0
                            )
                        else:
                            # Bullish: went down first (TP), then up
                            return self._create_exit(
                                breakout, levels, 
                                levels['take_profits'][highest_tp_hit],
                                candle['Time'], f'TP{highest_tp_hit}', highest_tp_hit
                            )
                    else:
                        return self._create_exit(
                            breakout, levels, 
                            levels['stop_loss'],
                            candle['Time'], 'SL', 0
                        )
        
        # End of day exit
        if len(post_entry_data) > 0:
            last_candle = post_entry_data.iloc[-1]
            return self._create_exit(
                breakout, levels,
                last_candle['Close'],
                last_candle['Time'], 'EOD', 0
            )
        
        return self._create_exit(
            breakout, levels,
            entry_price,
            breakout['entry_time'], 'EOD', 0
        )
    
    def _create_exit(self, breakout: dict, levels: dict, 
                     exit_price: float, exit_time: str, 
                     exit_type: str, exit_rr: int) -> dict:
        """Create exit information"""
        direction = breakout['direction']
        entry_price = breakout['entry_price']
        
        if direction == 'LONG':
            pnl = exit_price - entry_price
        else:
            pnl = entry_price - exit_price
        
        return {
            'exit_price': exit_price,
            'exit_time': exit_time,
            'exit_type': exit_type,
            'exit_rr': exit_rr,
            'pnl': pnl
        }
    
    def run_backtest(self) -> List[Trade]:
        """Run the complete backtest"""
        if self.all_data.empty:
            raise ValueError("No data loaded. Call load_data() first.")
        
        self.trades = []
        unique_dates = self.all_data['DateOnly'].unique()
        
        skipped_narrow = 0
        skipped_no_range = 0
        skipped_no_breakout = 0
        
        for date in unique_dates:
            day_data = self.all_data[self.all_data['DateOnly'] == date].copy()
            
            # Calculate opening range (30 minutes: 08:30-09:00)
            range_info = self.calculate_opening_range(day_data)
            if range_info is None:
                skipped_no_range += 1
                continue
            
            # Skip if range is too narrow
            if range_info['size'] < self.MIN_RANGE:
                skipped_narrow += 1
                continue
            
            # Find breakout with candle info (after 09:00)
            breakout = self.find_breakout_with_candle(day_data, range_info)
            if breakout is None:
                skipped_no_breakout += 1
                continue
            
            # Calculate body-based stops and targets
            levels = self.calculate_body_stops_and_targets(
                breakout['direction'],
                breakout['entry_price'],
                breakout
            )
            
            if levels is None:
                skipped_no_breakout += 1
                continue
            
            # Simulate trade
            exit_info = self.simulate_trade(day_data, breakout, levels)
            
            # Create trade record
            trade = Trade(
                date=str(date),
                direction=breakout['direction'],
                entry_price=breakout['entry_price'],
                entry_time=breakout['entry_time'],
                stop_loss=levels['stop_loss'],
                take_profits=levels['take_profits'],
                exit_price=exit_info['exit_price'],
                exit_time=exit_info['exit_time'],
                exit_type=exit_info['exit_type'],
                exit_rr=exit_info['exit_rr'],
                pnl=exit_info['pnl'],
                risk=levels['risk'],
                range_size=range_info['size'],
                candle_body_bottom=breakout['candle_body_bottom'],
                candle_body_top=breakout['candle_body_top']
            )
            self.trades.append(trade)
        
        print(f"\nBacktest Summary:")
        print(f"  Total trades: {len(self.trades)}")
        print(f"  Skipped (no range data): {skipped_no_range}")
        print(f"  Skipped (narrow range): {skipped_narrow}")
        print(f"  Skipped (no breakout): {skipped_no_breakout}")
        
        return self.trades
    
    def calculate_metrics_for_rr(self, target_rr: int) -> dict:
        """Calculate performance metrics for a specific R:R target
        
        For each R:R target, we calculate what would happen if we ONLY targeted
        that specific R:R level. A trade is a WIN only if it reaches the target TP.
        Trades that hit lower TPs are counted based on their actual outcome
        (would have continued to either hit target TP or SL/EOD).
        """
        if not self.trades:
            return {}
        
        # Recalculate P&L based on specific RR target
        pnls = []
        wins = []
        losses = []
        exit_types = {'SL': 0, f'TP{target_rr}': 0, 'EOD': 0}
        
        for t in self.trades:
            # Determine exit for this RR target
            if t.exit_type == 'SL':
                # Hit stop loss - this is a loss
                pnl = -t.risk
                exit_types['SL'] += 1
                pnls.append(pnl)
                losses.append(pnl)
            elif t.exit_rr >= target_rr:
                # Hit or exceeded target RR - this is a WIN
                pnl = t.risk * target_rr
                exit_types[f'TP{target_rr}'] += 1
                pnls.append(pnl)
                wins.append(pnl)
            elif t.exit_type == 'EOD':
                # Closed at EOD without hitting target - use actual PnL
                pnl = t.pnl
                exit_types['EOD'] += 1
                pnls.append(pnl)
                if pnl > 0:
                    wins.append(pnl)
                else:
                    losses.append(pnl)
            elif t.exit_rr > 0 and t.exit_rr < target_rr:
                # Hit a lower TP but not the target - this means we would have
                # continued holding and eventually hit EOD (since we didn't hit SL)
                # Use actual exit P&L from the lower TP
                pnl = t.risk * t.exit_rr  # P&L at the lower TP level
                exit_types['EOD'] += 1  # Categorize as EOD since target wasn't hit
                pnls.append(pnl)
                # This is NOT a win for this target RR (didn't hit target)
                # but P&L is positive
                wins.append(pnl)  # Still positive P&L
            else:
                # Fallback for any other case
                pnl = t.pnl
                exit_types['OTHER'] = exit_types.get('OTHER', 0) + 1
                pnls.append(pnl)
                if pnl > 0:
                    wins.append(pnl)
                else:
                    losses.append(pnl)
        
        total_trades = len(self.trades)
        
        # Win rate: only count trades that HIT the specific target RR
        target_wins = sum(1 for t in self.trades if t.exit_rr >= target_rr)
        win_rate = (target_wins / total_trades * 100) if total_trades > 0 else 0
        
        # Profit factor
        gross_profit = sum(wins) if wins else 0
        gross_loss = abs(sum(losses)) if losses else 0
        if gross_loss == 0:
            profit_factor = float('inf') if gross_profit > 0 else 0
        else:
            profit_factor = gross_profit / gross_loss
        
        # Drawdown calculation
        cumulative_pnl = np.cumsum(pnls)
        running_max = np.maximum.accumulate(cumulative_pnl)
        drawdowns = running_max - cumulative_pnl
        max_drawdown = np.max(drawdowns) if len(drawdowns) > 0 else 0
        
        # Direction breakdown
        long_trades = [t for t in self.trades if t.direction == 'LONG']
        short_trades = [t for t in self.trades if t.direction == 'SHORT']
        
        # Win rate by direction (only count hits of target RR)
        long_wins = sum(1 for t in self.trades if t.direction == 'LONG' and t.exit_rr >= target_rr)
        short_wins = sum(1 for t in self.trades if t.direction == 'SHORT' and t.exit_rr >= target_rr)
        
        return {
            'rr_target': target_rr,
            'total_trades': total_trades,
            'winning_trades': target_wins,
            'losing_trades': total_trades - target_wins,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_pnl': sum(pnls),
            'avg_pnl': np.mean(pnls) if pnls else 0,
            'max_drawdown': max_drawdown,
            'long_trades': len(long_trades),
            'short_trades': len(short_trades),
            'long_win_rate': (long_wins / len(long_trades) * 100) if long_trades else 0,
            'short_win_rate': (short_wins / len(short_trades) * 100) if short_trades else 0,
            'exit_types': exit_types,
            'avg_risk': np.mean([t.risk for t in self.trades])
        }
    
    def calculate_all_metrics(self) -> dict:
        """Calculate metrics for all RR ratios"""
        all_metrics = {}
        for rr in self.RR_RATIOS:
            all_metrics[rr] = self.calculate_metrics_for_rr(rr)
        
        # Also calculate yearly breakdown
        yearly_performance = {}
        for t in self.trades:
            try:
                date_str = str(t.date) if t.date else ""
                if '/' in date_str:
                    parts = date_str.split('/')
                    if len(parts) >= 3 and parts[-1].isdigit() and len(parts[-1]) >= 4:
                        year = parts[-1][:4]
                    else:
                        year = "Unknown"
                elif '-' in date_str:
                    parts = date_str.split('-')
                    if len(parts) >= 1 and parts[0].isdigit() and len(parts[0]) == 4:
                        year = parts[0]
                    else:
                        year = "Unknown"
                else:
                    year = "Unknown"
            except (IndexError, AttributeError, TypeError):
                year = "Unknown"
            
            if year not in yearly_performance:
                yearly_performance[year] = {
                    'trades': 0, 'long': 0, 'short': 0,
                    'exit_types': {}
                }
            
            yearly_performance[year]['trades'] += 1
            if t.direction == 'LONG':
                yearly_performance[year]['long'] += 1
            else:
                yearly_performance[year]['short'] += 1
            
            et = t.exit_type
            yearly_performance[year]['exit_types'][et] = yearly_performance[year]['exit_types'].get(et, 0) + 1
        
        return {
            'rr_metrics': all_metrics,
            'yearly': yearly_performance,
            'avg_range_size': np.mean([t.range_size for t in self.trades]),
            'avg_risk': np.mean([t.risk for t in self.trades])
        }
    
    def generate_report(self, all_metrics: dict) -> str:
        """Generate markdown report with RR comparison"""
        report = []
        report.append("# Opening Range Breakout (ORB) Backtest Report")
        report.append("## 30-Minute Opening Range with Body-Based Stop Loss")
        report.append("## R:R Analysis (1:1 to 1:5)")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## Strategy Overview")
        report.append("")
        report.append("This report presents the backtesting results of an Opening Range Breakout (ORB) strategy")
        report.append("with a **30-minute opening range** and **body-based stop loss** placement.")
        report.append("")
        report.append("### Strategy Rules")
        report.append("- **Opening Range**: High/Low of **08:30-09:00 CT** (14:30-15:00 UTC) - **30 minutes**")
        report.append("- **Entry Signal**: After 09:00 CT, first 5-min candle that closes above/below the range")
        report.append("- **Long Signal**: 5-minute candle closes above the range high")
        report.append("- **Short Signal**: 5-minute candle closes below the range low")
        report.append("- **Stop Loss**: Under the **BODY** of breakout candle (not the wick)")
        report.append("  - Long: min(Open, Close) of breakout candle")
        report.append("  - Short: max(Open, Close) of breakout candle")
        report.append("- **Take Profit**: Variable R:R ratios tested (1:1, 1:2, 1:3, 1:4, 1:5)")
        report.append("- **Filter**: Skip days with opening range < 20 points")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## R:R Comparison Summary")
        report.append("")
        report.append("| R:R Target | Win Rate | Profit Factor | Total P&L (pts) | Max Drawdown (pts) | Avg P&L |")
        report.append("|------------|----------|---------------|-----------------|--------------------|---------| ")
        
        rr_metrics = all_metrics['rr_metrics']
        for rr in self.RR_RATIOS:
            m = rr_metrics[rr]
            pf = f"{m['profit_factor']:.2f}" if m['profit_factor'] != float('inf') else "∞"
            report.append(f"| **1:{rr}** | {m['win_rate']:.2f}% | {pf} | {m['total_pnl']:.2f} | {m['max_drawdown']:.2f} | {m['avg_pnl']:.2f} |")
        
        report.append("")
        report.append("---")
        report.append("")
        
        # Detailed metrics for each RR
        for rr in self.RR_RATIOS:
            m = rr_metrics[rr]
            report.append(f"## Detailed Results: R:R 1:{rr}")
            report.append("")
            report.append("| Metric | Value |")
            report.append("|--------|-------|")
            report.append(f"| Total Trades | {m['total_trades']} |")
            report.append(f"| Winning Trades | {m['winning_trades']} |")
            report.append(f"| Losing Trades | {m['losing_trades']} |")
            report.append(f"| **Win Rate** | **{m['win_rate']:.2f}%** |")
            pf = f"{m['profit_factor']:.2f}" if m['profit_factor'] != float('inf') else "∞"
            report.append(f"| **Profit Factor** | **{pf}** |")
            report.append(f"| Total P&L (points) | {m['total_pnl']:.2f} |")
            report.append(f"| Average P&L per Trade | {m['avg_pnl']:.2f} |")
            report.append(f"| **Max Drawdown (points)** | **{m['max_drawdown']:.2f}** |")
            report.append(f"| Long Trades | {m['long_trades']} ({m['long_win_rate']:.1f}% win) |")
            report.append(f"| Short Trades | {m['short_trades']} ({m['short_win_rate']:.1f}% win) |")
            report.append("")
            
            # Exit types for this RR
            report.append(f"### Exit Distribution (1:{rr} Target)")
            report.append("")
            report.append("| Exit Type | Count | Percentage |")
            report.append("|-----------|-------|------------|")
            total = m['total_trades']
            for et, count in sorted(m['exit_types'].items()):
                pct = (count / total * 100) if total > 0 else 0
                report.append(f"| {et} | {count} | {pct:.1f}% |")
            
            report.append("")
            report.append("---")
            report.append("")
        
        # Yearly performance
        report.append("## Annual Performance Breakdown")
        report.append("")
        report.append("| Year | Trades | Long | Short | SL | TP1 | TP2 | TP3 | TP4 | TP5 | EOD |")
        report.append("|------|--------|------|-------|----|----|----|----|----|----|-----|")
        
        yearly = all_metrics['yearly']
        for year in sorted(yearly.keys()):
            yp = yearly[year]
            et = yp['exit_types']
            sl = et.get('SL', 0)
            tp1 = et.get('TP1', 0)
            tp2 = et.get('TP2', 0)
            tp3 = et.get('TP3', 0)
            tp4 = et.get('TP4', 0)
            tp5 = et.get('TP5', 0)
            eod = et.get('EOD', 0)
            report.append(f"| {year} | {yp['trades']} | {yp['long']} | {yp['short']} | {sl} | {tp1} | {tp2} | {tp3} | {tp4} | {tp5} | {eod} |")
        
        report.append("")
        report.append("---")
        report.append("")
        
        # Risk analysis
        report.append("## Risk Analysis")
        report.append("")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Average Range Size (30 min) | {all_metrics['avg_range_size']:.2f} points |")
        report.append(f"| Average Risk (SL Distance) | {all_metrics['avg_risk']:.2f} points |")
        report.append("")
        report.append("### Key Insights")
        report.append("")
        
        # Find best performing RR
        best_rr = max(rr_metrics.keys(), key=lambda x: rr_metrics[x]['total_pnl'])
        best_pf_rr = max(rr_metrics.keys(), key=lambda x: rr_metrics[x]['profit_factor'] if rr_metrics[x]['profit_factor'] != float('inf') else 0)
        best_wr_rr = max(rr_metrics.keys(), key=lambda x: rr_metrics[x]['win_rate'])
        
        report.append(f"- **Best P&L Performance**: R:R 1:{best_rr} with {rr_metrics[best_rr]['total_pnl']:.2f} points")
        best_pf = rr_metrics[best_pf_rr]['profit_factor']
        best_pf_str = f"{best_pf:.2f}" if best_pf != float('inf') else "∞"
        report.append(f"- **Best Profit Factor**: R:R 1:{best_pf_rr} with {best_pf_str}")
        report.append(f"- **Highest Win Rate**: R:R 1:{best_wr_rr} with {rr_metrics[best_wr_rr]['win_rate']:.2f}%")
        report.append("")
        
        # Strategy comparison with previous version
        report.append("### Strategy Differences from Previous Versions")
        report.append("")
        report.append("| Parameter | 15-min Range + Candle Low SL | 30-min Range + Body SL |")
        report.append("|-----------|------------------------------|------------------------|")
        report.append("| Opening Range | 08:30-08:45 (15 min) | **08:30-09:00 (30 min)** |")
        report.append("| Breakout After | 08:45 | **09:00** |")
        report.append("| Stop Loss Placement | Under candle LOW | **Under candle BODY** |")
        report.append("| Risk Size | Larger (full wick) | Smaller (body only) |")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## Notes")
        report.append("")
        report.append("- **Opening Range**: 30-minute range from 08:30-09:00 CT (14:30-15:00 UTC)")
        report.append("- **Stop Loss Placement**: Under the BODY of the breakout candle")
        report.append("  - For LONG: Stop = min(Open, Close)")
        report.append("  - For SHORT: Stop = max(Open, Close)")
        report.append("- **Risk Calculation**: Entry price minus Body Bottom (for longs)")
        report.append("- All P&L values are in NQ Futures points (1 point = $20 per contract)")
        report.append("- Time zone: Data is in UTC, strategy uses New York (CT) session times")
        report.append("- Regular session end: 15:00 CT = 21:00 UTC")
        report.append("")
        report.append("---")
        report.append("")
        report.append(f"*Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(report)


def main():
    """Main function to run the backtest"""
    data_dir = Path(__file__).parent
    
    print("=" * 70)
    print("Opening Range Breakout (ORB) Backtest")
    print("30-MINUTE OPENING RANGE (08:30-09:00 CT)")
    print("BODY-BASED STOP LOSS")
    print("NQ Futures 5-Minute Data (2018-2025)")
    print("Testing R:R Ratios: 1:1 to 1:5")
    print("=" * 70)
    print()
    
    # Initialize backtester
    backtester = ORB30MinBodySLBacktester(data_dir)
    
    # Load data
    print("Loading data...")
    backtester.load_data()
    
    # Run backtest
    print("\nRunning backtest...")
    trades = backtester.run_backtest()
    
    # Calculate all metrics
    print("\nCalculating metrics for all R:R ratios...")
    all_metrics = backtester.calculate_all_metrics()
    
    # Print summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY - 30-Min Range + Body-Based Stop Loss")
    print("=" * 70)
    print()
    print(f"Total Trades: {len(trades)}")
    print(f"Average Risk (SL Distance): {all_metrics['avg_risk']:.2f} points")
    print(f"Average Range Size (30 min): {all_metrics['avg_range_size']:.2f} points")
    print()
    print("-" * 70)
    print("R:R Comparison:")
    print("-" * 70)
    print(f"{'R:R':<8} {'Win Rate':<12} {'Profit Factor':<15} {'Total P&L':<15} {'Max DD':<12}")
    print("-" * 70)
    
    for rr in backtester.RR_RATIOS:
        m = all_metrics['rr_metrics'][rr]
        pf = f"{m['profit_factor']:.2f}" if m['profit_factor'] != float('inf') else "∞"
        print(f"1:{rr:<6} {m['win_rate']:.2f}%{'':<5} {pf:<15} {m['total_pnl']:.2f}{'':<5} {m['max_drawdown']:.2f}")
    
    print("=" * 70)
    
    # Generate and save report
    print("\nGenerating report...")
    report = backtester.generate_report(all_metrics)
    
    report_path = data_dir / "ORB_30Min_Body_SL_Report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
