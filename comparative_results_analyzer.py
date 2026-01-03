"""
Comparative Results Analyzer
Analyzes and compares performance of three risk management strategies
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from collections import defaultdict


class ComparativeResultsAnalyzer:
    """Analyzes and compares results from three strategies"""
    
    def __init__(self, results: Dict):
        """
        Args:
            results: Dictionary with results from all three strategies
        """
        self.results_a = results['strategy_a']
        self.results_b = [r for r in results['strategy_b'] if not r.skipped]
        self.results_b_all = results['strategy_b']
        self.results_c = results['strategy_c']
        self.entry_signals = results['entry_signals']
    
    def calculate_strategy_metrics(self, results: List, strategy_name: str) -> Dict:
        """Calculate metrics for a strategy"""
        
        if not results:
            return {
                'strategy': strategy_name,
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_drawdown': 0.0,
                'avg_duration_minutes': 0.0
            }
        
        # Extract PnL based on strategy type
        if strategy_name == 'Strategy A':
            pnls = [r.pnl for r in results]
            durations = [r.duration_minutes for r in results]
        elif strategy_name == 'Strategy B':
            pnls = [r.pnl for r in results]
            durations = [r.duration_minutes for r in results]
        else:  # Strategy C
            pnls = [r.total_pnl for r in results]
            durations = [r.duration_minutes for r in results]
        
        # Calculate metrics
        winning_pnls = [p for p in pnls if p > 0]
        losing_pnls = [p for p in pnls if p <= 0]
        
        total_wins = sum(winning_pnls)
        total_losses = abs(sum(losing_pnls))
        
        # Calculate drawdown
        cumulative = 0
        peak = 0
        max_dd = 0
        
        for pnl in pnls:
            cumulative += pnl
            if cumulative > peak:
                peak = cumulative
            dd = peak - cumulative
            if dd > max_dd:
                max_dd = dd
        
        return {
            'strategy': strategy_name,
            'total_trades': len(results),
            'winning_trades': len(winning_pnls),
            'losing_trades': len(losing_pnls),
            'win_rate': (len(winning_pnls) / len(results) * 100) if results else 0,
            'total_pnl': sum(pnls),
            'avg_win': np.mean(winning_pnls) if winning_pnls else 0,
            'avg_loss': np.mean(losing_pnls) if losing_pnls else 0,
            'profit_factor': (total_wins / total_losses) if total_losses > 0 else float('inf') if total_wins > 0 else 0,
            'max_drawdown': max_dd,
            'avg_duration_minutes': np.mean(durations) if durations else 0
        }
    
    def generate_comparison_table(self) -> pd.DataFrame:
        """Generate comparison table for all three strategies"""
        
        metrics_a = self.calculate_strategy_metrics(self.results_a, 'Strategy A')
        metrics_b = self.calculate_strategy_metrics(self.results_b, 'Strategy B')
        metrics_c = self.calculate_strategy_metrics(self.results_c, 'Strategy C')
        
        # Create comparison dataframe
        comparison = pd.DataFrame([metrics_a, metrics_b, metrics_c])
        
        return comparison
    
    def generate_detailed_report(self) -> str:
        """Generate detailed comparison report"""
        
        report = []
        report.append("=" * 80)
        report.append("COMPARATIVE RISK MANAGEMENT STRATEGIES - BACKTEST RESULTS")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        report.append("STRATEGY DESCRIPTIONS")
        report.append("-" * 80)
        report.append("")
        report.append("Strategy A: 'Scalper Fixe' (Mécanique)")
        report.append("  • SL: 20 points fixed")
        report.append("  • TP: 25 points fixed (single exit)")
        report.append("  • No breakeven management")
        report.append("")
        report.append("Strategy B: 'ICT Liquidité Range' (Structurelle)")
        report.append("  • SL: 2 points beyond signal candle's low/high")
        report.append("  • TP: Opposite side of 08:30 opening range")
        report.append("  • Skip trade if TP distance < 10 points")
        report.append("")
        report.append("Strategy C: 'Standard Deviation' (Expansion Volatilité)")
        report.append("  • SL: 20 points fixed")
        report.append("  • TP1: 2x H_Range (50% position)")
        report.append("  • TP2: 4x H_Range (50% position)")
        report.append("  • Move SL to breakeven after TP1 hit")
        report.append("")
        report.append("=" * 80)
        report.append("")
        
        # Entry signals summary
        report.append(f"Total Entry Signals Found: {len(self.entry_signals)}")
        report.append("")
        
        # Strategy B skips
        skipped_count = len([r for r in self.results_b_all if r.skipped])
        if skipped_count > 0:
            report.append(f"Strategy B Skipped Trades: {skipped_count} (R:R insufficient)")
            report.append("")
        
        # Get metrics
        comp_table = self.generate_comparison_table()
        
        # Format table
        report.append("PERFORMANCE COMPARISON")
        report.append("-" * 80)
        report.append("")
        
        # Header
        report.append(f"{'Metric':<30} {'Strategy A':<20} {'Strategy B':<20} {'Strategy C':<20}")
        report.append("-" * 90)
        
        # Metrics rows
        report.append(f"{'Total Trades':<30} {comp_table.iloc[0]['total_trades']:<20.0f} {comp_table.iloc[1]['total_trades']:<20.0f} {comp_table.iloc[2]['total_trades']:<20.0f}")
        report.append(f"{'Win Rate (%)':<30} {comp_table.iloc[0]['win_rate']:<20.2f} {comp_table.iloc[1]['win_rate']:<20.2f} {comp_table.iloc[2]['win_rate']:<20.2f}")
        report.append(f"{'Profit Factor':<30} {comp_table.iloc[0]['profit_factor']:<20.2f} {comp_table.iloc[1]['profit_factor']:<20.2f} {comp_table.iloc[2]['profit_factor']:<20.2f}")
        report.append(f"{'Total Net Profit (pts)':<30} {comp_table.iloc[0]['total_pnl']:<20.2f} {comp_table.iloc[1]['total_pnl']:<20.2f} {comp_table.iloc[2]['total_pnl']:<20.2f}")
        report.append(f"{'Avg Trade Duration (min)':<30} {comp_table.iloc[0]['avg_duration_minutes']:<20.1f} {comp_table.iloc[1]['avg_duration_minutes']:<20.1f} {comp_table.iloc[2]['avg_duration_minutes']:<20.1f}")
        report.append(f"{'Max Drawdown (pts)':<30} {comp_table.iloc[0]['max_drawdown']:<20.2f} {comp_table.iloc[1]['max_drawdown']:<20.2f} {comp_table.iloc[2]['max_drawdown']:<20.2f}")
        report.append("")
        
        # Detailed breakdown
        report.append("DETAILED BREAKDOWN")
        report.append("-" * 80)
        report.append("")
        
        for idx, strategy in enumerate(['Strategy A', 'Strategy B', 'Strategy C']):
            metrics = comp_table.iloc[idx]
            report.append(f"{strategy}:")
            report.append(f"  Winning Trades:    {metrics['winning_trades']:.0f}")
            report.append(f"  Losing Trades:     {metrics['losing_trades']:.0f}")
            report.append(f"  Average Win:       {metrics['avg_win']:.2f} points")
            report.append(f"  Average Loss:      {metrics['avg_loss']:.2f} points")
            report.append("")
        
        # Ranking
        report.append("=" * 80)
        report.append("STRATEGY RANKING")
        report.append("-" * 80)
        report.append("")
        
        # Rank by total PnL
        sorted_by_pnl = comp_table.sort_values('total_pnl', ascending=False)
        report.append("By Total Net Profit:")
        for i, row in enumerate(sorted_by_pnl.itertuples(), 1):
            report.append(f"  {i}. {row.strategy}: {row.total_pnl:+.2f} points")
        report.append("")
        
        # Rank by win rate
        sorted_by_wr = comp_table.sort_values('win_rate', ascending=False)
        report.append("By Win Rate:")
        for i, row in enumerate(sorted_by_wr.itertuples(), 1):
            report.append(f"  {i}. {row.strategy}: {row.win_rate:.2f}%")
        report.append("")
        
        # Rank by profit factor
        sorted_by_pf = comp_table.sort_values('profit_factor', ascending=False)
        report.append("By Profit Factor:")
        for i, row in enumerate(sorted_by_pf.itertuples(), 1):
            pf_str = f"{row.profit_factor:.2f}" if row.profit_factor != float('inf') else "∞"
            report.append(f"  {i}. {row.strategy}: {pf_str}")
        report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def export_to_csv(self, filename: str):
        """Export detailed results to CSV"""
        
        all_trades = []
        
        # Strategy A
        for i, result in enumerate(self.results_a):
            all_trades.append({
                'strategy': 'A',
                'trade_num': i + 1,
                'entry_price': result.entry_price,
                'stop_loss': result.stop_loss,
                'take_profit': result.take_profit,
                'exit_price': result.exit_price,
                'exit_reason': result.exit_reason,
                'pnl': result.pnl,
                'duration_minutes': result.duration_minutes
            })
        
        # Strategy B
        for i, result in enumerate(self.results_b):
            all_trades.append({
                'strategy': 'B',
                'trade_num': i + 1,
                'entry_price': result.entry_price,
                'stop_loss': result.stop_loss,
                'take_profit': result.take_profit,
                'exit_price': result.exit_price,
                'exit_reason': result.exit_reason,
                'pnl': result.pnl,
                'duration_minutes': result.duration_minutes
            })
        
        # Strategy C
        for i, result in enumerate(self.results_c):
            all_trades.append({
                'strategy': 'C',
                'trade_num': i + 1,
                'entry_price': result.entry_price,
                'stop_loss': result.stop_loss,
                'take_profit_1': result.take_profit_1,
                'take_profit_2': result.take_profit_2,
                'exit_price_1': result.exit_price_1,
                'exit_price_2': result.exit_price_2,
                'exit_reason_1': result.exit_reason_1,
                'exit_reason_2': result.exit_reason_2,
                'pnl': result.total_pnl,
                'duration_minutes': result.duration_minutes,
                'breakeven_activated': result.breakeven_activated
            })
        
        df = pd.DataFrame(all_trades)
        df.to_csv(filename, index=False)
        print(f"Detailed trade results exported to {filename}")


if __name__ == "__main__":
    print("Comparative Results Analyzer Module")
