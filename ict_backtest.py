"""
ICT Trading Strategies Backtest System
=======================================
Expert Python script for Quantitative Trading with ICT Price Action strategies

Author: Expert Python Quantitative Trading Specialist
Date: 2025
"""

import pandas as pd
import numpy as np
import glob
from datetime import datetime, time
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# Strategy Selection: Choose 'A', 'B', or 'C'
STRATEGY = 'A'  # A: Judas Swing | B: Power of 3 | C: Displacement

# Risk Management Mode: Choose 1, 2, or 3
RISK_MODE = 1  # 1: Scalper Fixe | 2: Swing Session | 3: Volatilité Dynamique

# Data Configuration
DATA_TIMEFRAME = '5m'  # Options: '1m', '5m', '15m'
START_YEAR = 2018
END_YEAR = 2025

# Trading Window (NO TIMEZONE CONVERSION - Raw time)
TRADING_START = time(1, 0)   # 01:00
TRADING_END = time(5, 0)     # 05:00 (Hard exit)

# Risk Management Parameters
RISK_MODES = {
    1: {'name': 'Scalper Fixe', 'sl': 15, 'tp': 30},
    2: {'name': 'Swing Session', 'sl': 40, 'tp': 100},
    3: {'name': 'Volatilité Dynamique', 'sl_multiplier': 2, 'tp_multiplier': 4}
}

# Strategy B Specific Parameters
POWER_OF_3_THRESHOLD = 20  # Points deviation from open price

# Strategy C Specific Parameters
ATR_PERIOD = 14
DISPLACEMENT_MULTIPLIER = 2  # ATR multiplier for displacement detection

# Capital & Position Sizing
INITIAL_CAPITAL = 100000
POSITION_SIZE = 1  # Number of contracts per trade

# ============================================================================
# DATA LOADING AND PREPROCESSING
# ============================================================================

def load_data(timeframe='5m', start_year=2018, end_year=2025):
    """
    Load and concatenate CSV files for the specified timeframe and year range.
    CSV format: Date;Time;Open;High;Low;Close;Volume
    """
    all_data = []
    
    for year in range(start_year, end_year + 1):
        pattern = f"*{year}*{timeframe}.csv"
        files = glob.glob(pattern)
        
        for file in files:
            try:
                # Read CSV with semicolon delimiter
                df = pd.read_csv(file, sep=';', header=0)
                
                # Rename columns
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                
                # Combine Date and Time into DateTime
                df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                                format='%d/%m/%Y %H:%M:%S',
                                                errors='coerce')
                
                # Drop rows with invalid dates
                df = df.dropna(subset=['DateTime'])
                
                # Keep only necessary columns
                df = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                
                all_data.append(df)
                print(f"✓ Loaded {file}: {len(df)} rows")
                
            except Exception as e:
                print(f"✗ Error loading {file}: {e}")
    
    if not all_data:
        raise ValueError(f"No data files found for timeframe {timeframe}")
    
    # Concatenate all data
    data = pd.concat(all_data, ignore_index=True)
    
    # Sort by DateTime
    data = data.sort_values('DateTime').reset_index(drop=True)
    
    # Remove duplicates
    data = data.drop_duplicates(subset=['DateTime']).reset_index(drop=True)
    
    print(f"\n{'='*60}")
    print(f"Total data loaded: {len(data)} rows")
    print(f"Date range: {data['DateTime'].min()} to {data['DateTime'].max()}")
    print(f"{'='*60}\n")
    
    return data

# ============================================================================
# TECHNICAL INDICATORS
# ============================================================================

def calculate_atr(data, period=14):
    """Calculate Average True Range (ATR)"""
    high = data['High']
    low = data['Low']
    close = data['Close'].shift(1)
    
    tr1 = high - low
    tr2 = abs(high - close)
    tr3 = abs(low - close)
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr

def filter_trading_hours(data):
    """Filter data to only include trading window (01:00 - 05:00)"""
    data['Time'] = data['DateTime'].dt.time
    mask = (data['Time'] >= TRADING_START) & (data['Time'] <= TRADING_END)
    return data[mask].copy()

# ============================================================================
# STRATEGY A: JUDAS SWING (FALSE BREAKOUT)
# ============================================================================

def strategy_judas_swing(data):
    """
    Concept: Trap traders at the beginning of session
    Logic: Define High/Low of first hour (01:00-02:00)
    
    Buy Signal: Price breaks below first hour Low but closes above it (reintegration)
    Sell Signal: Price breaks above first hour High but closes below it
    """
    data = data.copy()
    data['Date'] = data['DateTime'].dt.date
    data['Hour'] = data['DateTime'].dt.hour
    
    # Identify first hour candles (01:00-02:00)
    data['FirstHour'] = (data['Hour'] == 1)
    
    # Calculate first hour High/Low for each day
    first_hour_stats = data[data['FirstHour']].groupby('Date').agg({
        'High': 'max',
        'Low': 'min'
    }).rename(columns={'High': 'FirstHourHigh', 'Low': 'FirstHourLow'})
    
    # Merge back to main data
    data = data.merge(first_hour_stats, on='Date', how='left')
    
    # Forward fill the first hour levels for the rest of the session
    data['FirstHourHigh'] = data.groupby('Date')['FirstHourHigh'].ffill()
    data['FirstHourLow'] = data.groupby('Date')['FirstHourLow'].ffill()
    
    # Generate signals (only after first hour)
    data['Signal'] = 0
    
    # Buy signal: Low breaks below FirstHourLow but Close is above it
    buy_condition = (
        (data['Hour'] > 1) &  # After first hour
        (data['Low'] < data['FirstHourLow']) &  # Break below
        (data['Close'] > data['FirstHourLow'])  # Close above (reintegration)
    )
    
    # Sell signal: High breaks above FirstHourHigh but Close is below it
    sell_condition = (
        (data['Hour'] > 1) &  # After first hour
        (data['High'] > data['FirstHourHigh']) &  # Break above
        (data['Close'] < data['FirstHourHigh'])  # Close below
    )
    
    data.loc[buy_condition, 'Signal'] = 1   # Long
    data.loc[sell_condition, 'Signal'] = -1  # Short
    
    return data.reset_index(drop=True)

# ============================================================================
# STRATEGY B: POWER OF 3 INTRADAY (OPEN DEVIATION)
# ============================================================================

def strategy_power_of_3(data, threshold=20):
    """
    Concept: Buy below open (Discount), Sell above open (Premium)
    Reference: Opening price of 01:00 candle
    
    Buy Signal: Price >20 points below Open AND bullish candle forms
    Sell Signal: Price >20 points above Open AND bearish candle forms
    """
    data = data.copy()
    data['Date'] = data['DateTime'].dt.date
    data['Hour'] = data['DateTime'].dt.hour
    
    # Get the opening price of 01:00 for each day
    session_open = data[data['Hour'] == 1].groupby('Date')['Open'].first()
    session_open = session_open.rename('SessionOpen')
    
    # Merge back to main data
    data = data.merge(session_open, on='Date', how='left')
    data['SessionOpen'] = data.groupby('Date')['SessionOpen'].ffill()
    
    # Calculate deviation from session open
    data['Deviation'] = data['Close'] - data['SessionOpen']
    
    # Identify bullish and bearish candles
    data['Bullish'] = data['Close'] > data['Open']
    data['Bearish'] = data['Close'] < data['Open']
    
    # Generate signals
    data['Signal'] = 0
    
    # Buy signal: Price >threshold points below SessionOpen AND bullish candle
    buy_condition = (
        (data['Deviation'] < -threshold) &
        (data['Bullish'])
    )
    
    # Sell signal: Price >threshold points above SessionOpen AND bearish candle
    sell_condition = (
        (data['Deviation'] > threshold) &
        (data['Bearish'])
    )
    
    data.loc[buy_condition, 'Signal'] = 1   # Long
    data.loc[sell_condition, 'Signal'] = -1  # Short
    
    return data.reset_index(drop=True)

# ============================================================================
# STRATEGY C: DISPLACEMENT (IMPULSE CANDLES)
# ============================================================================

def strategy_displacement(data, atr_multiplier=2):
    """
    Concept: Follow institutional footprint (big candles)
    Calculation: Uses ATR(14)
    
    Buy Signal: Candle body > 2*ATR AND green candle. Enter at close.
    Sell Signal: Candle body > 2*ATR AND red candle. Enter at close.
    """
    data = data.copy()
    
    # Calculate ATR
    data['ATR'] = calculate_atr(data, ATR_PERIOD)
    
    # Calculate candle body size
    data['BodySize'] = abs(data['Close'] - data['Open'])
    
    # Identify displacement threshold
    data['DisplacementThreshold'] = atr_multiplier * data['ATR']
    
    # Generate signals
    data['Signal'] = 0
    
    # Buy signal: Big body AND green candle
    buy_condition = (
        (data['BodySize'] > data['DisplacementThreshold']) &
        (data['Close'] > data['Open'])  # Green candle
    )
    
    # Sell signal: Big body AND red candle
    sell_condition = (
        (data['BodySize'] > data['DisplacementThreshold']) &
        (data['Close'] < data['Open'])  # Red candle
    )
    
    data.loc[buy_condition, 'Signal'] = 1   # Long
    data.loc[sell_condition, 'Signal'] = -1  # Short
    
    return data.reset_index(drop=True)

# ============================================================================
# BACKTESTING ENGINE
# ============================================================================

def backtest(data, strategy_name, risk_mode):
    """
    Vectorized backtesting engine with stop-loss, take-profit, and hard exit at 05:00
    """
    data = data.copy()
    data = data.reset_index(drop=True)  # Reset index to ensure sequential integers
    
    # Get risk parameters
    risk_params = RISK_MODES[risk_mode]
    
    # Calculate ATR if needed for dynamic risk mode
    if risk_mode == 3:
        data['ATR'] = calculate_atr(data, ATR_PERIOD)
    
    # Initialize tracking columns
    data['Position'] = 0  # Current position: 0=flat, 1=long, -1=short
    data['EntryPrice'] = 0.0
    data['StopLoss'] = 0.0
    data['TakeProfit'] = 0.0
    data['PnL'] = 0.0
    data['Trade'] = 0  # Trade ID
    data['TradeExit'] = ''  # Exit reason
    
    # Trading state variables
    position = 0
    entry_price = 0.0
    stop_loss = 0.0
    take_profit = 0.0
    trade_count = 0
    equity = INITIAL_CAPITAL
    equity_curve = []
    trades = []
    
    for i in range(len(data)):
        current_time = data.loc[i, 'DateTime'].time()
        current_price = data.loc[i, 'Close']
        current_high = data.loc[i, 'High']
        current_low = data.loc[i, 'Low']
        signal = data.loc[i, 'Signal']
        
        # Hard exit at 05:00
        if current_time >= TRADING_END and position != 0:
            pnl = (current_price - entry_price) * position * POSITION_SIZE
            equity += pnl
            
            trades.append({
                'EntryTime': data.loc[data['Trade'] == trade_count, 'DateTime'].iloc[0],
                'ExitTime': data.loc[i, 'DateTime'],
                'Direction': 'Long' if position == 1 else 'Short',
                'EntryPrice': entry_price,
                'ExitPrice': current_price,
                'PnL': pnl,
                'ExitReason': 'HardExit'
            })
            
            data.loc[i, 'PnL'] = pnl
            data.loc[i, 'TradeExit'] = 'HardExit'
            position = 0
            entry_price = 0.0
        
        # Check for stop-loss or take-profit if in a position
        if position != 0:
            # Long position checks
            if position == 1:
                # Check stop-loss
                if current_low <= stop_loss:
                    pnl = (stop_loss - entry_price) * POSITION_SIZE
                    equity += pnl
                    
                    trades.append({
                        'EntryTime': data.loc[data['Trade'] == trade_count, 'DateTime'].iloc[0],
                        'ExitTime': data.loc[i, 'DateTime'],
                        'Direction': 'Long',
                        'EntryPrice': entry_price,
                        'ExitPrice': stop_loss,
                        'PnL': pnl,
                        'ExitReason': 'StopLoss'
                    })
                    
                    data.loc[i, 'PnL'] = pnl
                    data.loc[i, 'TradeExit'] = 'StopLoss'
                    position = 0
                    entry_price = 0.0
                
                # Check take-profit
                elif current_high >= take_profit:
                    pnl = (take_profit - entry_price) * POSITION_SIZE
                    equity += pnl
                    
                    trades.append({
                        'EntryTime': data.loc[data['Trade'] == trade_count, 'DateTime'].iloc[0],
                        'ExitTime': data.loc[i, 'DateTime'],
                        'Direction': 'Long',
                        'EntryPrice': entry_price,
                        'ExitPrice': take_profit,
                        'PnL': pnl,
                        'ExitReason': 'TakeProfit'
                    })
                    
                    data.loc[i, 'PnL'] = pnl
                    data.loc[i, 'TradeExit'] = 'TakeProfit'
                    position = 0
                    entry_price = 0.0
            
            # Short position checks
            elif position == -1:
                # Check stop-loss
                if current_high >= stop_loss:
                    pnl = (entry_price - stop_loss) * POSITION_SIZE
                    equity += pnl
                    
                    trades.append({
                        'EntryTime': data.loc[data['Trade'] == trade_count, 'DateTime'].iloc[0],
                        'ExitTime': data.loc[i, 'DateTime'],
                        'Direction': 'Short',
                        'EntryPrice': entry_price,
                        'ExitPrice': stop_loss,
                        'PnL': pnl,
                        'ExitReason': 'StopLoss'
                    })
                    
                    data.loc[i, 'PnL'] = pnl
                    data.loc[i, 'TradeExit'] = 'StopLoss'
                    position = 0
                    entry_price = 0.0
                
                # Check take-profit
                elif current_low <= take_profit:
                    pnl = (entry_price - take_profit) * POSITION_SIZE
                    equity += pnl
                    
                    trades.append({
                        'EntryTime': data.loc[data['Trade'] == trade_count, 'DateTime'].iloc[0],
                        'ExitTime': data.loc[i, 'DateTime'],
                        'Direction': 'Short',
                        'EntryPrice': entry_price,
                        'ExitPrice': take_profit,
                        'PnL': pnl,
                        'ExitReason': 'TakeProfit'
                    })
                    
                    data.loc[i, 'PnL'] = pnl
                    data.loc[i, 'TradeExit'] = 'TakeProfit'
                    position = 0
                    entry_price = 0.0
        
        # Enter new position if flat and signal present
        if position == 0 and signal != 0:
            trade_count += 1
            position = signal
            entry_price = current_price
            
            # Calculate stop-loss and take-profit based on risk mode
            if risk_mode == 3:  # Dynamic ATR-based
                atr_value = data.loc[i, 'ATR']
                if pd.notna(atr_value):
                    sl_distance = risk_params['sl_multiplier'] * atr_value
                    tp_distance = risk_params['tp_multiplier'] * atr_value
                else:
                    # Fallback to Mode 1 if ATR not available
                    sl_distance = RISK_MODES[1]['sl']
                    tp_distance = RISK_MODES[1]['tp']
            else:  # Fixed modes
                sl_distance = risk_params['sl']
                tp_distance = risk_params['tp']
            
            if position == 1:  # Long
                stop_loss = entry_price - sl_distance
                take_profit = entry_price + tp_distance
            else:  # Short
                stop_loss = entry_price + sl_distance
                take_profit = entry_price - tp_distance
            
            data.loc[i, 'Trade'] = trade_count
            data.loc[i, 'EntryPrice'] = entry_price
            data.loc[i, 'StopLoss'] = stop_loss
            data.loc[i, 'TakeProfit'] = take_profit
        
        # Update position tracking
        data.loc[i, 'Position'] = position
        equity_curve.append(equity)
    
    # Convert trades list to DataFrame
    trades_df = pd.DataFrame(trades)
    
    return data, trades_df, equity_curve

# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

def calculate_metrics(trades_df, equity_curve, initial_capital):
    """Calculate performance metrics"""
    if len(trades_df) == 0:
        return {
            'Total Trades': 0,
            'Win Rate (%)': 0,
            'Profit Factor': 0,
            'Total PnL': 0,
            'Final Equity': initial_capital,
            'Return (%)': 0
        }
    
    # Basic metrics
    total_trades = len(trades_df)
    winning_trades = len(trades_df[trades_df['PnL'] > 0])
    losing_trades = len(trades_df[trades_df['PnL'] < 0])
    
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    
    # Profit factor
    gross_profit = trades_df[trades_df['PnL'] > 0]['PnL'].sum()
    gross_loss = abs(trades_df[trades_df['PnL'] < 0]['PnL'].sum())
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
    
    # Total PnL
    total_pnl = trades_df['PnL'].sum()
    final_equity = equity_curve[-1] if equity_curve else initial_capital
    total_return = ((final_equity - initial_capital) / initial_capital * 100)
    
    metrics = {
        'Total Trades': total_trades,
        'Winning Trades': winning_trades,
        'Losing Trades': losing_trades,
        'Win Rate (%)': round(win_rate, 2),
        'Profit Factor': round(profit_factor, 2),
        'Total PnL': round(total_pnl, 2),
        'Gross Profit': round(gross_profit, 2),
        'Gross Loss': round(gross_loss, 2),
        'Initial Capital': initial_capital,
        'Final Equity': round(final_equity, 2),
        'Return (%)': round(total_return, 2)
    }
    
    return metrics

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("ICT TRADING STRATEGIES BACKTEST SYSTEM")
    print("="*60)
    
    # Display configuration
    strategy_names = {
        'A': 'Judas Swing (False Breakout)',
        'B': 'Power of 3 Intraday (Open Deviation)',
        'C': 'Displacement (Impulse Candles)'
    }
    
    print(f"\n📊 CONFIGURATION:")
    print(f"  Strategy: {STRATEGY} - {strategy_names[STRATEGY]}")
    print(f"  Risk Mode: {RISK_MODE} - {RISK_MODES[RISK_MODE]['name']}")
    print(f"  Timeframe: {DATA_TIMEFRAME}")
    print(f"  Years: {START_YEAR} - {END_YEAR}")
    print(f"  Trading Window: {TRADING_START} - {TRADING_END}")
    print(f"  Initial Capital: ${INITIAL_CAPITAL:,}")
    print()
    
    # Load data
    print("📂 Loading data...")
    data = load_data(DATA_TIMEFRAME, START_YEAR, END_YEAR)
    
    # Filter to trading hours
    print("🕐 Filtering to trading hours (01:00-05:00)...")
    data = filter_trading_hours(data)
    print(f"  Rows after filtering: {len(data)}")
    print()
    
    # Apply selected strategy
    print(f"🎯 Applying Strategy {STRATEGY}: {strategy_names[STRATEGY]}...")
    
    if STRATEGY == 'A':
        data = strategy_judas_swing(data)
    elif STRATEGY == 'B':
        data = strategy_power_of_3(data, POWER_OF_3_THRESHOLD)
    elif STRATEGY == 'C':
        data = strategy_displacement(data, DISPLACEMENT_MULTIPLIER)
    else:
        raise ValueError(f"Invalid strategy: {STRATEGY}")
    
    signals_count = len(data[data['Signal'] != 0])
    print(f"  Generated {signals_count} signals")
    print()
    
    # Run backtest
    print("⚙️  Running backtest...")
    data, trades_df, equity_curve = backtest(data, STRATEGY, RISK_MODE)
    print(f"  Completed {len(trades_df)} trades")
    print()
    
    # Calculate metrics
    print("📈 Calculating performance metrics...")
    metrics = calculate_metrics(trades_df, equity_curve, INITIAL_CAPITAL)
    print()
    
    # Display results
    print("="*60)
    print("BACKTEST RESULTS")
    print("="*60)
    
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"  {key:.<35} {value:>20,.2f}")
        else:
            print(f"  {key:.<35} {value:>20,}")
    
    print("="*60)
    
    # Display sample trades
    if len(trades_df) > 0:
        print("\n📋 Sample Trades (First 10):")
        print(trades_df.head(10).to_string(index=False))
        
        # Save results to CSV
        output_file = f"backtest_results_{STRATEGY}_mode{RISK_MODE}_{DATA_TIMEFRAME}.csv"
        trades_df.to_csv(output_file, index=False)
        print(f"\n💾 Full results saved to: {output_file}")
    
    print("\n✅ Backtest complete!\n")
    
    return data, trades_df, equity_curve, metrics


if __name__ == "__main__":
    data, trades_df, equity_curve, metrics = main()
