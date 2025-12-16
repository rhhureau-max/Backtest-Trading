#!/usr/bin/env python3
"""
FVG Backtest Results Analyzer
------------------------------
Additional analysis and filtering tool for backtest results.
Use this script to dive deeper into specific configurations or patterns.

Usage: python3 analyze_results.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

sns.set_style("whitegrid")


class ResultsAnalyzer:
    """Additional analysis tools for FVG backtest results"""
    
    def __init__(self, results_dir='results'):
        """Load backtest results"""
        self.results_dir = Path(results_dir)
        
        # Load data
        print("Loading backtest results...")
        self.summary = pd.read_csv(self.results_dir / 'backtest_results_summary.csv')
        self.trades = pd.read_csv(self.results_dir / 'all_trades_detailed.csv')
        
        # Convert date columns
        self.trades['date'] = pd.to_datetime(self.trades['date'])
        if 'exit_datetime' in self.trades.columns:
            self.trades['exit_datetime'] = pd.to_datetime(self.trades['exit_datetime'])
        
        print(f"✓ Loaded {len(self.summary)} configuration results")
        print(f"✓ Loaded {len(self.trades)} individual trades")
    
    def find_best_configurations(self, min_trades=20, top_n=20):
        """
        Find best performing configurations with statistical significance
        
        Parameters:
        -----------
        min_trades : int
            Minimum number of trades required
        top_n : int
            Number of top configurations to show
        """
        print(f"\n{'='*80}")
        print(f"TOP {top_n} CONFIGURATIONS (min {min_trades} trades)")
        print(f"{'='*80}\n")
        
        # Filter by minimum trades
        filtered = self.summary[self.summary['total_trades'] >= min_trades].copy()
        
        # Sort by profit factor
        filtered = filtered.sort_values('profit_factor', ascending=False)
        
        # Display top configurations
        display_cols = ['year', 'timeframe', 'stop_loss_type', 'rr_ratio', 
                       'total_trades', 'wins', 'losses', 'win_rate', 
                       'profit_factor', 'total_pnl']
        
        print(filtered[display_cols].head(top_n).to_string(index=False))
        
        return filtered.head(top_n)
    
    def analyze_by_fvg_type(self):
        """Analyze performance by FVG type (bullish vs bearish)"""
        print(f"\n{'='*80}")
        print("PERFORMANCE BY FVG TYPE")
        print(f"{'='*80}\n")
        
        bullish = self.trades[self.trades['fvg_type'] == 'bullish']
        bearish = self.trades[self.trades['fvg_type'] == 'bearish']
        
        for fvg_type, data in [('Bullish', bullish), ('Bearish', bearish)]:
            wins = len(data[data['outcome'] == 'win'])
            losses = len(data[data['outcome'] == 'loss'])
            total = wins + losses
            win_rate = (wins / total * 100) if total > 0 else 0
            
            total_pnl = data[data['outcome'].isin(['win', 'loss'])]['pnl'].sum()
            
            print(f"{fvg_type} FVGs:")
            print(f"  Total Trades: {total}")
            print(f"  Wins: {wins}")
            print(f"  Losses: {losses}")
            print(f"  Win Rate: {win_rate:.2f}%")
            print(f"  Total P&L: {total_pnl:.2f}")
            print()
    
    def analyze_monthly_performance(self):
        """Analyze performance by month"""
        print(f"\n{'='*80}")
        print("PERFORMANCE BY MONTH")
        print(f"{'='*80}\n")
        
        self.trades['month'] = self.trades['date'].dt.month
        self.trades['month_name'] = self.trades['date'].dt.strftime('%B')
        
        monthly = self.trades[self.trades['outcome'].isin(['win', 'loss'])].groupby('month').agg({
            'outcome': lambda x: (x == 'win').sum() / len(x) * 100,
            'pnl': ['sum', 'count']
        }).round(2)
        
        monthly.columns = ['Win Rate (%)', 'Total P&L', 'Trade Count']
        monthly['Month'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly = monthly[['Month', 'Trade Count', 'Win Rate (%)', 'Total P&L']]
        
        print(monthly.to_string())
    
    def compare_configurations(self, config1, config2):
        """
        Compare two specific configurations
        
        Parameters:
        -----------
        config1, config2 : dict
            Configuration dictionaries with keys: year, timeframe, stop_loss_type, rr_ratio
        """
        print(f"\n{'='*80}")
        print("CONFIGURATION COMPARISON")
        print(f"{'='*80}\n")
        
        for idx, config in enumerate([config1, config2], 1):
            mask = (
                (self.summary['year'] == config['year']) &
                (self.summary['timeframe'] == config['timeframe']) &
                (self.summary['stop_loss_type'] == config['stop_loss_type']) &
                (self.summary['rr_ratio'] == config['rr_ratio'])
            )
            
            result = self.summary[mask]
            
            if len(result) == 0:
                print(f"Configuration {idx} not found!")
                continue
            
            result = result.iloc[0]
            
            print(f"Configuration {idx}:")
            print(f"  Year: {config['year']}")
            print(f"  Timeframe: {config['timeframe']}")
            print(f"  Stop Loss: {config['stop_loss_type']}")
            print(f"  RR Ratio: {config['rr_ratio']}")
            print(f"  Total Trades: {result['total_trades']}")
            print(f"  Win Rate: {result['win_rate']:.2f}%")
            print(f"  Profit Factor: {result['profit_factor']:.2f}")
            print(f"  Total P&L: {result['total_pnl']:.2f}")
            print()
    
    def drawdown_analysis(self, year=None, timeframe=None):
        """
        Analyze maximum drawdown for configurations
        
        Parameters:
        -----------
        year : int, optional
            Specific year to analyze
        timeframe : str, optional
            Specific timeframe to analyze
        """
        print(f"\n{'='*80}")
        print("DRAWDOWN ANALYSIS")
        print(f"{'='*80}\n")
        
        # Filter trades
        trades = self.trades.copy()
        if year:
            trades = trades[trades['year'] == year]
        if timeframe:
            trades = trades[trades['timeframe'] == timeframe]
        
        # Group by configuration
        configs = trades.groupby(['year', 'timeframe', 'stop_loss_type', 'rr_ratio'])
        
        results = []
        for config, group in configs:
            group = group[group['outcome'].isin(['win', 'loss'])].sort_values('date')
            if len(group) < 5:
                continue
            
            # Calculate cumulative P&L
            group['cum_pnl'] = group['pnl'].cumsum()
            
            # Calculate drawdown
            running_max = group['cum_pnl'].cummax()
            drawdown = group['cum_pnl'] - running_max
            max_dd = drawdown.min()
            
            results.append({
                'year': config[0],
                'timeframe': config[1],
                'stop_loss': config[2],
                'rr_ratio': config[3],
                'max_drawdown': max_dd,
                'final_pnl': group['cum_pnl'].iloc[-1],
                'trades': len(group)
            })
        
        df_dd = pd.DataFrame(results)
        df_dd = df_dd.sort_values('max_drawdown')
        
        print("Configurations with LOWEST Maximum Drawdown:")
        print(df_dd.head(10).to_string(index=False))
        
        print("\nConfigurations with HIGHEST Maximum Drawdown:")
        print(df_dd.tail(10).to_string(index=False))
    
    def consecutive_analysis(self):
        """Analyze consecutive wins and losses"""
        print(f"\n{'='*80}")
        print("CONSECUTIVE WINS/LOSSES ANALYSIS")
        print(f"{'='*80}\n")
        
        # Sort by date
        trades = self.trades[self.trades['outcome'].isin(['win', 'loss'])].copy()
        trades = trades.sort_values('date')
        
        # Find consecutive patterns
        trades['is_win'] = (trades['outcome'] == 'win').astype(int)
        trades['streak'] = (trades['is_win'].diff() != 0).cumsum()
        
        streaks = trades.groupby('streak').agg({
            'is_win': ['first', 'count']
        })
        streaks.columns = ['is_win', 'length']
        
        # Separate wins and losses
        win_streaks = streaks[streaks['is_win'] == 1]['length']
        loss_streaks = streaks[streaks['is_win'] == 0]['length']
        
        print(f"Maximum consecutive wins: {win_streaks.max()}")
        print(f"Maximum consecutive losses: {loss_streaks.max()}")
        print(f"Average win streak: {win_streaks.mean():.2f}")
        print(f"Average loss streak: {loss_streaks.mean():.2f}")
    
    def export_filtered_results(self, filter_dict, output_file='filtered_results.csv'):
        """
        Export filtered results based on criteria
        
        Parameters:
        -----------
        filter_dict : dict
            Dictionary of filters, e.g., {'timeframe': '5m', 'win_rate': (30, 50)}
        output_file : str
            Output filename
        """
        filtered = self.summary.copy()
        
        for key, value in filter_dict.items():
            if isinstance(value, tuple):  # Range filter
                filtered = filtered[(filtered[key] >= value[0]) & (filtered[key] <= value[1])]
            else:  # Exact match
                filtered = filtered[filtered[key] == value]
        
        output_path = self.results_dir / output_file
        filtered.to_csv(output_path, index=False)
        print(f"\n✓ Exported {len(filtered)} filtered results to: {output_path}")
    
    def visualize_equity_curve(self, year, timeframe, stop_loss_type, rr_ratio):
        """
        Plot equity curve for specific configuration
        
        Parameters:
        -----------
        year : int
        timeframe : str
        stop_loss_type : str
        rr_ratio : float
        """
        # Filter trades for this configuration
        trades = self.trades[
            (self.trades['year'] == year) &
            (self.trades['timeframe'] == timeframe) &
            (self.trades['stop_loss_type'] == stop_loss_type) &
            (self.trades['rr_ratio'] == rr_ratio) &
            (self.trades['outcome'].isin(['win', 'loss']))
        ].copy()
        
        if len(trades) == 0:
            print("No trades found for this configuration!")
            return
        
        trades = trades.sort_values('date')
        trades['cum_pnl'] = trades['pnl'].cumsum()
        
        # Plot
        plt.figure(figsize=(14, 7))
        plt.plot(trades['date'], trades['cum_pnl'], linewidth=2)
        plt.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        plt.fill_between(trades['date'], trades['cum_pnl'], 0, 
                         where=(trades['cum_pnl'] >= 0), alpha=0.3, color='g', label='Profit')
        plt.fill_between(trades['date'], trades['cum_pnl'], 0, 
                         where=(trades['cum_pnl'] < 0), alpha=0.3, color='r', label='Loss')
        
        plt.title(f"Equity Curve: {year} | {timeframe} | {stop_loss_type} | RR {rr_ratio}", 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Cumulative P&L', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = f"equity_curve_{year}_{timeframe}_{stop_loss_type}_RR{rr_ratio}.png"
        plt.savefig(self.results_dir / filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved equity curve to: {self.results_dir / filename}")
        plt.close()


def main():
    """Main analysis menu"""
    print("\n" + "="*80)
    print(" FVG BACKTEST RESULTS ANALYZER ".center(80, "="))
    print("="*80)
    
    # Initialize analyzer
    analyzer = ResultsAnalyzer()
    
    # Run various analyses
    print("\n[1/5] Finding best configurations...")
    analyzer.find_best_configurations(min_trades=20, top_n=15)
    
    print("\n[2/5] Analyzing by FVG type...")
    analyzer.analyze_by_fvg_type()
    
    print("\n[3/5] Analyzing monthly performance...")
    analyzer.analyze_monthly_performance()
    
    print("\n[4/5] Analyzing consecutive wins/losses...")
    analyzer.consecutive_analysis()
    
    print("\n[5/5] Running drawdown analysis...")
    analyzer.drawdown_analysis()
    
    # Example: Export filtered results
    print("\n" + "="*80)
    print("EXPORTING FILTERED RESULTS")
    print("="*80)
    
    # Export 5m timeframe results with win rate > 35%
    analyzer.export_filtered_results(
        {'timeframe': '5m', 'win_rate': (35, 100), 'total_trades': (10, 1000)},
        'best_5m_configs.csv'
    )
    
    # Example: Create equity curve for best configuration
    print("\n" + "="*80)
    print("GENERATING EQUITY CURVE")
    print("="*80)
    
    # Get best configuration
    best = analyzer.summary[analyzer.summary['total_trades'] >= 20].nlargest(1, 'profit_factor').iloc[0]
    analyzer.visualize_equity_curve(
        int(best['year']), 
        best['timeframe'], 
        best['stop_loss_type'], 
        best['rr_ratio']
    )
    
    print("\n" + "="*80)
    print(" ANALYSIS COMPLETE ".center(80, "="))
    print("="*80)
    print("\nAdditional analysis files saved to 'results/' directory")


if __name__ == "__main__":
    main()
