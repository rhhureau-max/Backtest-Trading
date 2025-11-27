#!/usr/bin/env python3
"""
Tokyo-London Continuation Analysis Script

This script analyzes the continuation of the Tokyo session trend onto the London session,
using 1-minute, 5-minute, and 15-minute data from 2018 to 2025.

Session Definitions (Chicago/CT Timezone):
- Tokyo: 19:00 - 23:59 (last candle at 23:59/55/45 depending on timeframe)
- London (analysis window): 02:00 - 05:59 (last candle at 05:59/55/45 depending on timeframe)

A "GOOD" session is when London continues Tokyo's trend direction.
A "BAD" session is when London reverses Tokyo's trend direction.
"""

import os
import zipfile
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, time, timedelta
from typing import Optional, Tuple, Dict, List
import io


# Session time definitions (Chicago Time)
# Tokyo session: 19:00 - 23:59 (last candle depends on timeframe)
# London session: 02:00 - 05:59 (last candle depends on timeframe)
TOKYO_START = time(19, 0)
TOKYO_BASE_END_HOUR = 23  # Last hour containing Tokyo session candles
LONDON_START = time(2, 0)
LONDON_BASE_END_HOUR = 5  # Last hour containing London session candles

# Number of quartiles for trend strength analysis
NUM_QUARTILES = 4


def get_last_candle_time(base_hour: int, timeframe: str) -> time:
    """
    Get the last candle start time for a given session and timeframe.
    
    For a session ending at hour H:
    - 1m timeframe: last candle at H:59
    - 5m timeframe: last candle at H:55
    - 15m timeframe: last candle at H:45
    """
    minutes_map = {"1m": 59, "5m": 55, "15m": 45}
    minutes = minutes_map.get(timeframe, 59)
    return time(base_hour, minutes)


def read_csv_file(filepath: str) -> pd.DataFrame:
    """Read a CSV file and return a DataFrame."""
    df = pd.read_csv(
        filepath,
        sep=';',
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        skiprows=1  # Skip header row
    )
    return df


def read_zip_file(filepath: str) -> pd.DataFrame:
    """Read a CSV file from a zip archive."""
    with zipfile.ZipFile(filepath, 'r') as z:
        # Get the first CSV file in the archive
        csv_files = [f for f in z.namelist() if f.endswith('.csv')]
        if not csv_files:
            raise ValueError(f"No CSV file found in {filepath}")
        
        with z.open(csv_files[0]) as f:
            df = pd.read_csv(
                io.TextIOWrapper(f, encoding='utf-8'),
                sep=';',
                names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
                skiprows=1
            )
    return df


def load_data(data_dir: str, timeframe: str, years: List[int]) -> pd.DataFrame:
    """Load all data files for a given timeframe and years."""
    all_data = []
    
    for year in years:
        if timeframe == "1m":
            # 1m data may be in zip or csv format - check both dynamically
            zip_path = os.path.join(data_dir, f"{year} 1m.csv.zip")
            csv_path = os.path.join(data_dir, f"{year} 1m.csv")
            
            if os.path.exists(zip_path):
                try:
                    df = read_zip_file(zip_path)
                    all_data.append(df)
                    print(f"  Loaded {year} 1m from zip")
                except Exception as e:
                    print(f"  Error loading {zip_path}: {e}")
            elif os.path.exists(csv_path):
                try:
                    df = read_csv_file(csv_path)
                    all_data.append(df)
                    print(f"  Loaded {year} 1m from csv")
                except Exception as e:
                    print(f"  Error loading {csv_path}: {e}")
            else:
                print(f"  No 1m data found for {year}")
        else:
            csv_path = os.path.join(data_dir, f"{year} {timeframe}.csv")
            if os.path.exists(csv_path):
                try:
                    df = read_csv_file(csv_path)
                    all_data.append(df)
                    print(f"  Loaded {year} {timeframe}")
                except Exception as e:
                    print(f"  Error loading {csv_path}: {e}")
            else:
                print(f"  No {timeframe} data found for {year}")
    
    if not all_data:
        return pd.DataFrame()
    
    combined = pd.concat(all_data, ignore_index=True)
    
    # Parse datetime
    combined['DateTime'] = pd.to_datetime(
        combined['Date'] + ' ' + combined['Time'],
        format='%d/%m/%Y %H:%M:%S'
    )
    combined['DateOnly'] = combined['DateTime'].dt.date
    combined['TimeOnly'] = combined['DateTime'].dt.time
    combined['DayOfWeek'] = combined['DateTime'].dt.dayofweek  # 0=Monday, 6=Sunday
    combined['Year'] = combined['DateTime'].dt.year
    
    return combined.sort_values('DateTime').reset_index(drop=True)


def get_session_data(df: pd.DataFrame, date: datetime.date, 
                     start_time: time, end_time: time,
                     next_day: bool = False) -> pd.DataFrame:
    """Get data for a specific session on a given date."""
    target_date = date + timedelta(days=1) if next_day else date
    
    session_data = df[
        (df['DateOnly'] == target_date) &
        (df['TimeOnly'] >= start_time) &
        (df['TimeOnly'] <= end_time)
    ]
    
    return session_data


def calculate_trend(session_data: pd.DataFrame) -> Tuple[Optional[str], float]:
    """
    Calculate the trend direction and distance for a session.
    Returns: (direction, distance)
    - direction: 'bullish', 'bearish', or None if insufficient data
    - distance: absolute price difference
    """
    if session_data.empty or len(session_data) < 2:
        return None, 0.0
    
    first_candle = session_data.iloc[0]
    last_candle = session_data.iloc[-1]
    
    open_price = first_candle['Open']
    close_price = last_candle['Close']
    
    distance = close_price - open_price
    
    if close_price > open_price:
        return 'bullish', abs(distance)
    elif close_price < open_price:
        return 'bearish', abs(distance)
    else:
        return None, 0.0


def analyze_timeframe_vectorized(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Analyze all days for a given timeframe using vectorized operations."""
    if df.empty:
        return pd.DataFrame()
    
    print("  Preparing data...")
    
    # Get last candle times based on timeframe
    tokyo_end = get_last_candle_time(TOKYO_BASE_END_HOUR, timeframe)
    london_end = get_last_candle_time(LONDON_BASE_END_HOUR, timeframe)
    
    # Add helper columns for filtering
    df = df.copy()
    df['Hour'] = df['DateTime'].dt.hour
    df['Minute'] = df['DateTime'].dt.minute
    df['TimeMinutes'] = df['Hour'] * 60 + df['Minute']
    
    tokyo_start_minutes = TOKYO_START.hour * 60 + TOKYO_START.minute
    tokyo_end_minutes = tokyo_end.hour * 60 + tokyo_end.minute
    london_start_minutes = LONDON_START.hour * 60 + LONDON_START.minute
    london_end_minutes = london_end.hour * 60 + london_end.minute
    
    # Filter Tokyo session data (19:00 - 23:xx)
    tokyo_mask = (df['TimeMinutes'] >= tokyo_start_minutes) & (df['TimeMinutes'] <= tokyo_end_minutes)
    tokyo_df = df[tokyo_mask].copy()
    
    # Filter London session data (02:00 - 05:xx)
    london_mask = (df['TimeMinutes'] >= london_start_minutes) & (df['TimeMinutes'] <= london_end_minutes)
    london_df = df[london_mask].copy()
    
    print("  Processing Tokyo sessions...")
    
    # Get first and last candles for Tokyo sessions grouped by date
    tokyo_first = tokyo_df.sort_values('DateTime').groupby('DateOnly').first()[['Open', 'DateTime']].rename(
        columns={'Open': 'tokyo_open', 'DateTime': 'tokyo_first_dt'}
    )
    tokyo_last = tokyo_df.sort_values('DateTime').groupby('DateOnly').last()[['Close', 'DateTime']].rename(
        columns={'Close': 'tokyo_close', 'DateTime': 'tokyo_last_dt'}
    )
    tokyo_count = tokyo_df.groupby('DateOnly').size().rename('tokyo_candles')
    
    tokyo_summary = tokyo_first.join(tokyo_last).join(tokyo_count)
    tokyo_summary['tokyo_distance'] = (tokyo_summary['tokyo_close'] - tokyo_summary['tokyo_open']).abs()
    tokyo_summary['tokyo_trend'] = np.where(
        tokyo_summary['tokyo_close'] > tokyo_summary['tokyo_open'], 'bullish',
        np.where(tokyo_summary['tokyo_close'] < tokyo_summary['tokyo_open'], 'bearish', None)
    )
    
    print("  Processing London sessions...")
    
    # Get first and last candles for London sessions grouped by date
    london_first = london_df.sort_values('DateTime').groupby('DateOnly').first()[['Open', 'DateTime']].rename(
        columns={'Open': 'london_open', 'DateTime': 'london_first_dt'}
    )
    london_last = london_df.sort_values('DateTime').groupby('DateOnly').last()[['Close', 'DateTime']].rename(
        columns={'Close': 'london_close', 'DateTime': 'london_last_dt'}
    )
    london_count = london_df.groupby('DateOnly').size().rename('london_candles')
    
    london_summary = london_first.join(london_last).join(london_count)
    london_summary['london_distance'] = (london_summary['london_close'] - london_summary['london_open']).abs()
    london_summary['london_trend'] = np.where(
        london_summary['london_close'] > london_summary['london_open'], 'bullish',
        np.where(london_summary['london_close'] < london_summary['london_open'], 'bearish', None)
    )
    
    print("  Matching sessions...")
    
    # Session matching logic:
    # - Tokyo session occurs on Day D from 19:00-23:59
    # - The corresponding London session occurs on Day D+1 from 02:00-05:59
    # - tokyo_summary is indexed by Tokyo's date (D)
    # - london_summary is indexed by London's date (D+1)
    # - To join them, we shift Tokyo's date forward by 1 day (D -> D+1)
    # - Then both DataFrames are indexed by the London date (D+1)
    tokyo_summary_shifted = tokyo_summary.copy()
    tokyo_summary_shifted.index = (pd.to_datetime(tokyo_summary_shifted.index) + timedelta(days=1)).date
    
    # Join Tokyo (shifted) with London using London's date as the key
    combined = tokyo_summary_shifted.join(london_summary, how='inner', lsuffix='_tokyo', rsuffix='_london')
    
    # Filter out rows with None trends
    combined = combined[
        (combined['tokyo_trend'].notna()) & 
        (combined['london_trend'].notna()) &
        (combined['tokyo_trend'] != 'None') &
        (combined['london_trend'] != 'None')
    ]
    
    # Add additional columns
    # Note: 'date' is the London session date (D+1), but for day_of_week analysis
    # we use the Tokyo session date (D), hence subtracting 1 day
    combined['is_good'] = combined['tokyo_trend'] == combined['london_trend']
    combined['date'] = combined.index  # London session date
    combined['year'] = pd.to_datetime(combined.index).year
    tokyo_dates = pd.to_datetime(combined.index) - timedelta(days=1)
    combined['day_of_week'] = tokyo_dates.dayofweek  # Day of week when Tokyo session occurred
    
    print(f"  Found {len(combined)} valid session pairs")
    
    # Select relevant columns and reset index
    result = combined[[
        'date', 'year', 'day_of_week',
        'tokyo_trend', 'tokyo_distance',
        'london_trend', 'london_distance',
        'is_good', 'tokyo_candles', 'london_candles'
    ]].reset_index(drop=True)
    
    return result


def analyze_timeframe(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Analyze all days for a given timeframe."""
    return analyze_timeframe_vectorized(df, timeframe)


def generate_statistics(results_df: pd.DataFrame) -> Dict:
    """Generate comprehensive statistics from results."""
    if results_df.empty:
        return {}
    
    stats = {}
    
    # Overall statistics
    total_sessions = len(results_df)
    good_sessions = results_df['is_good'].sum()
    bad_sessions = total_sessions - good_sessions
    continuation_rate = (good_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    stats['overall'] = {
        'total': total_sessions,
        'good': good_sessions,
        'bad': bad_sessions,
        'rate': continuation_rate
    }
    
    # Yearly statistics
    yearly_stats = {}
    for year in sorted(results_df['year'].unique()):
        year_data = results_df[results_df['year'] == year]
        total = len(year_data)
        good = year_data['is_good'].sum()
        yearly_stats[year] = {
            'total': total,
            'good': good,
            'bad': total - good,
            'rate': (good / total * 100) if total > 0 else 0
        }
    stats['yearly'] = yearly_stats
    
    # Day of week statistics
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_stats = {}
    for day in range(7):
        day_data = results_df[results_df['day_of_week'] == day]
        total = len(day_data)
        good = day_data['is_good'].sum()
        daily_stats[day_names[day]] = {
            'total': total,
            'good': good,
            'bad': total - good,
            'rate': (good / total * 100) if total > 0 else 0
        }
    stats['daily'] = daily_stats
    
    # Advanced statistics
    stats['advanced'] = {
        'avg_tokyo_distance': results_df['tokyo_distance'].mean(),
        'avg_london_distance': results_df['london_distance'].mean(),
        'std_tokyo_distance': results_df['tokyo_distance'].std(),
        'std_london_distance': results_df['london_distance'].std(),
    }
    
    # Correlation between Tokyo distance and continuation
    # Split Tokyo distances into quartiles and calculate continuation rate for each
    if len(results_df) >= NUM_QUARTILES:
        results_df_copy = results_df.copy()
        try:
            # Try to create quartiles; may fail if too many duplicate values
            results_df_copy['tokyo_quartile'] = pd.qcut(
                results_df_copy['tokyo_distance'], 
                q=NUM_QUARTILES, 
                labels=['Q1 (Weak)', 'Q2', 'Q3', 'Q4 (Strong)'],
                duplicates='drop'
            )
            
            quartile_stats = {}
            # Iterate over available quartiles (may be fewer than 4 if duplicates were dropped)
            available_quartiles = [q for q in results_df_copy['tokyo_quartile'].unique() if pd.notna(q)]
            for quartile in available_quartiles:
                q_data = results_df_copy[results_df_copy['tokyo_quartile'] == quartile]
                total = len(q_data)
                good = q_data['is_good'].sum()
                quartile_stats[str(quartile)] = {
                    'total': total,
                    'good': good,
                    'rate': (good / total * 100) if total > 0 else 0
                }
            if quartile_stats:
                stats['quartiles'] = quartile_stats
        except ValueError:
            # Skip quartile analysis if it fails due to data distribution
            pass
    
    return stats


def generate_markdown_report(all_stats: Dict[str, Dict], output_path: str):
    """Generate the Markdown report."""
    
    lines = []
    lines.append("# Rapport d'Analyse de Continuation Tokyo-Londres")
    lines.append("")
    lines.append(f"**Date de génération:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## Introduction")
    lines.append("")
    lines.append("Cette analyse étudie la continuation de la tendance de la session Tokyo vers la session Londres.")
    lines.append("")
    lines.append("### Définitions des Sessions (Fuseau Horaire Chicago/CT)")
    lines.append("")
    lines.append("| Session | Heures (Chicago Time) |")
    lines.append("|---------|----------------------|")
    lines.append("| **Tokyo** | 19:00 - 00:00 |")
    lines.append("| **Londres** | 02:00 - 06:00 |")
    lines.append("")
    lines.append("### Critères d'Évaluation")
    lines.append("")
    lines.append("- **Session BONNE ✅** : La tendance de Londres continue dans la même direction que Tokyo")
    lines.append("- **Session MAUVAISE ❌** : La tendance de Londres inverse la direction de Tokyo")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Global Summary
    lines.append("## Résumé Global")
    lines.append("")
    lines.append("### Taux de Continuation par Timeframe")
    lines.append("")
    lines.append("| Timeframe | Sessions Analysées | Bonnes Sessions | Mauvaises Sessions | Taux de Continuation |")
    lines.append("|-----------|-------------------|-----------------|-------------------|---------------------|")
    
    for tf in ['1m', '5m', '15m']:
        if tf in all_stats and 'overall' in all_stats[tf]:
            s = all_stats[tf]['overall']
            lines.append(f"| {tf} | {s['total']} | {s['good']} | {s['bad']} | {s['rate']:.2f}% |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Yearly Analysis
    lines.append("## Analyse Annuelle (2018-2025)")
    lines.append("")
    
    for tf in ['1m', '5m', '15m']:
        if tf not in all_stats or 'yearly' not in all_stats[tf]:
            continue
            
        lines.append(f"### Timeframe: {tf}")
        lines.append("")
        lines.append("| Année | Total | Bonnes | Mauvaises | Taux (%) |")
        lines.append("|-------|-------|--------|-----------|----------|")
        
        for year in sorted(all_stats[tf]['yearly'].keys()):
            s = all_stats[tf]['yearly'][year]
            lines.append(f"| {year} | {s['total']} | {s['good']} | {s['bad']} | {s['rate']:.2f}% |")
        
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Day of Week Analysis
    lines.append("## Analyse par Jour de la Semaine")
    lines.append("")
    
    for tf in ['1m', '5m', '15m']:
        if tf not in all_stats or 'daily' not in all_stats[tf]:
            continue
            
        lines.append(f"### Timeframe: {tf}")
        lines.append("")
        lines.append("| Jour | Total | Bonnes | Mauvaises | Taux (%) |")
        lines.append("|------|-------|--------|-----------|----------|")
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_names_fr = {
            'Monday': 'Lundi',
            'Tuesday': 'Mardi',
            'Wednesday': 'Mercredi',
            'Thursday': 'Jeudi',
            'Friday': 'Vendredi',
            'Saturday': 'Samedi',
            'Sunday': 'Dimanche'
        }
        
        for day in day_order:
            if day in all_stats[tf]['daily']:
                s = all_stats[tf]['daily'][day]
                if s['total'] > 0:  # Only show days with data
                    lines.append(f"| {day_names_fr[day]} | {s['total']} | {s['good']} | {s['bad']} | {s['rate']:.2f}% |")
        
        # Best and worst days
        daily = all_stats[tf]['daily']
        valid_days = {k: v for k, v in daily.items() if v['total'] > 0}
        if valid_days:
            best_day = max(valid_days.items(), key=lambda x: x[1]['rate'])
            worst_day = min(valid_days.items(), key=lambda x: x[1]['rate'])
            lines.append("")
            lines.append(f"**Meilleur jour:** {day_names_fr[best_day[0]]} ({best_day[1]['rate']:.2f}%)")
            lines.append(f"**Pire jour:** {day_names_fr[worst_day[0]]} ({worst_day[1]['rate']:.2f}%)")
        
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Advanced Statistics
    lines.append("## Statistiques Avancées")
    lines.append("")
    
    for tf in ['1m', '5m', '15m']:
        if tf not in all_stats or 'advanced' not in all_stats[tf]:
            continue
            
        lines.append(f"### Timeframe: {tf}")
        lines.append("")
        s = all_stats[tf]['advanced']
        lines.append(f"- **Distance moyenne Tokyo:** {s['avg_tokyo_distance']:.4f} points")
        lines.append(f"- **Distance moyenne Londres:** {s['avg_london_distance']:.4f} points")
        lines.append(f"- **Écart-type distance Tokyo:** {s['std_tokyo_distance']:.4f} points")
        lines.append(f"- **Écart-type distance Londres:** {s['std_london_distance']:.4f} points")
        lines.append("")
        
        # Quartile analysis
        if 'quartiles' in all_stats[tf]:
            lines.append("#### Corrélation Force de Tendance Tokyo vs Continuation")
            lines.append("")
            lines.append("| Quartile de Force Tokyo | Sessions | Bonnes | Taux (%) |")
            lines.append("|------------------------|----------|--------|----------|")
            
            for quartile, qs in all_stats[tf]['quartiles'].items():
                lines.append(f"| {quartile} | {qs['total']} | {qs['good']} | {qs['rate']:.2f}% |")
            
            lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Summary Tables
    lines.append("## Tableaux Récapitulatifs")
    lines.append("")
    
    # Comparative table by timeframe
    lines.append("### Comparaison des Timeframes")
    lines.append("")
    lines.append("| Métrique | 1m | 5m | 15m |")
    lines.append("|----------|-----|-----|------|")
    
    metrics = ['total', 'good', 'bad', 'rate']
    metric_names = {
        'total': 'Sessions totales',
        'good': 'Bonnes sessions',
        'bad': 'Mauvaises sessions',
        'rate': 'Taux de continuation (%)'
    }
    
    for metric in metrics:
        row = f"| {metric_names[metric]} |"
        for tf in ['1m', '5m', '15m']:
            if tf in all_stats and 'overall' in all_stats[tf]:
                value = all_stats[tf]['overall'][metric]
                if metric == 'rate':
                    row += f" {value:.2f}% |"
                else:
                    row += f" {value} |"
            else:
                row += " N/A |"
        lines.append(row)
    
    lines.append("")
    
    # Year by year comprehensive table
    lines.append("### Récapitulatif Année par Année (Taux de Continuation %)")
    lines.append("")
    lines.append("| Année | 1m | 5m | 15m |")
    lines.append("|-------|-----|-----|------|")
    
    years = set()
    for tf in all_stats:
        if 'yearly' in all_stats[tf]:
            years.update(all_stats[tf]['yearly'].keys())
    
    for year in sorted(years):
        row = f"| {year} |"
        for tf in ['1m', '5m', '15m']:
            if tf in all_stats and 'yearly' in all_stats[tf] and year in all_stats[tf]['yearly']:
                rate = all_stats[tf]['yearly'][year]['rate']
                row += f" {rate:.2f}% |"
            else:
                row += " N/A |"
        lines.append(row)
    
    lines.append("")
    
    # Day by day comprehensive table
    lines.append("### Récapitulatif Jour par Jour (Taux de Continuation %)")
    lines.append("")
    lines.append("| Jour | 1m | 5m | 15m |")
    lines.append("|------|-----|-----|------|")
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_names_fr = {
        'Monday': 'Lundi',
        'Tuesday': 'Mardi',
        'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi',
        'Friday': 'Vendredi',
        'Saturday': 'Samedi',
        'Sunday': 'Dimanche'
    }
    
    for day in day_order:
        # Check if any timeframe has data for this day
        has_data = False
        for tf in all_stats:
            if 'daily' in all_stats[tf] and day in all_stats[tf]['daily']:
                if all_stats[tf]['daily'][day]['total'] > 0:
                    has_data = True
                    break
        
        if not has_data:
            continue
            
        row = f"| {day_names_fr[day]} |"
        for tf in ['1m', '5m', '15m']:
            if tf in all_stats and 'daily' in all_stats[tf] and day in all_stats[tf]['daily']:
                s = all_stats[tf]['daily'][day]
                if s['total'] > 0:
                    row += f" {s['rate']:.2f}% |"
                else:
                    row += " N/A |"
            else:
                row += " N/A |"
        lines.append(row)
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Conclusion")
    lines.append("")
    lines.append("Cette analyse fournit une vue d'ensemble complète de la tendance de continuation entre les sessions Tokyo et Londres.")
    lines.append("Les données peuvent être utilisées pour améliorer les stratégies de trading basées sur la continuation inter-sessions.")
    lines.append("")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Report generated: {output_path}")


def main():
    """Main function to run the analysis."""
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    data_dir = str(script_dir)
    
    print("=" * 60)
    print("Tokyo-London Continuation Analysis")
    print("=" * 60)
    print()
    
    # Define analysis parameters
    start_year = 2018
    end_year = datetime.now().year  # Dynamically use current year
    years = list(range(start_year, end_year + 1))
    timeframes = ['1m', '5m', '15m']
    
    all_stats = {}
    all_results = {}
    
    for tf in timeframes:
        print(f"\nProcessing {tf} timeframe...")
        print("-" * 40)
        
        # Load data
        df = load_data(data_dir, tf, years)
        
        if df.empty:
            print(f"  No data found for {tf}")
            continue
        
        print(f"  Total rows loaded: {len(df)}")
        
        # Analyze
        results = analyze_timeframe(df, tf)
        
        if results.empty:
            print(f"  No valid sessions found for {tf}")
            continue
        
        print(f"  Sessions analyzed: {len(results)}")
        
        # Generate statistics
        stats = generate_statistics(results)
        
        all_stats[tf] = stats
        all_results[tf] = results
        
        # Print summary
        if 'overall' in stats:
            print(f"  Continuation rate: {stats['overall']['rate']:.2f}%")
    
    print()
    print("=" * 60)
    print("Generating Report...")
    print("=" * 60)
    
    # Generate Markdown report
    report_path = os.path.join(data_dir, "rapport_continuation_tokyo_londres.md")
    generate_markdown_report(all_stats, report_path)
    
    print()
    print("Analysis complete!")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
