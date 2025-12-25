"""
Example: How to run backtests programmatically for all configurations
======================================================================

This script demonstrates how to test all strategy and risk mode combinations
and save the results for comparison.
"""

import subprocess
import re
import pandas as pd
from datetime import datetime

def update_backtest_config(strategy, risk_mode):
    """Update the configuration in ict_backtest.py"""
    with open('ict_backtest.py', 'r') as f:
        content = f.read()
    
    content = re.sub(r"STRATEGY = '[ABC]'", f"STRATEGY = '{strategy}'", content)
    content = re.sub(r"RISK_MODE = [123]", f"RISK_MODE = {risk_mode}", content)
    
    with open('ict_backtest.py', 'w') as f:
        f.write(content)

def run_backtest():
    """Run the backtest and return the output"""
    result = subprocess.run(['python3', 'ict_backtest.py'], 
                          capture_output=True, text=True, timeout=120)
    return result.stdout

def parse_metrics(output):
    """Parse metrics from backtest output"""
    metrics = {}
    lines = output.split('\n')
    
    for line in lines:
        if 'Total Trades' in line and '...' in line:
            metrics['Total_Trades'] = int(line.split()[-1].replace(',', ''))
        elif 'Winning Trades' in line:
            metrics['Winning_Trades'] = int(line.split()[-1].replace(',', ''))
        elif 'Losing Trades' in line:
            metrics['Losing_Trades'] = int(line.split()[-1].replace(',', ''))
        elif 'Win Rate (%)' in line:
            metrics['Win_Rate'] = float(line.split()[-1])
        elif 'Profit Factor' in line:
            metrics['Profit_Factor'] = float(line.split()[-1])
        elif 'Total PnL' in line:
            metrics['Total_PnL'] = float(line.split()[-1].replace(',', ''))
        elif 'Return (%)' in line:
            metrics['Return_Pct'] = float(line.split()[-1])
    
    return metrics

def main():
    """Run all strategy and risk mode combinations"""
    print("="*70)
    print("RUNNING ALL ICT BACKTEST CONFIGURATIONS")
    print("="*70)
    print()
    
    strategies = ['A', 'B', 'C']
    risk_modes = [1, 2, 3]
    
    strategy_names = {
        'A': 'Judas Swing',
        'B': 'Power of 3',
        'C': 'Displacement'
    }
    
    risk_names = {
        1: 'Scalper Fixe',
        2: 'Swing Session',
        3: 'Volatilité Dynamique'
    }
    
    results = []
    
    for strategy in strategies:
        for risk_mode in risk_modes:
            print(f"Testing Strategy {strategy} ({strategy_names[strategy]}) "
                  f"with Risk Mode {risk_mode} ({risk_names[risk_mode]})...")
            
            # Update configuration
            update_backtest_config(strategy, risk_mode)
            
            # Run backtest
            output = run_backtest()
            
            # Parse metrics
            metrics = parse_metrics(output)
            
            # Add configuration info
            metrics['Strategy'] = strategy
            metrics['Strategy_Name'] = strategy_names[strategy]
            metrics['Risk_Mode'] = risk_mode
            metrics['Risk_Name'] = risk_names[risk_mode]
            
            results.append(metrics)
            
            print(f"  ✓ {metrics.get('Total_Trades', 'N/A')} trades, "
                  f"Win Rate: {metrics.get('Win_Rate', 'N/A')}%, "
                  f"Return: {metrics.get('Return_Pct', 'N/A')}%\n")
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Reorder columns
    columns = ['Strategy', 'Strategy_Name', 'Risk_Mode', 'Risk_Name', 
               'Total_Trades', 'Winning_Trades', 'Losing_Trades',
               'Win_Rate', 'Profit_Factor', 'Total_PnL', 'Return_Pct']
    df = df[columns]
    
    # Save to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'backtest_comparison_{timestamp}.csv'
    df.to_csv(filename, index=False)
    
    print("\n" + "="*70)
    print("SUMMARY OF ALL CONFIGURATIONS")
    print("="*70)
    print()
    print(df.to_string(index=False))
    print()
    print(f"Results saved to: {filename}")
    print("="*70)
    
    # Find best configuration
    best_return = df.loc[df['Return_Pct'].idxmax()]
    print(f"\n🏆 Best Return: Strategy {best_return['Strategy']} + Mode {best_return['Risk_Mode']}")
    print(f"   {best_return['Strategy_Name']} with {best_return['Risk_Name']}")
    print(f"   Return: {best_return['Return_Pct']:.2f}%")
    
    best_pf = df.loc[df['Profit_Factor'].idxmax()]
    print(f"\n🎯 Best Profit Factor: Strategy {best_pf['Strategy']} + Mode {best_pf['Risk_Mode']}")
    print(f"   {best_pf['Strategy_Name']} with {best_pf['Risk_Name']}")
    print(f"   Profit Factor: {best_pf['Profit_Factor']:.2f}")
    
    best_wr = df.loc[df['Win_Rate'].idxmax()]
    print(f"\n🎲 Best Win Rate: Strategy {best_wr['Strategy']} + Mode {best_wr['Risk_Mode']}")
    print(f"   {best_wr['Strategy_Name']} with {best_wr['Risk_Name']}")
    print(f"   Win Rate: {best_wr['Win_Rate']:.2f}%\n")

if __name__ == "__main__":
    main()
