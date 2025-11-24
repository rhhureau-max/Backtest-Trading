#!/usr/bin/env python3
"""
Optimal RR Ratio Analysis Based on Body Size
---------------------------------------------
This script analyzes the relationship between the 8:30 AM candle body size
and win rate for each RR ratio to find the optimal RR given body size.

Author: Trading Strategy Analyzer
Date: 2025-11-24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from pathlib import Path

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (18, 14)


def load_trades():
    """Load all body retracement trades"""
    df = pd.read_csv('results/body_retracement_all_trades.csv')
    return df


def analyze_body_size_ranges(df):
    """
    Analyze win rates by body size ranges for each timeframe and RR
    """
    results = []
    
    for timeframe in ['1m', '5m', '15m']:
        tf_df = df[df['timeframe'] == timeframe].copy()
        
        if len(tf_df) == 0:
            continue
        
        # Define body size ranges based on percentiles
        body_sizes = tf_df['body_size'].unique()
        
        # Create 5 body size buckets based on quintiles
        tf_df['body_size_bucket'] = pd.qcut(tf_df['body_size'], q=5, labels=['Très petit', 'Petit', 'Moyen', 'Grand', 'Très grand'], duplicates='drop')
        
        for rr_ratio in tf_df['rr_ratio'].unique():
            for bucket in tf_df['body_size_bucket'].unique():
                bucket_df = tf_df[(tf_df['rr_ratio'] == rr_ratio) & (tf_df['body_size_bucket'] == bucket)]
                
                if len(bucket_df) == 0:
                    continue
                
                wins = len(bucket_df[bucket_df['outcome'] == 'win'])
                losses = len(bucket_df[bucket_df['outcome'] == 'loss'])
                total = wins + losses
                
                if total == 0:
                    continue
                
                win_rate = (wins / total) * 100
                
                # Get body size range for this bucket
                min_body = bucket_df['body_size'].min()
                max_body = bucket_df['body_size'].max()
                avg_body = bucket_df['body_size'].mean()
                
                results.append({
                    'timeframe': timeframe,
                    'rr_ratio': rr_ratio,
                    'body_size_bucket': bucket,
                    'min_body_size': min_body,
                    'max_body_size': max_body,
                    'avg_body_size': avg_body,
                    'total_trades': total,
                    'wins': wins,
                    'losses': losses,
                    'win_rate': win_rate
                })
    
    return pd.DataFrame(results)


def find_optimal_rr_by_body_size(df):
    """
    Find the optimal RR for each body size range
    """
    results = []
    
    for timeframe in ['1m', '5m', '15m']:
        tf_df = df[df['timeframe'] == timeframe].copy()
        
        if len(tf_df) == 0:
            continue
        
        # Create body size buckets - more granular
        tf_df['body_size_range'] = pd.cut(tf_df['body_size'], bins=10, precision=0)
        
        for body_range in tf_df['body_size_range'].unique():
            range_df = tf_df[tf_df['body_size_range'] == body_range]
            
            best_rr = None
            best_win_rate = 0
            best_expected_value = -float('inf')
            
            for rr_ratio in range_df['rr_ratio'].unique():
                rr_df = range_df[range_df['rr_ratio'] == rr_ratio]
                
                wins = len(rr_df[rr_df['outcome'] == 'win'])
                losses = len(rr_df[rr_df['outcome'] == 'loss'])
                total = wins + losses
                
                if total < 3:  # Minimum sample size
                    continue
                
                win_rate = (wins / total) * 100
                
                # Calculate expected value: (win_rate * RR) - ((1 - win_rate) * 1)
                expected_value = (win_rate / 100 * rr_ratio) - ((100 - win_rate) / 100)
                
                if expected_value > best_expected_value:
                    best_expected_value = expected_value
                    best_rr = rr_ratio
                    best_win_rate = win_rate
            
            if best_rr is not None:
                min_body = range_df['body_size'].min()
                max_body = range_df['body_size'].max()
                
                results.append({
                    'timeframe': timeframe,
                    'body_size_range': f"{min_body:.0f}-{max_body:.0f}",
                    'min_body_size': min_body,
                    'max_body_size': max_body,
                    'optimal_rr': best_rr,
                    'win_rate_at_optimal': best_win_rate,
                    'expected_value': best_expected_value,
                    'total_trades': len(range_df[range_df['rr_ratio'] == best_rr])
                })
    
    return pd.DataFrame(results)


def analyze_correlation(df):
    """
    Analyze correlation between body size and win rate for each RR
    """
    results = []
    
    for timeframe in ['1m', '5m', '15m']:
        tf_df = df[df['timeframe'] == timeframe].copy()
        
        for rr_ratio in tf_df['rr_ratio'].unique():
            rr_df = tf_df[tf_df['rr_ratio'] == rr_ratio]
            
            # Create binary win column
            rr_df['is_win'] = (rr_df['outcome'] == 'win').astype(int)
            
            # Calculate correlation
            correlation = rr_df['body_size'].corr(rr_df['is_win'])
            
            results.append({
                'timeframe': timeframe,
                'rr_ratio': rr_ratio,
                'correlation': correlation,
                'interpretation': 'Positive (plus grand = meilleur)' if correlation > 0.05 else (
                    'Négatif (plus petit = meilleur)' if correlation < -0.05 else 'Neutre')
            })
    
    return pd.DataFrame(results)


def create_detailed_analysis(df):
    """Create a comprehensive analysis report"""
    
    print("\n" + "="*120)
    print("ANALYSE DU RR OPTIMAL EN FONCTION DE LA TAILLE DU CORPS DE LA BOUGIE 8:30")
    print("="*120)
    
    # Section 1: Correlation Analysis
    print("\n\n" + "="*120)
    print("1. CORRÉLATION ENTRE TAILLE DU CORPS ET WIN RATE")
    print("="*120 + "\n")
    
    corr_df = analyze_correlation(df)
    
    for timeframe in ['1m', '5m', '15m']:
        tf_corr = corr_df[corr_df['timeframe'] == timeframe]
        print(f"\n📊 {timeframe.upper()}:")
        
        table_data = []
        for _, row in tf_corr.iterrows():
            table_data.append([
                f"{row['rr_ratio']:.1f}",
                f"{row['correlation']:.4f}",
                row['interpretation']
            ])
        
        print(tabulate(table_data, headers=['RR Ratio', 'Corrélation', 'Interprétation'], tablefmt='grid'))
    
    # Section 2: Body Size Range Analysis
    print("\n\n" + "="*120)
    print("2. WIN RATE PAR TRANCHE DE TAILLE DU CORPS")
    print("="*120 + "\n")
    
    bucket_df = analyze_body_size_ranges(df)
    
    for timeframe in ['1m', '5m', '15m']:
        tf_data = bucket_df[bucket_df['timeframe'] == timeframe]
        print(f"\n📊 {timeframe.upper()}:")
        
        # Pivot for better display
        pivot = tf_data.pivot_table(
            index='body_size_bucket',
            columns='rr_ratio',
            values='win_rate',
            aggfunc='mean'
        )
        
        # Create table
        table_data = []
        for bucket in pivot.index:
            row_data = [bucket]
            for rr in sorted(pivot.columns):
                val = pivot.loc[bucket, rr] if rr in pivot.columns else 0
                row_data.append(f"{val:.1f}%" if not pd.isna(val) else "-")
            table_data.append(row_data)
        
        headers = ['Taille Corps'] + [f'RR {r:.1f}' for r in sorted(pivot.columns)]
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Section 3: Optimal RR by Body Size
    print("\n\n" + "="*120)
    print("3. RR OPTIMAL PAR TRANCHE DE TAILLE DU CORPS")
    print("="*120 + "\n")
    
    optimal_df = find_optimal_rr_by_body_size(df)
    
    for timeframe in ['1m', '5m', '15m']:
        tf_opt = optimal_df[optimal_df['timeframe'] == timeframe].sort_values('min_body_size')
        
        if len(tf_opt) == 0:
            continue
        
        print(f"\n📊 {timeframe.upper()}:")
        
        table_data = []
        for _, row in tf_opt.iterrows():
            table_data.append([
                row['body_size_range'],
                f"{row['optimal_rr']:.1f}",
                f"{row['win_rate_at_optimal']:.1f}%",
                f"{row['expected_value']:.3f}",
                int(row['total_trades'])
            ])
        
        headers = ['Taille Corps', 'RR Optimal', 'Win Rate', 'Valeur Attendue', 'Trades']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Section 4: Key Findings Summary
    print("\n\n" + "="*120)
    print("4. CONCLUSIONS ET RECOMMANDATIONS")
    print("="*120 + "\n")
    
    # Find best configurations for each body size category
    for timeframe in ['1m', '5m', '15m']:
        tf_df = df[df['timeframe'] == timeframe]
        
        # Split into small and large bodies
        median_body = tf_df['body_size'].median()
        
        small_bodies = tf_df[tf_df['body_size'] < median_body]
        large_bodies = tf_df[tf_df['body_size'] >= median_body]
        
        print(f"\n🎯 {timeframe.upper()} (Médiane corps: {median_body:.1f} points):")
        
        # Best RR for small bodies
        best_small_rr = None
        best_small_wr = 0
        for rr in small_bodies['rr_ratio'].unique():
            rr_df = small_bodies[small_bodies['rr_ratio'] == rr]
            wins = len(rr_df[rr_df['outcome'] == 'win'])
            total = len(rr_df[rr_df['outcome'].isin(['win', 'loss'])])
            if total > 0:
                wr = wins / total * 100
                if wr > best_small_wr:
                    best_small_wr = wr
                    best_small_rr = rr
        
        # Best RR for large bodies
        best_large_rr = None
        best_large_wr = 0
        for rr in large_bodies['rr_ratio'].unique():
            rr_df = large_bodies[large_bodies['rr_ratio'] == rr]
            wins = len(rr_df[rr_df['outcome'] == 'win'])
            total = len(rr_df[rr_df['outcome'].isin(['win', 'loss'])])
            if total > 0:
                wr = wins / total * 100
                if wr > best_large_wr:
                    best_large_wr = wr
                    best_large_rr = rr
        
        print(f"   • Petits corps (< {median_body:.1f} pts): Meilleur RR = {best_small_rr} → {best_small_wr:.1f}% win rate")
        print(f"   • Grands corps (≥ {median_body:.1f} pts): Meilleur RR = {best_large_rr} → {best_large_wr:.1f}% win rate")
    
    return bucket_df, optimal_df


def create_visualizations(df, bucket_df, optimal_df):
    """Create comprehensive visualizations"""
    
    print("\n\n📈 Génération des visualisations...")
    
    # Figure 1: Win Rate by Body Size and RR - Heatmaps
    fig, axes = plt.subplots(1, 3, figsize=(20, 8))
    fig.suptitle('Win Rate (%) par Taille du Corps et RR Ratio\nAnalyse Body Retracement 62% (2018-2025)', 
                 fontsize=16, fontweight='bold')
    
    for idx, timeframe in enumerate(['1m', '5m', '15m']):
        ax = axes[idx]
        tf_data = bucket_df[bucket_df['timeframe'] == timeframe]
        
        if len(tf_data) == 0:
            continue
        
        # Create pivot table
        pivot = tf_data.pivot_table(
            index='body_size_bucket',
            columns='rr_ratio',
            values='win_rate',
            aggfunc='mean'
        )
        
        # Reorder index if possible
        try:
            order = ['Très petit', 'Petit', 'Moyen', 'Grand', 'Très grand']
            pivot = pivot.reindex([o for o in order if o in pivot.index])
        except:
            pass
        
        sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', 
                   center=30, vmin=0, vmax=60, ax=ax,
                   cbar_kws={'label': 'Win Rate (%)'})
        ax.set_title(f'{timeframe.upper()}', fontsize=14, fontweight='bold')
        ax.set_xlabel('RR Ratio', fontsize=11)
        ax.set_ylabel('Taille du Corps', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('results/optimal_rr_by_body_size_heatmap.png', dpi=300, bbox_inches='tight')
    print("✅ Heatmap sauvegardée: results/optimal_rr_by_body_size_heatmap.png")
    
    # Figure 2: Body Size vs Win Rate Scatter with Best RR Highlighted
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle('RR Optimal selon la Taille du Corps de la Bougie 8:30\nAnalyse 2018-2025', 
                 fontsize=16, fontweight='bold')
    
    for idx, timeframe in enumerate(['1m', '5m', '15m']):
        ax = axes[idx]
        tf_opt = optimal_df[optimal_df['timeframe'] == timeframe].sort_values('min_body_size')
        
        if len(tf_opt) == 0:
            continue
        
        # Plot optimal RR by body size range
        x = range(len(tf_opt))
        bars = ax.bar(x, tf_opt['optimal_rr'], color='steelblue', alpha=0.8)
        
        # Add win rate as text on bars
        for i, (_, row) in enumerate(tf_opt.iterrows()):
            ax.annotate(f"{row['win_rate_at_optimal']:.0f}%", 
                       xy=(i, row['optimal_rr'] + 0.2),
                       ha='center', fontsize=9, fontweight='bold')
        
        ax.set_xlabel('Taille du Corps (plage)', fontsize=11, fontweight='bold')
        ax.set_ylabel('RR Optimal', fontsize=11, fontweight='bold')
        ax.set_title(f'{timeframe.upper()}', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(tf_opt['body_size_range'], rotation=45, ha='right', fontsize=9)
        ax.set_ylim(0, 12)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('results/optimal_rr_by_body_size_bars.png', dpi=300, bbox_inches='tight')
    print("✅ Graphique barres sauvegardé: results/optimal_rr_by_body_size_bars.png")
    
    # Figure 3: Line charts showing win rate trend by body size for each RR
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle('Évolution du Win Rate selon la Taille du Corps pour Chaque RR\nAnalyse 2018-2025', 
                 fontsize=16, fontweight='bold')
    
    colors = plt.cm.viridis(np.linspace(0, 1, 9))
    
    for idx, timeframe in enumerate(['1m', '5m', '15m']):
        ax = axes[idx]
        tf_data = bucket_df[bucket_df['timeframe'] == timeframe]
        
        # Get unique buckets in order
        order = ['Très petit', 'Petit', 'Moyen', 'Grand', 'Très grand']
        
        for i, rr in enumerate(sorted(tf_data['rr_ratio'].unique())):
            rr_data = tf_data[tf_data['rr_ratio'] == rr]
            
            # Reorder by bucket
            rr_data = rr_data.set_index('body_size_bucket')
            ordered_data = []
            for bucket in order:
                if bucket in rr_data.index:
                    ordered_data.append(rr_data.loc[bucket, 'win_rate'])
                else:
                    ordered_data.append(np.nan)
            
            ax.plot(range(len(order)), ordered_data, marker='o', color=colors[i], 
                   label=f'RR {rr:.1f}', linewidth=2, markersize=6)
        
        ax.set_xlabel('Taille du Corps', fontsize=11, fontweight='bold')
        ax.set_ylabel('Win Rate (%)', fontsize=11, fontweight='bold')
        ax.set_title(f'{timeframe.upper()}', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(order)))
        ax.set_xticklabels(order, rotation=30, ha='right', fontsize=9)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/win_rate_trend_by_body_size.png', dpi=300, bbox_inches='tight')
    print("✅ Graphique tendance sauvegardé: results/win_rate_trend_by_body_size.png")


def export_results(bucket_df, optimal_df):
    """Export analysis results to CSV"""
    
    bucket_df.to_csv('results/winrate_by_body_size_bucket.csv', index=False)
    print("\n✅ Résultats par tranche exportés: results/winrate_by_body_size_bucket.csv")
    
    optimal_df.to_csv('results/optimal_rr_by_body_size.csv', index=False)
    print("✅ RR optimal par taille exporté: results/optimal_rr_by_body_size.csv")


def main():
    """Main execution function"""
    
    # Load trades
    print("\n📂 Chargement des trades...")
    df = load_trades()
    print(f"   {len(df)} trades chargés")
    
    # Create detailed analysis
    bucket_df, optimal_df = create_detailed_analysis(df)
    
    # Create visualizations
    create_visualizations(df, bucket_df, optimal_df)
    
    # Export results
    export_results(bucket_df, optimal_df)
    
    print("\n\n" + "="*120)
    print("✅ ANALYSE DU RR OPTIMAL PAR TAILLE DU CORPS TERMINÉE!")
    print("="*120)
    print("\nFichiers générés:")
    print("  • results/optimal_rr_by_body_size_heatmap.png")
    print("  • results/optimal_rr_by_body_size_bars.png")
    print("  • results/win_rate_trend_by_body_size.png")
    print("  • results/winrate_by_body_size_bucket.csv")
    print("  • results/optimal_rr_by_body_size.csv")
    print("\n")


if __name__ == "__main__":
    main()
