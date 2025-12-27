"""
London Killzone FVG Inversion Strategy Backtest
------------------------------------------------
Strategy: Trade Fair Value Gap (FVG) inversions during London Killzone (01:00-05:00)
Asset: Nasdaq 100 (NQ)
Timeframe: 15-minute
Data: 2018-2025

Author: Backtest Trading
Date: 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import glob
import os


class FVG:
    """Fair Value Gap class to store FVG information"""
    def __init__(self, fvg_type, top, bottom, index):
        self.type = fvg_type  # 'bullish' or 'bearish'
        self.top = top
        self.bottom = bottom
        self.index = index
        self.active = True
    
    def is_mitigated(self, high, low):
        """Check if FVG has been mitigated (price filled/entered the gap)"""
        if self.type == 'bullish':
            # Bullish FVG is mitigated if price goes into the gap from below
            # The gap is [self.bottom, self.top] where self.top > self.bottom
            # Mitigation: price high reaches into the gap
            return high >= self.bottom
        else:  # bearish
            # Bearish FVG is mitigated if price goes into the gap from above
            # The gap is [self.bottom, self.top] where self.top > self.bottom  
            # Mitigation: price low reaches into the gap
            return low <= self.top
    
    def check_inversion(self, close_price):
        """Check if price has inverted through the FVG"""
        if self.type == 'bullish':
            # Short signal: price closes BELOW bottom of bullish FVG
            return close_price < self.bottom
        else:  # bearish
            # Long signal: price closes ABOVE top of bearish FVG
            return close_price > self.top


class Trade:
    """Trade class to store trade information"""
    def __init__(self, trade_type, entry_price, entry_time, entry_idx, sl_price, tp1_price, tp2_price, tp3_price):
        self.type = trade_type  # 'long' or 'short'
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.entry_idx = entry_idx
        self.sl_price = sl_price
        self.tp1_price = tp1_price
        self.tp2_price = tp2_price
        self.tp3_price = tp3_price
        self.closed = False
        self.exit_price = None
        self.exit_time = None
        self.result_tp1 = None  # 'win', 'loss', or None
        self.result_tp2 = None
        self.result_tp3 = None
        self.pnl_tp1 = 0
        self.pnl_tp2 = 0
        self.pnl_tp3 = 0
    
    def update(self, current_idx, current_time, high, low):
        """Update trade status based on current price action"""
        if self.closed:
            return
        
        if self.type == 'long':
            # Check stop loss
            if low <= self.sl_price:
                if self.result_tp1 is None:
                    self.result_tp1 = 'loss'
                    self.pnl_tp1 = self.sl_price - self.entry_price
                if self.result_tp2 is None:
                    self.result_tp2 = 'loss'
                    self.pnl_tp2 = self.sl_price - self.entry_price
                if self.result_tp3 is None:
                    self.result_tp3 = 'loss'
                    self.pnl_tp3 = self.sl_price - self.entry_price
                self.closed = True
                self.exit_time = current_time
                return
            
            # Check take profits
            if self.result_tp1 is None and high >= self.tp1_price:
                self.result_tp1 = 'win'
                self.pnl_tp1 = self.tp1_price - self.entry_price
            
            if self.result_tp2 is None and high >= self.tp2_price:
                self.result_tp2 = 'win'
                self.pnl_tp2 = self.tp2_price - self.entry_price
            
            if self.result_tp3 is None and high >= self.tp3_price:
                self.result_tp3 = 'win'
                self.pnl_tp3 = self.tp3_price - self.entry_price
            
            # Close trade if all TPs hit
            if self.result_tp1 is not None and self.result_tp2 is not None and self.result_tp3 is not None:
                self.closed = True
                self.exit_time = current_time
        
        else:  # short
            # Check stop loss
            if high >= self.sl_price:
                if self.result_tp1 is None:
                    self.result_tp1 = 'loss'
                    self.pnl_tp1 = self.entry_price - self.sl_price
                if self.result_tp2 is None:
                    self.result_tp2 = 'loss'
                    self.pnl_tp2 = self.entry_price - self.sl_price
                if self.result_tp3 is None:
                    self.result_tp3 = 'loss'
                    self.pnl_tp3 = self.entry_price - self.sl_price
                self.closed = True
                self.exit_time = current_time
                return
            
            # Check take profits
            if self.result_tp1 is None and low <= self.tp1_price:
                self.result_tp1 = 'win'
                self.pnl_tp1 = self.entry_price - self.tp1_price
            
            if self.result_tp2 is None and low <= self.tp2_price:
                self.result_tp2 = 'win'
                self.pnl_tp2 = self.entry_price - self.tp2_price
            
            if self.result_tp3 is None and low <= self.tp3_price:
                self.result_tp3 = 'win'
                self.pnl_tp3 = self.entry_price - self.tp3_price
            
            # Close trade if all TPs hit
            if self.result_tp1 is not None and self.result_tp2 is not None and self.result_tp3 is not None:
                self.closed = True
                self.exit_time = current_time


def load_data(base_path):
    """Load and combine all 15m CSV files from 2018-2025"""
    print("Loading data files...")
    
    all_data = []
    years = range(2018, 2026)  # 2018 to 2025
    
    for year in years:
        file_path = os.path.join(base_path, f"{year} 15m.csv")
        if os.path.exists(file_path):
            print(f"  Loading {year} 15m.csv...")
            df = pd.read_csv(file_path, sep=';', skiprows=1, 
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            all_data.append(df)
        else:
            print(f"  Warning: {year} 15m.csv not found")
    
    # Combine all data
    df_combined = pd.concat(all_data, ignore_index=True)
    
    # Parse datetime
    df_combined['DateTime'] = pd.to_datetime(
        df_combined['Date'] + ' ' + df_combined['Time'],
        format='%d/%m/%Y %H:%M:%S'
    )
    
    # Sort by datetime
    df_combined = df_combined.sort_values('DateTime').reset_index(drop=True)
    
    # Extract time for filtering
    df_combined['TimeOnly'] = df_combined['DateTime'].dt.time
    
    print(f"\nTotal rows loaded: {len(df_combined)}")
    print(f"Date range: {df_combined['DateTime'].min()} to {df_combined['DateTime'].max()}")
    
    return df_combined


def identify_fvgs(df):
    """Identify Fair Value Gaps in the dataframe"""
    fvgs = []
    
    # Need at least 3 candles to identify FVG
    for i in range(2, len(df)):
        # Bullish FVG: Low[i-2] > High[i]
        if df.loc[i-2, 'Low'] > df.loc[i, 'High']:
            fvg = FVG(
                fvg_type='bullish',
                top=df.loc[i-2, 'Low'],
                bottom=df.loc[i, 'High'],
                index=i
            )
            fvgs.append(fvg)
        
        # Bearish FVG: High[i-2] < Low[i]
        elif df.loc[i-2, 'High'] < df.loc[i, 'Low']:
            fvg = FVG(
                fvg_type='bearish',
                top=df.loc[i, 'Low'],
                bottom=df.loc[i-2, 'High'],
                index=i
            )
            fvgs.append(fvg)
    
    return fvgs


def is_in_london_killzone(time_obj):
    """Check if time is in London Killzone (01:00 to 05:00)"""
    return time(1, 0) <= time_obj <= time(5, 0)


def backtest_strategy(df):
    """Run the backtest strategy"""
    print("\n" + "="*60)
    print("Running Backtest...")
    print("="*60)
    
    active_fvgs = []
    trades = []
    active_trade = None
    
    # Iterate through dataframe
    for i in range(2, len(df)):
        current_time = df.loc[i, 'DateTime']
        current_time_only = df.loc[i, 'TimeOnly']
        current_high = df.loc[i, 'High']
        current_low = df.loc[i, 'Low']
        current_close = df.loc[i, 'Close']
        current_open = df.loc[i, 'Open']
        in_killzone = is_in_london_killzone(current_time_only)
        
        # Update active trade if exists
        if active_trade is not None and not active_trade.closed:
            active_trade.update(i, current_time, current_high, current_low)
        
        # Check active FVGs for mitigation or inversion (before adding new FVGs)
        fvgs_to_remove = []
        for fvg in active_fvgs:
            if not fvg.active:
                continue
            
            # Check if FVG is mitigated (filled) - but not on the same candle it was created
            if i > fvg.index and fvg.is_mitigated(current_high, current_low):
                fvg.active = False
                fvgs_to_remove.append(fvg)
                continue
            
            # Check for inversion (only during killzone and if no active trade)
            # Also not on the same candle the FVG was created
            if i > fvg.index and in_killzone and (active_trade is None or active_trade.closed):
                if fvg.check_inversion(current_close):
                    # We have an inversion signal!
                    if fvg.type == 'bullish':
                        # Short entry: price closed below bullish FVG
                        trade_type = 'short'
                        entry_price = current_close
                        sl_price = current_high
                        risk = sl_price - entry_price
                        
                        if risk > 0:  # Valid trade
                            tp1_price = entry_price - (risk * 1.0)
                            tp2_price = entry_price - (risk * 1.5)
                            tp3_price = entry_price - (risk * 2.0)
                            
                            trade = Trade(
                                trade_type=trade_type,
                                entry_price=entry_price,
                                entry_time=current_time,
                                entry_idx=i,
                                sl_price=sl_price,
                                tp1_price=tp1_price,
                                tp2_price=tp2_price,
                                tp3_price=tp3_price
                            )
                            trades.append(trade)
                            active_trade = trade
                            fvg.active = False
                            fvgs_to_remove.append(fvg)
                    
                    else:  # bearish FVG
                        # Long entry: price closed above bearish FVG
                        trade_type = 'long'
                        entry_price = current_close
                        sl_price = current_low
                        risk = entry_price - sl_price
                        
                        if risk > 0:  # Valid trade
                            tp1_price = entry_price + (risk * 1.0)
                            tp2_price = entry_price + (risk * 1.5)
                            tp3_price = entry_price + (risk * 2.0)
                            
                            trade = Trade(
                                trade_type=trade_type,
                                entry_price=entry_price,
                                entry_time=current_time,
                                entry_idx=i,
                                sl_price=sl_price,
                                tp1_price=tp1_price,
                                tp2_price=tp2_price,
                                tp3_price=tp3_price
                            )
                            trades.append(trade)
                            active_trade = trade
                            fvg.active = False
                            fvgs_to_remove.append(fvg)
        
        # Remove inactive FVGs
        for fvg in fvgs_to_remove:
            if fvg in active_fvgs:
                active_fvgs.remove(fvg)
        
        # Identify new FVGs (only during killzone)
        if in_killzone:
            # Bullish FVG: Low[i-2] > High[i]
            if df.loc[i-2, 'Low'] > current_high:
                fvg = FVG(
                    fvg_type='bullish',
                    top=df.loc[i-2, 'Low'],
                    bottom=current_high,
                    index=i
                )
                active_fvgs.append(fvg)
            
            # Bearish FVG: High[i-2] < Low[i]
            elif df.loc[i-2, 'High'] < current_low:
                fvg = FVG(
                    fvg_type='bearish',
                    top=current_low,
                    bottom=df.loc[i-2, 'High'],
                    index=i
                )
                active_fvgs.append(fvg)
    
    return trades


def calculate_statistics(trades):
    """Calculate and print statistics for each RR target"""
    print("\n" + "="*60)
    print("BACKTEST RESULTS")
    print("="*60)
    
    if len(trades) == 0:
        print("\nNo trades executed during the backtest period.")
        return
    
    print(f"\nTotal Trades: {len(trades)}")
    
    # Calculate statistics for each TP level
    for tp_level, tp_name in [(1, 'TP1 (RR 1.0)'), (2, 'TP2 (RR 1.5)'), (3, 'TP3 (RR 2.0)')]:
        print(f"\n{'-'*60}")
        print(f"{tp_name}")
        print(f"{'-'*60}")
        
        wins = 0
        losses = 0
        total_pnl = 0
        
        for trade in trades:
            if tp_level == 1:
                result = trade.result_tp1
                pnl = trade.pnl_tp1
            elif tp_level == 2:
                result = trade.result_tp2
                pnl = trade.pnl_tp2
            else:
                result = trade.result_tp3
                pnl = trade.pnl_tp3
            
            if result == 'win':
                wins += 1
                total_pnl += pnl
            elif result == 'loss':
                losses += 1
                total_pnl += pnl
        
        total_closed = wins + losses
        win_rate = (wins / total_closed * 100) if total_closed > 0 else 0
        
        print(f"Closed Trades: {total_closed}")
        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Total PnL (Points): {total_pnl:.2f}")
        
        # Calculate average win and loss
        if wins > 0:
            avg_win = sum([t.pnl_tp1 if tp_level == 1 else (t.pnl_tp2 if tp_level == 2 else t.pnl_tp3) 
                          for t in trades if (t.result_tp1 if tp_level == 1 else (t.result_tp2 if tp_level == 2 else t.result_tp3)) == 'win']) / wins
            print(f"Average Win: {avg_win:.2f} points")
        
        if losses > 0:
            avg_loss = sum([t.pnl_tp1 if tp_level == 1 else (t.pnl_tp2 if tp_level == 2 else t.pnl_tp3) 
                           for t in trades if (t.result_tp1 if tp_level == 1 else (t.result_tp2 if tp_level == 2 else t.result_tp3)) == 'loss']) / losses
            print(f"Average Loss: {avg_loss:.2f} points")
    
    # Additional statistics
    print(f"\n{'-'*60}")
    print("Trade Type Distribution")
    print(f"{'-'*60}")
    long_trades = sum(1 for t in trades if t.type == 'long')
    short_trades = sum(1 for t in trades if t.type == 'short')
    print(f"Long Trades: {long_trades}")
    print(f"Short Trades: {short_trades}")
    
    print("\n" + "="*60)


def main():
    """Main execution function"""
    print("="*60)
    print("LONDON KILLZONE FVG INVERSION STRATEGY BACKTEST")
    print("="*60)
    print("\nStrategy Configuration:")
    print("  - Asset: Nasdaq 100 (NQ)")
    print("  - Timeframe: 15 minutes")
    print("  - Trading Window: 01:00 - 05:00 (London Killzone)")
    print("  - Data Period: 2018 - 2025")
    print("  - Risk-Reward Targets: 1.0, 1.5, 2.0")
    print()
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load data
    df = load_data(script_dir)
    
    # Run backtest
    trades = backtest_strategy(df)
    
    # Calculate and display statistics
    calculate_statistics(trades)
    
    print("\nBacktest completed successfully!")


if __name__ == "__main__":
    main()
