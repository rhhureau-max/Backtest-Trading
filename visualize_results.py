#!/usr/bin/env python3
"""
Visualization script for Tokyo Session Analysis results
Generates charts and visualizations from the analysis results
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

def load_results(filepath='tokyo_analysis_results.csv'):
    """Load the analysis results CSV."""
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found!")
        print("Please run tokyo_session_analysis.py first.")
        return None
    
    df = pd.read_csv(filepath)
    df['tokyo_start'] = pd.to_datetime(df['tokyo_start'])
    df['breakout_time'] = pd.to_datetime(df['breakout_time'])
    df['return_time'] = pd.to_datetime(df['return_time'])
    
    return df

def plot_overall_statistics(df):
    """Plot overall success rate statistics."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Tokyo Session Strategy - Statistiques Globales', fontsize=16, fontweight='bold')
    
    # 1. Success rate pie chart
    ax1 = axes[0, 0]
    success_counts = df['returned_to_eq'].value_counts()
    colors = ['#2ecc71', '#e74c3c']
    labels = ['Retour au 50%', 'Pas de retour']
    ax1.pie(success_counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.set_title('Taux de Réussite Global')
    
    # 2. Breakout type comparison
    ax2 = axes[0, 1]
    breakout_stats = df.groupby('breakout_type')['returned_to_eq'].agg(['sum', 'count'])
    breakout_stats['rate'] = (breakout_stats['sum'] / breakout_stats['count']) * 100
    
    x_pos = range(len(breakout_stats))
    bars = ax2.bar(x_pos, breakout_stats['rate'], color=['#3498db', '#e67e22'])
    ax2.set_xlabel('Type de Cassure')
    ax2.set_ylabel('Taux de Réussite (%)')
    ax2.set_title('Taux de Réussite par Type de Cassure')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(breakout_stats.index)
    ax2.set_ylim(0, 100)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n({int(breakout_stats.iloc[i]["sum"])}/{int(breakout_stats.iloc[i]["count"])})',
                ha='center', va='bottom')
    
    # 3. Time to return histogram
    ax3 = axes[1, 0]
    successful_returns = df[df['returned_to_eq'] == True]['time_to_return_hours'].dropna()
    ax3.hist(successful_returns, bins=24, color='#9b59b6', edgecolor='black', alpha=0.7)
    ax3.set_xlabel('Heures')
    ax3.set_ylabel('Fréquence')
    ax3.set_title('Distribution du Temps de Retour au 50%')
    ax3.axvline(successful_returns.mean(), color='red', linestyle='--', linewidth=2, label=f'Moyenne: {successful_returns.mean():.2f}h')
    ax3.axvline(successful_returns.median(), color='green', linestyle='--', linewidth=2, label=f'Médiane: {successful_returns.median():.2f}h')
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. Yearly performance
    ax4 = axes[1, 1]
    yearly_stats = df.groupby('year')['returned_to_eq'].agg(['sum', 'count'])
    yearly_stats['rate'] = (yearly_stats['sum'] / yearly_stats['count']) * 100
    
    bars = ax4.bar(yearly_stats.index, yearly_stats['rate'], color='#1abc9c', edgecolor='black', alpha=0.8)
    ax4.set_xlabel('Année')
    ax4.set_ylabel('Taux de Réussite (%)')
    ax4.set_title('Performance Annuelle')
    ax4.set_ylim(0, 100)
    ax4.grid(axis='y', alpha=0.3)
    ax4.axhline(y=df['returned_to_eq'].mean()*100, color='red', linestyle='--', linewidth=2, label='Moyenne globale')
    ax4.legend()
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        year_idx = yearly_stats.index[i]
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n({int(yearly_stats.loc[year_idx, "sum"])}/{int(yearly_stats.loc[year_idx, "count"])})',
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    return fig

def plot_time_series(df):
    """Plot time series analysis."""
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('Tokyo Session Strategy - Analyse Temporelle', fontsize=16, fontweight='bold')
    
    # 1. Cumulative success rate over time
    ax1 = axes[0]
    df_sorted = df.sort_values('tokyo_start')
    df_sorted['cumulative_success'] = df_sorted['returned_to_eq'].expanding().mean() * 100
    
    ax1.plot(df_sorted['tokyo_start'], df_sorted['cumulative_success'], linewidth=2, color='#3498db')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Taux de Réussite Cumulé (%)')
    ax1.set_title('Évolution du Taux de Réussite Cumulé')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 100)
    
    # Format x-axis dates
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 2. Monthly signal count
    ax2 = axes[1]
    df_sorted['year_month'] = df_sorted['tokyo_start'].dt.to_period('M')
    monthly_counts = df_sorted.groupby('year_month').size()
    monthly_success = df_sorted.groupby('year_month')['returned_to_eq'].sum()
    
    x_vals = range(len(monthly_counts))
    ax2.bar(x_vals, monthly_counts, label='Total Signaux', alpha=0.7, color='#95a5a6')
    ax2.bar(x_vals, monthly_success, label='Signaux Réussis', alpha=0.9, color='#2ecc71')
    ax2.set_xlabel('Mois')
    ax2.set_ylabel('Nombre de Signaux')
    ax2.set_title('Nombre de Signaux par Mois')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # Set x-axis labels (show every 6 months)
    step = max(1, len(monthly_counts) // 20)
    ax2.set_xticks(x_vals[::step])
    ax2.set_xticklabels([str(month) for month in monthly_counts.index[::step]], rotation=45, ha='right')
    
    plt.tight_layout()
    return fig

def plot_range_analysis(df):
    """Plot analysis based on Tokyo range."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Tokyo Session Strategy - Analyse de la Range', fontsize=16, fontweight='bold')
    
    # 1. Success rate vs Tokyo range
    ax1 = axes[0]
    
    # Create range bins
    df['range_bin'] = pd.cut(df['tokyo_range'], bins=10)
    range_stats = df.groupby('range_bin')['returned_to_eq'].agg(['mean', 'count'])
    range_stats = range_stats[range_stats['count'] >= 10]  # Only show bins with enough data
    
    x_pos = range(len(range_stats))
    bars = ax1.bar(x_pos, range_stats['mean'] * 100, color='#e74c3c', alpha=0.7)
    ax1.set_xlabel('Range Tokyo (Points)')
    ax1.set_ylabel('Taux de Réussite (%)')
    ax1.set_title('Taux de Réussite vs Range de Tokyo')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([f'{interval.left:.0f}-{interval.right:.0f}' for interval in range_stats.index], 
                         rotation=45, ha='right', fontsize=8)
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)
    ax1.axhline(y=df['returned_to_eq'].mean()*100, color='blue', linestyle='--', linewidth=2, label='Moyenne')
    ax1.legend()
    
    # 2. Distribution of Tokyo range
    ax2 = axes[1]
    ax2.hist(df['tokyo_range'], bins=30, color='#f39c12', edgecolor='black', alpha=0.7)
    ax2.set_xlabel('Range Tokyo (Points)')
    ax2.set_ylabel('Fréquence')
    ax2.set_title('Distribution de la Range Tokyo')
    ax2.axvline(df['tokyo_range'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Moyenne: {df["tokyo_range"].mean():.2f}')
    ax2.axvline(df['tokyo_range'].median(), color='green', linestyle='--', linewidth=2,
                label=f'Médiane: {df["tokyo_range"].median():.2f}')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig

def generate_summary_text(df):
    """Generate a text summary of the analysis."""
    total_signals = len(df)
    successful = df['returned_to_eq'].sum()
    success_rate = (successful / total_signals) * 100
    
    high_breaks = df[df['breakout_type'] == 'HIGH']
    low_breaks = df[df['breakout_type'] == 'LOW']
    
    high_success_rate = (high_breaks['returned_to_eq'].sum() / len(high_breaks) * 100) if len(high_breaks) > 0 else 0
    low_success_rate = (low_breaks['returned_to_eq'].sum() / len(low_breaks) * 100) if len(low_breaks) > 0 else 0
    
    successful_times = df[df['returned_to_eq'] == True]['time_to_return_hours'].dropna()
    
    summary = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║           TOKYO SESSION STRATEGY - RÉSUMÉ DE L'ANALYSE                     ║
╚════════════════════════════════════════════════════════════════════════════╝

Période: {df['date'].min()} à {df['date'].max()}

📊 STATISTIQUES GLOBALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total de signaux:              {total_signals}
Signaux réussis:               {successful}
Signaux échoués:               {total_signals - successful}

🎯 PROBABILITÉ GLOBALE:         {success_rate:.2f}%

📈 PAR TYPE DE CASSURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cassures HIGH:                 {len(high_breaks)} signaux → {high_success_rate:.2f}% de réussite
Cassures LOW:                  {len(low_breaks)} signaux → {low_success_rate:.2f}% de réussite

⏱️ TEMPS DE RETOUR (pour les signaux réussis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Moyenne:                       {successful_times.mean():.2f} heures
Médiane:                       {successful_times.median():.2f} heures
Minimum:                       {successful_times.min():.2f} heures
Maximum:                       {successful_times.max():.2f} heures

📊 RANGE TOKYO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Range moyenne:                 {df['tokyo_range'].mean():.2f} points
Range médiane:                 {df['tokyo_range'].median():.2f} points
Range min/max:                 {df['tokyo_range'].min():.2f} / {df['tokyo_range'].max():.2f} points

╔════════════════════════════════════════════════════════════════════════════╗
║  Graphiques sauvegardés:                                                    ║
║  - tokyo_statistics.png                                                     ║
║  - tokyo_time_series.png                                                    ║
║  - tokyo_range_analysis.png                                                 ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    return summary

def main():
    """Main function to generate all visualizations."""
    print("="*80)
    print("Tokyo Session Analysis - Générateur de Visualisations")
    print("="*80)
    
    # Load results
    print("\nChargement des résultats...")
    df = load_results()
    
    if df is None:
        return
    
    print(f"Résultats chargés: {len(df)} signaux")
    
    # Generate plots
    print("\nGénération des graphiques...")
    
    try:
        print("  1. Statistiques globales...")
        fig1 = plot_overall_statistics(df)
        fig1.savefig('tokyo_statistics.png', dpi=300, bbox_inches='tight')
        plt.close(fig1)
        
        print("  2. Analyse temporelle...")
        fig2 = plot_time_series(df)
        fig2.savefig('tokyo_time_series.png', dpi=300, bbox_inches='tight')
        plt.close(fig2)
        
        print("  3. Analyse de la range...")
        fig3 = plot_range_analysis(df)
        fig3.savefig('tokyo_range_analysis.png', dpi=300, bbox_inches='tight')
        plt.close(fig3)
        
        print("\n✓ Tous les graphiques ont été générés avec succès!")
        
    except Exception as e:
        print(f"\n✗ Erreur lors de la génération des graphiques: {e}")
        print("Note: Assurez-vous que matplotlib est installé: pip install matplotlib")
        return
    
    # Print summary
    print("\n" + generate_summary_text(df))
    
    print("\n" + "="*80)
    print("Visualisation terminée!")
    print("="*80)

if __name__ == "__main__":
    main()
