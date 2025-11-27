"""
Configuration settings for the backtest strategy.
"""
from dataclasses import dataclass
from typing import Tuple
from datetime import time


@dataclass
class SessionConfig:
    """Trading session configuration."""
    name: str
    start: time
    end: time


@dataclass
class BacktestConfig:
    """Main backtest configuration."""
    # Backtest period
    start_year: int = 2018
    end_year: int = 2025
    
    # Risk/Reward ratio for take profit
    risk_reward_ratio: float = 2.0
    
    # Stop loss buffer in price units (percentage of price)
    stop_loss_buffer_pct: float = 0.0001  # 0.01% buffer
    
    # FVG detection parameters
    fvg_min_gap_pct: float = 0.0001  # Minimum gap size as percentage of price
    
    # FVG zone tolerance for price interaction checks
    fvg_zone_tolerance_upper: float = 1.001  # 0.1% tolerance above
    fvg_zone_tolerance_lower: float = 0.999  # 0.1% tolerance below
    
    # Liquidity sweep buffer percentage
    liquidity_sweep_buffer_pct: float = 0.0002  # 0.02% buffer for sweep detection
    
    # Fractal lookback periods for liquidity detection
    fractal_lookback: int = 2  # Standard Williams fractal
    
    # Maximum number of candles to wait for FVG fill
    max_fvg_fill_candles: int = 50
    
    # Data directory (relative to main.py)
    data_dir: str = ".."
    
    # Trading sessions (UTC)
    sessions: Tuple[SessionConfig, ...] = (
        SessionConfig("Session 1", time(2, 0), time(5, 0)),
        SessionConfig("Session 2", time(8, 30), time(11, 0)),
    )
    
    # Timeframe file patterns
    htf_h1_pattern: str = "{year} 1H.csv"
    htf_m15_pattern: str = "{year} 15m.csv"
    ltf_m5_pattern: str = "{year} 5m.csv"
    
    # Logging
    log_level: str = "WARNING"
    log_trades: bool = True


# Default configuration instance
DEFAULT_CONFIG = BacktestConfig()
