"""
Report Generator Module for 8:30 Strategy Backtest

This module generates reports and visualizations for backtest results.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import os

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def generate_results_csv(results: List[Dict], output_path: str) -> None:
    """
    Generate CSV file with all backtest results.
    
    Args:
        results: List of result dictionaries
        output_path: Path to output CSV file
    """
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)
    print(f"Results saved to: {output_path}")


def generate_trades_csv(trades: pd.DataFrame, output_path: str) -> None:
    """
    Generate CSV file with individual trade logs.
    
    Args:
        trades: DataFrame with trade details
        output_path: Path to output CSV file
    """
    trades.to_csv(output_path, index=False)
    print(f"Trades log saved to: {output_path}")


def generate_win_rate_table(results: List[Dict], timeframe: str) -> str:
    """
    Generate a formatted table of win rates by SL type and RR.
    
    Args:
        results: List of result dictionaries
        timeframe: The timeframe to filter by
        
    Returns:
        Formatted table as string
    """
    # Filter results for this timeframe
    tf_results = [r for r in results if r['timeframe'] == timeframe]
    
    if not tf_results:
        return f"No results for timeframe: {timeframe}"
    
    # Get unique SL types and RR values
    sl_types = sorted(set(r['sl_type'] for r in tf_results))
    rr_values = sorted(set(r['rr'] for r in tf_results))
    
    # Create table header
    header = "| SL Type | " + " | ".join([f"RR {rr}" for rr in rr_values]) + " |"
    separator = "|" + "-" * 9 + "|" + "|".join(["-" * 8 for _ in rr_values]) + "|"
    
    lines = [header, separator]
    
    # Create rows
    for sl_type in sl_types:
        row_values = []
        for rr in rr_values:
            # Find matching result
            matching = [r for r in tf_results 
                       if r['sl_type'] == sl_type and r['rr'] == rr]
            if matching:
                win_rate = matching[0]['win_rate']
                row_values.append(f"{win_rate:.1f}%")
            else:
                row_values.append("N/A")
        
        row = f"| {sl_type:7} | " + " | ".join([f"{v:6}" for v in row_values]) + " |"
        lines.append(row)
    
    return "\n".join(lines)


def generate_markdown_report(results: List[Dict], trades: pd.DataFrame,
                             output_path: str) -> None:
    """
    Generate a comprehensive markdown report.
    
    Args:
        results: List of result dictionaries
        trades: DataFrame with trade details
        output_path: Path to output markdown file
    """
    lines = []
    
    # Header
    lines.append("# 8:30 Strategy Backtest Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    
    # Overall statistics
    df_results = pd.DataFrame(results)
    
    total_trades_analyzed = df_results['total_trades'].sum() if len(df_results) > 0 else 0
    unique_combinations = len(df_results)
    
    lines.append(f"- **Total combinations tested**: {unique_combinations}")
    lines.append(f"- **Timeframes analyzed**: 1m, 5m, 15m")
    lines.append(f"- **Period**: 2018-2025")
    lines.append("")
    
    # Best combinations
    lines.append("## Best Combinations by Win Rate")
    lines.append("")
    
    if len(df_results) > 0:
        best_combinations = df_results.nlargest(10, 'win_rate')[
            ['timeframe', 'sl_type', 'rr', 'win_rate', 'profit_factor', 
             'expectancy', 'total_trades']
        ]
        
        lines.append("| Timeframe | SL Type | RR | Win Rate | PF | Expectancy | Trades |")
        lines.append("|-----------|---------|-----|----------|-----|------------|--------|")
        
        for _, row in best_combinations.iterrows():
            pf = f"{row['profit_factor']:.2f}" if row['profit_factor'] != float('inf') else "∞"
            lines.append(
                f"| {row['timeframe']} | {row['sl_type']} | {row['rr']} | "
                f"{row['win_rate']:.1f}% | {pf} | {row['expectancy']:.2f} | "
                f"{row['total_trades']} |"
            )
    
    lines.append("")
    
    # Best by expectancy
    lines.append("## Best Combinations by Expectancy")
    lines.append("")
    
    if len(df_results) > 0:
        best_expectancy = df_results.nlargest(10, 'expectancy')[
            ['timeframe', 'sl_type', 'rr', 'win_rate', 'profit_factor', 
             'expectancy', 'total_trades']
        ]
        
        lines.append("| Timeframe | SL Type | RR | Win Rate | PF | Expectancy | Trades |")
        lines.append("|-----------|---------|-----|----------|-----|------------|--------|")
        
        for _, row in best_expectancy.iterrows():
            pf = f"{row['profit_factor']:.2f}" if row['profit_factor'] != float('inf') else "∞"
            lines.append(
                f"| {row['timeframe']} | {row['sl_type']} | {row['rr']} | "
                f"{row['win_rate']:.1f}% | {pf} | {row['expectancy']:.2f} | "
                f"{row['total_trades']} |"
            )
    
    lines.append("")
    
    # Tables by timeframe
    for tf in ['1m', '5m', '15m']:
        lines.append(f"## Results for Timeframe: {tf.upper()}")
        lines.append("")
        lines.append("### Win Rate Table")
        lines.append("```")
        lines.append(generate_win_rate_table(results, tf))
        lines.append("```")
        lines.append("")
    
    # Direction analysis
    lines.append("## Direction Analysis")
    lines.append("")
    
    if len(df_results) > 0:
        lines.append("| Timeframe | SL Type | RR | Long WR | Short WR | Long # | Short # |")
        lines.append("|-----------|---------|-----|---------|----------|--------|---------|")
        
        # Show a subset of results for direction analysis
        sample = df_results[df_results['rr'] == 2.0].head(15)
        
        for _, row in sample.iterrows():
            lines.append(
                f"| {row['timeframe']} | {row['sl_type']} | {row['rr']} | "
                f"{row['win_rate_long']:.1f}% | {row['win_rate_short']:.1f}% | "
                f"{row['num_long']} | {row['num_short']} |"
            )
    
    lines.append("")
    
    # Conclusions
    lines.append("## Observations and Conclusions")
    lines.append("")
    
    if len(df_results) > 0:
        best_wr = df_results.loc[df_results['win_rate'].idxmax()]
        best_exp = df_results.loc[df_results['expectancy'].idxmax()]
        
        lines.append(f"1. **Highest Win Rate**: {best_wr['win_rate']:.1f}% achieved with "
                    f"{best_wr['timeframe']} timeframe, {best_wr['sl_type']} SL, "
                    f"and RR {best_wr['rr']}")
        
        lines.append(f"2. **Best Expectancy**: {best_exp['expectancy']:.2f}R achieved with "
                    f"{best_exp['timeframe']} timeframe, {best_exp['sl_type']} SL, "
                    f"and RR {best_exp['rr']}")
        
        # Average by SL type
        avg_by_sl = df_results.groupby('sl_type')['win_rate'].mean()
        best_sl = avg_by_sl.idxmax()
        lines.append(f"3. **Most Consistent SL Type**: {best_sl} with average win rate "
                    f"of {avg_by_sl[best_sl]:.1f}%")
    
    lines.append("")
    lines.append("---")
    lines.append("*Report generated by 8:30 Strategy Backtest System*")
    
    # Write to file
    with open(output_path, 'w') as f:
        f.write("\n".join(lines))
    
    print(f"Report saved to: {output_path}")


def generate_charts(results: List[Dict], trades: pd.DataFrame,
                    output_dir: str) -> None:
    """
    Generate performance charts.
    
    Args:
        results: List of result dictionaries
        trades: DataFrame with trade details
        output_dir: Directory to save charts
    """
    if not HAS_MATPLOTLIB:
        print("matplotlib not available, skipping chart generation")
        return
    
    df_results = pd.DataFrame(results)
    
    if len(df_results) == 0:
        return
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Chart 1: Win Rate by RR for each SL type
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, tf in enumerate(['1m', '5m', '15m']):
        ax = axes[idx]
        tf_data = df_results[df_results['timeframe'] == tf]
        
        for sl_type in tf_data['sl_type'].unique():
            sl_data = tf_data[tf_data['sl_type'] == sl_type].sort_values('rr')
            ax.plot(sl_data['rr'], sl_data['win_rate'], marker='o', label=sl_type)
        
        ax.set_xlabel('Risk/Reward Ratio')
        ax.set_ylabel('Win Rate (%)')
        ax.set_title(f'Win Rate by RR - {tf.upper()}')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'win_rate_by_rr.png'), dpi=150)
    plt.close()
    
    # Chart 2: Expectancy by RR for each SL type
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, tf in enumerate(['1m', '5m', '15m']):
        ax = axes[idx]
        tf_data = df_results[df_results['timeframe'] == tf]
        
        for sl_type in tf_data['sl_type'].unique():
            sl_data = tf_data[tf_data['sl_type'] == sl_type].sort_values('rr')
            ax.plot(sl_data['rr'], sl_data['expectancy'], marker='o', label=sl_type)
        
        ax.set_xlabel('Risk/Reward Ratio')
        ax.set_ylabel('Expectancy (R)')
        ax.set_title(f'Expectancy by RR - {tf.upper()}')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'expectancy_by_rr.png'), dpi=150)
    plt.close()
    
    # Chart 3: Heatmap of win rates
    for tf in ['1m', '5m', '15m']:
        tf_data = df_results[df_results['timeframe'] == tf]
        
        if len(tf_data) == 0:
            continue
        
        pivot = tf_data.pivot_table(
            values='win_rate', 
            index='sl_type', 
            columns='rr',
            aggfunc='mean'
        )
        
        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
        
        ax.set_xticks(range(len(pivot.columns)))
        ax.set_xticklabels([f'RR {c}' for c in pivot.columns])
        ax.set_yticks(range(len(pivot.index)))
        ax.set_yticklabels(pivot.index)
        
        # Add values to cells
        for i in range(len(pivot.index)):
            for j in range(len(pivot.columns)):
                value = pivot.values[i, j]
                if not np.isnan(value):
                    ax.text(j, i, f'{value:.1f}%', ha='center', va='center', 
                           color='black' if 30 < value < 70 else 'white')
        
        plt.colorbar(im, label='Win Rate (%)')
        ax.set_title(f'Win Rate Heatmap - {tf.upper()}')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'heatmap_{tf}.png'), dpi=150)
        plt.close()
    
    print(f"Charts saved to: {output_dir}")


if __name__ == "__main__":
    print("Report generator module loaded successfully")
    print(f"matplotlib available: {HAS_MATPLOTLIB}")
