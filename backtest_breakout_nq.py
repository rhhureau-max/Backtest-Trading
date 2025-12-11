"""
NQ Futures Breakout Backtesting Tool
=====================================
This script implements a comprehensive backtesting system for NQ futures
based on oblique trendline breakouts with momentum confirmation.

Features:
- Dynamic oblique resistance/support line detection
- Momentum filter for breakout validation
- Multiple stop-loss scenarios
- Time-filtered trading sessions
- Detailed performance statistics
"""

import os
import zipfile
import pandas as pd
import numpy as np
import yaml
import matplotlib.pyplot as plt
from datetime import datetime, time
from dataclasses import dataclass
from typing import List, Tuple, Optional
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
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    pnl: Optional[float] = None
    result: Optional[str] = None  # 'WIN', 'LOSS', 'OPEN'
    session: Optional[str] = None
    year: Optional[int] = None


@dataclass
class SwingPoint:
    """Represents a swing high or swing low."""
    index: int
    time: datetime
    price: float
    type: str  # 'HIGH' or 'LOW'


class NQBacktester:
    """Main backtesting class for NQ futures breakout strategy."""
    
    # Configuration constants for plotting
    MAX_SL_TYPES_TO_PLOT = 3  # Maximum number of SL types to show in equity curve
    MAX_PLOT_HEIGHT_INCHES = 16  # Maximum figure height to prevent memory issues

    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize the backtester with configuration."""
        self.config = self._load_config(config_path)
        self.data: Optional[pd.DataFrame] = None
        self.trades: List[Trade] = []
        self.swing_highs: List[SwingPoint] = []
        self.swing_lows: List[SwingPoint] = []
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_data(self) -> pd.DataFrame:
        """Load and concatenate all 1-minute data from 2018-2025."""
        all_data = []
        data_dir = self.config['data']['data_directory']
        
        for year in range(self.config['data']['start_year'], 
                         self.config['data']['end_year'] + 1):
            # Try compressed file first, then uncompressed
            zip_file = os.path.join(data_dir, f"{year} 1m.csv.zip")
            csv_file = os.path.join(data_dir, f"{year} 1m.csv")
            
            df = None
            if os.path.exists(zip_file):
                print(f"Loading {zip_file}...")
                with zipfile.ZipFile(zip_file, 'r') as z:
                    # Get the first file in the zip
                    file_list = z.namelist()
                    if file_list:
                        with z.open(file_list[0]) as f:
                            raw_bytes = f.read()
                            try:
                                content = raw_bytes.decode('utf-8')
                            except UnicodeDecodeError:
                                content = raw_bytes.decode('utf-8', errors='replace')
                                print(f"  Warning: Encoding issues detected, some characters replaced")
                            df = pd.read_csv(StringIO(content), sep=';')
            elif os.path.exists(csv_file):
                print(f"Loading {csv_file}...")
                df = pd.read_csv(csv_file, sep=';')
            else:
                print(f"Warning: No data file found for year {year}")
                continue
            
            if df is not None and not df.empty:
                all_data.append(df)
                print(f"  Loaded {len(df)} rows for {year}")
        
        if not all_data:
            raise ValueError("No data files found!")
        
        # Concatenate all dataframes
        self.data = pd.concat(all_data, ignore_index=True)
        
        # Parse datetime
        self.data['datetime'] = pd.to_datetime(
            self.data['Column1'] + ' ' + self.data['Column2'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Rename columns for clarity
        self.data = self.data.rename(columns={
            'Column3': 'Open',
            'Column4': 'High',
            'Column5': 'Low',
            'Column6': 'Close',
            'Column7': 'Volume'
        })
        
        # Sort by datetime
        self.data = self.data.sort_values('datetime').reset_index(drop=True)
        
        # Add derived columns
        self.data['year'] = self.data['datetime'].dt.year
        self.data['time'] = self.data['datetime'].dt.time
        self.data['body'] = abs(self.data['Close'] - self.data['Open'])
        self.data['is_bullish'] = self.data['Close'] > self.data['Open']
        
        print(f"\nTotal data loaded: {len(self.data)} rows")
        print(f"Date range: {self.data['datetime'].min()} to {self.data['datetime'].max()}")
        
        return self.data
    
    def _is_in_trading_session(self, t: time) -> Tuple[bool, str]:
        """Check if a time is within active trading sessions."""
        sessions = self.config['trading_sessions']
        
        # Parse session times
        s1_start = datetime.strptime(sessions['session_1']['start'], '%H:%M:%S').time()
        s1_end = datetime.strptime(sessions['session_1']['end'], '%H:%M:%S').time()
        s2_start = datetime.strptime(sessions['session_2']['start'], '%H:%M:%S').time()
        s2_end = datetime.strptime(sessions['session_2']['end'], '%H:%M:%S').time()
        
        if s1_start <= t <= s1_end:
            return True, 'Session_1 (02:00-05:00)'
        elif s2_start <= t <= s2_end:
            return True, 'Session_2 (08:30-11:00)'
        return False, None
    
    def detect_swing_points(self, start_idx: int, lookback: int) -> Tuple[List[SwingPoint], List[SwingPoint]]:
        """
        Detect swing highs and swing lows in the lookback period.
        A swing high is a bar with high greater than both neighboring bars.
        A swing low is a bar with low less than both neighboring bars.
        """
        swing_highs = []
        swing_lows = []
        
        end_idx = start_idx
        begin_idx = max(0, start_idx - lookback)
        
        # Detect swings using completed bars only (no look-ahead bias)
        # A swing is confirmed when we have at least 2 bars after it to verify the reversal
        for i in range(begin_idx + 2, end_idx - 1):
            # Check for swing high (confirmed by lower highs on both sides)
            if i > 1 and i < end_idx - 1:
                if (self.data.iloc[i]['High'] > self.data.iloc[i-1]['High'] and
                    self.data.iloc[i]['High'] > self.data.iloc[i+1]['High']):
                    swing_highs.append(SwingPoint(
                        index=i,
                        time=self.data.iloc[i]['datetime'],
                        price=self.data.iloc[i]['High'],
                        type='HIGH'
                    ))
                
                # Check for swing low
                if (self.data.iloc[i]['Low'] < self.data.iloc[i-1]['Low'] and
                    self.data.iloc[i]['Low'] < self.data.iloc[i+1]['Low']):
                    swing_lows.append(SwingPoint(
                        index=i,
                        time=self.data.iloc[i]['datetime'],
                        price=self.data.iloc[i]['Low'],
                        type='LOW'
                    ))
        
        return swing_highs, swing_lows
    
    def calculate_trendline(self, points: List[SwingPoint]) -> Tuple[Optional[float], Optional[float]]:
        """
        Calculate oblique trendline from swing points.
        Returns slope and intercept.
        Uses the most recent points for the trendline.
        """
        if len(points) < 2:
            return None, None
        
        # Use the two most recent swing points
        points = sorted(points, key=lambda p: p.index)[-2:]
        
        x = np.array([p.index for p in points])
        y = np.array([p.price for p in points])
        
        # Calculate slope and intercept
        if len(x) >= 2 and x[-1] != x[0]:
            slope = (y[-1] - y[0]) / (x[-1] - x[0])
            intercept = y[0] - slope * x[0]
            return slope, intercept
        
        return None, None
    
    def get_trendline_value(self, slope: float, intercept: float, index: int) -> float:
        """Get the trendline value at a given index."""
        return slope * index + intercept
    
    def check_momentum_filter(self, idx: int, is_bullish: bool) -> bool:
        """
        Check if the breakout candle passes the momentum filter.
        The candle body must be larger than the average of the previous N candles.
        """
        avg_period = self.config['momentum']['average_period']
        
        if idx < avg_period:
            return False
        
        # Calculate average body of previous candles (use iloc for better performance)
        prev_bodies = self.data.iloc[idx - avg_period:idx]['body'].mean()
        current_body = self.data.iloc[idx]['body']
        
        # Check if current body is larger than average
        if current_body <= prev_bodies:
            return False
        
        # Check if candle direction matches the expected direction (use iloc)
        current_is_bullish = self.data.iloc[idx]['is_bullish']
        
        return current_is_bullish == is_bullish
    
    def find_initial_swing(self, swing_points: List[SwingPoint], direction: str) -> Optional[float]:
        """
        Find the first swing point of the trend for take profit target.
        For LONG: First swing high (initial peak of downtrend)
        For SHORT: First swing low (initial trough of uptrend)
        """
        if not swing_points:
            return None
        
        # Get the earliest swing point in the lookback period
        sorted_swings = sorted(swing_points, key=lambda p: p.index)
        if sorted_swings:
            return sorted_swings[0].price
        return None
    
    def calculate_stop_loss(self, idx: int, direction: str, sl_pct: float) -> float:
        """
        Calculate stop loss based on retracement of signal candle.
        """
        bar = self.data.iloc[idx]
        close = bar['Close']
        
        if direction == 'LONG':
            low = bar['Low']
            # SL is between close and low (retracement)
            sl = close - (close - low) * sl_pct
        else:  # SHORT
            high = bar['High']
            # SL is between close and high (retracement)
            sl = close + (high - close) * sl_pct
        
        return sl
    
    def detect_downtrend(self, swing_highs: List[SwingPoint]) -> bool:
        """
        Detect if we're in a downtrend (for LONG breakout setup).
        Downtrend: Lower swing highs.
        """
        if len(swing_highs) < 2:
            return False
        
        sorted_highs = sorted(swing_highs, key=lambda p: p.index)
        # Check if recent highs are lower than earlier highs
        for i in range(1, len(sorted_highs)):
            if sorted_highs[i].price >= sorted_highs[i-1].price:
                return False
        return True
    
    def detect_uptrend(self, swing_lows: List[SwingPoint]) -> bool:
        """
        Detect if we're in an uptrend (for SHORT breakdown setup).
        Uptrend: Higher swing lows.
        """
        if len(swing_lows) < 2:
            return False
        
        sorted_lows = sorted(swing_lows, key=lambda p: p.index)
        # Check if recent lows are higher than earlier lows
        for i in range(1, len(sorted_lows)):
            if sorted_lows[i].price <= sorted_lows[i-1].price:
                return False
        return True
    
    def simulate_trade_exit(self, trade: Trade, entry_idx: int) -> Trade:
        """
        Simulate trade exit by checking subsequent bars.
        Uses iloc for better performance.
        """
        for i in range(entry_idx + 1, len(self.data)):
            bar = self.data.iloc[i]
            
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
    
    def run_backtest(self) -> List[Trade]:
        """Run the complete backtest."""
        if self.data is None:
            self.load_data()
        
        lookback = self.config['swing_detection']['lookback_period']
        min_swings = self.config['swing_detection']['min_swing_points']
        sl_levels = self.config['stop_loss_levels']
        
        print("\nRunning backtest...")
        total_bars = len(self.data)
        
        # Track signals to avoid duplicate trades per bar (key: entry_time, direction, sl_type)
        processed_signals = set()
        
        for idx in range(lookback, total_bars):
            if idx % 100000 == 0:
                print(f"  Processing bar {idx}/{total_bars} ({100*idx/total_bars:.1f}%)")
            
            # Cache current bar data for performance
            current_bar = self.data.iloc[idx]
            current_time = current_bar['time']
            
            # Check if in trading session
            in_session, session_name = self._is_in_trading_session(current_time)
            
            if not in_session:
                continue
            
            # Detect swing points in lookback period
            swing_highs, swing_lows = self.detect_swing_points(idx, lookback)
            
            current_close = current_bar['Close']
            current_dt = current_bar['datetime']
            current_year = current_bar['year']
            
            # Check for LONG setup (breakout above resistance in downtrend)
            if len(swing_highs) >= min_swings and self.detect_downtrend(swing_highs):
                slope, intercept = self.calculate_trendline(swing_highs)
                
                if slope is not None and slope < 0:  # Downward sloping resistance
                    resistance_level = self.get_trendline_value(slope, intercept, idx)
                    
                    # Check for breakout
                    if current_close > resistance_level:
                        # Check momentum filter (bullish candle)
                        if self.check_momentum_filter(idx, is_bullish=True):
                            # Get take profit (first swing high)
                            take_profit = self.find_initial_swing(swing_highs, 'LONG')
                            
                            if take_profit is not None and take_profit > current_close:
                                # Create trades for each SL level
                                for sl_pct in sl_levels:
                                    sl_name = f"SL_{int(sl_pct*100)}"
                                    signal_key = (current_dt, 'LONG', sl_name)
                                    
                                    if signal_key not in processed_signals:
                                        processed_signals.add(signal_key)
                                        stop_loss = self.calculate_stop_loss(idx, 'LONG', sl_pct)
                                        
                                        trade = Trade(
                                            entry_time=current_dt,
                                            entry_price=current_close,
                                            direction='LONG',
                                            stop_loss=stop_loss,
                                            take_profit=take_profit,
                                            sl_type=sl_name,
                                            session=session_name,
                                            year=current_year
                                        )
                                        
                                        # Simulate trade exit
                                        trade = self.simulate_trade_exit(trade, idx)
                                        self.trades.append(trade)
            
            # Check for SHORT setup (breakdown below support in uptrend)
            if len(swing_lows) >= min_swings and self.detect_uptrend(swing_lows):
                slope, intercept = self.calculate_trendline(swing_lows)
                
                if slope is not None and slope > 0:  # Upward sloping support
                    support_level = self.get_trendline_value(slope, intercept, idx)
                    
                    # Check for breakdown
                    if current_close < support_level:
                        # Check momentum filter (bearish candle)
                        if self.check_momentum_filter(idx, is_bullish=False):
                            # Get take profit (first swing low)
                            take_profit = self.find_initial_swing(swing_lows, 'SHORT')
                            
                            if take_profit is not None and take_profit < current_close:
                                # Create trades for each SL level
                                for sl_pct in sl_levels:
                                    sl_name = f"SL_{int(sl_pct*100)}"
                                    signal_key = (current_dt, 'SHORT', sl_name)
                                    
                                    if signal_key not in processed_signals:
                                        processed_signals.add(signal_key)
                                        stop_loss = self.calculate_stop_loss(idx, 'SHORT', sl_pct)
                                        
                                        trade = Trade(
                                            entry_time=current_dt,
                                            entry_price=current_close,
                                            direction='SHORT',
                                            stop_loss=stop_loss,
                                            take_profit=take_profit,
                                            sl_type=sl_name,
                                            session=session_name,
                                            year=current_year
                                        )
                                        
                                        # Simulate trade exit
                                        trade = self.simulate_trade_exit(trade, idx)
                                        self.trades.append(trade)
        
        print(f"\nBacktest complete. Total trades: {len(self.trades)}")
        return self.trades
    
    def calculate_statistics(self) -> dict:
        """Calculate comprehensive performance statistics."""
        if not self.trades:
            return {}
        
        # Filter out open trades
        closed_trades = [t for t in self.trades if t.result in ['WIN', 'LOSS']]
        
        if not closed_trades:
            return {'error': 'No closed trades'}
        
        stats = {
            'total_trades': len(closed_trades),
            'by_sl_type': {},
            'by_direction': {},
            'by_session': {},
            'by_year': {},
            'overall': {}
        }
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame([{
            'entry_time': t.entry_time,
            'entry_price': t.entry_price,
            'exit_time': t.exit_time,
            'exit_price': t.exit_price,
            'direction': t.direction,
            'sl_type': t.sl_type,
            'stop_loss': t.stop_loss,
            'take_profit': t.take_profit,
            'pnl': t.pnl,
            'result': t.result,
            'session': t.session,
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
            
            rr_ratio = avg_win / avg_loss if avg_loss > 0 else float('inf')
            
            total_profit = wins['pnl'].sum() if len(wins) > 0 else 0
            total_loss = abs(losses['pnl'].sum()) if len(losses) > 0 else 0
            
            profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')
            
            # Calculate drawdown
            cumulative = subset['pnl'].cumsum()
            rolling_max = cumulative.expanding().max()
            drawdown = cumulative - rolling_max
            max_drawdown = drawdown.min()
            
            return {
                'trades': len(subset),
                'wins': len(wins),
                'losses': len(losses),
                'win_rate': round(win_rate, 2),
                'avg_win': round(avg_win, 2),
                'avg_loss': round(avg_loss, 2),
                'risk_reward_ratio': round(rr_ratio, 2) if rr_ratio != float('inf') else None,
                'profit_factor': round(profit_factor, 2) if profit_factor != float('inf') else None,
                'total_pnl': round(subset['pnl'].sum(), 2),
                'max_drawdown': round(max_drawdown, 2)
            }
        
        # Overall statistics
        stats['overall'] = calc_metrics(df)
        
        # By SL type
        for sl_type in df['sl_type'].unique():
            subset = df[df['sl_type'] == sl_type]
            stats['by_sl_type'][sl_type] = calc_metrics(subset)
        
        # By direction
        for direction in df['direction'].unique():
            subset = df[df['direction'] == direction]
            stats['by_direction'][direction] = calc_metrics(subset)
        
        # By session
        for session in df['session'].unique():
            subset = df[df['session'] == session]
            stats['by_session'][session] = calc_metrics(subset)
        
        # By year
        for year in sorted(df['year'].unique()):
            subset = df[df['year'] == year]
            stats['by_year'][str(year)] = calc_metrics(subset)
        
        return stats
    
    def generate_equity_curve(self, output_path: str):
        """Generate and save equity curve chart."""
        if not self.trades:
            print("No trades to plot.")
            return
        
        closed_trades = [t for t in self.trades if t.result in ['WIN', 'LOSS']]
        
        if not closed_trades:
            print("No closed trades to plot.")
            return
        
        # Sort by exit time
        sorted_trades = sorted(closed_trades, key=lambda t: t.exit_time)
        
        # Create separate equity curves for each SL type (sorted for consistent ordering)
        sl_types = sorted(set(t.sl_type for t in sorted_trades))[:self.MAX_SL_TYPES_TO_PLOT]
        num_plots = len(sl_types) + 1  # +1 for overall curve
        max_height = min(4 * num_plots, self.MAX_PLOT_HEIGHT_INCHES)
        
        fig, axes = plt.subplots(num_plots, 1, figsize=(14, max_height))
        
        if num_plots == 1:
            axes = [axes]
        
        # Overall equity curve
        all_pnls = [t.pnl for t in sorted_trades]
        cumulative = np.cumsum(all_pnls)
        axes[0].plot(cumulative, label='Overall', color='blue')
        axes[0].set_title('Overall Equity Curve')
        axes[0].set_xlabel('Trade Number')
        axes[0].set_ylabel('Cumulative P&L (Points)')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        
        # Equity curves by SL type
        colors = ['green', 'orange', 'red']
        for i, sl_type in enumerate(sorted(sl_types)):
            sl_trades = [t for t in sorted_trades if t.sl_type == sl_type]
            pnls = [t.pnl for t in sl_trades]
            cumulative = np.cumsum(pnls)
            
            ax_idx = i + 1  # Overall curve is at index 0, SL types start at 1
            if ax_idx < len(axes):
                axes[ax_idx].plot(cumulative, label=sl_type, color=colors[i % len(colors)])
                axes[ax_idx].set_title(f'Equity Curve - {sl_type}')
                axes[ax_idx].set_xlabel('Trade Number')
                axes[ax_idx].set_ylabel('Cumulative P&L (Points)')
                axes[ax_idx].grid(True, alpha=0.3)
                axes[ax_idx].legend()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()
        print(f"Equity curve saved to {output_path}")
    
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
            'PnL': t.pnl,
            'Result': t.result,
            'Session': t.session,
            'Year': t.year
        } for t in self.trades])
        
        df.to_csv(output_path, index=False)
        print(f"Trade log saved to {output_path}")
    
    @staticmethod
    def _format_stat(value) -> str:
        """Format statistic value for report, handling None values."""
        return 'N/A' if value is None else str(value)
    
    def generate_report(self, output_path: str, stats: dict):
        """Generate detailed markdown report."""
        report = []
        report.append("# NQ Futures Breakout Backtest Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"\n**Data Period:** {self.config['data']['start_year']} - {self.config['data']['end_year']}")
        report.append(f"\n**Total Data Points:** {len(self.data):,}")
        
        report.append("\n\n## Strategy Overview")
        report.append("\nThis backtest evaluates a breakout trading strategy based on:")
        report.append("- Oblique trendline breakouts (resistance for LONG, support for SHORT)")
        report.append("- Momentum confirmation (candle body > average)")
        report.append("- Multiple stop-loss scenarios (50%, 75%, 100% retracement)")
        report.append(f"- Trading sessions: 02:00-05:00 and 08:30-11:00")
        
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
            report.append(f"| Risk/Reward Ratio | {self._format_stat(o['risk_reward_ratio'])} |")
            report.append(f"| Profit Factor | {self._format_stat(o['profit_factor'])} |")
            report.append(f"| Total P&L | {o['total_pnl']} pts |")
            report.append(f"| Maximum Drawdown | {o['max_drawdown']} pts |")
        
        report.append("\n\n## Performance by Stop Loss Type")
        if 'by_sl_type' in stats:
            report.append(f"\n| SL Type | Trades | Win Rate | Avg R:R | Profit Factor | Total P&L | Max DD |")
            report.append(f"|---------|--------|----------|---------|---------------|-----------|--------|")
            for sl_type, m in sorted(stats['by_sl_type'].items()):
                if m:
                    report.append(f"| {sl_type} | {m['trades']} | {m['win_rate']}% | {self._format_stat(m['risk_reward_ratio'])} | {self._format_stat(m['profit_factor'])} | {m['total_pnl']} | {m['max_drawdown']} |")
        
        report.append("\n\n## Performance by Direction")
        if 'by_direction' in stats:
            report.append(f"\n| Direction | Trades | Wins | Losses | Win Rate | Profit Factor | Total P&L |")
            report.append(f"|-----------|--------|------|--------|----------|---------------|-----------|")
            for direction, m in stats['by_direction'].items():
                if m:
                    report.append(f"| {direction} | {m['trades']} | {m['wins']} | {m['losses']} | {m['win_rate']}% | {self._format_stat(m['profit_factor'])} | {m['total_pnl']} |")
        
        report.append("\n\n## Performance by Trading Session")
        if 'by_session' in stats:
            report.append(f"\n| Session | Trades | Win Rate | Profit Factor | Total P&L | Max DD |")
            report.append(f"|---------|--------|----------|---------------|-----------|--------|")
            for session, m in stats['by_session'].items():
                if m:
                    report.append(f"| {session} | {m['trades']} | {m['win_rate']}% | {self._format_stat(m['profit_factor'])} | {m['total_pnl']} | {m['max_drawdown']} |")
        
        report.append("\n\n## Performance by Year")
        if 'by_year' in stats:
            report.append(f"\n| Year | Trades | Wins | Losses | Win Rate | Profit Factor | Total P&L |")
            report.append(f"|------|--------|------|--------|----------|---------------|-----------|")
            for year, m in sorted(stats['by_year'].items()):
                if m:
                    report.append(f"| {year} | {m['trades']} | {m['wins']} | {m['losses']} | {m['win_rate']}% | {self._format_stat(m['profit_factor'])} | {m['total_pnl']} |")
        
        report.append("\n\n## Configuration Used")
        report.append(f"\n```yaml")
        report.append(f"Swing Detection Lookback: {self.config['swing_detection']['lookback_period']} bars")
        report.append(f"Momentum Average Period: {self.config['momentum']['average_period']} periods")
        report.append(f"Stop Loss Levels: {self.config['stop_loss_levels']}")
        report.append(f"Trading Session 1: 02:00-05:00")
        report.append(f"Trading Session 2: 08:30-11:00")
        report.append(f"```")
        
        report.append("\n\n## Equity Curve")
        report.append("\n![Equity Curve](equity_curve.png)")
        
        report.append("\n\n## Trade Log")
        report.append("\nSee `trades_log.csv` for detailed trade-by-trade breakdown.")
        
        report.append("\n\n---")
        report.append("\n*Report generated by NQ Futures Breakout Backtester*")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"Report saved to {output_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='NQ Futures Breakout Backtester')
    parser.add_argument('--config', default='config.yaml', help='Path to configuration file')
    args = parser.parse_args()
    
    # Initialize backtester
    print("=" * 60)
    print("NQ Futures Breakout Backtester")
    print("=" * 60)
    
    backtester = NQBacktester(config_path=args.config)
    
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
    trades_log_path = os.path.join(results_dir, backtester.config['output']['trades_log_file'])
    report_path = os.path.join(results_dir, backtester.config['output']['report_file'])
    equity_curve_path = os.path.join(results_dir, backtester.config['output']['equity_curve_file'])
    
    backtester.save_trades_log(trades_log_path)
    backtester.generate_equity_curve(equity_curve_path)
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
    
    print(f"\nResults saved to: {results_dir}/")
    print("  - backtest_report.md")
    print("  - trades_log.csv")
    print("  - equity_curve.png")


if __name__ == '__main__':
    main()
