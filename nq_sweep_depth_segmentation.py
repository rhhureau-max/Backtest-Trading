"""
NQ Sweep Depth Segmentation Analysis
======================================
This script segments trades by sweep depth to identify the "ideal zone" for manipulation.

Strategy: SL3 (Signal Candle) + TP 1R
Analysis Goal: Test if sweep depth has non-linear relationship with profitability

Segmentation Buckets:
- Panier A: Micro-Manipulation (< 10 points)
- Panier B: Standard Sweep (10 to 15 points)
- Panier C: Extended Sweep (15 to 20 points)
- Panier D: Deep Sweep / Breakout (>= 20 points)

Hypothesis: Sweeps > 20 points are continuations (losing trades in reversal strategy)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional
import warnings

warnings.filterwarnings('ignore')


class NQSweepDepthSegmentation:
    """Sweep Depth Segmentation Analysis for NQ trading strategy"""
    
    # Constants
    MAX_BARS_LOOKAHEAD = 1000  # Maximum bars to check for TP/SL
    SL3_BUFFER = 0.25  # Buffer in points for SL3
    START_YEAR = 2018
    END_YEAR = 2026
    
    # Segmentation buckets
    BUCKETS = {
        'A': {'name': 'Micro-Manipulation', 'range': '< 10 pts', 'min': 0, 'max': 10},
        'B': {'name': 'Standard Sweep', 'range': '10-15 pts', 'min': 10, 'max': 15},
        'C': {'name': 'Extended Sweep', 'range': '15-20 pts', 'min': 15, 'max': 20},
        'D': {'name': 'Deep Sweep / Breakout', 'range': '>= 20 pts', 'min': 20, 'max': float('inf')}
    }
    
    def __init__(self, data_directory: str):
        """
        Initialize the analyzer
        
        Args:
            data_directory: Path to directory containing CSV files
        """
        self.data_directory = data_directory
        self.df = None
        self.all_trades = []
        
    def load_data(self) -> pd.DataFrame:
        """Load all 5-minute CSV files from 2018-2025"""
        print("Loading data files...")
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
                    skiprows=1,
                    encoding='utf-8-sig'
                )
                all_data.append(df)
            else:
                print(f"  Warning: {filename} not found")
        
        if not all_data:
            raise FileNotFoundError("No data files found!")
        
        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Parse datetime - format DD/MM/YYYY and HH:MM:SS
        combined_df['DateTime'] = pd.to_datetime(
            combined_df['Date'] + ' ' + combined_df['Time'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
        
        # Sort by datetime
        combined_df = combined_df.sort_values('DateTime').reset_index(drop=True)
        
        # Extract time components
        combined_df['Date_only'] = combined_df['DateTime'].dt.date
        combined_df['Hour'] = combined_df['DateTime'].dt.hour
        combined_df['Minute'] = combined_df['DateTime'].dt.minute
        
        print(f"Total records loaded: {len(combined_df)}")
        print(f"Date range: {combined_df['DateTime'].min()} to {combined_df['DateTime'].max()}")
        
        self.df = combined_df
        return combined_df
    
    def identify_tokyo_session(self, date) -> Optional[Dict]:
        """
        Identify Tokyo session for a given date (19:00-23:00 previous day)
        
        Args:
            date: The current trading date (Day N)
            
        Returns:
            Dictionary with Tokyo_High, Tokyo_Low, Tokyo_EQ, or None if not found
        """
        previous_date = date - timedelta(days=1)
        
        tokyo_data = self.df[
            (self.df['Date_only'] == previous_date) &
            (self.df['Hour'] >= 19) &
            (self.df['Hour'] < 24)
        ]
        
        if len(tokyo_data) == 0:
            return None
        
        tokyo_high = tokyo_data['High'].max()
        tokyo_low = tokyo_data['Low'].min()
        tokyo_eq = (tokyo_high + tokyo_low) / 2
        
        return {
            'Tokyo_High': tokyo_high,
            'Tokyo_Low': tokyo_low,
            'Tokyo_EQ': tokyo_eq,
            'session_date': previous_date
        }
    
    def detect_fvg(self, df_slice: pd.DataFrame, fvg_type: str) -> List[Dict]:
        """
        Detect Fair Value Gaps in the data
        
        Args:
            df_slice: DataFrame slice to analyze
            fvg_type: 'bullish' or 'bearish'
            
        Returns:
            List of FVG dictionaries with start_idx, gap_low, gap_high
        """
        fvgs = []
        
        if len(df_slice) < 3:
            return fvgs
        
        df_slice = df_slice.reset_index(drop=True)
        
        for i in range(2, len(df_slice)):
            if fvg_type == 'bullish':
                # Bullish FVG: Low of candle (i-2) > High of candle (i)
                if df_slice.loc[i-2, 'Low'] > df_slice.loc[i, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i, 'High'],
                        'gap_high': df_slice.loc[i-2, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime']
                    })
            elif fvg_type == 'bearish':
                # Bearish FVG: Low of candle (i) > High of candle (i-2)
                if df_slice.loc[i, 'Low'] > df_slice.loc[i-2, 'High']:
                    fvgs.append({
                        'idx': i,
                        'gap_low': df_slice.loc[i-2, 'High'],
                        'gap_high': df_slice.loc[i, 'Low'],
                        'datetime': df_slice.loc[i, 'DateTime']
                    })
        
        return fvgs
    
    def check_sweep(self, killzone_data: pd.DataFrame, tokyo_high: float, tokyo_low: float) -> Dict:
        """
        Check if price sweeps Tokyo_High or Tokyo_Low during killzone
        
        Returns:
            Dictionary with sweep_type ('high', 'low', or None), sweep_extreme
        """
        high_swept = False
        low_swept = False
        sweep_high_extreme = None
        sweep_low_extreme = None
        first_high_sweep_idx = None
        first_low_sweep_idx = None
        
        for idx, row in killzone_data.iterrows():
            # Check if high was swept
            if row['High'] > tokyo_high:
                high_swept = True
                if sweep_high_extreme is None or row['High'] > sweep_high_extreme:
                    sweep_high_extreme = row['High']
                if first_high_sweep_idx is None:
                    first_high_sweep_idx = idx
            
            # Check if low was swept
            if row['Low'] < tokyo_low:
                low_swept = True
                if sweep_low_extreme is None or row['Low'] < sweep_low_extreme:
                    sweep_low_extreme = row['Low']
                if first_low_sweep_idx is None:
                    first_low_sweep_idx = idx
        
        # Determine which sweep occurred first
        if high_swept and not low_swept:
            return {
                'sweep_type': 'high',
                'sweep_extreme': sweep_high_extreme
            }
        elif low_swept and not high_swept:
            return {
                'sweep_type': 'low',
                'sweep_extreme': sweep_low_extreme
            }
        elif high_swept and low_swept:
            if first_high_sweep_idx < first_low_sweep_idx:
                return {
                    'sweep_type': 'high',
                    'sweep_extreme': sweep_high_extreme
                }
            else:
                return {
                    'sweep_type': 'low',
                    'sweep_extreme': sweep_low_extreme
                }
        
        return {
            'sweep_type': None,
            'sweep_extreme': None
        }
    
    def find_entry_signal(self, killzone_data: pd.DataFrame, sweep_info: Dict, 
                          trade_type: str) -> Optional[Dict]:
        """
        Find entry signal based on FVG inversion
        
        Args:
            killzone_data: Data during killzone period
            sweep_info: Information about the sweep
            trade_type: 'short' or 'long'
            
        Returns:
            Entry information or None
        """
        killzone_data = killzone_data.reset_index(drop=True)
        
        if trade_type == 'short':
            # Look for bullish FVG during/after sweep, then candle closing below it
            fvgs = self.detect_fvg(killzone_data, 'bullish')
            
            for fvg in fvgs:
                # Check subsequent candles for close below FVG
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
            # Look for bearish FVG during/after sweep, then candle closing above it
            fvgs = self.detect_fvg(killzone_data, 'bearish')
            
            for fvg in fvgs:
                # Check subsequent candles for close above FVG
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
        """
        Calculate SL3 (Stop Loss Signal Candle)
        
        Args:
            entry_info: Entry information
            trade_type: 'short' or 'long'
            
        Returns:
            SL3 price level
        """
        entry_price = entry_info['entry_price']
        
        if trade_type == 'short':
            # SL3: Signal Candle High + small buffer
            sl3 = max(entry_info['signal_candle_high'], entry_price) + self.SL3_BUFFER
        else:
            # SL3: Signal Candle Low - small buffer
            sl3 = min(entry_info['signal_candle_low'], entry_price) - self.SL3_BUFFER
        
        return sl3
    
    def calculate_sweep_depth(self, tokyo_reference: float, sweep_extreme: float, trade_type: str) -> float:
        """
        Calculate Sweep_Depth: Absolute distance in points between the broken level
        and the extreme price reached before entry validation.
        
        Args:
            tokyo_reference: Tokyo_High (for shorts) or Tokyo_Low (for longs)
            sweep_extreme: Highest high (for shorts) or lowest low (for longs) during sweep
            trade_type: 'short' or 'long'
            
        Returns:
            Sweep depth in points (always positive)
        """
        sweep_depth = abs(sweep_extreme - tokyo_reference)
        return sweep_depth
    
    def simulate_trade(self, entry_info: Dict, trade_type: str, sl3: float, start_idx: int) -> str:
        """
        Simulate a trade with SL3 and TP at 1R
        
        Args:
            entry_info: Entry information
            trade_type: 'short' or 'long'
            sl3: Stop loss level
            start_idx: Start index in the full DataFrame
            
        Returns:
            Result: 'win' or 'loss'
        """
        entry_price = entry_info['entry_price']
        risk = abs(entry_price - sl3)
        
        # Calculate TP at 1R
        if trade_type == 'short':
            tp = entry_price - risk
        else:
            tp = entry_price + risk
        
        # Get future data after entry
        end_idx = min(start_idx + self.MAX_BARS_LOOKAHEAD, len(self.df))
        future_data = self.df.iloc[start_idx:end_idx]
        
        if len(future_data) == 0:
            return 'loss'
        
        # Use vectorized operations for better performance
        highs = future_data['High'].values
        lows = future_data['Low'].values
        
        for i in range(len(future_data)):
            high = highs[i]
            low = lows[i]
            
            if trade_type == 'short':
                # Check if stop loss is hit
                if high >= sl3:
                    return 'loss'
                # Check if TP is hit
                if low <= tp:
                    return 'win'
            else:  # long
                # Check if stop loss is hit
                if low <= sl3:
                    return 'loss'
                # Check if TP is hit
                if high >= tp:
                    return 'win'
        
        # If we exit the loop without hitting TP or SL
        return 'loss'
    
    def identify_all_setups(self):
        """
        Identify all valid setups and calculate sweep depth
        """
        print("\n" + "="*70)
        print("IDENTIFYING ALL TRADING SETUPS (SL3 + 1R)")
        print("="*70)
        
        if self.df is None:
            self.load_data()
        
        # Get unique dates for iteration
        unique_dates = sorted(self.df['Date_only'].unique())
        
        print(f"\nAnalyzing {len(unique_dates)} trading days...")
        
        processed = 0
        
        for current_date in unique_dates:
            processed += 1
            if processed % 100 == 0:
                print(f"  Processed {processed}/{len(unique_dates)} days... ({processed/len(unique_dates)*100:.1f}%)")
            
            # Get Tokyo session reference levels (from previous day)
            tokyo_levels = self.identify_tokyo_session(current_date)
            
            if tokyo_levels is None:
                continue
            
            # Get killzone data (01:00-04:00 on current date)
            killzone_data = self.df[
                (self.df['Date_only'] == current_date) &
                (self.df['Hour'] >= 1) &
                (self.df['Hour'] < 4)
            ].copy()
            
            if len(killzone_data) == 0:
                continue
            
            # Check for sweep of Tokyo levels
            sweep_info = self.check_sweep(
                killzone_data,
                tokyo_levels['Tokyo_High'],
                tokyo_levels['Tokyo_Low']
            )
            
            if sweep_info['sweep_type'] is None:
                continue
            
            # Determine trade type based on sweep
            if sweep_info['sweep_type'] == 'high':
                trade_type = 'short'
                tokyo_reference = tokyo_levels['Tokyo_High']
            else:
                trade_type = 'long'
                tokyo_reference = tokyo_levels['Tokyo_Low']
            
            # Find entry signal
            entry_info = self.find_entry_signal(killzone_data, sweep_info, trade_type)
            
            if entry_info is None:
                continue
            
            # Calculate SL3
            sl3 = self.calculate_sl3(entry_info, trade_type)
            
            # Calculate Sweep_Depth
            sweep_depth = self.calculate_sweep_depth(
                tokyo_reference,
                sweep_info['sweep_extreme'],
                trade_type
            )
            
            # Get the index in the full dataframe where entry occurred
            entry_datetime = entry_info['entry_datetime']
            start_idx = self.df[self.df['DateTime'] == entry_datetime].index[0] + 1
            
            # Simulate trade
            outcome = self.simulate_trade(entry_info, trade_type, sl3, start_idx)
            
            # Calculate profit
            entry_price = entry_info['entry_price']
            risk = abs(entry_price - sl3)
            
            if outcome == 'win':
                profit_points = risk  # 1R
            else:
                profit_points = -risk  # -1R
            
            # Store trade with sweep depth
            trade = {
                'date': current_date,
                'type': trade_type,
                'entry_price': entry_price,
                'stop_loss': sl3,
                'risk': risk,
                'tokyo_high': tokyo_levels['Tokyo_High'],
                'tokyo_low': tokyo_levels['Tokyo_Low'],
                'tokyo_eq': tokyo_levels['Tokyo_EQ'],
                'sweep_extreme': sweep_info['sweep_extreme'],
                'tokyo_reference': tokyo_reference,
                'sweep_depth': sweep_depth,
                'entry_datetime': entry_datetime,
                'outcome': outcome,
                'profit_points': profit_points
            }
            
            self.all_trades.append(trade)
        
        print(f"\nTotal trades identified: {len(self.all_trades)}")
    
    def segment_trades_by_depth(self) -> Dict:
        """
        Segment trades into 4 buckets based on sweep depth
        
        Returns:
            Dictionary with segmented trades for each bucket
        """
        segmented = {}
        
        for bucket_id, bucket_info in self.BUCKETS.items():
            min_depth = bucket_info['min']
            max_depth = bucket_info['max']
            
            if max_depth == float('inf'):
                trades = [t for t in self.all_trades if t['sweep_depth'] >= min_depth]
            else:
                trades = [t for t in self.all_trades 
                         if min_depth <= t['sweep_depth'] < max_depth]
            
            segmented[bucket_id] = trades
        
        return segmented
    
    def calculate_bucket_statistics(self, bucket_trades: List[Dict]) -> Dict:
        """
        Calculate performance statistics for a bucket
        
        Args:
            bucket_trades: List of trades in the bucket
            
        Returns:
            Dictionary with performance metrics
        """
        if not bucket_trades:
            return {
                'Nb_Trades': 0,
                'Winrate_%': 0.0,
                'Net_Profit_Points': 0.0,
                'Avg_Profit_Per_Trade': 0.0,
                'Profit_Factor': 0.0
            }
        
        nb_trades = len(bucket_trades)
        wins = sum(1 for t in bucket_trades if t['outcome'] == 'win')
        losses = sum(1 for t in bucket_trades if t['outcome'] == 'loss')
        
        winrate = (wins / nb_trades * 100) if nb_trades > 0 else 0.0
        
        net_profit = sum(t['profit_points'] for t in bucket_trades)
        avg_profit = net_profit / nb_trades if nb_trades > 0 else 0.0
        
        # Calculate Profit Factor
        gross_profit = sum(t['profit_points'] for t in bucket_trades if t['outcome'] == 'win')
        gross_loss = abs(sum(t['profit_points'] for t in bucket_trades if t['outcome'] == 'loss'))
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0.0
        
        return {
            'Nb_Trades': nb_trades,
            'Winrate_%': round(winrate, 2),
            'Net_Profit_Points': round(net_profit, 2),
            'Avg_Profit_Per_Trade': round(avg_profit, 2),
            'Profit_Factor': round(profit_factor, 2)
        }
    
    def generate_comparative_table(self) -> pd.DataFrame:
        """
        Generate comparative performance table for all buckets
        
        Returns:
            DataFrame with comparative results
        """
        print("\n" + "="*70)
        print("SEGMENTATION ANALYSIS BY SWEEP DEPTH")
        print("="*70)
        
        # Segment trades
        segmented = self.segment_trades_by_depth()
        
        # Build results table
        results = []
        
        for bucket_id in ['A', 'B', 'C', 'D']:
            bucket_info = self.BUCKETS[bucket_id]
            bucket_trades = segmented[bucket_id]
            stats = self.calculate_bucket_statistics(bucket_trades)
            
            results.append({
                'Panier': f"{bucket_id} - {bucket_info['name']}",
                'Range_Depth': bucket_info['range'],
                'Nb_Trades': stats['Nb_Trades'],
                'Winrate_%': stats['Winrate_%'],
                'Net_Profit_Points': stats['Net_Profit_Points'],
                'Avg_Profit_Per_Trade': stats['Avg_Profit_Per_Trade'],
                'Profit_Factor': stats['Profit_Factor']
            })
        
        results_df = pd.DataFrame(results)
        
        # Display table
        print("\n" + "="*70)
        print("TABLEAU COMPARATIF PAR PANIER DE PROFONDEUR")
        print("="*70)
        print(results_df.to_string(index=False))
        
        return results_df
    
    def analyze_and_interpret(self, results_df: pd.DataFrame):
        """
        Analyze results and provide interpretation
        
        Args:
            results_df: DataFrame with bucket results
        """
        print("\n" + "="*70)
        print("ANALYSE ET INTERPRÉTATION")
        print("="*70)
        
        # Find best performing bucket
        best_bucket_idx = results_df['Net_Profit_Points'].idxmax()
        best_bucket = results_df.iloc[best_bucket_idx]
        
        print(f"\n🏆 MEILLEUR PANIER:")
        print(f"   Panier: {best_bucket['Panier']}")
        print(f"   Range: {best_bucket['Range_Depth']}")
        print(f"   Nombre de Trades: {best_bucket['Nb_Trades']}")
        print(f"   Winrate: {best_bucket['Winrate_%']:.2f}%")
        print(f"   Profit Net: {best_bucket['Net_Profit_Points']:.2f} points")
        print(f"   Profit Moyen/Trade: {best_bucket['Avg_Profit_Per_Trade']:.2f} points")
        print(f"   Profit Factor: {best_bucket['Profit_Factor']:.2f}")
        
        # Analyze Panier D (Deep Sweep hypothesis)
        panier_d = results_df[results_df['Panier'].str.startswith('D')].iloc[0]
        
        print(f"\n📊 VALIDATION DE L'HYPOTHÈSE (Panier D - Deep Sweep):")
        print(f"   Hypothèse: Les mouvements > 20 points sont des continuations")
        print(f"   (donc des pertes en stratégie de reversal)")
        print(f"   ")
        print(f"   Résultats Panier D (>= 20 points):")
        print(f"   - Nombre de Trades: {panier_d['Nb_Trades']}")
        print(f"   - Winrate: {panier_d['Winrate_%']:.2f}%")
        print(f"   - Profit Net: {panier_d['Net_Profit_Points']:.2f} points")
        print(f"   - Profit Factor: {panier_d['Profit_Factor']:.2f}")
        
        # Interpretation
        if panier_d['Winrate_%'] < 50:
            print(f"   ")
            print(f"   ✅ HYPOTHÈSE VALIDÉE:")
            print(f"   Le Winrate du Panier D ({panier_d['Winrate_%']:.2f}%) est < 50%,")
            print(f"   ce qui confirme que les sweeps profonds (> 20 pts) sont")
            print(f"   majoritairement des continuations/breakouts et non des manipulations.")
        elif panier_d['Winrate_%'] < results_df['Winrate_%'].mean():
            print(f"   ")
            print(f"   ⚠️  HYPOTHÈSE PARTIELLEMENT VALIDÉE:")
            print(f"   Le Winrate du Panier D ({panier_d['Winrate_%']:.2f}%) est inférieur")
            print(f"   à la moyenne globale ({results_df['Winrate_%'].mean():.2f}%),")
            print(f"   suggérant une tendance vers les continuations, mais pas de manière drastique.")
        else:
            print(f"   ")
            print(f"   ❌ HYPOTHÈSE NON VALIDÉE:")
            print(f"   Le Winrate du Panier D ({panier_d['Winrate_%']:.2f}%) est similaire ou")
            print(f"   supérieur à la moyenne, suggérant que même les sweeps profonds")
            print(f"   peuvent être des manipulations rentables.")
        
        # Overall insights
        print(f"\n💡 INSIGHTS CLÉS:")
        
        # Check if there's a clear pattern
        winrates = results_df['Winrate_%'].tolist()
        if winrates[0] > winrates[1] > winrates[2] > winrates[3]:
            print(f"   - Relation inversement linéaire: Plus le sweep est profond,")
            print(f"     plus le winrate diminue. Zone idéale = sweeps peu profonds.")
        elif winrates[0] < winrates[1] or winrates[1] < winrates[2]:
            print(f"   - Relation non-linéaire détectée: Il existe une 'zone idéale'")
            print(f"     de profondeur de sweep qui maximise la performance.")
        
        # Volume distribution
        total_trades = results_df['Nb_Trades'].sum()
        print(f"   ")
        print(f"   Distribution du volume de trades:")
        for _, row in results_df.iterrows():
            pct = (row['Nb_Trades'] / total_trades * 100) if total_trades > 0 else 0
            print(f"   - {row['Panier']}: {row['Nb_Trades']} trades ({pct:.1f}%)")
    
    def export_results(self, results_df: pd.DataFrame):
        """
        Export results to CSV file
        
        Args:
            results_df: DataFrame with bucket results
        """
        output_file = os.path.join(self.data_directory, 'nq_sweep_depth_segmentation_results.csv')
        results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n" + "="*70)
        print(f"Results exported to: {output_file}")
        print("="*70)
        
        # Also export all trades with sweep depth
        trades_df = pd.DataFrame(self.all_trades)
        trades_output = os.path.join(self.data_directory, 'nq_sweep_depth_all_trades.csv')
        trades_df.to_csv(trades_output, index=False, encoding='utf-8-sig')
        print(f"All trades exported to: {trades_output}")


def main():
    """Main execution function"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║        NQ SWEEP DEPTH SEGMENTATION ANALYSIS                      ║
    ║        Strategy: SL3 (Signal Candle) + TP 1R                     ║
    ║        Analysis: Non-linear relationship identification          ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Set data directory
    data_directory = os.environ.get('NQ_DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize analyzer
    analyzer = NQSweepDepthSegmentation(data_directory)
    
    # Load data
    analyzer.load_data()
    
    # Identify all setups and calculate sweep depth
    analyzer.identify_all_setups()
    
    # Generate comparative table
    results_df = analyzer.generate_comparative_table()
    
    # Analyze and interpret results
    analyzer.analyze_and_interpret(results_df)
    
    # Export results
    analyzer.export_results(results_df)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
