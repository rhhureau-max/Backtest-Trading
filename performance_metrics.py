"""
Performance Metrics Calculator
Calculates comprehensive trading statistics and risk metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime


class PerformanceMetrics:
    """Calculate trading performance metrics"""
    
    def __init__(self, trades_df, initial_capital=10000):
        self.trades_df = trades_df
        self.initial_capital = initial_capital
        
    def calculate_all_metrics(self):
        """
        Calculate all performance metrics
        
        Returns:
        --------
        dict
            Dictionary containing all metrics
        """
        if len(self.trades_df) == 0:
            return self._empty_metrics()
        
        metrics = {}
        
        # Basic Statistics
        metrics['total_trades'] = len(self.trades_df)
        metrics['winning_trades'] = len(self.trades_df[self.trades_df['pnl'] > 0])
        metrics['losing_trades'] = len(self.trades_df[self.trades_df['pnl'] < 0])
        metrics['breakeven_trades'] = len(self.trades_df[self.trades_df['pnl'] == 0])
        
        # Win Rate
        if metrics['total_trades'] > 0:
            metrics['win_rate'] = (metrics['winning_trades'] / metrics['total_trades']) * 100
        else:
            metrics['win_rate'] = 0
        
        # P&L Statistics
        metrics['total_pnl'] = self.trades_df['pnl'].sum()
        metrics['avg_pnl'] = self.trades_df['pnl'].mean()
        metrics['median_pnl'] = self.trades_df['pnl'].median()
        metrics['std_pnl'] = self.trades_df['pnl'].std()
        
        # Win/Loss Analysis
        winning_trades = self.trades_df[self.trades_df['pnl'] > 0]
        losing_trades = self.trades_df[self.trades_df['pnl'] < 0]
        
        if len(winning_trades) > 0:
            metrics['avg_win'] = winning_trades['pnl'].mean()
            metrics['max_win'] = winning_trades['pnl'].max()
        else:
            metrics['avg_win'] = 0
            metrics['max_win'] = 0
            
        if len(losing_trades) > 0:
            metrics['avg_loss'] = losing_trades['pnl'].mean()
            metrics['max_loss'] = losing_trades['pnl'].min()
        else:
            metrics['avg_loss'] = 0
            metrics['max_loss'] = 0
        
        # Profit Factor
        total_wins = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
        total_losses = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0
        
        if total_losses > 0:
            metrics['profit_factor'] = total_wins / total_losses
        else:
            metrics['profit_factor'] = np.inf if total_wins > 0 else 0
        
        # Risk/Reward Ratio
        if metrics['avg_loss'] != 0:
            metrics['risk_reward_ratio'] = abs(metrics['avg_win'] / metrics['avg_loss'])
        else:
            metrics['risk_reward_ratio'] = np.inf if metrics['avg_win'] > 0 else 0
        
        # Equity Curve
        self.trades_df['cumulative_pnl'] = self.trades_df['pnl'].cumsum()
        self.trades_df['equity'] = self.initial_capital + self.trades_df['cumulative_pnl']
        
        # Return Metrics
        metrics['total_return'] = (metrics['total_pnl'] / self.initial_capital) * 100
        metrics['avg_return_per_trade'] = self.trades_df['return_pct'].mean()
        
        # Drawdown Analysis
        running_max = self.trades_df['equity'].expanding().max()
        drawdown = (self.trades_df['equity'] - running_max) / running_max * 100
        metrics['max_drawdown'] = drawdown.min()
        
        # Calculate consecutive wins/losses
        self.trades_df['is_win'] = self.trades_df['pnl'] > 0
        self.trades_df['streak'] = (self.trades_df['is_win'] != 
                                     self.trades_df['is_win'].shift()).cumsum()
        
        win_streaks = self.trades_df[self.trades_df['is_win']].groupby('streak').size()
        loss_streaks = self.trades_df[~self.trades_df['is_win']].groupby('streak').size()
        
        metrics['max_consecutive_wins'] = win_streaks.max() if len(win_streaks) > 0 else 0
        metrics['max_consecutive_losses'] = loss_streaks.max() if len(loss_streaks) > 0 else 0
        
        # Sharpe Ratio (annualized, assuming 252 trading days)
        if len(self.trades_df) > 1 and self.trades_df['return_pct'].std() > 0:
            metrics['sharpe_ratio'] = (self.trades_df['return_pct'].mean() / 
                                       self.trades_df['return_pct'].std()) * np.sqrt(252)
        else:
            metrics['sharpe_ratio'] = 0
        
        # Exit Reason Analysis
        exit_reasons = self.trades_df['exit_reason'].value_counts()
        metrics['tp_exits'] = exit_reasons.get('TP', 0)
        metrics['sl_exits'] = exit_reasons.get('SL', 0)
        metrics['eod_exits'] = exit_reasons.get('EOD', 0)
        
        # Direction Analysis
        long_trades = self.trades_df[self.trades_df['direction'] == 'Long']
        short_trades = self.trades_df[self.trades_df['direction'] == 'Short']
        
        metrics['long_trades'] = len(long_trades)
        metrics['short_trades'] = len(short_trades)
        
        if len(long_trades) > 0:
            metrics['long_win_rate'] = (len(long_trades[long_trades['pnl'] > 0]) / 
                                        len(long_trades)) * 100
            metrics['long_pnl'] = long_trades['pnl'].sum()
        else:
            metrics['long_win_rate'] = 0
            metrics['long_pnl'] = 0
            
        if len(short_trades) > 0:
            metrics['short_win_rate'] = (len(short_trades[short_trades['pnl'] > 0]) / 
                                         len(short_trades)) * 100
            metrics['short_pnl'] = short_trades['pnl'].sum()
        else:
            metrics['short_win_rate'] = 0
            metrics['short_pnl'] = 0
        
        return metrics
    
    def _empty_metrics(self):
        """Return empty metrics when no trades"""
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'breakeven_trades': 0,
            'win_rate': 0,
            'total_pnl': 0,
            'avg_pnl': 0,
            'median_pnl': 0,
            'std_pnl': 0,
            'avg_win': 0,
            'max_win': 0,
            'avg_loss': 0,
            'max_loss': 0,
            'profit_factor': 0,
            'risk_reward_ratio': 0,
            'total_return': 0,
            'avg_return_per_trade': 0,
            'max_drawdown': 0,
            'max_consecutive_wins': 0,
            'max_consecutive_losses': 0,
            'sharpe_ratio': 0,
            'tp_exits': 0,
            'sl_exits': 0,
            'eod_exits': 0,
            'long_trades': 0,
            'short_trades': 0,
            'long_win_rate': 0,
            'long_pnl': 0,
            'short_win_rate': 0,
            'short_pnl': 0,
        }
    
    def get_monthly_performance(self):
        """
        Calculate monthly performance
        
        Returns:
        --------
        pd.DataFrame
            Monthly performance statistics
        """
        if len(self.trades_df) == 0:
            return pd.DataFrame()
        
        df = self.trades_df.copy()
        df['year_month'] = pd.to_datetime(df['entry_time']).dt.to_period('M')
        
        monthly = df.groupby('year_month').agg({
            'pnl': ['sum', 'count', 'mean'],
            'return_pct': 'mean'
        }).round(2)
        
        monthly.columns = ['total_pnl', 'num_trades', 'avg_pnl', 'avg_return_pct']
        
        # Calculate win rate per month
        wins_per_month = df[df['pnl'] > 0].groupby('year_month').size()
        monthly['win_rate'] = (wins_per_month / monthly['num_trades'] * 100).fillna(0).round(2)
        
        return monthly
    
    def get_yearly_performance(self):
        """
        Calculate yearly performance
        
        Returns:
        --------
        pd.DataFrame
            Yearly performance statistics
        """
        if len(self.trades_df) == 0:
            return pd.DataFrame()
        
        df = self.trades_df.copy()
        df['year'] = pd.to_datetime(df['entry_time']).dt.year
        
        yearly = df.groupby('year').agg({
            'pnl': ['sum', 'count', 'mean'],
            'return_pct': 'mean'
        }).round(2)
        
        yearly.columns = ['total_pnl', 'num_trades', 'avg_pnl', 'avg_return_pct']
        
        # Calculate win rate per year
        wins_per_year = df[df['pnl'] > 0].groupby('year').size()
        yearly['win_rate'] = (wins_per_year / yearly['num_trades'] * 100).fillna(0).round(2)
        
        return yearly
