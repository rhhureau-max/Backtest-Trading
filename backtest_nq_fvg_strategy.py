"""
Nasdaq Futures (NQ) FVG Inversion Strategy Backtester
======================================================

This script backtests a Fair Value Gap (FVG) inversion strategy on NQ 5-minute data
from 2018 to 2025, using ICT concepts and VWAP as a trend filter.

Strategy Rules:
- Time Filter: London Killzone (01:00-04:00 local time)
- Trend Filter: VWAP (daily reset)
- Entry: FVG Inversion signals
- Risk Management: 1:1 R/R, max 1 trade per day
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import os
import glob


class NQFVGBacktester:
    """Backtester for NQ FVG Inversion Strategy"""
    
    def __init__(self, data_path='/home/runner/work/Backtest-Trading/Backtest-Trading'):
        """
        Initialize the backtester
        
        Args:
            data_path: Path to directory containing CSV files
        """
        self.data_path = data_path
        self.df = None
        self.trades = []
        self.performance = {}
        
    def load_data(self):
        """Load and merge all 5m CSV files from 2018 to 2025"""
        print("Loading data files...")
        
        all_data = []
        years = range(2018, 2026)  # 2018 to 2025
        
        for year in years:
            file_path = os.path.join(self.data_path, f"{year} 5m.csv")
            if os.path.exists(file_path):
                print(f"Loading {year} data...")
                df_year = pd.read_csv(file_path, sep=';')
                all_data.append(df_year)
            else:
                print(f"Warning: {file_path} not found")
        
        if not all_data:
            raise ValueError("No data files found!")
        
        # Combine all years
        df = pd.concat(all_data, ignore_index=True)
        
        # Rename columns
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Parse datetime (data is already in Chicago timezone - no conversion needed)
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        
        # Set DateTime as index
        df.set_index('DateTime', inplace=True)
        
        # Keep only necessary columns
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Convert to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Sort by datetime
        df.sort_index(inplace=True)
        
        # Remove any duplicates
        df = df[~df.index.duplicated(keep='first')]
        
        print(f"Loaded {len(df)} candles from {df.index[0]} to {df.index[-1]}")
        
        self.df = df
        return df
    
    def calculate_vwap(self):
        """Calculate VWAP that resets at the start of each trading day"""
        print("Calculating VWAP...")
        
        df = self.df
        
        # Typical Price
        df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
        
        # Create date column for grouping
        df['DateOnly'] = df.index.date
        
        # Calculate cumulative values per day
        df['TPV'] = df['TP'] * df['Volume']
        df['CumTPV'] = df.groupby('DateOnly')['TPV'].cumsum()
        df['CumVolume'] = df.groupby('DateOnly')['Volume'].cumsum()
        
        # Calculate VWAP
        df['VWAP'] = df['CumTPV'] / df['CumVolume']
        
        # Clean up temporary columns
        df.drop(['TP', 'TPV', 'CumTPV', 'CumVolume'], axis=1, inplace=True)
        
        print("VWAP calculated successfully")
        
    def detect_fvg(self):
        """
        Detect Fair Value Gaps (FVG)
        
        Bearish FVG: Low[i-2] > High[i] (gap between candles)
        Bullish FVG: High[i-2] < Low[i]
        """
        print("Detecting Fair Value Gaps...")
        
        df = self.df
        
        # Initialize FVG columns
        df['Bearish_FVG'] = False
        df['Bullish_FVG'] = False
        df['Bearish_FVG_Top'] = np.nan
        df['Bearish_FVG_Bottom'] = np.nan
        df['Bullish_FVG_Top'] = np.nan
        df['Bullish_FVG_Bottom'] = np.nan
        
        # Need at least 3 candles to detect FVG
        for i in range(2, len(df)):
            # Bearish FVG: Low of candle[i-2] > High of candle[i]
            if df.iloc[i-2]['Low'] > df.iloc[i]['High']:
                df.iloc[i, df.columns.get_loc('Bearish_FVG')] = True
                df.iloc[i, df.columns.get_loc('Bearish_FVG_Top')] = df.iloc[i-2]['Low']
                df.iloc[i, df.columns.get_loc('Bearish_FVG_Bottom')] = df.iloc[i]['High']
            
            # Bullish FVG: High of candle[i-2] < Low of candle[i]
            if df.iloc[i-2]['High'] < df.iloc[i]['Low']:
                df.iloc[i, df.columns.get_loc('Bullish_FVG')] = True
                df.iloc[i, df.columns.get_loc('Bullish_FVG_Top')] = df.iloc[i]['Low']
                df.iloc[i, df.columns.get_loc('Bullish_FVG_Bottom')] = df.iloc[i-2]['High']
        
        bearish_count = df['Bearish_FVG'].sum()
        bullish_count = df['Bullish_FVG'].sum()
        print(f"Detected {bearish_count} Bearish FVGs and {bullish_count} Bullish FVGs")
        
    def apply_time_filter(self):
        """Apply London Killzone time filter (01:00 - 04:00)"""
        print("Applying time filter (London Killzone: 01:00-04:00)...")
        
        df = self.df
        
        # Extract hour from index
        df['Hour'] = df.index.hour
        df['Minute'] = df.index.minute
        
        # London Killzone: 01:00 to 04:00
        df['In_Killzone'] = (
            ((df['Hour'] == 1) | (df['Hour'] == 2) | (df['Hour'] == 3)) |
            ((df['Hour'] == 4) & (df['Minute'] == 0))
        )
        
        killzone_candles = df['In_Killzone'].sum()
        print(f"Found {killzone_candles} candles in London Killzone")
        
    def detect_fvg_inversions(self):
        """
        Detect FVG Inversion signals
        
        Long Signal: After Bearish FVG, candle closes STRICTLY above top of gap (Low of candle 1)
        Short Signal: After Bullish FVG, candle closes STRICTLY below bottom of gap (High of candle 1)
        """
        print("Detecting FVG inversions...")
        
        df = self.df
        
        # Initialize signal columns
        df['Long_Signal'] = False
        df['Short_Signal'] = False
        df['Signal_SL'] = np.nan
        df['Signal_Entry'] = np.nan
        
        # Track active FVGs (not yet inverted)
        active_bearish_fvgs = []  # List of (index, top, bottom)
        active_bullish_fvgs = []  # List of (index, top, bottom)
        
        for i in range(len(df)):
            current_row = df.iloc[i]
            current_close = current_row['Close']
            current_high = current_row['High']
            current_low = current_row['Low']
            
            # Add new FVGs to tracking lists
            if current_row['Bearish_FVG']:
                active_bearish_fvgs.append((
                    i,
                    current_row['Bearish_FVG_Top'],
                    current_row['Bearish_FVG_Bottom']
                ))
            
            if current_row['Bullish_FVG']:
                active_bullish_fvgs.append((
                    i,
                    current_row['Bullish_FVG_Top'],
                    current_row['Bullish_FVG_Bottom']
                ))
            
            # Check for Long signals (Bearish FVG inversion)
            # Close must be STRICTLY above top of gap
            for fvg_idx, fvg_top, fvg_bottom in active_bearish_fvgs[:]:
                if current_close > fvg_top:
                    # FVG Inverted - Long Signal
                    df.iloc[i, df.columns.get_loc('Long_Signal')] = True
                    df.iloc[i, df.columns.get_loc('Signal_Entry')] = current_close
                    df.iloc[i, df.columns.get_loc('Signal_SL')] = current_low
                    # Remove this FVG as it's been inverted
                    active_bearish_fvgs.remove((fvg_idx, fvg_top, fvg_bottom))
                    break  # Only one signal per candle
            
            # Check for Short signals (Bullish FVG inversion)
            # Close must be STRICTLY below bottom of gap
            if not df.iloc[i]['Long_Signal']:  # Avoid multiple signals on same candle
                for fvg_idx, fvg_top, fvg_bottom in active_bullish_fvgs[:]:
                    if current_close < fvg_bottom:
                        # FVG Inverted - Short Signal
                        df.iloc[i, df.columns.get_loc('Short_Signal')] = True
                        df.iloc[i, df.columns.get_loc('Signal_Entry')] = current_close
                        df.iloc[i, df.columns.get_loc('Signal_SL')] = current_high
                        # Remove this FVG as it's been inverted
                        active_bullish_fvgs.remove((fvg_idx, fvg_top, fvg_bottom))
                        break  # Only one signal per candle
        
        long_signals = df['Long_Signal'].sum()
        short_signals = df['Short_Signal'].sum()
        print(f"Detected {long_signals} Long signals and {short_signals} Short signals")
        
    def apply_vwap_filter(self):
        """
        Apply VWAP trend filter to signals
        
        Long: Signal candle close > VWAP
        Short: Signal candle close < VWAP
        """
        print("Applying VWAP trend filter...")
        
        df = self.df
        
        # Filter Long signals: Close must be > VWAP
        long_before = df['Long_Signal'].sum()
        df.loc[df['Long_Signal'] & (df['Close'] <= df['VWAP']), 'Long_Signal'] = False
        long_after = df['Long_Signal'].sum()
        
        # Filter Short signals: Close must be < VWAP
        short_before = df['Short_Signal'].sum()
        df.loc[df['Short_Signal'] & (df['Close'] >= df['VWAP']), 'Short_Signal'] = False
        short_after = df['Short_Signal'].sum()
        
        print(f"Long signals after VWAP filter: {long_before} -> {long_after}")
        print(f"Short signals after VWAP filter: {short_before} -> {short_after}")
        
    def execute_trades(self):
        """
        Execute trades based on signals with all filters applied
        
        Rules:
        - Max 1 trade per day
        - 1:1 Risk/Reward ratio
        - Force close at 16:00 if still open
        """
        print("Executing trades...")
        
        df = self.df
        trades = []
        
        active_trade = None
        traded_dates = set()  # Track dates where we already traded
        
        for i in range(len(df)):
            current_row = df.iloc[i]
            current_date = current_row['DateOnly']
            current_time = df.index[i]
            current_close = current_row['Close']
            current_high = current_row['High']
            current_low = current_row['Low']
            
            # Check if we should force close (16:00)
            if active_trade and df.index[i].hour == 16 and df.index[i].minute == 0:
                # Force close
                exit_price = current_close
                pnl = (exit_price - active_trade['entry']) if active_trade['direction'] == 'Long' else (active_trade['entry'] - exit_price)
                
                trade_record = {
                    'entry_time': active_trade['entry_time'],
                    'exit_time': current_time,
                    'direction': active_trade['direction'],
                    'entry_price': active_trade['entry'],
                    'exit_price': exit_price,
                    'sl': active_trade['sl'],
                    'tp': active_trade['tp'],
                    'pnl': pnl,
                    'result': 'Force Close',
                    'risk': active_trade['risk']
                }
                trades.append(trade_record)
                active_trade = None
                continue
            
            # Check if active trade hits SL or TP
            if active_trade:
                if active_trade['direction'] == 'Long':
                    # Check if SL hit (low touches or goes below SL)
                    if current_low <= active_trade['sl']:
                        exit_price = active_trade['sl']
                        pnl = exit_price - active_trade['entry']
                        result = 'Loss'
                    # Check if TP hit (high touches or goes above TP)
                    elif current_high >= active_trade['tp']:
                        exit_price = active_trade['tp']
                        pnl = exit_price - active_trade['entry']
                        result = 'Win'
                    else:
                        continue  # Trade still active
                else:  # Short
                    # Check if SL hit (high touches or goes above SL)
                    if current_high >= active_trade['sl']:
                        exit_price = active_trade['sl']
                        pnl = active_trade['entry'] - exit_price
                        result = 'Loss'
                    # Check if TP hit (low touches or goes below TP)
                    elif current_low <= active_trade['tp']:
                        exit_price = active_trade['tp']
                        pnl = active_trade['entry'] - exit_price
                        result = 'Win'
                    else:
                        continue  # Trade still active
                
                # Trade closed
                trade_record = {
                    'entry_time': active_trade['entry_time'],
                    'exit_time': current_time,
                    'direction': active_trade['direction'],
                    'entry_price': active_trade['entry'],
                    'exit_price': exit_price,
                    'sl': active_trade['sl'],
                    'tp': active_trade['tp'],
                    'pnl': pnl,
                    'result': result,
                    'risk': active_trade['risk']
                }
                trades.append(trade_record)
                active_trade = None
                continue
            
            # Check for new signals (only if no active trade and not traded today)
            if current_date not in traded_dates and not active_trade:
                # Check if in killzone
                if not current_row['In_Killzone']:
                    continue
                
                # Check for Long signal
                if current_row['Long_Signal']:
                    entry = current_row['Signal_Entry']
                    sl = current_row['Signal_SL']
                    risk = entry - sl
                    tp = entry + risk  # 1:1 R/R
                    
                    active_trade = {
                        'entry_time': current_time,
                        'direction': 'Long',
                        'entry': entry,
                        'sl': sl,
                        'tp': tp,
                        'risk': risk
                    }
                    traded_dates.add(current_date)
                
                # Check for Short signal
                elif current_row['Short_Signal']:
                    entry = current_row['Signal_Entry']
                    sl = current_row['Signal_SL']
                    risk = sl - entry
                    tp = entry - risk  # 1:1 R/R
                    
                    active_trade = {
                        'entry_time': current_time,
                        'direction': 'Short',
                        'entry': entry,
                        'sl': sl,
                        'tp': tp,
                        'risk': risk
                    }
                    traded_dates.add(current_date)
        
        self.trades = trades
        print(f"Executed {len(trades)} trades")
        
    def calculate_performance(self):
        """Calculate performance metrics"""
        print("\nCalculating performance metrics...")
        
        if not self.trades:
            print("No trades to analyze!")
            return
        
        trades_df = pd.DataFrame(self.trades)
        
        # Total trades
        total_trades = len(trades_df)
        
        # Win/Loss breakdown
        wins = len(trades_df[trades_df['result'] == 'Win'])
        losses = len(trades_df[trades_df['result'] == 'Loss'])
        force_closes = len(trades_df[trades_df['result'] == 'Force Close'])
        
        # Win rate
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        # PnL statistics
        total_pnl = trades_df['pnl'].sum()
        gross_profit = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(trades_df[trades_df['pnl'] < 0]['pnl'].sum())
        
        # Profit factor
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else np.inf
        
        # Cumulative returns
        trades_df['cumulative_pnl'] = trades_df['pnl'].cumsum()
        
        # Max drawdown
        cumulative = trades_df['cumulative_pnl']
        running_max = cumulative.cummax()
        drawdown = cumulative - running_max
        max_drawdown = drawdown.min()
        
        # Average trade
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if wins > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losses > 0 else 0
        avg_trade = trades_df['pnl'].mean()
        
        # Store performance metrics
        self.performance = {
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'force_closes': force_closes,
            'win_rate': win_rate,
            'total_return': total_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'avg_trade': avg_trade
        }
        
        # Store trades dataframe
        self.trades_df = trades_df
        
    def print_performance(self):
        """Print performance metrics"""
        print("\n" + "="*60)
        print("PERFORMANCE METRICS")
        print("="*60)
        print(f"Total Trades: {self.performance['total_trades']}")
        print(f"Wins: {self.performance['wins']}")
        print(f"Losses: {self.performance['losses']}")
        print(f"Force Closes: {self.performance['force_closes']}")
        print(f"Win Rate: {self.performance['win_rate']:.2f}%")
        print(f"\nTotal Return: {self.performance['total_return']:.2f} points")
        print(f"Gross Profit: {self.performance['gross_profit']:.2f} points")
        print(f"Gross Loss: {self.performance['gross_loss']:.2f} points")
        print(f"Profit Factor: {self.performance['profit_factor']:.2f}")
        print(f"Max Drawdown: {self.performance['max_drawdown']:.2f} points")
        print(f"\nAverage Win: {self.performance['avg_win']:.2f} points")
        print(f"Average Loss: {self.performance['avg_loss']:.2f} points")
        print(f"Average Trade: {self.performance['avg_trade']:.2f} points")
        print("="*60)
        
    def plot_results(self, save_path='backtest_results.png'):
        """
        Plot backtest results
        
        Args:
            save_path: Path to save the plot
        """
        if not self.trades:
            print("No trades to plot!")
            return
        
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        
        # Plot 1: Cumulative PnL
        ax1 = axes[0]
        cumulative_pnl = self.trades_df['cumulative_pnl']
        ax1.plot(cumulative_pnl.values, linewidth=2, color='blue')
        ax1.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax1.set_title('Cumulative PnL (Points)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Trade Number')
        ax1.set_ylabel('Cumulative PnL (Points)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Individual Trade PnL
        ax2 = axes[1]
        colors = ['green' if pnl > 0 else 'red' for pnl in self.trades_df['pnl']]
        ax2.bar(range(len(self.trades_df)), self.trades_df['pnl'], color=colors, alpha=0.7)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax2.set_title('Individual Trade PnL', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Trade Number')
        ax2.set_ylabel('PnL (Points)')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Drawdown
        ax3 = axes[2]
        cumulative = self.trades_df['cumulative_pnl']
        running_max = cumulative.cummax()
        drawdown = cumulative - running_max
        ax3.fill_between(range(len(drawdown)), drawdown.values, 0, color='red', alpha=0.3)
        ax3.plot(drawdown.values, color='red', linewidth=2)
        ax3.set_title('Drawdown', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Trade Number')
        ax3.set_ylabel('Drawdown (Points)')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nPlot saved to: {save_path}")
        plt.close()
        
    def plot_trades_on_chart(self, start_date=None, end_date=None, save_path='trades_chart.png'):
        """
        Plot price chart with trades marked
        
        Args:
            start_date: Start date for chart (None = use first trade date)
            end_date: End date for chart (None = use last trade date)
            save_path: Path to save the plot
        """
        if not self.trades:
            print("No trades to plot!")
            return
        
        trades_df = self.trades_df
        
        # Determine date range
        if start_date is None:
            start_date = trades_df['entry_time'].min()
        if end_date is None:
            end_date = trades_df['exit_time'].max()
        
        # Filter data for date range
        mask = (self.df.index >= start_date) & (self.df.index <= end_date)
        df_plot = self.df[mask]
        
        if len(df_plot) == 0:
            print("No data in specified date range!")
            return
        
        # Create figure
        fig, ax = plt.subplots(figsize=(20, 10))
        
        # Plot price
        ax.plot(df_plot.index, df_plot['Close'], linewidth=1, color='black', label='Close Price')
        ax.plot(df_plot.index, df_plot['VWAP'], linewidth=1, color='orange', alpha=0.7, label='VWAP')
        
        # Plot trades
        for _, trade in trades_df.iterrows():
            if trade['entry_time'] >= start_date and trade['entry_time'] <= end_date:
                # Entry marker
                if trade['direction'] == 'Long':
                    ax.scatter(trade['entry_time'], trade['entry_price'], 
                             color='green', marker='^', s=200, zorder=5, label='Long Entry' if _ == 0 else '')
                else:
                    ax.scatter(trade['entry_time'], trade['entry_price'], 
                             color='red', marker='v', s=200, zorder=5, label='Short Entry' if _ == 0 else '')
                
                # Exit marker
                if trade['result'] == 'Win':
                    exit_color = 'blue'
                    exit_marker = '*'
                elif trade['result'] == 'Loss':
                    exit_color = 'purple'
                    exit_marker = 'x'
                else:
                    exit_color = 'gray'
                    exit_marker = 'o'
                
                ax.scatter(trade['exit_time'], trade['exit_price'], 
                         color=exit_color, marker=exit_marker, s=150, zorder=5)
                
                # Draw line from entry to exit
                ax.plot([trade['entry_time'], trade['exit_time']], 
                       [trade['entry_price'], trade['exit_price']], 
                       color='blue' if trade['result'] == 'Win' else 'red', 
                       linestyle='--', linewidth=1, alpha=0.5)
        
        ax.set_title('NQ Price Chart with Trades', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date/Time')
        ax.set_ylabel('Price')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Trades chart saved to: {save_path}")
        plt.close()
        
    def run_backtest(self):
        """Run the complete backtest"""
        print("\n" + "="*60)
        print("STARTING NQ FVG INVERSION STRATEGY BACKTEST")
        print("="*60 + "\n")
        
        # Step 1: Load data
        self.load_data()
        
        # Step 2: Calculate VWAP
        self.calculate_vwap()
        
        # Step 3: Detect FVGs
        self.detect_fvg()
        
        # Step 4: Apply time filter
        self.apply_time_filter()
        
        # Step 5: Detect FVG inversions
        self.detect_fvg_inversions()
        
        # Step 6: Apply VWAP filter
        self.apply_vwap_filter()
        
        # Step 7: Execute trades
        self.execute_trades()
        
        # Step 8: Calculate performance
        self.calculate_performance()
        
        # Step 9: Print results
        self.print_performance()
        
        # Step 10: Plot results
        self.plot_results()
        
        print("\n" + "="*60)
        print("BACKTEST COMPLETED")
        print("="*60)
        
        return self.performance, self.trades_df


def main():
    """Main execution function"""
    # Initialize backtester
    backtester = NQFVGBacktester()
    
    # Run backtest
    performance, trades = backtester.run_backtest()
    
    # Optional: Plot a sample of trades on price chart (first 100 trades)
    if len(trades) > 0:
        print("\nGenerating trades chart for first period...")
        # Get date range for first 50 trades
        if len(trades) >= 50:
            start = trades.iloc[0]['entry_time']
            end = trades.iloc[49]['exit_time']
            backtester.plot_trades_on_chart(start_date=start, end_date=end, 
                                           save_path='trades_chart_sample.png')
    
    # Save trades to CSV
    if len(trades) > 0:
        trades.to_csv('backtest_trades.csv', index=False)
        print(f"\nTrades saved to: backtest_trades.csv")
    
    return backtester


if __name__ == "__main__":
    backtester = main()
