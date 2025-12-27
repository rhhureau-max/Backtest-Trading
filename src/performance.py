"""
Performance metrics calculation.
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from strategies.base_strategy import Trade


class PerformanceMetrics:
    """
    Calculate performance metrics for trading strategies.
    """
    
    def __init__(self, trades: List[Trade], risk_free_rate: float = 0.02):
        self.trades = [t for t in trades if t.status in ['closed', 'stopped']]
        self.risk_free_rate = risk_free_rate
    
    def calculate_all_metrics(self) -> Dict[str, float]:
        """
        Calculate all performance metrics.
        
        Returns:
            Dictionary with all metrics
        """
        if not self.trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'average_win': 0.0,
                'average_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0,
                'sharpe_ratio': 0.0,
                'total_return': 0.0
            }
        
        total_trades = len(self.trades)
        pnls = [t.pnl for t in self.trades]
        
        winning_trades = [t for t in self.trades if t.pnl > 0]
        losing_trades = [t for t in self.trades if t.pnl <= 0]
        
        winning_count = len(winning_trades)
        losing_count = len(losing_trades)
        
        win_rate = (winning_count / total_trades * 100) if total_trades > 0 else 0.0
        
        total_pnl = sum(pnls)
        
        average_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0.0
        average_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0.0
        
        gross_profit = sum([t.pnl for t in winning_trades]) if winning_trades else 0.0
        gross_loss = abs(sum([t.pnl for t in losing_trades])) if losing_trades else 0.0
        
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf') if gross_profit > 0 else 0.0
        
        max_drawdown = self._calculate_max_drawdown(pnls)
        sharpe_ratio = self._calculate_sharpe_ratio(pnls)
        
        # Total return as percentage (assuming each point = $1 or equivalent)
        total_return = total_pnl
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_count,
            'losing_trades': losing_count,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'average_win': average_win,
            'average_loss': average_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'total_return': total_return
        }
    
    def _calculate_max_drawdown(self, pnls: List[float]) -> float:
        """
        Calculate maximum drawdown.
        
        Args:
            pnls: List of PnL values
        
        Returns:
            Maximum drawdown value
        """
        if not pnls:
            return 0.0
        
        cumulative = np.cumsum(pnls)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = running_max - cumulative
        
        return np.max(drawdown) if len(drawdown) > 0 else 0.0
    
    def _calculate_sharpe_ratio(self, pnls: List[float]) -> float:
        """
        Calculate Sharpe Ratio.
        
        Args:
            pnls: List of PnL values
        
        Returns:
            Sharpe ratio
        """
        if not pnls or len(pnls) < 2:
            return 0.0
        
        # Convert PnL to returns
        returns = np.array(pnls)
        
        # Calculate mean and std of returns
        mean_return = np.mean(returns)
        std_return = np.std(returns, ddof=1)
        
        if std_return == 0:
            return 0.0
        
        # Annualized Sharpe Ratio (assuming daily returns)
        # Using 252 trading days per year
        sharpe = (mean_return * 252 - self.risk_free_rate) / (std_return * np.sqrt(252))
        
        return sharpe
    
    def get_trade_distribution(self) -> Dict[str, int]:
        """
        Get distribution of trade outcomes.
        
        Returns:
            Dictionary with trade distribution
        """
        if not self.trades:
            return {
                'tp1_only': 0,
                'tp1_and_tp2': 0,
                'stopped_out': 0,
                'closed_manually': 0
            }
        
        tp1_only = sum(1 for t in self.trades if t.tp1_hit and not t.tp2_hit and t.status == 'closed')
        tp1_and_tp2 = sum(1 for t in self.trades if t.tp1_hit and t.tp2_hit)
        stopped_out = sum(1 for t in self.trades if t.status == 'stopped')
        closed_manually = sum(1 for t in self.trades if t.status == 'closed' and not t.tp1_hit)
        
        return {
            'tp1_only': tp1_only,
            'tp1_and_tp2': tp1_and_tp2,
            'stopped_out': stopped_out,
            'closed_manually': closed_manually
        }
    
    def get_monthly_performance(self) -> pd.DataFrame:
        """
        Get monthly performance breakdown.
        
        Returns:
            DataFrame with monthly PnL
        """
        if not self.trades:
            return pd.DataFrame()
        
        trade_data = []
        for trade in self.trades:
            trade_data.append({
                'date': trade.entry_time,
                'pnl': trade.pnl
            })
        
        df = pd.DataFrame(trade_data)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        monthly = df.groupby('month').agg({
            'pnl': ['sum', 'count', 'mean']
        }).round(2)
        
        monthly.columns = ['total_pnl', 'trade_count', 'avg_pnl']
        
        return monthly
