#!/usr/bin/env python3
"""
NQ IVFG Strategy Backtester

This script implements the NQ IVFG (Inverted Fair Value Gap) strategy
from the Pine Script and backtests it on historical 5-minute and 4-hour data.

Strategy Logic:
1. Time Filter: Trade only during 01:00-05:00 (London Killzone)
2. Trend Filter: EMA 20 from 4H timeframe
3. FVG Detection: Fair Value Gaps on 5m chart
4. IVFG Signal: Price crosses inverted FVG within 12-bar memory
5. Risk Management: 3 modes (Structural, Fixed Points, ATR-based)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import glob
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Configuration parameters for the backtest"""
    
    # Capital & Costs
    INITIAL_CAPITAL = 100_000
    COMMISSION_PER_TRADE = 2.50
    TICK_SIZE = 0.25  # NQ tick size
    SLIPPAGE_TICKS = 2
    SLIPPAGE = SLIPPAGE_TICKS * TICK_SIZE
    
    # Time Filter (London Killzone)
    ENABLE_TIME_FILTER = True
    SESSION_START_HOUR = 1
    SESSION_END_HOUR = 5
    
    # Trend Filter
    EMA_LENGTH = 20
    
    # IVFG Settings
    FVG_LOOKBACK = 12  # 12-bar memory for FVG
    FVG_THRESHOLD = 0.0  # Minimum FVG size in points
    
    # Risk Management - Mode A (Structural)
    SL_BUFFER_TICKS = 5
    RR_RATIO = 2.0
    
    # Risk Management - Mode B (Fixed Points)
    SL_POINTS_FIXED = 20
    TP_POINTS_FIXED = 40
    
    # Risk Management - Mode C (ATR Based)
    ATR_LENGTH = 14
    SL_ATR_MULT = 1.5
    TP_ATR_MULT = 3.0
    
    # File paths
    DATA_DIR = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    RESULTS_DIR = "/home/runner/work/Backtest-Trading/Backtest-Trading/results"


# ============================================================================
# DATA LOADING
# ============================================================================

def load_csv_files(timeframe: str, years: List[int]) -> pd.DataFrame:
    """
    Load and concatenate CSV files for multiple years.
    
    Args:
        timeframe: '5m' or '4H'
        years: List of years to load
        
    Returns:
        Combined DataFrame with datetime index
    """
    dfs = []
    
    for year in years:
        filename = f"{year} {timeframe}.csv"
        filepath = os.path.join(Config.DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: {filename} not found")
            continue
            
        try:
            # Read CSV with semicolon delimiter, skip header
            df = pd.read_csv(filepath, sep=';', skiprows=1, 
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            
            # Combine Date and Time into datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S')
            
            # Set datetime as index and select OHLCV columns
            df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
            df = df.set_index('DateTime')
            
            # Convert to numeric
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Remove any rows with NaN values
            df = df.dropna()
            
            dfs.append(df)
            print(f"Loaded {filename}: {len(df)} rows")
            
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
            continue
    
    if not dfs:
        raise ValueError(f"No data loaded for {timeframe}")
    
    # Concatenate all dataframes
    combined = pd.concat(dfs, axis=0)
    combined = combined.sort_index()
    
    # Remove duplicates
    combined = combined[~combined.index.duplicated(keep='first')]
    
    print(f"\nTotal {timeframe} data: {len(combined)} rows")
    print(f"Date range: {combined.index[0]} to {combined.index[-1]}")
    
    return combined


def merge_timeframes(df_5m: pd.DataFrame, df_4h: pd.DataFrame) -> pd.DataFrame:
    """
    Merge 5-minute data with 4-hour EMA values.
    
    Args:
        df_5m: 5-minute OHLCV data
        df_4h: 4-hour OHLCV data
        
    Returns:
        5-minute DataFrame with 4H EMA column
    """
    # Calculate EMA on 4H data
    df_4h['EMA_20'] = df_4h['Close'].ewm(span=Config.EMA_LENGTH, adjust=False).mean()
    
    # Forward fill 4H EMA to 5m timeframe
    df_merged = df_5m.copy()
    df_merged['EMA_4H'] = df_4h['EMA_20'].reindex(df_merged.index, method='ffill')
    
    return df_merged


# ============================================================================
# INDICATOR CALCULATIONS
# ============================================================================

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Average True Range"""
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr


def detect_fvg(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect Fair Value Gaps (FVG) on the dataframe.
    
    Bullish FVG: low[2] > high[0] (gap up)
    Bearish FVG: high[2] < low[0] (gap down)
    
    Returns:
        bullish_fvgs: DataFrame with bullish FVG info
        bearish_fvgs: DataFrame with bearish FVG info
    """
    bullish_fvgs = []
    bearish_fvgs = []
    
    for i in range(2, len(df)):
        # Bullish FVG: gap between bar[i-2].low and bar[i].high
        if df['Low'].iloc[i-2] > df['High'].iloc[i]:
            gap_size = df['Low'].iloc[i-2] - df['High'].iloc[i]
            if gap_size >= Config.FVG_THRESHOLD:
                bullish_fvgs.append({
                    'bar_index': i,
                    'datetime': df.index[i],
                    'top': df['Low'].iloc[i-2],
                    'bottom': df['High'].iloc[i],
                    'size': gap_size
                })
        
        # Bearish FVG: gap between bar[i-2].high and bar[i].low
        if df['High'].iloc[i-2] < df['Low'].iloc[i]:
            gap_size = df['Low'].iloc[i] - df['High'].iloc[i-2]
            if gap_size >= Config.FVG_THRESHOLD:
                bearish_fvgs.append({
                    'bar_index': i,
                    'datetime': df.index[i],
                    'top': df['Low'].iloc[i],
                    'bottom': df['High'].iloc[i-2],
                    'size': gap_size
                })
    
    return pd.DataFrame(bullish_fvgs), pd.DataFrame(bearish_fvgs)


# ============================================================================
# STRATEGY LOGIC
# ============================================================================

class IVFGStrategy:
    """NQ IVFG Strategy Implementation"""
    
    def __init__(self, df: pd.DataFrame, risk_mode: str):
        """
        Initialize strategy
        
        Args:
            df: DataFrame with OHLCV and EMA_4H
            risk_mode: 'Mode A', 'Mode B', or 'Mode C'
        """
        self.df = df.copy()
        self.risk_mode = risk_mode
        self.trades = []
        self.equity_curve = []
        self.capital = Config.INITIAL_CAPITAL
        self.current_position = None
        
        # Calculate ATR for Mode C
        if risk_mode == 'Mode C':
            self.df['ATR'] = calculate_atr(self.df, Config.ATR_LENGTH)
        
        # Detect all FVGs
        print(f"Detecting FVGs...")
        self.bullish_fvgs, self.bearish_fvgs = detect_fvg(self.df)
        print(f"Found {len(self.bullish_fvgs)} bullish FVGs and {len(self.bearish_fvgs)} bearish FVGs")
    
    def is_in_session(self, dt: datetime) -> bool:
        """Check if datetime is within trading session"""
        if not Config.ENABLE_TIME_FILTER:
            return True
        
        hour = dt.hour
        if Config.SESSION_START_HOUR < Config.SESSION_END_HOUR:
            return Config.SESSION_START_HOUR <= hour < Config.SESSION_END_HOUR
        else:
            return hour >= Config.SESSION_START_HOUR or hour < Config.SESSION_END_HOUR
    
    def get_trend(self, i: int) -> str:
        """
        Get trend based on price vs 4H EMA
        
        Returns: 'bullish', 'bearish', or 'neutral'
        """
        close = self.df['Close'].iloc[i]
        ema = self.df['EMA_4H'].iloc[i]
        
        if pd.isna(ema):
            return 'neutral'
        
        if close > ema:
            return 'bullish'
        elif close < ema:
            return 'bearish'
        else:
            return 'neutral'
    
    def check_ivfg_signal(self, i: int, trend: str) -> Tuple[bool, str, float]:
        """
        Check for IVFG signal with 12-bar memory
        
        Returns:
            (has_signal, signal_type, fvg_level)
        """
        current_bar = i
        current_close = self.df['Close'].iloc[i]
        prev_close = self.df['Close'].iloc[i-1]
        
        # Long Signal: Bullish trend + close crosses above bearish FVG top
        if trend == 'bullish':
            # Look for bearish FVGs within last 12 bars
            recent_bear_fvgs = self.bearish_fvgs[
                (self.bearish_fvgs['bar_index'] <= current_bar) &
                (self.bearish_fvgs['bar_index'] > current_bar - Config.FVG_LOOKBACK)
            ]
            
            for _, fvg in recent_bear_fvgs.iterrows():
                fvg_top = fvg['top']
                # Check if close crosses above FVG top
                if current_close > fvg_top and prev_close <= fvg_top:
                    return True, 'long', fvg_top
        
        # Short Signal: Bearish trend + close crosses below bullish FVG bottom
        elif trend == 'bearish':
            # Look for bullish FVGs within last 12 bars
            recent_bull_fvgs = self.bullish_fvgs[
                (self.bullish_fvgs['bar_index'] <= current_bar) &
                (self.bullish_fvgs['bar_index'] > current_bar - Config.FVG_LOOKBACK)
            ]
            
            for _, fvg in recent_bull_fvgs.iterrows():
                fvg_bottom = fvg['bottom']
                # Check if close crosses below FVG bottom
                if current_close < fvg_bottom and prev_close >= fvg_bottom:
                    return True, 'short', fvg_bottom
        
        return False, None, None
    
    def calculate_sl_tp(self, i: int, signal_type: str) -> Tuple[float, float]:
        """
        Calculate Stop Loss and Take Profit based on risk mode
        
        Returns:
            (stop_loss, take_profit)
        """
        close = self.df['Close'].iloc[i]
        high = self.df['High'].iloc[i]
        low = self.df['Low'].iloc[i]
        
        if self.risk_mode == 'Mode A':
            # Structural: Based on signal candle structure
            if signal_type == 'long':
                sl = low - (Config.SL_BUFFER_TICKS * Config.TICK_SIZE)
                risk = close - sl
                tp = close + (risk * Config.RR_RATIO)
            else:  # short
                sl = high + (Config.SL_BUFFER_TICKS * Config.TICK_SIZE)
                risk = sl - close
                tp = close - (risk * Config.RR_RATIO)
        
        elif self.risk_mode == 'Mode B':
            # Fixed Points
            if signal_type == 'long':
                sl = close - Config.SL_POINTS_FIXED
                tp = close + Config.TP_POINTS_FIXED
            else:  # short
                sl = close + Config.SL_POINTS_FIXED
                tp = close - Config.TP_POINTS_FIXED
        
        elif self.risk_mode == 'Mode C':
            # ATR Based
            atr = self.df['ATR'].iloc[i]
            if pd.isna(atr):
                atr = 20  # Default fallback
            
            if signal_type == 'long':
                sl = close - (atr * Config.SL_ATR_MULT)
                tp = close + (atr * Config.TP_ATR_MULT)
            else:  # short
                sl = close + (atr * Config.SL_ATR_MULT)
                tp = close - (atr * Config.TP_ATR_MULT)
        
        return sl, tp
    
    def open_position(self, i: int, signal_type: str, entry_price: float, 
                     stop_loss: float, take_profit: float):
        """Open a new position"""
        self.current_position = {
            'type': signal_type,
            'entry_bar': i,
            'entry_datetime': self.df.index[i],
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'capital_at_entry': self.capital
        }
    
    def close_position(self, i: int, exit_price: float, exit_reason: str):
        """Close current position and record trade"""
        if self.current_position is None:
            return
        
        pos = self.current_position
        
        # Calculate P&L
        if pos['type'] == 'long':
            raw_pnl = exit_price - pos['entry_price']
        else:  # short
            raw_pnl = pos['entry_price'] - exit_price
        
        # Apply slippage and commission
        pnl = raw_pnl - Config.SLIPPAGE - (2 * Config.COMMISSION_PER_TRADE)
        
        # Update capital
        self.capital += pnl
        
        # Record trade
        trade = {
            'entry_datetime': pos['entry_datetime'],
            'exit_datetime': self.df.index[i],
            'type': pos['type'],
            'entry_price': pos['entry_price'],
            'exit_price': exit_price,
            'stop_loss': pos['stop_loss'],
            'take_profit': pos['take_profit'],
            'pnl': pnl,
            'exit_reason': exit_reason,
            'bars_held': i - pos['entry_bar']
        }
        
        self.trades.append(trade)
        self.current_position = None
    
    def check_exit_conditions(self, i: int) -> Tuple[bool, float, str]:
        """
        Check if current position should be exited
        
        Returns:
            (should_exit, exit_price, exit_reason)
        """
        if self.current_position is None:
            return False, None, None
        
        high = self.df['High'].iloc[i]
        low = self.df['Low'].iloc[i]
        close = self.df['Close'].iloc[i]
        pos = self.current_position
        
        if pos['type'] == 'long':
            # Check stop loss
            if low <= pos['stop_loss']:
                return True, pos['stop_loss'], 'stop_loss'
            # Check take profit
            if high >= pos['take_profit']:
                return True, pos['take_profit'], 'take_profit'
        
        else:  # short
            # Check stop loss
            if high >= pos['stop_loss']:
                return True, pos['stop_loss'], 'stop_loss'
            # Check take profit
            if low <= pos['take_profit']:
                return True, pos['take_profit'], 'take_profit'
        
        return False, None, None
    
    def run_backtest(self):
        """Run the backtest on the data"""
        print(f"\nRunning backtest with {self.risk_mode}...")
        print(f"Total bars: {len(self.df)}")
        
        # Need at least 3 bars for FVG detection + EMA warmup
        start_index = max(3, Config.EMA_LENGTH + 1)
        
        for i in range(start_index, len(self.df)):
            # Track equity
            self.equity_curve.append({
                'datetime': self.df.index[i],
                'equity': self.capital
            })
            
            # Check exit conditions first
            if self.current_position is not None:
                should_exit, exit_price, exit_reason = self.check_exit_conditions(i)
                if should_exit:
                    self.close_position(i, exit_price, exit_reason)
            
            # Only look for new entries if no position
            if self.current_position is None:
                # Check time filter
                if not self.is_in_session(self.df.index[i]):
                    continue
                
                # Check trend
                trend = self.get_trend(i)
                if trend == 'neutral':
                    continue
                
                # Need at least 1 previous bar for crossover detection
                if i < 1:
                    continue
                
                # Check for IVFG signal
                has_signal, signal_type, fvg_level = self.check_ivfg_signal(i, trend)
                
                if has_signal:
                    # Calculate entry price (close of signal bar + slippage)
                    entry_price = self.df['Close'].iloc[i]
                    if signal_type == 'long':
                        entry_price += Config.SLIPPAGE
                    else:
                        entry_price -= Config.SLIPPAGE
                    
                    # Calculate SL and TP
                    stop_loss, take_profit = self.calculate_sl_tp(i, signal_type)
                    
                    # Open position
                    self.open_position(i, signal_type, entry_price, stop_loss, take_profit)
        
        # Close any open position at the end
        if self.current_position is not None:
            final_price = self.df['Close'].iloc[-1]
            self.close_position(len(self.df)-1, final_price, 'end_of_data')
        
        print(f"Backtest complete. Total trades: {len(self.trades)}")
        
        return self.trades, self.equity_curve


# ============================================================================
# PERFORMANCE ANALYSIS
# ============================================================================

def calculate_metrics(trades: List[Dict], equity_curve: List[Dict], 
                     initial_capital: float) -> Dict:
    """Calculate performance metrics"""
    
    if not trades:
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0,
            'total_pnl': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'profit_factor': 0,
            'max_drawdown': 0,
            'max_drawdown_pct': 0,
            'sharpe_ratio': 0,
            'final_capital': initial_capital,
            'total_return_pct': 0
        }
    
    trades_df = pd.DataFrame(trades)
    equity_df = pd.DataFrame(equity_curve)
    
    # Basic stats
    total_trades = len(trades_df)
    winning_trades = len(trades_df[trades_df['pnl'] > 0])
    losing_trades = len(trades_df[trades_df['pnl'] < 0])
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    # P&L stats
    total_pnl = trades_df['pnl'].sum()
    wins = trades_df[trades_df['pnl'] > 0]['pnl']
    losses = trades_df[trades_df['pnl'] < 0]['pnl']
    
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0
    
    total_wins = wins.sum() if len(wins) > 0 else 0
    total_losses = abs(losses.sum()) if len(losses) > 0 else 0
    profit_factor = (total_wins / total_losses) if total_losses > 0 else 0
    
    # Drawdown
    equity_df['peak'] = equity_df['equity'].cummax()
    equity_df['drawdown'] = equity_df['equity'] - equity_df['peak']
    max_drawdown = equity_df['drawdown'].min()
    max_dd_pct = (max_drawdown / equity_df['peak'].max() * 100) if equity_df['peak'].max() > 0 else 0
    
    # Returns
    final_capital = equity_df['equity'].iloc[-1]
    total_return_pct = ((final_capital - initial_capital) / initial_capital * 100)
    
    # Sharpe Ratio (annualized)
    trades_df['return'] = trades_df['pnl'] / initial_capital
    if len(trades_df['return']) > 1:
        sharpe_ratio = (trades_df['return'].mean() / trades_df['return'].std()) * np.sqrt(252) if trades_df['return'].std() > 0 else 0
    else:
        sharpe_ratio = 0
    
    return {
        'total_trades': total_trades,
        'winning_trades': winning_trades,
        'losing_trades': losing_trades,
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'profit_factor': profit_factor,
        'max_drawdown': max_drawdown,
        'max_drawdown_pct': max_dd_pct,
        'sharpe_ratio': sharpe_ratio,
        'final_capital': final_capital,
        'total_return_pct': total_return_pct
    }


def analyze_trade_distribution(trades: List[Dict]) -> pd.DataFrame:
    """Analyze trade distribution by hour, day of week, month"""
    if not trades:
        return pd.DataFrame()
    
    trades_df = pd.DataFrame(trades)
    trades_df['entry_hour'] = trades_df['entry_datetime'].dt.hour
    trades_df['entry_dow'] = trades_df['entry_datetime'].dt.dayofweek
    trades_df['entry_month'] = trades_df['entry_datetime'].dt.month
    trades_df['entry_year'] = trades_df['entry_datetime'].dt.year
    
    return trades_df


def analyze_monthly_performance(trades: List[Dict]) -> pd.DataFrame:
    """Calculate monthly performance breakdown"""
    if not trades:
        return pd.DataFrame()
    
    trades_df = pd.DataFrame(trades)
    trades_df['year_month'] = trades_df['entry_datetime'].dt.to_period('M')
    
    monthly = trades_df.groupby('year_month').agg({
        'pnl': ['sum', 'count', 'mean'],
    }).round(2)
    
    monthly.columns = ['Total PnL', 'Trades', 'Avg PnL']
    monthly['Win Rate %'] = trades_df.groupby('year_month').apply(
        lambda x: (len(x[x['pnl'] > 0]) / len(x) * 100) if len(x) > 0 else 0
    ).round(2)
    
    return monthly


def analyze_yearly_performance(trades: List[Dict]) -> pd.DataFrame:
    """Calculate yearly performance breakdown"""
    if not trades:
        return pd.DataFrame()
    
    trades_df = pd.DataFrame(trades)
    trades_df['year'] = trades_df['entry_datetime'].dt.year
    
    yearly = trades_df.groupby('year').agg({
        'pnl': ['sum', 'count', 'mean'],
    }).round(2)
    
    yearly.columns = ['Total PnL', 'Trades', 'Avg PnL']
    yearly['Win Rate %'] = trades_df.groupby('year').apply(
        lambda x: (len(x[x['pnl'] > 0]) / len(x) * 100) if len(x) > 0 else 0
    ).round(2)
    
    return yearly


# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_equity_curve(equity_curve: List[Dict], risk_mode: str, output_path: str):
    """Plot equity curve"""
    if not equity_curve:
        print("No equity data to plot")
        return
    
    equity_df = pd.DataFrame(equity_curve)
    
    plt.figure(figsize=(14, 7))
    plt.plot(equity_df['datetime'], equity_df['equity'], linewidth=2)
    plt.title(f'Equity Curve - {risk_mode}', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Equity ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.xticks(rotation=45)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved equity curve: {output_path}")


def plot_drawdown(equity_curve: List[Dict], risk_mode: str, output_path: str):
    """Plot drawdown chart"""
    if not equity_curve:
        print("No equity data to plot")
        return
    
    equity_df = pd.DataFrame(equity_curve)
    equity_df['peak'] = equity_df['equity'].cummax()
    equity_df['drawdown'] = equity_df['equity'] - equity_df['peak']
    equity_df['drawdown_pct'] = (equity_df['drawdown'] / equity_df['peak'] * 100)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Dollar drawdown
    ax1.fill_between(equity_df['datetime'], equity_df['drawdown'], 0, 
                     alpha=0.3, color='red')
    ax1.plot(equity_df['datetime'], equity_df['drawdown'], color='red', linewidth=1)
    ax1.set_title(f'Drawdown ($) - {risk_mode}', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Drawdown ($)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    
    # Percentage drawdown
    ax2.fill_between(equity_df['datetime'], equity_df['drawdown_pct'], 0, 
                     alpha=0.3, color='red')
    ax2.plot(equity_df['datetime'], equity_df['drawdown_pct'], color='red', linewidth=1)
    ax2.set_title(f'Drawdown (%) - {risk_mode}', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Drawdown (%)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved drawdown chart: {output_path}")


def plot_trade_distribution(trades: List[Dict], risk_mode: str, output_path: str):
    """Plot trade distribution analysis"""
    if not trades:
        print("No trades to plot")
        return
    
    trades_df = analyze_trade_distribution(trades)
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle(f'Trade Distribution Analysis - {risk_mode}', fontsize=16, fontweight='bold')
    
    # 1. P&L Distribution
    ax = axes[0, 0]
    ax.hist(trades_df['pnl'], bins=50, edgecolor='black', alpha=0.7)
    ax.axvline(0, color='red', linestyle='--', linewidth=2)
    ax.set_title('P&L Distribution')
    ax.set_xlabel('P&L ($)')
    ax.set_ylabel('Frequency')
    ax.grid(True, alpha=0.3)
    
    # 2. Trades by Hour
    ax = axes[0, 1]
    hour_counts = trades_df['entry_hour'].value_counts().sort_index()
    ax.bar(hour_counts.index, hour_counts.values, edgecolor='black', alpha=0.7)
    ax.set_title('Trades by Hour')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Number of Trades')
    ax.grid(True, alpha=0.3)
    
    # 3. Trades by Day of Week
    ax = axes[0, 2]
    dow_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    dow_counts = trades_df['entry_dow'].value_counts().sort_index()
    ax.bar([dow_names[i] for i in dow_counts.index], dow_counts.values, 
           edgecolor='black', alpha=0.7)
    ax.set_title('Trades by Day of Week')
    ax.set_xlabel('Day')
    ax.set_ylabel('Number of Trades')
    ax.grid(True, alpha=0.3)
    
    # 4. Win/Loss by Trade Type
    ax = axes[1, 0]
    long_trades = trades_df[trades_df['type'] == 'long']
    short_trades = trades_df[trades_df['type'] == 'short']
    
    long_wins = len(long_trades[long_trades['pnl'] > 0])
    long_losses = len(long_trades[long_trades['pnl'] <= 0])
    short_wins = len(short_trades[short_trades['pnl'] > 0])
    short_losses = len(short_trades[short_trades['pnl'] <= 0])
    
    x = np.arange(2)
    width = 0.35
    ax.bar(x - width/2, [long_wins, short_wins], width, label='Wins', 
           color='green', alpha=0.7)
    ax.bar(x + width/2, [long_losses, short_losses], width, label='Losses', 
           color='red', alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(['Long', 'Short'])
    ax.set_title('Win/Loss by Trade Type')
    ax.set_ylabel('Number of Trades')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 5. Cumulative P&L
    ax = axes[1, 1]
    trades_df_sorted = trades_df.sort_values('entry_datetime')
    cumulative_pnl = trades_df_sorted['pnl'].cumsum()
    ax.plot(range(len(cumulative_pnl)), cumulative_pnl, linewidth=2)
    ax.axhline(0, color='red', linestyle='--', linewidth=1)
    ax.set_title('Cumulative P&L')
    ax.set_xlabel('Trade Number')
    ax.set_ylabel('Cumulative P&L ($)')
    ax.grid(True, alpha=0.3)
    
    # 6. Trade Duration
    ax = axes[1, 2]
    ax.hist(trades_df['bars_held'], bins=30, edgecolor='black', alpha=0.7)
    ax.set_title('Trade Duration (bars)')
    ax.set_xlabel('Bars Held')
    ax.set_ylabel('Frequency')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved trade distribution: {output_path}")


def plot_monthly_returns(trades: List[Dict], risk_mode: str, output_path: str):
    """Plot monthly returns heatmap"""
    if not trades:
        print("No trades to plot")
        return
    
    trades_df = pd.DataFrame(trades)
    trades_df['year'] = trades_df['entry_datetime'].dt.year
    trades_df['month'] = trades_df['entry_datetime'].dt.month
    
    # Create pivot table
    monthly_pnl = trades_df.groupby(['year', 'month'])['pnl'].sum().reset_index()
    pivot = monthly_pnl.pivot(index='year', columns='month', values='pnl')
    
    plt.figure(figsize=(14, 8))
    
    # Create heatmap
    im = plt.imshow(pivot, cmap='RdYlGn', aspect='auto', interpolation='nearest')
    
    # Set ticks
    plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.yticks(range(len(pivot.index)), pivot.index)
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('P&L ($)', rotation=270, labelpad=20)
    
    # Add values to cells
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            value = pivot.iloc[i, j]
            if not pd.isna(value):
                text_color = 'white' if abs(value) > pivot.abs().max().max() * 0.5 else 'black'
                plt.text(j, i, f'${value:.0f}', ha='center', va='center', 
                        color=text_color, fontsize=8)
    
    plt.title(f'Monthly Returns Heatmap - {risk_mode}', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Year', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved monthly returns: {output_path}")


# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_report(results: Dict[str, Dict], output_path: str):
    """Generate comprehensive text report"""
    
    with open(output_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("NQ IVFG STRATEGY BACKTEST REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Backtest Period: 2018-2025\n")
        f.write(f"Initial Capital: ${Config.INITIAL_CAPITAL:,.2f}\n")
        f.write(f"Commission: ${Config.COMMISSION_PER_TRADE} per trade\n")
        f.write(f"Slippage: {Config.SLIPPAGE_TICKS} ticks (${Config.SLIPPAGE})\n\n")
        
        f.write("Strategy Parameters:\n")
        f.write(f"  - Time Filter: {Config.SESSION_START_HOUR}:00 - {Config.SESSION_END_HOUR}:00\n")
        f.write(f"  - EMA Length: {Config.EMA_LENGTH} (4H)\n")
        f.write(f"  - FVG Lookback: {Config.FVG_LOOKBACK} bars\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("RESULTS BY RISK MANAGEMENT MODE\n")
        f.write("=" * 80 + "\n\n")
        
        for mode, data in results.items():
            metrics = data['metrics']
            
            f.write("-" * 80 + "\n")
            f.write(f"{mode}\n")
            f.write("-" * 80 + "\n\n")
            
            f.write("Performance Metrics:\n")
            f.write(f"  Total Trades:        {metrics['total_trades']}\n")
            f.write(f"  Winning Trades:      {metrics['winning_trades']}\n")
            f.write(f"  Losing Trades:       {metrics['losing_trades']}\n")
            f.write(f"  Win Rate:            {metrics['win_rate']:.2f}%\n")
            f.write(f"  Profit Factor:       {metrics['profit_factor']:.2f}\n\n")
            
            f.write("Returns:\n")
            f.write(f"  Total P&L:           ${metrics['total_pnl']:,.2f}\n")
            f.write(f"  Total Return:        {metrics['total_return_pct']:.2f}%\n")
            f.write(f"  Average Win:         ${metrics['avg_win']:.2f}\n")
            f.write(f"  Average Loss:        ${metrics['avg_loss']:.2f}\n")
            f.write(f"  Final Capital:       ${metrics['final_capital']:,.2f}\n\n")
            
            f.write("Risk Metrics:\n")
            f.write(f"  Max Drawdown:        ${metrics['max_drawdown']:,.2f}\n")
            f.write(f"  Max Drawdown %:      {metrics['max_drawdown_pct']:.2f}%\n")
            f.write(f"  Sharpe Ratio:        {metrics['sharpe_ratio']:.2f}\n\n")
            
            # Yearly breakdown
            if not data['yearly'].empty:
                f.write("Yearly Performance:\n")
                f.write(data['yearly'].to_string())
                f.write("\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
    
    print(f"Saved report: {output_path}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    print("=" * 80)
    print("NQ IVFG STRATEGY BACKTESTER")
    print("=" * 80)
    print()
    
    # Create results directory
    os.makedirs(Config.RESULTS_DIR, exist_ok=True)
    
    # Load data
    print("Loading historical data...")
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    
    try:
        df_5m = load_csv_files('5m', years)
        df_4h = load_csv_files('4H', years)
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return
    
    # Merge timeframes
    print("\nMerging timeframes...")
    df = merge_timeframes(df_5m, df_4h)
    print(f"Merged data shape: {df.shape}")
    
    # Run backtests for all risk modes
    risk_modes = ['Mode A', 'Mode B', 'Mode C']
    results = {}
    
    for mode in risk_modes:
        print(f"\n{'=' * 80}")
        print(f"BACKTESTING: {mode}")
        print(f"{'=' * 80}")
        
        # Initialize strategy
        strategy = IVFGStrategy(df, mode)
        
        # Run backtest
        trades, equity_curve = strategy.run_backtest()
        
        # Calculate metrics
        metrics = calculate_metrics(trades, equity_curve, Config.INITIAL_CAPITAL)
        
        # Analyze performance
        monthly = analyze_monthly_performance(trades)
        yearly = analyze_yearly_performance(trades)
        
        # Store results
        results[mode] = {
            'trades': trades,
            'equity_curve': equity_curve,
            'metrics': metrics,
            'monthly': monthly,
            'yearly': yearly
        }
        
        # Print summary
        print(f"\n{mode} Summary:")
        print(f"  Total Trades: {metrics['total_trades']}")
        print(f"  Win Rate: {metrics['win_rate']:.2f}%")
        print(f"  Profit Factor: {metrics['profit_factor']:.2f}")
        print(f"  Total Return: {metrics['total_return_pct']:.2f}%")
        print(f"  Max Drawdown: {metrics['max_drawdown_pct']:.2f}%")
        
        # Generate visualizations
        mode_safe = mode.replace(' ', '_').replace('-', '')
        
        plot_equity_curve(
            equity_curve, mode, 
            os.path.join(Config.RESULTS_DIR, f'equity_curve_{mode_safe}.png')
        )
        
        plot_drawdown(
            equity_curve, mode,
            os.path.join(Config.RESULTS_DIR, f'drawdown_{mode_safe}.png')
        )
        
        plot_trade_distribution(
            trades, mode,
            os.path.join(Config.RESULTS_DIR, f'trade_distribution_{mode_safe}.png')
        )
        
        plot_monthly_returns(
            trades, mode,
            os.path.join(Config.RESULTS_DIR, f'monthly_returns_{mode_safe}.png')
        )
        
        # Save trades to CSV
        if trades:
            trades_df = pd.DataFrame(trades)
            trades_df.to_csv(
                os.path.join(Config.RESULTS_DIR, f'trades_{mode_safe}.csv'),
                index=False
            )
            print(f"  Saved trades CSV")
    
    # Generate comprehensive report
    print(f"\n{'=' * 80}")
    print("GENERATING REPORT")
    print(f"{'=' * 80}")
    
    generate_report(
        results,
        os.path.join(Config.RESULTS_DIR, 'backtest_report.txt')
    )
    
    # Summary comparison
    print(f"\n{'=' * 80}")
    print("SUMMARY COMPARISON")
    print(f"{'=' * 80}\n")
    
    comparison = pd.DataFrame({
        mode: {
            'Total Trades': results[mode]['metrics']['total_trades'],
            'Win Rate %': f"{results[mode]['metrics']['win_rate']:.2f}",
            'Profit Factor': f"{results[mode]['metrics']['profit_factor']:.2f}",
            'Total Return %': f"{results[mode]['metrics']['total_return_pct']:.2f}",
            'Max DD %': f"{results[mode]['metrics']['max_drawdown_pct']:.2f}",
            'Sharpe Ratio': f"{results[mode]['metrics']['sharpe_ratio']:.2f}",
            'Final Capital': f"${results[mode]['metrics']['final_capital']:,.2f}"
        }
        for mode in risk_modes
    })
    
    print(comparison.T)
    
    comparison.T.to_csv(os.path.join(Config.RESULTS_DIR, 'comparison.csv'))
    
    print(f"\n{'=' * 80}")
    print(f"BACKTEST COMPLETE")
    print(f"{'=' * 80}")
    print(f"\nAll results saved to: {Config.RESULTS_DIR}")
    print("\nGenerated files:")
    print("  - backtest_report.txt (detailed text report)")
    print("  - comparison.csv (mode comparison)")
    print("  - trades_*.csv (trade logs for each mode)")
    print("  - equity_curve_*.png (equity curves)")
    print("  - drawdown_*.png (drawdown charts)")
    print("  - trade_distribution_*.png (distribution analysis)")
    print("  - monthly_returns_*.png (monthly heatmaps)")


if __name__ == '__main__':
    main()
