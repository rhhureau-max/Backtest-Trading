"""
Configuration settings for the backtesting system.
"""

# Trading Parameters
SPREAD_POINTS = 1.5  # Spread in points per trade
LONDON_SESSION_START = "08:00:00"  # Paris time
LONDON_SESSION_END = "12:00:00"    # Paris time
ASIAN_SESSION_START = "00:00:00"   # Paris time
ASIAN_SESSION_END = "08:00:00"     # Paris time

# Data Parameters
DATA_DIR = "."  # Root directory containing CSV files
TIMEFRAMES = {
    '1m': '1m',
    '5m': '5m',
    '15m': '15m',
    '1h': '1H',
    '1d': '1D',
    '4h': '4H'
}

# Years to backtest
YEARS = list(range(2018, 2026))

# Strategy Parameters
JUDAS_SWING_PARAMS = {
    'atr_period': 14,
    'atr_multiplier': 0.2,  # 20% of ATR for stop loss buffer
    'tp1_percentage': 0.5,  # 50% of position at TP1
    'tp2_percentage': 0.5   # 50% of position at TP2
}

ORB_RETEST_PARAMS = {
    'orb_start': '08:00:00',
    'orb_end': '09:00:00',
    'tp1_percentage': 0.7,  # 70% of position at TP1
    'tp2_percentage': 0.3   # 30% of position at TP2
}

HTF_TREND_PARAMS = {
    'ema_period': 9,
    'fib_ote_low': 0.62,  # 62% Fibonacci retracement
    'fib_ote_high': 0.79  # 79% Fibonacci retracement
}

# Performance Metrics
RISK_FREE_RATE = 0.02  # 2% annual risk-free rate for Sharpe calculation
