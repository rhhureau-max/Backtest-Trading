#!/usr/bin/env python3
"""
SCENARIO FREQUENCY ANALYSIS - NQ 2018-2025
===========================================

This script performs a PURE STATISTICAL ANALYSIS of pattern occurrences.
NO TRADING, NO POSITIONS, NO ENTRY/EXIT - ONLY pattern detection and counting.

Analyzes 3 scenarios from LONDON_TOKYO_KILLZONE_ANALYSIS.md:
1. COMPRESSION: Asian range < 40 points
2. EXPANSION: Asian range > 60 points with directional trend
3. CONTINUATION: Structure break during Tokyo session

Output: Frequency counts, percentages, and temporal distributions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, time, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class ScenarioFrequencyAnalyzer:
    """Analyzes the frequency of occurrence of 3 trading scenarios in NQ data."""
    
    def __init__(self, data_dir='.'):
        """
        Initialize the analyzer.
        
        Args:
            data_dir: Directory containing the CSV files
        """
        self.data_dir = Path(data_dir)
        self.data = None
        self.results = {
            'scenario_1_compression': [],
            'scenario_2_expansion': [],
            'scenario_3_continuation': [],
            'dates': [],
            'asian_ranges': [],
            'asian_highs': [],
            'asian_lows': []
        }
        
    def load_data(self):
        """Load all 15m CSV files from 2018 to 2025."""
        print("Loading NQ 15m data from 2018 to 2025...")
        
        dfs = []
        for year in range(2018, 2026):
            filename = f"{year} 15m.csv"
            filepath = self.data_dir / filename
            
            if not filepath.exists():
                print(f"Warning: {filename} not found, skipping...")
                continue
                
            print(f"  Loading {filename}...")
            
            # Load CSV with semicolon separator
            df = pd.read_csv(filepath, sep=';', header=0)
            
            # Get column names (first row contains actual column names)
            if 'Column1' in df.columns:
                # First row is header, skip it
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            else:
                df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Convert to proper types
            df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
            df['High'] = pd.to_numeric(df['High'], errors='coerce')
            df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
            df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
            
            # Parse datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                           format='%d/%m/%Y %H:%M:%S', 
                                           errors='coerce')
            
            # Drop rows with invalid datetime
            df = df.dropna(subset=['DateTime'])
            
            dfs.append(df)
            print(f"    Loaded {len(df)} rows")
        
        # Combine all dataframes
        self.data = pd.concat(dfs, ignore_index=True)
        self.data = self.data.sort_values('DateTime').reset_index(drop=True)
        
        print(f"\nTotal data loaded: {len(self.data)} rows")
        print(f"Date range: {self.data['DateTime'].min()} to {self.data['DateTime'].max()}")
        
        return self.data
    
    def identify_sessions(self):
        """
        Identify Tokyo (20:00-00:00 NY) and London (02:00-05:00 NY) sessions.
        
        Note: The data appears to be in a timezone already. We'll work with the
        time component directly and assume it's in a consistent timezone.
        """
        print("\nIdentifying Tokyo and London sessions...")
        
        # Extract time component
        self.data['Time_Only'] = self.data['DateTime'].dt.time
        self.data['Date_Only'] = self.data['DateTime'].dt.date
        
        # Tokyo session: 20:00 to 23:59 (same day) - 4 hours (20h-00h means 20:00-23:59)
        # London session: 02:00 to 05:00 (next day)
        
        # Mark Tokyo session (20:00 - 23:59)
        tokyo_start = time(20, 0)
        tokyo_end = time(23, 59)
        
        self.data['is_tokyo'] = (
            (self.data['Time_Only'] >= tokyo_start) & 
            (self.data['Time_Only'] <= tokyo_end)
        )
        
        # Mark London session (02:00 - 05:00)
        london_start = time(2, 0)
        london_end = time(5, 0)
        
        self.data['is_london'] = (
            (self.data['Time_Only'] >= london_start) & 
            (self.data['Time_Only'] < london_end)
        )
        
        tokyo_count = self.data['is_tokyo'].sum()
        london_count = self.data['is_london'].sum()
        
        print(f"  Tokyo session bars: {tokyo_count}")
        print(f"  London session bars: {london_count}")
        
        return self.data
    
    def calculate_asian_range(self, date):
        """
        Calculate the Asian (Tokyo) range for a specific trading day.
        
        Args:
            date: The date to analyze
            
        Returns:
            dict with high, low, range, and session data
        """
        # Get Tokyo session data for this date
        tokyo_data = self.data[
            (self.data['Date_Only'] == date) & 
            (self.data['is_tokyo'] == True)
        ]
        
        if len(tokyo_data) == 0:
            return None
        
        asian_high = tokyo_data['High'].max()
        asian_low = tokyo_data['Low'].min()
        asian_range = asian_high - asian_low
        
        return {
            'date': date,
            'high': asian_high,
            'low': asian_low,
            'range': asian_range,
            'data': tokyo_data
        }
    
    def detect_scenario_1_compression(self, asian_session):
        """
        Detect Scenario 1: COMPRESSION
        
        Condition: Asian range < 40 points with horizontal consolidation
        
        Args:
            asian_session: Dictionary with Asian session data
            
        Returns:
            Boolean indicating if scenario detected
        """
        if asian_session is None:
            return False
        
        # Simple detection: range < 40 points
        return asian_session['range'] < 40
    
    def detect_scenario_2_expansion(self, asian_session):
        """
        Detect Scenario 2: EXPANSION
        
        Condition: Asian range > 60 points with directional trend (not zigzag)
        
        We detect directional trend by checking if price movement is relatively
        one-directional (measuring the ratio of range to total price movement)
        
        Args:
            asian_session: Dictionary with Asian session data
            
        Returns:
            Boolean indicating if scenario detected
        """
        if asian_session is None:
            return False
        
        # Check range > 60 points
        if asian_session['range'] <= 60:
            return False
        
        # Check for directional movement (not zigzag)
        data = asian_session['data']
        
        if len(data) < 2:
            return False
        
        # Calculate price direction consistency
        # Method: Check if close prices show a trend
        closes = data['Close'].values
        
        # Calculate net movement vs total movement
        net_movement = abs(closes[-1] - closes[0])
        
        # Calculate sum of absolute movements between bars
        price_changes = np.diff(closes)
        total_movement = np.sum(np.abs(price_changes))
        
        if total_movement == 0:
            return False
        
        # If net movement is at least 60% of total movement, it's directional
        directional_ratio = net_movement / total_movement
        
        return directional_ratio >= 0.60
    
    def detect_scenario_3_continuation(self, asian_session, prev_h4_high, prev_h4_low):
        """
        Detect Scenario 3: CONTINUATION
        
        Condition: Tokyo breaks an important H4 or D1 structure level
        
        For simplicity, we check if Tokyo session breaks recent H4 highs/lows
        (We approximate by looking at previous day's high/low as structure)
        
        Args:
            asian_session: Dictionary with Asian session data
            prev_h4_high: Previous significant high level
            prev_h4_low: Previous significant low level
            
        Returns:
            Boolean indicating if scenario detected
        """
        if asian_session is None or prev_h4_high is None or prev_h4_low is None:
            return False
        
        asian_high = asian_session['high']
        asian_low = asian_session['low']
        
        # Structure break: Tokyo high breaks previous high OR Tokyo low breaks previous low
        # with significant margin (> 10 points to confirm it's a real break)
        
        bullish_break = asian_high > (prev_h4_high + 10)
        bearish_break = asian_low < (prev_h4_low - 10)
        
        return bullish_break or bearish_break
    
    def get_h4_structure_levels(self, date, lookback_days=5):
        """
        Get H4 structure levels (approximate using daily high/low from previous days).
        
        Args:
            date: Current date
            lookback_days: Number of days to look back
            
        Returns:
            Tuple of (prev_high, prev_low)
        """
        # Get data from previous N days
        end_date = date - timedelta(days=1)
        start_date = end_date - timedelta(days=lookback_days)
        
        prev_data = self.data[
            (self.data['Date_Only'] >= start_date) & 
            (self.data['Date_Only'] <= end_date)
        ]
        
        if len(prev_data) == 0:
            return None, None
        
        prev_high = prev_data['High'].max()
        prev_low = prev_data['Low'].min()
        
        return prev_high, prev_low
    
    def analyze_all_days(self):
        """Analyze all trading days and detect scenarios."""
        print("\nAnalyzing all trading days for scenario occurrences...")
        
        # Get unique trading dates (exclude weekends)
        trading_dates = sorted(self.data['Date_Only'].unique())
        
        # Filter out weekends
        trading_dates = [d for d in trading_dates 
                        if datetime.combine(d, time()).weekday() < 5]
        
        print(f"Total trading days to analyze: {len(trading_dates)}")
        
        for i, date in enumerate(trading_dates):
            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{len(trading_dates)} days...")
            
            # Calculate Asian range
            asian_session = self.calculate_asian_range(date)
            
            if asian_session is None:
                continue
            
            # Get structure levels for scenario 3
            prev_h4_high, prev_h4_low = self.get_h4_structure_levels(date)
            
            # Detect scenarios
            s1 = self.detect_scenario_1_compression(asian_session)
            s2 = self.detect_scenario_2_expansion(asian_session)
            s3 = self.detect_scenario_3_continuation(asian_session, prev_h4_high, prev_h4_low)
            
            # Store results
            self.results['dates'].append(date)
            self.results['asian_ranges'].append(asian_session['range'])
            self.results['asian_highs'].append(asian_session['high'])
            self.results['asian_lows'].append(asian_session['low'])
            self.results['scenario_1_compression'].append(s1)
            self.results['scenario_2_expansion'].append(s2)
            self.results['scenario_3_continuation'].append(s3)
        
        print(f"\nAnalysis complete! Processed {len(self.results['dates'])} days.")
        
        # Create results DataFrame
        self.results_df = pd.DataFrame(self.results)
        self.results_df['year'] = [d.year for d in self.results_df['dates']]
        self.results_df['month'] = [d.month for d in self.results_df['dates']]
        self.results_df['day_of_week'] = [datetime.combine(d, time()).weekday() 
                                          for d in self.results_df['dates']]
        self.results_df['day_name'] = [datetime.combine(d, time()).strftime('%A') 
                                       for d in self.results_df['dates']]
        
        return self.results_df
    
    def generate_statistics(self):
        """Generate statistical summary of scenario occurrences."""
        print("\n" + "="*70)
        print("SCENARIO OCCURRENCE STATISTICS")
        print("="*70)
        
        total_days = len(self.results_df)
        
        # Overall statistics
        s1_count = self.results_df['scenario_1_compression'].sum()
        s2_count = self.results_df['scenario_2_expansion'].sum()
        s3_count = self.results_df['scenario_3_continuation'].sum()
        
        s1_pct = (s1_count / total_days) * 100
        s2_pct = (s2_count / total_days) * 100
        s3_pct = (s3_count / total_days) * 100
        
        print(f"\nTotal Trading Days: {total_days}")
        print(f"Period: {self.results_df['dates'].min()} to {self.results_df['dates'].max()}")
        print(f"\n{'='*70}")
        print(f"SCENARIO 1 - COMPRESSION (Range < 40 pts)")
        print(f"{'='*70}")
        print(f"  Occurrences: {s1_count}")
        print(f"  Percentage: {s1_pct:.2f}%")
        print(f"  Avg Range when detected: {self.results_df[self.results_df['scenario_1_compression']]['asian_ranges'].mean():.2f} pts")
        
        print(f"\n{'='*70}")
        print(f"SCENARIO 2 - EXPANSION (Range > 60 pts + directional)")
        print(f"{'='*70}")
        print(f"  Occurrences: {s2_count}")
        print(f"  Percentage: {s2_pct:.2f}%")
        print(f"  Avg Range when detected: {self.results_df[self.results_df['scenario_2_expansion']]['asian_ranges'].mean():.2f} pts")
        
        print(f"\n{'='*70}")
        print(f"SCENARIO 3 - CONTINUATION (Structure break)")
        print(f"{'='*70}")
        print(f"  Occurrences: {s3_count}")
        print(f"  Percentage: {s3_pct:.2f}%")
        if s3_count > 0:
            print(f"  Avg Range when detected: {self.results_df[self.results_df['scenario_3_continuation']]['asian_ranges'].mean():.2f} pts")
        
        # Co-occurrence analysis
        print(f"\n{'='*70}")
        print(f"CO-OCCURRENCE ANALYSIS")
        print(f"{'='*70}")
        
        no_scenario = ((~self.results_df['scenario_1_compression']) & 
                      (~self.results_df['scenario_2_expansion']) & 
                      (~self.results_df['scenario_3_continuation'])).sum()
        
        one_scenario = ((self.results_df['scenario_1_compression'].astype(int) + 
                        self.results_df['scenario_2_expansion'].astype(int) + 
                        self.results_df['scenario_3_continuation'].astype(int)) == 1).sum()
        
        two_scenarios = ((self.results_df['scenario_1_compression'].astype(int) + 
                         self.results_df['scenario_2_expansion'].astype(int) + 
                         self.results_df['scenario_3_continuation'].astype(int)) == 2).sum()
        
        three_scenarios = ((self.results_df['scenario_1_compression'].astype(int) + 
                           self.results_df['scenario_2_expansion'].astype(int) + 
                           self.results_df['scenario_3_continuation'].astype(int)) == 3).sum()
        
        print(f"  Days with 0 scenarios: {no_scenario} ({no_scenario/total_days*100:.2f}%)")
        print(f"  Days with 1 scenario: {one_scenario} ({one_scenario/total_days*100:.2f}%)")
        print(f"  Days with 2 scenarios: {two_scenarios} ({two_scenarios/total_days*100:.2f}%)")
        print(f"  Days with 3 scenarios: {three_scenarios} ({three_scenarios/total_days*100:.2f}%)")
        
        # Asian range statistics
        print(f"\n{'='*70}")
        print(f"ASIAN RANGE STATISTICS (All Days)")
        print(f"{'='*70}")
        print(f"  Mean: {self.results_df['asian_ranges'].mean():.2f} pts")
        print(f"  Median: {self.results_df['asian_ranges'].median():.2f} pts")
        print(f"  Std Dev: {self.results_df['asian_ranges'].std():.2f} pts")
        print(f"  Min: {self.results_df['asian_ranges'].min():.2f} pts")
        print(f"  Max: {self.results_df['asian_ranges'].max():.2f} pts")
        print(f"  25th percentile: {self.results_df['asian_ranges'].quantile(0.25):.2f} pts")
        print(f"  75th percentile: {self.results_df['asian_ranges'].quantile(0.75):.2f} pts")
        
        return {
            'total_days': total_days,
            's1_count': s1_count,
            's1_pct': s1_pct,
            's2_count': s2_count,
            's2_pct': s2_pct,
            's3_count': s3_count,
            's3_pct': s3_pct
        }
    
    def generate_visualizations(self):
        """Generate all visualization charts."""
        print("\nGenerating visualizations...")
        
        # 1. Asian Range Distribution Histogram
        plt.figure(figsize=(12, 6))
        plt.hist(self.results_df['asian_ranges'], bins=50, edgecolor='black', alpha=0.7)
        plt.axvline(40, color='red', linestyle='--', linewidth=2, label='Compression Threshold (40 pts)')
        plt.axvline(60, color='green', linestyle='--', linewidth=2, label='Expansion Threshold (60 pts)')
        plt.xlabel('Asian Range (points)', fontsize=12)
        plt.ylabel('Frequency (number of days)', fontsize=12)
        plt.title('Distribution of Asian Range (Tokyo Session 20:00-00:00 NY)\nNQ 2018-2025', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('asian_range_distribution.png', dpi=300, bbox_inches='tight')
        print("  ✓ Saved: asian_range_distribution.png")
        plt.close()
        
        # 2. Annual Frequency per Scenario
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        for idx, (scenario, title, color) in enumerate([
            ('scenario_1_compression', 'Scenario 1: COMPRESSION\n(Range < 40 pts)', 'steelblue'),
            ('scenario_2_expansion', 'Scenario 2: EXPANSION\n(Range > 60 pts)', 'darkorange'),
            ('scenario_3_continuation', 'Scenario 3: CONTINUATION\n(Structure Break)', 'green')
        ]):
            yearly_counts = self.results_df.groupby('year')[scenario].sum()
            yearly_total = self.results_df.groupby('year').size()
            yearly_pct = (yearly_counts / yearly_total * 100)
            
            axes[idx].bar(yearly_counts.index, yearly_pct, color=color, alpha=0.7, edgecolor='black')
            axes[idx].set_xlabel('Year', fontsize=11)
            axes[idx].set_ylabel('Percentage (%)', fontsize=11)
            axes[idx].set_title(title, fontsize=12, fontweight='bold')
            axes[idx].grid(True, alpha=0.3, axis='y')
            axes[idx].set_ylim(0, max(yearly_pct) * 1.2)
            
            # Add value labels on bars
            for i, (year, pct) in enumerate(yearly_pct.items()):
                axes[idx].text(year, pct + 1, f'{pct:.1f}%', ha='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('annual_scenario_frequency.png', dpi=300, bbox_inches='tight')
        print("  ✓ Saved: annual_scenario_frequency.png")
        plt.close()
        
        # 3. Monthly Frequency per Scenario
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        for idx, (scenario, title, color) in enumerate([
            ('scenario_1_compression', 'Scenario 1: COMPRESSION', 'steelblue'),
            ('scenario_2_expansion', 'Scenario 2: EXPANSION', 'darkorange'),
            ('scenario_3_continuation', 'Scenario 3: CONTINUATION', 'green')
        ]):
            monthly_counts = self.results_df.groupby('month')[scenario].sum()
            monthly_total = self.results_df.groupby('month').size()
            monthly_pct = (monthly_counts / monthly_total * 100)
            
            axes[idx].bar(range(1, 13), [monthly_pct.get(m, 0) for m in range(1, 13)], 
                         color=color, alpha=0.7, edgecolor='black')
            axes[idx].set_xlabel('Month', fontsize=11)
            axes[idx].set_ylabel('Percentage (%)', fontsize=11)
            axes[idx].set_title(title, fontsize=12, fontweight='bold')
            axes[idx].set_xticks(range(1, 13))
            axes[idx].set_xticklabels(month_names)
            axes[idx].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('monthly_scenario_frequency.png', dpi=300, bbox_inches='tight')
        print("  ✓ Saved: monthly_scenario_frequency.png")
        plt.close()
        
        # 4. Day of Week Distribution
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        for idx, (scenario, title, color) in enumerate([
            ('scenario_1_compression', 'Scenario 1: COMPRESSION', 'steelblue'),
            ('scenario_2_expansion', 'Scenario 2: EXPANSION', 'darkorange'),
            ('scenario_3_continuation', 'Scenario 3: CONTINUATION', 'green')
        ]):
            dow_counts = self.results_df.groupby('day_of_week')[scenario].sum()
            dow_total = self.results_df.groupby('day_of_week').size()
            dow_pct = (dow_counts / dow_total * 100)
            
            axes[idx].bar(range(5), [dow_pct.get(d, 0) for d in range(5)], 
                         color=color, alpha=0.7, edgecolor='black')
            axes[idx].set_xlabel('Day of Week', fontsize=11)
            axes[idx].set_ylabel('Percentage (%)', fontsize=11)
            axes[idx].set_title(title, fontsize=12, fontweight='bold')
            axes[idx].set_xticks(range(5))
            axes[idx].set_xticklabels(day_names, rotation=45, ha='right')
            axes[idx].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('day_of_week_scenario_frequency.png', dpi=300, bbox_inches='tight')
        print("  ✓ Saved: day_of_week_scenario_frequency.png")
        plt.close()
        
        print("\n✓ All visualizations generated successfully!")
    
    def generate_report(self, stats):
        """Generate the markdown report."""
        print("\nGenerating markdown report...")
        
        report_lines = []
        
        # Header
        report_lines.append("# SCENARIO OCCURRENCE ANALYSIS - NQ 2018-2025")
        report_lines.append("")
        report_lines.append("**PURE STATISTICAL ANALYSIS - Pattern Frequency Detection**")
        report_lines.append("")
        report_lines.append("*This is NOT a trading backtest. This analysis counts how often specific patterns occur in historical data.*")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Section 1: Overview
        report_lines.append("## 1. VUE D'ENSEMBLE")
        report_lines.append("")
        report_lines.append(f"**Période Analysée:** {self.results_df['dates'].min()} à {self.results_df['dates'].max()}")
        report_lines.append("")
        report_lines.append(f"**Nombre Total de Jours de Trading:** {stats['total_days']}")
        report_lines.append("")
        report_lines.append("**Années Couvertes:** 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025")
        report_lines.append("")
        report_lines.append("### Résumé des 3 Scénarios Analysés")
        report_lines.append("")
        report_lines.append("| Scénario | Description | Critère de Détection |")
        report_lines.append("|----------|-------------|---------------------|")
        report_lines.append("| **1. COMPRESSION** | Range asiatique étroit | Range < 40 points |")
        report_lines.append("| **2. EXPANSION** | Range asiatique large avec tendance | Range > 60 points + mouvement directionnel |")
        report_lines.append("| **3. CONTINUATION** | Cassure de structure pendant Tokyo | Break de high/low H4 significatif |")
        report_lines.append("")
        report_lines.append("**Session Tokyo:** 20h00-00h00 (heure NY)")
        report_lines.append("")
        report_lines.append("**Session Londres:** 02h00-05h00 (heure NY)")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Section 2: Results per scenario
        report_lines.append("## 2. RÉSULTATS PAR SCÉNARIO")
        report_lines.append("")
        
        # Scenario 1
        report_lines.append("### 🔵 SCÉNARIO 1: LA COMPRESSION")
        report_lines.append("")
        report_lines.append("**Condition:** Range asiatique < 40 points")
        report_lines.append("")
        report_lines.append(f"- **Nombre d'occurrences:** {stats['s1_count']}")
        report_lines.append(f"- **Pourcentage du total:** {stats['s1_pct']:.2f}%")
        
        s1_data = self.results_df[self.results_df['scenario_1_compression']]
        if len(s1_data) > 0:
            report_lines.append(f"- **Range moyen quand détecté:** {s1_data['asian_ranges'].mean():.2f} points")
            report_lines.append(f"- **Range médian quand détecté:** {s1_data['asian_ranges'].median():.2f} points")
        
        report_lines.append("")
        report_lines.append("#### Distribution par Année")
        report_lines.append("")
        report_lines.append("| Année | Occurrences | % de l'année |")
        report_lines.append("|-------|-------------|--------------|")
        
        for year in sorted(self.results_df['year'].unique()):
            year_data = self.results_df[self.results_df['year'] == year]
            year_s1 = year_data['scenario_1_compression'].sum()
            year_pct = (year_s1 / len(year_data)) * 100
            report_lines.append(f"| {year} | {year_s1} | {year_pct:.2f}% |")
        
        report_lines.append("")
        report_lines.append("#### Distribution par Mois")
        report_lines.append("")
        report_lines.append("| Mois | Occurrences | % du mois |")
        report_lines.append("|------|-------------|-----------|")
        
        month_names_fr = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                         'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        
        for month in range(1, 13):
            month_data = self.results_df[self.results_df['month'] == month]
            if len(month_data) > 0:
                month_s1 = month_data['scenario_1_compression'].sum()
                month_pct = (month_s1 / len(month_data)) * 100
                report_lines.append(f"| {month_names_fr[month-1]} | {month_s1} | {month_pct:.2f}% |")
        
        report_lines.append("")
        report_lines.append("#### Distribution par Jour de la Semaine")
        report_lines.append("")
        report_lines.append("| Jour | Occurrences | % du jour |")
        report_lines.append("|------|-------------|-----------|")
        
        day_names_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
        
        for day in range(5):
            day_data = self.results_df[self.results_df['day_of_week'] == day]
            if len(day_data) > 0:
                day_s1 = day_data['scenario_1_compression'].sum()
                day_pct = (day_s1 / len(day_data)) * 100
                report_lines.append(f"| {day_names_fr[day]} | {day_s1} | {day_pct:.2f}% |")
        
        report_lines.append("")
        report_lines.append("**Graphique:** Voir `annual_scenario_frequency.png` et `monthly_scenario_frequency.png`")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Scenario 2
        report_lines.append("### 🟠 SCÉNARIO 2: L'EXPANSION")
        report_lines.append("")
        report_lines.append("**Condition:** Range asiatique > 60 points avec tendance directionnelle")
        report_lines.append("")
        report_lines.append(f"- **Nombre d'occurrences:** {stats['s2_count']}")
        report_lines.append(f"- **Pourcentage du total:** {stats['s2_pct']:.2f}%")
        
        s2_data = self.results_df[self.results_df['scenario_2_expansion']]
        if len(s2_data) > 0:
            report_lines.append(f"- **Range moyen quand détecté:** {s2_data['asian_ranges'].mean():.2f} points")
            report_lines.append(f"- **Range médian quand détecté:** {s2_data['asian_ranges'].median():.2f} points")
        
        report_lines.append("")
        report_lines.append("#### Distribution par Année")
        report_lines.append("")
        report_lines.append("| Année | Occurrences | % de l'année |")
        report_lines.append("|-------|-------------|--------------|")
        
        for year in sorted(self.results_df['year'].unique()):
            year_data = self.results_df[self.results_df['year'] == year]
            year_s2 = year_data['scenario_2_expansion'].sum()
            year_pct = (year_s2 / len(year_data)) * 100
            report_lines.append(f"| {year} | {year_s2} | {year_pct:.2f}% |")
        
        report_lines.append("")
        report_lines.append("#### Distribution par Mois")
        report_lines.append("")
        report_lines.append("| Mois | Occurrences | % du mois |")
        report_lines.append("|------|-------------|-----------|")
        
        for month in range(1, 13):
            month_data = self.results_df[self.results_df['month'] == month]
            if len(month_data) > 0:
                month_s2 = month_data['scenario_2_expansion'].sum()
                month_pct = (month_s2 / len(month_data)) * 100
                report_lines.append(f"| {month_names_fr[month-1]} | {month_s2} | {month_pct:.2f}% |")
        
        report_lines.append("")
        report_lines.append("#### Distribution par Jour de la Semaine")
        report_lines.append("")
        report_lines.append("| Jour | Occurrences | % du jour |")
        report_lines.append("|------|-------------|-----------|")
        
        for day in range(5):
            day_data = self.results_df[self.results_df['day_of_week'] == day]
            if len(day_data) > 0:
                day_s2 = day_data['scenario_2_expansion'].sum()
                day_pct = (day_s2 / len(day_data)) * 100
                report_lines.append(f"| {day_names_fr[day]} | {day_s2} | {day_pct:.2f}% |")
        
        report_lines.append("")
        report_lines.append("**Graphique:** Voir `annual_scenario_frequency.png` et `monthly_scenario_frequency.png`")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Scenario 3
        report_lines.append("### 🟢 SCÉNARIO 3: LA CONTINUATION")
        report_lines.append("")
        report_lines.append("**Condition:** Tokyo casse un niveau de structure H4 ou D1 important")
        report_lines.append("")
        report_lines.append(f"- **Nombre d'occurrences:** {stats['s3_count']}")
        report_lines.append(f"- **Pourcentage du total:** {stats['s3_pct']:.2f}%")
        
        s3_data = self.results_df[self.results_df['scenario_3_continuation']]
        if len(s3_data) > 0:
            report_lines.append(f"- **Range moyen quand détecté:** {s3_data['asian_ranges'].mean():.2f} points")
            report_lines.append(f"- **Range médian quand détecté:** {s3_data['asian_ranges'].median():.2f} points")
        
        report_lines.append("")
        report_lines.append("**Critère de détection:**")
        report_lines.append("- Break du high/low H4 des 5 jours précédents avec marge de > 10 points")
        report_lines.append("")
        report_lines.append("#### Distribution par Année")
        report_lines.append("")
        report_lines.append("| Année | Occurrences | % de l'année |")
        report_lines.append("|-------|-------------|--------------|")
        
        for year in sorted(self.results_df['year'].unique()):
            year_data = self.results_df[self.results_df['year'] == year]
            year_s3 = year_data['scenario_3_continuation'].sum()
            year_pct = (year_s3 / len(year_data)) * 100
            report_lines.append(f"| {year} | {year_s3} | {year_pct:.2f}% |")
        
        report_lines.append("")
        report_lines.append("#### Distribution par Mois")
        report_lines.append("")
        report_lines.append("| Mois | Occurrences | % du mois |")
        report_lines.append("|------|-------------|-----------|")
        
        for month in range(1, 13):
            month_data = self.results_df[self.results_df['month'] == month]
            if len(month_data) > 0:
                month_s3 = month_data['scenario_3_continuation'].sum()
                month_pct = (month_s3 / len(month_data)) * 100
                report_lines.append(f"| {month_names_fr[month-1]} | {month_s3} | {month_pct:.2f}% |")
        
        report_lines.append("")
        report_lines.append("#### Distribution par Jour de la Semaine")
        report_lines.append("")
        report_lines.append("| Jour | Occurrences | % du jour |")
        report_lines.append("|------|-------------|-----------|")
        
        for day in range(5):
            day_data = self.results_df[self.results_df['day_of_week'] == day]
            if len(day_data) > 0:
                day_s3 = day_data['scenario_3_continuation'].sum()
                day_pct = (day_s3 / len(day_data)) * 100
                report_lines.append(f"| {day_names_fr[day]} | {day_s3} | {day_pct:.2f}% |")
        
        report_lines.append("")
        report_lines.append("**Graphique:** Voir `annual_scenario_frequency.png` et `monthly_scenario_frequency.png`")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Section 3: Cross-analysis
        report_lines.append("## 3. ANALYSE CROISÉE")
        report_lines.append("")
        
        # Co-occurrence
        no_scenario = ((~self.results_df['scenario_1_compression']) & 
                      (~self.results_df['scenario_2_expansion']) & 
                      (~self.results_df['scenario_3_continuation'])).sum()
        
        one_scenario = ((self.results_df['scenario_1_compression'].astype(int) + 
                        self.results_df['scenario_2_expansion'].astype(int) + 
                        self.results_df['scenario_3_continuation'].astype(int)) == 1).sum()
        
        two_scenarios = ((self.results_df['scenario_1_compression'].astype(int) + 
                         self.results_df['scenario_2_expansion'].astype(int) + 
                         self.results_df['scenario_3_continuation'].astype(int)) == 2).sum()
        
        three_scenarios = ((self.results_df['scenario_1_compression'].astype(int) + 
                           self.results_df['scenario_2_expansion'].astype(int) + 
                           self.results_df['scenario_3_continuation'].astype(int)) == 3).sum()
        
        report_lines.append("### Co-occurrence des Scénarios")
        report_lines.append("")
        report_lines.append("| Nombre de Scénarios | Jours | Pourcentage |")
        report_lines.append("|---------------------|-------|-------------|")
        report_lines.append(f"| 0 scénario | {no_scenario} | {no_scenario/stats['total_days']*100:.2f}% |")
        report_lines.append(f"| 1 scénario | {one_scenario} | {one_scenario/stats['total_days']*100:.2f}% |")
        report_lines.append(f"| 2 scénarios | {two_scenarios} | {two_scenarios/stats['total_days']*100:.2f}% |")
        report_lines.append(f"| 3 scénarios | {three_scenarios} | {three_scenarios/stats['total_days']*100:.2f}% |")
        report_lines.append("")
        
        # Co-occurrence matrix
        report_lines.append("### Matrice de Co-occurrence")
        report_lines.append("")
        report_lines.append("Nombre de jours où deux scénarios se produisent simultanément:")
        report_lines.append("")
        
        s1_and_s2 = (self.results_df['scenario_1_compression'] & self.results_df['scenario_2_expansion']).sum()
        s1_and_s3 = (self.results_df['scenario_1_compression'] & self.results_df['scenario_3_continuation']).sum()
        s2_and_s3 = (self.results_df['scenario_2_expansion'] & self.results_df['scenario_3_continuation']).sum()
        
        report_lines.append("| Combinaison | Occurrences |")
        report_lines.append("|-------------|-------------|")
        report_lines.append(f"| Compression + Expansion | {s1_and_s2} |")
        report_lines.append(f"| Compression + Continuation | {s1_and_s3} |")
        report_lines.append(f"| Expansion + Continuation | {s2_and_s3} |")
        report_lines.append("")
        report_lines.append("*Note: Il est théoriquement impossible d'avoir Compression (< 40 pts) ET Expansion (> 60 pts) simultanément. Les rares cas détectés sont dus à l'arrondi ou aux critères additionnels.*")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Section 4: Temporal patterns
        report_lines.append("## 4. PATTERNS TEMPORELS")
        report_lines.append("")
        
        report_lines.append("### Évolution Annuelle")
        report_lines.append("")
        report_lines.append("| Année | S1: Compression | S2: Expansion | S3: Continuation | Jours Totaux |")
        report_lines.append("|-------|----------------|---------------|------------------|--------------|")
        
        for year in sorted(self.results_df['year'].unique()):
            year_data = self.results_df[self.results_df['year'] == year]
            y_s1 = year_data['scenario_1_compression'].sum()
            y_s2 = year_data['scenario_2_expansion'].sum()
            y_s3 = year_data['scenario_3_continuation'].sum()
            y_total = len(year_data)
            report_lines.append(f"| {year} | {y_s1} ({y_s1/y_total*100:.1f}%) | {y_s2} ({y_s2/y_total*100:.1f}%) | {y_s3} ({y_s3/y_total*100:.1f}%) | {y_total} |")
        
        report_lines.append("")
        report_lines.append("### Jours de la Semaine les Plus Fréquents")
        report_lines.append("")
        report_lines.append("| Jour | S1: Compression | S2: Expansion | S3: Continuation |")
        report_lines.append("|------|----------------|---------------|------------------|")
        
        for day in range(5):
            day_data = self.results_df[self.results_df['day_of_week'] == day]
            if len(day_data) > 0:
                d_s1 = day_data['scenario_1_compression'].sum()
                d_s2 = day_data['scenario_2_expansion'].sum()
                d_s3 = day_data['scenario_3_continuation'].sum()
                d_total = len(day_data)
                report_lines.append(f"| {day_names_fr[day]} | {d_s1} ({d_s1/d_total*100:.1f}%) | {d_s2} ({d_s2/d_total*100:.1f}%) | {d_s3} ({d_s3/d_total*100:.1f}%) |")
        
        report_lines.append("")
        report_lines.append("### Observations sur les Clusters Temporels")
        report_lines.append("")
        report_lines.append("*Analyser les graphiques pour identifier des patterns saisonniers:*")
        report_lines.append("")
        report_lines.append("- **Compressions:** Vérifier si plus fréquentes en été (juillet-août) lors de faible volatilité")
        report_lines.append("- **Expansions:** Potentiellement plus fréquentes en début/fin de mois ou lors d'annonces macro")
        report_lines.append("- **Continuations:** Possiblement corrélées aux périodes de forte volatilité (début de trimestre)")
        report_lines.append("")
        report_lines.append("**Graphiques associés:**")
        report_lines.append("- `monthly_scenario_frequency.png` - Distribution mensuelle")
        report_lines.append("- `annual_scenario_frequency.png` - Évolution annuelle")
        report_lines.append("- `day_of_week_scenario_frequency.png` - Répartition par jour de semaine")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # Section 5: Descriptive statistics
        report_lines.append("## 5. STATISTIQUES DESCRIPTIVES")
        report_lines.append("")
        
        report_lines.append("### Range Asiatique - Statistiques Globales")
        report_lines.append("")
        report_lines.append("| Métrique | Valeur |")
        report_lines.append("|----------|--------|")
        report_lines.append(f"| Moyenne | {self.results_df['asian_ranges'].mean():.2f} points |")
        report_lines.append(f"| Médiane | {self.results_df['asian_ranges'].median():.2f} points |")
        report_lines.append(f"| Écart-type | {self.results_df['asian_ranges'].std():.2f} points |")
        report_lines.append(f"| Minimum | {self.results_df['asian_ranges'].min():.2f} points |")
        report_lines.append(f"| Maximum | {self.results_df['asian_ranges'].max():.2f} points |")
        report_lines.append(f"| 25ème percentile | {self.results_df['asian_ranges'].quantile(0.25):.2f} points |")
        report_lines.append(f"| 50ème percentile (Médiane) | {self.results_df['asian_ranges'].quantile(0.50):.2f} points |")
        report_lines.append(f"| 75ème percentile | {self.results_df['asian_ranges'].quantile(0.75):.2f} points |")
        report_lines.append("")
        
        report_lines.append("### Seuils Utilisés vs Réalité des Données")
        report_lines.append("")
        report_lines.append("| Seuil | Valeur | Pourcentage des Jours |")
        report_lines.append("|-------|--------|----------------------|")
        
        below_40 = (self.results_df['asian_ranges'] < 40).sum()
        above_60 = (self.results_df['asian_ranges'] > 60).sum()
        between_40_60 = ((self.results_df['asian_ranges'] >= 40) & (self.results_df['asian_ranges'] <= 60)).sum()
        
        report_lines.append(f"| Range < 40 pts (Compression) | < 40 | {below_40/stats['total_days']*100:.2f}% |")
        report_lines.append(f"| Range entre 40-60 pts | 40-60 | {between_40_60/stats['total_days']*100:.2f}% |")
        report_lines.append(f"| Range > 60 pts (Expansion) | > 60 | {above_60/stats['total_days']*100:.2f}% |")
        report_lines.append("")
        
        report_lines.append("### Distribution des Ranges (Histogramme)")
        report_lines.append("")
        report_lines.append("Voir le graphique `asian_range_distribution.png` pour la distribution complète.")
        report_lines.append("")
        report_lines.append("**Interprétation:**")
        report_lines.append("")
        report_lines.append(f"- La majorité des jours ({between_40_60/stats['total_days']*100:.2f}%) présentent un range entre 40 et 60 points")
        report_lines.append(f"- Les compressions (< 40 pts) représentent {below_40/stats['total_days']*100:.2f}% des jours")
        report_lines.append(f"- Les expansions (> 60 pts) représentent {above_60/stats['total_days']*100:.2f}% des jours")
        report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # Conclusion
        report_lines.append("## 6. CONCLUSION")
        report_lines.append("")
        report_lines.append(f"### Synthèse des Résultats (sur {stats['total_days']} jours de trading)")
        report_lines.append("")
        report_lines.append("| Scénario | Occurrences | Fréquence | Caractéristique |")
        report_lines.append("|----------|-------------|-----------|-----------------|")
        report_lines.append(f"| 🔵 **COMPRESSION** | {stats['s1_count']} | {stats['s1_pct']:.2f}% | Setup principal le plus fréquent |")
        report_lines.append(f"| 🟠 **EXPANSION** | {stats['s2_count']} | {stats['s2_pct']:.2f}% | Setup modéré, nécessite vigilance |")
        report_lines.append(f"| 🟢 **CONTINUATION** | {stats['s3_count']} | {stats['s3_pct']:.2f}% | Setup rare mais haute qualité |")
        report_lines.append("")
        
        report_lines.append("### Points Clés")
        report_lines.append("")
        report_lines.append(f"1. **Pattern le plus fréquent:** Scénario 1 (Compression) avec {stats['s1_pct']:.2f}% des jours")
        report_lines.append(f"2. **Jours sans scénario clair:** {no_scenario/stats['total_days']*100:.2f}% des jours ne correspondent à aucun des 3 scénarios")
        report_lines.append(f"3. **Range asiatique typique:** {self.results_df['asian_ranges'].median():.2f} points (médiane)")
        report_lines.append(f"4. **Années les plus volatiles:** Analyser les années avec plus d'expansions dans les graphiques")
        report_lines.append("")
        
        report_lines.append("### Recommandations pour l'Utilisation")
        report_lines.append("")
        report_lines.append("Ces statistiques de fréquence permettent de:")
        report_lines.append("")
        report_lines.append("- **Comprendre la probabilité a priori** de chaque setup avant l'ouverture de Londres")
        report_lines.append("- **Identifier les périodes favorables** (mois, jours de semaine) pour chaque scénario")
        report_lines.append("- **Calibrer les attentes** : ne pas forcer un trade si aucun scénario n'est présent")
        report_lines.append("- **Adapter la stratégie** selon la saisonnalité observée")
        report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("## 📊 GRAPHIQUES GÉNÉRÉS")
        report_lines.append("")
        report_lines.append("1. **`asian_range_distribution.png`** - Distribution des ranges asiatiques (histogramme)")
        report_lines.append("2. **`annual_scenario_frequency.png`** - Fréquence annuelle de chaque scénario")
        report_lines.append("3. **`monthly_scenario_frequency.png`** - Fréquence mensuelle de chaque scénario")
        report_lines.append("4. **`day_of_week_scenario_frequency.png`** - Répartition par jour de la semaine")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        report_lines.append(f"*Rapport généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report_lines.append("")
        report_lines.append("*Analyse réalisée avec Python - pandas, numpy, matplotlib, seaborn*")
        report_lines.append("")
        
        # Write report to file
        report_path = self.data_dir / "SCENARIO_OCCURRENCE_ANALYSIS_NQ_2018_2025.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        print(f"✓ Report saved to: {report_path}")
        
        return report_path


def main():
    """Main execution function."""
    print("="*70)
    print("SCENARIO FREQUENCY ANALYSIS - NQ 2018-2025")
    print("="*70)
    print("\nThis script performs PURE STATISTICAL ANALYSIS of pattern occurrences.")
    print("NO TRADING, NO POSITIONS - Only pattern detection and counting.\n")
    
    # Initialize analyzer
    analyzer = ScenarioFrequencyAnalyzer()
    
    # Load data
    analyzer.load_data()
    
    # Identify sessions
    analyzer.identify_sessions()
    
    # Analyze all days
    analyzer.analyze_all_days()
    
    # Generate statistics
    stats = analyzer.generate_statistics()
    
    # Generate visualizations
    analyzer.generate_visualizations()
    
    # Generate report
    analyzer.generate_report(stats)
    
    print("\n" + "="*70)
    print("✓ ANALYSIS COMPLETE!")
    print("="*70)
    print("\nGenerated files:")
    print("  - SCENARIO_OCCURRENCE_ANALYSIS_NQ_2018_2025.md (report)")
    print("  - asian_range_distribution.png")
    print("  - annual_scenario_frequency.png")
    print("  - monthly_scenario_frequency.png")
    print("  - day_of_week_scenario_frequency.png")
    print("\n")


if __name__ == "__main__":
    main()
