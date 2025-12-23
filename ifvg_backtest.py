#!/usr/bin/env python3
"""
IFVG (Inversion Fair Value Gap) Backtest Script for NQ Futures
Processes Judas Swings and calculates three different TP scenarios with separate win rates
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import zipfile
import os
from typing import Tuple, List, Dict, Optional
import io

# Constants
COMMISSION = 4.0  # $4 per trade
SL_OFFSET = 0.5  # Points beyond manipulation extreme


class IFVGBacktester:
    """Backtests IFVG strategy with three different TP scenarios"""
    
    def __init__(self, judas_swings_path: str, data_dir: str):
        self.judas_swings_path = judas_swings_path
        self.data_dir = data_dir
        self.judas_swings = None
        self.price_data = {}
        
    def load_judas_swings(self):
        """Load the Judas Swing results"""
        print("Loading Judas Swings...")
        self.judas_swings = pd.read_csv(self.judas_swings_path)
        self.judas_swings['date'] = pd.to_datetime(self.judas_swings['date'])
        
        # Calculate manipulation extreme for each swing
        self.judas_swings['manipulation_extreme'] = self.judas_swings.apply(
            lambda row: row['manipulation_low'] if row['direction'] == 'bearish' else row['manipulation_high'],
            axis=1
        )
        
        print(f"Loaded {len(self.judas_swings)} Judas Swings")
        
    def load_price_data(self, timeframe: str, year: int) -> pd.DataFrame:
        """Load price data for a specific timeframe and year"""
        if timeframe == '1m':
            # Handle zipped files
            zip_path = os.path.join(self.data_dir, f"{year} 1m.csv.zip")
            csv_path = os.path.join(self.data_dir, f"{year} 1m.csv")
            
            if os.path.exists(zip_path):
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Find the CSV file in the zip
                    csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                    if csv_files:
                        with zip_ref.open(csv_files[0]) as f:
                            df = pd.read_csv(f, delimiter=';', skiprows=1, 
                                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
                    else:
                        return None
            elif os.path.exists(csv_path):
                df = pd.read_csv(csv_path, delimiter=';', skiprows=1,
                               names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            else:
                return None
        else:  # 5m
            csv_path = os.path.join(self.data_dir, f"{year} {timeframe}.csv")
            if not os.path.exists(csv_path):
                return None
            df = pd.read_csv(csv_path, delimiter=';', skiprows=1,
                           names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        
        # Combine Date and Time columns
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        df = df.set_index('DateTime')
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        return df
    
    def get_price_data_for_date(self, date: datetime, timeframe: str) -> pd.DataFrame:
        """Get price data for a specific date and timeframe"""
        year = date.year
        key = f"{year}_{timeframe}"
        
        if key not in self.price_data:
            self.price_data[key] = self.load_price_data(timeframe, year)
        
        if self.price_data[key] is None:
            return None
        
        # Filter for the specific date
        date_str = date.date()
        df = self.price_data[key]
        return df[df.index.date == date_str]
    
    def detect_fvgs(self, df: pd.DataFrame, direction: str) -> List[Dict]:
        """
        Detect Fair Value Gaps in price data
        
        Args:
            df: Price data DataFrame
            direction: 'bearish' (for long setups) or 'bullish' (for short setups)
        
        Returns:
            List of FVG dictionaries with high, low, and timestamp
        """
        fvgs = []
        
        if len(df) < 3:
            return fvgs
        
        for i in range(1, len(df) - 1):
            if direction == 'bearish':
                # Bearish FVG: candle[i-1].Low > candle[i+1].High
                if df.iloc[i-1]['Low'] > df.iloc[i+1]['High']:
                    fvgs.append({
                        'high': df.iloc[i-1]['Low'],
                        'low': df.iloc[i+1]['High'],
                        'timestamp': df.index[i],
                        'type': 'bearish'
                    })
            else:  # bullish
                # Bullish FVG: candle[i-1].High < candle[i+1].Low
                if df.iloc[i-1]['High'] < df.iloc[i+1]['Low']:
                    fvgs.append({
                        'high': df.iloc[i+1]['Low'],
                        'low': df.iloc[i-1]['High'],
                        'timestamp': df.index[i],
                        'type': 'bullish'
                    })
        
        return fvgs
    
    def find_manipulation_leg(self, df: pd.DataFrame, swing: pd.Series) -> Tuple[pd.DataFrame, Optional[datetime]]:
        """
        Find the manipulation leg from Tokyo level break to Manipulation_Extreme
        
        Returns:
            Tuple of (manipulation_df, extreme_time)
        """
        direction = swing['direction']
        tokyo_high = swing['tokyo_high']
        tokyo_low = swing['tokyo_low']
        manipulation_extreme = swing['manipulation_extreme']
        
        # Find when Tokyo range was broken
        if direction == 'bearish':
            # Look for break below Tokyo low
            break_mask = df['Low'] < tokyo_low
        else:  # bullish
            # Look for break above Tokyo high
            break_mask = df['High'] > tokyo_high
        
        if not break_mask.any():
            return None, None
        
        break_time = df[break_mask].index[0]
        
        # Find when manipulation extreme was reached
        if direction == 'bearish':
            extreme_mask = df['Low'] <= manipulation_extreme
        else:
            extreme_mask = df['High'] >= manipulation_extreme
        
        extreme_data = df[extreme_mask]
        if len(extreme_data) == 0:
            return None, None
        
        extreme_time = extreme_data.index[0]
        
        # Return data from break to extreme
        manipulation_df = df[(df.index >= break_time) & (df.index <= extreme_time)]
        
        return manipulation_df, extreme_time
    
    def check_entry_trigger(self, df: pd.DataFrame, fvg: Dict, direction: str) -> Optional[Tuple[datetime, float]]:
        """
        Check if price closes through the FVG (inversion)
        
        Returns:
            Tuple of (entry_time, entry_price) or None
        """
        if direction == 'bearish':
            # Long setup: Close ABOVE bearish FVG high
            trigger_mask = df['Close'] > fvg['high']
        else:
            # Short setup: Close BELOW bullish FVG low
            trigger_mask = df['Close'] < fvg['low']
        
        if trigger_mask.any():
            entry_time = df[trigger_mask].index[0]
            entry_price = df.loc[entry_time, 'Close']
            return entry_time, entry_price
        
        return None
    
    def simulate_trade(self, df: pd.DataFrame, entry_time: datetime, entry_price: float,
                      sl: float, tp1: float, tp2: float, direction: str) -> Dict:
        """
        Simulate a trade with three scenarios:
        A) 100% at Equilibrium (TP1)
        B) 100% at Opposing Liquidity (TP2)
        C) 50/50 split
        
        Returns:
            Dictionary with results for all three scenarios
        """
        # Get data after entry
        trade_df = df[df.index > entry_time]
        
        if len(trade_df) == 0:
            return None
        
        results = {
            'scenario_a': {'outcome': None, 'pnl': 0},
            'scenario_b': {'outcome': None, 'pnl': 0},
            'scenario_c': {'outcome': None, 'pnl': 0}
        }
        
        tp1_hit_time = None
        tp2_hit_time = None
        sl_hit_time = None
        
        # Track what gets hit and when
        for idx, row in trade_df.iterrows():
            if direction == 'bearish':  # Long trade
                # Check TP1 (closer target)
                if tp1_hit_time is None and row['High'] >= tp1:
                    tp1_hit_time = idx
                
                # Check TP2 (further target)
                if tp2_hit_time is None and row['High'] >= tp2:
                    tp2_hit_time = idx
                
                # Check SL
                if sl_hit_time is None and row['Low'] <= sl:
                    sl_hit_time = idx
            else:  # Short trade
                # Check TP1 (closer target)
                if tp1_hit_time is None and row['Low'] <= tp1:
                    tp1_hit_time = idx
                
                # Check TP2 (further target)
                if tp2_hit_time is None and row['Low'] <= tp2:
                    tp2_hit_time = idx
                
                # Check SL
                if sl_hit_time is None and row['High'] >= sl:
                    sl_hit_time = idx
            
            # Break if something was hit
            if tp1_hit_time or tp2_hit_time or sl_hit_time:
                break
        
        # Determine outcomes for each scenario
        points_to_pnl = 20  # NQ: $20 per point
        
        # Scenario A: 100% at TP1
        if tp1_hit_time is not None and (sl_hit_time is None or tp1_hit_time <= sl_hit_time):
            results['scenario_a']['outcome'] = 'win'
            if direction == 'bearish':
                results['scenario_a']['pnl'] = (tp1 - entry_price) * points_to_pnl - COMMISSION
            else:
                results['scenario_a']['pnl'] = (entry_price - tp1) * points_to_pnl - COMMISSION
        elif sl_hit_time is not None:
            results['scenario_a']['outcome'] = 'loss'
            if direction == 'bearish':
                results['scenario_a']['pnl'] = (sl - entry_price) * points_to_pnl - COMMISSION
            else:
                results['scenario_a']['pnl'] = (entry_price - sl) * points_to_pnl - COMMISSION
        
        # Scenario B: 100% at TP2
        if tp2_hit_time is not None and (sl_hit_time is None or tp2_hit_time <= sl_hit_time):
            results['scenario_b']['outcome'] = 'win'
            if direction == 'bearish':
                results['scenario_b']['pnl'] = (tp2 - entry_price) * points_to_pnl - COMMISSION
            else:
                results['scenario_b']['pnl'] = (entry_price - tp2) * points_to_pnl - COMMISSION
        elif sl_hit_time is not None:
            results['scenario_b']['outcome'] = 'loss'
            if direction == 'bearish':
                results['scenario_b']['pnl'] = (sl - entry_price) * points_to_pnl - COMMISSION
            else:
                results['scenario_b']['pnl'] = (entry_price - sl) * points_to_pnl - COMMISSION
        
        # Scenario C: 50/50 split
        if tp1_hit_time is not None and (sl_hit_time is None or tp1_hit_time <= sl_hit_time):
            # TP1 hit first - take 50% profit, move to breakeven
            if direction == 'bearish':
                first_half_pnl = (tp1 - entry_price) * points_to_pnl * 0.5
            else:
                first_half_pnl = (entry_price - tp1) * points_to_pnl * 0.5
            
            # Now check what happens with remaining position (BE stop)
            be_df = trade_df[trade_df.index > tp1_hit_time]
            second_half_pnl = 0
            
            if len(be_df) > 0:
                for idx, row in be_df.iterrows():
                    if direction == 'bearish':
                        # Check if TP2 hit
                        if tp2_hit_time and idx >= tp2_hit_time:
                            second_half_pnl = (tp2 - entry_price) * points_to_pnl * 0.5
                            break
                        # Check if BE stop hit
                        if row['Low'] <= entry_price:
                            second_half_pnl = 0  # Breakeven
                            break
                    else:
                        # Check if TP2 hit
                        if tp2_hit_time and idx >= tp2_hit_time:
                            second_half_pnl = (entry_price - tp2) * points_to_pnl * 0.5
                            break
                        # Check if BE stop hit
                        if row['High'] >= entry_price:
                            second_half_pnl = 0  # Breakeven
                            break
            
            total_pnl = first_half_pnl + second_half_pnl - COMMISSION
            results['scenario_c']['pnl'] = total_pnl
            results['scenario_c']['outcome'] = 'win' if total_pnl > 0 else 'breakeven' if total_pnl >= -COMMISSION else 'loss'
            
        elif sl_hit_time is not None:
            # SL hit before TP1
            results['scenario_c']['outcome'] = 'loss'
            if direction == 'bearish':
                results['scenario_c']['pnl'] = (sl - entry_price) * points_to_pnl - COMMISSION
            else:
                results['scenario_c']['pnl'] = (entry_price - sl) * points_to_pnl - COMMISSION
        
        return results
    
    def backtest_swing(self, swing: pd.Series, timeframe: str) -> List[Dict]:
        """
        Backtest a single Judas Swing for IFVG entries
        
        Returns:
            List of trade dictionaries
        """
        date = swing['date']
        direction = swing['direction']
        
        # Get price data for this date
        df = self.get_price_data_for_date(date, timeframe)
        
        if df is None or len(df) == 0:
            return []
        
        # Find manipulation leg
        manip_df, extreme_time = self.find_manipulation_leg(df, swing)
        
        if manip_df is None or len(manip_df) == 0:
            return []
        
        # Detect FVGs during manipulation
        fvgs = self.detect_fvgs(manip_df, direction)
        
        if len(fvgs) == 0:
            return []
        
        # Calculate TPs and SL
        tokyo_eq = (swing['tokyo_high'] + swing['tokyo_low']) / 2
        
        if direction == 'bearish':
            # Long setup
            opposing_liquidity = swing['tokyo_high']
            sl = swing['manipulation_extreme'] - SL_OFFSET
            tp1 = tokyo_eq
            tp2 = opposing_liquidity
        else:
            # Short setup
            opposing_liquidity = swing['tokyo_low']
            sl = swing['manipulation_extreme'] + SL_OFFSET
            tp1 = tokyo_eq
            tp2 = opposing_liquidity
        
        # Search for entries from extreme time to 23:00
        search_end_time = datetime.combine(date.date(), time(23, 0))
        search_df = df[(df.index > extreme_time) & (df.index <= search_end_time)]
        
        if len(search_df) == 0:
            return []
        
        trades = []
        
        # Check each FVG for entry trigger
        for fvg in fvgs:
            # Only check for entries after the FVG formed
            fvg_search_df = search_df[search_df.index > fvg['timestamp']]
            
            entry_result = self.check_entry_trigger(fvg_search_df, fvg, direction)
            
            if entry_result:
                entry_time, entry_price = entry_result
                
                # Simulate the trade with all three scenarios
                trade_results = self.simulate_trade(search_df, entry_time, entry_price, 
                                                   sl, tp1, tp2, direction)
                
                if trade_results:
                    # Create trade records for each scenario
                    for scenario_name, scenario_result in trade_results.items():
                        if scenario_result['outcome'] is not None:
                            trades.append({
                                'Date': date.strftime('%Y-%m-%d'),
                                'Direction': direction,
                                'Entry_Price': entry_price,
                                'SL': sl,
                                'TP1': tp1,
                                'TP2': tp2,
                                'Scenario': scenario_name,
                                'Outcome': scenario_result['outcome'],
                                'PnL': scenario_result['pnl'],
                                'FVG_High': fvg['high'],
                                'FVG_Low': fvg['low']
                            })
                    
                    # Only take first entry per swing
                    break
        
        return trades
    
    def run_backtest(self, timeframe: str) -> pd.DataFrame:
        """
        Run complete backtest for a given timeframe
        
        Args:
            timeframe: '1m' or '5m'
        
        Returns:
            DataFrame with all trades
        """
        print(f"\n{'='*60}")
        print(f"Running backtest for {timeframe} timeframe")
        print(f"{'='*60}")
        
        all_trades = []
        
        for idx, swing in self.judas_swings.iterrows():
            if (idx + 1) % 100 == 0:
                print(f"Processing swing {idx + 1}/{len(self.judas_swings)}...")
            
            trades = self.backtest_swing(swing, timeframe)
            all_trades.extend(trades)
        
        if len(all_trades) == 0:
            print(f"No trades found for {timeframe}")
            return pd.DataFrame()
        
        df_trades = pd.DataFrame(all_trades)
        return df_trades
    
    def calculate_statistics(self, df_trades: pd.DataFrame) -> Dict:
        """Calculate statistics for each scenario"""
        stats = {}
        
        scenarios = df_trades['Scenario'].unique()
        
        for scenario in scenarios:
            scenario_trades = df_trades[df_trades['Scenario'] == scenario]
            
            wins = scenario_trades[scenario_trades['Outcome'] == 'win']
            losses = scenario_trades[scenario_trades['Outcome'] == 'loss']
            
            total_trades = len(scenario_trades)
            win_count = len(wins)
            loss_count = len(losses)
            win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0
            
            total_pnl = scenario_trades['PnL'].sum()
            avg_win = wins['PnL'].mean() if len(wins) > 0 else 0
            avg_loss = losses['PnL'].mean() if len(losses) > 0 else 0
            
            # Calculate profit factor
            gross_profit = wins['PnL'].sum() if len(wins) > 0 else 0
            gross_loss = abs(losses['PnL'].sum()) if len(losses) > 0 else 0
            profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
            
            # Calculate expectancy
            expectancy = (total_pnl / total_trades) if total_trades > 0 else 0
            
            stats[scenario] = {
                'total_trades': total_trades,
                'wins': win_count,
                'losses': loss_count,
                'win_rate': win_rate,
                'total_pnl': total_pnl,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': profit_factor,
                'expectancy': expectancy
            }
        
        return stats
    
    def print_statistics(self, stats: Dict, timeframe: str):
        """Print formatted statistics"""
        print(f"\n{'='*60}")
        print(f"STATISTICS FOR {timeframe.upper()} TIMEFRAME")
        print(f"{'='*60}\n")
        
        for scenario, data in stats.items():
            print(f"\n{scenario.upper().replace('_', ' ')}:")
            print(f"  Total Trades: {data['total_trades']}")
            print(f"  Wins: {data['wins']}")
            print(f"  Losses: {data['losses']}")
            print(f"  Win Rate: {data['win_rate']:.2f}%")
            print(f"  Total P&L: ${data['total_pnl']:,.2f}")
            print(f"  Avg Win: ${data['avg_win']:,.2f}")
            print(f"  Avg Loss: ${data['avg_loss']:,.2f}")
            print(f"  Profit Factor: {data['profit_factor']:.2f}")
            print(f"  Expectancy: ${data['expectancy']:,.2f}")


def main():
    """Main execution function"""
    # Set paths
    judas_swings_path = "/home/runner/work/Backtest-Trading/Backtest-Trading/judas_swing_results.csv"
    data_dir = "/home/runner/work/Backtest-Trading/Backtest-Trading"
    
    # Initialize backtester
    backtester = IFVGBacktester(judas_swings_path, data_dir)
    
    # Load Judas Swings
    backtester.load_judas_swings()
    
    # Run backtests for both timeframes
    timeframes = ['1m', '5m']
    
    for timeframe in timeframes:
        # Run backtest
        df_trades = backtester.run_backtest(timeframe)
        
        if len(df_trades) > 0:
            # Save results
            output_file = f"{data_dir}/ifvg_backtest_{timeframe}.csv"
            df_trades.to_csv(output_file, index=False)
            print(f"\nResults saved to: {output_file}")
            
            # Calculate and print statistics
            stats = backtester.calculate_statistics(df_trades)
            backtester.print_statistics(stats, timeframe)
        else:
            print(f"\nNo trades to save for {timeframe}")
    
    print("\n" + "="*60)
    print("BACKTEST COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
