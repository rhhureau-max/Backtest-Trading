"""
Daily Bias Probability Analysis Script

Expert Quant Trader - ICT (Inner Circle Trader) & Price Action Analysis

This script analyzes historical daily (1D) data to calculate statistical probabilities
of daily bias (Close > Open or Close < Open) based on previous day conditions.

Author: Expert Quant Trader
Date: 2025-12-10
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class DailyBiasProbabilityAnalyzer:
    """
    Analyzer for calculating daily bias probabilities based on ICT concepts and Price Action.
    """
    
    def __init__(self, symbol='EURUSD=X', start_date='2018-01-01', end_date=None, use_local_csv=False, csv_dir=None):
        """
        Initialize the analyzer with symbol and date range.
        
        Args:
            symbol: Trading symbol (default: EURUSD=X for forex, or BTC-USD for crypto)
            start_date: Start date for analysis (YYYY-MM-DD)
            end_date: End date for analysis (default: today)
            use_local_csv: If True, load data from local CSV files instead of yfinance
            csv_dir: Directory containing CSV files (default: current directory)
        """
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.now().strftime('%Y-%m-%d')
        self.use_local_csv = use_local_csv
        self.csv_dir = csv_dir if csv_dir else '.'
        self.df = None
        
    def fetch_data(self):
        """
        Fetch historical daily data using yfinance or local CSV files.
        """
        if self.use_local_csv:
            self.load_local_csv()
        else:
            self.fetch_yfinance_data()
    
    def load_local_csv(self):
        """
        Load data from local CSV files (NQ or ES format).
        """
        print(f"📊 Loading data from local CSV files...")
        
        try:
            # Try to find and load CSV files for the year range
            start_year = int(self.start_date.split('-')[0])
            current_year = datetime.now().year
            
            dataframes = []
            
            for year in range(start_year, current_year + 1):
                csv_file = f"{self.csv_dir}/{year} 1D.csv"
                try:
                    # Load CSV with semicolon separator
                    df_year = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
                    
                    # Check if it has the expected columns
                    if 'Column1' in df_year.columns:
                        # NQ/ES format
                        df_year['DateTime'] = pd.to_datetime(df_year['Column1'] + ' ' + df_year['Column2'], 
                                                             format='%d/%m/%Y %H:%M:%S')
                        df_year['Open'] = df_year['Column3'].astype(float)
                        df_year['High'] = df_year['Column4'].astype(float)
                        df_year['Low'] = df_year['Column5'].astype(float)
                        df_year['Close'] = df_year['Column6'].astype(float)
                        df_year['Volume'] = df_year['Column7'].astype(float)
                        
                        df_year = df_year[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
                        df_year.set_index('DateTime', inplace=True)
                        dataframes.append(df_year)
                        print(f"   ✅ Loaded {len(df_year)} rows from {year} 1D.csv")
                except FileNotFoundError:
                    continue
                except Exception as e:
                    print(f"   ⚠️  Error loading {year}: {e}")
                    continue
            
            if dataframes:
                self.df = pd.concat(dataframes)
                self.df = self.df.sort_index()
                
                # Filter by date range
                self.df = self.df[self.df.index >= self.start_date]
                if self.end_date:
                    self.df = self.df[self.df.index <= self.end_date]
                
                print(f"✅ Successfully loaded {len(self.df)} daily candles from local CSV")
                self.prepare_data()
            else:
                raise ValueError("No CSV files found or loaded")
                
        except Exception as e:
            print(f"❌ Error loading local CSV: {e}")
            raise
    
    def fetch_yfinance_data(self):
        """
        Fetch data from Yahoo Finance using yfinance.
        """
        print(f"📊 Fetching data for {self.symbol} from {self.start_date} to {self.end_date}...")
        
        try:
            ticker = yf.Ticker(self.symbol)
            self.df = ticker.history(start=self.start_date, end=self.end_date, interval='1d')
            
            if self.df.empty:
                print(f"⚠️  No data found for {self.symbol}. Trying alternative symbol...")
                # Try alternative symbol format
                if self.symbol == 'EURUSD=X':
                    self.symbol = 'BTC-USD'
                    ticker = yf.Ticker(self.symbol)
                    self.df = ticker.history(start=self.start_date, end=self.end_date, interval='1d')
            
            if not self.df.empty:
                print(f"✅ Successfully fetched {len(self.df)} daily candles for {self.symbol}")
                self.prepare_data()
            else:
                raise ValueError("Unable to fetch data from yfinance")
                
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            raise
    
    def prepare_data(self):
        """
        Prepare data with additional columns for analysis.
        """
        # Ensure we have OHLC columns
        if 'Open' not in self.df.columns:
            raise ValueError("Missing required OHLC columns")
        
        # Calculate candle direction (Green/Red)
        self.df['Candle_Direction'] = np.where(self.df['Close'] > self.df['Open'], 1, -1)  # 1=Green, -1=Red
        self.df['Is_Green'] = self.df['Candle_Direction'] == 1
        self.df['Is_Red'] = self.df['Candle_Direction'] == -1
        
        # Calculate daily range
        self.df['Daily_Range'] = self.df['High'] - self.df['Low']
        
        # Calculate Average Daily Range (10 periods)
        self.df['ADR_10'] = self.df['Daily_Range'].rolling(window=10).mean()
        
        # Calculate relative range (current range vs ADR)
        self.df['Range_Ratio'] = self.df['Daily_Range'] / self.df['ADR_10']
        
        # Shift previous day values for analysis
        self.df['Prev_High'] = self.df['High'].shift(1)
        self.df['Prev_Low'] = self.df['Low'].shift(1)
        self.df['Prev_Open'] = self.df['Open'].shift(1)
        self.df['Prev_Close'] = self.df['Close'].shift(1)
        self.df['Prev_Direction'] = self.df['Candle_Direction'].shift(1)
        
        # Previous 2 days (J-2)
        self.df['Prev2_High'] = self.df['High'].shift(2)
        self.df['Prev2_Low'] = self.df['Low'].shift(2)
        self.df['Prev2_Open'] = self.df['Open'].shift(2)
        self.df['Prev2_Close'] = self.df['Close'].shift(2)
        
        # Previous 3 days
        self.df['Prev3_Direction'] = self.df['Candle_Direction'].shift(3)
        
        print(f"✅ Data prepared with {len(self.df)} rows")
    
    def analyze_momentum_sequences(self):
        """
        Analysis 1: Candle Sequence Momentum
        Calculate probability of green/red candle after consecutive green/red candles.
        """
        print("\n" + "="*80)
        print("📈 ANALYSIS 1: MOMENTUM SEQUENCES (Candle Streaks)")
        print("="*80)
        
        results = {}
        
        # After 1 green candle
        mask_1_green = self.df['Prev_Direction'] == 1
        total_1_green = mask_1_green.sum()
        next_green_after_1_green = (mask_1_green & (self.df['Candle_Direction'] == 1)).sum()
        prob_green_after_1_green = (next_green_after_1_green / total_1_green * 100) if total_1_green > 0 else 0
        
        print(f"\n🟢 After 1 GREEN candle:")
        print(f"   • Total occurrences: {total_1_green}")
        print(f"   • Next candle GREEN: {next_green_after_1_green} ({prob_green_after_1_green:.2f}%)")
        print(f"   • Next candle RED: {total_1_green - next_green_after_1_green} ({100 - prob_green_after_1_green:.2f}%)")
        
        results['1_green'] = {
            'total': int(total_1_green),
            'next_green': int(next_green_after_1_green),
            'prob_green': prob_green_after_1_green,
            'prob_red': 100 - prob_green_after_1_green
        }
        
        # After 2 consecutive green candles
        mask_2_green = (self.df['Prev_Direction'] == 1) & (self.df['Prev_Direction'].shift(1) == 1)
        total_2_green = mask_2_green.sum()
        next_green_after_2_green = (mask_2_green & (self.df['Candle_Direction'] == 1)).sum()
        prob_green_after_2_green = (next_green_after_2_green / total_2_green * 100) if total_2_green > 0 else 0
        
        print(f"\n🟢🟢 After 2 consecutive GREEN candles:")
        print(f"   • Total occurrences: {total_2_green}")
        print(f"   • Next candle GREEN: {next_green_after_2_green} ({prob_green_after_2_green:.2f}%)")
        print(f"   • Next candle RED: {total_2_green - next_green_after_2_green} ({100 - prob_green_after_2_green:.2f}%)")
        
        results['2_green'] = {
            'total': int(total_2_green),
            'next_green': int(next_green_after_2_green),
            'prob_green': prob_green_after_2_green,
            'prob_red': 100 - prob_green_after_2_green
        }
        
        # After 3 consecutive green candles
        mask_3_green = (self.df['Prev_Direction'] == 1) & \
                       (self.df['Prev_Direction'].shift(1) == 1) & \
                       (self.df['Prev3_Direction'] == 1)
        total_3_green = mask_3_green.sum()
        next_green_after_3_green = (mask_3_green & (self.df['Candle_Direction'] == 1)).sum()
        prob_green_after_3_green = (next_green_after_3_green / total_3_green * 100) if total_3_green > 0 else 0
        
        print(f"\n🟢🟢🟢 After 3 consecutive GREEN candles:")
        print(f"   • Total occurrences: {total_3_green}")
        print(f"   • Next candle GREEN: {next_green_after_3_green} ({prob_green_after_3_green:.2f}%)")
        print(f"   • Next candle RED: {total_3_green - next_green_after_3_green} ({100 - prob_green_after_3_green:.2f}%)")
        
        results['3_green'] = {
            'total': int(total_3_green),
            'next_green': int(next_green_after_3_green),
            'prob_green': prob_green_after_3_green,
            'prob_red': 100 - prob_green_after_3_green
        }
        
        # RED CANDLES ANALYSIS
        # After 1 red candle
        mask_1_red = self.df['Prev_Direction'] == -1
        total_1_red = mask_1_red.sum()
        next_red_after_1_red = (mask_1_red & (self.df['Candle_Direction'] == -1)).sum()
        prob_red_after_1_red = (next_red_after_1_red / total_1_red * 100) if total_1_red > 0 else 0
        
        print(f"\n🔴 After 1 RED candle:")
        print(f"   • Total occurrences: {total_1_red}")
        print(f"   • Next candle RED: {next_red_after_1_red} ({prob_red_after_1_red:.2f}%)")
        print(f"   • Next candle GREEN: {total_1_red - next_red_after_1_red} ({100 - prob_red_after_1_red:.2f}%)")
        
        results['1_red'] = {
            'total': int(total_1_red),
            'next_red': int(next_red_after_1_red),
            'prob_red': prob_red_after_1_red,
            'prob_green': 100 - prob_red_after_1_red
        }
        
        # After 2 consecutive red candles
        mask_2_red = (self.df['Prev_Direction'] == -1) & (self.df['Prev_Direction'].shift(1) == -1)
        total_2_red = mask_2_red.sum()
        next_red_after_2_red = (mask_2_red & (self.df['Candle_Direction'] == -1)).sum()
        prob_red_after_2_red = (next_red_after_2_red / total_2_red * 100) if total_2_red > 0 else 0
        
        print(f"\n🔴🔴 After 2 consecutive RED candles:")
        print(f"   • Total occurrences: {total_2_red}")
        print(f"   • Next candle RED: {next_red_after_2_red} ({prob_red_after_2_red:.2f}%)")
        print(f"   • Next candle GREEN: {total_2_red - next_red_after_2_red} ({100 - prob_red_after_2_red:.2f}%)")
        
        results['2_red'] = {
            'total': int(total_2_red),
            'next_red': int(next_red_after_2_red),
            'prob_red': prob_red_after_2_red,
            'prob_green': 100 - prob_red_after_2_red
        }
        
        # After 3 consecutive red candles
        mask_3_red = (self.df['Prev_Direction'] == -1) & \
                     (self.df['Prev_Direction'].shift(1) == -1) & \
                     (self.df['Prev3_Direction'] == -1)
        total_3_red = mask_3_red.sum()
        next_red_after_3_red = (mask_3_red & (self.df['Candle_Direction'] == -1)).sum()
        prob_red_after_3_red = (next_red_after_3_red / total_3_red * 100) if total_3_red > 0 else 0
        
        print(f"\n🔴🔴🔴 After 3 consecutive RED candles:")
        print(f"   • Total occurrences: {total_3_red}")
        print(f"   • Next candle RED: {next_red_after_3_red} ({prob_red_after_3_red:.2f}%)")
        print(f"   • Next candle GREEN: {total_3_red - next_red_after_3_red} ({100 - prob_red_after_3_red:.2f}%)")
        
        results['3_red'] = {
            'total': int(total_3_red),
            'next_red': int(next_red_after_3_red),
            'prob_red': prob_red_after_3_red,
            'prob_green': 100 - prob_red_after_3_red
        }
        
        return results
    
    def analyze_price_action_ict(self):
        """
        Analysis 2: Price Action & ICT Liquidity Concepts
        - PDH/PDL Sweep detection
        - Inside Bar detection
        """
        print("\n" + "="*80)
        print("🎯 ANALYSIS 2: PRICE ACTION & ICT (Liquidity)")
        print("="*80)
        
        results = {}
        
        # PDH Sweep Detection (J-1 wicks above J-2 high but doesn't close above)
        # Bullish sweep: High[J-1] > High[J-2] but Close[J-1] < High[J-2]
        pdh_sweep = (self.df['Prev_High'] > self.df['Prev2_High']) & \
                    (self.df['Prev_Close'] < self.df['Prev2_High'])
        
        total_pdh_sweep = pdh_sweep.sum()
        reversal_after_pdh_sweep = (pdh_sweep & (self.df['Candle_Direction'] == -1)).sum()  # RED reversal
        prob_reversal_pdh = (reversal_after_pdh_sweep / total_pdh_sweep * 100) if total_pdh_sweep > 0 else 0
        
        print(f"\n💧 PDH (Previous Day High) SWEEP:")
        print(f"   Definition: J-1 wicks above J-2 high but closes below (liquidity grab)")
        print(f"   • Total PDH sweeps detected: {total_pdh_sweep}")
        print(f"   • Bearish reversal on J (RED): {reversal_after_pdh_sweep} ({prob_reversal_pdh:.2f}%)")
        print(f"   • Continuation bullish (GREEN): {total_pdh_sweep - reversal_after_pdh_sweep} ({100 - prob_reversal_pdh:.2f}%)")
        
        results['pdh_sweep'] = {
            'total': int(total_pdh_sweep),
            'reversal_bearish': int(reversal_after_pdh_sweep),
            'prob_reversal': prob_reversal_pdh,
            'prob_continuation': 100 - prob_reversal_pdh
        }
        
        # PDL Sweep Detection (J-1 wicks below J-2 low but doesn't close below)
        # Bearish sweep: Low[J-1] < Low[J-2] but Close[J-1] > Low[J-2]
        pdl_sweep = (self.df['Prev_Low'] < self.df['Prev2_Low']) & \
                    (self.df['Prev_Close'] > self.df['Prev2_Low'])
        
        total_pdl_sweep = pdl_sweep.sum()
        reversal_after_pdl_sweep = (pdl_sweep & (self.df['Candle_Direction'] == 1)).sum()  # GREEN reversal
        prob_reversal_pdl = (reversal_after_pdl_sweep / total_pdl_sweep * 100) if total_pdl_sweep > 0 else 0
        
        print(f"\n💧 PDL (Previous Day Low) SWEEP:")
        print(f"   Definition: J-1 wicks below J-2 low but closes above (liquidity grab)")
        print(f"   • Total PDL sweeps detected: {total_pdl_sweep}")
        print(f"   • Bullish reversal on J (GREEN): {reversal_after_pdl_sweep} ({prob_reversal_pdl:.2f}%)")
        print(f"   • Continuation bearish (RED): {total_pdl_sweep - reversal_after_pdl_sweep} ({100 - prob_reversal_pdl:.2f}%)")
        
        results['pdl_sweep'] = {
            'total': int(total_pdl_sweep),
            'reversal_bullish': int(reversal_after_pdl_sweep),
            'prob_reversal': prob_reversal_pdl,
            'prob_continuation': 100 - prob_reversal_pdl
        }
        
        # Inside Bar Detection
        # J-1 is inside J-2: High[J-1] < High[J-2] AND Low[J-1] > Low[J-2]
        inside_bar = (self.df['Prev_High'] < self.df['Prev2_High']) & \
                     (self.df['Prev_Low'] > self.df['Prev2_Low'])
        
        total_inside_bar = inside_bar.sum()
        bullish_expansion = (inside_bar & (self.df['Candle_Direction'] == 1)).sum()
        bearish_expansion = (inside_bar & (self.df['Candle_Direction'] == -1)).sum()
        prob_bullish_ib = (bullish_expansion / total_inside_bar * 100) if total_inside_bar > 0 else 0
        prob_bearish_ib = (bearish_expansion / total_inside_bar * 100) if total_inside_bar > 0 else 0
        
        print(f"\n📊 INSIDE BAR Pattern:")
        print(f"   Definition: J-1 contained within J-2 range (consolidation)")
        print(f"   • Total Inside Bars detected: {total_inside_bar}")
        print(f"   • Bullish expansion on J (GREEN): {bullish_expansion} ({prob_bullish_ib:.2f}%)")
        print(f"   • Bearish expansion on J (RED): {bearish_expansion} ({prob_bearish_ib:.2f}%)")
        
        # Additional analysis: Direction based on J-2 trend
        inside_bar_after_green = inside_bar & (self.df['Prev2_Close'] > self.df['Prev2_Open'])
        total_ib_after_green = inside_bar_after_green.sum()
        bullish_after_green_ib = (inside_bar_after_green & (self.df['Candle_Direction'] == 1)).sum()
        prob_bullish_after_green = (bullish_after_green_ib / total_ib_after_green * 100) if total_ib_after_green > 0 else 0
        
        print(f"\n   📈 Inside Bar after GREEN J-2:")
        print(f"      • Total: {total_ib_after_green}")
        print(f"      • Bullish continuation (GREEN): {bullish_after_green_ib} ({prob_bullish_after_green:.2f}%)")
        
        inside_bar_after_red = inside_bar & (self.df['Prev2_Close'] < self.df['Prev2_Open'])
        total_ib_after_red = inside_bar_after_red.sum()
        bearish_after_red_ib = (inside_bar_after_red & (self.df['Candle_Direction'] == -1)).sum()
        prob_bearish_after_red = (bearish_after_red_ib / total_ib_after_red * 100) if total_ib_after_red > 0 else 0
        
        print(f"\n   📉 Inside Bar after RED J-2:")
        print(f"      • Total: {total_ib_after_red}")
        print(f"      • Bearish continuation (RED): {bearish_after_red_ib} ({prob_bearish_after_red:.2f}%)")
        
        results['inside_bar'] = {
            'total': int(total_inside_bar),
            'bullish_expansion': int(bullish_expansion),
            'bearish_expansion': int(bearish_expansion),
            'prob_bullish': prob_bullish_ib,
            'prob_bearish': prob_bearish_ib,
            'after_green': {
                'total': int(total_ib_after_green),
                'bullish_continuation': int(bullish_after_green_ib),
                'prob': prob_bullish_after_green
            },
            'after_red': {
                'total': int(total_ib_after_red),
                'bearish_continuation': int(bearish_after_red_ib),
                'prob': prob_bearish_after_red
            }
        }
        
        return results
    
    def analyze_volatility_compression(self):
        """
        Analysis 3: Volatility (Range) Analysis
        Compare J-1 range to ADR (10-day average) to detect compression/expansion.
        """
        print("\n" + "="*80)
        print("📊 ANALYSIS 3: VOLATILITY ANALYSIS (Range & Compression)")
        print("="*80)
        
        results = {}
        
        # Remove NaN values for ADR calculation
        df_clean = self.df.dropna(subset=['ADR_10', 'Range_Ratio'])
        
        # Low volatility compression: J-1 range < 0.5 * ADR (very tight range)
        low_vol_compression = df_clean['Range_Ratio'].shift(1) < 0.5
        total_low_vol = low_vol_compression.sum()
        
        if total_low_vol > 0:
            # Major expansion: J range > 1.5 * ADR
            major_expansion_after_compression = (low_vol_compression & (df_clean['Range_Ratio'] > 1.5)).sum()
            prob_expansion = (major_expansion_after_compression / total_low_vol * 100)
            
            # Direction after compression
            bullish_after_compression = (low_vol_compression & (df_clean['Candle_Direction'] == 1)).sum()
            bearish_after_compression = (low_vol_compression & (df_clean['Candle_Direction'] == -1)).sum()
            prob_bullish_compression = (bullish_after_compression / total_low_vol * 100)
            prob_bearish_compression = (bearish_after_compression / total_low_vol * 100)
            
            print(f"\n🔒 LOW VOLATILITY COMPRESSION (J-1 range < 0.5 × ADR):")
            print(f"   • Total occurrences: {total_low_vol}")
            print(f"   • Major expansion on J (range > 1.5 × ADR): {major_expansion_after_compression} ({prob_expansion:.2f}%)")
            print(f"   • Direction on J:")
            print(f"      - Bullish (GREEN): {bullish_after_compression} ({prob_bullish_compression:.2f}%)")
            print(f"      - Bearish (RED): {bearish_after_compression} ({prob_bearish_compression:.2f}%)")
        else:
            prob_expansion = 0
            prob_bullish_compression = 0
            prob_bearish_compression = 0
            major_expansion_after_compression = 0
            bullish_after_compression = 0
            bearish_after_compression = 0
        
        results['low_volatility'] = {
            'total': int(total_low_vol),
            'major_expansion': int(major_expansion_after_compression),
            'prob_expansion': prob_expansion,
            'bullish': int(bullish_after_compression),
            'bearish': int(bearish_after_compression),
            'prob_bullish': prob_bullish_compression,
            'prob_bearish': prob_bearish_compression
        }
        
        # Medium volatility compression: 0.5 <= J-1 range < 0.7 * ADR
        medium_vol_compression = (df_clean['Range_Ratio'].shift(1) >= 0.5) & (df_clean['Range_Ratio'].shift(1) < 0.7)
        total_medium_vol = medium_vol_compression.sum()
        
        if total_medium_vol > 0:
            expansion_after_medium = (medium_vol_compression & (df_clean['Range_Ratio'] > 1.2)).sum()
            prob_expansion_medium = (expansion_after_medium / total_medium_vol * 100)
            
            bullish_after_medium = (medium_vol_compression & (df_clean['Candle_Direction'] == 1)).sum()
            bearish_after_medium = (medium_vol_compression & (df_clean['Candle_Direction'] == -1)).sum()
            prob_bullish_medium = (bullish_after_medium / total_medium_vol * 100)
            prob_bearish_medium = (bearish_after_medium / total_medium_vol * 100)
            
            print(f"\n🔓 MEDIUM VOLATILITY COMPRESSION (0.5 ≤ J-1 range < 0.7 × ADR):")
            print(f"   • Total occurrences: {total_medium_vol}")
            print(f"   • Expansion on J (range > 1.2 × ADR): {expansion_after_medium} ({prob_expansion_medium:.2f}%)")
            print(f"   • Direction on J:")
            print(f"      - Bullish (GREEN): {bullish_after_medium} ({prob_bullish_medium:.2f}%)")
            print(f"      - Bearish (RED): {bearish_after_medium} ({prob_bearish_medium:.2f}%)")
        else:
            prob_expansion_medium = 0
            prob_bullish_medium = 0
            prob_bearish_medium = 0
            expansion_after_medium = 0
            bullish_after_medium = 0
            bearish_after_medium = 0
        
        results['medium_volatility'] = {
            'total': int(total_medium_vol),
            'expansion': int(expansion_after_medium),
            'prob_expansion': prob_expansion_medium,
            'bullish': int(bullish_after_medium),
            'bearish': int(bearish_after_medium),
            'prob_bullish': prob_bullish_medium,
            'prob_bearish': prob_bearish_medium
        }
        
        # High volatility (expansion): J-1 range > 1.5 * ADR
        high_vol_expansion = df_clean['Range_Ratio'].shift(1) > 1.5
        total_high_vol = high_vol_expansion.sum()
        
        if total_high_vol > 0:
            # Contraction after expansion: J range < 0.8 * ADR
            contraction_after_expansion = (high_vol_expansion & (df_clean['Range_Ratio'] < 0.8)).sum()
            prob_contraction = (contraction_after_expansion / total_high_vol * 100)
            
            # Continued expansion
            continued_expansion = (high_vol_expansion & (df_clean['Range_Ratio'] > 1.2)).sum()
            prob_continued = (continued_expansion / total_high_vol * 100)
            
            print(f"\n🚀 HIGH VOLATILITY EXPANSION (J-1 range > 1.5 × ADR):")
            print(f"   • Total occurrences: {total_high_vol}")
            print(f"   • Contraction on J (range < 0.8 × ADR): {contraction_after_expansion} ({prob_contraction:.2f}%)")
            print(f"   • Continued expansion (range > 1.2 × ADR): {continued_expansion} ({prob_continued:.2f}%)")
        else:
            prob_contraction = 0
            prob_continued = 0
            contraction_after_expansion = 0
            continued_expansion = 0
        
        results['high_volatility'] = {
            'total': int(total_high_vol),
            'contraction': int(contraction_after_expansion),
            'prob_contraction': prob_contraction,
            'continued_expansion': int(continued_expansion),
            'prob_continued': prob_continued
        }
        
        # Average Daily Range statistics
        avg_range = df_clean['Daily_Range'].mean()
        median_range = df_clean['Daily_Range'].median()
        avg_adr = df_clean['ADR_10'].mean()
        
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"   • Average Daily Range: {avg_range:.4f}")
        print(f"   • Median Daily Range: {median_range:.4f}")
        print(f"   • Average ADR (10 periods): {avg_adr:.4f}")
        
        results['statistics'] = {
            'avg_range': float(avg_range),
            'median_range': float(median_range),
            'avg_adr': float(avg_adr)
        }
        
        return results
    
    def run_full_analysis(self):
        """
        Run complete analysis pipeline.
        """
        print("="*80)
        print("🎯 DAILY BIAS PROBABILITY ANALYSIS - ICT & PRICE ACTION")
        print("="*80)
        print(f"Symbol: {self.symbol}")
        print(f"Period: {self.start_date} to {self.end_date}")
        print("="*80)
        
        # Fetch data
        self.fetch_data()
        
        # Run all analyses
        momentum_results = self.analyze_momentum_sequences()
        price_action_results = self.analyze_price_action_ict()
        volatility_results = self.analyze_volatility_compression()
        
        # Summary
        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE")
        print("="*80)
        print(f"\nTotal data points analyzed: {len(self.df)}")
        print(f"Date range: {self.df.index[0].strftime('%Y-%m-%d')} to {self.df.index[-1].strftime('%Y-%m-%d')}")
        print("\n💡 KEY INSIGHTS:")
        print("   • Momentum sequences show continuation vs reversal probabilities")
        print("   • PDH/PDL sweeps indicate liquidity grabs with reversal potential")
        print("   • Inside bars signal consolidation before expansion")
        print("   • Volatility compression often precedes major moves")
        
        return {
            'momentum': momentum_results,
            'price_action': price_action_results,
            'volatility': volatility_results
        }


def main():
    """
    Main execution function.
    """
    print("\n" + "="*80)
    print("🚀 STARTING DAILY BIAS PROBABILITY ANALYSIS")
    print("="*80)
    
    # Check if we should use local CSV files
    import os
    csv_dir = '/home/runner/work/Backtest-Trading/Backtest-Trading'
    use_local = os.path.exists(f'{csv_dir}/2018 1D.csv')
    
    if use_local:
        print("\n📂 Using local NQ CSV files for analysis")
        print("-" * 80)
        analyzer = DailyBiasProbabilityAnalyzer(
            symbol='NQ', 
            start_date='2018-01-01',
            use_local_csv=True,
            csv_dir=csv_dir
        )
        results = analyzer.run_full_analysis()
    else:
        # Default analysis for EURUSD
        print("\n📊 Analysis 1: EURUSD (via yfinance)")
        print("-" * 80)
        analyzer_eurusd = DailyBiasProbabilityAnalyzer(symbol='EURUSD=X', start_date='2018-01-01')
        
        try:
            results_eurusd = analyzer_eurusd.run_full_analysis()
        except Exception as e:
            print(f"⚠️  EURUSD analysis failed: {e}")
            print("Trying alternative symbol BTC-USD...")
            
            # Fallback to BTC-USD if EURUSD fails
            print("\n📊 Analysis: BTC-USD (via yfinance)")
            print("-" * 80)
            analyzer_btc = DailyBiasProbabilityAnalyzer(symbol='BTC-USD', start_date='2018-01-01')
            results_btc = analyzer_btc.run_full_analysis()
    
    print("\n" + "="*80)
    print("🎉 ALL ANALYSES COMPLETED SUCCESSFULLY")
    print("="*80)
    print("\n📝 Notes:")
    print("   • This script can be run on Google Colab or locally")
    print("   • Supports both yfinance (EURUSD=X, BTC-USD) and local CSV files")
    print("   • Adjust the symbol parameter to analyze different assets")
    print("   • Modify date range as needed for specific periods")
    print("   • All probabilities are based on historical data (2018-present)")
    print("\n")


if __name__ == "__main__":
    main()
