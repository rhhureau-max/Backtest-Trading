"""
NQ (Nasdaq) ICT Filter Backtest
================================
This script tests ICT-based institutional filters on the London Manipulation strategy
to improve trade quality by filtering with higher timeframe structure.

Filters tested:
1. H1 Market Structure Shift (MSS)
2. Midnight Open (Power of 3)
3. Combination of both filters
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import List, Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class NQICTFilterBacktester:
    """ICT Filter backtesting class for NQ trading strategy"""
    
    # Constants
    MAX_BARS_LOOKAHEAD = 1000  # Maximum bars to check for TP/SL
    SL3_BUFFER = 0.25  # Small buffer in points for SL3 (aggressive)
    START_YEAR = 2018
    END_YEAR = 2026
    SWING_LOOKBACK = 2  # Bars to look back/forward for swing detection
    
    def __init__(self, data_directory: str):
        """
        Initialize the ICT filter backtester
        
        Args:
            data_directory: Path to directory containing CSV files
        """
        self.data_directory = data_directory
        self.df_5m = None
        self.df_1h = None
        self.setups = []
        
    def load_5m_data(self) -> pd.DataFrame:
        """Load all 5-minute CSV files"""
        print("Loading 5-minute data files...")
        all_data = []
        
        for year in range(self.START_YEAR, self.END_YEAR):
            filename = f"{year} 5m.csv"
            filepath = os.path.join(self.data_directory, filename)
            
            if os.path.exists(filepath):
                print(f"  Loading {filename}...")
                df = pd.read_csv(
                    filepath,
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )
                all_data.append(df)
        
        if not all_data:
            raise FileNotFoundError("No 5m data files found!")
        
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df['DateTime'] = pd.to_datetime(
            combined_df['Date'] + ' ' + combined_df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        for col in ['Open', 'High', 'Low', 'Close']:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        combined_df['Date_only'] = combined_df['DateTime'].dt.date
        combined_df['Hour'] = combined_df['DateTime'].dt.hour
        combined_df['Minute'] = combined_df['DateTime'].dt.minute
        
        print(f"Total 5m records loaded: {len(combined_df)}")
        print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
        
        self.df_5m = combined_df
        return combined_df
    
    def load_1h_data(self) -> pd.DataFrame:
        """Load all 1-hour CSV files"""
        print("\nLoading 1-hour data files...")
        all_data = []
        
        for year in range(self.START_YEAR, self.END_YEAR):
            filename = f"{year} 1H.csv"
            filepath = os.path.join(self.data_directory, filename)
            
            if os.path.exists(filepath):
                print(f"  Loading {filename}...")
                df = pd.read_csv(
                    filepath,
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1
                )
                all_data.append(df)
        
        if not all_data:
            raise FileNotFoundError("No 1H data files found!")
        
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df['DateTime'] = pd.to_datetime(
            combined_df['Date'] + ' ' + combined_df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        for col in ['Open', 'High', 'Low', 'Close']:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        
        print(f"Total 1H records loaded: {len(combined_df)}")
        
        self.df_1h = combined_df
        return combined_df
    
    def detect_swings_1h(self):
        """
        Detect swing highs and lows on 1H timeframe
        A swing high is higher than 2 bars before and 2 bars after
        A swing low is lower than 2 bars before and 2 bars after
        """
        print("\nDetecting H1 swing points...")
        
        self.df_1h['Swing_High'] = False
        self.df_1h['Swing_Low'] = False
        self.df_1h['Swing_High_Price'] = np.nan
        self.df_1h['Swing_Low_Price'] = np.nan
        
        lookback = self.SWING_LOOKBACK
        
        for i in range(lookback, len(self.df_1h) - lookback):
            current_high = self.df_1h.loc[i, 'High']
            current_low = self.df_1h.loc[i, 'Low']
            
            # Check swing high
            is_swing_high = True
            for j in range(i - lookback, i + lookback + 1):
                if j != i and self.df_1h.loc[j, 'High'] >= current_high:
                    is_swing_high = False
                    break
            
            if is_swing_high:
                self.df_1h.loc[i, 'Swing_High'] = True
                self.df_1h.loc[i, 'Swing_High_Price'] = current_high
            
            # Check swing low
            is_swing_low = True
            for j in range(i - lookback, i + lookback + 1):
                if j != i and self.df_1h.loc[j, 'Low'] <= current_low:
                    is_swing_low = False
                    break
            
            if is_swing_low:
                self.df_1h.loc[i, 'Swing_Low'] = True
                self.df_1h.loc[i, 'Swing_Low_Price'] = current_low
        
        swing_highs = self.df_1h['Swing_High'].sum()
        swing_lows = self.df_1h['Swing_Low'].sum()
        print(f"Detected {swing_highs} swing highs and {swing_lows} swing lows on H1")
    
    def get_h1_bias_at_time(self, target_datetime: datetime) -> Optional[str]:
        """
        Get the H1 Market Structure bias at a specific time
        Returns 'bullish', 'bearish', or None
        """
        # Get H1 data up to this time
        h1_before = self.df_1h[self.df_1h['DateTime'] <= target_datetime].copy()
        
        if len(h1_before) < 10:
            return None
        
        # Find the last confirmed swing high and low
        last_swing_high_idx = h1_before[h1_before['Swing_High']].index
        last_swing_low_idx = h1_before[h1_before['Swing_Low']].index
        
        if len(last_swing_high_idx) == 0 or len(last_swing_low_idx) == 0:
            return None
        
        last_swing_high = last_swing_high_idx[-1]
        last_swing_low = last_swing_low_idx[-1]
        
        last_swing_high_price = h1_before.loc[last_swing_high, 'Swing_High_Price']
        last_swing_low_price = h1_before.loc[last_swing_low, 'Swing_Low_Price']
        
        # Get current close price
        current_close = h1_before.iloc[-1]['Close']
        
        # Check for Break of Structure (BOS)
        # Bullish bias: Price closed above last swing high
        if current_close > last_swing_high_price:
            return 'bullish'
        
        # Bearish bias: Price closed below last swing low
        if current_close < last_swing_low_price:
            return 'bearish'
        
        return None
    
    def get_midnight_open(self, date) -> Optional[float]:
        """
        Get the midnight open price (00:00 Chicago time) for a given date
        """
        # Find the 00:00 candle on the 5m timeframe for the current day
        midnight_candles = self.df_5m[
            (self.df_5m['Date_only'] == date) &
            (self.df_5m['Hour'] == 0) &
            (self.df_5m['Minute'] == 0)
        ]
        
        if len(midnight_candles) > 0:
            return midnight_candles.iloc[0]['Open']
        
        return None
    
    def identify_tokyo_session(self, date) -> Optional[Dict]:
        """Identify Tokyo session for a given date"""
        previous_date = date - timedelta(days=1)
        
        tokyo_data = self.df_5m[
            (self.df_5m['Date_only'] == previous_date) &
            (self.df_5m['Hour'] >= 19) &
            (self.df_5m['Hour'] < 24)
        ]
        
        if len(tokyo_data) == 0:
            return None
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        tokyo_eq = (tokyo_high + tokyo_low) / 2
        
        return {
            'Tokyo_High': tokyo_high,
            'Tokyo_Low': tokyo_low,
            'Tokyo_EQ': tokyo_eq
        }
    
    def detect_fvg(self, df_slice: pd.DataFrame, fvg_type: str) -> List[Dict]:
        """Detect Fair Value Gaps"""
        fvgs = []
        
        if len(df_slice) < 3:
            return fvgs
        
        df_slice = df_slice.reset_index(drop=True)
        
        for i in range(2, len(df_slice)):
            if fvg_type == 'bullish':
                if df_slice.loc[i-2, 'Low'] > df_slice.loc[i, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i, 'High'],
                        'gap_high': df_slice.loc[i-2, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime']
                    })
            elif fvg_type == 'bearish':
                if df_slice.loc[i, 'Low'] > df_slice.loc[i-2, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i-2, 'High'],
                        'gap_high': df_slice.loc[i, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime']
                    })
        
        return fvgs
    
    def check_sweep(self, killzone_data: pd.DataFrame, tokyo_high: float, tokyo_low: float) -> Dict:
        """Check if price sweeps Tokyo levels"""
        high_swept = False
        low_swept = False
        sweep_high_extreme = None
        sweep_low_extreme = None
        first_high_sweep_idx = None
        first_low_sweep_idx = None
        
        for idx, row in killzone_data.iterrows():
            if row['High'] > tokyo_high:
                high_swept = True
                if sweep_high_extreme is None or row['High'] > sweep_high_extreme:
                    sweep_high_extreme = row['High']
                if first_high_sweep_idx is None:
                    first_high_sweep_idx = idx
            
            if row['Low'] < tokyo_low:
                low_swept = True
                if sweep_low_extreme is None or row['Low'] < sweep_low_extreme:
                    sweep_low_extreme = row['Low']
                if first_low_sweep_idx is None:
                    first_low_sweep_idx = idx
        
        if high_swept and low_swept:
            if first_high_sweep_idx < first_low_sweep_idx:
                return {'sweep_type': 'high', 'sweep_extreme': sweep_high_extreme}
            else:
                return {'sweep_type': 'low', 'sweep_extreme': sweep_low_extreme}
        elif high_swept:
            return {'sweep_type': 'high', 'sweep_extreme': sweep_high_extreme}
        elif low_swept:
            return {'sweep_type': 'low', 'sweep_extreme': sweep_low_extreme}
        
        return {'sweep_type': None, 'sweep_extreme': None}
    
    def find_entry_signal(self, killzone_data: pd.DataFrame, sweep_info: Dict, trade_type: str) -> Optional[Dict]:
        """Find entry signal based on FVG inversion"""
        killzone_data = killzone_data.reset_index(drop=True)
        
        if trade_type == 'short':
            fvgs = self.detect_fvg(killzone_data, 'bullish')
            
            for fvg in fvgs:
                for i in range(fvg['idx'] + 1, len(killzone_data)):
                    if killzone_data.loc[i, 'Close'] < fvg['gap_low']:
                        return {
                            'entry_idx': i,
                            'entry_price': killzone_data.loc[i, 'Close'],
                            'entry_datetime': killzone_data.loc[i, 'DateTime'],
                            'signal_candle_high': killzone_data.loc[i, 'High'],
                            'signal_candle_low': killzone_data.loc[i, 'Low'],
                            'fvg': fvg
                        }
        
        elif trade_type == 'long':
            fvgs = self.detect_fvg(killzone_data, 'bearish')
            
            for fvg in fvgs:
                for i in range(fvg['idx'] + 1, len(killzone_data)):
                    if killzone_data.loc[i, 'Close'] > fvg['gap_high']:
                        return {
                            'entry_idx': i,
                            'entry_price': killzone_data.loc[i, 'Close'],
                            'entry_datetime': killzone_data.loc[i, 'DateTime'],
                            'signal_candle_high': killzone_data.loc[i, 'High'],
                            'signal_candle_low': killzone_data.loc[i, 'Low'],
                            'fvg': fvg
                        }
        
        return None
    
    def calculate_sl3(self, entry_info: Dict, trade_type: str) -> float:
        """Calculate SL3 (Signal Candle stop loss)"""
        entry_price = entry_info['entry_price']
        
        if trade_type == 'short':
            sl3 = max(entry_info['signal_candle_high'], entry_price) + self.SL3_BUFFER
        else:
            sl3 = min(entry_info['signal_candle_low'], entry_price) - self.SL3_BUFFER
        
        return sl3
    
    def simulate_trade(self, entry_info: Dict, trade_type: str, sl3: float, start_idx: int) -> str:
        """Simulate trade with SL3 and TP at 1R"""
        entry_price = entry_info['entry_price']
        risk = abs(entry_price - sl3)
        
        if trade_type == 'short':
            tp = entry_price - risk
        else:
            tp = entry_price + risk
        
        end_idx = min(start_idx + self.MAX_BARS_LOOKAHEAD, len(self.df_5m))
        future_data = self.df_5m.iloc[start_idx:end_idx]
        
        if len(future_data) == 0:
            return 'loss'
        
        highs = future_data['High'].values
        lows = future_data['Low'].values
        
        for i in range(len(future_data)):
            if trade_type == 'short':
                if highs[i] >= sl3:
                    return 'loss'
                if lows[i] <= tp:
                    return 'win'
            else:
                if lows[i] <= sl3:
                    return 'loss'
                if highs[i] >= tp:
                    return 'win'
        
        return 'loss'
    
    def identify_all_setups(self):
        """Identify all valid trading setups without filters"""
        print("\n" + "="*70)
        print("IDENTIFYING ALL TRADING SETUPS (SL3 + 1R Strategy)")
        print("="*70)
        
        self.setups = []
        unique_dates = sorted(self.df_5m['Date_only'].unique())
        
        print(f"\nAnalyzing {len(unique_dates)} trading days...")
        processed = 0
        
        for current_date in unique_dates:
            processed += 1
            if processed % 100 == 0:
                print(f"  Processed {processed}/{len(unique_dates)} days... ({processed/len(unique_dates)*100:.1f}%)")
            
            tokyo_levels = self.identify_tokyo_session(current_date)
            if tokyo_levels is None:
                continue
            
            killzone_data = self.df_5m[
                (self.df_5m['Date_only'] == current_date) &
                (self.df_5m['Hour'] >= 1) &
                (self.df_5m['Hour'] < 4)
            ].copy()
            
            if len(killzone_data) == 0:
                continue
            
            sweep_info = self.check_sweep(killzone_data, tokyo_levels['Tokyo_High'], tokyo_levels['Tokyo_Low'])
            if sweep_info['sweep_type'] is None:
                continue
            
            trade_type = 'short' if sweep_info['sweep_type'] == 'high' else 'long'
            entry_info = self.find_entry_signal(killzone_data, sweep_info, trade_type)
            
            if entry_info is None:
                continue
            
            sl3 = self.calculate_sl3(entry_info, trade_type)
            entry_datetime = entry_info['entry_datetime']
            main_df_idx = self.df_5m[self.df_5m['DateTime'] == entry_datetime].index[0]
            
            # Get H1 bias at entry time
            h1_bias = self.get_h1_bias_at_time(entry_datetime)
            
            # Get midnight open
            midnight_open = self.get_midnight_open(current_date)
            
            setup = {
                'date': current_date,
                'type': trade_type,
                'entry_info': entry_info,
                'sweep_extreme': sweep_info['sweep_extreme'],
                'tokyo_levels': tokyo_levels,
                'sl3': sl3,
                'main_df_idx': main_df_idx,
                'h1_bias': h1_bias,
                'midnight_open': midnight_open,
                'entry_price': entry_info['entry_price']
            }
            
            self.setups.append(setup)
        
        print(f"\nTotal setups identified: {len(self.setups)}")
        return self.setups
    
    def run_filter_comparison(self) -> pd.DataFrame:
        """Run backtest with different ICT filters"""
        print("\n" + "="*70)
        print("RUNNING ICT FILTER COMPARISON")
        print("="*70)
        
        results = []
        
        # Case A: No Filter (Baseline)
        print("\n  Processing Case A: No Filter (Baseline)...")
        filtered_setups_a = self.setups
        results.append(self.calculate_metrics(filtered_setups_a, "A_No_Filter"))
        
        # Case B: H1 Market Structure Shift Filter
        print("  Processing Case B: H1 MSS Filter...")
        filtered_setups_b = []
        for setup in self.setups:
            h1_bias = setup['h1_bias']
            trade_type = setup['type']
            
            # Only take trades aligned with H1 bias
            if h1_bias == 'bullish' and trade_type == 'long':
                filtered_setups_b.append(setup)
            elif h1_bias == 'bearish' and trade_type == 'short':
                filtered_setups_b.append(setup)
        
        results.append(self.calculate_metrics(filtered_setups_b, "B_H1_MSS"))
        
        # Case C: Midnight Open Filter
        print("  Processing Case C: Midnight Open Filter...")
        filtered_setups_c = []
        for setup in self.setups:
            midnight_open = setup['midnight_open']
            trade_type = setup['type']
            entry_price = setup['entry_price']
            
            if midnight_open is None:
                continue
            
            # Short only if above midnight open (premium)
            if trade_type == 'short' and entry_price > midnight_open:
                filtered_setups_c.append(setup)
            # Long only if below midnight open (discount)
            elif trade_type == 'long' and entry_price < midnight_open:
                filtered_setups_c.append(setup)
        
        results.append(self.calculate_metrics(filtered_setups_c, "C_Midnight_Open"))
        
        # Case D: Combo (Both filters must align)
        print("  Processing Case D: Combo Filter (H1 MSS + Midnight)...")
        filtered_setups_d = []
        for setup in self.setups:
            h1_bias = setup['h1_bias']
            midnight_open = setup['midnight_open']
            trade_type = setup['type']
            entry_price = setup['entry_price']
            
            if midnight_open is None:
                continue
            
            # Both filters must agree
            h1_aligned = (h1_bias == 'bullish' and trade_type == 'long') or (h1_bias == 'bearish' and trade_type == 'short')
            midnight_aligned = (trade_type == 'short' and entry_price > midnight_open) or (trade_type == 'long' and entry_price < midnight_open)
            
            if h1_aligned and midnight_aligned:
                filtered_setups_d.append(setup)
        
        results.append(self.calculate_metrics(filtered_setups_d, "D_Combo"))
        
        results_df = pd.DataFrame(results)
        return results_df
    
    def calculate_metrics(self, setups: List[Dict], filter_name: str) -> Dict:
        """Calculate performance metrics for a filtered set of setups"""
        if len(setups) == 0:
            return {
                'Nom_Filtre': filter_name,
                'Nb_Trades': 0,
                'Winrate_%': 0.0,
                'Net_Profit_Points': 0.0,
                'Gross_Win_Points': 0.0,
                'Gross_Loss_Points': 0.0,
                'Profit_Factor': 0.0,
                'Max_Drawdown': 0
            }
        
        wins = 0
        losses = 0
        gross_win = 0.0
        gross_loss = 0.0
        
        for setup in setups:
            result = self.simulate_trade(
                setup['entry_info'],
                setup['type'],
                setup['sl3'],
                setup['main_df_idx']
            )
            
            entry_price = setup['entry_price']
            sl3 = setup['sl3']
            risk = abs(entry_price - sl3)
            
            if result == 'win':
                wins += 1
                gross_win += risk  # 1R profit
            else:
                losses += 1
                gross_loss += risk  # 1R loss
        
        total_trades = wins + losses
        winrate = (wins / total_trades * 100) if total_trades > 0 else 0
        net_profit = gross_win - gross_loss
        profit_factor = (gross_win / gross_loss) if gross_loss > 0 else 0
        
        # Calculate max consecutive losses
        consecutive_losses = []
        current_streak = 0
        
        for setup in setups:
            result = self.simulate_trade(
                setup['entry_info'],
                setup['type'],
                setup['sl3'],
                setup['main_df_idx']
            )
            
            if result == 'loss':
                current_streak += 1
            else:
                if current_streak > 0:
                    consecutive_losses.append(current_streak)
                current_streak = 0
        
        if current_streak > 0:
            consecutive_losses.append(current_streak)
        
        max_dd = max(consecutive_losses) if consecutive_losses else 0
        
        return {
            'Nom_Filtre': filter_name,
            'Nb_Trades': total_trades,
            'Winrate_%': round(winrate, 2),
            'Net_Profit_Points': round(net_profit, 2),
            'Gross_Win_Points': round(gross_win, 2),
            'Gross_Loss_Points': round(gross_loss, 2),
            'Profit_Factor': round(profit_factor, 2),
            'Max_Drawdown': max_dd
        }
    
    def run_full_backtest(self):
        """Run the complete ICT filter backtest"""
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║        NQ ICT FILTER BACKTEST                                    ║
    ║        Testing H1 Structure & Midnight Open Filters              ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
        
        # Load data
        self.load_5m_data()
        self.load_1h_data()
        
        # Detect swings on H1
        self.detect_swings_1h()
        
        # Identify all setups
        self.identify_all_setups()
        
        if len(self.setups) == 0:
            print("\nNo valid setups found!")
            return None
        
        # Run filter comparison
        results_df = self.run_filter_comparison()
        
        # Print results
        print("\n" + "="*70)
        print("ICT FILTER COMPARISON RESULTS")
        print("="*70)
        print("\nPerformance Comparison Across 4 Filter Cases:\n")
        print(results_df.to_string(index=False))
        
        # Export to CSV
        output_file = 'nq_ict_filter_results.csv'
        results_df.to_csv(output_file, index=False)
        print(f"\n{'='*70}")
        print(f"Results exported to: {os.path.abspath(output_file)}")
        print("="*70)
        
        # Analysis
        self.print_analysis(results_df)
        
        return results_df
    
    def print_analysis(self, results_df: pd.DataFrame):
        """Print analysis and recommendations"""
        print("\n" + "="*70)
        print("ANALYSIS AND RECOMMENDATIONS")
        print("="*70)
        
        # Best by winrate
        best_winrate_idx = results_df['Winrate_%'].idxmax()
        best_winrate = results_df.loc[best_winrate_idx]
        
        print(f"\n1. Best Win Rate:")
        print(f"   Filter: {best_winrate['Nom_Filtre']}")
        print(f"   Win Rate: {best_winrate['Winrate_%']:.2f}%")
        print(f"   Trades: {best_winrate['Nb_Trades']}")
        print(f"   Net Profit: {best_winrate['Net_Profit_Points']:.2f} points")
        print(f"   Profit Factor: {best_winrate['Profit_Factor']:.2f}")
        
        # Best by profit factor
        best_pf_idx = results_df['Profit_Factor'].idxmax()
        best_pf = results_df.loc[best_pf_idx]
        
        print(f"\n2. Best Profit Factor:")
        print(f"   Filter: {best_pf['Nom_Filtre']}")
        print(f"   Profit Factor: {best_pf['Profit_Factor']:.2f}")
        print(f"   Win Rate: {best_pf['Winrate_%']:.2f}%")
        print(f"   Trades: {best_pf['Nb_Trades']}")
        print(f"   Net Profit: {best_pf['Net_Profit_Points']:.2f} points")
        
        # Best by net profit
        best_profit_idx = results_df['Net_Profit_Points'].idxmax()
        best_profit = results_df.loc[best_profit_idx]
        
        print(f"\n3. Best Net Profit:")
        print(f"   Filter: {best_profit['Nom_Filtre']}")
        print(f"   Net Profit: {best_profit['Net_Profit_Points']:.2f} points")
        print(f"   Win Rate: {best_profit['Winrate_%']:.2f}%")
        print(f"   Trades: {best_profit['Nb_Trades']}")
        print(f"   Profit Factor: {best_profit['Profit_Factor']:.2f}")
        
        # Filter effectiveness
        baseline = results_df[results_df['Nom_Filtre'] == 'A_No_Filter'].iloc[0]
        
        print(f"\n4. Filter Effectiveness Comparison:")
        for idx, row in results_df.iterrows():
            if row['Nom_Filtre'] != 'A_No_Filter':
                trade_reduction = ((baseline['Nb_Trades'] - row['Nb_Trades']) / baseline['Nb_Trades'] * 100) if baseline['Nb_Trades'] > 0 else 0
                winrate_improvement = row['Winrate_%'] - baseline['Winrate_%']
                
                print(f"\n   {row['Nom_Filtre']}:")
                print(f"     Trade Reduction: {trade_reduction:.1f}% ({baseline['Nb_Trades']} → {row['Nb_Trades']} trades)")
                print(f"     Winrate Change: {winrate_improvement:+.2f}% ({baseline['Winrate_%']:.2f}% → {row['Winrate_%']:.2f}%)")
                print(f"     Profit Factor: {row['Profit_Factor']:.2f} (baseline: {baseline['Profit_Factor']:.2f})")
        
        # Final recommendation
        print(f"\n5. Final Recommendation:")
        
        # Find filters with >65% winrate and positive profit factor
        good_filters = results_df[
            (results_df['Winrate_%'] >= 65) &
            (results_df['Profit_Factor'] > 1.0) &
            (results_df['Nb_Trades'] > 0)
        ]
        
        if len(good_filters) > 0:
            best_overall = good_filters.loc[good_filters['Profit_Factor'].idxmax()]
            print(f"   ✅ USE {best_overall['Nom_Filtre'].upper()}")
            print(f"   Reason: Achieves {best_overall['Winrate_%']:.2f}% win rate (target: 65-70%)")
            print(f"   with {best_overall['Profit_Factor']:.2f} profit factor over {best_overall['Nb_Trades']} trades.")
        else:
            print(f"   ⚠️  NO FILTER MEETS TARGET (65-70% winrate + PF > 1.0)")
            print(f"   Best available: {best_winrate['Nom_Filtre']} with {best_winrate['Winrate_%']:.2f}% winrate")
        
        print("\n" + "="*70)
        print("BACKTEST COMPLETE")
        print("="*70)


if __name__ == "__main__":
    data_directory = os.environ.get('NQ_DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    
    backtester = NQICTFilterBacktester(data_directory)
    results = backtester.run_full_backtest()
