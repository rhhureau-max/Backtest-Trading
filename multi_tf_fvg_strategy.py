#!/usr/bin/env python3
"""
Multi-Timeframe FVG + Liquidity Sweep Strategy

Strategy Logic (as described by user):
1. A 4H or 1H FVG is broken by a wick (liquidity sweep on higher timeframe)
2. Price continues its initial movement
3. A 15m FVG is created just before the liquidity sweep
4. Entry when the 15m FVG is broken (closed below for short, above for long)

Analysis window: 2:00 AM to 12:00 PM Chicago time (CST/CDT)

Author: Trading Analysis Tool
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum


class TradeDirection(Enum):
    LONG = "long"
    SHORT = "short"


@dataclass
class FVG:
    """Fair Value Gap"""
    datetime: datetime
    fvg_type: str  # 'bullish' or 'bearish'
    gap_high: float
    gap_low: float
    gap_size: float
    timeframe: str
    
    def __str__(self):
        return f"[{self.datetime}] {self.fvg_type.upper()} FVG {self.timeframe}: {self.gap_low:.2f} - {self.gap_high:.2f}"


@dataclass
class LiquiditySweep:
    """Liquidity Sweep Event on Higher Timeframe"""
    datetime: datetime
    sweep_type: str  # 'bullish' or 'bearish'
    level: float
    high: float
    low: float
    close: float
    timeframe: str


@dataclass
class TradeSetup:
    """Complete Trade Setup"""
    setup_id: int
    htf_fvg: FVG  # 4H or 1H FVG that was swept
    fvg_15m: FVG  # 15m FVG created before the sweep
    sweep: LiquiditySweep
    direction: TradeDirection
    entry_datetime: datetime
    entry_price: float
    stop_loss: float
    risk_points: float


@dataclass
class TradeResult:
    """Trade Result"""
    setup: TradeSetup
    exit_datetime: datetime
    exit_price: float
    pnl_points: float
    rr_achieved: float
    tp1_hit: bool = False
    tp2_hit: bool = False
    tp3_hit: bool = False
    max_favorable_excursion: float = 0.0
    max_adverse_excursion: float = 0.0


class MultiTFStrategy:
    """Multi-Timeframe FVG + Sweep Strategy"""
    
    def __init__(
        self,
        data_dir: str = ".",
        fvg_min_size_pct: float = 0.0001,
        swing_lookback: int = 5,
        sl_buffer_pct: float = 0.0005,
        max_htf_fvg_age_candles: int = 20,
        max_15m_fvg_age_candles: int = 10
    ):
        self.data_dir = Path(data_dir)
        self.fvg_min_size_pct = fvg_min_size_pct
        self.swing_lookback = swing_lookback
        self.sl_buffer_pct = sl_buffer_pct
        self.max_htf_fvg_age_candles = max_htf_fvg_age_candles
        self.max_15m_fvg_age_candles = max_15m_fvg_age_candles
    
    def load_data(self, year: int) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Load 4H, 1H, 15m and 1m data for a given year"""
        
        def load_csv(filename: str) -> pd.DataFrame:
            filepath = self.data_dir / filename
            if not filepath.exists():
                raise FileNotFoundError(f"File not found: {filepath}")
            
            df = pd.read_csv(filepath, sep=';', header=0)
            df.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            
            # Parse datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
            df.set_index('DateTime', inplace=True)
            
            # Convert to numeric
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df.dropna(inplace=True)
            return df
        
        df_4h = load_csv(f"{year} 4H.csv")
        df_1h = load_csv(f"{year} 1H.csv")
        df_15m = load_csv(f"{year} 15m.csv")
        
        # Load 1m data (may be zipped or xlsx for older years)
        try:
            df_1m = load_csv(f"{year} 1m.csv")
        except FileNotFoundError:
            # Try xlsx
            xlsx_path = self.data_dir / f"{year} 1m.xlsx"
            if xlsx_path.exists():
                df_1m = pd.read_excel(xlsx_path)
                df_1m.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                df_1m['DateTime'] = pd.to_datetime(df_1m['Date'].astype(str) + ' ' + df_1m['Time'].astype(str))
                df_1m.set_index('DateTime', inplace=True)
                for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                    df_1m[col] = pd.to_numeric(df_1m[col], errors='coerce')
                df_1m.dropna(inplace=True)
            else:
                raise FileNotFoundError(f"Neither CSV nor XLSX found for {year} 1m data")
        
        return df_4h, df_1h, df_15m, df_1m
    
    def is_in_chicago_trading_window(self, dt: datetime) -> bool:
        """Check if datetime is between 2:00 AM and 12:00 PM Chicago time
        Note: The data appears to be in a specific timezone. We'll filter by hour.
        Assuming data is in UTC or similar, we adjust accordingly.
        For simplicity, we'll use the raw hours from the data (which seems to be in a consistent timezone)
        """
        # Chicago is UTC-6 (CST) or UTC-5 (CDT)
        # The data appears to be in a European timezone or UTC
        # We'll assume data is UTC and Chicago is UTC-6
        # So 2:00 AM Chicago = 8:00 UTC, 12:00 PM Chicago = 18:00 UTC
        
        # Actually let's just use the hour from the data as-is
        # and let the user interpret based on their understanding
        hour = dt.hour
        return 8 <= hour <= 18  # Approximate window for 2:00-12:00 Chicago if data is in UTC
    
    def detect_fvg(self, df: pd.DataFrame, timeframe: str) -> List[FVG]:
        """Detect all FVGs in the dataframe"""
        fvgs = []
        
        highs = df['High'].values
        lows = df['Low'].values
        
        for i in range(2, len(df)):
            candle1_high = highs[i - 2]
            candle1_low = lows[i - 2]
            candle3_high = highs[i]
            candle3_low = lows[i]
            
            # Bullish FVG (gap up)
            if candle1_high < candle3_low:
                gap_low = candle1_high
                gap_high = candle3_low
                gap_size = gap_high - gap_low
                gap_size_pct = gap_size / gap_low if gap_low > 0 else 0
                
                if gap_size_pct >= self.fvg_min_size_pct:
                    fvgs.append(FVG(
                        datetime=df.index[i - 1],
                        fvg_type='bullish',
                        gap_high=gap_high,
                        gap_low=gap_low,
                        gap_size=gap_size,
                        timeframe=timeframe
                    ))
            
            # Bearish FVG (gap down)
            elif candle1_low > candle3_high:
                gap_low = candle3_high
                gap_high = candle1_low
                gap_size = gap_high - gap_low
                gap_size_pct = gap_size / gap_low if gap_low > 0 else 0
                
                if gap_size_pct >= self.fvg_min_size_pct:
                    fvgs.append(FVG(
                        datetime=df.index[i - 1],
                        fvg_type='bearish',
                        gap_high=gap_high,
                        gap_low=gap_low,
                        gap_size=gap_size,
                        timeframe=timeframe
                    ))
        
        return fvgs
    
    def detect_wick_sweep_of_fvg(
        self, 
        df_htf: pd.DataFrame, 
        fvg: FVG,
        max_candles_after: int = 20
    ) -> Optional[Tuple[datetime, str]]:
        """
        Detect if an FVG was swept by a wick (not body)
        Returns the datetime and sweep type if found
        """
        # Find candles after the FVG
        fvg_idx = df_htf.index.get_loc(fvg.datetime) if fvg.datetime in df_htf.index else None
        if fvg_idx is None:
            # Find closest index after FVG datetime
            fvg_idx = df_htf.index.searchsorted(fvg.datetime)
        
        if fvg_idx >= len(df_htf):
            return None
        
        end_idx = min(fvg_idx + max_candles_after, len(df_htf))
        
        for i in range(fvg_idx + 1, end_idx):
            candle = df_htf.iloc[i]
            
            if fvg.fvg_type == 'bullish':
                # For bullish FVG, look for wick going into the gap (bearish sweep)
                # The low should go into the gap but close should be above gap_high
                if candle['Low'] <= fvg.gap_high and candle['Low'] >= fvg.gap_low:
                    if candle['Close'] > fvg.gap_high or candle['Open'] > fvg.gap_high:
                        # Wick swept into the bullish FVG - this is a bullish sweep (continuation)
                        return (df_htf.index[i], 'bullish')
            
            elif fvg.fvg_type == 'bearish':
                # For bearish FVG, look for wick going into the gap (bullish sweep)
                # The high should go into the gap but close should be below gap_low
                if candle['High'] >= fvg.gap_low and candle['High'] <= fvg.gap_high:
                    if candle['Close'] < fvg.gap_low or candle['Open'] < fvg.gap_low:
                        # Wick swept into the bearish FVG - this is a bearish sweep (continuation)
                        return (df_htf.index[i], 'bearish')
        
        return None
    
    def find_15m_fvg_before_sweep(
        self,
        df_15m: pd.DataFrame,
        sweep_datetime: datetime,
        sweep_type: str,
        lookback_candles: int = 10
    ) -> Optional[FVG]:
        """Find a 15m FVG created just before the sweep"""
        
        # Get 15m candles before the sweep
        df_before = df_15m[df_15m.index < sweep_datetime]
        
        if len(df_before) < 3:
            return None
        
        # Look for FVG in the last N candles before sweep
        start_idx = max(0, len(df_before) - lookback_candles)
        
        highs = df_before['High'].values
        lows = df_before['Low'].values
        
        found_fvg = None
        
        for i in range(start_idx + 2, len(df_before)):
            candle1_high = highs[i - 2]
            candle1_low = lows[i - 2]
            candle3_high = highs[i]
            candle3_low = lows[i]
            
            # For bullish sweep, look for bullish FVG (created during up move)
            if sweep_type == 'bullish':
                if candle1_high < candle3_low:
                    gap_low = candle1_high
                    gap_high = candle3_low
                    gap_size = gap_high - gap_low
                    
                    if gap_size > 0:
                        found_fvg = FVG(
                            datetime=df_before.index[i - 1],
                            fvg_type='bullish',
                            gap_high=gap_high,
                            gap_low=gap_low,
                            gap_size=gap_size,
                            timeframe='15m'
                        )
            
            # For bearish sweep, look for bearish FVG (created during down move)
            elif sweep_type == 'bearish':
                if candle1_low > candle3_high:
                    gap_low = candle3_high
                    gap_high = candle1_low
                    gap_size = gap_high - gap_low
                    
                    if gap_size > 0:
                        found_fvg = FVG(
                            datetime=df_before.index[i - 1],
                            fvg_type='bearish',
                            gap_high=gap_high,
                            gap_low=gap_low,
                            gap_size=gap_size,
                            timeframe='15m'
                        )
        
        return found_fvg
    
    def find_entry_15m(
        self,
        df_15m: pd.DataFrame,
        fvg_15m: FVG,
        sweep_datetime: datetime,
        sweep_type: str,
        max_candles: int = 20
    ) -> Optional[Tuple[datetime, float]]:
        """
        Find entry on 15m when the FVG is broken after the sweep
        """
        # Get 15m candles after the sweep
        df_after = df_15m[df_15m.index >= sweep_datetime]
        
        if len(df_after) < 1:
            return None
        
        max_candles = min(len(df_after), max_candles)
        
        for i in range(max_candles):
            candle = df_after.iloc[i]
            
            # For bullish sweep followed by reversal (short entry)
            # Entry when price closes below the bullish FVG
            if sweep_type == 'bullish' and fvg_15m.fvg_type == 'bullish':
                if candle['Close'] < fvg_15m.gap_low:
                    return (df_after.index[i], candle['Close'])
            
            # For bearish sweep followed by reversal (long entry)
            # Entry when price closes above the bearish FVG
            elif sweep_type == 'bearish' and fvg_15m.fvg_type == 'bearish':
                if candle['Close'] > fvg_15m.gap_high:
                    return (df_after.index[i], candle['Close'])
        
        return None
    
    def run_analysis(self, year: int) -> List[TradeSetup]:
        """Run the multi-timeframe analysis"""
        
        print(f"Loading data for {year}...")
        df_4h, df_1h, df_15m, df_1m = self.load_data(year)
        
        print(f"4H: {len(df_4h)} candles ({df_4h.index.min()} to {df_4h.index.max()})")
        print(f"1H: {len(df_1h)} candles")
        print(f"15m: {len(df_15m)} candles")
        print(f"1m: {len(df_1m)} candles")
        
        setups = []
        setup_id = 0
        
        # Detect FVGs on 4H and 1H
        print("\n[1/4] Detecting FVGs on 4H...")
        fvgs_4h = self.detect_fvg(df_4h, '4H')
        print(f"Found {len(fvgs_4h)} FVGs on 4H")
        
        print("[2/4] Detecting FVGs on 1H...")
        fvgs_1h = self.detect_fvg(df_1h, '1H')
        print(f"Found {len(fvgs_1h)} FVGs on 1H")
        
        # Combine HTF FVGs
        all_htf_fvgs = fvgs_4h + fvgs_1h
        all_htf_fvgs.sort(key=lambda x: x.datetime)
        
        print(f"\n[3/4] Scanning for HTF FVG wick sweeps and 15m FVG setups...")
        
        for htf_fvg in all_htf_fvgs:
            # Check if in trading window
            if not self.is_in_chicago_trading_window(htf_fvg.datetime):
                continue
            
            # Detect if this HTF FVG was swept by a wick
            df_htf = df_4h if htf_fvg.timeframe == '4H' else df_1h
            sweep_result = self.detect_wick_sweep_of_fvg(df_htf, htf_fvg)
            
            if sweep_result is None:
                continue
            
            sweep_datetime, sweep_type = sweep_result
            
            # Check if sweep is in trading window
            if not self.is_in_chicago_trading_window(sweep_datetime):
                continue
            
            # Find 15m FVG created just before the sweep
            fvg_15m = self.find_15m_fvg_before_sweep(
                df_15m, sweep_datetime, sweep_type, 
                self.max_15m_fvg_age_candles
            )
            
            if fvg_15m is None:
                continue
            
            # Find entry on 15m
            entry_result = self.find_entry_15m(
                df_15m, fvg_15m, sweep_datetime, sweep_type
            )
            
            if entry_result is None:
                continue
            
            entry_datetime, entry_price = entry_result
            
            # Check if entry is in trading window
            if not self.is_in_chicago_trading_window(entry_datetime):
                continue
            
            # Determine direction and calculate SL
            if sweep_type == 'bullish':
                # Bullish sweep then reversal = SHORT
                direction = TradeDirection.SHORT
                sl = fvg_15m.gap_high * (1 + self.sl_buffer_pct)
                risk = sl - entry_price
            else:
                # Bearish sweep then reversal = LONG
                direction = TradeDirection.LONG
                sl = fvg_15m.gap_low * (1 - self.sl_buffer_pct)
                risk = entry_price - sl
            
            if risk <= 0:
                continue
            
            setup_id += 1
            setup = TradeSetup(
                setup_id=setup_id,
                htf_fvg=htf_fvg,
                fvg_15m=fvg_15m,
                sweep=LiquiditySweep(
                    datetime=sweep_datetime,
                    sweep_type=sweep_type,
                    level=htf_fvg.gap_high if sweep_type == 'bullish' else htf_fvg.gap_low,
                    high=0, low=0, close=0,
                    timeframe=htf_fvg.timeframe
                ),
                direction=direction,
                entry_datetime=entry_datetime,
                entry_price=entry_price,
                stop_loss=sl,
                risk_points=risk
            )
            setups.append(setup)
        
        print(f"\n[4/4] Found {len(setups)} valid setups in trading window (08:00-18:00 UTC / ~2:00-12:00 Chicago)")
        
        return setups
    
    def generate_report(self, setups: List[TradeSetup], year: int) -> str:
        """Generate analysis report"""
        
        report = []
        report.append("# 📊 Analyse Multi-Timeframe: HTF FVG Sweep + 15m FVG Strategy\n")
        report.append("---\n")
        
        report.append("## 🎯 Logique de la Stratégie\n")
        report.append("""
Cette stratégie combine plusieurs timeframes:

1. **FVG 4H ou 1H**: Identifier un FVG sur le timeframe supérieur
2. **Wick Sweep**: Le prix touche le FVG avec une mèche (pas le corps)
3. **FVG 15m**: Un FVG 15m a été créé juste avant le sweep (pendant le mouvement)
4. **Entrée 15m**: Quand le prix casse et clôture au-delà du FVG 15m après le sweep
5. **Stop Loss**: Au-dessus/en-dessous du FVG 15m cassé

**Fenêtre d'analyse**: 2:00 AM - 12:00 PM heure de Chicago (≈ 08:00-18:00 UTC)
""")
        
        report.append(f"\n## 📈 Résumé {year}\n")
        report.append(f"| Métrique | Valeur |\n")
        report.append(f"|----------|--------|\n")
        report.append(f"| Setups détectés | {len(setups)} |\n")
        
        if setups:
            longs = sum(1 for s in setups if s.direction == TradeDirection.LONG)
            shorts = sum(1 for s in setups if s.direction == TradeDirection.SHORT)
            htf_4h = sum(1 for s in setups if s.htf_fvg.timeframe == '4H')
            htf_1h = sum(1 for s in setups if s.htf_fvg.timeframe == '1H')
            
            report.append(f"| Trades LONG | {longs} |\n")
            report.append(f"| Trades SHORT | {shorts} |\n")
            report.append(f"| Basés sur FVG 4H | {htf_4h} |\n")
            report.append(f"| Basés sur FVG 1H | {htf_1h} |\n")
        
        report.append("\n## 📝 Détail des Setups\n")
        
        for setup in setups[-20:]:  # Show last 20 setups
            direction_emoji = "🟢" if setup.direction == TradeDirection.LONG else "🔴"
            report.append(f"\n### Setup #{setup.setup_id} - {direction_emoji} {setup.direction.value.upper()}\n")
            report.append(f"- **HTF FVG ({setup.htf_fvg.timeframe})**: {setup.htf_fvg.fvg_type.upper()} @ {setup.htf_fvg.datetime}")
            report.append(f"  - Zone: {setup.htf_fvg.gap_low:.2f} - {setup.htf_fvg.gap_high:.2f}")
            report.append(f"- **Sweep**: @ {setup.sweep.datetime}")
            report.append(f"- **FVG 15m**: {setup.fvg_15m.fvg_type.upper()} @ {setup.fvg_15m.datetime}")
            report.append(f"  - Zone: {setup.fvg_15m.gap_low:.2f} - {setup.fvg_15m.gap_high:.2f}")
            report.append(f"- **Entrée**: {setup.entry_price:.2f} @ {setup.entry_datetime}")
            report.append(f"- **Stop Loss**: {setup.stop_loss:.2f}")
            report.append(f"- **Risk**: {setup.risk_points:.2f} points")
            report.append("")
        
        if len(setups) > 20:
            report.append(f"\n*... et {len(setups) - 20} autres setups*\n")
        
        return "\n".join(report)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-TF FVG + Sweep Strategy Analysis')
    parser.add_argument('--year', type=int, default=2025, help='Year to analyze')
    parser.add_argument('--output', type=str, default='MULTI_TF_ANALYSIS.md', help='Output report file')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("MULTI-TIMEFRAME FVG + SWEEP STRATEGY ANALYSIS")
    print("=" * 60)
    
    strategy = MultiTFStrategy()
    
    try:
        setups = strategy.run_analysis(args.year)
        
        # Generate report
        report = strategy.generate_report(setups, args.year)
        
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Report saved to: {output_path.absolute()}")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total setups found: {len(setups)}")
        if setups:
            longs = sum(1 for s in setups if s.direction == TradeDirection.LONG)
            shorts = sum(1 for s in setups if s.direction == TradeDirection.SHORT)
            print(f"   LONG: {longs}, SHORT: {shorts}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
