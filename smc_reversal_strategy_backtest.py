"""
SMC Reversal Strategy Backtest - NQ 5-Minute Data (2018-2025)
==============================================================

Strategy: Reversal trading during 01:00-07:00 session using Smart Money Concepts

Logic:
1. Identify Fractal Highs/Lows (6-candle lookback)
2. Detect Sweep: Price exceeds Fractal High but closes below or reverses within 3 candles
3. Confirm MSS: Price breaks the last Fractal Low that led to the high
4. Entry: 50% Fibonacci retracement of the bearish leg (Sweep High to MSS Low)
5. Stop Loss: Above the Sweep High
6. Take Profit: First unfilled FVG (Fair Value Gap) created during MSS leg

Author: SMC Strategy Expert
Date: 2025-12-12
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import glob
import warnings
warnings.filterwarnings('ignore')


class SMCReversalBacktest:
    """
    Backtest SMC Reversal Strategy on NQ 5-minute data.
    """
    
    # Constants
    NQ_POINT_VALUE = 20  # $20 per point for NQ futures
    
    def __init__(self, data_files_pattern, session_start='01:00:00', session_end='07:00:00'):
        """
        Initialize the backtest.
        
        Parameters:
        -----------
        data_files_pattern : str
            Pattern to match NQ 5-minute CSV files (e.g., '*5m.csv')
        session_start : str
            Session start time (HH:MM:SS)
        session_end : str
            Session end time (HH:MM:SS)
        """
        self.data_files_pattern = data_files_pattern
        self.session_start = session_start
        self.session_end = session_end
        self.df = None
        self.trades = []
        
    def load_data(self):
        """Load and prepare NQ 5-minute data from all years."""
        print("Loading NQ 5-minute data...")
        
        # Find all matching CSV files
        files = sorted(glob.glob(self.data_files_pattern))
        
        if len(files) == 0:
            raise FileNotFoundError(f"No CSV files found matching pattern: {self.data_files_pattern}")
        
        print(f"Found {len(files)} data files")
        
        # Load all files
        dfs = []
        for file in files:
            try:
                df_temp = pd.read_csv(file, sep=';')
                # Rename columns
                df_temp.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                dfs.append(df_temp)
                print(f"  Loaded {file}: {len(df_temp)} rows")
            except Exception as e:
                print(f"  Error loading {file}: {e}")
        
        # Combine all data
        self.df = pd.concat(dfs, ignore_index=True)
        print(f"\nTotal rows loaded: {len(self.df)}")
        
        # Parse datetime
        self.df['DateTime'] = pd.to_datetime(
            self.df['Date'] + ' ' + self.df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Sort by datetime
        self.df = self.df.sort_values('DateTime').reset_index(drop=True)
        
        # Extract date and time components
        self.df['DateOnly'] = self.df['DateTime'].dt.date
        self.df['TimeOnly'] = self.df['DateTime'].dt.time
        
        print(f"Date range: {self.df['DateTime'].min()} to {self.df['DateTime'].max()}")
        print(f"Data prepared successfully!\n")
        
        return self.df
    
    def detect_fractals(self, lookback=6):
        """
        Detect Fractal Highs and Lows.
        
        A Fractal High must be higher than the previous 6 candles.
        A Fractal Low must be lower than the previous 6 candles.
        
        Parameters:
        -----------
        lookback : int
            Number of candles to look back for fractal detection
        """
        print(f"Detecting fractals with {lookback}-candle lookback...")
        
        # Initialize columns
        self.df['FractalHigh'] = False
        self.df['FractalLow'] = False
        
        # Optimized rolling window approach
        highs = self.df['High'].values
        lows = self.df['Low'].values
        
        for i in range(lookback, len(self.df)):
            # Check if current high is higher than previous lookback candles
            if highs[i] > highs[i-lookback:i].max():
                self.df.loc[i, 'FractalHigh'] = True
            
            # Check if current low is lower than previous lookback candles
            if lows[i] < lows[i-lookback:i].min():
                self.df.loc[i, 'FractalLow'] = True
        
        fractal_highs = self.df['FractalHigh'].sum()
        fractal_lows = self.df['FractalLow'].sum()
        print(f"Found {fractal_highs} Fractal Highs and {fractal_lows} Fractal Lows\n")
        
        return self.df
    
    def detect_fvg_bearish(self):
        """
        Detect Bearish FVG (Fair Value Gap).
        
        Bearish FVG: Gap between High[i] and Low[i-2]
        When High[i] < Low[i-2], there's a gap down
        """
        print("Detecting Bearish FVGs...")
        
        self.df['FVG_Bearish'] = False
        self.df['FVG_Top'] = np.nan
        self.df['FVG_Bottom'] = np.nan
        
        for i in range(2, len(self.df)):
            # Bearish FVG: High[i] < Low[i-2]
            if self.df.loc[i, 'High'] < self.df.loc[i-2, 'Low']:
                self.df.loc[i, 'FVG_Bearish'] = True
                self.df.loc[i, 'FVG_Top'] = self.df.loc[i-2, 'Low']
                self.df.loc[i, 'FVG_Bottom'] = self.df.loc[i, 'High']
        
        fvg_count = self.df['FVG_Bearish'].sum()
        print(f"Found {fvg_count} Bearish FVGs\n")
        
        return self.df
    
    def filter_session_data(self):
        """Filter data to only include the 01:00-07:00 session."""
        print(f"Filtering data for session {self.session_start} - {self.session_end}...")
        
        session_start_time = datetime.strptime(self.session_start, '%H:%M:%S').time()
        session_end_time = datetime.strptime(self.session_end, '%H:%M:%S').time()
        
        mask = (self.df['TimeOnly'] >= session_start_time) & (self.df['TimeOnly'] <= session_end_time)
        session_df = self.df[mask].copy()
        
        print(f"Session data: {len(session_df)} rows ({len(session_df) / len(self.df) * 100:.2f}% of total)")
        print(f"Unique dates: {session_df['DateOnly'].nunique()}\n")
        
        return session_df
    
    def find_sweep_opportunities(self, session_df):
        """
        Find Sweep opportunities within a session.
        
        Sweep: Price exceeds a Fractal High but:
        - Closes below that high (wick rejection), OR
        - Shows reversal within next 3 candles
        
        Returns list of sweep opportunities with details.
        """
        sweeps = []
        
        # Get all fractal highs in this session
        fractal_highs = session_df[session_df['FractalHigh'] == True].copy()
        
        for idx, fractal_row in fractal_highs.iterrows():
            fractal_high = fractal_row['High']
            fractal_time = fractal_row['DateTime']
            
            # Look for sweeps after this fractal
            future_mask = session_df['DateTime'] > fractal_time
            future_candles = session_df[future_mask].copy()
            
            for f_idx, candle in future_candles.iterrows():
                # Check if price exceeds the fractal high
                if candle['High'] > fractal_high:
                    # Check condition: closes below the high (wick)
                    closes_below = candle['Close'] < fractal_high
                    
                    # Check condition: reversal within 3 candles
                    reversal_within_3 = False
                    next_3_candles = future_candles[future_candles['DateTime'] > candle['DateTime']].head(3)
                    if len(next_3_candles) > 0:
                        # Reversal = any of next 3 candles closes below fractal high
                        reversal_within_3 = (next_3_candles['Close'] < fractal_high).any()
                    
                    # If either condition met, it's a sweep
                    if closes_below or reversal_within_3:
                        sweeps.append({
                            'date': candle['DateOnly'],
                            'sweep_time': candle['DateTime'],
                            'sweep_idx': f_idx,
                            'sweep_high': candle['High'],
                            'fractal_high': fractal_high,
                            'fractal_time': fractal_time,
                            'fractal_idx': idx
                        })
                        break  # Only take first sweep of this fractal
        
        return sweeps
    
    def check_mss(self, session_df, sweep):
        """
        Check for MSS (Market Structure Shift) after a sweep.
        
        MSS: Price breaks the last significant Fractal Low that led to the swept high.
        
        Returns MSS details if found, None otherwise.
        """
        # Find fractal lows between the fractal high and the sweep
        mask = ((session_df['DateTime'] > sweep['fractal_time']) & 
                (session_df['DateTime'] < sweep['sweep_time']) & 
                (session_df['FractalLow'] == True))
        
        fractal_lows_between = session_df[mask]
        
        if len(fractal_lows_between) == 0:
            return None
        
        # Get the last (most recent) fractal low before the sweep
        last_fractal_low = fractal_lows_between.iloc[-1]
        fractal_low_value = last_fractal_low['Low']
        
        # Look for price breaking below this fractal low after the sweep
        future_mask = session_df['DateTime'] > sweep['sweep_time']
        future_candles = session_df[future_mask]
        
        for idx, candle in future_candles.iterrows():
            if candle['Low'] < fractal_low_value:
                # MSS confirmed!
                return {
                    'mss_time': candle['DateTime'],
                    'mss_idx': idx,
                    'mss_low': candle['Low'],
                    'fractal_low_value': fractal_low_value,
                    'fractal_low_time': last_fractal_low['DateTime']
                }
        
        return None
    
    def calculate_fibonacci_entry(self, sweep_high, mss_low):
        """
        Calculate 50% Fibonacci retracement entry.
        
        Parameters:
        -----------
        sweep_high : float
            High of the sweep candle
        mss_low : float
            Low of the MSS candle
        
        Returns:
        --------
        float : Entry price at 50% retracement
        """
        return sweep_high - (sweep_high - mss_low) * 0.5
    
    def find_first_unfilled_fvg(self, session_df, mss_details, entry_time):
        """
        Find the first unfilled FVG created during the MSS leg.
        
        An FVG is considered unfilled if price hasn't retraced into it yet.
        """
        # Get FVGs created during or after MSS and before entry
        mask = ((session_df['DateTime'] >= mss_details['mss_time']) & 
                (session_df['DateTime'] <= entry_time) &
                (session_df['FVG_Bearish'] == True))
        
        fvgs = session_df[mask]
        
        if len(fvgs) == 0:
            return None
        
        # Take the first FVG
        first_fvg = fvgs.iloc[0]
        
        # Check if it's still unfilled at entry time
        # FVG is filled if price has gone back up into it
        future_mask = ((session_df['DateTime'] > first_fvg['DateTime']) & 
                       (session_df['DateTime'] <= entry_time))
        future_candles = session_df[future_mask]
        
        fvg_top = first_fvg['FVG_Top']
        fvg_bottom = first_fvg['FVG_Bottom']
        
        # Check if any future candle went back into the FVG
        filled = (future_candles['High'] >= fvg_bottom).any()
        
        if not filled:
            return {
                'fvg_top': fvg_top,
                'fvg_bottom': fvg_bottom,
                'fvg_time': first_fvg['DateTime']
            }
        
        # If first FVG is filled, try next ones
        for idx, fvg_row in fvgs.iloc[1:].iterrows():
            fvg_top = fvg_row['FVG_Top']
            fvg_bottom = fvg_row['FVG_Bottom']
            
            future_mask = ((session_df['DateTime'] > fvg_row['DateTime']) & 
                          (session_df['DateTime'] <= entry_time))
            future_candles = session_df[future_mask]
            
            filled = (future_candles['High'] >= fvg_bottom).any()
            
            if not filled:
                return {
                    'fvg_top': fvg_top,
                    'fvg_bottom': fvg_bottom,
                    'fvg_time': fvg_row['DateTime']
                }
        
        return None
    
    def simulate_trade(self, session_df, all_df, sweep, mss_details, entry_price, stop_loss, take_profit):
        """
        Simulate a single SHORT trade and track its outcome.
        
        Returns trade result dictionary.
        """
        # Entry is after MSS confirmation
        entry_time = mss_details['mss_time']
        
        # Look for price reaching entry level (price must retrace UP to entry)
        future_mask = (session_df['DateTime'] > entry_time)
        future_candles = session_df[future_mask]
        
        entry_filled = False
        entry_filled_time = None
        entry_filled_idx = None
        
        # Check if entry gets filled (price retraces up to 50% fib on a SHORT trade)
        for idx, candle in future_candles.iterrows():
            # For SHORT: Entry filled if price reaches or goes above entry price
            if candle['High'] >= entry_price:
                entry_filled = True
                entry_filled_time = candle['DateTime']
                entry_filled_idx = idx
                break
        
        if not entry_filled:
            return None  # Entry never filled
        
        # Now simulate the SHORT trade after entry
        # Look at all data after entry (can exit after 07:00)
        after_entry_mask = (all_df['DateTime'] > entry_filled_time)
        after_entry_candles = all_df[after_entry_mask]
        
        trade_result = {
            'date': sweep['date'],
            'entry_time': entry_filled_time,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'sweep_high': sweep['sweep_high'],
            'mss_low': mss_details['mss_low'],
            'outcome': None,
            'exit_price': None,
            'exit_time': None,
            'pnl_points': None,
            'risk_points': None,
            'rr_ratio': None
        }
        
        # Check each candle for SL or TP hit
        for idx, candle in after_entry_candles.iterrows():
            # For SHORT trade:
            # Stop loss hit when price goes ABOVE stop loss
            if candle['High'] >= stop_loss:
                trade_result['outcome'] = 'Loss'
                trade_result['exit_price'] = stop_loss
                trade_result['exit_time'] = candle['DateTime']
                # SHORT P&L: Entry - Exit (negative when SL hit)
                trade_result['pnl_points'] = entry_price - stop_loss
                break
            
            # Take profit hit when price goes AT OR BELOW take profit
            if candle['Low'] <= take_profit:
                trade_result['outcome'] = 'Win'
                trade_result['exit_price'] = take_profit
                trade_result['exit_time'] = candle['DateTime']
                # SHORT P&L: Entry - Exit (positive when TP hit)
                trade_result['pnl_points'] = entry_price - take_profit
                break
        
        # If no exit found in data
        if trade_result['outcome'] is None:
            return None
        
        # Calculate risk and R:R ratio
        # For SHORT: Risk = Stop Loss - Entry (positive value)
        trade_result['risk_points'] = stop_loss - entry_price
        if trade_result['risk_points'] > 0:
            trade_result['rr_ratio'] = trade_result['pnl_points'] / trade_result['risk_points']
        
        return trade_result
    
    def run_backtest(self):
        """
        Run the complete backtest on all data.
        """
        print("="*80)
        print("Starting SMC Reversal Strategy Backtest")
        print("="*80)
        
        # Load data
        self.load_data()
        
        # Detect fractals
        self.detect_fractals(lookback=6)
        
        # Detect FVGs
        self.detect_fvg_bearish()
        
        # Filter to session data
        session_df = self.filter_session_data()
        
        # Get unique dates
        unique_dates = session_df['DateOnly'].unique()
        print(f"Processing {len(unique_dates)} trading sessions...\n")
        
        # Process each session with progress indicator
        total_sessions = len(unique_dates)
        for idx, date in enumerate(unique_dates, 1):
            if idx % 100 == 0:
                print(f"  Progress: {idx}/{total_sessions} sessions ({idx/total_sessions*100:.1f}%)")
            # Get session data for this date
            date_mask = session_df['DateOnly'] == date
            day_session = session_df[date_mask].copy()
            
            if len(day_session) < 10:  # Need minimum candles
                continue
            
            # Find sweep opportunities
            sweeps = self.find_sweep_opportunities(day_session)
            
            for sweep in sweeps:
                # Check for MSS
                mss_details = self.check_mss(day_session, sweep)
                
                if mss_details is None:
                    continue
                
                # Calculate entry (50% Fib)
                entry_price = self.calculate_fibonacci_entry(
                    sweep['sweep_high'], 
                    mss_details['mss_low']
                )
                
                # Set stop loss (above sweep high)
                stop_loss = sweep['sweep_high']
                
                # Find take profit (first unfilled FVG)
                fvg = self.find_first_unfilled_fvg(
                    day_session, 
                    mss_details, 
                    mss_details['mss_time']
                )
                
                if fvg is None:
                    continue  # No FVG target
                
                # Take profit at FVG bottom (target of bearish move)
                take_profit = fvg['fvg_bottom']
                
                # Validate SHORT trade setup: TP should be BELOW entry
                if take_profit >= entry_price:
                    continue  # Invalid setup for SHORT
                
                # Validate: Entry should be BELOW stop loss
                if entry_price >= stop_loss:
                    continue  # Invalid setup
                
                # Simulate the trade
                trade_result = self.simulate_trade(
                    day_session,
                    self.df,  # Use all data for exit tracking
                    sweep,
                    mss_details,
                    entry_price,
                    stop_loss,
                    take_profit
                )
                
                if trade_result is not None:
                    self.trades.append(trade_result)
        
        print(f"\nBacktest complete! Found {len(self.trades)} trades.\n")
        
        return self.trades
    
    def calculate_metrics(self):
        """
        Calculate performance metrics.
        """
        if len(self.trades) == 0:
            print("No trades to analyze.")
            return
        
        print("="*80)
        print("PERFORMANCE METRICS")
        print("="*80)
        
        # Total trades
        total_trades = len(self.trades)
        print(f"Total Trades: {total_trades}")
        
        # Wins and losses
        wins = [t for t in self.trades if t['outcome'] == 'Win']
        losses = [t for t in self.trades if t['outcome'] == 'Loss']
        
        num_wins = len(wins)
        num_losses = len(losses)
        
        print(f"Wins: {num_wins}")
        print(f"Losses: {num_losses}")
        
        # Win rate
        win_rate = (num_wins / total_trades) * 100 if total_trades > 0 else 0
        print(f"Win Rate: {win_rate:.2f}%")
        
        # Total P&L in points
        total_pnl = sum([t['pnl_points'] for t in self.trades])
        print(f"Total P&L: {total_pnl:.2f} points")
        
        # Average win and loss
        if num_wins > 0:
            avg_win = sum([t['pnl_points'] for t in wins]) / num_wins
            print(f"Average Win: {avg_win:.2f} points")
        
        if num_losses > 0:
            avg_loss = sum([abs(t['pnl_points']) for t in losses]) / num_losses
            print(f"Average Loss: {avg_loss:.2f} points")
        
        # Average R:R ratio
        rr_ratios = [t['rr_ratio'] for t in self.trades if t['rr_ratio'] is not None]
        if len(rr_ratios) > 0:
            avg_rr = sum(rr_ratios) / len(rr_ratios)
            print(f"Average R:R Ratio: {avg_rr:.2f}")
        
        # Profit factor
        gross_profit = sum([t['pnl_points'] for t in wins]) if num_wins > 0 else 0
        gross_loss = sum([abs(t['pnl_points']) for t in losses]) if num_losses > 0 else 0
        
        if gross_loss > 0:
            profit_factor = gross_profit / gross_loss
            print(f"Profit Factor: {profit_factor:.2f}")
        else:
            print("Profit Factor: N/A (no losses)")
        
        print("="*80)
        
        return {
            'total_trades': total_trades,
            'wins': num_wins,
            'losses': num_losses,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_rr': avg_rr if len(rr_ratios) > 0 else 0,
            'profit_factor': profit_factor if gross_loss > 0 else 0
        }
    
    def plot_equity_curve(self, risk_per_trade_pct=1.0, initial_capital=100000):
        """
        Plot cumulative equity curve.
        
        Parameters:
        -----------
        risk_per_trade_pct : float
            Risk per trade as percentage of capital (default 1%)
        initial_capital : float
            Starting capital in USD (default $100,000)
        """
        if len(self.trades) == 0:
            print("No trades to plot.")
            return
        
        print(f"\nGenerating equity curve (Risk per trade: {risk_per_trade_pct}%, Initial capital: ${initial_capital:,.0f})...")
        
        # Sort trades by entry time
        sorted_trades = sorted(self.trades, key=lambda x: x['entry_time'])
        
        # Calculate equity curve
        equity = [initial_capital]
        capital = initial_capital
        
        for trade in sorted_trades:
            # Calculate position size based on risk
            risk_amount = capital * (risk_per_trade_pct / 100)
            risk_points = trade['risk_points']
            
            # Position size = risk amount / (risk points * point value)
            # Using NQ point value constant
            position_size = risk_amount / (risk_points * self.NQ_POINT_VALUE) if risk_points > 0 else 0
            
            # Calculate P&L in dollars
            pnl_dollars = trade['pnl_points'] * self.NQ_POINT_VALUE * position_size
            
            # Update capital
            capital += pnl_dollars
            equity.append(capital)
        
        # Calculate return percentage
        total_return = ((equity[-1] - initial_capital) / initial_capital) * 100
        
        # Plot
        plt.figure(figsize=(14, 7))
        plt.plot(range(len(equity)), equity, linewidth=2, color='#2E86AB')
        plt.axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.5, label='Initial Capital')
        plt.fill_between(range(len(equity)), initial_capital, equity, 
                         where=[e >= initial_capital for e in equity], 
                         alpha=0.3, color='green', label='Profit')
        plt.fill_between(range(len(equity)), initial_capital, equity, 
                         where=[e < initial_capital for e in equity], 
                         alpha=0.3, color='red', label='Loss')
        
        plt.title(f'SMC Reversal Strategy - Cumulative Equity Curve\n'
                  f'Total Return: {total_return:.2f}% | Final Equity: ${equity[-1]:,.2f}',
                  fontsize=14, fontweight='bold')
        plt.xlabel('Trade Number', fontsize=12)
        plt.ylabel('Equity ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='best')
        plt.tight_layout()
        
        # Save figure
        filename = 'smc_reversal_equity_curve.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Equity curve saved as {filename}")
        
        plt.show()
        
        print(f"\nFinal Equity: ${equity[-1]:,.2f}")
        print(f"Total Return: {total_return:.2f}%")
        print(f"Maximum Equity: ${max(equity):,.2f}")
        print(f"Minimum Equity: ${min(equity):,.2f}")


def main():
    """
    Main execution function.
    """
    print("\n" + "="*80)
    print("SMC REVERSAL STRATEGY BACKTEST - NQ 5-MINUTE DATA (2018-2025)")
    print("="*80 + "\n")
    
    # Initialize backtest
    # Pattern to match all NQ 5-minute CSV files (relative path)
    import os
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    data_pattern = os.path.join(repo_dir, '*5m.csv')
    
    backtest = SMCReversalBacktest(
        data_files_pattern=data_pattern,
        session_start='01:00:00',
        session_end='07:00:00'
    )
    
    # Run backtest
    trades = backtest.run_backtest()
    
    # Calculate metrics
    metrics = backtest.calculate_metrics()
    
    # Plot equity curve
    backtest.plot_equity_curve(risk_per_trade_pct=1.0, initial_capital=100000)
    
    print("\n" + "="*80)
    print("BACKTEST COMPLETE!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
