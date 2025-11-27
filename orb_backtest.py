"""
Opening Range Breakout (ORB) Backtesting Strategy for NQ Futures

This script implements a complete ORB backtesting strategy using 5-minute NQ Futures data.

Strategy Rules:
- Opening Range: High/Low of 08:30-08:45 CT (14:30-14:45 UTC)
- Long Signal: 5-min candle closes above the range high
- Short Signal: 5-min candle closes below the range low
- Stop Loss: 50% of range OR opposite end if range < 40 points
- Take Profit: TP1 = 1:1 RR, TP2 = 1:2 RR
- Filter: Skip days with range < 20 points
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, time, timedelta
from dataclasses import dataclass
from typing import Optional, List
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
    tp1: float
    tp2: float
    exit_price: float = 0.0
    exit_time: str = ''
    exit_type: str = ''  # 'SL', 'TP1', 'TP2', 'EOD'
    pnl: float = 0.0
    range_size: float = 0.0
    

class ORBBacktester:
    """Opening Range Breakout Backtester for NQ Futures"""
    
    # Time constants (in UTC)
    RANGE_START = time(14, 30)  # 08:30 CT = 14:30 UTC
    RANGE_END = time(14, 45)    # 08:45 CT = 14:45 UTC
    SESSION_END = time(21, 0)   # 15:00 CT = 21:00 UTC (end of regular session)
    
    # Strategy parameters
    MIN_RANGE = 20  # Minimum range size in points
    NARROW_RANGE_THRESHOLD = 40  # Threshold for using opposite end as SL
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.trades: List[Trade] = []
        self.all_data: pd.DataFrame = pd.DataFrame()
        
    def load_data(self, years: List[int] = None) -> pd.DataFrame:
        """Load 5-minute data for specified years"""
        if years is None:
            years = list(range(2018, 2026))
        
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
        """Calculate the opening range (High/Low) for 08:30-08:45 CT (14:30-14:45 UTC)"""
        # Filter for the opening range period (14:30, 14:35, 14:40)
        # 14:30 candle covers 14:30:00 to 14:34:59
        # 14:35 candle covers 14:35:00 to 14:39:59
        # 14:40 candle covers 14:40:00 to 14:44:59
        range_data = day_data[
            (day_data['TimeOnly'] >= self.RANGE_START) &
            (day_data['TimeOnly'] < self.RANGE_END)
        ]
        
        if len(range_data) < 3:  # Need at least 3 candles (14:30, 14:35, 14:40)
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
    
    def find_breakout(self, day_data: pd.DataFrame, range_info: dict) -> Optional[dict]:
        """Find the first breakout after the opening range"""
        # Get candles after the opening range (14:45 and onwards)
        post_range_data = day_data[
            (day_data['TimeOnly'] >= self.RANGE_END) &
            (day_data['TimeOnly'] < self.SESSION_END)
        ]
        
        for _, candle in post_range_data.iterrows():
            # Long breakout: candle closes above range high
            if candle['Close'] > range_info['high']:
                return {
                    'direction': 'LONG',
                    'entry_price': candle['Close'],
                    'entry_time': candle['Time'],
                    'entry_idx': candle.name
                }
            
            # Short breakout: candle closes below range low
            if candle['Close'] < range_info['low']:
                return {
                    'direction': 'SHORT',
                    'entry_price': candle['Close'],
                    'entry_time': candle['Time'],
                    'entry_idx': candle.name
                }
        
        return None
    
    def calculate_stops_and_targets(self, direction: str, entry_price: float, 
                                     range_info: dict) -> Optional[dict]:
        """Calculate stop loss and take profit levels"""
        range_size = range_info['size']
        
        if direction == 'LONG':
            # Stop loss: 50% of range OR opposite end if range < 40 points
            if range_size < self.NARROW_RANGE_THRESHOLD:
                stop_loss = range_info['low']
            else:
                stop_loss = range_info['mid']
            
            risk = entry_price - stop_loss
            # Validate risk is positive (entry must be above stop loss for long)
            if risk <= 0:
                return None
            tp1 = entry_price + risk  # 1:1 RR
            tp2 = entry_price + (2 * risk)  # 1:2 RR
        else:  # SHORT
            if range_size < self.NARROW_RANGE_THRESHOLD:
                stop_loss = range_info['high']
            else:
                stop_loss = range_info['mid']
            
            risk = stop_loss - entry_price
            # Validate risk is positive (entry must be below stop loss for short)
            if risk <= 0:
                return None
            tp1 = entry_price - risk  # 1:1 RR
            tp2 = entry_price - (2 * risk)  # 1:2 RR
        
        return {
            'stop_loss': stop_loss,
            'tp1': tp1,
            'tp2': tp2,
            'risk': risk
        }
    
    def simulate_trade(self, day_data: pd.DataFrame, breakout: dict, 
                       levels: dict) -> dict:
        """Simulate the trade to find exit
        
        When multiple levels could be hit in the same candle, we use the candle's
        open-to-close direction to infer which level was likely hit first.
        
        Note: This is a simplification. In reality, intra-candle price action
        cannot be determined from OHLC data alone. We assume:
        - For longs in bearish candles: price went up first (potential TP), then down
        - For longs in bullish candles: price went down first (potential SL), then up
        This heuristic may not always be accurate.
        """
        direction = breakout['direction']
        entry_price = breakout['entry_price']
        entry_idx = breakout['entry_idx']
        
        # Get all candles after entry until session end
        post_entry_data = day_data[
            (day_data.index > entry_idx) &
            (day_data['TimeOnly'] < self.SESSION_END)
        ]
        
        for _, candle in post_entry_data.iterrows():
            sl_hit = False
            tp1_hit = False
            tp2_hit = False
            
            if direction == 'LONG':
                sl_hit = candle['Low'] <= levels['stop_loss']
                tp1_hit = candle['High'] >= levels['tp1']
                tp2_hit = candle['High'] >= levels['tp2']
                
                # If only one level hit, exit at that level
                if sl_hit and not tp1_hit and not tp2_hit:
                    return self._create_exit(breakout, levels, levels['stop_loss'], 
                                            candle['Time'], 'SL')
                if tp2_hit and not sl_hit:
                    return self._create_exit(breakout, levels, levels['tp2'], 
                                            candle['Time'], 'TP2')
                if tp1_hit and not sl_hit:
                    return self._create_exit(breakout, levels, levels['tp1'], 
                                            candle['Time'], 'TP1')
                
                # Multiple levels hit - use candle direction to determine order
                if sl_hit and (tp1_hit or tp2_hit):
                    candle_bullish = candle['Close'] >= candle['Open']
                    if candle_bullish:
                        # Bullish candle: likely went down first (SL), then up
                        return self._create_exit(breakout, levels, levels['stop_loss'], 
                                                candle['Time'], 'SL')
                    else:
                        # Bearish candle: likely went up first (TP), then down
                        if tp2_hit:
                            return self._create_exit(breakout, levels, levels['tp2'], 
                                                    candle['Time'], 'TP2')
                        return self._create_exit(breakout, levels, levels['tp1'], 
                                                candle['Time'], 'TP1')
            else:  # SHORT
                sl_hit = candle['High'] >= levels['stop_loss']
                tp1_hit = candle['Low'] <= levels['tp1']
                tp2_hit = candle['Low'] <= levels['tp2']
                
                # If only one level hit, exit at that level
                if sl_hit and not tp1_hit and not tp2_hit:
                    return self._create_exit(breakout, levels, levels['stop_loss'], 
                                            candle['Time'], 'SL')
                if tp2_hit and not sl_hit:
                    return self._create_exit(breakout, levels, levels['tp2'], 
                                            candle['Time'], 'TP2')
                if tp1_hit and not sl_hit:
                    return self._create_exit(breakout, levels, levels['tp1'], 
                                            candle['Time'], 'TP1')
                
                # Multiple levels hit - use candle direction to determine order
                if sl_hit and (tp1_hit or tp2_hit):
                    candle_bearish = candle['Close'] <= candle['Open']
                    if candle_bearish:
                        # Bearish candle: likely went up first (SL), then down
                        return self._create_exit(breakout, levels, levels['stop_loss'], 
                                                candle['Time'], 'SL')
                    else:
                        # Bullish candle: likely went down first (TP), then up
                        if tp2_hit:
                            return self._create_exit(breakout, levels, levels['tp2'], 
                                                    candle['Time'], 'TP2')
                        return self._create_exit(breakout, levels, levels['tp1'], 
                                                candle['Time'], 'TP1')
        
        # End of day exit
        if len(post_entry_data) > 0:
            last_candle = post_entry_data.iloc[-1]
            return self._create_exit(breakout, levels,
                                    last_candle['Close'],
                                    last_candle['Time'], 'EOD')
        
        # No data after entry - use entry price
        return self._create_exit(breakout, levels,
                                entry_price,
                                breakout['entry_time'], 'EOD')
    
    def _create_exit(self, breakout: dict, levels: dict, 
                     exit_price: float, exit_time: str, exit_type: str) -> dict:
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
            
            # Calculate opening range
            range_info = self.calculate_opening_range(day_data)
            if range_info is None:
                skipped_no_range += 1
                continue
            
            # Skip if range is too narrow
            if range_info['size'] < self.MIN_RANGE:
                skipped_narrow += 1
                continue
            
            # Find breakout
            breakout = self.find_breakout(day_data, range_info)
            if breakout is None:
                skipped_no_breakout += 1
                continue
            
            # Calculate stops and targets
            levels = self.calculate_stops_and_targets(
                breakout['direction'],
                breakout['entry_price'],
                range_info
            )
            
            # Skip if risk calculation is invalid (entry on wrong side of stop)
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
                tp1=levels['tp1'],
                tp2=levels['tp2'],
                exit_price=exit_info['exit_price'],
                exit_time=exit_info['exit_time'],
                exit_type=exit_info['exit_type'],
                pnl=exit_info['pnl'],
                range_size=range_info['size']
            )
            self.trades.append(trade)
        
        print(f"\nBacktest Summary:")
        print(f"  Total trades: {len(self.trades)}")
        print(f"  Skipped (no range data): {skipped_no_range}")
        print(f"  Skipped (narrow range): {skipped_narrow}")
        print(f"  Skipped (no breakout): {skipped_no_breakout}")
        
        return self.trades
    
    def calculate_metrics(self) -> dict:
        """Calculate performance metrics"""
        if not self.trades:
            return {}
        
        pnls = [t.pnl for t in self.trades]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]
        
        # Basic metrics
        total_trades = len(self.trades)
        winning_trades = len(wins)
        losing_trades = len(losses)
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Profit factor
        gross_profit = sum(wins) if wins else 0
        gross_loss = abs(sum(losses)) if losses else 1
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Drawdown calculation
        cumulative_pnl = np.cumsum(pnls)
        running_max = np.maximum.accumulate(cumulative_pnl)
        drawdowns = running_max - cumulative_pnl
        max_drawdown = np.max(drawdowns) if len(drawdowns) > 0 else 0
        
        # Direction breakdown
        long_trades = [t for t in self.trades if t.direction == 'LONG']
        short_trades = [t for t in self.trades if t.direction == 'SHORT']
        
        long_wins = len([t for t in long_trades if t.pnl > 0])
        short_wins = len([t for t in short_trades if t.pnl > 0])
        
        # Exit type breakdown
        exit_types = {}
        for t in self.trades:
            exit_types[t.exit_type] = exit_types.get(t.exit_type, 0) + 1
        
        # Yearly performance
        yearly_performance = {}
        for t in self.trades:
            year = t.date[:4]
            if year not in yearly_performance:
                yearly_performance[year] = {
                    'trades': 0, 'wins': 0, 'pnl': 0, 'long': 0, 'short': 0
                }
            yearly_performance[year]['trades'] += 1
            yearly_performance[year]['pnl'] += t.pnl
            if t.pnl > 0:
                yearly_performance[year]['wins'] += 1
            if t.direction == 'LONG':
                yearly_performance[year]['long'] += 1
            else:
                yearly_performance[year]['short'] += 1
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_pnl': sum(pnls),
            'avg_pnl': np.mean(pnls),
            'max_drawdown': max_drawdown,
            'long_trades': len(long_trades),
            'short_trades': len(short_trades),
            'long_win_rate': (long_wins / len(long_trades) * 100) if long_trades else 0,
            'short_win_rate': (short_wins / len(short_trades) * 100) if short_trades else 0,
            'exit_types': exit_types,
            'yearly_performance': yearly_performance,
            'avg_range_size': np.mean([t.range_size for t in self.trades])
        }
    
    def generate_report(self, metrics: dict) -> str:
        """Generate markdown report"""
        report = []
        report.append("# Opening Range Breakout (ORB) Backtest Report")
        report.append("")
        report.append("## Strategy Overview")
        report.append("")
        report.append("This report presents the backtesting results of an Opening Range Breakout (ORB) strategy")
        report.append("applied to NQ Futures 5-minute data from 2018-2025.")
        report.append("")
        report.append("### Strategy Rules")
        report.append("- **Opening Range**: High/Low of 08:30-08:45 CT (14:30-14:45 UTC)")
        report.append("- **Long Signal**: 5-minute candle closes above the range high")
        report.append("- **Short Signal**: 5-minute candle closes below the range low")
        report.append("- **Stop Loss**: 50% of range OR opposite end if range < 40 points")
        report.append("- **Take Profit**: TP1 = 1:1 R/R, TP2 = 1:2 R/R")
        report.append("- **Filter**: Skip days with range < 20 points")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## Performance Summary")
        report.append("")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Total Trades | {metrics['total_trades']} |")
        report.append(f"| Winning Trades | {metrics['winning_trades']} |")
        report.append(f"| Losing Trades | {metrics['losing_trades']} |")
        report.append(f"| **Win Rate** | **{metrics['win_rate']:.2f}%** |")
        report.append(f"| **Profit Factor** | **{metrics['profit_factor']:.2f}** |")
        report.append(f"| Total P&L (points) | {metrics['total_pnl']:.2f} |")
        report.append(f"| Average P&L per Trade | {metrics['avg_pnl']:.2f} |")
        report.append(f"| **Max Drawdown (points)** | **{metrics['max_drawdown']:.2f}** |")
        report.append(f"| Average Range Size | {metrics['avg_range_size']:.2f} |")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## Long vs Short Distribution")
        report.append("")
        report.append("| Direction | Trades | Win Rate |")
        report.append("|-----------|--------|----------|")
        report.append(f"| Long | {metrics['long_trades']} | {metrics['long_win_rate']:.2f}% |")
        report.append(f"| Short | {metrics['short_trades']} | {metrics['short_win_rate']:.2f}% |")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## Exit Types")
        report.append("")
        report.append("| Exit Type | Count | Percentage |")
        report.append("|-----------|-------|------------|")
        
        total = metrics['total_trades']
        exit_labels = {'SL': 'Stop Loss', 'TP1': 'Take Profit 1 (1:1)', 
                       'TP2': 'Take Profit 2 (1:2)', 'EOD': 'End of Session'}
        for exit_type in ['SL', 'TP1', 'TP2', 'EOD']:
            count = metrics['exit_types'].get(exit_type, 0)
            pct = (count / total * 100) if total > 0 else 0
            label = exit_labels.get(exit_type, exit_type)
            report.append(f"| {label} | {count} | {pct:.1f}% |")
        
        report.append("")
        report.append("---")
        report.append("")
        report.append("## Annual Performance (2018-2025)")
        report.append("")
        report.append("| Year | Trades | Wins | Win Rate | P&L (points) | Long | Short |")
        report.append("|------|--------|------|----------|--------------|------|-------|")
        
        for year in sorted(metrics['yearly_performance'].keys()):
            yp = metrics['yearly_performance'][year]
            wr = (yp['wins'] / yp['trades'] * 100) if yp['trades'] > 0 else 0
            report.append(f"| {year} | {yp['trades']} | {yp['wins']} | {wr:.1f}% | {yp['pnl']:.2f} | {yp['long']} | {yp['short']} |")
        
        report.append("")
        report.append("---")
        report.append("")
        report.append("## Notes")
        report.append("")
        report.append("- All P&L values are in NQ Futures points (1 point = $20 per contract)")
        report.append("- Time zone: Data is in UTC, strategy uses New York (CT) session times")
        report.append("- Opening Range: 08:30-08:45 CT = 14:30-14:45 UTC")
        report.append("- Regular session end: 15:00 CT = 21:00 UTC")
        report.append("")
        report.append("---")
        report.append("")
        report.append(f"*Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(report)


def main():
    """Main function to run the backtest"""
    # Set data directory
    data_dir = Path(__file__).parent
    
    print("=" * 60)
    print("Opening Range Breakout (ORB) Backtest")
    print("NQ Futures 5-Minute Data (2018-2025)")
    print("=" * 60)
    print()
    
    # Initialize backtester
    backtester = ORBBacktester(data_dir)
    
    # Load data
    print("Loading data...")
    backtester.load_data()
    
    # Run backtest
    print("\nRunning backtest...")
    trades = backtester.run_backtest()
    
    # Calculate metrics
    print("\nCalculating metrics...")
    metrics = backtester.calculate_metrics()
    
    # Print summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total Trades: {metrics['total_trades']}")
    print(f"Win Rate: {metrics['win_rate']:.2f}%")
    print(f"Profit Factor: {metrics['profit_factor']:.2f}")
    print(f"Total P&L: {metrics['total_pnl']:.2f} points")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2f} points")
    print(f"Long Trades: {metrics['long_trades']} (Win Rate: {metrics['long_win_rate']:.1f}%)")
    print(f"Short Trades: {metrics['short_trades']} (Win Rate: {metrics['short_win_rate']:.1f}%)")
    print()
    
    # Generate and save report
    print("Generating report...")
    report = backtester.generate_report(metrics)
    
    report_path = data_dir / "ORB_Backtest_Report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_path}")
    print("=" * 60)
    
    # Also print yearly breakdown
    print("\nYearly Performance:")
    print("-" * 60)
    for year in sorted(metrics['yearly_performance'].keys()):
        yp = metrics['yearly_performance'][year]
        wr = (yp['wins'] / yp['trades'] * 100) if yp['trades'] > 0 else 0
        print(f"  {year}: {yp['trades']} trades, {wr:.1f}% win rate, {yp['pnl']:.2f} points")


if __name__ == "__main__":
    main()
