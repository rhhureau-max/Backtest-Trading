#!/usr/bin/env python3
"""
SMT (Smart Money Technique) Divergence Detector

This script analyzes NQ (NASDAQ) and ES (S&P 500) trading data to detect
SMT divergences during London and New York AM trading sessions.

SMT Divergence occurs when:
- Bullish SMT: One asset makes Lower Low (LL) while other makes Higher Low (HL)
  → The asset with HL is the bullish leader (stronger/refuses to go lower)
- Bearish SMT: One asset makes Higher High (HH) while other makes Lower High (LH)
  → The asset with LH is the bearish leader (weaker/refuses to go higher)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from datetime import datetime, time
import os
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')


class SMTDivergenceDetector:
    """Detects SMT divergences between NQ and ES futures."""
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the detector.
        
        Args:
            base_path: Base directory containing CSV files
        """
        self.base_path = base_path
        self.london_session = (time(2, 0), time(5, 0))  # 02:00-05:00 Chicago time
        self.ny_session = (time(8, 30), time(11, 0))    # 08:30-11:00 Chicago time
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load OHLC data from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame with datetime index and OHLC columns
        """
        # Read CSV with semicolon delimiter
        df = pd.read_csv(
            filepath,
            sep=';',
            parse_dates=False,
            dayfirst=True
        )
        
        # Combine date and time columns
        df['datetime'] = pd.to_datetime(
            df['Column1'] + ' ' + df['Column2'],
            format='%d/%m/%Y %H:%M:%S'
        )
        
        # Rename columns
        df = df.rename(columns={
            'Column3': 'Open',
            'Column4': 'High',
            'Column5': 'Low',
            'Column6': 'Close',
            'Column7': 'Volume'
        })
        
        # Set datetime as index and select relevant columns
        df = df.set_index('datetime')[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Convert to numeric
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df.dropna()
    
    def load_nq_data(self, year: int, timeframe: str) -> pd.DataFrame:
        """Load NQ data for a specific year and timeframe."""
        filepath = os.path.join(self.base_path, f"{year} {timeframe}.csv")
        if os.path.exists(filepath):
            return self.load_data(filepath)
        return pd.DataFrame()
    
    def load_es_data(self, year_range: str, timeframe: str) -> pd.DataFrame:
        """Load ES data for a year range and timeframe."""
        filepath = os.path.join(self.base_path, f"ES {timeframe} ({year_range}).csv")
        if os.path.exists(filepath):
            return self.load_data(filepath)
        return pd.DataFrame()
    
    def filter_session(self, df: pd.DataFrame, session_name: str) -> pd.DataFrame:
        """
        Filter dataframe to specific trading session.
        
        Args:
            df: DataFrame with datetime index
            session_name: 'london' or 'ny'
            
        Returns:
            Filtered DataFrame
        """
        if session_name.lower() == 'london':
            start_time, end_time = self.london_session
        elif session_name.lower() == 'ny':
            start_time, end_time = self.ny_session
        else:
            raise ValueError("session_name must be 'london' or 'ny'")
        
        # Filter by time of day
        mask = (df.index.time >= start_time) & (df.index.time < end_time)
        return df[mask].copy()
    
    def find_swing_points(self, df: pd.DataFrame, order: int = 5) -> Tuple[pd.Series, pd.Series]:
        """
        Find swing highs and swing lows using local extrema.
        
        Args:
            df: DataFrame with OHLC data
            order: Number of candles on each side to compare (default: 5)
            
        Returns:
            Tuple of (swing_highs, swing_lows) as Series with datetime index
        """
        # Find local maxima (swing highs) using High prices
        high_indices = argrelextrema(df['High'].values, np.greater_equal, order=order)[0]
        swing_highs = pd.Series(df['High'].iloc[high_indices].values, 
                               index=df.index[high_indices])
        
        # Find local minima (swing lows) using Low prices
        low_indices = argrelextrema(df['Low'].values, np.less_equal, order=order)[0]
        swing_lows = pd.Series(df['Low'].iloc[low_indices].values,
                              index=df.index[low_indices])
        
        return swing_highs, swing_lows
    
    def align_swings(self, swings1: pd.Series, swings2: pd.Series, 
                    tolerance_minutes: int = 10) -> List[Tuple[datetime, float, float]]:
        """
        Align swing points between two assets within a time tolerance.
        
        Args:
            swings1: Swing points for asset 1
            swings2: Swing points for asset 2
            tolerance_minutes: Time tolerance in minutes (default: 10)
            
        Returns:
            List of tuples (timestamp, value1, value2) for aligned swings
        """
        aligned = []
        tolerance = pd.Timedelta(minutes=tolerance_minutes)
        
        for ts1, val1 in swings1.items():
            # Find closest swing in asset 2 within tolerance
            time_diffs = abs(swings2.index - ts1)
            if len(time_diffs) > 0:
                min_diff_idx = time_diffs.argmin()
                min_diff = time_diffs[min_diff_idx]
                
                if min_diff <= tolerance:
                    ts2 = swings2.index[min_diff_idx]
                    val2 = swings2.iloc[min_diff_idx]
                    aligned.append((ts1, val1, val2))
        
        return aligned
    
    def detect_divergence_type(self, prev_val: float, curr_val: float,
                              prev_val_other: float, curr_val_other: float,
                              is_high: bool) -> Dict:
        """
        Detect if there's an SMT divergence between two aligned swing points.
        
        Args:
            prev_val: Previous swing value for asset 1
            curr_val: Current swing value for asset 1
            prev_val_other: Previous swing value for asset 2
            curr_val_other: Current swing value for asset 2
            is_high: True if analyzing highs, False if analyzing lows
            
        Returns:
            Dict with divergence info or None if no divergence
        """
        if is_high:
            # Analyzing swing highs for bearish divergence
            asset1_direction = "HH" if curr_val > prev_val else "LH" if curr_val < prev_val else "EH"
            asset2_direction = "HH" if curr_val_other > prev_val_other else "LH" if curr_val_other < prev_val_other else "EH"
            
            # Bearish SMT: One makes HH, other makes LH
            if asset1_direction == "HH" and asset2_direction == "LH":
                return {
                    'type': 'bearish',
                    'leader': 'asset2',  # Asset 2 is weaker (refuses to go higher)
                    'asset1_dir': asset1_direction,
                    'asset2_dir': asset2_direction
                }
            elif asset1_direction == "LH" and asset2_direction == "HH":
                return {
                    'type': 'bearish',
                    'leader': 'asset1',  # Asset 1 is weaker (refuses to go higher)
                    'asset1_dir': asset1_direction,
                    'asset2_dir': asset2_direction
                }
        else:
            # Analyzing swing lows for bullish divergence
            asset1_direction = "LL" if curr_val < prev_val else "HL" if curr_val > prev_val else "EL"
            asset2_direction = "LL" if curr_val_other < prev_val_other else "HL" if curr_val_other > prev_val_other else "EL"
            
            # Bullish SMT: One makes LL, other makes HL
            if asset1_direction == "LL" and asset2_direction == "HL":
                return {
                    'type': 'bullish',
                    'leader': 'asset2',  # Asset 2 is stronger (refuses to go lower)
                    'asset1_dir': asset1_direction,
                    'asset2_dir': asset2_direction
                }
            elif asset1_direction == "HL" and asset2_direction == "LL":
                return {
                    'type': 'bullish',
                    'leader': 'asset1',  # Asset 1 is stronger (refuses to go lower)
                    'asset1_dir': asset1_direction,
                    'asset2_dir': asset2_direction
                }
        
        return None
    
    def detect_smt_divergences(self, nq_highs: pd.Series, nq_lows: pd.Series,
                              es_highs: pd.Series, es_lows: pd.Series) -> List[Dict]:
        """
        Detect SMT divergences between NQ and ES.
        
        Returns:
            List of divergence dictionaries
        """
        divergences = []
        
        # Align swing highs for bearish divergence detection
        aligned_highs = self.align_swings(nq_highs, es_highs)
        
        # Detect bearish divergences (comparing consecutive swing highs)
        for i in range(1, len(aligned_highs)):
            prev_ts, prev_nq, prev_es = aligned_highs[i-1]
            curr_ts, curr_nq, curr_es = aligned_highs[i]
            
            div = self.detect_divergence_type(prev_nq, curr_nq, prev_es, curr_es, is_high=True)
            
            if div:
                divergences.append({
                    'timestamp': curr_ts,
                    'prev_timestamp': prev_ts,
                    'type': div['type'],
                    'leader': 'NQ' if div['leader'] == 'asset1' else 'ES',
                    'nq_prev': prev_nq,
                    'nq_curr': curr_nq,
                    'es_prev': prev_es,
                    'es_curr': curr_es,
                    'nq_direction': div['asset1_dir'],
                    'es_direction': div['asset2_dir'],
                    'swing_type': 'high'
                })
        
        # Align swing lows for bullish divergence detection
        aligned_lows = self.align_swings(nq_lows, es_lows)
        
        # Detect bullish divergences (comparing consecutive swing lows)
        for i in range(1, len(aligned_lows)):
            prev_ts, prev_nq, prev_es = aligned_lows[i-1]
            curr_ts, curr_nq, curr_es = aligned_lows[i]
            
            div = self.detect_divergence_type(prev_nq, curr_nq, prev_es, curr_es, is_high=False)
            
            if div:
                divergences.append({
                    'timestamp': curr_ts,
                    'prev_timestamp': prev_ts,
                    'type': div['type'],
                    'leader': 'NQ' if div['leader'] == 'asset1' else 'ES',
                    'nq_prev': prev_nq,
                    'nq_curr': curr_nq,
                    'es_prev': prev_es,
                    'es_curr': curr_es,
                    'nq_direction': div['asset1_dir'],
                    'es_direction': div['asset2_dir'],
                    'swing_type': 'low'
                })
        
        return divergences
    
    def analyze_session(self, nq_df: pd.DataFrame, es_df: pd.DataFrame,
                       session_name: str) -> Tuple[List[Dict], pd.DataFrame, pd.DataFrame]:
        """
        Analyze a specific session for SMT divergences.
        
        Returns:
            Tuple of (divergences, filtered_nq, filtered_es)
        """
        # Filter to session times
        nq_session = self.filter_session(nq_df, session_name)
        es_session = self.filter_session(es_df, session_name)
        
        if len(nq_session) == 0 or len(es_session) == 0:
            return [], nq_session, es_session
        
        # Find swing points
        nq_highs, nq_lows = self.find_swing_points(nq_session)
        es_highs, es_lows = self.find_swing_points(es_session)
        
        # Detect divergences
        divergences = self.detect_smt_divergences(nq_highs, nq_lows, es_highs, es_lows)
        
        # Add session info
        for div in divergences:
            div['session'] = session_name
        
        return divergences, nq_session, es_session
    
    def generate_statistics(self, divergences: List[Dict]) -> pd.DataFrame:
        """
        Generate summary statistics from detected divergences.
        
        Returns:
            DataFrame with statistics
        """
        if not divergences:
            return pd.DataFrame()
        
        df = pd.DataFrame(divergences)
        
        # Statistics by session
        stats = []
        
        for session in ['london', 'ny']:
            session_divs = df[df['session'] == session]
            
            if len(session_divs) == 0:
                continue
            
            total = len(session_divs)
            bullish = len(session_divs[session_divs['type'] == 'bullish'])
            bearish = len(session_divs[session_divs['type'] == 'bearish'])
            
            # Count leadership
            nq_bullish_leader = len(session_divs[(session_divs['type'] == 'bullish') & 
                                                 (session_divs['leader'] == 'NQ')])
            es_bullish_leader = len(session_divs[(session_divs['type'] == 'bullish') & 
                                                 (session_divs['leader'] == 'ES')])
            nq_bearish_leader = len(session_divs[(session_divs['type'] == 'bearish') & 
                                                  (session_divs['leader'] == 'NQ')])
            es_bearish_leader = len(session_divs[(session_divs['type'] == 'bearish') & 
                                                  (session_divs['leader'] == 'ES')])
            
            stats.append({
                'Session': session.upper(),
                'Total Divergences': total,
                'Bullish SMT': bullish,
                'Bearish SMT': bearish,
                'NQ Bullish Leader': nq_bullish_leader,
                'ES Bullish Leader': es_bullish_leader,
                'NQ Bearish Leader': nq_bearish_leader,
                'ES Bearish Leader': es_bearish_leader
            })
        
        # Add totals
        if len(df) > 0:
            total = len(df)
            bullish = len(df[df['type'] == 'bullish'])
            bearish = len(df[df['type'] == 'bearish'])
            
            nq_bullish_leader = len(df[(df['type'] == 'bullish') & (df['leader'] == 'NQ')])
            es_bullish_leader = len(df[(df['type'] == 'bullish') & (df['leader'] == 'ES')])
            nq_bearish_leader = len(df[(df['type'] == 'bearish') & (df['leader'] == 'NQ')])
            es_bearish_leader = len(df[(df['type'] == 'bearish') & (df['leader'] == 'ES')])
            
            stats.append({
                'Session': 'TOTAL',
                'Total Divergences': total,
                'Bullish SMT': bullish,
                'Bearish SMT': bearish,
                'NQ Bullish Leader': nq_bullish_leader,
                'ES Bullish Leader': es_bullish_leader,
                'NQ Bearish Leader': nq_bearish_leader,
                'ES Bearish Leader': es_bearish_leader
            })
        
        return pd.DataFrame(stats)
    
    def plot_divergence_example(self, divergence: Dict, nq_df: pd.DataFrame, 
                               es_df: pd.DataFrame, output_path: str = None):
        """
        Plot an example of detected SMT divergence.
        
        Args:
            divergence: Divergence dictionary
            nq_df: NQ DataFrame for the session
            es_df: ES DataFrame for the session
            output_path: Path to save the plot (optional)
        """
        # Get time window around divergence (2 hours before to 1 hour after)
        start_time = divergence['prev_timestamp'] - pd.Timedelta(hours=1)
        end_time = divergence['timestamp'] + pd.Timedelta(minutes=30)
        
        nq_plot = nq_df[(nq_df.index >= start_time) & (nq_df.index <= end_time)]
        es_plot = es_df[(es_df.index >= start_time) & (es_df.index <= end_time)]
        
        if len(nq_plot) == 0 or len(es_plot) == 0:
            return
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True)
        
        # Plot NQ
        ax1.plot(nq_plot.index, nq_plot['Close'], label='NQ Close', color='blue', linewidth=1.5)
        ax1.scatter([divergence['prev_timestamp'], divergence['timestamp']],
                   [divergence['nq_prev'], divergence['nq_curr']], 
                   color='red', s=100, zorder=5, label='Swing Points')
        ax1.plot([divergence['prev_timestamp'], divergence['timestamp']],
                [divergence['nq_prev'], divergence['nq_curr']], 
                color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax1.set_ylabel('NQ Price', fontsize=12, fontweight='bold')
        ax1.set_title(f"NQ: {divergence['nq_direction']}", fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot ES
        ax2.plot(es_plot.index, es_plot['Close'], label='ES Close', color='green', linewidth=1.5)
        ax2.scatter([divergence['prev_timestamp'], divergence['timestamp']],
                   [divergence['es_prev'], divergence['es_curr']], 
                   color='red', s=100, zorder=5, label='Swing Points')
        ax2.plot([divergence['prev_timestamp'], divergence['timestamp']],
                [divergence['es_prev'], divergence['es_curr']], 
                color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax2.set_ylabel('ES Price', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax2.set_title(f"ES: {divergence['es_direction']}", fontsize=11)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Main title
        div_type = divergence['type'].upper()
        leader = divergence['leader']
        session = divergence['session'].upper()
        fig.suptitle(f"{div_type} SMT Divergence - {leader} Leader - {session} Session\n"
                    f"Detected at {divergence['timestamp'].strftime('%Y-%m-%d %H:%M')}",
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"Plot saved to: {output_path}")
        
        plt.close()
    
    def run_analysis(self, years: List[int] = [2024], timeframe: str = '5m',
                    output_dir: str = 'smt_analysis_results'):
        """
        Run complete SMT divergence analysis.
        
        Args:
            years: List of years to analyze
            timeframe: '5m' or '15m'
            output_dir: Directory to save results
        """
        print("="*80)
        print("SMT DIVERGENCE DETECTOR")
        print("="*80)
        print(f"Analyzing {timeframe} timeframe for years: {years}")
        print(f"Sessions: London (02:00-05:00), New York AM (08:30-11:00)")
        print("="*80)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        all_divergences = []
        
        for year in years:
            print(f"\n### Processing {year} ###")
            
            # Load NQ data
            nq_df = self.load_nq_data(year, timeframe)
            if len(nq_df) == 0:
                print(f"  ⚠ No NQ data found for {year}")
                continue
            
            # Load ES data - try different year ranges based on known file structure
            es_df = pd.DataFrame()
            
            # Determine which ES file to use based on year and timeframe
            if timeframe == '5m':
                if year <= 2020:
                    year_ranges = ["2018-2020"]
                elif year <= 2023:
                    year_ranges = ["2021-2023"]
                else:
                    year_ranges = ["2024-2025"]
            else:
                # For other timeframes, try consolidated file first
                year_ranges = ["2018-2025"]
            
            # Try the identified ranges
            for year_range in year_ranges:
                es_df = self.load_es_data(year_range, timeframe)
                if len(es_df) > 0:
                    break
            
            # If still no ES data, try other common patterns
            if len(es_df) == 0:
                for year_range in [f"{year}-{year+1}", f"{year-1}-{year+1}", "2018-2025"]:
                    es_df = self.load_es_data(year_range, timeframe)
                    if len(es_df) > 0:
                        break
            
            if len(es_df) == 0:
                print(f"  ⚠ No ES data found for {year}")
                continue
            
            # Filter ES data to match year
            es_df = es_df[es_df.index.year == year]
            
            print(f"  ✓ Loaded {len(nq_df)} NQ candles, {len(es_df)} ES candles")
            
            # Analyze London session
            print("  → Analyzing London session...")
            london_divs, nq_london, es_london = self.analyze_session(nq_df, es_df, 'london')
            print(f"    Found {len(london_divs)} divergences")
            
            # Analyze NY session
            print("  → Analyzing NY session...")
            ny_divs, nq_ny, es_ny = self.analyze_session(nq_df, es_df, 'ny')
            print(f"    Found {len(ny_divs)} divergences")
            
            all_divergences.extend(london_divs)
            all_divergences.extend(ny_divs)
            
            # Plot examples (first divergence of each type per session)
            plotted_types = set()
            for div in london_divs + ny_divs:
                plot_key = (div['session'], div['type'])
                if plot_key not in plotted_types and len(plotted_types) < 4:
                    session_df_nq = nq_london if div['session'] == 'london' else nq_ny
                    session_df_es = es_london if div['session'] == 'london' else es_ny
                    
                    filename = f"smt_example_{year}_{div['session']}_{div['type']}.png"
                    output_path = os.path.join(output_dir, filename)
                    
                    self.plot_divergence_example(div, session_df_nq, session_df_es, output_path)
                    plotted_types.add(plot_key)
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        
        # Generate statistics
        if all_divergences:
            stats_df = self.generate_statistics(all_divergences)
            print("\n### STATISTICS ###")
            print(stats_df.to_string(index=False))
            
            # Save statistics
            stats_path = os.path.join(output_dir, 'smt_statistics.csv')
            stats_df.to_csv(stats_path, index=False)
            print(f"\n✓ Statistics saved to: {stats_path}")
            
            # Save detailed divergences
            divs_df = pd.DataFrame(all_divergences)
            divs_path = os.path.join(output_dir, 'smt_divergences_detailed.csv')
            divs_df.to_csv(divs_path, index=False)
            print(f"✓ Detailed divergences saved to: {divs_path}")
            
            # Leadership analysis
            print("\n### LEADERSHIP ANALYSIS ###")
            bullish_divs = divs_df[divs_df['type'] == 'bullish']
            bearish_divs = divs_df[divs_df['type'] == 'bearish']
            
            if len(bullish_divs) > 0:
                nq_bull_pct = (len(bullish_divs[bullish_divs['leader'] == 'NQ']) / len(bullish_divs)) * 100
                print(f"Bullish Leader: NQ {nq_bull_pct:.1f}% | ES {100-nq_bull_pct:.1f}%")
                
            if len(bearish_divs) > 0:
                nq_bear_pct = (len(bearish_divs[bearish_divs['leader'] == 'NQ']) / len(bearish_divs)) * 100
                print(f"Bearish Leader: NQ {nq_bear_pct:.1f}% | ES {100-nq_bear_pct:.1f}%")
        else:
            print("\n⚠ No divergences detected")
        
        print("\n" + "="*80)
        print(f"Results saved to: {output_dir}/")
        print("="*80)


def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Detect SMT divergences between NQ and ES futures',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze 2024 data with 5-minute timeframe
  python smt_divergence_detector.py --years 2024 --timeframe 5m
  
  # Analyze multiple years with 15-minute timeframe
  python smt_divergence_detector.py --years 2023 2024 --timeframe 15m
  
  # Specify custom data directory
  python smt_divergence_detector.py --years 2024 --path /path/to/data
        """
    )
    
    parser.add_argument(
        '--years',
        type=int,
        nargs='+',
        default=[2024],
        help='Years to analyze (default: 2024)'
    )
    
    parser.add_argument(
        '--timeframe',
        type=str,
        choices=['5m', '15m'],
        default='5m',
        help='Timeframe to analyze (default: 5m)'
    )
    
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Base path to CSV files (default: current directory)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='smt_analysis_results',
        help='Output directory for results (default: smt_analysis_results)'
    )
    
    args = parser.parse_args()
    
    # Run analysis
    detector = SMTDivergenceDetector(base_path=args.path)
    detector.run_analysis(
        years=args.years,
        timeframe=args.timeframe,
        output_dir=args.output
    )


if __name__ == '__main__':
    main()
