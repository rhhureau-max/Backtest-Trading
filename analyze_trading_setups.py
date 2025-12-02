#!/usr/bin/env python3
"""
Trading Setup Pattern Analyzer with Risk/Reward Analysis

This script analyzes trading data from 2018 to today for specific setup patterns:
1. Bearish Setup: 8:30 AM candle is bearish, next candle is bullish and closes above max of last 5 candles
2. Bullish Setup: 8:30 AM candle is bullish, next candle is bearish and closes below min of last 5 candles

Data analyzed: 1-minute, 5-minute, and 15-minute timeframes

Extended with comprehensive Risk/Reward analysis:
- 4 Stop-Loss placements: 100%, 75%, 50%, 25% body retracement
- 9 RR ratios: 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0
- Performance metrics: Win rate, P/L, Expectancy, etc.
"""

import pandas as pd
import zipfile
import os
from datetime import datetime, time
from typing import List, Dict, Tuple, Optional
import io

class TradingSetupAnalyzer:
    def __init__(self, base_path: str, start_year: int = 2018, end_year: int = 2025):
        self.base_path = base_path
        self.years = list(range(start_year, end_year + 1))
        self.timeframes = ['1m', '5m', '15m']
        self.results = {tf: {'bearish_setups': [], 'bullish_setups': []} for tf in self.timeframes}
        
        # Risk/Reward analysis parameters
        self.sl_placements = {
            '100%': 1.00,  # Full body retracement
            '75%': 0.75,   # 75% body retracement
            '50%': 0.50,   # 50% body retracement
            '25%': 0.25    # 25% body retracement
        }
        self.rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        self.rr_results = {}
        
        # Trade simulation parameters
        self.MAX_CANDLES_TO_CHECK = 500  # Maximum candles to check after entry for TP/SL
        self.ENTRY_CANDLE_OFFSET = 2  # Start checking 2 candles after setup (setup_index + 2)
        
    def load_data(self, year: int, timeframe: str) -> pd.DataFrame:
        """Load data for a specific year and timeframe"""
        filename = f"{year} {timeframe}.csv"
        filepath = os.path.join(self.base_path, filename)
        
        # For 1m data from 2018-2024, read from zip files
        if timeframe == '1m' and year < 2025:
            zip_filename = f"{year} {timeframe}.csv.zip"
            zip_filepath = os.path.join(self.base_path, zip_filename)
            
            if not os.path.exists(zip_filepath):
                print(f"Warning: {zip_filename} not found")
                return pd.DataFrame()
            
            try:
                with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                    # Get the name of the CSV file inside the zip
                    csv_filename = zip_ref.namelist()[0]
                    with zip_ref.open(csv_filename) as csv_file:
                        df = pd.read_csv(csv_file, sep=';', header=0)
            except Exception as e:
                print(f"Error reading {zip_filename}: {e}")
                return pd.DataFrame()
        else:
            # For other files, read directly
            if not os.path.exists(filepath):
                print(f"Warning: {filename} not found")
                return pd.DataFrame()
            
            try:
                df = pd.read_csv(filepath, sep=';', header=0)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                return pd.DataFrame()
        
        # Rename columns for easier access
        df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        # Parse datetime
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
        df['TimeOnly'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
        
        # Convert price columns to float
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def is_bearish_candle(self, row: pd.Series) -> bool:
        """Check if a candle is bearish (Close < Open)"""
        return row['Close'] < row['Open']
    
    def is_bullish_candle(self, row: pd.Series) -> bool:
        """Check if a candle is bullish (Close > Open)"""
        return row['Close'] > row['Open']
    
    def find_setups(self, df: pd.DataFrame, timeframe: str) -> Tuple[List[Dict], List[Dict]]:
        """
        Find both setup patterns in the data
        
        Returns:
            Tuple of (bearish_setups, bullish_setups)
        """
        bearish_setups = []
        bullish_setups = []
        
        if len(df) < 7:  # Need at least 7 candles (5 previous + 8:30 + next)
            return bearish_setups, bullish_setups
        
        # Define 8:30 AM time
        target_time = time(8, 30, 0)
        
        # Iterate through the dataframe
        for i in range(5, len(df) - 1):  # Need 5 previous candles and 1 next candle
            current_row = df.iloc[i]
            next_row = df.iloc[i + 1]
            
            # Check if current candle is at 8:30 AM
            if current_row['TimeOnly'] != target_time:
                continue
            
            # Get the last 5 candles before 8:30 AM
            prev_5_candles = df.iloc[i-5:i]
            max_of_last_5 = prev_5_candles['High'].max()
            min_of_last_5 = prev_5_candles['Low'].min()
            
            # BEARISH SETUP: 8:30 bearish, next bullish and closes above max of last 5
            if self.is_bearish_candle(current_row) and self.is_bullish_candle(next_row):
                if next_row['Close'] > max_of_last_5:
                    setup = {
                        'date': current_row['Date'],
                        'time_830': current_row['Time'],
                        'time_next': next_row['Time'],
                        'open_830': current_row['Open'],
                        'high_830': current_row['High'],
                        'low_830': current_row['Low'],
                        'close_830': current_row['Close'],
                        'open_next': next_row['Open'],
                        'high_next': next_row['High'],
                        'low_next': next_row['Low'],
                        'close_next': next_row['Close'],
                        'max_last_5': max_of_last_5,
                        'min_last_5': min_of_last_5,
                        'close_above_max_by': next_row['Close'] - max_of_last_5,
                        'timeframe': timeframe
                    }
                    bearish_setups.append(setup)
            
            # BULLISH SETUP: 8:30 bullish, next bearish and closes below min of last 5
            if self.is_bullish_candle(current_row) and self.is_bearish_candle(next_row):
                if next_row['Close'] < min_of_last_5:
                    setup = {
                        'date': current_row['Date'],
                        'time_830': current_row['Time'],
                        'time_next': next_row['Time'],
                        'open_830': current_row['Open'],
                        'high_830': current_row['High'],
                        'low_830': current_row['Low'],
                        'close_830': current_row['Close'],
                        'open_next': next_row['Open'],
                        'high_next': next_row['High'],
                        'low_next': next_row['Low'],
                        'close_next': next_row['Close'],
                        'max_last_5': max_of_last_5,
                        'min_last_5': min_of_last_5,
                        'close_below_min_by': min_of_last_5 - next_row['Close'],
                        'timeframe': timeframe
                    }
                    bullish_setups.append(setup)
        
        return bearish_setups, bullish_setups
    
    def format_profit_factor(self, pf: Optional[float], width: int = 8) -> str:
        """
        Format profit factor for display, handling None (undefined) case
        
        Args:
            pf: Profit factor value or None if undefined
            width: Field width for formatting
        
        Returns:
            Formatted string
        """
        if pf is None:
            return "N/A".ljust(width)
        return f"{pf:<{width}.2f}"
    
    def extract_year_from_date(self, date_str: str) -> int:
        """
        Extract year from date string in DD/MM/YYYY format
        
        Args:
            date_str: Date string in format DD/MM/YYYY
        
        Returns:
            Year as integer
        """
        date_parts = date_str.split('/')
        return int(date_parts[2])
    
    def calculate_sl_level(self, setup: Dict, sl_placement: float, setup_type: str) -> float:
        """
        Calculate Stop-Loss level based on 8:30 AM candle body retracement
        
        Args:
            setup: Setup dictionary with OHLC data
            sl_placement: Percentage of body retracement (0.25, 0.50, 0.75, 1.00)
            setup_type: 'bearish' or 'bullish'
        
        Returns:
            Stop-Loss price level
        """
        open_830 = setup['open_830']
        close_830 = setup['close_830']
        
        if setup_type == 'bearish':
            # For bearish setup (8:30 bearish, going LONG on breakout)
            # SL is at: Close + (sl_placement * body_size)
            # 100% = Open (top of bearish candle)
            body_size = open_830 - close_830
            sl = close_830 + (sl_placement * body_size)
        else:  # bullish setup
            # For bullish setup (8:30 bullish, going SHORT on breakdown)
            # SL is at: Close - (sl_placement * body_size)
            # 100% = Open (bottom of bullish candle)
            body_size = close_830 - open_830
            sl = close_830 - (sl_placement * body_size)
        
        return sl
    
    def calculate_tp_level(self, entry: float, sl: float, rr_ratio: float, setup_type: str) -> float:
        """
        Calculate Take-Profit level based on entry, stop-loss, and RR ratio
        
        Args:
            entry: Entry price
            sl: Stop-Loss price
            rr_ratio: Risk/Reward ratio
            setup_type: 'bearish' or 'bullish'
        
        Returns:
            Take-Profit price level
        """
        risk = abs(entry - sl)
        reward = rr_ratio * risk
        
        if setup_type == 'bearish':
            # Going LONG
            tp = entry + reward
        else:  # bullish setup
            # Going SHORT
            tp = entry - reward
        
        return tp
    
    def simulate_trade(self, setup: Dict, df: pd.DataFrame, entry: float, sl: float, 
                       tp: float, setup_type: str, setup_index: int) -> Dict:
        """
        Simulate trade execution by checking subsequent price action
        
        Args:
            setup: Setup dictionary
            df: DataFrame with all price data
            entry: Entry price
            sl: Stop-Loss price
            tp: Take-Profit price
            setup_type: 'bearish' or 'bullish'
            setup_index: Index in DataFrame where setup occurred
        
        Returns:
            Trade result dictionary
        """
        hit_tp = False
        hit_sl = False
        exit_price = None
        exit_candle_index = None
        bars_in_trade = 0
        
        # Start checking from ENTRY_CANDLE_OFFSET candles after setup
        # setup_index points to the entry candle (next candle after 8:30)
        # We add 2 to skip: [0] = entry candle itself, [1] = first candle after entry
        # So we start checking from the second candle after entry
        start_index = setup_index + self.ENTRY_CANDLE_OFFSET
        end_index = min(start_index + self.MAX_CANDLES_TO_CHECK, len(df))
        
        for i in range(start_index, end_index):
            candle = df.iloc[i]
            bars_in_trade += 1
            
            if setup_type == 'bearish':
                # Long trade: Check if TP (above) or SL (below) was hit
                # Check SL first (more conservative)
                if candle['Low'] <= sl:
                    hit_sl = True
                    exit_price = sl
                    exit_candle_index = i
                    break
                elif candle['High'] >= tp:
                    hit_tp = True
                    exit_price = tp
                    exit_candle_index = i
                    break
            else:  # bullish setup
                # Short trade: Check if TP (below) or SL (above) was hit
                # Check SL first (more conservative)
                if candle['High'] >= sl:
                    hit_sl = True
                    exit_price = sl
                    exit_candle_index = i
                    break
                elif candle['Low'] <= tp:
                    hit_tp = True
                    exit_price = tp
                    exit_candle_index = i
                    break
        
        # Calculate P/L
        if exit_price:
            if setup_type == 'bearish':
                pl = exit_price - entry
            else:
                pl = entry - exit_price
        else:
            # Trade didn't close within observation period - mark as unknown
            # Use None to distinguish from actual zero P/L
            pl = None
            hit_sl = None  # Unknown outcome
            hit_tp = None
        
        return {
            'hit_tp': hit_tp,
            'hit_sl': hit_sl,
            'exit_price': exit_price,
            'pl_points': pl,
            'bars_in_trade': bars_in_trade,
            'exit_candle_index': exit_candle_index
        }
    
    def analyze_rr_for_setup(self, setup: Dict, df: pd.DataFrame, setup_index: int, 
                             setup_type: str) -> Dict:
        """
        Analyze all RR combinations for a single setup
        
        Args:
            setup: Setup dictionary
            df: DataFrame with price data
            setup_index: Index where setup occurred
            setup_type: 'bearish' or 'bullish'
        
        Returns:
            Dictionary with results for all SL/RR combinations
        """
        entry = setup['close_next']  # Entry at close of next candle
        results = {}
        
        for sl_name, sl_pct in self.sl_placements.items():
            sl_level = self.calculate_sl_level(setup, sl_pct, setup_type)
            results[sl_name] = {}
            
            for rr_ratio in self.rr_ratios:
                tp_level = self.calculate_tp_level(entry, sl_level, rr_ratio, setup_type)
                
                trade_result = self.simulate_trade(
                    setup, df, entry, sl_level, tp_level, 
                    setup_type, setup_index
                )
                
                results[sl_name][rr_ratio] = {
                    'entry': entry,
                    'sl': sl_level,
                    'tp': tp_level,
                    'result': trade_result
                }
        
        return results
    
    def analyze_all_rr_combinations(self):
        """
        Analyze Risk/Reward for all identified setups across all timeframes
        Optimized to load each data file only once
        """
        print("\n" + "=" * 80)
        print("RISK/REWARD ANALYSIS")
        print("=" * 80)
        print(f"SL Placements: {', '.join(self.sl_placements.keys())}")
        print(f"RR Ratios: {', '.join(map(str, self.rr_ratios))}")
        print("=" * 80)
        print()
        
        for timeframe in self.timeframes:
            print(f"\nAnalyzing {timeframe} setups...")
            
            # Initialize results structure for this timeframe
            if timeframe not in self.rr_results:
                self.rr_results[timeframe] = {
                    'bearish': [],
                    'bullish': []
                }
            
            # Load data once per year and process all setups from that year
            for year in self.years:
                print(f"  Loading {year} data...", end=" ")
                df = self.load_data(year, timeframe)
                if df.empty:
                    print("SKIPPED")
                    continue
                
                # Process bearish setups from this year
                bearish_count = 0
                bullish_count = 0
                
                bearish_setups = self.results[timeframe]['bearish_setups']
                for setup in bearish_setups:
                    # Check if this setup is from current year
                    setup_date = setup['date']
                    setup_year = self.extract_year_from_date(setup_date)
                    
                    if setup_year != year:
                        continue
                    
                    setup_time = setup['time_next']
                    
                    # Match by date and time
                    mask = (df['Date'] == setup_date) & (df['Time'] == setup_time)
                    matching_indices = df.index[mask].tolist()
                    
                    if matching_indices:
                        setup_index = matching_indices[0]
                        rr_analysis = self.analyze_rr_for_setup(
                            setup, df, setup_index, 'bearish'
                        )
                        
                        self.rr_results[timeframe]['bearish'].append({
                            'setup': setup,
                            'rr_analysis': rr_analysis
                        })
                        bearish_count += 1
                
                # Process bullish setups from this year
                bullish_setups = self.results[timeframe]['bullish_setups']
                for setup in bullish_setups:
                    # Check if this setup is from current year
                    setup_date = setup['date']
                    setup_year = self.extract_year_from_date(setup_date)
                    
                    if setup_year != year:
                        continue
                    
                    setup_time = setup['time_next']
                    
                    # Match by date and time
                    mask = (df['Date'] == setup_date) & (df['Time'] == setup_time)
                    matching_indices = df.index[mask].tolist()
                    
                    if matching_indices:
                        setup_index = matching_indices[0]
                        rr_analysis = self.analyze_rr_for_setup(
                            setup, df, setup_index, 'bullish'
                        )
                        
                        self.rr_results[timeframe]['bullish'].append({
                            'setup': setup,
                            'rr_analysis': rr_analysis
                        })
                        bullish_count += 1
                
                print(f"✓ (B:{bearish_count}, Bu:{bullish_count})")
            
            print(f"  Total analyzed: Bearish={len(self.rr_results[timeframe]['bearish'])}, " 
                  f"Bullish={len(self.rr_results[timeframe]['bullish'])}")
        
        print("\nRisk/Reward analysis complete!")
    
    def calculate_performance_metrics(self, results_list: List[Dict], 
                                     sl_name: str, rr_ratio: float) -> Dict:
        """
        Calculate performance metrics for a specific SL placement and RR ratio
        
        Args:
            results_list: List of setup results with RR analysis
            sl_name: Stop-Loss placement name
            rr_ratio: Risk/Reward ratio
        
        Returns:
            Dictionary with performance metrics
        """
        winners = []
        losers = []
        unknown = []
        
        for item in results_list:
            rr_analysis = item['rr_analysis']
            if sl_name in rr_analysis and rr_ratio in rr_analysis[sl_name]:
                trade_data = rr_analysis[sl_name][rr_ratio]
                result = trade_data['result']
                
                if result['hit_tp'] is True:
                    winners.append(result['pl_points'])
                elif result['hit_sl'] is True:
                    losers.append(result['pl_points'])
                else:
                    unknown.append(result)
        
        total_trades = len(winners) + len(losers)
        
        if total_trades == 0:
            return {
                'total_trades': 0,
                'winners': 0,
                'losers': 0,
                'unknown': len(unknown),
                'win_rate': 0.0,
                'total_pl': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'expectancy': 0.0,
                'profit_factor': 0.0
            }
        
        win_rate = len(winners) / total_trades * 100
        total_pl = sum(winners) + sum(losers)
        avg_win = sum(winners) / len(winners) if winners else 0.0
        avg_loss = sum(losers) / len(losers) if losers else 0.0
        
        # Expectancy = (Win% × Avg Win) - (Loss% × |Avg Loss|)
        expectancy = (len(winners) / total_trades * avg_win) - \
                     (len(losers) / total_trades * abs(avg_loss))
        
        # Profit Factor = Gross Profit / Gross Loss
        gross_profit = sum(winners) if winners else 0.0
        gross_loss = abs(sum(losers)) if losers else 0.0
        # Use None for undefined profit factor (no losses) rather than infinity
        # This makes it easier to handle in comparisons and display
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else None
        
        return {
            'total_trades': total_trades,
            'winners': len(winners),
            'losers': len(losers),
            'unknown': len(unknown),
            'win_rate': win_rate,
            'total_pl': total_pl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'expectancy': expectancy,
            'profit_factor': profit_factor
        }
    
    def analyze_all_data(self):
        """Analyze all years and timeframes"""
        print("=" * 80)
        print("TRADING SETUP PATTERN ANALYZER")
        print("=" * 80)
        print(f"Analysis Period: 2018-2025")
        print(f"Timeframes: {', '.join(self.timeframes)}")
        print("=" * 80)
        print()
        
        for timeframe in self.timeframes:
            print(f"\nProcessing {timeframe} data...")
            
            for year in self.years:
                print(f"  Loading {year}...", end=" ")
                df = self.load_data(year, timeframe)
                
                if df.empty:
                    print("SKIPPED (no data)")
                    continue
                
                bearish, bullish = self.find_setups(df, timeframe)
                self.results[timeframe]['bearish_setups'].extend(bearish)
                self.results[timeframe]['bullish_setups'].extend(bullish)
                
                print(f"✓ (Bearish: {len(bearish)}, Bullish: {len(bullish)})")
        
        print("\nAnalysis complete!")
    
    def generate_report(self, output_file: str = "trading_setup_report.txt"):
        """Generate a detailed report of the findings"""
        report_lines = []
        
        # Header
        report_lines.append("=" * 100)
        report_lines.append("TRADING SETUP PATTERN ANALYSIS REPORT")
        report_lines.append("=" * 100)
        report_lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Analysis Period: 2018 - 2025")
        report_lines.append("")
        
        # Setup Definitions
        report_lines.append("SETUP DEFINITIONS:")
        report_lines.append("-" * 100)
        report_lines.append("1. BEARISH SETUP:")
        report_lines.append("   - 8:30 AM candle is BEARISH (Close < Open)")
        report_lines.append("   - Next candle is BULLISH (Close > Open)")
        report_lines.append("   - Next candle closes ABOVE the maximum of the last 5 candles")
        report_lines.append("")
        report_lines.append("2. BULLISH SETUP:")
        report_lines.append("   - 8:30 AM candle is BULLISH (Close > Open)")
        report_lines.append("   - Next candle is BEARISH (Close < Open)")
        report_lines.append("   - Next candle closes BELOW the minimum of the last 5 candles")
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append("")
        
        # Summary Statistics
        report_lines.append("SUMMARY STATISTICS")
        report_lines.append("=" * 100)
        report_lines.append("")
        
        total_bearish = 0
        total_bullish = 0
        
        for timeframe in self.timeframes:
            bearish_count = len(self.results[timeframe]['bearish_setups'])
            bullish_count = len(self.results[timeframe]['bullish_setups'])
            total_bearish += bearish_count
            total_bullish += bullish_count
            
            report_lines.append(f"{timeframe.upper()} Timeframe:")
            report_lines.append(f"  Bearish Setups: {bearish_count}")
            report_lines.append(f"  Bullish Setups: {bullish_count}")
            report_lines.append(f"  Total Setups:   {bearish_count + bullish_count}")
            report_lines.append("")
        
        report_lines.append("-" * 100)
        report_lines.append(f"GRAND TOTAL:")
        report_lines.append(f"  Total Bearish Setups: {total_bearish}")
        report_lines.append(f"  Total Bullish Setups: {total_bullish}")
        report_lines.append(f"  Total All Setups:     {total_bearish + total_bullish}")
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append("")
        
        # Detailed Setup Information
        for timeframe in self.timeframes:
            report_lines.append("")
            report_lines.append("=" * 100)
            report_lines.append(f"DETAILED SETUPS - {timeframe.upper()} TIMEFRAME")
            report_lines.append("=" * 100)
            report_lines.append("")
            
            # Bearish Setups
            bearish_setups = self.results[timeframe]['bearish_setups']
            report_lines.append(f"BEARISH SETUPS ({len(bearish_setups)} found)")
            report_lines.append("-" * 100)
            
            if bearish_setups:
                for idx, setup in enumerate(bearish_setups, 1):
                    report_lines.append(f"\n#{idx}. Date: {setup['date']}")
                    report_lines.append(f"    8:30 AM Candle (Bearish):")
                    report_lines.append(f"      Time: {setup['time_830']}")
                    report_lines.append(f"      Open:  {setup['open_830']:.2f}")
                    report_lines.append(f"      High:  {setup['high_830']:.2f}")
                    report_lines.append(f"      Low:   {setup['low_830']:.2f}")
                    report_lines.append(f"      Close: {setup['close_830']:.2f}")
                    report_lines.append(f"    Next Candle (Bullish):")
                    report_lines.append(f"      Time: {setup['time_next']}")
                    report_lines.append(f"      Open:  {setup['open_next']:.2f}")
                    report_lines.append(f"      High:  {setup['high_next']:.2f}")
                    report_lines.append(f"      Low:   {setup['low_next']:.2f}")
                    report_lines.append(f"      Close: {setup['close_next']:.2f}")
                    report_lines.append(f"    Key Levels:")
                    report_lines.append(f"      Max of Last 5 Candles: {setup['max_last_5']:.2f}")
                    report_lines.append(f"      Close Above Max By:    {setup['close_above_max_by']:.2f}")
            else:
                report_lines.append("  No bearish setups found.")
            
            report_lines.append("")
            report_lines.append("-" * 100)
            
            # Bullish Setups
            bullish_setups = self.results[timeframe]['bullish_setups']
            report_lines.append(f"\nBULLISH SETUPS ({len(bullish_setups)} found)")
            report_lines.append("-" * 100)
            
            if bullish_setups:
                for idx, setup in enumerate(bullish_setups, 1):
                    report_lines.append(f"\n#{idx}. Date: {setup['date']}")
                    report_lines.append(f"    8:30 AM Candle (Bullish):")
                    report_lines.append(f"      Time: {setup['time_830']}")
                    report_lines.append(f"      Open:  {setup['open_830']:.2f}")
                    report_lines.append(f"      High:  {setup['high_830']:.2f}")
                    report_lines.append(f"      Low:   {setup['low_830']:.2f}")
                    report_lines.append(f"      Close: {setup['close_830']:.2f}")
                    report_lines.append(f"    Next Candle (Bearish):")
                    report_lines.append(f"      Time: {setup['time_next']}")
                    report_lines.append(f"      Open:  {setup['open_next']:.2f}")
                    report_lines.append(f"      High:  {setup['high_next']:.2f}")
                    report_lines.append(f"      Low:   {setup['low_next']:.2f}")
                    report_lines.append(f"      Close: {setup['close_next']:.2f}")
                    report_lines.append(f"    Key Levels:")
                    report_lines.append(f"      Min of Last 5 Candles: {setup['min_last_5']:.2f}")
                    report_lines.append(f"      Close Below Min By:    {setup['close_below_min_by']:.2f}")
            else:
                report_lines.append("  No bullish setups found.")
            
            report_lines.append("")
        
        # Additional Statistics
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append("ADDITIONAL STATISTICS")
        report_lines.append("=" * 100)
        report_lines.append("")
        
        for timeframe in self.timeframes:
            report_lines.append(f"{timeframe.upper()} Timeframe Analysis:")
            
            bearish_setups = self.results[timeframe]['bearish_setups']
            bullish_setups = self.results[timeframe]['bullish_setups']
            
            if bearish_setups:
                avg_break = sum(s['close_above_max_by'] for s in bearish_setups) / len(bearish_setups)
                max_break = max(s['close_above_max_by'] for s in bearish_setups)
                min_break = min(s['close_above_max_by'] for s in bearish_setups)
                
                report_lines.append(f"  Bearish Setup Statistics:")
                report_lines.append(f"    Average breakout above max: {avg_break:.2f}")
                report_lines.append(f"    Maximum breakout above max: {max_break:.2f}")
                report_lines.append(f"    Minimum breakout above max: {min_break:.2f}")
            
            if bullish_setups:
                avg_break = sum(s['close_below_min_by'] for s in bullish_setups) / len(bullish_setups)
                max_break = max(s['close_below_min_by'] for s in bullish_setups)
                min_break = min(s['close_below_min_by'] for s in bullish_setups)
                
                report_lines.append(f"  Bullish Setup Statistics:")
                report_lines.append(f"    Average breakout below min: {avg_break:.2f}")
                report_lines.append(f"    Maximum breakout below min: {max_break:.2f}")
                report_lines.append(f"    Minimum breakout below min: {min_break:.2f}")
            
            report_lines.append("")
        
        report_lines.append("=" * 100)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 100)
        
        # Write to file
        report_content = "\n".join(report_lines)
        output_path = os.path.join(self.base_path, output_file)
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        print(f"\nReport saved to: {output_path}")
        print(f"Report size: {len(report_content)} bytes")
        print("\nTo view the full report, run: cat {0}".format(output_path))
        
        return output_path
    
    def generate_rr_report(self, output_file: str = "rr_analysis_report.txt"):
        """Generate comprehensive Risk/Reward analysis report"""
        report_lines = []
        
        # Header
        report_lines.append("=" * 120)
        report_lines.append("RISK/REWARD ANALYSIS REPORT")
        report_lines.append("=" * 120)
        report_lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Analysis Period: 2018 - 2025")
        report_lines.append("")
        
        # Analysis Parameters
        report_lines.append("ANALYSIS PARAMETERS:")
        report_lines.append("-" * 120)
        report_lines.append("Stop-Loss Placements (based on 8:30 AM candle body):")
        report_lines.append("  - 100%: Full body retracement (SL at Open)")
        report_lines.append("  - 75%:  75% body retracement")
        report_lines.append("  - 50%:  50% body retracement (middle of body)")
        report_lines.append("  - 25%:  25% body retracement (close SL)")
        report_lines.append("")
        report_lines.append(f"Risk/Reward Ratios: {', '.join(map(str, self.rr_ratios))}")
        report_lines.append("")
        report_lines.append("Entry: Close of breakout/breakdown candle")
        report_lines.append("Trade Direction:")
        report_lines.append("  - Bearish Setup: LONG (buy on breakout above resistance)")
        report_lines.append("  - Bullish Setup: SHORT (sell on breakdown below support)")
        report_lines.append("")
        report_lines.append("=" * 120)
        report_lines.append("")
        
        # Summary for each timeframe
        for timeframe in self.timeframes:
            report_lines.append("")
            report_lines.append("=" * 120)
            report_lines.append(f"{timeframe.upper()} TIMEFRAME ANALYSIS")
            report_lines.append("=" * 120)
            report_lines.append("")
            
            # Bearish Setups (LONG trades)
            report_lines.append("-" * 120)
            report_lines.append(f"BEARISH SETUPS (LONG TRADES) - {len(self.rr_results[timeframe]['bearish'])} setups")
            report_lines.append("-" * 120)
            report_lines.append("")
            
            for sl_name in ['100%', '75%', '50%', '25%']:
                report_lines.append(f"\nStop-Loss Placement: {sl_name} Body Retracement")
                report_lines.append("-" * 120)
                
                # Table header
                header = f"{'RR Ratio':<10} {'Trades':<8} {'Winners':<9} {'Losers':<8} {'Unknown':<9} " \
                        f"{'Win Rate':<10} {'Total P/L':<12} {'Avg Win':<10} {'Avg Loss':<11} " \
                        f"{'Expectancy':<12} {'PF':<8}"
                report_lines.append(header)
                report_lines.append("-" * 120)
                
                for rr_ratio in self.rr_ratios:
                    metrics = self.calculate_performance_metrics(
                        self.rr_results[timeframe]['bearish'],
                        sl_name,
                        rr_ratio
                    )
                    
                    line = f"{rr_ratio:<10.1f} {metrics['total_trades']:<8} " \
                           f"{metrics['winners']:<9} {metrics['losers']:<8} {metrics['unknown']:<9} " \
                           f"{metrics['win_rate']:<10.2f} {metrics['total_pl']:<12.2f} " \
                           f"{metrics['avg_win']:<10.2f} {metrics['avg_loss']:<11.2f} " \
                           f"{metrics['expectancy']:<12.2f} " \
                           f"{self.format_profit_factor(metrics['profit_factor'])}"
                    
                    report_lines.append(line)
                
                report_lines.append("")
            
            # Bullish Setups (SHORT trades)
            report_lines.append("")
            report_lines.append("-" * 120)
            report_lines.append(f"BULLISH SETUPS (SHORT TRADES) - {len(self.rr_results[timeframe]['bullish'])} setups")
            report_lines.append("-" * 120)
            report_lines.append("")
            
            for sl_name in ['100%', '75%', '50%', '25%']:
                report_lines.append(f"\nStop-Loss Placement: {sl_name} Body Retracement")
                report_lines.append("-" * 120)
                
                # Table header
                header = f"{'RR Ratio':<10} {'Trades':<8} {'Winners':<9} {'Losers':<8} {'Unknown':<9} " \
                        f"{'Win Rate':<10} {'Total P/L':<12} {'Avg Win':<10} {'Avg Loss':<11} " \
                        f"{'Expectancy':<12} {'PF':<8}"
                report_lines.append(header)
                report_lines.append("-" * 120)
                
                for rr_ratio in self.rr_ratios:
                    metrics = self.calculate_performance_metrics(
                        self.rr_results[timeframe]['bullish'],
                        sl_name,
                        rr_ratio
                    )
                    
                    line = f"{rr_ratio:<10.1f} {metrics['total_trades']:<8} " \
                           f"{metrics['winners']:<9} {metrics['losers']:<8} {metrics['unknown']:<9} " \
                           f"{metrics['win_rate']:<10.2f} {metrics['total_pl']:<12.2f} " \
                           f"{metrics['avg_win']:<10.2f} {metrics['avg_loss']:<11.2f} " \
                           f"{metrics['expectancy']:<12.2f} " \
                           f"{self.format_profit_factor(metrics['profit_factor'])}"
                    
                    report_lines.append(line)
                
                report_lines.append("")
        
        # Best Performing Combinations
        report_lines.append("")
        report_lines.append("=" * 120)
        report_lines.append("BEST PERFORMING COMBINATIONS")
        report_lines.append("=" * 120)
        report_lines.append("")
        
        all_combinations = []
        
        for timeframe in self.timeframes:
            for setup_type in ['bearish', 'bullish']:
                for sl_name in ['100%', '75%', '50%', '25%']:
                    for rr_ratio in self.rr_ratios:
                        metrics = self.calculate_performance_metrics(
                            self.rr_results[timeframe][setup_type],
                            sl_name,
                            rr_ratio
                        )
                        
                        if metrics['total_trades'] >= 10:  # Only consider combinations with at least 10 trades
                            all_combinations.append({
                                'timeframe': timeframe,
                                'setup_type': setup_type,
                                'sl_placement': sl_name,
                                'rr_ratio': rr_ratio,
                                'metrics': metrics
                            })
        
        # Sort by expectancy
        sorted_by_expectancy = sorted(all_combinations, 
                                      key=lambda x: x['metrics']['expectancy'], 
                                      reverse=True)[:10]
        
        report_lines.append("TOP 10 BY EXPECTANCY (min 10 trades):")
        report_lines.append("-" * 120)
        header = f"{'Rank':<6} {'Timeframe':<12} {'Setup Type':<13} {'SL':<8} {'RR':<6} " \
                f"{'Trades':<8} {'Win%':<8} {'Expectancy':<12} {'Total P/L':<12} {'PF':<8}"
        report_lines.append(header)
        report_lines.append("-" * 120)
        
        for rank, combo in enumerate(sorted_by_expectancy, 1):
            line = f"{rank:<6} {combo['timeframe'].upper():<12} " \
                   f"{combo['setup_type'].capitalize():<13} {combo['sl_placement']:<8} " \
                   f"{combo['rr_ratio']:<6.1f} {combo['metrics']['total_trades']:<8} " \
                   f"{combo['metrics']['win_rate']:<8.2f} {combo['metrics']['expectancy']:<12.2f} " \
                   f"{combo['metrics']['total_pl']:<12.2f} " \
                   f"{self.format_profit_factor(combo['metrics']['profit_factor'])}"
            report_lines.append(line)
        
        report_lines.append("")
        
        # Sort by win rate
        sorted_by_winrate = sorted(all_combinations, 
                                   key=lambda x: x['metrics']['win_rate'], 
                                   reverse=True)[:10]
        
        report_lines.append("")
        report_lines.append("TOP 10 BY WIN RATE (min 10 trades):")
        report_lines.append("-" * 120)
        report_lines.append(header)
        report_lines.append("-" * 120)
        
        for rank, combo in enumerate(sorted_by_winrate, 1):
            line = f"{rank:<6} {combo['timeframe'].upper():<12} " \
                   f"{combo['setup_type'].capitalize():<13} {combo['sl_placement']:<8} " \
                   f"{combo['rr_ratio']:<6.1f} {combo['metrics']['total_trades']:<8} " \
                   f"{combo['metrics']['win_rate']:<8.2f} {combo['metrics']['expectancy']:<12.2f} " \
                   f"{combo['metrics']['total_pl']:<12.2f} " \
                   f"{self.format_profit_factor(combo['metrics']['profit_factor'])}"
            report_lines.append(line)
        
        report_lines.append("")
        
        # Sort by total P/L
        sorted_by_pl = sorted(all_combinations, 
                             key=lambda x: x['metrics']['total_pl'], 
                             reverse=True)[:10]
        
        report_lines.append("")
        report_lines.append("TOP 10 BY TOTAL PROFIT/LOSS (min 10 trades):")
        report_lines.append("-" * 120)
        report_lines.append(header)
        report_lines.append("-" * 120)
        
        for rank, combo in enumerate(sorted_by_pl, 1):
            line = f"{rank:<6} {combo['timeframe'].upper():<12} " \
                   f"{combo['setup_type'].capitalize():<13} {combo['sl_placement']:<8} " \
                   f"{combo['rr_ratio']:<6.1f} {combo['metrics']['total_trades']:<8} " \
                   f"{combo['metrics']['win_rate']:<8.2f} {combo['metrics']['expectancy']:<12.2f} " \
                   f"{combo['metrics']['total_pl']:<12.2f} " \
                   f"{self.format_profit_factor(combo['metrics']['profit_factor'])}"
            report_lines.append(line)
        
        report_lines.append("")
        report_lines.append("=" * 120)
        report_lines.append("LEGEND:")
        report_lines.append("  Trades:     Total number of completed trades (excludes unknown outcomes)")
        report_lines.append("  Winners:    Number of trades that hit Take-Profit")
        report_lines.append("  Losers:     Number of trades that hit Stop-Loss")
        report_lines.append("  Unknown:    Trades that didn't hit TP or SL within observation period")
        report_lines.append("  Win Rate:   Percentage of winning trades")
        report_lines.append("  Total P/L:  Total profit/loss in points")
        report_lines.append("  Avg Win:    Average profit per winning trade")
        report_lines.append("  Avg Loss:   Average loss per losing trade")
        report_lines.append("  Expectancy: Expected profit per trade = (Win% × Avg Win) - (Loss% × |Avg Loss|)")
        report_lines.append("  PF:         Profit Factor = Gross Profit / Gross Loss")
        report_lines.append("=" * 120)
        report_lines.append("END OF RISK/REWARD ANALYSIS REPORT")
        report_lines.append("=" * 120)
        
        # Write to file
        report_content = "\n".join(report_lines)
        output_path = os.path.join(self.base_path, output_file)
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        print(f"\nRisk/Reward analysis report saved to: {output_path}")
        print(f"Report size: {len(report_content)} bytes")
        
        return output_path

def main():
    # Get the base path (use current directory if running from repo, or use absolute path)
    import sys
    base_path = os.path.dirname(os.path.abspath(__file__)) if os.path.dirname(os.path.abspath(__file__)) else os.getcwd()
    
    # Parse command-line arguments if provided
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    
    print(f"Using base path: {base_path}")
    
    # Create analyzer instance (default: 2018-2025)
    analyzer = TradingSetupAnalyzer(base_path)
    
    # Analyze all data to find setups
    analyzer.analyze_all_data()
    
    # Generate initial setup report
    analyzer.generate_report()
    
    # Perform Risk/Reward analysis on all setups
    analyzer.analyze_all_rr_combinations()
    
    # Generate comprehensive RR analysis report
    analyzer.generate_rr_report()
    
    print("\n" + "=" * 80)
    print("ALL ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nGenerated Reports:")
    print("  1. trading_setup_report.txt - Setup identification report")
    print("  2. rr_analysis_report.txt - Comprehensive Risk/Reward analysis")
    print("=" * 80)

if __name__ == "__main__":
    main()
