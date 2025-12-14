"""
Example Usage Scripts for ICT London Open Backtest
==================================================

This file contains example code snippets for analyzing the backtest results
and customizing the strategy parameters.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# Example 1: Load and Analyze Trade Log
# ============================================================================

def analyze_trade_log():
    """
    Load the trade log and perform basic analysis
    """
    # Load trade log
    trades = pd.read_csv('ict_london_open_trades.csv')
    trades['entry_time'] = pd.to_datetime(trades['entry_time'])
    
    print("=== TRADE LOG ANALYSIS ===\n")
    
    # Basic statistics
    print(f"Total Trades: {len(trades)}")
    print(f"Win Rate: {(trades['outcome'] == 'win').sum() / len(trades) * 100:.2f}%")
    print(f"Average P&L: ${trades['dollar_pnl'].mean():.2f}")
    print(f"Total P&L: ${trades['dollar_pnl'].sum():.2f}\n")
    
    # Best and worst trades
    print("=== TOP 5 WINNING TRADES ===")
    print(trades.nlargest(5, 'dollar_pnl')[['date', 'direction', 'dollar_pnl', 'hour']])
    
    print("\n=== TOP 5 LOSING TRADES ===")
    print(trades.nsmallest(5, 'dollar_pnl')[['date', 'direction', 'dollar_pnl', 'hour']])
    
    # Consecutive wins/losses
    trades['consecutive'] = (trades['outcome'] != trades['outcome'].shift()).cumsum()
    streaks = trades.groupby(['consecutive', 'outcome']).size()
    print(f"\n=== STREAK ANALYSIS ===")
    print(f"Longest Winning Streak: {streaks.get('win', pd.Series()).max()}")
    print(f"Longest Losing Streak: {streaks.get('loss', pd.Series()).max()}")
    
    return trades


# ============================================================================
# Example 2: Compare Bullish vs Bearish Setups
# ============================================================================

def compare_directions():
    """
    Compare performance of bullish vs bearish setups
    """
    trades = pd.read_csv('ict_london_open_trades.csv')
    
    print("\n=== BULLISH VS BEARISH COMPARISON ===\n")
    
    for direction in ['bullish', 'bearish']:
        subset = trades[trades['direction'] == direction]
        win_rate = (subset['outcome'] == 'win').sum() / len(subset) * 100
        avg_pnl = subset['dollar_pnl'].mean()
        total_pnl = subset['dollar_pnl'].sum()
        
        print(f"{direction.upper()}:")
        print(f"  Trades: {len(subset)}")
        print(f"  Win Rate: {win_rate:.2f}%")
        print(f"  Avg P&L: ${avg_pnl:.2f}")
        print(f"  Total P&L: ${total_pnl:.2f}\n")


# ============================================================================
# Example 3: Time-Based Analysis
# ============================================================================

def time_analysis():
    """
    Analyze performance by time of day and day of week
    """
    trades = pd.read_csv('ict_london_open_trades.csv')
    
    print("\n=== TIME-BASED ANALYSIS ===\n")
    
    # Hour analysis with filtering recommendation
    print("Performance by Hour:")
    hour_stats = trades.groupby('hour').agg({
        'dollar_pnl': ['sum', 'mean', 'count'],
        'outcome': lambda x: (x == 'win').sum() / len(x) * 100
    })
    hour_stats.columns = ['Total P&L', 'Avg P&L', 'Trades', 'Win Rate %']
    print(hour_stats)
    
    # Identify best hours
    best_hours = hour_stats[hour_stats['Win Rate %'] > 60].index.tolist()
    print(f"\nRecommended Trading Hours (>60% win rate): {best_hours}")
    
    # Weekday analysis
    print("\n\nPerformance by Weekday:")
    weekday_stats = trades.groupby('weekday').agg({
        'dollar_pnl': ['sum', 'count'],
        'outcome': lambda x: (x == 'win').sum() / len(x) * 100
    })
    weekday_stats.columns = ['Total P&L', 'Trades', 'Win Rate %']
    print(weekday_stats)


# ============================================================================
# Example 4: Drawdown Analysis
# ============================================================================

def analyze_drawdowns():
    """
    Detailed drawdown analysis
    """
    trades = pd.read_csv('ict_london_open_trades.csv')
    trades['entry_time'] = pd.to_datetime(trades['entry_time'])
    
    # Calculate metrics
    trades['cumulative_pnl'] = trades['dollar_pnl'].cumsum()
    trades['cumulative_max'] = trades['cumulative_pnl'].cummax()
    trades['drawdown'] = trades['cumulative_pnl'] - trades['cumulative_max']
    trades['drawdown_pct'] = (trades['drawdown'] / trades['cumulative_max'] * 100).fillna(0)
    
    print("\n=== DRAWDOWN ANALYSIS ===\n")
    print(f"Maximum Drawdown: ${trades['drawdown'].min():.2f}")
    print(f"Maximum Drawdown %: {trades['drawdown_pct'].min():.2f}%")
    
    # Find drawdown periods
    in_drawdown = trades['drawdown'] < 0
    dd_periods = (in_drawdown != in_drawdown.shift()).cumsum()
    
    drawdown_periods = []
    for period in dd_periods[in_drawdown].unique():
        period_trades = trades[dd_periods == period]
        if len(period_trades) > 0:
            drawdown_periods.append({
                'start': period_trades['entry_time'].min(),
                'end': period_trades['entry_time'].max(),
                'duration_days': (period_trades['entry_time'].max() - 
                                 period_trades['entry_time'].min()).days,
                'max_dd': period_trades['drawdown'].min(),
                'trades': len(period_trades)
            })
    
    # Show major drawdown periods
    dd_df = pd.DataFrame(drawdown_periods).sort_values('max_dd')
    print("\n=== TOP 3 DRAWDOWN PERIODS ===")
    print(dd_df.head(3))


# ============================================================================
# Example 5: Risk-Adjusted Returns
# ============================================================================

def calculate_risk_metrics():
    """
    Calculate various risk-adjusted performance metrics
    """
    trades = pd.read_csv('ict_london_open_trades.csv')
    
    print("\n=== RISK-ADJUSTED METRICS ===\n")
    
    # Basic metrics
    total_pnl = trades['dollar_pnl'].sum()
    num_trades = len(trades)
    
    # Sharpe-like ratio (returns / volatility)
    avg_return = trades['dollar_pnl'].mean()
    std_return = trades['dollar_pnl'].std()
    sharpe = avg_return / std_return if std_return > 0 else 0
    
    print(f"Average Return per Trade: ${avg_return:.2f}")
    print(f"Std Deviation: ${std_return:.2f}")
    print(f"Sharpe-like Ratio: {sharpe:.3f}")
    
    # Win/Loss ratio
    wins = trades[trades['outcome'] == 'win']['dollar_pnl']
    losses = trades[trades['outcome'] == 'loss']['dollar_pnl']
    
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0
    win_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
    
    print(f"\nAverage Win: ${avg_win:.2f}")
    print(f"Average Loss: ${avg_loss:.2f}")
    print(f"Win/Loss Ratio: {win_loss_ratio:.2f}")
    
    # Profit factor
    gross_profit = wins.sum() if len(wins) > 0 else 0
    gross_loss = abs(losses.sum()) if len(losses) > 0 else 0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
    
    print(f"\nGross Profit: ${gross_profit:.2f}")
    print(f"Gross Loss: ${gross_loss:.2f}")
    print(f"Profit Factor: {profit_factor:.2f}")
    
    # Expectancy
    win_rate = len(wins) / num_trades
    expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)
    
    print(f"\nWin Rate: {win_rate*100:.2f}%")
    print(f"Expectancy: ${expectancy:.2f}")


# ============================================================================
# Example 6: Custom Visualization
# ============================================================================

def create_custom_charts():
    """
    Create custom analysis charts
    """
    trades = pd.read_csv('ict_london_open_trades.csv')
    trades['entry_time'] = pd.to_datetime(trades['entry_time'])
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Custom ICT Strategy Analysis', fontsize=14, fontweight='bold')
    
    # 1. Monthly P&L
    trades['month'] = trades['entry_time'].dt.to_period('M')
    monthly_pnl = trades.groupby('month')['dollar_pnl'].sum()
    monthly_pnl.plot(kind='bar', ax=axes[0, 0], color='steelblue')
    axes[0, 0].set_title('Monthly P&L')
    axes[0, 0].set_xlabel('Month')
    axes[0, 0].set_ylabel('P&L ($)')
    axes[0, 0].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 2. Win Rate by Hour
    hour_winrate = trades.groupby('hour').apply(
        lambda x: (x['outcome'] == 'win').sum() / len(x) * 100
    )
    hour_winrate.plot(kind='bar', ax=axes[0, 1], color='green', alpha=0.7)
    axes[0, 1].set_title('Win Rate by Hour')
    axes[0, 1].set_xlabel('Hour')
    axes[0, 1].set_ylabel('Win Rate (%)')
    axes[0, 1].axhline(y=50, color='red', linestyle='--', alpha=0.5)
    
    # 3. P&L by Direction
    direction_pnl = trades.groupby('direction')['dollar_pnl'].sum()
    direction_pnl.plot(kind='bar', ax=axes[1, 0], color=['green', 'red'], alpha=0.7)
    axes[1, 0].set_title('Total P&L by Direction')
    axes[1, 0].set_xlabel('Direction')
    axes[1, 0].set_ylabel('Total P&L ($)')
    axes[1, 0].tick_params(axis='x', rotation=0)
    
    # 4. Trade Duration Distribution
    trades['duration'] = (pd.to_datetime(trades['exit_time']) - 
                          pd.to_datetime(trades['entry_time'])).dt.total_seconds() / 3600
    trades['duration'].hist(bins=30, ax=axes[1, 1], color='purple', alpha=0.7)
    axes[1, 1].set_title('Trade Duration Distribution')
    axes[1, 1].set_xlabel('Duration (hours)')
    axes[1, 1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('custom_analysis.png', dpi=300, bbox_inches='tight')
    print("\n=== Custom charts saved to custom_analysis.png ===")
    plt.close()


# ============================================================================
# Example 7: Filter Optimal Setups
# ============================================================================

def find_optimal_filters():
    """
    Identify optimal filters to improve performance
    """
    trades = pd.read_csv('ict_london_open_trades.csv')
    
    print("\n=== OPTIMAL FILTER ANALYSIS ===\n")
    
    # Test hour filter
    print("If we only trade during hour 3:")
    hour3 = trades[trades['hour'] == 3]
    print(f"  Trades: {len(hour3)}")
    print(f"  Win Rate: {(hour3['outcome'] == 'win').sum() / len(hour3) * 100:.2f}%")
    print(f"  Total P&L: ${hour3['dollar_pnl'].sum():.2f}")
    print(f"  Avg P&L: ${hour3['dollar_pnl'].mean():.2f}")
    
    # Test avoiding hour 1
    print("\nIf we avoid hour 1:")
    no_hour1 = trades[trades['hour'] != 1]
    print(f"  Trades: {len(no_hour1)}")
    print(f"  Win Rate: {(no_hour1['outcome'] == 'win').sum() / len(no_hour1) * 100:.2f}%")
    print(f"  Total P&L: ${no_hour1['dollar_pnl'].sum():.2f}")
    print(f"  Improvement: ${no_hour1['dollar_pnl'].sum() - trades['dollar_pnl'].sum():.2f}")
    
    # Test Thursday only
    print("\nIf we only trade on Thursday:")
    thursday = trades[trades['weekday'] == 'Thursday']
    print(f"  Trades: {len(thursday)}")
    print(f"  Win Rate: {(thursday['outcome'] == 'win').sum() / len(thursday) * 100:.2f}%")
    print(f"  Total P&L: ${thursday['dollar_pnl'].sum():.2f}")
    print(f"  Avg P&L: ${thursday['dollar_pnl'].mean():.2f}")


# ============================================================================
# Main execution
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("ICT LONDON OPEN - ADVANCED ANALYSIS EXAMPLES")
    print("="*70)
    
    # Run all examples
    try:
        trades = analyze_trade_log()
        compare_directions()
        time_analysis()
        analyze_drawdowns()
        calculate_risk_metrics()
        find_optimal_filters()
        create_custom_charts()
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        
    except FileNotFoundError:
        print("\nError: Trade log file not found.")
        print("Please run the main backtest first:")
        print("  python ict_london_open_backtest.py")
    except Exception as e:
        print(f"\nError during analysis: {e}")
