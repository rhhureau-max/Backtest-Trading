"""
NQ Futures Range Breakout Backtesting Tool
===========================================
This script implements a range breakout strategy backtesting system.

Strategy:
- LONG: When a candle breaks above the high of the previous 15 candles
  and closes above that range high
- SHORT: When a candle breaks below the low of the previous 15 candles
  and closes below that range low

Features:
- Multiple timeframes: 1m, 5m, 15m
- Multiple stop-loss levels: 50%, 75%, 100% retracement
- Multiple take-profit targets: R:R 1, 2, 3, 4, 5
- Time filter: 02:00 to 12:00
"""

import os
import zipfile
import pandas as pd
import numpy as np
import yaml
from datetime import datetime, time
from dataclasses import dataclass
from typing import List, Optional, Dict
from io import StringIO


@dataclass
class Trade:
    """Represents a single trade."""
    entry_time: datetime
    entry_price: float
    direction: str  # 'LONG' or 'SHORT'
    stop_loss: float
    take_profit: float
    sl_type: str  # 'SL_50', 'SL_75', 'SL_100'
    rr_target: int  # 1, 2, 3, 4, 5
    timeframe: str  # '1m', '5m', '15m'
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    pnl: Optional[float] = None
    result: Optional[str] = None  # 'WIN', 'LOSS', 'OPEN'
    year: Optional[int] = None


class RangeBreakoutBacktester:
    """Main backtesting class for range breakout strategy."""

    def __init__(self, config_path: str = 'config_range.yaml'):
        """Initialize the backtester with configuration."""
        self.config = self._load_config(config_path)
        self.data_1m: Optional[pd.DataFrame] = None
        self.data_5m: Optional[pd.DataFrame] = None
        self.data_15m: Optional[pd.DataFrame] = None
        self.trades: List[Trade] = []

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        default_config = {
            'data': {
                'start_year': 2018,
                'end_year': 2025,
                'data_directory': '.'
            },
            'strategy': {
                'lookback_period': 15,
                'timeframes': ['1m', '5m', '15m'],
                'sl_levels': [0.50, 0.75, 1.00],
                'rr_targets': [1, 2, 3, 4, 5]
            },
            'trading_session': {
                'start': '02:00:00',
                'end': '12:00:00'
            },
            'output': {
                'results_directory': 'results',
                'report_file': 'range_breakout_report.md',
                'trades_log_file': 'range_breakout_trades.csv'
            }
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return default_config

    def load_data(self) -> None:
        """Load all required timeframe data."""
        print("Loading 1-minute data...")
        self.data_1m = self._load_timeframe_data('1m')
        
        print("Loading 5-minute data...")
        self.data_5m = self._load_timeframe_data('5m')
        
        print("Loading 15-minute data...")
        self.data_15m = self._load_timeframe_data('15m')

    def _load_timeframe_data(self, timeframe: str) -> pd.DataFrame:
        """Load and concatenate data for a specific timeframe."""
        all_data = []
        data_dir = self.config['data']['data_directory']
        
        for year in range(self.config['data']['start_year'],
                         self.config['data']['end_year'] + 1):
            # Try compressed file first, then uncompressed
            zip_file = os.path.join(data_dir, f"{year} {timeframe}.csv.zip")
            csv_file = os.path.join(data_dir, f"{year} {timeframe}.csv")
            
            df = None
            if os.path.exists(zip_file):
                with zipfile.ZipFile(zip_file, 'r') as z:
                    file_list = z.namelist()
                    if file_list:
                        with z.open(file_list[0]) as f:
                            raw_bytes = f.read()
                            try:
                                content = raw_bytes.decode('utf-8')
                            except UnicodeDecodeError:
                                content = raw_bytes.decode('utf-8', errors='replace')
                            df = pd.read_csv(StringIO(content), sep=';')
            elif os.path.exists(csv_file):
                df = pd.read_csv(csv_file, sep=';')
            else:
                print(f"  Warning: No {timeframe} data file found for year {year}")
                continue
            
            if df is not None and not df.empty:
                all_data.append(df)
                print(f"  Loaded {len(df)} rows for {year} {timeframe}")
        
        if not all_data:
            raise ValueError(f"No {timeframe} data files found!")
        
        # Concatenate all dataframes
        data = pd.concat(all_data, ignore_index=True)
        
        # Parse datetime
        data['datetime'] = pd.to_datetime(
            data['Column1'] + ' ' + data['Column2'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Rename columns
        data = data.rename(columns={
            'Column3': 'Open',
            'Column4': 'High',
            'Column5': 'Low',
            'Column6': 'Close',
            'Column7': 'Volume'
        })
        
        # Sort by datetime
        data = data.sort_values('datetime').reset_index(drop=True)
        
        # Add derived columns
        data['year'] = data['datetime'].dt.year
        data['time'] = data['datetime'].dt.time
        
        print(f"  Total {timeframe} data: {len(data)} rows")
        return data

    def _is_in_trading_session(self, t: time) -> bool:
        """Check if a time is within the trading session."""
        session = self.config['trading_session']
        start = datetime.strptime(session['start'], '%H:%M:%S').time()
        end = datetime.strptime(session['end'], '%H:%M:%S').time()
        return start <= t <= end

    def detect_range_breakout(self, data: pd.DataFrame, idx: int, lookback: int) -> tuple:
        """
        Detect if current bar breaks the range of previous N bars.
        Returns: (direction, range_high, range_low) or (None, None, None)
        """
        if idx < lookback:
            return None, None, None
        
        # Get the range of previous N bars (excluding current bar)
        prev_bars = data.iloc[idx - lookback:idx]
        range_high = prev_bars['High'].max()
        range_low = prev_bars['Low'].min()
        
        current_bar = data.iloc[idx]
        current_close = current_bar['Close']
        current_high = current_bar['High']
        current_low = current_bar['Low']
        
        # LONG: Close breaks above range high
        if current_close > range_high and current_high > range_high:
            return 'LONG', range_high, range_low
        
        # SHORT: Close breaks below range low
        if current_close < range_low and current_low < range_low:
            return 'SHORT', range_high, range_low
        
        return None, None, None

    def calculate_stop_loss(self, bar: pd.Series, direction: str, sl_pct: float) -> float:
        """Calculate stop loss based on retracement of signal candle."""
        close = bar['Close']
        
        if direction == 'LONG':
            low = bar['Low']
            # SL is between close and low (retracement)
            return close - (close - low) * sl_pct
        else:  # SHORT
            high = bar['High']
            # SL is between close and high (retracement)
            return close + (high - close) * sl_pct

    def calculate_take_profit(self, entry_price: float, stop_loss: float, 
                             direction: str, rr_ratio: int) -> float:
        """Calculate take profit based on risk-reward ratio."""
        risk = abs(entry_price - stop_loss)
        reward = risk * rr_ratio
        
        if direction == 'LONG':
            return entry_price + reward
        else:  # SHORT
            return entry_price - reward

    def simulate_trade_exit(self, trade: Trade, data: pd.DataFrame, entry_idx: int) -> Trade:
        """Simulate trade exit by checking subsequent bars."""
        for i in range(entry_idx + 1, len(data)):
            bar = data.iloc[i]
            
            if trade.direction == 'LONG':
                # Check stop loss hit
                if bar['Low'] <= trade.stop_loss:
                    trade.exit_time = bar['datetime']
                    trade.exit_price = trade.stop_loss
                    trade.pnl = trade.exit_price - trade.entry_price
                    trade.result = 'LOSS'
                    return trade
                
                # Check take profit hit
                if bar['High'] >= trade.take_profit:
                    trade.exit_time = bar['datetime']
                    trade.exit_price = trade.take_profit
                    trade.pnl = trade.exit_price - trade.entry_price
                    trade.result = 'WIN'
                    return trade
            
            else:  # SHORT
                # Check stop loss hit
                if bar['High'] >= trade.stop_loss:
                    trade.exit_time = bar['datetime']
                    trade.exit_price = trade.stop_loss
                    trade.pnl = trade.entry_price - trade.exit_price
                    trade.result = 'LOSS'
                    return trade
                
                # Check take profit hit
                if bar['Low'] <= trade.take_profit:
                    trade.exit_time = bar['datetime']
                    trade.exit_price = trade.take_profit
                    trade.pnl = trade.entry_price - trade.exit_price
                    trade.result = 'WIN'
                    return trade
        
        # Trade still open at end of data
        trade.result = 'OPEN'
        return trade

    def run_backtest_for_timeframe(self, timeframe: str, data: pd.DataFrame) -> List[Trade]:
        """Run backtest for a specific timeframe."""
        trades = []
        lookback = self.config['strategy']['lookback_period']
        sl_levels = self.config['strategy']['sl_levels']
        rr_targets = self.config['strategy']['rr_targets']
        
        total_bars = len(data)
        print(f"\n  Processing {timeframe} ({total_bars} bars)...")
        
        # Track signals to avoid duplicates
        processed_signals = set()
        
        for idx in range(lookback, total_bars):
            if idx % 100000 == 0:
                print(f"    Bar {idx}/{total_bars} ({100*idx/total_bars:.1f}%)")
            
            current_bar = data.iloc[idx]
            current_time = current_bar['time']
            
            # Check if in trading session (02:00 to 12:00)
            if not self._is_in_trading_session(current_time):
                continue
            
            # Detect range breakout
            direction, range_high, range_low = self.detect_range_breakout(
                data, idx, lookback
            )
            
            if direction is None:
                continue
            
            entry_price = current_bar['Close']
            entry_time = current_bar['datetime']
            current_year = current_bar['year']
            
            # Create trades for each SL level and RR target combination
            for sl_pct in sl_levels:
                for rr_target in rr_targets:
                    sl_name = f"SL_{int(sl_pct * 100)}"
                    signal_key = (entry_time, direction, sl_name, rr_target, timeframe)
                    
                    if signal_key in processed_signals:
                        continue
                    processed_signals.add(signal_key)
                    
                    stop_loss = self.calculate_stop_loss(current_bar, direction, sl_pct)
                    take_profit = self.calculate_take_profit(
                        entry_price, stop_loss, direction, rr_target
                    )
                    
                    trade = Trade(
                        entry_time=entry_time,
                        entry_price=entry_price,
                        direction=direction,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        sl_type=sl_name,
                        rr_target=rr_target,
                        timeframe=timeframe,
                        year=current_year
                    )
                    
                    # Simulate trade exit
                    trade = self.simulate_trade_exit(trade, data, idx)
                    trades.append(trade)
        
        return trades

    def run_backtest(self) -> List[Trade]:
        """Run the complete backtest for all timeframes."""
        if self.data_1m is None:
            self.load_data()
        
        self.trades = []
        timeframes = self.config['strategy']['timeframes']
        
        print("\nRunning backtest...")
        
        if '1m' in timeframes and self.data_1m is not None:
            self.trades.extend(self.run_backtest_for_timeframe('1m', self.data_1m))
        
        if '5m' in timeframes and self.data_5m is not None:
            self.trades.extend(self.run_backtest_for_timeframe('5m', self.data_5m))
        
        if '15m' in timeframes and self.data_15m is not None:
            self.trades.extend(self.run_backtest_for_timeframe('15m', self.data_15m))
        
        print(f"\nBacktest complete. Total trades: {len(self.trades)}")
        return self.trades

    def calculate_statistics(self) -> Dict:
        """Calculate comprehensive performance statistics."""
        if not self.trades:
            return {}
        
        # Filter out open trades
        closed_trades = [t for t in self.trades if t.result in ['WIN', 'LOSS']]
        
        if not closed_trades:
            return {'error': 'No closed trades'}
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'entry_time': t.entry_time,
            'entry_price': t.entry_price,
            'exit_time': t.exit_time,
            'exit_price': t.exit_price,
            'direction': t.direction,
            'sl_type': t.sl_type,
            'rr_target': t.rr_target,
            'timeframe': t.timeframe,
            'stop_loss': t.stop_loss,
            'take_profit': t.take_profit,
            'pnl': t.pnl,
            'result': t.result,
            'year': t.year
        } for t in closed_trades])
        
        def calc_metrics(subset):
            if len(subset) == 0:
                return None
            
            wins = subset[subset['result'] == 'WIN']
            losses = subset[subset['result'] == 'LOSS']
            
            win_rate = len(wins) / len(subset) * 100 if len(subset) > 0 else 0
            
            avg_win = wins['pnl'].mean() if len(wins) > 0 else 0
            avg_loss = abs(losses['pnl'].mean()) if len(losses) > 0 else 0
            
            total_profit = wins['pnl'].sum() if len(wins) > 0 else 0
            total_loss = abs(losses['pnl'].sum()) if len(losses) > 0 else 0
            
            profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')
            
            return {
                'trades': len(subset),
                'wins': len(wins),
                'losses': len(losses),
                'win_rate': round(win_rate, 2),
                'avg_win': round(avg_win, 2),
                'avg_loss': round(avg_loss, 2),
                'profit_factor': round(profit_factor, 2) if profit_factor != float('inf') else None,
                'total_pnl': round(subset['pnl'].sum(), 2)
            }
        
        stats = {
            'total_trades': len(closed_trades),
            'overall': calc_metrics(df),
            'by_timeframe': {},
            'by_sl_type': {},
            'by_rr_target': {},
            'by_direction': {},
            'by_timeframe_sl_rr': {},
            'matrix': {}  # Win rate matrix: SL x RR for each timeframe
        }
        
        # By timeframe
        for tf in df['timeframe'].unique():
            subset = df[df['timeframe'] == tf]
            stats['by_timeframe'][tf] = calc_metrics(subset)
        
        # By SL type
        for sl in sorted(df['sl_type'].unique()):
            subset = df[df['sl_type'] == sl]
            stats['by_sl_type'][sl] = calc_metrics(subset)
        
        # By RR target
        for rr in sorted(df['rr_target'].unique()):
            subset = df[df['rr_target'] == rr]
            stats['by_rr_target'][f'RR_{rr}'] = calc_metrics(subset)
        
        # By direction
        for direction in df['direction'].unique():
            subset = df[df['direction'] == direction]
            stats['by_direction'][direction] = calc_metrics(subset)
        
        # Create win rate matrix for each timeframe
        for tf in sorted(df['timeframe'].unique()):
            tf_df = df[df['timeframe'] == tf]
            matrix = {}
            for sl in sorted(tf_df['sl_type'].unique()):
                matrix[sl] = {}
                for rr in sorted(tf_df['rr_target'].unique()):
                    subset = tf_df[(tf_df['sl_type'] == sl) & (tf_df['rr_target'] == rr)]
                    if len(subset) > 0:
                        wins = len(subset[subset['result'] == 'WIN'])
                        matrix[sl][f'RR_{rr}'] = round(wins / len(subset) * 100, 2)
                    else:
                        matrix[sl][f'RR_{rr}'] = 0
            stats['matrix'][tf] = matrix
        
        # Detailed breakdown: timeframe + SL + RR
        for tf in sorted(df['timeframe'].unique()):
            for sl in sorted(df['sl_type'].unique()):
                for rr in sorted(df['rr_target'].unique()):
                    subset = df[(df['timeframe'] == tf) & 
                               (df['sl_type'] == sl) & 
                               (df['rr_target'] == rr)]
                    key = f"{tf}_{sl}_RR{rr}"
                    stats['by_timeframe_sl_rr'][key] = calc_metrics(subset)
        
        return stats

    def save_trades_log(self, output_path: str):
        """Save detailed trade log to CSV."""
        if not self.trades:
            print("No trades to save.")
            return
        
        df = pd.DataFrame([{
            'Entry_Time': t.entry_time,
            'Exit_Time': t.exit_time,
            'Direction': t.direction,
            'Entry_Price': t.entry_price,
            'Exit_Price': t.exit_price,
            'Stop_Loss': t.stop_loss,
            'Take_Profit': t.take_profit,
            'SL_Type': t.sl_type,
            'RR_Target': t.rr_target,
            'Timeframe': t.timeframe,
            'PnL': t.pnl,
            'Result': t.result,
            'Year': t.year
        } for t in self.trades])
        
        df.to_csv(output_path, index=False)
        print(f"Trade log saved to {output_path}")

    @staticmethod
    def _format_stat(value) -> str:
        """Format statistic value for report, handling None values."""
        return 'N/A' if value is None else str(value)

    def generate_report(self, output_path: str, stats: Dict):
        """Generate detailed markdown report."""
        report = []
        report.append("# NQ Futures Range Breakout Backtest Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n**Data Period:** {self.config['data']['start_year']} - {self.config['data']['end_year']}")
        report.append(f"\n**Trading Session:** 02:00 - 12:00")
        
        report.append("\n\n## Strategy Overview")
        report.append("\nThis backtest evaluates a range breakout strategy:")
        report.append("- **LONG**: Current candle closes above the high of the previous 15 candles")
        report.append("- **SHORT**: Current candle closes below the low of the previous 15 candles")
        report.append("- **Timeframes**: 1m, 5m, 15m")
        report.append("- **Stop Loss Levels**: 50%, 75%, 100% retracement of signal candle")
        report.append("- **Take Profit Targets**: Risk-Reward ratios of 1, 2, 3, 4, 5")
        
        report.append("\n\n## Overall Performance")
        if 'overall' in stats and stats['overall']:
            o = stats['overall']
            report.append(f"\n| Metric | Value |")
            report.append(f"|--------|-------|")
            report.append(f"| Total Trades | {o['trades']} |")
            report.append(f"| Wins | {o['wins']} |")
            report.append(f"| Losses | {o['losses']} |")
            report.append(f"| Win Rate | {o['win_rate']}% |")
            report.append(f"| Average Win | {o['avg_win']} pts |")
            report.append(f"| Average Loss | {o['avg_loss']} pts |")
            report.append(f"| Profit Factor | {self._format_stat(o['profit_factor'])} |")
            report.append(f"| Total P&L | {o['total_pnl']} pts |")
        
        report.append("\n\n## Performance by Timeframe")
        if 'by_timeframe' in stats:
            report.append(f"\n| Timeframe | Trades | Win Rate | Profit Factor | Total P&L |")
            report.append(f"|-----------|--------|----------|---------------|-----------|")
            for tf, m in sorted(stats['by_timeframe'].items()):
                if m:
                    report.append(f"| {tf} | {m['trades']} | {m['win_rate']}% | {self._format_stat(m['profit_factor'])} | {m['total_pnl']} |")
        
        report.append("\n\n## Performance by Stop Loss Type")
        if 'by_sl_type' in stats:
            report.append(f"\n| SL Type | Trades | Win Rate | Profit Factor | Total P&L |")
            report.append(f"|---------|--------|----------|---------------|-----------|")
            for sl, m in sorted(stats['by_sl_type'].items()):
                if m:
                    report.append(f"| {sl} | {m['trades']} | {m['win_rate']}% | {self._format_stat(m['profit_factor'])} | {m['total_pnl']} |")
        
        report.append("\n\n## Performance by Risk-Reward Target")
        if 'by_rr_target' in stats:
            report.append(f"\n| RR Target | Trades | Win Rate | Profit Factor | Total P&L |")
            report.append(f"|-----------|--------|----------|---------------|-----------|")
            for rr, m in sorted(stats['by_rr_target'].items()):
                if m:
                    report.append(f"| {rr} | {m['trades']} | {m['win_rate']}% | {self._format_stat(m['profit_factor'])} | {m['total_pnl']} |")
        
        report.append("\n\n## Performance by Direction")
        if 'by_direction' in stats:
            report.append(f"\n| Direction | Trades | Wins | Losses | Win Rate | Profit Factor | Total P&L |")
            report.append(f"|-----------|--------|------|--------|----------|---------------|-----------|")
            for direction, m in stats['by_direction'].items():
                if m:
                    report.append(f"| {direction} | {m['trades']} | {m['wins']} | {m['losses']} | {m['win_rate']}% | {self._format_stat(m['profit_factor'])} | {m['total_pnl']} |")
        
        # Win Rate Matrix for each timeframe
        report.append("\n\n## Win Rate Matrix (SL% x R:R Target)")
        if 'matrix' in stats:
            for tf, matrix in sorted(stats['matrix'].items()):
                report.append(f"\n### {tf} Timeframe")
                
                # Get RR columns
                if matrix:
                    first_sl = list(matrix.keys())[0]
                    rr_cols = sorted(matrix[first_sl].keys())
                    
                    header = "| SL Type | " + " | ".join(rr_cols) + " |"
                    separator = "|---------|" + "|".join(["-----" for _ in rr_cols]) + "|"
                    report.append(f"\n{header}")
                    report.append(separator)
                    
                    for sl in sorted(matrix.keys()):
                        row = f"| {sl} |"
                        for rr in rr_cols:
                            row += f" {matrix[sl][rr]}% |"
                        report.append(row)
        
        # Detailed breakdown table
        report.append("\n\n## Detailed Breakdown (Timeframe + SL + RR)")
        if 'by_timeframe_sl_rr' in stats:
            report.append(f"\n| Combo | Trades | Win Rate | Wins | Losses | Profit Factor | Total P&L |")
            report.append(f"|-------|--------|----------|------|--------|---------------|-----------|")
            for combo, m in sorted(stats['by_timeframe_sl_rr'].items()):
                if m and m['trades'] > 0:
                    report.append(f"| {combo} | {m['trades']} | {m['win_rate']}% | {m['wins']} | {m['losses']} | {self._format_stat(m['profit_factor'])} | {m['total_pnl']} |")
        
        report.append("\n\n## Configuration")
        report.append(f"\n```yaml")
        report.append(f"Lookback Period: 15 bars")
        report.append(f"Timeframes: 1m, 5m, 15m")
        report.append(f"Stop Loss Levels: [50%, 75%, 100%]")
        report.append(f"Risk-Reward Targets: [1, 2, 3, 4, 5]")
        report.append(f"Trading Session: 02:00 - 12:00")
        report.append(f"```")
        
        report.append("\n\n## Trade Log")
        report.append("\nSee `range_breakout_trades.csv` for detailed trade-by-trade breakdown.")
        
        report.append("\n\n---")
        report.append("\n*Report generated by NQ Futures Range Breakout Backtester*")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"Report saved to {output_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='NQ Futures Range Breakout Backtester')
    parser.add_argument('--config', default='config_range.yaml', 
                       help='Path to configuration file')
    args = parser.parse_args()
    
    print("=" * 60)
    print("NQ Futures Range Breakout Backtester")
    print("=" * 60)
    
    backtester = RangeBreakoutBacktester(config_path=args.config)
    
    # Load data
    backtester.load_data()
    
    # Run backtest
    trades = backtester.run_backtest()
    
    # Calculate statistics
    stats = backtester.calculate_statistics()
    
    # Create results directory
    results_dir = backtester.config['output']['results_directory']
    os.makedirs(results_dir, exist_ok=True)
    
    # Save outputs
    trades_log_path = os.path.join(results_dir, 
                                   backtester.config['output']['trades_log_file'])
    report_path = os.path.join(results_dir, 
                               backtester.config['output']['report_file'])
    
    backtester.save_trades_log(trades_log_path)
    backtester.generate_report(report_path, stats)
    
    # Print summary
    print("\n" + "=" * 60)
    print("BACKTEST COMPLETE")
    print("=" * 60)
    
    if 'overall' in stats and stats['overall']:
        print(f"\nTotal Trades: {stats['overall']['trades']}")
        print(f"Win Rate: {stats['overall']['win_rate']}%")
        print(f"Profit Factor: {stats['overall']['profit_factor']}")
        print(f"Total P&L: {stats['overall']['total_pnl']} points")
    
    # Print win rate matrix summary
    if 'matrix' in stats:
        for tf, matrix in sorted(stats['matrix'].items()):
            print(f"\n{tf} Win Rate Matrix (SL% x R:R):")
            if matrix:
                first_sl = list(matrix.keys())[0]
                rr_cols = sorted(matrix[first_sl].keys())
                print("          " + "  ".join([f"{rr:>6}" for rr in rr_cols]))
                for sl in sorted(matrix.keys()):
                    row = f"{sl:>8}  " + "  ".join([f"{matrix[sl][rr]:>5.1f}%" for rr in rr_cols])
                    print(row)
    
    print(f"\nResults saved to: {results_dir}/")
    print(f"  - {backtester.config['output']['report_file']}")
    print(f"  - {backtester.config['output']['trades_log_file']}")


if __name__ == '__main__':
    main()
