#!/usr/bin/env python3
"""
FVG (Fair Value Gap) Risk/Reward Analysis Script for Nasdaq Mini Futures
Analyzes 8:29 AM Chicago candle FVGs with various Stop Loss placements and R:R ratios
"""

import os
import zipfile
import io
import pandas as pd


def load_csv_data(filepath: str) -> pd.DataFrame:
    """Load CSV data from a file, handling both regular CSV and zipped CSV files."""
    if filepath.endswith('.zip'):
        with zipfile.ZipFile(filepath, 'r') as z:
            csv_names = [n for n in z.namelist() if n.endswith('.csv')]
            if not csv_names:
                raise ValueError(f"No CSV file found in {filepath}")
            with z.open(csv_names[0]) as f:
                df = pd.read_csv(io.BytesIO(f.read()), sep=';')
    else:
        df = pd.read_csv(filepath, sep=';')
    
    return df


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Parse dates and times, and prepare the dataframe for analysis."""
    df.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M:%S')
    df = df.sort_values('datetime').reset_index(drop=True)
    return df


def load_all_data_for_timeframe(data_dir: str, timeframe: str, years: range) -> pd.DataFrame:
    """Load all data for a specific timeframe across multiple years."""
    all_data = []
    
    for year in years:
        if timeframe == '1m':
            if year == 2025:
                filepath = os.path.join(data_dir, f'{year} 1m.csv')
            else:
                filepath = os.path.join(data_dir, f'{year} 1m.csv.zip')
        else:
            filepath = os.path.join(data_dir, f'{year} {timeframe}.csv')
        
        if not os.path.exists(filepath):
            continue
        
        try:
            df = load_csv_data(filepath)
            df = prepare_dataframe(df)
            all_data.append(df)
        except Exception:
            pass
    
    if not all_data:
        return pd.DataFrame()
    
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values('datetime').reset_index(drop=True)
    return combined


def identify_fvg_with_details(df: pd.DataFrame, target_time: str = '08:29:00') -> pd.DataFrame:
    """
    Identify Fair Value Gaps (FVG) at a specific candle time with all necessary details
    for Stop Loss and Take Profit calculations.
    """
    target_candles = df[df['time'] == target_time].copy()
    fvg_data = []
    
    for idx in target_candles.index:
        if idx < 1 or idx >= len(df) - 1:
            continue
        
        candle_n_minus_1 = df.iloc[idx - 1]
        candle_n = df.iloc[idx]
        candle_n_plus_1 = df.iloc[idx + 1]
        
        high_n_minus_1 = candle_n_minus_1['high']
        low_n_minus_1 = candle_n_minus_1['low']
        low_n_plus_1 = candle_n_plus_1['low']
        high_n_plus_1 = candle_n_plus_1['high']
        
        fvg_type = None
        
        # BULLISH FVG: LOW of N+1 > HIGH of N-1
        if low_n_plus_1 > high_n_minus_1:
            fvg_type = 'BULLISH'
        # BEARISH FVG: HIGH of N+1 < LOW of N-1
        elif high_n_plus_1 < low_n_minus_1:
            fvg_type = 'BEARISH'
        
        if fvg_type:
            # Calculate FVG boundaries
            if fvg_type == 'BULLISH':
                fvg_top = low_n_plus_1
                fvg_bottom = high_n_minus_1
            else:  # BEARISH
                fvg_top = low_n_minus_1
                fvg_bottom = high_n_plus_1
            
            fvg_middle = (fvg_top + fvg_bottom) / 2
            
            # Body of candle N (8h29)
            body_top_n = max(candle_n['open'], candle_n['close'])
            body_bottom_n = min(candle_n['open'], candle_n['close'])
            
            fvg_data.append({
                'datetime': candle_n['datetime'],
                'date': candle_n['date'],
                'fvg_type': fvg_type,
                'high_n_minus_1': high_n_minus_1,
                'low_n_minus_1': low_n_minus_1,
                'open_n': candle_n['open'],
                'high_n': candle_n['high'],
                'low_n': candle_n['low'],
                'close_n': candle_n['close'],
                'body_top_n': body_top_n,
                'body_bottom_n': body_bottom_n,
                'low_n_plus_1': low_n_plus_1,
                'high_n_plus_1': high_n_plus_1,
                'fvg_top': fvg_top,
                'fvg_bottom': fvg_bottom,
                'fvg_middle': fvg_middle,
                'idx_n': idx
            })
    
    return pd.DataFrame(fvg_data)


def calculate_stop_loss(fvg: pd.Series, sl_type: str) -> float:
    """
    Calculate stop loss level based on the type.
    
    SL Types:
    - 'sl1': Under LOW of N+1 (bullish) / Above HIGH of N+1 (bearish)
    - 'sl2': Middle of FVG
    - 'sl3': Under body of N (bullish) / Above body of N (bearish)
    - 'sl4': Under wick of N (bullish) / Above wick of N (bearish)
    """
    fvg_type = fvg['fvg_type']
    
    if sl_type == 'sl1':
        # Under LOW of N+1 (bullish) / Above HIGH of N+1 (bearish)
        if fvg_type == 'BULLISH':
            return fvg['low_n_plus_1']
        else:
            return fvg['high_n_plus_1']
    
    elif sl_type == 'sl2':
        # Middle of FVG
        return fvg['fvg_middle']
    
    elif sl_type == 'sl3':
        # Under body of N (bullish) / Above body of N (bearish)
        if fvg_type == 'BULLISH':
            return fvg['body_bottom_n']
        else:
            return fvg['body_top_n']
    
    elif sl_type == 'sl4':
        # Under wick/candle of N (bullish) / Above wick/candle of N (bearish)
        if fvg_type == 'BULLISH':
            return fvg['low_n']
        else:
            return fvg['high_n']
    
    return None


def calculate_rr_results(df: pd.DataFrame, fvg_df: pd.DataFrame, 
                         rr_ratios: list, sl_type: str, max_candles: int = 100) -> dict:
    """
    Calculate win probability for each R:R ratio with given stop loss type.
    
    Entry is at OPEN of candle N+2.
    - For BULLISH: SL below entry, TP above entry
    - For BEARISH: SL above entry, TP below entry
    """
    results = {
        'global': {rr: {'wins': 0, 'losses': 0, 'total': 0} for rr in rr_ratios},
        'bullish': {rr: {'wins': 0, 'losses': 0, 'total': 0} for rr in rr_ratios},
        'bearish': {rr: {'wins': 0, 'losses': 0, 'total': 0} for rr in rr_ratios}
    }
    
    for _, fvg in fvg_df.iterrows():
        idx_n = fvg['idx_n']
        fvg_type = fvg['fvg_type']
        
        # Entry at candle N+2
        entry_idx = idx_n + 2
        
        if entry_idx >= len(df):
            continue
        
        entry_price = df.iloc[entry_idx]['open']
        sl_level = calculate_stop_loss(fvg, sl_type)
        
        if sl_level is None:
            continue
        
        # Calculate risk (distance to SL)
        if fvg_type == 'BULLISH':
            risk = entry_price - sl_level
            if risk <= 0:
                continue  # Invalid setup
        else:  # BEARISH
            risk = sl_level - entry_price
            if risk <= 0:
                continue  # Invalid setup
        
        for rr in rr_ratios:
            # Calculate take profit level
            reward = risk * rr
            
            if fvg_type == 'BULLISH':
                tp_level = entry_price + reward
            else:  # BEARISH
                tp_level = entry_price - reward
            
            # Check if TP or SL is hit first within max_candles
            end_idx = min(entry_idx + max_candles, len(df))
            
            outcome = None
            for i in range(entry_idx, end_idx):
                candle = df.iloc[i]
                
                if fvg_type == 'BULLISH':
                    # Check SL first (low touches or goes below SL)
                    if candle['low'] <= sl_level:
                        outcome = 'loss'
                        break
                    # Check TP (high touches or goes above TP)
                    if candle['high'] >= tp_level:
                        outcome = 'win'
                        break
                else:  # BEARISH
                    # Check SL first (high touches or goes above SL)
                    if candle['high'] >= sl_level:
                        outcome = 'loss'
                        break
                    # Check TP (low touches or goes below TP)
                    if candle['low'] <= tp_level:
                        outcome = 'win'
                        break
            
            if outcome:
                results['global'][rr]['total'] += 1
                results[fvg_type.lower()][rr]['total'] += 1
                
                if outcome == 'win':
                    results['global'][rr]['wins'] += 1
                    results[fvg_type.lower()][rr]['wins'] += 1
                else:
                    results['global'][rr]['losses'] += 1
                    results[fvg_type.lower()][rr]['losses'] += 1
    
    return results


def generate_markdown_report(all_results: dict, total_fvg_counts: dict, 
                             rr_ratios: list, sl_descriptions: dict) -> str:
    """Generate a markdown report with all R:R analysis results."""
    
    lines = []
    lines.append("# Analyse FVG Risk/Reward 8h29 - Nasdaq Mini Futures")
    lines.append("")
    lines.append("## 📊 Résumé de l'analyse")
    lines.append("")
    lines.append("**Instrument:** Nasdaq Mini Futures")
    lines.append("**Période analysée:** 2018-2025")
    lines.append("**Bougie cible:** 08:29:00 (Heure Chicago) / 15:29:00 (Heure Paris)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📈 Méthodologie")
    lines.append("")
    lines.append("### Définition du FVG")
    lines.append("- **FVG Haussier:** LOW de N+1 > HIGH de N-1")
    lines.append("- **FVG Baissier:** HIGH de N+1 < LOW de N-1")
    lines.append("")
    lines.append("### Stratégie d'entrée")
    lines.append("- **1 minute:** Entrée à 8h31 (ouverture de N+2)")
    lines.append("- **5 minutes:** Entrée à 8h39 (ouverture de N+2)")
    lines.append("- **15 minutes:** Entrée à 8h59 (ouverture de N+2)")
    lines.append("")
    lines.append("### Types de Stop Loss analysés")
    for sl_key, sl_desc in sl_descriptions.items():
        lines.append(f"- **{sl_key.upper()}:** {sl_desc}")
    lines.append("")
    lines.append("### Ratios Risk/Reward analysés")
    lines.append(f"- {', '.join([str(rr) for rr in rr_ratios])}")
    lines.append("")
    lines.append("---")
    
    # Results for each timeframe
    for timeframe in ['1m', '5m', '15m']:
        if timeframe == '1m':
            tf_display = "1 Minute"
        elif timeframe == '5m':
            tf_display = "5 Minutes"
        else:
            tf_display = "15 Minutes"
        
        lines.append("")
        lines.append(f"## ⏱️ Timeframe {tf_display}")
        lines.append("")
        
        fvg_counts = total_fvg_counts.get(timeframe, {'total': 0, 'bullish': 0, 'bearish': 0})
        lines.append(f"**Total FVG détectés:** {fvg_counts['total']} (Haussiers: {fvg_counts['bullish']}, Baissiers: {fvg_counts['bearish']})")
        lines.append("")
        
        # For each SL type
        for sl_type in ['sl1', 'sl2', 'sl3', 'sl4']:
            sl_desc = sl_descriptions[sl_type]
            lines.append(f"### {sl_type.upper()}: {sl_desc}")
            lines.append("")
            
            results = all_results.get(timeframe, {}).get(sl_type, {})
            
            # Global results table
            lines.append("#### Résultats Globaux")
            lines.append("")
            lines.append("| R:R | Trades | Wins | Losses | Win Rate |")
            lines.append("|:---:|:------:|:----:|:------:|:--------:|")
            
            for rr in rr_ratios:
                data = results.get('global', {}).get(rr, {'wins': 0, 'losses': 0, 'total': 0})
                total = data['total']
                wins = data['wins']
                losses = data['losses']
                win_rate = f"{(wins/total*100):.2f}%" if total > 0 else "N/A"
                lines.append(f"| {rr} | {total} | {wins} | {losses} | {win_rate} |")
            
            lines.append("")
            
            # Bullish results table
            lines.append("#### FVG Haussiers")
            lines.append("")
            lines.append("| R:R | Trades | Wins | Losses | Win Rate |")
            lines.append("|:---:|:------:|:----:|:------:|:--------:|")
            
            for rr in rr_ratios:
                data = results.get('bullish', {}).get(rr, {'wins': 0, 'losses': 0, 'total': 0})
                total = data['total']
                wins = data['wins']
                losses = data['losses']
                win_rate = f"{(wins/total*100):.2f}%" if total > 0 else "N/A"
                lines.append(f"| {rr} | {total} | {wins} | {losses} | {win_rate} |")
            
            lines.append("")
            
            # Bearish results table
            lines.append("#### FVG Baissiers")
            lines.append("")
            lines.append("| R:R | Trades | Wins | Losses | Win Rate |")
            lines.append("|:---:|:------:|:----:|:------:|:--------:|")
            
            for rr in rr_ratios:
                data = results.get('bearish', {}).get(rr, {'wins': 0, 'losses': 0, 'total': 0})
                total = data['total']
                wins = data['wins']
                losses = data['losses']
                win_rate = f"{(wins/total*100):.2f}%" if total > 0 else "N/A"
                lines.append(f"| {rr} | {total} | {wins} | {losses} | {win_rate} |")
            
            lines.append("")
        
        lines.append("---")
    
    lines.append("")
    lines.append("*Analyse générée automatiquement par le script `fvg_rr_analysis_829.py`*")
    
    return "\n".join(lines)


def main():
    """Main function to run the FVG R:R analysis for 8:29 candle."""
    # Configuration
    data_dir = os.path.dirname(os.path.abspath(__file__))
    years = range(2018, 2026)
    timeframes = ['1m', '5m', '15m']
    rr_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    sl_types = ['sl1', 'sl2', 'sl3', 'sl4']
    target_time = '08:29:00'
    
    sl_descriptions = {
        'sl1': "Stop Loss sous le LOW de N+1 (haussier) / au-dessus du HIGH de N+1 (baissier)",
        'sl2': "Stop Loss au milieu du FVG de 8h29",
        'sl3': "Stop Loss sous le corps de la bougie 8h29 (haussier) / au-dessus (baissier)",
        'sl4': "Stop Loss sous la mèche de la bougie 8h29 (haussier) / au-dessus (baissier)"
    }
    
    print("=" * 60)
    print("=== ANALYSE FVG Risk/Reward 8h29 - Nasdaq Mini Futures ===")
    print("=" * 60)
    print(f"Période : {years.start}-{years.stop - 1}")
    print(f"Bougie cible : {target_time} (Chicago Time)")
    print(f"Ratios R:R : {rr_ratios}")
    print()
    
    all_results = {}
    total_fvg_counts = {}
    
    for timeframe in timeframes:
        print(f"\nChargement des données {timeframe}...")
        
        df = load_all_data_for_timeframe(data_dir, timeframe, years)
        
        if df.empty:
            print(f"Aucune donnée disponible pour le timeframe {timeframe}")
            continue
        
        print(f"Total: {len(df)} lignes chargées")
        
        # Identify FVGs
        fvg_df = identify_fvg_with_details(df, target_time)
        
        if fvg_df.empty:
            print(f"Aucun FVG détecté pour le timeframe {timeframe}")
            continue
        
        bullish_count = len(fvg_df[fvg_df['fvg_type'] == 'BULLISH'])
        bearish_count = len(fvg_df[fvg_df['fvg_type'] == 'BEARISH'])
        
        total_fvg_counts[timeframe] = {
            'total': len(fvg_df),
            'bullish': bullish_count,
            'bearish': bearish_count
        }
        
        print(f"FVG détectés: {len(fvg_df)} (Haussiers: {bullish_count}, Baissiers: {bearish_count})")
        
        all_results[timeframe] = {}
        
        for sl_type in sl_types:
            print(f"  Calcul pour {sl_type.upper()}...")
            results = calculate_rr_results(df, fvg_df, rr_ratios, sl_type)
            all_results[timeframe][sl_type] = results
    
    # Generate markdown report
    print("\nGénération du rapport markdown...")
    report = generate_markdown_report(all_results, total_fvg_counts, rr_ratios, sl_descriptions)
    
    # Save report
    report_path = os.path.join(data_dir, 'analyse_rr_829.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nRapport sauvegardé: {report_path}")
    
    # Also print summary to console
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    for timeframe in timeframes:
        if timeframe not in all_results:
            continue
        
        if timeframe == '1m':
            tf_display = "1 MINUTE"
        elif timeframe == '5m':
            tf_display = "5 MINUTES"
        else:
            tf_display = "15 MINUTES"
        
        print(f"\nTIMEFRAME {tf_display}:")
        
        for sl_type in sl_types:
            results = all_results[timeframe].get(sl_type, {})
            print(f"\n  {sl_type.upper()}: {sl_descriptions[sl_type][:50]}...")
            print(f"  R:R   |  Global  | Haussier | Baissier")
            print(f"  ------|----------|----------|----------")
            
            for rr in rr_ratios:
                global_data = results.get('global', {}).get(rr, {'wins': 0, 'total': 0})
                bullish_data = results.get('bullish', {}).get(rr, {'wins': 0, 'total': 0})
                bearish_data = results.get('bearish', {}).get(rr, {'wins': 0, 'total': 0})
                
                g_rate = f"{(global_data['wins']/global_data['total']*100):6.2f}%" if global_data['total'] > 0 else "  N/A  "
                b_rate = f"{(bullish_data['wins']/bullish_data['total']*100):6.2f}%" if bullish_data['total'] > 0 else "  N/A  "
                be_rate = f"{(bearish_data['wins']/bearish_data['total']*100):6.2f}%" if bearish_data['total'] > 0 else "  N/A  "
                
                print(f"  {rr:4.1f}  | {g_rate} | {b_rate} | {be_rate}")
    
    print("\n" + "=" * 60)
    print("Analyse terminée.")
    print("=" * 60)


if __name__ == "__main__":
    main()
