"""
Create visualizations for R/R ratio analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (16, 12)

# Load data
df = pd.read_csv('results_rr_analysis/rr_comparison_summary.csv')

# Create figure with subplots
fig, axes = plt.subplots(3, 2, figsize=(18, 14))
fig.suptitle('FVG Trading Strategy - Risk/Reward Ratio Analysis (2018-2024)', 
             fontsize=18, fontweight='bold', y=0.995)

timeframes = ['1m', '5m', '15m']
colors = ['#3498db', '#e74c3c', '#2ecc71']

# Plot 1: Total Return by R/R Ratio
ax = axes[0, 0]
for i, tf in enumerate(timeframes):
    data = df[df['Timeframe'] == tf]
    ax.plot(data['Risk_Reward_Ratio'], data['Total_Return_Pct'], 
           marker='o', linewidth=2.5, markersize=8, label=tf.upper(), color=colors[i])
ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Return (%)', fontsize=12, fontweight='bold')
ax.set_title('Total Return vs Risk/Reward Ratio', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# Plot 2: Win Rate by R/R Ratio
ax = axes[0, 1]
for i, tf in enumerate(timeframes):
    data = df[df['Timeframe'] == tf]
    ax.plot(data['Risk_Reward_Ratio'], data['Win_Rate_Pct'], 
           marker='s', linewidth=2.5, markersize=8, label=tf.upper(), color=colors[i])
ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Win Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Win Rate vs Risk/Reward Ratio', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# Plot 3: Sharpe Ratio by R/R Ratio
ax = axes[1, 0]
for i, tf in enumerate(timeframes):
    data = df[df['Timeframe'] == tf]
    ax.plot(data['Risk_Reward_Ratio'], data['Sharpe_Ratio'], 
           marker='^', linewidth=2.5, markersize=8, label=tf.upper(), color=colors[i])
ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Sharpe Ratio', fontsize=12, fontweight='bold')
ax.set_title('Sharpe Ratio vs Risk/Reward Ratio', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Sharpe=1.0')

# Plot 4: Max Drawdown by R/R Ratio
ax = axes[1, 1]
for i, tf in enumerate(timeframes):
    data = df[df['Timeframe'] == tf]
    ax.plot(data['Risk_Reward_Ratio'], data['Max_Drawdown_Pct'], 
           marker='v', linewidth=2.5, markersize=8, label=tf.upper(), color=colors[i])
ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Max Drawdown (%)', fontsize=12, fontweight='bold')
ax.set_title('Max Drawdown vs Risk/Reward Ratio', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# Plot 5: Profit Factor by R/R Ratio
ax = axes[2, 0]
for i, tf in enumerate(timeframes):
    data = df[df['Timeframe'] == tf]
    ax.plot(data['Risk_Reward_Ratio'], data['Profit_Factor'], 
           marker='D', linewidth=2.5, markersize=8, label=tf.upper(), color=colors[i])
ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Profit Factor', fontsize=12, fontweight='bold')
ax.set_title('Profit Factor vs Risk/Reward Ratio', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Break-even')

# Plot 6: Heatmap of Total Return
ax = axes[2, 1]
pivot_data = df.pivot(index='Timeframe', columns='Risk_Reward_Ratio', values='Total_Return_Pct')
pivot_data = pivot_data.reindex(['1m', '5m', '15m'])
sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='RdYlGn', center=30, 
           cbar_kws={'label': 'Total Return (%)'}, ax=ax, linewidths=0.5)
ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Timeframe', fontsize=12, fontweight='bold')
ax.set_title('Total Return Heatmap', fontsize=14, fontweight='bold')
ax.set_yticklabels(['1M', '5M', '15M'], rotation=0)

plt.tight_layout()
plt.savefig('results_rr_analysis/rr_analysis_visualization.png', dpi=150, bbox_inches='tight')
print("Visualization saved to: results_rr_analysis/rr_analysis_visualization.png")

# Create a second figure showing best configuration
fig2, ax = plt.subplots(1, 1, figsize=(14, 8))

# Bar chart comparing best R/R for each timeframe
best_configs = []
for tf in timeframes:
    data = df[df['Timeframe'] == tf]
    best_rr = data.loc[data['Total_Return_Pct'].idxmax()]
    best_configs.append({
        'Timeframe': tf.upper(),
        'Best_RR': best_rr['Risk_Reward_Ratio'],
        'Return': best_rr['Total_Return_Pct'],
        'Sharpe': best_rr['Sharpe_Ratio'],
        'Win_Rate': best_rr['Win_Rate_Pct'],
        'Max_DD': best_rr['Max_Drawdown_Pct']
    })

best_df = pd.DataFrame(best_configs)

x = range(len(timeframes))
width = 0.15

ax.bar([i - 2*width for i in x], best_df['Return'], width, label='Total Return (%)', color='#2ecc71')
ax.bar([i - width for i in x], best_df['Sharpe']*10, width, label='Sharpe Ratio (×10)', color='#3498db')
ax.bar([i for i in x], best_df['Win_Rate'], width, label='Win Rate (%)', color='#f39c12')
ax.bar([i + width for i in x], -best_df['Max_DD'], width, label='Max DD (abs %)', color='#e74c3c')

ax.set_xlabel('Timeframe', fontsize=14, fontweight='bold')
ax.set_ylabel('Value', fontsize=14, fontweight='bold')
ax.set_title('Best Risk/Reward Ratio Configuration by Timeframe', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([f"{row['Timeframe']}\n(R/R {row['Best_RR']})" for _, row in best_df.iterrows()])
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
ax.axhline(y=0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig('results_rr_analysis/best_configurations.png', dpi=150, bbox_inches='tight')
print("Best configurations visualization saved to: results_rr_analysis/best_configurations.png")

print("\nAnalysis complete!")
print(f"\nBest overall configuration:")
best_overall = df.loc[df['Total_Return_Pct'].idxmax()]
print(f"  Timeframe: {best_overall['Timeframe'].upper()}")
print(f"  Risk/Reward Ratio: {best_overall['Risk_Reward_Ratio']}")
print(f"  Total Return: {best_overall['Total_Return_Pct']:.2f}%")
print(f"  Sharpe Ratio: {best_overall['Sharpe_Ratio']:.2f}")
print(f"  Win Rate: {best_overall['Win_Rate_Pct']:.2f}%")
print(f"  Max Drawdown: {best_overall['Max_Drawdown_Pct']:.2f}%")
