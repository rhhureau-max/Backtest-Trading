#!/usr/bin/env python3
"""
Win Rate Summary Report
-----------------------
Aggregates and displays win rates across all configurations
for the FVG backtesting analysis (2018-2025)

A "good trade" reaches the take-profit level (TP)
A "bad trade" hits the stop-loss level (SL)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)

def load_results():
    """Load the backtest results summary"""
    df = pd.read_csv('results/backtest_results_summary.csv')
    return df

def aggregate_by_timeframe_sl_rr(df):
    """
    Aggregate results by timeframe, stop_loss_type, and rr_ratio
    across all years (2018-2025)
    """
    # Group by timeframe, stop_loss_type, and rr_ratio
    grouped = df.groupby(['timeframe', 'stop_loss_type', 'rr_ratio']).agg({
        'total_trades': 'sum',
        'wins': 'sum',
        'losses': 'sum',
        'total_pnl': 'sum',
        'gross_profit': 'sum',
        'gross_loss': 'sum'
    }).reset_index()
    
    # Calculate aggregated metrics
    grouped['win_rate'] = (grouped['wins'] / grouped['total_trades'] * 100).round(2)
    grouped['profit_factor'] = (grouped['gross_profit'] / grouped['gross_loss']).round(2)
    
    # Replace inf with 0 where there are no losses
    grouped['profit_factor'] = grouped['profit_factor'].replace([np.inf, -np.inf], 0)
    
    return grouped

def create_summary_tables(df):
    """Create detailed summary tables for each timeframe"""
    
    print("\n" + "="*100)
    print("RAPPORT DES RATIOS DE TRADES GAGNANTS PAR CONFIGURATION (2018-2025)")
    print("="*100)
    print("\nTrade Bon = Trade qui atteint le TP (Take Profit)")
    print("Trade Mauvais = Trade qui touche le SL (Stop Loss)")
    print("\n")
    
    for timeframe in ['1m', '5m', '15m']:
        print("\n" + "-"*100)
        print(f"TIMEFRAME: {timeframe.upper()}")
        print("-"*100)
        
        tf_data = df[df['timeframe'] == timeframe]
        
        for sl_type in ['middle', 'edge']:
            print(f"\n📍 Stop Loss Position: {sl_type.upper()} du FVG")
            print("-"*100)
            
            sl_data = tf_data[tf_data['stop_loss_type'] == sl_type]
            
            # Prepare table data
            table_data = []
            for _, row in sl_data.iterrows():
                table_data.append([
                    f"{row['rr_ratio']:.1f}",
                    row['total_trades'],
                    row['wins'],
                    row['losses'],
                    f"{row['win_rate']:.2f}%",
                    f"{row['profit_factor']:.2f}",
                    f"{row['total_pnl']:.2f}"
                ])
            
            headers = ['RR Ratio', 'Total Trades', 'Trades Bons', 'Trades Mauvais', 
                      'Win Rate (%)', 'Profit Factor', 'P&L Total']
            
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Overall summary
    print("\n\n" + "="*100)
    print("RÉSUMÉ GLOBAL PAR TIMEFRAME ET STOP LOSS (2018-2025)")
    print("="*100 + "\n")
    
    # Aggregate by timeframe and stop loss (averaging across RR ratios)
    summary = df.groupby(['timeframe', 'stop_loss_type']).agg({
        'total_trades': 'sum',
        'wins': 'sum',
        'losses': 'sum',
        'total_pnl': 'sum'
    }).reset_index()
    
    summary['win_rate'] = (summary['wins'] / summary['total_trades'] * 100).round(2)
    
    summary_data = []
    for _, row in summary.iterrows():
        summary_data.append([
            row['timeframe'].upper(),
            row['stop_loss_type'].upper(),
            row['total_trades'],
            row['wins'],
            row['losses'],
            f"{row['win_rate']:.2f}%",
            f"{row['total_pnl']:.2f}"
        ])
    
    headers = ['Timeframe', 'Stop Loss', 'Total Trades', 'Trades Bons', 
              'Trades Mauvais', 'Win Rate Moyen', 'P&L Total']
    print(tabulate(summary_data, headers=headers, tablefmt='grid'))
    
    return df

def create_visualization(df):
    """Create comprehensive win rate visualizations"""
    
    fig, axes = plt.subplots(3, 2, figsize=(18, 14))
    fig.suptitle('Ratios de Trades Gagnants par Configuration (2018-2025)', 
                 fontsize=16, fontweight='bold')
    
    timeframes = ['1m', '5m', '15m']
    
    for idx, timeframe in enumerate(timeframes):
        tf_data = df[df['timeframe'] == timeframe]
        
        # Win Rate by RR Ratio (left column)
        ax1 = axes[idx, 0]
        for sl_type in ['middle', 'edge']:
            sl_data = tf_data[tf_data['stop_loss_type'] == sl_type]
            ax1.plot(sl_data['rr_ratio'], sl_data['win_rate'], 
                    marker='o', linewidth=2, markersize=8,
                    label=f'SL {sl_type.capitalize()}')
        
        ax1.set_xlabel('Risk-Reward Ratio', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Win Rate (%)', fontsize=11, fontweight='bold')
        ax1.set_title(f'{timeframe.upper()} - Win Rate par RR Ratio', 
                     fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(df['rr_ratio'].unique())
        
        # Total Trades by RR Ratio (right column)
        ax2 = axes[idx, 1]
        middle_data = tf_data[tf_data['stop_loss_type'] == 'middle']
        edge_data = tf_data[tf_data['stop_loss_type'] == 'edge']
        
        x = np.arange(len(middle_data['rr_ratio'].unique()))
        width = 0.35
        
        ax2.bar(x - width/2, middle_data['wins'], width, 
               label='Trades Bons (SL Middle)', alpha=0.8, color='green')
        ax2.bar(x - width/2, middle_data['losses'], width, 
               bottom=middle_data['wins'], label='Trades Mauvais (SL Middle)', 
               alpha=0.8, color='red')
        
        ax2.bar(x + width/2, edge_data['wins'], width, 
               label='Trades Bons (SL Edge)', alpha=0.8, color='lightgreen')
        ax2.bar(x + width/2, edge_data['losses'], width, 
               bottom=edge_data['wins'], label='Trades Mauvais (SL Edge)', 
               alpha=0.8, color='lightcoral')
        
        ax2.set_xlabel('Risk-Reward Ratio', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Nombre de Trades', fontsize=11, fontweight='bold')
        ax2.set_title(f'{timeframe.upper()} - Distribution Trades Bons/Mauvais', 
                     fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels([f'{r:.1f}' for r in middle_data['rr_ratio']])
        ax2.legend(fontsize=8, loc='upper right')
        ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('results/win_rate_summary_by_configuration.png', dpi=300, bbox_inches='tight')
    print(f"\n✅ Graphique sauvegardé: results/win_rate_summary_by_configuration.png")
    
    # Create heatmap comparison
    create_heatmap_comparison(df)

def create_heatmap_comparison(df):
    """Create heatmap showing win rates across all configurations"""
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle('Heatmap: Win Rate (%) par Timeframe, Stop Loss et RR Ratio (2018-2025)', 
                 fontsize=16, fontweight='bold')
    
    for idx, timeframe in enumerate(['1m', '5m', '15m']):
        tf_data = df[df['timeframe'] == timeframe]
        
        # Pivot data for heatmap
        pivot_data = tf_data.pivot_table(
            index='stop_loss_type', 
            columns='rr_ratio', 
            values='win_rate'
        )
        
        ax = axes[idx]
        sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='RdYlGn', 
                   center=30, vmin=0, vmax=50, ax=ax, cbar_kws={'label': 'Win Rate (%)'})
        ax.set_title(f'{timeframe.upper()}', fontsize=14, fontweight='bold')
        ax.set_xlabel('RR Ratio', fontsize=12)
        ax.set_ylabel('Stop Loss Type', fontsize=12)
        ax.set_yticklabels(['Edge', 'Middle'], rotation=0)
    
    plt.tight_layout()
    plt.savefig('results/win_rate_heatmap_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✅ Heatmap sauvegardée: results/win_rate_heatmap_comparison.png")

def export_to_csv(df):
    """Export aggregated summary to CSV"""
    output_file = 'results/win_rate_summary_2018_2025.csv'
    
    # Sort by timeframe, stop_loss_type, and rr_ratio
    df_sorted = df.sort_values(['timeframe', 'stop_loss_type', 'rr_ratio'])
    
    # Select and rename columns for clarity
    export_df = df_sorted[[
        'timeframe', 'stop_loss_type', 'rr_ratio', 'total_trades', 
        'wins', 'losses', 'win_rate', 'profit_factor', 'total_pnl'
    ]].copy()
    
    export_df.columns = [
        'Timeframe', 'Stop_Loss_Type', 'RR_Ratio', 'Total_Trades',
        'Trades_Bons', 'Trades_Mauvais', 'Win_Rate_Percent', 
        'Profit_Factor', 'Total_PnL'
    ]
    
    export_df.to_csv(output_file, index=False)
    print(f"\n✅ Résultats exportés: {output_file}")
    
    return output_file

def find_best_configurations(df, top_n=10):
    """Find and display the best configurations by win rate"""
    
    print("\n\n" + "="*100)
    print(f"TOP {top_n} MEILLEURES CONFIGURATIONS PAR WIN RATE (2018-2025)")
    print("="*100 + "\n")
    
    # Sort by win rate and total trades
    df_sorted = df.sort_values(['win_rate', 'total_trades'], ascending=[False, False])
    top_configs = df_sorted.head(top_n)
    
    table_data = []
    for idx, row in top_configs.iterrows():
        table_data.append([
            idx + 1,
            row['timeframe'].upper(),
            row['stop_loss_type'].upper(),
            f"{row['rr_ratio']:.1f}",
            row['total_trades'],
            row['wins'],
            row['losses'],
            f"{row['win_rate']:.2f}%",
            f"{row['profit_factor']:.2f}",
            f"{row['total_pnl']:.2f}"
        ])
    
    headers = ['Rang', 'Timeframe', 'Stop Loss', 'RR Ratio', 'Total Trades', 
              'Trades Bons', 'Trades Mauvais', 'Win Rate', 'Profit Factor', 'P&L Total']
    
    print(tabulate(table_data, headers=headers, tablefmt='grid'))

def main():
    """Main execution function"""
    
    print("\n" + "="*100)
    print("ANALYSE DES RATIOS DE TRADES GAGNANTS - FVG STRATEGY (2018-2025)")
    print("="*100)
    
    # Load results
    print("\n📂 Chargement des résultats du backtest...")
    df_full = load_results()
    
    # Aggregate data
    print("📊 Agrégation des données par configuration...")
    df_aggregated = aggregate_by_timeframe_sl_rr(df_full)
    
    # Create summary tables
    create_summary_tables(df_aggregated)
    
    # Find best configurations
    find_best_configurations(df_aggregated, top_n=15)
    
    # Create visualizations
    print("\n\n📈 Génération des visualisations...")
    create_visualization(df_aggregated)
    
    # Export to CSV
    print("\n💾 Export des résultats...")
    export_to_csv(df_aggregated)
    
    print("\n\n" + "="*100)
    print("✅ ANALYSE TERMINÉE!")
    print("="*100)
    print("\nFichiers générés:")
    print("  • results/win_rate_summary_2018_2025.csv")
    print("  • results/win_rate_summary_by_configuration.png")
    print("  • results/win_rate_heatmap_comparison.png")
    print("\n")

if __name__ == "__main__":
    main()
