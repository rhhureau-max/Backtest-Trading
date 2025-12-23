"""
Metrics calculation module for backtest performance analysis.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any
from dataclasses import dataclass
from trade_manager import Trade, TradeStatus


@dataclass
class BacktestMetrics:
    """Container for all backtest metrics."""
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    
    gross_profit: float = 0.0
    gross_loss: float = 0.0
    net_profit: float = 0.0
    profit_factor: float = 0.0
    
    max_drawdown: float = 0.0
    max_drawdown_pct: float = 0.0
    
    avg_win: float = 0.0
    avg_loss: float = 0.0
    avg_rr: float = 0.0
    
    # By year
    stats_by_year: Dict[int, Dict[str, Any]] = None
    
    # By session
    stats_by_session: Dict[str, Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.stats_by_year is None:
            self.stats_by_year = {}
        if self.stats_by_session is None:
            self.stats_by_session = {}


def calculate_metrics(trades: List[Trade]) -> BacktestMetrics:
    """
    Calculate all backtest metrics from a list of trades.
    
    Args:
        trades: List of closed Trade objects
        
    Returns:
        BacktestMetrics object with all calculated metrics
    """
    metrics = BacktestMetrics()
    
    # Filter to closed trades only
    closed_trades = [t for t in trades if t.status in [TradeStatus.CLOSED_WIN, TradeStatus.CLOSED_LOSS]]
    
    if not closed_trades:
        return metrics
    
    metrics.total_trades = len(closed_trades)
    
    # Win/Loss counts
    wins = [t for t in closed_trades if t.status == TradeStatus.CLOSED_WIN]
    losses = [t for t in closed_trades if t.status == TradeStatus.CLOSED_LOSS]
    
    metrics.winning_trades = len(wins)
    metrics.losing_trades = len(losses)
    
    # Win rate
    metrics.win_rate = (metrics.winning_trades / metrics.total_trades) * 100 if metrics.total_trades > 0 else 0
    
    # Profit/Loss calculations (using normalized PnL based on risk)
    # Normalize by risk to make results comparable
    for trade in closed_trades:
        if trade.risk > 0:
            normalized_pnl = trade.pnl / trade.risk  # Result in R-multiples
            if trade.status == TradeStatus.CLOSED_WIN:
                metrics.gross_profit += normalized_pnl
            else:
                metrics.gross_loss += abs(normalized_pnl)
    
    metrics.net_profit = metrics.gross_profit - metrics.gross_loss
    
    # Profit factor
    metrics.profit_factor = metrics.gross_profit / metrics.gross_loss if metrics.gross_loss > 0 else float('inf')
    
    # Average win/loss in R-multiples
    if wins:
        win_rrs = [t.actual_rr for t in wins]
        metrics.avg_win = np.mean(win_rrs)
    
    if losses:
        loss_rrs = [abs(t.actual_rr) for t in losses]
        metrics.avg_loss = np.mean(loss_rrs)
    
    # Average realized R:R
    all_rrs = [t.actual_rr for t in closed_trades]
    metrics.avg_rr = np.mean(all_rrs)
    
    # Maximum drawdown calculation
    metrics.max_drawdown, metrics.max_drawdown_pct = calculate_max_drawdown(closed_trades)
    
    # Stats by year
    metrics.stats_by_year = calculate_stats_by_year(closed_trades)
    
    # Stats by session
    metrics.stats_by_session = calculate_stats_by_session(closed_trades)
    
    return metrics


def calculate_max_drawdown(trades: List[Trade]) -> tuple:
    """
    Calculate maximum drawdown from trade sequence.
    
    Returns:
        Tuple of (max_drawdown_in_R, max_drawdown_percentage)
        The percentage represents the drawdown relative to the highest equity peak.
    """
    if not trades:
        return 0.0, 0.0
    
    # Sort trades by exit time
    sorted_trades = sorted(trades, key=lambda t: t.exit_time if t.exit_time else t.entry_time)
    
    # Calculate equity curve (in R-multiples, starting from 0)
    equity = [0.0]
    
    for trade in sorted_trades:
        if trade.risk > 0:
            r_result = trade.pnl / trade.risk
            equity.append(equity[-1] + r_result)
    
    if len(equity) < 2:
        return 0.0, 0.0
    
    # Calculate drawdown
    peak = equity[0]
    max_dd = 0.0
    max_dd_at_peak = 0.0
    current_peak_for_max_dd = 0.0
    
    for value in equity:
        if value > peak:
            peak = value
        dd = peak - value
        if dd > max_dd:
            max_dd = dd
            current_peak_for_max_dd = peak
    
    # Calculate percentage: if peak is positive, use that; otherwise express as absolute
    if current_peak_for_max_dd > 0:
        max_dd_pct = (max_dd / current_peak_for_max_dd) * 100
    else:
        # If peak was never positive, just show raw drawdown
        max_dd_pct = 0.0
    
    return max_dd, max_dd_pct


def calculate_stats_by_year(trades: List[Trade]) -> Dict[int, Dict[str, Any]]:
    """Calculate statistics grouped by year."""
    stats = {}
    
    # Group trades by year
    by_year = {}
    for trade in trades:
        year = trade.year
        if year not in by_year:
            by_year[year] = []
        by_year[year].append(trade)
    
    for year, year_trades in sorted(by_year.items()):
        wins = [t for t in year_trades if t.status == TradeStatus.CLOSED_WIN]
        losses = [t for t in year_trades if t.status == TradeStatus.CLOSED_LOSS]
        
        total = len(year_trades)
        win_count = len(wins)
        
        gross_profit = sum(t.pnl / t.risk for t in wins if t.risk > 0)
        gross_loss = sum(abs(t.pnl / t.risk) for t in losses if t.risk > 0)
        
        stats[year] = {
            'total_trades': total,
            'wins': win_count,
            'losses': len(losses),
            'win_rate': (win_count / total) * 100 if total > 0 else 0,
            'gross_profit_r': gross_profit,
            'gross_loss_r': gross_loss,
            'net_profit_r': gross_profit - gross_loss,
            'profit_factor': gross_profit / gross_loss if gross_loss > 0 else float('inf'),
            'avg_rr': np.mean([t.actual_rr for t in year_trades]) if year_trades else 0,
        }
    
    return stats


def calculate_stats_by_session(trades: List[Trade]) -> Dict[str, Dict[str, Any]]:
    """Calculate statistics grouped by trading session."""
    stats = {}
    
    # Group trades by session
    by_session = {}
    for trade in trades:
        session = trade.session
        if session not in by_session:
            by_session[session] = []
        by_session[session].append(trade)
    
    for session, session_trades in sorted(by_session.items()):
        wins = [t for t in session_trades if t.status == TradeStatus.CLOSED_WIN]
        losses = [t for t in session_trades if t.status == TradeStatus.CLOSED_LOSS]
        
        total = len(session_trades)
        win_count = len(wins)
        
        gross_profit = sum(t.pnl / t.risk for t in wins if t.risk > 0)
        gross_loss = sum(abs(t.pnl / t.risk) for t in losses if t.risk > 0)
        
        stats[session] = {
            'total_trades': total,
            'wins': win_count,
            'losses': len(losses),
            'win_rate': (win_count / total) * 100 if total > 0 else 0,
            'gross_profit_r': gross_profit,
            'gross_loss_r': gross_loss,
            'net_profit_r': gross_profit - gross_loss,
            'profit_factor': gross_profit / gross_loss if gross_loss > 0 else float('inf'),
            'avg_rr': np.mean([t.actual_rr for t in session_trades]) if session_trades else 0,
        }
    
    return stats


def generate_results_markdown(metrics: BacktestMetrics, trades: List[Trade]) -> str:
    """
    Generate a markdown report of backtest results.
    
    Args:
        metrics: Calculated backtest metrics
        trades: List of all trades
        
    Returns:
        Markdown formatted string
    """
    md = []
    md.append("# Backtest Results\n")
    md.append(f"*Generated from backtest of Liquidity Sweep strategy*\n")
    md.append("---\n")
    
    # Summary Statistics
    md.append("## Summary Statistics\n")
    md.append(f"| Metric | Value |")
    md.append(f"|--------|-------|")
    md.append(f"| **Total Trades** | {metrics.total_trades} |")
    md.append(f"| **Winning Trades** | {metrics.winning_trades} |")
    md.append(f"| **Losing Trades** | {metrics.losing_trades} |")
    md.append(f"| **Win Rate** | {metrics.win_rate:.2f}% |")
    md.append(f"| **Profit Factor** | {metrics.profit_factor:.2f} |")
    md.append(f"| **Net Profit (R)** | {metrics.net_profit:.2f}R |")
    md.append(f"| **Maximum Drawdown** | {metrics.max_drawdown:.2f}R ({metrics.max_drawdown_pct:.2f}%) |")
    md.append(f"| **Average Win (R:R)** | {metrics.avg_win:.2f} |")
    md.append(f"| **Average Loss (R:R)** | {metrics.avg_loss:.2f} |")
    md.append(f"| **Average Realized R:R** | {metrics.avg_rr:.2f} |")
    md.append("")
    
    # Statistics by Year
    md.append("## Statistics by Year\n")
    if metrics.stats_by_year:
        md.append("| Year | Trades | Wins | Losses | Win Rate | Net Profit (R) | Profit Factor | Avg R:R |")
        md.append("|------|--------|------|--------|----------|----------------|---------------|---------|")
        for year, stats in sorted(metrics.stats_by_year.items()):
            pf = f"{stats['profit_factor']:.2f}" if stats['profit_factor'] != float('inf') else "∞"
            md.append(
                f"| {year} | {stats['total_trades']} | {stats['wins']} | {stats['losses']} | "
                f"{stats['win_rate']:.1f}% | {stats['net_profit_r']:.2f}R | {pf} | {stats['avg_rr']:.2f} |"
            )
    else:
        md.append("*No yearly data available*")
    md.append("")
    
    # Statistics by Session
    md.append("## Statistics by Session\n")
    if metrics.stats_by_session:
        md.append("| Session | Trades | Wins | Losses | Win Rate | Net Profit (R) | Profit Factor | Avg R:R |")
        md.append("|---------|--------|------|--------|----------|----------------|---------------|---------|")
        for session, stats in sorted(metrics.stats_by_session.items()):
            pf = f"{stats['profit_factor']:.2f}" if stats['profit_factor'] != float('inf') else "∞"
            md.append(
                f"| {session} | {stats['total_trades']} | {stats['wins']} | {stats['losses']} | "
                f"{stats['win_rate']:.1f}% | {stats['net_profit_r']:.2f}R | {pf} | {stats['avg_rr']:.2f} |"
            )
    else:
        md.append("*No session data available*")
    md.append("")
    
    # Strategy Description
    md.append("## Strategy Description\n")
    md.append("### Trading Sessions (UTC)")
    md.append("- **Session 1**: 02:00 to 05:00")
    md.append("- **Session 2**: 08:30 to 11:00\n")
    
    md.append("### HTF Context")
    md.append("- Liquidity sweep on old high/low (detected using fractals)\n")
    
    md.append("### LTF Entry (M5)")
    md.append("1. New FVG forms in M5 (displacement)")
    md.append("2. Price retraces to fill M5 FVG")
    md.append("3. Reversal candle confirms entry\n")
    
    md.append("### Trade Management")
    md.append("- Entry: At close of reversal candle")
    md.append("- Stop Loss: Below/above swing created during FVG rejection")
    md.append("- Take Profit: 1:1 Risk/Reward ratio\n")
    
    md.append("---")
    md.append("*Note: All profit/loss values are expressed in R-multiples (risk units)*")
    
    return "\n".join(md)
