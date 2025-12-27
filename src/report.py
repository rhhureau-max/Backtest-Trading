"""
Generate comparison reports for strategy performance.
"""

import pandas as pd
from typing import List, Dict
from performance import PerformanceMetrics
from strategies.base_strategy import BaseStrategy


class StrategyReport:
    """
    Generate comprehensive reports comparing multiple strategies.
    """
    
    def __init__(self, strategies: List[BaseStrategy]):
        self.strategies = strategies
    
    def generate_comparison_report(self) -> pd.DataFrame:
        """
        Generate comparison report for all strategies.
        
        Returns:
            DataFrame with comparison metrics
        """
        comparison_data = []
        
        for strategy in self.strategies:
            metrics_calculator = PerformanceMetrics(strategy.trades)
            metrics = metrics_calculator.calculate_all_metrics()
            
            comparison_data.append({
                'Strategy': strategy.name,
                'Total Trades': metrics['total_trades'],
                'Win Rate (%)': round(metrics['win_rate'], 2),
                'Total PnL': round(metrics['total_pnl'], 2),
                'Average Win': round(metrics['average_win'], 2),
                'Average Loss': round(metrics['average_loss'], 2),
                'Profit Factor': round(metrics['profit_factor'], 2) if metrics['profit_factor'] != float('inf') else 'Inf',
                'Max Drawdown': round(metrics['max_drawdown'], 2),
                'Sharpe Ratio': round(metrics['sharpe_ratio'], 2),
                'Total Return': round(metrics['total_return'], 2)
            })
        
        return pd.DataFrame(comparison_data)
    
    def generate_detailed_report(self, strategy_name: str) -> Dict:
        """
        Generate detailed report for a specific strategy.
        
        Args:
            strategy_name: Name of the strategy
        
        Returns:
            Dictionary with detailed metrics
        """
        strategy = next((s for s in self.strategies if s.name == strategy_name), None)
        
        if strategy is None:
            return {}
        
        metrics_calculator = PerformanceMetrics(strategy.trades)
        metrics = metrics_calculator.calculate_all_metrics()
        distribution = metrics_calculator.get_trade_distribution()
        monthly = metrics_calculator.get_monthly_performance()
        
        return {
            'metrics': metrics,
            'distribution': distribution,
            'monthly': monthly
        }
    
    def print_comparison_report(self):
        """
        Print comparison report to console.
        """
        print("\n" + "="*80)
        print("STRATEGY COMPARISON REPORT")
        print("="*80)
        
        comparison_df = self.generate_comparison_report()
        print(comparison_df.to_string(index=False))
        
        print("\n" + "="*80)
        print("BEST PERFORMING STRATEGY")
        print("="*80)
        
        # Determine best strategy by different metrics
        if not comparison_df.empty:
            best_pnl = comparison_df.loc[comparison_df['Total PnL'].idxmax(), 'Strategy']
            best_win_rate = comparison_df.loc[comparison_df['Win Rate (%)'].idxmax(), 'Strategy']
            best_sharpe = comparison_df.loc[comparison_df['Sharpe Ratio'].idxmax(), 'Strategy']
            
            print(f"  Highest Total PnL: {best_pnl}")
            print(f"  Highest Win Rate: {best_win_rate}")
            print(f"  Highest Sharpe Ratio: {best_sharpe}")
        
        print("\n")
    
    def print_detailed_report(self, strategy_name: str):
        """
        Print detailed report for a specific strategy.
        
        Args:
            strategy_name: Name of the strategy
        """
        print("\n" + "="*80)
        print(f"DETAILED REPORT: {strategy_name}")
        print("="*80)
        
        report = self.generate_detailed_report(strategy_name)
        
        if not report:
            print(f"Strategy '{strategy_name}' not found.")
            return
        
        # Print metrics
        print("\nPERFORMANCE METRICS:")
        print("-"*80)
        metrics = report['metrics']
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Print trade distribution
        print("\nTRADE DISTRIBUTION:")
        print("-"*80)
        distribution = report['distribution']
        for key, value in distribution.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Print monthly performance
        print("\nMONTHLY PERFORMANCE:")
        print("-"*80)
        monthly = report['monthly']
        if not monthly.empty:
            print(monthly.to_string())
        else:
            print("  No data available")
        
        print("\n")
    
    def generate_kpi_recommendations(self) -> str:
        """
        Generate KPI recommendations for validating trailing stop effectiveness.
        
        Returns:
            String with recommendations
        """
        recommendations = """
KPI RECOMMENDATIONS FOR TRAILING STOP VALIDATION
=================================================

To validate whether the trailing stop (Strategy C) is superior to fixed TP approaches:

1. SHARPE RATIO COMPARISON
   - Strategy C should have a higher Sharpe Ratio if it effectively captures trends
   - Compare against Strategies A & B to see risk-adjusted returns
   - Target: Sharpe > 1.5 for meaningful outperformance

2. AVERAGE WIN SIZE
   - Trailing stops should capture larger wins during strong trends
   - Compare avg_win of Strategy C vs. Strategies A & B
   - Target: 30-50% higher average win than fixed TP strategies

3. PROFIT FACTOR
   - Higher profit factor indicates better risk/reward management
   - Target: Profit Factor > 1.5 for sustainable strategy
   - Compare across all three strategies

4. WIN RATE vs. REWARD ANALYSIS
   - Strategy C may have lower win rate but higher reward per win
   - Calculate: (Win Rate * Avg Win) / |Avg Loss|
   - Target: Ratio > 2.0 indicates good risk management

5. MAXIMUM DRAWDOWN
   - Trailing stops should protect capital during reversals
   - Strategy C should have comparable or lower drawdown than fixed TP
   - Target: Max DD < 25% of Total PnL

6. MARKET CONDITION ANALYSIS
   - Trailing stops perform better in trending markets
   - Analyze monthly performance to identify optimal market conditions
   - Consider: Are there specific months/years where Strategy C outperforms?

7. TRADE DURATION
   - Trailing stops typically hold trades longer
   - Compare average holding period across strategies
   - Target: Longer trades with proportionally higher returns

RECOMMENDATION CRITERIA:
- If Strategy C has: Higher Sharpe + Higher Avg Win + Reasonable Max DD
  → Trailing stop is superior
- If Strategy C has: Lower Win Rate but significantly higher Avg Win
  → Trailing stop captures trends effectively
- If Strategy C has: Similar/worse metrics across the board
  → Fixed TP strategies are more suitable for this market

IMPLEMENTATION SUGGESTIONS:
- Consider hybrid approach: Use trailing stop only in strong trending conditions
- Test different EMA periods (5, 9, 13, 21) for optimal trailing stop
- Implement regime filter to switch between fixed TP and trailing stop
"""
        return recommendations
