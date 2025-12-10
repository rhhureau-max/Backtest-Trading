"""
Next Day Bias Probability Study
================================

Quantitative Analyst - Conditional Probability & Pattern Recognition Specialist

This script analyzes 5 predictive scenarios to determine next-day bias probabilities
based on current day structure for NQ & ES futures.

For each scenario, calculates:
- Win Rate: % times next day follows theoretical bias
- Loss Rate: % times next day does opposite
- Average Return: Mean performance in points next day

Author: Senior Quant Analyst - Pattern Recognition Expert
Date: 2025-12-10
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class NextDayBiasProbabilityAnalyzer:
    """
    Analyzer for next-day bias probabilities based on current day patterns.
    """
    
    def __init__(self, symbol='NQ', start_date='2018-01-01', csv_dir='.'):
        """
        Initialize the analyzer.
        
        Args:
            symbol: Trading symbol (NQ or ES)
            start_date: Start date for analysis
            csv_dir: Directory containing CSV files
        """
        self.symbol = symbol
        self.start_date = start_date
        self.csv_dir = csv_dir
        
        # Dataframes
        self.df_1d = None
        self.df_1h = None
        
        # Results storage
        self.results = {}
        
    def load_data(self):
        """
        Load daily and 1H data for analysis.
        """
        print(f"📊 Loading data for {self.symbol}...")
        
        try:
            # Load 1D data
            self.df_1d = self._load_timeframe('1D')
            print(f"   ✅ Daily: {len(self.df_1d)} candles")
            
            # Load 1H data (for intraday gap analysis)
            self.df_1h = self._load_timeframe('1H')
            print(f"   ✅ 1H: {len(self.df_1h)} candles")
            
            # Prepare data
            self._prepare_data()
            
            print(f"✅ Data loaded and prepared\n")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def _load_timeframe(self, timeframe):
        """
        Load CSV data for a specific timeframe.
        """
        start_year = int(self.start_date.split('-')[0])
        current_year = datetime.now().year
        
        dataframes = []
        
        for year in range(start_year, current_year + 1):
            csv_file = f"{self.csv_dir}/{year} {timeframe}.csv"
            try:
                df_year = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
                
                if 'Column1' in df_year.columns:
                    df_year['DateTime'] = pd.to_datetime(
                        df_year['Column1'] + ' ' + df_year['Column2'],
                        format='%d/%m/%Y %H:%M:%S'
                    )
                    df_year['Open'] = df_year['Column3'].astype(float)
                    df_year['High'] = df_year['Column4'].astype(float)
                    df_year['Low'] = df_year['Column5'].astype(float)
                    df_year['Close'] = df_year['Column6'].astype(float)
                    df_year['Volume'] = df_year['Column7'].astype(float)
                    
                    df_year = df_year[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                    df_year.set_index('DateTime', inplace=True)
                    dataframes.append(df_year)
            except FileNotFoundError:
                continue
        
        if dataframes:
            df = pd.concat(dataframes)
            df = df.sort_index()
            df = df[df.index >= self.start_date]
            return df
        else:
            raise ValueError(f"No data found for {self.symbol} {timeframe}")
    
    def _prepare_data(self):
        """
        Prepare data with additional calculated columns.
        """
        df = self.df_1d.copy()
        
        # Basic calculations
        df['Range'] = df['High'] - df['Low']
        df['Body'] = df['Close'] - df['Open']
        df['Is_Green'] = df['Close'] > df['Open']
        df['Is_Red'] = df['Close'] < df['Open']
        
        # Volume moving average
        df['Volume_MA20'] = df['Volume'].rolling(window=20).mean()
        
        # Close position in range (0-100%)
        df['Close_Position'] = ((df['Close'] - df['Low']) / df['Range'] * 100).fillna(50)
        
        # Previous day values
        df['Prev_High'] = df['High'].shift(1)
        df['Prev_Low'] = df['Low'].shift(1)
        df['Prev_Close'] = df['Close'].shift(1)
        df['Prev_Open'] = df['Open'].shift(1)
        
        # Next day values (for outcome)
        df['Next_Open'] = df['Open'].shift(-1)
        df['Next_High'] = df['High'].shift(-1)
        df['Next_Low'] = df['Low'].shift(-1)
        df['Next_Close'] = df['Close'].shift(-1)
        df['Next_Is_Green'] = df['Next_Close'] > df['Next_Open']
        df['Next_Return'] = df['Next_Close'] - df['Next_Open']
        
        self.df_1d = df
    
    def scenario_1_momentum_continuation(self):
        """
        SCENARIO 1: Momentum Continuation (Strong Close)
        
        Condition J: Close in top 10% of range AND volume > 20-day MA
        Theoretical Bias J+1: BULLISH
        Question: If buy at open J+1 and close at end, what's success rate?
        """
        print("="*80)
        print("📈 SCENARIO 1: Momentum Continuation (Strong Close)")
        print("="*80)
        
        df = self.df_1d.copy()
        
        # Filter condition
        condition = (df['Close_Position'] >= 90) & (df['Volume'] > df['Volume_MA20'])
        
        # Get matching days
        df_filtered = df[condition].dropna(subset=['Next_Is_Green', 'Next_Return'])
        
        total_occurrences = len(df_filtered)
        
        if total_occurrences == 0:
            print("❌ No occurrences found for this scenario\n")
            return None
        
        # Calculate statistics
        bullish_next_day = df_filtered['Next_Is_Green'].sum()
        bearish_next_day = total_occurrences - bullish_next_day
        
        win_rate = (bullish_next_day / total_occurrences * 100)
        loss_rate = (bearish_next_day / total_occurrences * 100)
        avg_return = df_filtered['Next_Return'].mean()
        
        # Additional stats
        positive_returns = (df_filtered['Next_Return'] > 0).sum()
        negative_returns = (df_filtered['Next_Return'] < 0).sum()
        
        print(f"\n📊 Results:")
        print(f"   • Total occurrences: {total_occurrences}")
        print(f"   • Theoretical bias: BULLISH (buy at open J+1)")
        print(f"\n   Win Rate (J+1 Green): {bullish_next_day} / {total_occurrences} = {win_rate:.2f}%")
        print(f"   Loss Rate (J+1 Red): {bearish_next_day} / {total_occurrences} = {loss_rate:.2f}%")
        print(f"\n   Positive Returns: {positive_returns} ({positive_returns/total_occurrences*100:.2f}%)")
        print(f"   Negative Returns: {negative_returns} ({negative_returns/total_occurrences*100:.2f}%)")
        print(f"\n   Average Return (pts): {avg_return:.2f}")
        print(f"   Best Return: {df_filtered['Next_Return'].max():.2f} pts")
        print(f"   Worst Return: {df_filtered['Next_Return'].min():.2f} pts")
        print(f"   Median Return: {df_filtered['Next_Return'].median():.2f} pts")
        
        self.results['scenario_1'] = {
            'name': 'Momentum Continuation',
            'total_occurrences': total_occurrences,
            'win_rate': win_rate,
            'loss_rate': loss_rate,
            'avg_return': avg_return,
            'bullish_days': int(bullish_next_day),
            'bearish_days': int(bearish_next_day)
        }
        
        return self.results['scenario_1']
    
    def scenario_2_failed_breakdown(self):
        """
        SCENARIO 2: Failed Breakdown (Rejection / Turtle Soup)
        
        Condition J: Low breaks previous day low BUT closes green and above prev low
        Theoretical Bias J+1: BULLISH (reversal)
        Question: What's probability J+1 is green?
        """
        print("="*80)
        print("📈 SCENARIO 2: Failed Breakdown (Turtle Soup)")
        print("="*80)
        
        df = self.df_1d.copy()
        
        # Filter condition: swept below prev low but closed green and above it
        condition = (df['Low'] < df['Prev_Low']) & \
                    (df['Is_Green']) & \
                    (df['Close'] > df['Prev_Low'])
        
        df_filtered = df[condition].dropna(subset=['Next_Is_Green', 'Next_Return'])
        
        total_occurrences = len(df_filtered)
        
        if total_occurrences == 0:
            print("❌ No occurrences found for this scenario\n")
            return None
        
        # Calculate statistics
        bullish_next_day = df_filtered['Next_Is_Green'].sum()
        bearish_next_day = total_occurrences - bullish_next_day
        
        win_rate = (bullish_next_day / total_occurrences * 100)
        loss_rate = (bearish_next_day / total_occurrences * 100)
        avg_return = df_filtered['Next_Return'].mean()
        
        print(f"\n📊 Results:")
        print(f"   • Total occurrences: {total_occurrences}")
        print(f"   • Theoretical bias: BULLISH (reversal after rejection)")
        print(f"\n   Win Rate (J+1 Green): {bullish_next_day} / {total_occurrences} = {win_rate:.2f}%")
        print(f"   Loss Rate (J+1 Red): {bearish_next_day} / {total_occurrences} = {loss_rate:.2f}%")
        print(f"\n   Average Return (pts): {avg_return:.2f}")
        print(f"   Best Return: {df_filtered['Next_Return'].max():.2f} pts")
        print(f"   Worst Return: {df_filtered['Next_Return'].min():.2f} pts")
        
        self.results['scenario_2'] = {
            'name': 'Failed Breakdown',
            'total_occurrences': total_occurrences,
            'win_rate': win_rate,
            'loss_rate': loss_rate,
            'avg_return': avg_return,
            'bullish_days': int(bullish_next_day),
            'bearish_days': int(bearish_next_day)
        }
        
        return self.results['scenario_2']
    
    def scenario_3_inside_day_compression(self):
        """
        SCENARIO 3: Inside Day Compression
        
        Condition J: High < Prev_High AND Low > Prev_Low (inside bar)
        Theoretical Bias J+1: EXPANSION (breakout)
        Question: If J+1 breaks high of inside day, what's success rate finishing green?
        """
        print("="*80)
        print("📈 SCENARIO 3: Inside Day Compression")
        print("="*80)
        
        df = self.df_1d.copy()
        
        # Filter condition: inside day
        condition = (df['High'] < df['Prev_High']) & (df['Low'] > df['Prev_Low'])
        
        df_filtered = df[condition].dropna(subset=['Next_High', 'Next_Is_Green', 'Next_Return'])
        
        total_occurrences = len(df_filtered)
        
        if total_occurrences == 0:
            print("❌ No occurrences found for this scenario\n")
            return None
        
        # Check if next day breaks high of inside day
        breaks_high = df_filtered['Next_High'] > df_filtered['High']
        df_breakout = df_filtered[breaks_high]
        
        total_breakouts = len(df_breakout)
        
        if total_breakouts == 0:
            print("❌ No breakouts found\n")
            return None
        
        # Calculate statistics for breakouts
        bullish_breakout = df_breakout['Next_Is_Green'].sum()
        bearish_breakout = total_breakouts - bullish_breakout
        
        win_rate = (bullish_breakout / total_breakouts * 100)
        loss_rate = (bearish_breakout / total_breakouts * 100)
        avg_return = df_breakout['Next_Return'].mean()
        
        print(f"\n📊 Results:")
        print(f"   • Total Inside Days: {total_occurrences}")
        print(f"   • Breakouts (Next day high > Inside high): {total_breakouts} ({total_breakouts/total_occurrences*100:.2f}%)")
        print(f"   • Theoretical bias: BULLISH EXPANSION")
        print(f"\n   Win Rate (Breakout & Green): {bullish_breakout} / {total_breakouts} = {win_rate:.2f}%")
        print(f"   Loss Rate (Breakout but Red): {bearish_breakout} / {total_breakouts} = {loss_rate:.2f}%")
        print(f"\n   Average Return (pts): {avg_return:.2f}")
        print(f"   Best Return: {df_breakout['Next_Return'].max():.2f} pts")
        print(f"   Worst Return: {df_breakout['Next_Return'].min():.2f} pts")
        
        self.results['scenario_3'] = {
            'name': 'Inside Day Compression',
            'total_occurrences': total_occurrences,
            'total_breakouts': total_breakouts,
            'breakout_rate': total_breakouts/total_occurrences*100,
            'win_rate': win_rate,
            'loss_rate': loss_rate,
            'avg_return': avg_return,
            'bullish_days': int(bullish_breakout),
            'bearish_days': int(bearish_breakout)
        }
        
        return self.results['scenario_3']
    
    def scenario_4_three_day_rule(self):
        """
        SCENARIO 4: Three Day Rule (Mean Reversion)
        
        Condition J: 3 consecutive red days
        Theoretical Bias J+1: BULLISH (technical bounce)
        Question: After 3 red days on NQ, what's bullish vs bearish ratio for day 4?
        """
        print("="*80)
        print("📈 SCENARIO 4: Three Day Rule (Mean Reversion)")
        print("="*80)
        
        df = self.df_1d.copy()
        
        # Check for 3 consecutive red days
        df['Is_Red_1'] = df['Is_Red']
        df['Is_Red_2'] = df['Is_Red'].shift(1)
        df['Is_Red_3'] = df['Is_Red'].shift(2)
        
        condition = df['Is_Red_1'] & df['Is_Red_2'] & df['Is_Red_3']
        
        df_filtered = df[condition].dropna(subset=['Next_Is_Green', 'Next_Return'])
        
        total_occurrences = len(df_filtered)
        
        if total_occurrences == 0:
            print("❌ No occurrences found for this scenario\n")
            return None
        
        # Calculate statistics
        bullish_next_day = df_filtered['Next_Is_Green'].sum()
        bearish_next_day = total_occurrences - bullish_next_day
        
        win_rate = (bullish_next_day / total_occurrences * 100)
        loss_rate = (bearish_next_day / total_occurrences * 100)
        avg_return = df_filtered['Next_Return'].mean()
        
        print(f"\n📊 Results:")
        print(f"   • Total occurrences (3 consecutive red days): {total_occurrences}")
        print(f"   • Theoretical bias: BULLISH (mean reversion bounce)")
        print(f"\n   Win Rate (Day 4 Green): {bullish_next_day} / {total_occurrences} = {win_rate:.2f}%")
        print(f"   Loss Rate (Day 4 Red): {bearish_next_day} / {total_occurrences} = {loss_rate:.2f}%")
        print(f"   Bullish/Bearish Ratio: {bullish_next_day}/{bearish_next_day} = {bullish_next_day/bearish_next_day:.2f}" if bearish_next_day > 0 else "   Bullish/Bearish Ratio: All bullish")
        print(f"\n   Average Return (pts): {avg_return:.2f}")
        print(f"   Best Return: {df_filtered['Next_Return'].max():.2f} pts")
        print(f"   Worst Return: {df_filtered['Next_Return'].min():.2f} pts")
        
        self.results['scenario_4'] = {
            'name': 'Three Day Rule',
            'total_occurrences': total_occurrences,
            'win_rate': win_rate,
            'loss_rate': loss_rate,
            'avg_return': avg_return,
            'bullish_days': int(bullish_next_day),
            'bearish_days': int(bearish_next_day)
        }
        
        return self.results['scenario_4']
    
    def scenario_5_gap_up_continuation(self):
        """
        SCENARIO 5: Gap Up Non-Filled (Institutional Strength)
        
        Condition J+1: Market opens with gap > 0.3% from J close
        Theoretical Bias J+1: CONTINUATION (gap and go)
        Question: If gap not filled in first hour, what's % chance day finishes higher than open?
        """
        print("="*80)
        print("📈 SCENARIO 5: Gap Up Continuation (Gap and Go)")
        print("="*80)
        
        df_1d = self.df_1d.copy()
        df_1h = self.df_1h.copy()
        
        # Calculate gap percentage
        df_1d['Gap_Pct'] = ((df_1d['Open'] - df_1d['Prev_Close']) / df_1d['Prev_Close'] * 100)
        
        # Filter for gap up > 0.3%
        condition = df_1d['Gap_Pct'] > 0.3
        df_filtered = df_1d[condition].dropna(subset=['Open', 'Close'])
        
        total_occurrences = len(df_filtered)
        
        if total_occurrences == 0:
            print("❌ No occurrences found for this scenario\n")
            return None
        
        # Check if gap filled in first hour
        gaps_not_filled = []
        gaps_filled = []
        
        for idx, row in df_filtered.iterrows():
            date = idx.date()
            open_price = row['Open']
            prev_close = row['Prev_Close']
            close_price = row['Close']
            
            # Get first hour of trading
            first_hour = df_1h[
                (df_1h.index.date == date) &
                (df_1h.index.hour >= 9) &
                (df_1h.index.hour < 11)
            ]
            
            if len(first_hour) > 0:
                # Check if gap was filled (touched prev close)
                gap_filled = (first_hour['Low'] <= prev_close).any()
                
                if not gap_filled:
                    # Gap not filled - check if finished higher than open
                    finished_higher = close_price > open_price
                    gaps_not_filled.append({
                        'date': date,
                        'finished_higher': finished_higher,
                        'return': close_price - open_price,
                        'gap_pct': row['Gap_Pct']
                    })
                else:
                    gaps_filled.append(date)
        
        df_gaps_not_filled = pd.DataFrame(gaps_not_filled)
        
        if len(df_gaps_not_filled) == 0:
            print("❌ No gaps that remained unfilled in first hour\n")
            return None
        
        # Calculate statistics
        total_unfilled = len(df_gaps_not_filled)
        finished_higher = df_gaps_not_filled['finished_higher'].sum()
        finished_lower = total_unfilled - finished_higher
        
        win_rate = (finished_higher / total_unfilled * 100)
        loss_rate = (finished_lower / total_unfilled * 100)
        avg_return = df_gaps_not_filled['return'].mean()
        
        print(f"\n📊 Results:")
        print(f"   • Total gap up days (>0.3%): {total_occurrences}")
        print(f"   • Gaps NOT filled in first hour: {total_unfilled} ({total_unfilled/total_occurrences*100:.2f}%)")
        print(f"   • Gaps filled in first hour: {len(gaps_filled)} ({len(gaps_filled)/total_occurrences*100:.2f}%)")
        print(f"   • Theoretical bias: BULLISH CONTINUATION")
        print(f"\n   Win Rate (Finished higher than open): {finished_higher} / {total_unfilled} = {win_rate:.2f}%")
        print(f"   Loss Rate (Finished lower than open): {finished_lower} / {total_unfilled} = {loss_rate:.2f}%")
        print(f"\n   Average Return from open (pts): {avg_return:.2f}")
        print(f"   Best Return: {df_gaps_not_filled['return'].max():.2f} pts")
        print(f"   Worst Return: {df_gaps_not_filled['return'].min():.2f} pts")
        print(f"   Average Gap Size: {df_gaps_not_filled['gap_pct'].mean():.2f}%")
        
        self.results['scenario_5'] = {
            'name': 'Gap Up Continuation',
            'total_occurrences': total_occurrences,
            'total_unfilled': total_unfilled,
            'win_rate': win_rate,
            'loss_rate': loss_rate,
            'avg_return': avg_return,
            'finished_higher': int(finished_higher),
            'finished_lower': int(finished_lower)
        }
        
        return self.results['scenario_5']
    
    def run_all_scenarios(self):
        """
        Run all 5 scenarios and display comparison.
        """
        print("\n" + "="*80)
        print("🎯 NEXT DAY BIAS PROBABILITY STUDY")
        print(f"Symbol: {self.symbol}")
        print(f"Period: {self.start_date} to {datetime.now().strftime('%Y-%m-%d')}")
        print("="*80 + "\n")
        
        # Load data
        self.load_data()
        
        # Run all scenarios
        print("Starting probability analysis...\n")
        
        self.scenario_1_momentum_continuation()
        print()
        
        self.scenario_2_failed_breakdown()
        print()
        
        self.scenario_3_inside_day_compression()
        print()
        
        self.scenario_4_three_day_rule()
        print()
        
        self.scenario_5_gap_up_continuation()
        print()
        
        # Comparison table
        self._print_comparison_table()
        
        return self.results
    
    def _print_comparison_table(self):
        """
        Print comparison table of all scenarios.
        """
        print("\n" + "="*80)
        print("📊 SCENARIOS COMPARISON TABLE")
        print("="*80)
        
        print(f"\n{'Scenario':<35} {'Count':<8} {'Win Rate':<12} {'Avg Return':<12}")
        print("-" * 80)
        
        for key in ['scenario_1', 'scenario_2', 'scenario_3', 'scenario_4', 'scenario_5']:
            if key in self.results and self.results[key]:
                r = self.results[key]
                count = r.get('total_occurrences', r.get('total_unfilled', 0))
                print(f"{r['name']:<35} "
                      f"{count:<8} "
                      f"{r['win_rate']:<11.2f}% "
                      f"{r['avg_return']:<11.2f}pts")
        
        print("\n" + "="*80)
        print("💡 INTERPRETATION GUIDE:")
        print("="*80)
        print("   • Win Rate > 55%: Statistical edge exists")
        print("   • Win Rate 45-55%: No clear edge (coin flip)")
        print("   • Win Rate < 45%: Consider contrarian approach")
        print("   • Avg Return > 0: Positive expectancy")
        print()


def main():
    """
    Main execution function.
    """
    print("\n" + "="*80)
    print("🚀 NEXT DAY BIAS PROBABILITY STUDY")
    print("="*80)
    print("\nQuantitative Analyst - Pattern Recognition & Conditional Probabilities")
    print("Analyzing predictive patterns for next-day bias")
    print("\n" + "="*80 + "\n")
    
    # Analyze NQ
    print("📊 Analysis 1: NQ (Nasdaq 100 Futures)")
    print("-" * 80)
    analyzer_nq = NextDayBiasProbabilityAnalyzer(
        symbol='NQ',
        start_date='2018-01-01',
        csv_dir='.'
    )
    results_nq = analyzer_nq.run_all_scenarios()
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
    print("\n📝 Summary:")
    print("   • All 5 predictive scenarios analyzed")
    print("   • Conditional probabilities calculated")
    print("   • Win rates and average returns provided")
    print("   • Statistical edges identified")
    print("\n")


if __name__ == "__main__":
    main()
