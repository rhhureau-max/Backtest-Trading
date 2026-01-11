"""
NQ Futures FVG (Fair Value Gap) Inversion Backtesting Script
=============================================================

Strategy:
- Detects Bearish and Bullish FVGs on 3-minute data
- Enters LONG when price closes above a Bearish FVG
- Enters SHORT when price closes below a Bullish FVG

Session Constraints:
- London killzone: 01:00-04:00 CT
- New York killzone: 08:30-11:00 CT
- One Bullet Rule: Only first valid signal per session

Risk Management:
- Stop Loss: Below/Above signal candle low/high
- Take Profit: 1:1 Risk-to-Reward ratio
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import sys
import os


class FVGInversionBacktest:
    """Backtest engine for FVG Inversion strategy on NQ Futures"""
    
    def __init__(self, csv_file):
        """
        Initialize the backtest with data file
        
        Parameters:
        -----------
        csv_file : str
            Path to the CSV file containing 1-minute NQ data
        """
        self.csv_file = csv_file
        self.data = None
        self.data_3min = None
        self.trades = []
        self.equity_curve = []
        
        # Session definitions (Chicago Time)
        self.london_start = time(1, 0)
        self.london_end = time(4, 0)
        self.ny_start = time(8, 30)
        self.ny_end = time(11, 0)
        
    def load_and_preprocess_data(self):
        """Load CSV data and convert to proper datetime format"""
        print("Loading data from CSV...")
        
        try:
            # Load data with semicolon separator
            df = pd.read_csv(self.csv_file, sep=';')
            
            # Handle column names - rename if needed
            if 'Column1' in df.columns:
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Combine Date and Time columns
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S')
            
            # Set DateTime as index
            df.set_index('DateTime', inplace=True)
            
            # Keep only OHLC columns
            df = df[['Open', 'High', 'Low', 'Close']]
            
            # Sort by datetime
            df.sort_index(inplace=True)
            
            self.data = df
            print(f"Loaded {len(df)} records from {df.index[0]} to {df.index[-1]}")
            
            return True
            
        except FileNotFoundError:
            print(f"ERROR: File '{self.csv_file}' not found!")
            return False
        except Exception as e:
            print(f"ERROR loading data: {e}")
            return False
    
    def resample_to_3min(self):
        """Resample 1-minute data to 3-minute timeframe"""
        print("Resampling to 3-minute timeframe...")
        
        try:
            # Resample with proper OHLC aggregation
            resampled = self.data.resample('3min').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last'
            })
            
            # Drop any NaN rows (incomplete periods)
            resampled.dropna(inplace=True)
            
            self.data_3min = resampled
            print(f"Resampled to {len(resampled)} 3-minute bars")
            
            return True
            
        except Exception as e:
            print(f"ERROR resampling data: {e}")
            return False
    
    def detect_fvgs(self):
        """
        Detect Fair Value Gaps in the 3-minute data
        
        Bearish FVG: Low[i-2] > High[i] -> Gap between High[i] and Low[i-2]
        Bullish FVG: High[i-2] < Low[i] -> Gap between High[i-2] and Low[i]
        """
        df = self.data_3min.copy()
        
        # Initialize FVG columns
        df['Bearish_FVG_Top'] = np.nan
        df['Bearish_FVG_Bottom'] = np.nan
        df['Bullish_FVG_Top'] = np.nan
        df['Bullish_FVG_Bottom'] = np.nan
        
        # Detect FVGs (need at least 3 candles)
        for i in range(2, len(df)):
            # Bearish FVG: Low[i-2] > High[i]
            if df['Low'].iloc[i-2] > df['High'].iloc[i]:
                df.iloc[i, df.columns.get_loc('Bearish_FVG_Top')] = df['Low'].iloc[i-2]
                df.iloc[i, df.columns.get_loc('Bearish_FVG_Bottom')] = df['High'].iloc[i]
            
            # Bullish FVG: High[i-2] < Low[i]
            if df['High'].iloc[i-2] < df['Low'].iloc[i]:
                df.iloc[i, df.columns.get_loc('Bullish_FVG_Top')] = df['Low'].iloc[i]
                df.iloc[i, df.columns.get_loc('Bullish_FVG_Bottom')] = df['High'].iloc[i-2]
        
        self.data_3min = df
        
        # Count detected FVGs
        bearish_count = df['Bearish_FVG_Top'].notna().sum()
        bullish_count = df['Bullish_FVG_Top'].notna().sum()
        print(f"Detected {bearish_count} Bearish FVGs and {bullish_count} Bullish FVGs")
    
    def get_session(self, dt):
        """
        Determine which trading session a datetime belongs to
        
        Parameters:
        -----------
        dt : datetime
            The datetime to check
            
        Returns:
        --------
        str : 'London', 'New York', or None
        """
        t = dt.time()
        
        # Check London session (01:00-04:00)
        if self.london_start <= t < self.london_end:
            return 'London'
        
        # Check New York session (08:30-11:00)
        if self.ny_start <= t < self.ny_end:
            return 'New York'
        
        return None
    
    def run_backtest(self):
        """Execute the FVG Inversion backtest strategy"""
        print("\nRunning backtest...")
        
        df = self.data_3min.copy()
        
        # Track active FVGs (most recent ones)
        active_bearish_fvg = None  # (top, bottom, created_index)
        active_bullish_fvg = None  # (top, bottom, created_index)
        
        # Track session state
        current_session = None
        current_session_date = None
        session_traded = False
        
        # Track open position
        open_position = None  # {'type': 'LONG/SHORT', 'entry': price, 'sl': price, 'tp': price, ...}
        
        total_bars = len(df)
        
        for i in range(2, total_bars):
            current_dt = df.index[i]
            current_time = current_dt.time()
            current_date = current_dt.date()
            session = self.get_session(current_dt)
            
            # Update session tracking
            if session != current_session or current_date != current_session_date:
                # New session or new day
                if session == 'New York':
                    # Reset on New York session start
                    session_traded = False
                current_session = session
                current_session_date = current_date
            
            # Skip if not in a trading session
            if session is None:
                continue
            
            # Update active FVGs if new ones are created
            if pd.notna(df['Bearish_FVG_Top'].iloc[i]):
                active_bearish_fvg = (
                    df['Bearish_FVG_Top'].iloc[i],
                    df['Bearish_FVG_Bottom'].iloc[i],
                    i
                )
            
            if pd.notna(df['Bullish_FVG_Top'].iloc[i]):
                active_bullish_fvg = (
                    df['Bullish_FVG_Top'].iloc[i],
                    df['Bullish_FVG_Bottom'].iloc[i],
                    i
                )
            
            # Check if we have an open position - manage exit
            if open_position is not None:
                high = df['High'].iloc[i]
                low = df['Low'].iloc[i]
                
                if open_position['type'] == 'LONG':
                    # Check stop loss
                    if low <= open_position['sl']:
                        # Stop loss hit
                        exit_price = open_position['sl']
                        pnl = exit_price - open_position['entry']
                        self._close_trade(open_position, current_dt, exit_price, pnl, 'Stop Loss')
                        open_position = None
                        continue
                    
                    # Check take profit
                    if high >= open_position['tp']:
                        # Take profit hit
                        exit_price = open_position['tp']
                        pnl = exit_price - open_position['entry']
                        self._close_trade(open_position, current_dt, exit_price, pnl, 'Take Profit')
                        open_position = None
                        continue
                
                elif open_position['type'] == 'SHORT':
                    # Check stop loss
                    if high >= open_position['sl']:
                        # Stop loss hit
                        exit_price = open_position['sl']
                        pnl = open_position['entry'] - exit_price
                        self._close_trade(open_position, current_dt, exit_price, pnl, 'Stop Loss')
                        open_position = None
                        continue
                    
                    # Check take profit
                    if low <= open_position['tp']:
                        # Take profit hit
                        exit_price = open_position['tp']
                        pnl = open_position['entry'] - exit_price
                        self._close_trade(open_position, current_dt, exit_price, pnl, 'Take Profit')
                        open_position = None
                        continue
            
            # Check for new entry signals (only if no position and haven't traded in this session)
            if open_position is None and not session_traded:
                close_price = df['Close'].iloc[i]
                high = df['High'].iloc[i]
                low = df['Low'].iloc[i]
                
                # LONG Signal: Bearish FVG exists and close is ABOVE its top
                if active_bearish_fvg is not None:
                    fvg_top, fvg_bottom, fvg_idx = active_bearish_fvg
                    
                    # Check if FVG was created before current candle
                    if fvg_idx < i and close_price > fvg_top:
                        # Enter LONG
                        entry_price = close_price
                        stop_loss = low
                        risk = entry_price - stop_loss
                        take_profit = entry_price + risk  # 1:1 RR
                        
                        open_position = {
                            'type': 'LONG',
                            'entry': entry_price,
                            'sl': stop_loss,
                            'tp': take_profit,
                            'entry_time': current_dt,
                            'session': session,
                            'risk': risk
                        }
                        
                        session_traded = True
                        continue
                
                # SHORT Signal: Bullish FVG exists and close is BELOW its bottom
                if active_bullish_fvg is not None:
                    fvg_top, fvg_bottom, fvg_idx = active_bullish_fvg
                    
                    # Check if FVG was created before current candle
                    if fvg_idx < i and close_price < fvg_bottom:
                        # Enter SHORT
                        entry_price = close_price
                        stop_loss = high
                        risk = stop_loss - entry_price
                        take_profit = entry_price - risk  # 1:1 RR
                        
                        open_position = {
                            'type': 'SHORT',
                            'entry': entry_price,
                            'sl': stop_loss,
                            'tp': take_profit,
                            'entry_time': current_dt,
                            'session': session,
                            'risk': risk
                        }
                        
                        session_traded = True
                        continue
        
        print(f"Backtest complete. Total trades: {len(self.trades)}")
    
    def _close_trade(self, position, exit_time, exit_price, pnl, exit_reason):
        """Record a closed trade"""
        trade = {
            'Entry Time': position['entry_time'],
            'Exit Time': exit_time,
            'Type': position['type'],
            'Session': position['session'],
            'Entry Price': position['entry'],
            'Exit Price': exit_price,
            'Stop Loss': position['sl'],
            'Take Profit': position['tp'],
            'Risk': position['risk'],
            'PnL': pnl,
            'Exit Reason': exit_reason,
            'Win': pnl > 0
        }
        self.trades.append(trade)
        
        # Update equity curve
        if len(self.equity_curve) == 0:
            self.equity_curve.append({'Time': exit_time, 'Equity': pnl})
        else:
            prev_equity = self.equity_curve[-1]['Equity']
            self.equity_curve.append({'Time': exit_time, 'Equity': prev_equity + pnl})
    
    def generate_statistics(self):
        """Generate and print performance statistics"""
        if len(self.trades) == 0:
            print("\nNo trades were executed during the backtest period.")
            return
        
        df_trades = pd.DataFrame(self.trades)
        
        print("\n" + "="*70)
        print("BACKTEST RESULTS - FVG INVERSION STRATEGY")
        print("="*70)
        
        # Overall statistics
        total_trades = len(df_trades)
        winning_trades = df_trades['Win'].sum()
        losing_trades = total_trades - winning_trades
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        gross_profit = df_trades[df_trades['PnL'] > 0]['PnL'].sum()
        gross_loss = abs(df_trades[df_trades['PnL'] < 0]['PnL'].sum())
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else np.inf
        net_profit = df_trades['PnL'].sum()
        
        print(f"\nOVERALL STATISTICS:")
        print(f"  Total Trades:    {total_trades}")
        print(f"  Winning Trades:  {winning_trades}")
        print(f"  Losing Trades:   {losing_trades}")
        print(f"  Win Rate:        {win_rate:.2f}%")
        print(f"  Profit Factor:   {profit_factor:.2f}")
        print(f"  Net Profit:      {net_profit:.2f} points")
        print(f"  Gross Profit:    {gross_profit:.2f} points")
        print(f"  Gross Loss:      {gross_loss:.2f} points")
        
        # Statistics by session
        print(f"\n{'-'*70}")
        print("STATISTICS BY SESSION:")
        print(f"{'-'*70}")
        
        for session in ['London', 'New York']:
            session_trades = df_trades[df_trades['Session'] == session]
            
            if len(session_trades) == 0:
                print(f"\n{session.upper()} SESSION: No trades")
                continue
            
            s_total = len(session_trades)
            s_wins = session_trades['Win'].sum()
            s_losses = s_total - s_wins
            s_win_rate = (s_wins / s_total * 100) if s_total > 0 else 0
            
            s_gross_profit = session_trades[session_trades['PnL'] > 0]['PnL'].sum()
            s_gross_loss = abs(session_trades[session_trades['PnL'] < 0]['PnL'].sum())
            s_profit_factor = (s_gross_profit / s_gross_loss) if s_gross_loss > 0 else np.inf
            s_net_profit = session_trades['PnL'].sum()
            
            print(f"\n{session.upper()} SESSION:")
            print(f"  Total Trades:    {s_total}")
            print(f"  Winning Trades:  {s_wins}")
            print(f"  Losing Trades:   {s_losses}")
            print(f"  Win Rate:        {s_win_rate:.2f}%")
            print(f"  Profit Factor:   {s_profit_factor:.2f}")
            print(f"  Net Profit:      {s_net_profit:.2f} points")
        
        print("\n" + "="*70)
    
    def plot_equity_curve(self):
        """Plot the cumulative equity curve"""
        if len(self.equity_curve) == 0:
            print("No equity data to plot.")
            return
        
        df_equity = pd.DataFrame(self.equity_curve)
        
        plt.figure(figsize=(14, 7))
        plt.plot(df_equity['Time'], df_equity['Equity'], linewidth=2, color='blue')
        plt.title('FVG Inversion Strategy - Cumulative Equity Curve', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Cumulative Profit/Loss (Points)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='r', linestyle='--', linewidth=1)
        
        # Add shading for profit/loss regions
        plt.fill_between(df_equity['Time'], df_equity['Equity'], 0, 
                        where=(df_equity['Equity'] >= 0), alpha=0.3, color='green', label='Profit')
        plt.fill_between(df_equity['Time'], df_equity['Equity'], 0, 
                        where=(df_equity['Equity'] < 0), alpha=0.3, color='red', label='Loss')
        
        plt.legend(loc='best')
        plt.tight_layout()
        
        # Save plot
        output_file = 'fvg_inversion_equity_curve.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nEquity curve saved to: {output_file}")
        
        # Show plot
        plt.show()
    
    def export_trades(self, filename='fvg_inversion_trades.csv'):
        """Export all trades to CSV file"""
        if len(self.trades) == 0:
            print("No trades to export.")
            return
        
        df_trades = pd.DataFrame(self.trades)
        df_trades.to_csv(filename, index=False)
        print(f"Trades exported to: {filename}")


def main():
    """Main execution function"""
    print("="*70)
    print("NQ FUTURES - FVG INVERSION BACKTEST")
    print("="*70)
    
    # Define input file
    input_file = 'NQ_1min_2018_2024.csv'
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"\nERROR: Input file '{input_file}' not found!")
        print("Please ensure the file exists in the current directory.")
        print("\nExpected format:")
        print("  - Semicolon-separated CSV")
        print("  - Columns: Date, Time, Open, High, Low, Close")
        print("  - Date format: DD/MM/YYYY")
        print("  - Time format: HH:MM:SS")
        print("  - All times in Chicago Time (CT)")
        return
    
    # Initialize backtest
    backtest = FVGInversionBacktest(input_file)
    
    # Load and process data
    if not backtest.load_and_preprocess_data():
        return
    
    if not backtest.resample_to_3min():
        return
    
    # Detect FVGs
    backtest.detect_fvgs()
    
    # Run backtest
    backtest.run_backtest()
    
    # Generate results
    backtest.generate_statistics()
    
    # Export trades
    backtest.export_trades()
    
    # Plot equity curve
    backtest.plot_equity_curve()
    
    print("\nBacktest completed successfully!")


if __name__ == "__main__":
    main()
