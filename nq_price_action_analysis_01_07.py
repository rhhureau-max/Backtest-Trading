"""
NQ Futures Session Analysis (01:00-07:00)
==========================================
This script analyzes NQ futures price action during the 01:00-07:00 session window
across multiple years (2018-2025) using 5-minute data.

Analyses included:
1. Distribution of returns (directionality)
2. Volatility and range analysis
3. Timing analysis of session extremes
4. Day-of-week effects
5. Open drive correlation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, time
import warnings

warnings.filterwarnings('ignore')


class NQSessionAnalyzer:
    """Analyzer for NQ futures session data during 01:00-07:00 window"""
    
    def __init__(self, data_directory):
        """
        Initialize the analyzer with the data directory.
        
        Args:
            data_directory (str): Path to directory containing CSV files
        """
        self.data_directory = Path(data_directory)
        self.session_start = time(1, 0, 0)  # 01:00:00
        self.session_end = time(7, 0, 0)     # 07:00:00
        self.all_data = None
        self.session_data = None
        
    def load_data(self):
        """Load all 5-minute data files from 2018-2025"""
        print("Loading NQ 5-minute data files...")
        
        all_dataframes = []
        years = range(2018, 2026)  # 2018-2025
        
        for year in years:
            file_path = self.data_directory / f"{year} 5m.csv"
            
            if not file_path.exists():
                print(f"  Warning: {file_path.name} not found, skipping...")
                continue
            
            try:
                # Load CSV with semicolon separator
                df = pd.read_csv(
                    file_path,
                    sep=';',
                    names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                    skiprows=1  # Skip header row
                )
                
                # Convert date and time
                df['DateTime'] = pd.to_datetime(
                    df['Date'] + ' ' + df['Time'],
                    format='%d/%m/%Y %H:%M:%S'
                )
                
                # Extract time component
                df['TimeOnly'] = df['DateTime'].dt.time
                
                # Add year column for tracking
                df['Year'] = year
                
                all_dataframes.append(df)
                print(f"  Loaded {year} 5m.csv: {len(df)} rows")
                
            except Exception as e:
                print(f"  Error loading {file_path.name}: {e}")
                continue
        
        if not all_dataframes:
            raise ValueError("No data files could be loaded!")
        
        # Combine all data
        self.all_data = pd.concat(all_dataframes, ignore_index=True)
        self.all_data = self.all_data.sort_values('DateTime').reset_index(drop=True)
        
        print(f"\nTotal data loaded: {len(self.all_data)} rows")
        print(f"Date range: {self.all_data['DateTime'].min()} to {self.all_data['DateTime'].max()}")
        
    def filter_session_window(self):
        """Filter data to 01:00-07:00 time window"""
        print("\nFiltering to 01:00-07:00 session window...")
        
        # Filter by time window (01:00:00 <= time <= 07:00:00)
        mask = (self.all_data['TimeOnly'] >= self.session_start) & \
               (self.all_data['TimeOnly'] <= self.session_end)
        
        self.session_data = self.all_data[mask].copy()
        
        print(f"Filtered data: {len(self.session_data)} rows")
        
    def create_daily_sessions(self):
        """Aggregate 5-minute data into daily sessions"""
        print("\nCreating daily session aggregates...")
        
        # Extract date only
        self.session_data['Date'] = self.session_data['DateTime'].dt.date
        
        # Get the first candle (01:00) for each date
        first_candles = self.session_data.groupby('Date').first().reset_index()
        
        # Aggregate session data
        sessions = []
        
        for date in self.session_data['Date'].unique():
            day_data = self.session_data[self.session_data['Date'] == date]
            
            if len(day_data) == 0:
                continue
            
            # Session metrics
            session_open = day_data.iloc[0]['Open']
            session_close = day_data.iloc[-1]['Close']
            session_high = day_data['High'].max()
            session_low = day_data['Low'].min()
            
            # Find when high and low occurred
            high_idx = day_data['High'].idxmax()
            low_idx = day_data['Low'].idxmin()
            high_time = day_data.loc[high_idx, 'TimeOnly']
            low_time = day_data.loc[low_idx, 'TimeOnly']
            
            # First candle (01:00) direction
            first_candle_bullish = day_data.iloc[0]['Close'] > day_data.iloc[0]['Open']
            
            # Day of week
            day_of_week = pd.to_datetime(date).day_name()
            year = pd.to_datetime(date).year
            
            sessions.append({
                'Date': date,
                'Year': year,
                'DayOfWeek': day_of_week,
                'Open': session_open,
                'High': session_high,
                'Low': session_low,
                'Close': session_close,
                'Range': session_high - session_low,
                'Return': session_close - session_open,
                'IsBullish': session_close > session_open,
                'HighTime': high_time,
                'LowTime': low_time,
                'FirstCandleBullish': first_candle_bullish
            })
        
        self.daily_sessions = pd.DataFrame(sessions)
        print(f"Created {len(self.daily_sessions)} daily sessions")
        
    def analyze_directionality(self):
        """Analysis 1: Distribution of returns"""
        print("\n" + "="*70)
        print("ANALYSIS 1: DISTRIBUTION OF RETURNS (DIRECTIONNALITÉ)")
        print("="*70)
        
        total_sessions = len(self.daily_sessions)
        bullish_sessions = self.daily_sessions['IsBullish'].sum()
        bearish_sessions = total_sessions - bullish_sessions
        
        bullish_pct = (bullish_sessions / total_sessions) * 100
        bearish_pct = (bearish_sessions / total_sessions) * 100
        
        avg_return = self.daily_sessions['Return'].mean()
        avg_bullish_return = self.daily_sessions[self.daily_sessions['IsBullish']]['Return'].mean()
        avg_bearish_return = self.daily_sessions[~self.daily_sessions['IsBullish']]['Return'].mean()
        
        print(f"\nTotal sessions analyzed: {total_sessions}")
        print(f"\nBullish sessions (Close > Open): {bullish_sessions} ({bullish_pct:.2f}%)")
        print(f"Bearish sessions (Close < Open): {bearish_sessions} ({bearish_pct:.2f}%)")
        print(f"\nAverage session return: {avg_return:.2f} points")
        print(f"Average bullish session return: {avg_bullish_return:.2f} points")
        print(f"Average bearish session return: {avg_bearish_return:.2f} points")
        
        return {
            'total': total_sessions,
            'bullish': bullish_sessions,
            'bearish': bearish_sessions,
            'bullish_pct': bullish_pct,
            'avg_return': avg_return
        }
    
    def analyze_volatility(self):
        """Analysis 2: Volatility and range"""
        print("\n" + "="*70)
        print("ANALYSIS 2: VOLATILITY AND RANGE")
        print("="*70)
        
        avg_range = self.daily_sessions['Range'].mean()
        median_range = self.daily_sessions['Range'].median()
        std_range = self.daily_sessions['Range'].std()
        
        print(f"\nOverall statistics:")
        print(f"Average session range: {avg_range:.2f} points")
        print(f"Median session range: {median_range:.2f} points")
        print(f"Standard deviation: {std_range:.2f} points")
        
        # Yearly breakdown
        print(f"\nYearly breakdown:")
        yearly_stats = self.daily_sessions.groupby('Year').agg({
            'Range': ['mean', 'median', 'std', 'count']
        }).round(2)
        
        print(yearly_stats)
        
        return yearly_stats
    
    def analyze_timing_extremes(self):
        """Analysis 3: Timing analysis of session extremes"""
        print("\n" + "="*70)
        print("ANALYSIS 3: TIMING OF SESSION EXTREMES")
        print("="*70)
        
        # Convert times to minutes since 01:00
        def time_to_minutes(t):
            return t.hour * 60 + t.minute - 60  # Subtract 60 to start at 0 (01:00)
        
        self.daily_sessions['HighMinutes'] = self.daily_sessions['HighTime'].apply(time_to_minutes)
        self.daily_sessions['LowMinutes'] = self.daily_sessions['LowTime'].apply(time_to_minutes)
        
        # Create 15-minute bins (0-360 minutes = 6 hours)
        bins = list(range(0, 361, 15))
        labels = [f"{1 + i//60:02d}:{i%60:02d}" for i in bins[:-1]]
        
        high_dist = pd.cut(self.daily_sessions['HighMinutes'], bins=bins, labels=labels)
        low_dist = pd.cut(self.daily_sessions['LowMinutes'], bins=bins, labels=labels)
        
        high_counts = high_dist.value_counts().sort_index()
        low_counts = low_dist.value_counts().sort_index()
        
        print("\nHIGH occurrence distribution (by 15-min intervals):")
        print(high_counts)
        
        print("\nLOW occurrence distribution (by 15-min intervals):")
        print(low_counts)
        
        # Check extremes at open vs close
        highs_at_open = (self.daily_sessions['HighMinutes'] <= 15).sum()
        highs_at_close = (self.daily_sessions['HighMinutes'] >= 345).sum()
        lows_at_open = (self.daily_sessions['LowMinutes'] <= 15).sum()
        lows_at_close = (self.daily_sessions['LowMinutes'] >= 345).sum()
        
        total = len(self.daily_sessions)
        
        print(f"\nExtreme timing summary:")
        print(f"Highs in first 15 min (01:00-01:15): {highs_at_open} ({highs_at_open/total*100:.2f}%)")
        print(f"Highs in last 15 min (06:45-07:00): {highs_at_close} ({highs_at_close/total*100:.2f}%)")
        print(f"Lows in first 15 min (01:00-01:15): {lows_at_open} ({lows_at_open/total*100:.2f}%)")
        print(f"Lows in last 15 min (06:45-07:00): {lows_at_close} ({lows_at_close/total*100:.2f}%)")
        
        return high_counts, low_counts
    
    def analyze_day_of_week(self):
        """Analysis 4: Day-of-week effects"""
        print("\n" + "="*70)
        print("ANALYSIS 4: DAY-OF-WEEK EFFECTS")
        print("="*70)
        
        # Order days correctly
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        dow_stats = self.daily_sessions.groupby('DayOfWeek').agg({
            'Range': ['mean', 'median'],
            'Return': 'mean',
            'IsBullish': ['sum', 'count']
        }).round(2)
        
        # Calculate bullish percentage
        dow_stats['Bullish%'] = (
            dow_stats[('IsBullish', 'sum')] / dow_stats[('IsBullish', 'count')] * 100
        ).round(2)
        
        # Reindex by day order
        existing_days = [d for d in day_order if d in dow_stats.index]
        dow_stats = dow_stats.reindex(existing_days)
        
        print("\nDay-of-week comparative analysis:")
        print(dow_stats)
        
        return dow_stats
    
    def analyze_open_drive(self):
        """Analysis 5: Open drive correlation"""
        print("\n" + "="*70)
        print("ANALYSIS 5: OPEN DRIVE CORRELATION")
        print("="*70)
        
        # Filter sessions where first candle (01:00) is bullish
        first_bullish = self.daily_sessions[self.daily_sessions['FirstCandleBullish']]
        first_bearish = self.daily_sessions[~self.daily_sessions['FirstCandleBullish']]
        
        # Calculate probabilities
        total_first_bullish = len(first_bullish)
        total_first_bearish = len(first_bearish)
        
        session_bullish_given_first_bullish = first_bullish['IsBullish'].sum()
        session_bullish_given_first_bearish = first_bearish['IsBullish'].sum()
        
        prob_bullish_given_first_bullish = (
            session_bullish_given_first_bullish / total_first_bullish * 100
        ) if total_first_bullish > 0 else 0
        
        prob_bullish_given_first_bearish = (
            session_bullish_given_first_bearish / total_first_bearish * 100
        ) if total_first_bearish > 0 else 0
        
        print(f"\nFirst candle (01:00) BULLISH:")
        print(f"  Total sessions: {total_first_bullish}")
        print(f"  Sessions closing bullish: {session_bullish_given_first_bullish}")
        print(f"  Probability: {prob_bullish_given_first_bullish:.2f}%")
        
        print(f"\nFirst candle (01:00) BEARISH:")
        print(f"  Total sessions: {total_first_bearish}")
        print(f"  Sessions closing bullish: {session_bullish_given_first_bearish}")
        print(f"  Probability: {prob_bullish_given_first_bearish:.2f}%")
        
        print(f"\nConclusion:")
        if prob_bullish_given_first_bullish > 55:
            print(f"  Strong positive correlation: First bullish candle increases probability")
            print(f"  of bullish session close by {prob_bullish_given_first_bullish - 50:.2f}%")
        elif prob_bullish_given_first_bullish < 45:
            print(f"  Reversal tendency: First bullish candle often reverses")
        else:
            print(f"  Weak correlation: First candle direction has limited predictive power")
        
        return {
            'first_bullish_count': total_first_bullish,
            'prob_bullish_given_first_bullish': prob_bullish_given_first_bullish,
            'first_bearish_count': total_first_bearish,
            'prob_bullish_given_first_bearish': prob_bullish_given_first_bearish
        }
    
    def create_visualizations(self, high_counts, low_counts):
        """Create matplotlib charts for the analysis"""
        print("\n" + "="*70)
        print("GENERATING VISUALIZATIONS")
        print("="*70)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Chart 1: Session Range Distribution
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        
        self.daily_sessions['Range'].hist(bins=50, ax=ax1, color='steelblue', edgecolor='black', alpha=0.7)
        ax1.axvline(self.daily_sessions['Range'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
        ax1.axvline(self.daily_sessions['Range'].median(), color='green', linestyle='--', linewidth=2, label='Median')
        
        ax1.set_xlabel('Session Range (points)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title('NQ Session Range Distribution (01:00-07:00)\n2018-2025', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        chart1_path = self.data_directory / 'nq_session_range_distribution.png'
        plt.tight_layout()
        plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
        print(f"  Saved: {chart1_path.name}")
        plt.close()
        
        # Chart 2: Timing Histogram for Highs and Lows
        fig2, (ax2a, ax2b) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Highs timing
        x_pos = np.arange(len(high_counts))
        ax2a.bar(x_pos, high_counts.values, color='green', alpha=0.7, edgecolor='black')
        ax2a.set_xticks(x_pos[::2])  # Show every other label to avoid crowding
        ax2a.set_xticklabels(high_counts.index[::2], rotation=45, ha='right')
        ax2a.set_ylabel('Frequency', fontsize=12)
        ax2a.set_title('Session HIGH Timing Distribution (15-min intervals)', fontsize=13, fontweight='bold')
        ax2a.grid(True, alpha=0.3, axis='y')
        
        # Lows timing
        x_pos = np.arange(len(low_counts))
        ax2b.bar(x_pos, low_counts.values, color='red', alpha=0.7, edgecolor='black')
        ax2b.set_xticks(x_pos[::2])
        ax2b.set_xticklabels(low_counts.index[::2], rotation=45, ha='right')
        ax2b.set_xlabel('Time', fontsize=12)
        ax2b.set_ylabel('Frequency', fontsize=12)
        ax2b.set_title('Session LOW Timing Distribution (15-min intervals)', fontsize=13, fontweight='bold')
        ax2b.grid(True, alpha=0.3, axis='y')
        
        fig2.suptitle('NQ Session Extremes Timing Analysis (01:00-07:00)\n2018-2025', 
                      fontsize=15, fontweight='bold', y=0.995)
        
        chart2_path = self.data_directory / 'nq_session_timing_histogram.png'
        plt.tight_layout()
        plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
        print(f"  Saved: {chart2_path.name}")
        plt.close()
        
        print("\nVisualization complete!")
    
    def generate_synthesis(self):
        """Generate synthesis conclusion on recurring biases"""
        print("\n" + "="*70)
        print("SYNTHESIS: RECURRING BIASES IN 01:00-07:00 SESSION")
        print("="*70)
        
        # Calculate key metrics
        bullish_pct = (self.daily_sessions['IsBullish'].sum() / len(self.daily_sessions)) * 100
        avg_range = self.daily_sessions['Range'].mean()
        
        # Open drive correlation
        first_bullish = self.daily_sessions[self.daily_sessions['FirstCandleBullish']]
        prob_continue = (first_bullish['IsBullish'].sum() / len(first_bullish) * 100) if len(first_bullish) > 0 else 50
        
        # Extreme timing
        highs_early = (self.daily_sessions['HighMinutes'] <= 60).sum()  # First hour
        highs_late = (self.daily_sessions['HighMinutes'] >= 300).sum()   # Last hour
        lows_early = (self.daily_sessions['LowMinutes'] <= 60).sum()
        lows_late = (self.daily_sessions['LowMinutes'] >= 300).sum()
        
        total = len(self.daily_sessions)
        
        print("\n📊 KEY FINDINGS:")
        print(f"\n1. DIRECTIONAL BIAS:")
        if abs(bullish_pct - 50) > 5:
            bias = "BULLISH" if bullish_pct > 50 else "BEARISH"
            print(f"   ✓ {bias} bias detected ({bullish_pct:.1f}% vs {100-bullish_pct:.1f}%)")
        else:
            print(f"   ✓ Neutral session (balanced at ~50%)")
        
        print(f"\n2. VOLATILITY:")
        print(f"   ✓ Average session range: {avg_range:.2f} points")
        print(f"   ✓ Typical move represents significant intraday opportunity")
        
        print(f"\n3. TIMING PATTERNS:")
        print(f"   Highs in first hour: {highs_early/total*100:.1f}%")
        print(f"   Highs in last hour: {highs_late/total*100:.1f}%")
        print(f"   Lows in first hour: {lows_early/total*100:.1f}%")
        print(f"   Lows in last hour: {lows_late/total*100:.1f}%")
        
        if highs_early > highs_late * 1.3:
            print(f"   ✓ BIAS: Session highs tend to form early")
        elif highs_late > highs_early * 1.3:
            print(f"   ✓ BIAS: Session highs tend to form late")
        else:
            print(f"   ✓ No strong timing bias for highs")
        
        if lows_early > lows_late * 1.3:
            print(f"   ✓ BIAS: Session lows tend to form early")
        elif lows_late > lows_early * 1.3:
            print(f"   ✓ BIAS: Session lows tend to form late")
        else:
            print(f"   ✓ No strong timing bias for lows")
        
        print(f"\n4. OPEN DRIVE CORRELATION:")
        if prob_continue > 55:
            print(f"   ✓ STRONG CORRELATION: First candle direction predicts session ({prob_continue:.1f}%)")
        elif prob_continue < 45:
            print(f"   ✓ REVERSAL PATTERN: First candle often reverses ({100-prob_continue:.1f}% opposite)")
        else:
            print(f"   ✓ WEAK CORRELATION: First candle has limited predictive power")
        
        print(f"\n5. TRADING IMPLICATIONS:")
        print(f"   • Monitor first 15-60 minutes for extreme formation tendencies")
        print(f"   • Consider {avg_range:.0f}-point average range for position sizing")
        print(f"   • Day-of-week analysis may reveal additional edge opportunities")
        print(f"   • First candle correlation: {'Consider continuation' if prob_continue > 55 else 'Watch for reversals' if prob_continue < 45 else 'Remain neutral'}")
        
        print("\n" + "="*70)
    
    def run_complete_analysis(self):
        """Run all analyses and generate complete report"""
        print("\n" + "="*70)
        print("NQ FUTURES SESSION ANALYSIS (01:00-07:00)")
        print("="*70)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load and prepare data
        self.load_data()
        self.filter_session_window()
        self.create_daily_sessions()
        
        # Run analyses
        self.analyze_directionality()
        self.analyze_volatility()
        high_counts, low_counts = self.analyze_timing_extremes()
        self.analyze_day_of_week()
        self.analyze_open_drive()
        
        # Generate visualizations
        self.create_visualizations(high_counts, low_counts)
        
        # Generate synthesis
        self.generate_synthesis()
        
        print("\n✅ Analysis complete!")


def main():
    """Main execution function"""
    # Set the data directory (current directory where CSV files are located)
    data_dir = Path(__file__).parent
    
    # Create analyzer and run
    analyzer = NQSessionAnalyzer(data_dir)
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()
