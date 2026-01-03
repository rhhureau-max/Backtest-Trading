"""
Results Analyzer Module
Generates comprehensive performance reports and analytics
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from collections import defaultdict


class ResultsAnalyzer:
    """Analyzes backtest results and generates reports"""
    
    def __init__(self, trades: List):
        """
        Args:
            trades: List of Trade objects
        """
        self.trades = trades
        self.closed_trades = [t for t in trades if t.is_fully_closed()]
    
    def calculate_drawdown(self, equity_curve: List[float]) -> Dict:
        """
        Calculate maximum drawdown
        
        Args:
            equity_curve: List of cumulative PnL values
            
        Returns:
            Dictionary with drawdown metrics
        """
        if not equity_curve:
            return {'max_drawdown': 0, 'max_drawdown_pct': 0}
        
        cumulative = np.array(equity_curve)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = running_max - cumulative
        max_dd = np.max(drawdown)
        
        # Calculate percentage drawdown
        max_equity = np.max(cumulative) if np.max(cumulative) > 0 else 1
        max_dd_pct = (max_dd / max_equity) * 100 if max_equity > 0 else 0
        
        return {
            'max_drawdown': max_dd,
            'max_drawdown_pct': max_dd_pct
        }
    
    def get_equity_curve(self) -> List[float]:
        """Get cumulative PnL equity curve"""
        equity = []
        cumulative = 0
        
        # Use entry_time attribute which exists in both old and new Trade objects
        for trade in sorted(self.closed_trades, key=lambda t: t.entry_time):
            cumulative += trade.get_total_pnl()
            equity.append(cumulative)
        
        return equity
    
    def get_overall_metrics(self) -> Dict:
        """Calculate overall performance metrics"""
        if not self.closed_trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0,
                'max_drawdown_pct': 0.0
            }
        
        winning_trades = [t for t in self.closed_trades if t.get_total_pnl() > 0]
        losing_trades = [t for t in self.closed_trades if t.get_total_pnl() <= 0]
        
        total_wins = sum(t.get_total_pnl() for t in winning_trades)
        total_losses = abs(sum(t.get_total_pnl() for t in losing_trades))
        
        equity_curve = self.get_equity_curve()
        dd_metrics = self.calculate_drawdown(equity_curve)
        
        return {
            'total_trades': len(self.closed_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': len(winning_trades) / len(self.closed_trades) * 100 if self.closed_trades else 0,
            'total_pnl': sum(t.get_total_pnl() for t in self.closed_trades),
            'avg_win': total_wins / len(winning_trades) if winning_trades else 0,
            'avg_loss': total_losses / len(losing_trades) if losing_trades else 0,
            'profit_factor': total_wins / total_losses if total_losses > 0 else float('inf'),
            'max_drawdown': dd_metrics['max_drawdown'],
            'max_drawdown_pct': dd_metrics['max_drawdown_pct']
        }
    
    def get_yearly_metrics(self) -> Dict[int, Dict]:
        """Calculate performance metrics by year"""
        yearly_trades = defaultdict(list)
        
        for trade in self.closed_trades:
            year = trade.entry_time.year
            yearly_trades[year].append(trade)
        
        yearly_metrics = {}
        
        for year, trades in sorted(yearly_trades.items()):
            winning = [t for t in trades if t.get_total_pnl() > 0]
            losing = [t for t in trades if t.get_total_pnl() <= 0]
            
            total_wins = sum(t.get_total_pnl() for t in winning)
            total_losses = abs(sum(t.get_total_pnl() for t in losing))
            
            yearly_metrics[year] = {
                'total_trades': len(trades),
                'winning_trades': len(winning),
                'losing_trades': len(losing),
                'win_rate': len(winning) / len(trades) * 100 if trades else 0,
                'total_pnl': sum(t.get_total_pnl() for t in trades),
                'avg_win': total_wins / len(winning) if winning else 0,
                'avg_loss': total_losses / len(losing) if losing else 0,
                'profit_factor': total_wins / total_losses if total_losses > 0 else float('inf')
            }
        
        return yearly_metrics
    
    def get_direction_metrics(self) -> Dict[str, Dict]:
        """Calculate performance metrics by direction (LONG vs SHORT)"""
        long_trades = [t for t in self.closed_trades if t.direction == 'LONG']
        short_trades = [t for t in self.closed_trades if t.direction == 'SHORT']
        
        metrics = {}
        
        for direction, trades in [('LONG', long_trades), ('SHORT', short_trades)]:
            if not trades:
                metrics[direction] = {
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'win_rate': 0.0,
                    'total_pnl': 0.0,
                    'avg_win': 0.0,
                    'avg_loss': 0.0,
                    'profit_factor': 0.0
                }
                continue
            
            winning = [t for t in trades if t.get_total_pnl() > 0]
            losing = [t for t in trades if t.get_total_pnl() <= 0]
            
            total_wins = sum(t.get_total_pnl() for t in winning)
            total_losses = abs(sum(t.get_total_pnl() for t in losing))
            
            metrics[direction] = {
                'total_trades': len(trades),
                'winning_trades': len(winning),
                'losing_trades': len(losing),
                'win_rate': len(winning) / len(trades) * 100 if trades else 0,
                'total_pnl': sum(t.get_total_pnl() for t in trades),
                'avg_win': total_wins / len(winning) if winning else 0,
                'avg_loss': total_losses / len(losing) if losing else 0,
                'profit_factor': total_wins / total_losses if total_losses > 0 else float('inf')
            }
        
        return metrics
    
    def generate_report(self) -> str:
        """Generate comprehensive text report"""
        report = []
        report.append("=" * 80)
        report.append("NQ ICT STRATEGY BACKTEST RESULTS")
        report.append("=" * 80)
        report.append("")
        
        # Overall metrics
        overall = self.get_overall_metrics()
        report.append("OVERALL PERFORMANCE")
        report.append("-" * 80)
        report.append(f"Total Trades:        {overall['total_trades']}")
        report.append(f"Winning Trades:      {overall['winning_trades']}")
        report.append(f"Losing Trades:       {overall['losing_trades']}")
        report.append(f"Win Rate:            {overall['win_rate']:.2f}%")
        report.append(f"Total PnL:           {overall['total_pnl']:.2f} points")
        report.append(f"Average Win:         {overall['avg_win']:.2f} points")
        report.append(f"Average Loss:        {overall['avg_loss']:.2f} points")
        
        if overall['profit_factor'] == float('inf'):
            report.append(f"Profit Factor:       ∞ (no losing trades)")
        else:
            report.append(f"Profit Factor:       {overall['profit_factor']:.2f}")
        
        report.append(f"Max Drawdown:        {overall['max_drawdown']:.2f} points ({overall['max_drawdown_pct']:.2f}%)")
        report.append("")
        
        # Yearly breakdown
        yearly = self.get_yearly_metrics()
        if yearly:
            report.append("YEARLY PERFORMANCE")
            report.append("-" * 80)
            report.append(f"{'Year':<6} {'Trades':<8} {'Win':<6} {'Loss':<6} {'WinRate':<10} {'PnL':<12} {'PF':<8}")
            report.append("-" * 80)
            
            for year in sorted(yearly.keys()):
                metrics = yearly[year]
                pf_str = f"{metrics['profit_factor']:.2f}" if metrics['profit_factor'] != float('inf') else "∞"
                report.append(
                    f"{year:<6} {metrics['total_trades']:<8} "
                    f"{metrics['winning_trades']:<6} {metrics['losing_trades']:<6} "
                    f"{metrics['win_rate']:<9.2f}% {metrics['total_pnl']:<11.2f} {pf_str:<8}"
                )
            report.append("")
        
        # Direction breakdown
        direction = self.get_direction_metrics()
        report.append("PERFORMANCE BY DIRECTION")
        report.append("-" * 80)
        
        for dir_name in ['LONG', 'SHORT']:
            metrics = direction[dir_name]
            report.append(f"\n{dir_name} Trades:")
            report.append(f"  Total Trades:      {metrics['total_trades']}")
            report.append(f"  Winning Trades:    {metrics['winning_trades']}")
            report.append(f"  Losing Trades:     {metrics['losing_trades']}")
            report.append(f"  Win Rate:          {metrics['win_rate']:.2f}%")
            report.append(f"  Total PnL:         {metrics['total_pnl']:.2f} points")
            report.append(f"  Average Win:       {metrics['avg_win']:.2f} points")
            report.append(f"  Average Loss:      {metrics['avg_loss']:.2f} points")
            
            if metrics['profit_factor'] == float('inf'):
                report.append(f"  Profit Factor:     ∞")
            else:
                report.append(f"  Profit Factor:     {metrics['profit_factor']:.2f}")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def export_to_csv(self, filename: str = "backtest_results.csv"):
        """Export trade details to CSV file"""
        trade_data = []
        
        for trade in self.closed_trades:
            for position in trade.positions:
                trade_data.append({
                    'trade_id': trade.trade_id,
                    'entry_time': trade.entry_time,
                    'direction': trade.direction,
                    'entry_price': trade.entry_price,
                    'tp_level': position.tp_level,
                    'stop_loss': position.stop_loss,
                    'take_profit': position.take_profit if position.take_profit else 'Runner',
                    'exit_time': position.exit_time,
                    'exit_price': position.exit_price,
                    'exit_reason': position.exit_reason,
                    'pnl': position.pnl,
                    'position_size': position.position_size
                })
        
        df = pd.DataFrame(trade_data)
        df.to_csv(filename, index=False)
        print(f"Trade details exported to {filename}")
        
        return df


if __name__ == "__main__":
    print("Results Analyzer module loaded successfully")
