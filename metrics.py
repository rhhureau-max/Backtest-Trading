"""
Metrics Module for 8:30 Strategy Backtest

This module calculates performance metrics for the backtest.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def calculate_win_rate(trades: pd.DataFrame) -> float:
    """
    Calculate win rate percentage.
    
    Args:
        trades: DataFrame with trade results
        
    Returns:
        Win rate as percentage
    """
    if len(trades) == 0:
        return 0.0
    
    wins = len(trades[trades['result'] == 'Win'])
    return (wins / len(trades)) * 100


def calculate_profit_factor(trades: pd.DataFrame) -> float:
    """
    Calculate profit factor (total gains / total losses).
    
    Args:
        trades: DataFrame with trade results
        
    Returns:
        Profit factor (inf if no losses)
    """
    wins = trades[trades['result'] == 'Win']
    losses = trades[trades['result'] == 'Loss']
    
    total_gains = wins['pnl_r'].sum() if len(wins) > 0 else 0
    total_losses = abs(losses['pnl_r'].sum()) if len(losses) > 0 else 0
    
    if total_losses == 0:
        return float('inf') if total_gains > 0 else 0
    
    return total_gains / total_losses


def calculate_expectancy(trades: pd.DataFrame) -> float:
    """
    Calculate expectancy: (Win% * Avg Win) - (Loss% * Avg Loss).
    
    Args:
        trades: DataFrame with trade results
        
    Returns:
        Expectancy value in R
    """
    if len(trades) == 0:
        return 0.0
    
    wins = trades[trades['result'] == 'Win']
    losses = trades[trades['result'] == 'Loss']
    
    win_pct = len(wins) / len(trades)
    loss_pct = len(losses) / len(trades)
    
    avg_win = wins['pnl_r'].mean() if len(wins) > 0 else 0
    avg_loss = abs(losses['pnl_r'].mean()) if len(losses) > 0 else 0
    
    return (win_pct * avg_win) - (loss_pct * avg_loss)


def calculate_average_rr(trades: pd.DataFrame) -> float:
    """
    Calculate average RR realized.
    
    Args:
        trades: DataFrame with trade results
        
    Returns:
        Average RR
    """
    if len(trades) == 0:
        return 0.0
    
    return trades['pnl_r'].mean()


def calculate_max_consecutive(trades: pd.DataFrame, result_type: str) -> int:
    """
    Calculate maximum consecutive wins or losses.
    
    Args:
        trades: DataFrame with trade results
        result_type: 'Win' or 'Loss'
        
    Returns:
        Max consecutive count
    """
    if len(trades) == 0:
        return 0
    
    results = trades['result'].values
    max_consec = 0
    current_consec = 0
    
    for r in results:
        if r == result_type:
            current_consec += 1
            max_consec = max(max_consec, current_consec)
        else:
            current_consec = 0
    
    return max_consec


def calculate_max_drawdown(trades: pd.DataFrame) -> float:
    """
    Calculate maximum drawdown as percentage.
    
    Args:
        trades: DataFrame with trade results
        
    Returns:
        Max drawdown percentage
    """
    if len(trades) == 0:
        return 0.0
    
    # Calculate cumulative R returns
    cumulative = trades['pnl_r'].cumsum()
    
    # Calculate running maximum
    running_max = cumulative.expanding().max()
    
    # Calculate drawdown
    drawdown = running_max - cumulative
    
    # Max drawdown as percentage of peak (use starting capital of 100R)
    starting_capital = 100.0
    peaks = starting_capital + running_max
    max_dd = (drawdown / peaks * 100).max()
    
    return max_dd if not np.isnan(max_dd) else 0.0


def calculate_direction_stats(trades: pd.DataFrame) -> Dict:
    """
    Calculate statistics by direction (LONG/SHORT).
    
    Args:
        trades: DataFrame with trade results
        
    Returns:
        Dict with direction statistics
    """
    long_trades = trades[trades['direction'] == 'LONG']
    short_trades = trades[trades['direction'] == 'SHORT']
    
    return {
        'num_long': len(long_trades),
        'num_short': len(short_trades),
        'win_rate_long': calculate_win_rate(long_trades),
        'win_rate_short': calculate_win_rate(short_trades)
    }


def calculate_all_metrics(trades: pd.DataFrame) -> Dict:
    """
    Calculate all performance metrics.
    
    Args:
        trades: DataFrame with trade results
        
    Returns:
        Dict with all metrics
    """
    completed_trades = trades[trades['result'].isin(['Win', 'Loss'])].copy()
    
    direction_stats = calculate_direction_stats(completed_trades)
    
    return {
        'total_trades': len(completed_trades),
        'wins': len(completed_trades[completed_trades['result'] == 'Win']),
        'losses': len(completed_trades[completed_trades['result'] == 'Loss']),
        'win_rate': calculate_win_rate(completed_trades),
        'profit_factor': calculate_profit_factor(completed_trades),
        'expectancy': calculate_expectancy(completed_trades),
        'avg_rr': calculate_average_rr(completed_trades),
        'max_consec_wins': calculate_max_consecutive(completed_trades, 'Win'),
        'max_consec_losses': calculate_max_consecutive(completed_trades, 'Loss'),
        'max_drawdown': calculate_max_drawdown(completed_trades),
        **direction_stats
    }


def format_metrics_table(results: List[Dict]) -> pd.DataFrame:
    """
    Format results into a summary table.
    
    Args:
        results: List of result dictionaries
        
    Returns:
        Formatted DataFrame
    """
    df = pd.DataFrame(results)
    
    # Round numeric columns
    numeric_cols = ['win_rate', 'profit_factor', 'expectancy', 'avg_rr', 
                    'max_drawdown', 'win_rate_long', 'win_rate_short']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].round(2)
    
    return df


if __name__ == "__main__":
    # Test the metrics module
    print("Metrics module loaded successfully")
    
    # Create sample data for testing
    sample_trades = pd.DataFrame({
        'result': ['Win', 'Loss', 'Win', 'Win', 'Loss', 'Win'],
        'pnl_r': [2.0, -1.0, 2.0, 2.0, -1.0, 2.0],
        'direction': ['LONG', 'SHORT', 'LONG', 'SHORT', 'LONG', 'SHORT']
    })
    
    metrics = calculate_all_metrics(sample_trades)
    print("\nSample metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
