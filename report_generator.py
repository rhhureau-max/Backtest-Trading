"""
Report Generator Module
Generates comprehensive HTML and Markdown reports
"""

import pandas as pd
from datetime import datetime
import os


class ReportGenerator:
    """Generate comprehensive analysis reports"""
    
    def __init__(self, results_dict, output_dir='results'):
        """
        Parameters:
        -----------
        results_dict : dict
            Dictionary with timeframes as keys and (trades_df, metrics) tuples as values
        output_dir : str
            Directory to save reports
        """
        self.results = results_dict
        self.output_dir = output_dir
        
    def generate_markdown_report(self, filename='backtest_report.md'):
        """Generate comprehensive Markdown report"""
        
        report = []
        report.append("# FVG Trading Strategy Backtest Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("\n---\n")
        
        # Executive Summary
        report.append("## Executive Summary\n")
        report.append("This report presents the results of backtesting a Fair Value Gap (FVG) trading strategy ")
        report.append("across multiple timeframes from 2018 to 2024.\n")
        
        # Strategy Description
        report.append("## Strategy Description\n")
        report.append("### FVG Detection")
        report.append("- **Detection Time:** 8:30 AM daily")
        report.append("- **Bullish FVG:** Occurs when `candle[i-1].high < candle[i+1].low`")
        report.append("- **Bearish FVG:** Occurs when `candle[i-1].low > candle[i+1].high`\n")
        
        report.append("### Entry Rules")
        report.append("- **1-minute:** Enter at close of 8:31 candle")
        report.append("- **5-minute:** Enter at close of 8:35 candle")
        report.append("- **15-minute:** Enter at close of 8:45 candle\n")
        
        report.append("### Exit Rules")
        report.append("- **Stop Loss (SL):** Middle of FVG gap")
        report.append("- **Take Profit (TP):** 2:1 risk/reward ratio")
        report.append("- **End of Day (EOD):** Close any open positions\n")
        
        report.append("---\n")
        
        # Performance Comparison Table
        report.append("## Performance Comparison Across Timeframes\n")
        
        comparison_data = []
        for tf in ['1m', '5m', '15m']:
            if tf in self.results:
                metrics = self.results[tf]['metrics']
                comparison_data.append({
                    'Timeframe': tf,
                    'Total Trades': metrics['total_trades'],
                    'Win Rate (%)': f"{metrics['win_rate']:.2f}",
                    'Total Return (%)': f"{metrics['total_return']:.2f}",
                    'Profit Factor': f"{metrics['profit_factor']:.2f}",
                    'Sharpe Ratio': f"{metrics['sharpe_ratio']:.2f}",
                    'Max Drawdown (%)': f"{metrics['max_drawdown']:.2f}",
                    'Avg Win ($)': f"{metrics['avg_win']:.2f}",
                    'Avg Loss ($)': f"{metrics['avg_loss']:.2f}",
                })
        
        if comparison_data:
            df_comparison = pd.DataFrame(comparison_data)
            report.append(df_comparison.to_markdown(index=False))
            report.append("\n")
        
        # Detailed Results by Timeframe
        report.append("---\n")
        report.append("## Detailed Results by Timeframe\n")
        
        for tf in ['1m', '5m', '15m']:
            if tf not in self.results:
                continue
                
            trades_df = self.results[tf]['trades_df']
            metrics = self.results[tf]['metrics']
            
            report.append(f"\n### {tf.upper()} Timeframe\n")
            
            # Overall Statistics
            report.append("#### Overall Statistics\n")
            report.append(f"- **Total Trades:** {metrics['total_trades']}")
            report.append(f"- **Winning Trades:** {metrics['winning_trades']}")
            report.append(f"- **Losing Trades:** {metrics['losing_trades']}")
            report.append(f"- **Win Rate:** {metrics['win_rate']:.2f}%")
            report.append(f"- **Total P&L:** ${metrics['total_pnl']:.2f}")
            report.append(f"- **Total Return:** {metrics['total_return']:.2f}%\n")
            
            # Risk Metrics
            report.append("#### Risk Metrics\n")
            report.append(f"- **Max Drawdown:** {metrics['max_drawdown']:.2f}%")
            report.append(f"- **Sharpe Ratio:** {metrics['sharpe_ratio']:.2f}")
            report.append(f"- **Max Consecutive Wins:** {metrics['max_consecutive_wins']}")
            report.append(f"- **Max Consecutive Losses:** {metrics['max_consecutive_losses']}\n")
            
            # Win/Loss Analysis
            report.append("#### Win/Loss Analysis\n")
            report.append(f"- **Average Win:** ${metrics['avg_win']:.2f}")
            report.append(f"- **Average Loss:** ${metrics['avg_loss']:.2f}")
            report.append(f"- **Max Win:** ${metrics['max_win']:.2f}")
            report.append(f"- **Max Loss:** ${metrics['max_loss']:.2f}")
            report.append(f"- **Profit Factor:** {metrics['profit_factor']:.2f}")
            report.append(f"- **Risk/Reward Ratio:** {metrics['risk_reward_ratio']:.2f}\n")
            
            # Exit Analysis
            report.append("#### Exit Analysis\n")
            report.append(f"- **Take Profit Exits:** {metrics['tp_exits']} ({metrics['tp_exits']/metrics['total_trades']*100:.1f}%)")
            report.append(f"- **Stop Loss Exits:** {metrics['sl_exits']} ({metrics['sl_exits']/metrics['total_trades']*100:.1f}%)")
            report.append(f"- **End of Day Exits:** {metrics['eod_exits']} ({metrics['eod_exits']/metrics['total_trades']*100:.1f}%)\n")
            
            # Direction Analysis
            report.append("#### Direction Analysis\n")
            report.append(f"- **Long Trades:** {metrics['long_trades']}")
            report.append(f"  - Win Rate: {metrics['long_win_rate']:.2f}%")
            report.append(f"  - Total P&L: ${metrics['long_pnl']:.2f}")
            report.append(f"- **Short Trades:** {metrics['short_trades']}")
            report.append(f"  - Win Rate: {metrics['short_win_rate']:.2f}%")
            report.append(f"  - Total P&L: ${metrics['short_pnl']:.2f}\n")
            
            # Yearly Performance
            if len(trades_df) > 0:
                report.append("#### Yearly Performance\n")
                from performance_metrics import PerformanceMetrics
                pm = PerformanceMetrics(trades_df)
                yearly = pm.get_yearly_performance()
                if not yearly.empty:
                    report.append(yearly.to_markdown())
                    report.append("\n")
            
            # Visualizations
            report.append("#### Visualizations\n")
            report.append(f"![Equity Curve]({self.output_dir}/equity_curve_{tf}.png)\n")
            report.append(f"![Drawdown]({self.output_dir}/drawdown_{tf}.png)\n")
            report.append(f"![Trade Distribution]({self.output_dir}/trade_distribution_{tf}.png)\n")
            report.append(f"![Performance Heatmap]({self.output_dir}/performance_heatmap_{tf}.png)\n")
            
            report.append("---\n")
        
        # Best Performing Periods Analysis
        report.append("## Best Performing Periods\n")
        
        for tf in ['1m', '5m', '15m']:
            if tf not in self.results or len(self.results[tf]['trades_df']) == 0:
                continue
                
            trades_df = self.results[tf]['trades_df']
            
            report.append(f"\n### {tf.upper()} Timeframe\n")
            
            # Best year
            df_copy = trades_df.copy()
            df_copy['year'] = pd.to_datetime(df_copy['entry_time']).dt.year
            yearly_pnl = df_copy.groupby('year')['pnl'].sum()
            best_year = yearly_pnl.idxmax()
            best_year_pnl = yearly_pnl.max()
            
            report.append(f"- **Best Year:** {best_year} (P&L: ${best_year_pnl:.2f})")
            
            # Worst year
            worst_year = yearly_pnl.idxmin()
            worst_year_pnl = yearly_pnl.min()
            report.append(f"- **Worst Year:** {worst_year} (P&L: ${worst_year_pnl:.2f})")
            
            # Best month
            df_copy['year_month'] = pd.to_datetime(df_copy['entry_time']).dt.to_period('M')
            monthly_pnl = df_copy.groupby('year_month')['pnl'].sum()
            best_month = monthly_pnl.idxmax()
            best_month_pnl = monthly_pnl.max()
            
            report.append(f"- **Best Month:** {best_month} (P&L: ${best_month_pnl:.2f})\n")
        
        # Strategy Robustness Evaluation
        report.append("---\n")
        report.append("## Strategy Robustness Evaluation\n")
        
        report.append("### Key Findings\n")
        
        # Find best timeframe
        best_tf = None
        best_return = float('-inf')
        for tf in ['1m', '5m', '15m']:
            if tf in self.results:
                total_return = self.results[tf]['metrics']['total_return']
                if total_return > best_return:
                    best_return = total_return
                    best_tf = tf
        
        if best_tf:
            report.append(f"- **Best Performing Timeframe:** {best_tf.upper()} with {best_return:.2f}% total return")
        
        # Consistency analysis
        report.append("\n### Consistency Analysis\n")
        for tf in ['1m', '5m', '15m']:
            if tf in self.results:
                metrics = self.results[tf]['metrics']
                win_rate = metrics['win_rate']
                profit_factor = metrics['profit_factor']
                sharpe = metrics['sharpe_ratio']
                
                consistency_score = 0
                if win_rate >= 50:
                    consistency_score += 1
                if profit_factor >= 1.5:
                    consistency_score += 1
                if sharpe >= 1.0:
                    consistency_score += 1
                
                report.append(f"- **{tf.upper()}:** Consistency Score {consistency_score}/3")
                if consistency_score >= 2:
                    report.append(f"  - ✅ Shows good consistency")
                else:
                    report.append(f"  - ⚠️ Shows moderate consistency")
        
        report.append("\n### Recommendations\n")
        report.append("Based on the 7-year backtest analysis:\n")
        
        # Generate recommendations based on results
        for tf in ['1m', '5m', '15m']:
            if tf in self.results:
                metrics = self.results[tf]['metrics']
                if metrics['win_rate'] >= 50 and metrics['profit_factor'] >= 1.5:
                    report.append(f"- **{tf.upper()}:** Strategy shows promise with positive expectancy")
                elif metrics['win_rate'] >= 40:
                    report.append(f"- **{tf.upper()}:** Strategy needs optimization to improve win rate")
                else:
                    report.append(f"- **{tf.upper()}:** Strategy requires significant adjustments")
        
        report.append("\n### Risk Considerations\n")
        report.append("- Monitor maximum drawdown periods carefully")
        report.append("- Consider position sizing based on account risk tolerance")
        report.append("- Be aware of consecutive losing streaks")
        report.append("- Backtest results may not guarantee future performance\n")
        
        # Footer
        report.append("---\n")
        report.append("*End of Report*\n")
        
        # Save report
        report_path = os.path.join(self.output_dir, filename)
        with open(report_path, 'w') as f:
            f.write('\n'.join(report))
        
        print(f"\nMarkdown report saved to: {report_path}")
        return report_path
    
    def generate_html_report(self, filename='backtest_report.html'):
        """Generate HTML report from markdown"""
        
        # Generate markdown first
        md_file = self.generate_markdown_report()
        
        # Read markdown content
        with open(md_file, 'r') as f:
            md_content = f.read()
        
        # Simple HTML wrapper (for basic conversion)
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>FVG Trading Strategy Backtest Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        hr {{
            border: none;
            border-top: 2px solid #3498db;
            margin: 30px 0;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <pre style="white-space: pre-wrap;">{md_content}</pre>
</body>
</html>
"""
        
        html_path = os.path.join(self.output_dir, filename)
        with open(html_path, 'w') as f:
            f.write(html)
        
        print(f"HTML report saved to: {html_path}")
        return html_path
