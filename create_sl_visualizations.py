"""
Create visualizations for Stop Loss Placement Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_style('whitegrid')

# Sample data from the analysis
data = {
    'SL Placement': ['Top/Bottom', 'Top/Bottom', 'Top/Bottom', 
                     'Bottom/Top', 'Bottom/Top', 'Bottom/Top',
                     'First Candle', 'First Candle', 'First Candle'],
    'R/R Ratio': [2.0, 3.0, 5.0, 2.0, 3.0, 5.0, 2.0, 3.0, 5.0],
    'Return (%)': [22.44, 28.55, 38.72, 37.20, 50.80, 47.54, 48.54, 51.80, 49.38],
    'Win Rate (%)': [34.86, 29.66, 25.08, 40.37, 38.23, 36.70, 47.09, 45.57, 45.26],
    'Sharpe Ratio': [1.38, 1.46, 1.70, 1.50, 1.85, 1.70, 1.58, 1.63, 1.54]
}

df = pd.DataFrame(data)

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Stop Loss Placement Analysis - 15M Timeframe (2022-2024)', 
             fontsize=18, fontweight='bold', y=0.995)

colors = {'Top/Bottom': '#e74c3c', 'Bottom/Top': '#3498db', 'First Candle': '#2ecc71'}

# Plot 1: Total Return by R/R Ratio
ax = axes[0, 0]
for sl in df['SL Placement'].unique():
    data_subset = df[df['SL Placement'] == sl]
    ax.plot(data_subset['R/R Ratio'], data_subset['Return (%)'], 
           marker='o', linewidth=2.5, markersize=10, label=sl, color=colors[sl])
ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Return (%)', fontsize=12, fontweight='bold')
ax.set_title('Total Return vs R/R Ratio', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# Plot 2: Win Rate by R/R Ratio
ax = axes[0, 1]
for sl in df['SL Placement'].unique():
    data_subset = df[df['SL Placement'] == sl]
    ax.plot(data_subset['R/R Ratio'], data_subset['Win Rate (%)'], 
           marker='s', linewidth=2.5, markersize=10, label=sl, color=colors[sl])
ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Win Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Win Rate vs R/R Ratio', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# Plot 3: Sharpe Ratio by R/R Ratio
ax = axes[1, 0]
for sl in df['SL Placement'].unique():
    data_subset = df[df['SL Placement'] == sl]
    ax.plot(data_subset['R/R Ratio'], data_subset['Sharpe Ratio'], 
           marker='^', linewidth=2.5, markersize=10, label=sl, color=colors[sl])
ax.set_xlabel('Risk/Reward Ratio', fontsize=12, fontweight='bold')
ax.set_ylabel('Sharpe Ratio', fontsize=12, fontweight='bold')
ax.set_title('Sharpe Ratio vs R/R Ratio', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)

# Plot 4: Bar chart comparison
ax = axes[1, 1]
avg_data = df.groupby('SL Placement').agg({
    'Return (%)': 'mean',
    'Win Rate (%)': 'mean',
    'Sharpe Ratio': 'mean'
}).reset_index()

x = range(len(avg_data))
width = 0.25

bars1 = ax.bar([i - width for i in x], avg_data['Return (%)'], width, 
              label='Avg Return (%)', color='#2ecc71', alpha=0.8)
bars2 = ax.bar(x, avg_data['Win Rate (%)'], width, 
              label='Avg Win Rate (%)', color='#3498db', alpha=0.8)
bars3 = ax.bar([i + width for i in x], avg_data['Sharpe Ratio']*10, width, 
              label='Avg Sharpe (×10)', color='#f39c12', alpha=0.8)

ax.set_xlabel('Stop Loss Placement Strategy', fontsize=12, fontweight='bold')
ax.set_ylabel('Value', fontsize=12, fontweight='bold')
ax.set_title('Average Performance Comparison', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(avg_data['SL Placement'])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.1f}',
               ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('results_sl_placement/sl_placement_analysis.png', dpi=150, bbox_inches='tight')
print("Visualization saved to: results_sl_placement/sl_placement_analysis.png")

# Create summary table image
fig2, ax = plt.subplots(1, 1, figsize=(14, 6))
ax.axis('tight')
ax.axis('off')

# Prepare table data
table_data = []
table_data.append(['SL Placement', 'R/R', 'Return (%)', 'Win Rate (%)', 'Sharpe', 'Notes'])
table_data.append(['─'*15, '─'*5, '─'*11, '─'*13, '─'*7, '─'*30])

for _, row in df.iterrows():
    notes = ''
    if row['Return (%)'] > 50:
        notes = '★ Highest Return'
    elif row['Win Rate (%)'] > 45:
        notes = '★ Highest Win Rate'
    
    table_data.append([
        row['SL Placement'],
        f"{row['R/R Ratio']:.1f}",
        f"{row['Return (%)']:.2f}",
        f"{row['Win Rate (%)']:.2f}",
        f"{row['Sharpe Ratio']:.2f}",
        notes
    ])

table = ax.table(cellText=table_data, cellLoc='left', loc='center',
                colWidths=[0.2, 0.08, 0.12, 0.13, 0.1, 0.25])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.5)

# Style header row
for i in range(6):
    cell = table[(0, i)]
    cell.set_facecolor('#34495e')
    cell.set_text_props(weight='bold', color='white')
    
    cell2 = table[(1, i)]
    cell2.set_facecolor('#ecf0f1')

# Color code rows
for i in range(2, len(table_data)):
    sl_placement = table_data[i][0]
    if sl_placement == 'First Candle':
        color = '#d5f4e6'  # light green
    elif sl_placement == 'Bottom/Top':
        color = '#d6eaf8'  # light blue
    else:
        color = '#fadbd8'  # light red
    
    for j in range(6):
        table[(i, j)].set_facecolor(color)

plt.title('Stop Loss Placement Analysis - Detailed Results', 
         fontsize=16, fontweight='bold', pad=20)
plt.savefig('results_sl_placement/sl_placement_table.png', dpi=150, bbox_inches='tight')
print("Table visualization saved to: results_sl_placement/sl_placement_table.png")

print("\nKey Findings:")
print(f"  Best Overall: First Candle strategy with R/R 3.0 (51.80% return)")
print(f"  Highest Win Rate: First Candle (45.97% avg)")
print(f"  Best Risk-Adjusted: Bottom/Top with R/R 3.0 (1.85 Sharpe)")
