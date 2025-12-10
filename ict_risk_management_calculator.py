#!/usr/bin/env python3
"""
ICT Risk Management Calculator
================================

Calculates precise entry and exit parameters for ICT Liquidity Sweep setups
with detailed risk management scenarios.

Author: ICT Strategy Implementation
Date: December 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
from typing import Dict, List, Tuple, Optional
import sys

# Import the main analyzer
from ict_liquidity_sweep_reversal import ICTLiquiditySweepAnalyzer


class ICTRiskManagementCalculator:
    """
    Calculates precise entry, stop loss, and take profit levels for ICT setups.
    """
    
    def __init__(self):
        """Initialize the risk management calculator."""
        self.analyzer = ICTLiquiditySweepAnalyzer()
        
    def calculate_entry_exit_params(self, setup: Dict, candle_data: pd.DataFrame, idx: int) -> Dict:
        """
        Calculate precise entry and exit parameters for a setup.
        
        Args:
            setup: Setup dictionary from analyzer
            candle_data: DataFrame with OHLC data
            idx: Index of the sweep candle
            
        Returns:
            Dictionary with entry/exit parameters
        """
        sweep_info = setup['sweep_info']
        fvg_info = setup['fvg_info']
        
        # Get the sweep candle
        sweep_candle = candle_data.iloc[idx]
        
        # Determine direction
        is_bullish = sweep_info['direction'] == 'bullish_reversal'
        
        # 1. ENTRY POINT - Proximal Line of FVG (start of gap)
        if fvg_info.get('has_fvg'):
            if is_bullish:
                # For bullish reversal, enter at bottom of FVG (proximal line)
                entry_price = fvg_info['gap_bottom']
            else:
                # For bearish reversal, enter at top of FVG (proximal line)
                entry_price = fvg_info['gap_top']
        else:
            # If no FVG, use the close of the sweep candle
            entry_price = sweep_candle['close']
        
        # 2. STOP LOSS SCENARIO A (Conservative) - Extreme of wick
        if is_bullish:
            # For bullish, SL below the low (sweep low)
            sl_conservative = sweep_info['sweep_low']
        else:
            # For bearish, SL above the high (sweep high)
            sl_conservative = sweep_info['sweep_high']
        
        # 3. STOP LOSS SCENARIO B (Aggressive) - Edge of body
        sweep_open = sweep_candle['open']
        sweep_close = sweep_candle['close']
        
        if is_bullish:
            # For bullish, SL at body low (min of open/close)
            sl_aggressive = min(sweep_open, sweep_close)
        else:
            # For bearish, SL at body high (max of open/close)
            sl_aggressive = max(sweep_open, sweep_close)
        
        # 4. Calculate Risk for both scenarios
        risk_conservative = abs(entry_price - sl_conservative)
        risk_aggressive = abs(entry_price - sl_aggressive)
        
        # 5. Calculate Take Profit levels for both scenarios
        tps_conservative = {}
        tps_aggressive = {}
        
        rr_ratios = [1.0, 1.5, 2.0]
        
        for rr in rr_ratios:
            if is_bullish:
                # For bullish, TPs are above entry
                tps_conservative[f'RR_{rr}'] = entry_price + (risk_conservative * rr)
                tps_aggressive[f'RR_{rr}'] = entry_price + (risk_aggressive * rr)
            else:
                # For bearish, TPs are below entry
                tps_conservative[f'RR_{rr}'] = entry_price - (risk_conservative * rr)
                tps_aggressive[f'RR_{rr}'] = entry_price - (risk_aggressive * rr)
        
        return {
            'entry_price': entry_price,
            'direction': 'LONG' if is_bullish else 'SHORT',
            'scenario_a_conservative': {
                'stop_loss': sl_conservative,
                'risk_points': risk_conservative,
                'take_profits': tps_conservative
            },
            'scenario_b_aggressive': {
                'stop_loss': sl_aggressive,
                'risk_points': risk_aggressive,
                'take_profits': tps_aggressive
            },
            'sweep_candle': {
                'open': sweep_open,
                'high': sweep_candle['high'],
                'low': sweep_candle['low'],
                'close': sweep_close
            }
        }
    
    def analyze_with_risk_management(self, year: int = 2024, timeframe: str = '15m') -> List[Dict]:
        """
        Run full analysis with risk management calculations.
        
        Args:
            year: Year to analyze
            timeframe: Timeframe to analyze
            
        Returns:
            List of setups with risk management parameters
        """
        # Load data
        self.analyzer.load_data(year)
        
        # Get base setups
        setups = self.analyzer.analyze_session(
            timeframe=timeframe,
            start_date=f'{year}-01-01',
            end_date=f'{year}-12-31'
        )
        
        # Get the dataframe for this timeframe
        df = self.analyzer.nq_data[timeframe]
        
        # Add risk management calculations to each setup
        enhanced_setups = []
        
        for setup in setups:
            # Find the candle index
            setup_time = setup['datetime']
            
            # Find closest candle
            time_diffs = abs(df['datetime'] - setup_time)
            idx = time_diffs.argmin()
            
            # Calculate entry/exit params
            risk_params = self.calculate_entry_exit_params(setup, df, idx)
            
            # Merge with original setup
            enhanced_setup = {**setup, 'risk_management': risk_params}
            enhanced_setups.append(enhanced_setup)
        
        return enhanced_setups
    
    def backtest_setups(self, setups: List[Dict], df: pd.DataFrame) -> Dict:
        """
        Backtest all setups to calculate win rates.
        
        Args:
            setups: List of enhanced setups with risk management
            df: DataFrame with price data for forward testing
            
        Returns:
            Dictionary with backtest statistics for both scenarios
        """
        results_a = {'wins': 0, 'losses': 0, 'total_profit': 0}
        results_b = {'wins': 0, 'losses': 0, 'total_profit': 0}
        
        for setup in setups:
            rm = setup['risk_management']
            entry = rm['entry_price']
            direction = rm['direction']
            
            # Find the setup time and index
            setup_time = setup['datetime']
            time_diffs = abs(df['datetime'] - setup_time)
            idx = time_diffs.argmin()
            
            # Look forward 100 candles (25 hours on 15m chart)
            forward_window = df.iloc[idx+1:idx+101]  # Start from next candle
            
            if len(forward_window) < 10:
                continue  # Not enough data
            
            # Test Scenario A (Conservative)
            sl_a = rm['scenario_a_conservative']['stop_loss']
            tp_a = rm['scenario_a_conservative']['take_profits']['RR_1.0']
            
            hit_tp_a = False
            hit_sl_a = False
            entry_filled_a = False
            
            for _, candle in forward_window.iterrows():
                # Check if entry is filled first
                if not entry_filled_a:
                    if direction == 'LONG':
                        # For LONG, entry fills if price drops to entry level
                        if candle['low'] <= entry:
                            entry_filled_a = True
                    else:  # SHORT
                        # For SHORT, entry fills if price rises to entry level
                        if candle['high'] >= entry:
                            entry_filled_a = True
                    
                    # If entry not filled yet, continue to next candle
                    if not entry_filled_a:
                        continue
                
                # Once entry is filled, check for TP/SL
                if direction == 'LONG':
                    if candle['low'] <= sl_a:
                        hit_sl_a = True
                        break
                    if candle['high'] >= tp_a:
                        hit_tp_a = True
                        break
                else:  # SHORT
                    if candle['high'] >= sl_a:
                        hit_sl_a = True
                        break
                    if candle['low'] <= tp_a:
                        hit_tp_a = True
                        break
            
            if entry_filled_a:
                if hit_tp_a:
                    results_a['wins'] += 1
                    results_a['total_profit'] += rm['scenario_a_conservative']['risk_points']
                elif hit_sl_a:
                    results_a['losses'] += 1
                    results_a['total_profit'] -= rm['scenario_a_conservative']['risk_points']
            
            # Test Scenario B (Aggressive)
            sl_b = rm['scenario_b_aggressive']['stop_loss']
            tp_b = rm['scenario_b_aggressive']['take_profits']['RR_1.0']
            
            hit_tp_b = False
            hit_sl_b = False
            entry_filled_b = False
            
            for _, candle in forward_window.iterrows():
                # Check if entry is filled first
                if not entry_filled_b:
                    if direction == 'LONG':
                        if candle['low'] <= entry:
                            entry_filled_b = True
                    else:  # SHORT
                        if candle['high'] >= entry:
                            entry_filled_b = True
                    
                    if not entry_filled_b:
                        continue
                
                # Once entry is filled, check for TP/SL
                if direction == 'LONG':
                    if candle['low'] <= sl_b:
                        hit_sl_b = True
                        break
                    if candle['high'] >= tp_b:
                        hit_tp_b = True
                        break
                else:  # SHORT
                    if candle['high'] >= sl_b:
                        hit_sl_b = True
                        break
                    if candle['low'] <= tp_b:
                        hit_tp_b = True
                        break
            
            if entry_filled_b:
                if hit_tp_b:
                    results_b['wins'] += 1
                    results_b['total_profit'] += rm['scenario_b_aggressive']['risk_points']
                elif hit_sl_b:
                    results_b['losses'] += 1
                    results_b['total_profit'] -= rm['scenario_b_aggressive']['risk_points']
        
        # Calculate statistics
        total_a = results_a['wins'] + results_a['losses']
        total_b = results_b['wins'] + results_b['losses']
        
        return {
            'scenario_a': {
                'wins': results_a['wins'],
                'losses': results_a['losses'],
                'total_trades': total_a,
                'win_rate': (results_a['wins'] / total_a * 100) if total_a > 0 else 0,
                'total_profit_points': results_a['total_profit'],
                'total_profit_usd': results_a['total_profit'] * 20,
                'avg_profit_per_trade': (results_a['total_profit'] / total_a) if total_a > 0 else 0
            },
            'scenario_b': {
                'wins': results_b['wins'],
                'losses': results_b['losses'],
                'total_trades': total_b,
                'win_rate': (results_b['wins'] / total_b * 100) if total_b > 0 else 0,
                'total_profit_points': results_b['total_profit'],
                'total_profit_usd': results_b['total_profit'] * 20,
                'avg_profit_per_trade': (results_b['total_profit'] / total_b) if total_b > 0 else 0
            }
        }
    
    def generate_risk_management_report(self, setups: List[Dict], 
                                       backtest_stats: Dict = None,
                                       london_only: bool = False,
                                       ny_only: bool = False) -> str:
        """
        Generate detailed risk management report.
        
        Args:
            setups: List of enhanced setup dictionaries
            backtest_stats: Dictionary with backtest statistics
            london_only: Filter to London killzone only
            ny_only: Filter to NY killzone only
            
        Returns:
            Formatted report string
        """
        # Filter by killzone if requested
        if london_only:
            setups = [s for s in setups if s['killzone'] == 'London Open']
            zone_name = "LONDON KILLZONE (01:00-04:00 CSV Time)"
        elif ny_only:
            setups = [s for s in setups if s['killzone'] == 'NY Open']
            zone_name = "NEW YORK KILLZONE (08:30-11:00 CSV Time)"
        else:
            zone_name = "ALL KILLZONES"
        
        if len(setups) == 0:
            return f"\n⚠️  No setups found for {zone_name}.\n"
        
        # Sort by probability score (highest first)
        setups_sorted = sorted(setups, key=lambda x: x['probability_score'], reverse=True)
        
        report = []
        report.append("\n" + "="*100)
        report.append(f"ICT RISK MANAGEMENT CALCULATOR - {zone_name}")
        report.append("="*100 + "\n")
        
        report.append(f"Total Setups: {len(setups_sorted)}\n")
        
        # Add backtest statistics if available
        if backtest_stats:
            report.append("="*100)
            report.append("📊 BACKTEST RESULTS (RR 1:1)")
            report.append("="*100 + "\n")
            
            stats_a = backtest_stats['scenario_a']
            stats_b = backtest_stats['scenario_b']
            
            report.append("SCENARIO A (CONSERVATIVE - Stop at Wick Extreme):")
            report.append(f"  Total Trades: {stats_a['total_trades']}")
            report.append(f"  Wins: {stats_a['wins']} | Losses: {stats_a['losses']}")
            report.append(f"  Win Rate: {stats_a['win_rate']:.2f}%")
            report.append(f"  Total Profit: {stats_a['total_profit_points']:.2f} points (${stats_a['total_profit_usd']:,.2f})")
            report.append(f"  Avg Profit/Trade: {stats_a['avg_profit_per_trade']:.2f} points")
            
            report.append(f"\nSCENARIO B (AGGRESSIVE - Stop at Body Edge):")
            report.append(f"  Total Trades: {stats_b['total_trades']}")
            report.append(f"  Wins: {stats_b['wins']} | Losses: {stats_b['losses']}")
            report.append(f"  Win Rate: {stats_b['win_rate']:.2f}%")
            report.append(f"  Total Profit: {stats_b['total_profit_points']:.2f} points (${stats_b['total_profit_usd']:,.2f})")
            report.append(f"  Avg Profit/Trade: {stats_b['avg_profit_per_trade']:.2f} points")
            
            report.append(f"\n")
        
        # Show best setup details
        report.append("="*100)
        report.append("BEST SETUP - DETAILED RISK MANAGEMENT PARAMETERS")
        report.append("="*100 + "\n")
        
        best_setup = setups_sorted[0]
        
        # Basic Info
        report.append(f"📅 Date/Time: {best_setup['datetime'].strftime('%Y-%m-%d %H:%M:%S %Z')}")
        report.append(f"⏱️  Timeframe: {best_setup['timeframe']}")
        report.append(f"🎯 Killzone: {best_setup['killzone']}")
        report.append(f"💰 Market Price at Setup: {best_setup['price']:.2f} NQ")
        report.append(f"🎲 Probability Score: {best_setup['probability_score']}/9 ({best_setup['overall_probability']})")
        
        # Setup Details
        sweep = best_setup['sweep_info']
        report.append(f"\n🔄 LIQUIDITY SWEEP:")
        report.append(f"   Type: {sweep['type']}")
        report.append(f"   Sweep Level: {sweep['sweep_level']:.2f}")
        report.append(f"   Expected Direction: {sweep['direction'].replace('_', ' ').title()}")
        
        # Risk Management Parameters
        rm = best_setup['risk_management']
        report.append(f"\n{'='*100}")
        report.append(f"📊 RISK MANAGEMENT PARAMETERS")
        report.append(f"{'='*100}\n")
        
        report.append(f"🎯 ENTRY ORDER:")
        report.append(f"   Order Type: LIMIT ORDER")
        report.append(f"   Entry Price: {rm['entry_price']:.2f} NQ")
        report.append(f"   Direction: {rm['direction']}")
        if best_setup['fvg_info'].get('has_fvg'):
            report.append(f"   Rationale: Proximal Line of FVG (Gap {'Bottom' if rm['direction'] == 'LONG' else 'Top'})")
        else:
            report.append(f"   Rationale: Close of sweep candle (no FVG available)")
        
        # Sweep Candle Details
        sc = rm['sweep_candle']
        report.append(f"\n📊 SWEEP CANDLE STRUCTURE:")
        report.append(f"   Open:  {sc['open']:.2f}")
        report.append(f"   High:  {sc['high']:.2f}")
        report.append(f"   Low:   {sc['low']:.2f}")
        report.append(f"   Close: {sc['close']:.2f}")
        
        # Scenario A - Conservative
        report.append(f"\n{'='*100}")
        report.append(f"📍 SCENARIO A - CONSERVATIVE (Stop Loss at Wick Extreme)")
        report.append(f"{'='*100}\n")
        
        scenario_a = rm['scenario_a_conservative']
        report.append(f"🛑 STOP LOSS: {scenario_a['stop_loss']:.2f} NQ")
        report.append(f"   Location: Extreme of sweep {'low' if rm['direction'] == 'LONG' else 'high'} (absolute wick)")
        report.append(f"   Risk: {scenario_a['risk_points']:.2f} points")
        report.append(f"   Risk in $: ${scenario_a['risk_points'] * 20:.2f} per contract (NQ = $20/point)")
        
        report.append(f"\n💰 TAKE PROFIT LEVELS:")
        for rr_name, tp_price in scenario_a['take_profits'].items():
            rr_value = rr_name.replace('RR_', '')
            reward = abs(tp_price - rm['entry_price'])
            report.append(f"   TP {rr_value} (1:{rr_value}): {tp_price:.2f} NQ")
            report.append(f"      Reward: {reward:.2f} points = ${reward * 20:.2f}")
        
        # Scenario B - Aggressive
        report.append(f"\n{'='*100}")
        report.append(f"📍 SCENARIO B - AGGRESSIVE (Stop Loss at Body Edge)")
        report.append(f"{'='*100}\n")
        
        scenario_b = rm['scenario_b_aggressive']
        report.append(f"🛑 STOP LOSS: {scenario_b['stop_loss']:.2f} NQ")
        report.append(f"   Location: Edge of candle body ({'low' if rm['direction'] == 'LONG' else 'high'} of open/close)")
        report.append(f"   Risk: {scenario_b['risk_points']:.2f} points")
        report.append(f"   Risk in $: ${scenario_b['risk_points'] * 20:.2f} per contract (NQ = $20/point)")
        
        report.append(f"\n💰 TAKE PROFIT LEVELS:")
        for rr_name, tp_price in scenario_b['take_profits'].items():
            rr_value = rr_name.replace('RR_', '')
            reward = abs(tp_price - rm['entry_price'])
            report.append(f"   TP {rr_value} (1:{rr_value}): {tp_price:.2f} NQ")
            report.append(f"      Reward: {reward:.2f} points = ${reward * 20:.2f}")
        
        # Comparison
        report.append(f"\n{'='*100}")
        report.append(f"⚖️  SCENARIO COMPARISON")
        report.append(f"{'='*100}\n")
        
        risk_diff = scenario_a['risk_points'] - scenario_b['risk_points']
        report.append(f"Risk Difference: {risk_diff:.2f} points (${risk_diff * 20:.2f})")
        report.append(f"Conservative requires {risk_diff:.2f} more points of risk")
        report.append(f"")
        
        # Calculate position sizing examples
        report.append(f"📊 POSITION SIZING EXAMPLES (2% Account Risk on $100,000 account):")
        account_risk = 100000 * 0.02  # $2,000
        
        contracts_a = int(account_risk / (scenario_a['risk_points'] * 20))
        contracts_b = int(account_risk / (scenario_b['risk_points'] * 20))
        
        report.append(f"   Scenario A (Conservative): {contracts_a} contracts")
        report.append(f"   Scenario B (Aggressive): {contracts_b} contracts")
        
        # FVG Info
        if best_setup['fvg_info'].get('has_fvg'):
            fvg = best_setup['fvg_info']
            report.append(f"\n📍 FAIR VALUE GAP (Entry Refinement Zone):")
            report.append(f"   Type: {fvg['type']}")
            report.append(f"   Gap Bottom: {fvg['gap_bottom']:.2f}")
            report.append(f"   Gap Top: {fvg['gap_top']:.2f}")
            report.append(f"   Gap Size: {fvg['gap_size']:.2f} points ({fvg['gap_size_pct']:.3f}%)")
        
        # Summary table
        report.append(f"\n{'='*100}")
        report.append(f"📋 QUICK REFERENCE TABLE")
        report.append(f"{'='*100}\n")
        
        report.append(f"{'Parameter':<30} {'Scenario A':<25} {'Scenario B':<25}")
        report.append(f"{'-'*80}")
        
        # Format values separately to avoid nested f-string issues
        entry_a = f"{rm['entry_price']:.2f}"
        entry_b = f"{rm['entry_price']:.2f}"
        sl_a = f"{scenario_a['stop_loss']:.2f}"
        sl_b = f"{scenario_b['stop_loss']:.2f}"
        risk_a = f"{scenario_a['risk_points']:.2f}"
        risk_b = f"{scenario_b['risk_points']:.2f}"
        tp1_a = f"{scenario_a['take_profits']['RR_1.0']:.2f}"
        tp1_b = f"{scenario_b['take_profits']['RR_1.0']:.2f}"
        tp15_a = f"{scenario_a['take_profits']['RR_1.5']:.2f}"
        tp15_b = f"{scenario_b['take_profits']['RR_1.5']:.2f}"
        tp2_a = f"{scenario_a['take_profits']['RR_2.0']:.2f}"
        tp2_b = f"{scenario_b['take_profits']['RR_2.0']:.2f}"
        
        report.append(f"{'Entry Price':<30} {entry_a:<25} {entry_b:<25}")
        report.append(f"{'Direction':<30} {rm['direction']:<25} {rm['direction']:<25}")
        report.append(f"{'Stop Loss':<30} {sl_a:<25} {sl_b:<25}")
        report.append(f"{'Risk (points)':<30} {risk_a:<25} {risk_b:<25}")
        report.append(f"{'TP 1:1':<30} {tp1_a:<25} {tp1_b:<25}")
        report.append(f"{'TP 1:1.5':<30} {tp15_a:<25} {tp15_b:<25}")
        report.append(f"{'TP 1:2':<30} {tp2_a:<25} {tp2_b:<25}")
        
        report.append(f"\n{'='*100}\n")
        
        # Show top 5 other setups summary
        if len(setups_sorted) > 1:
            report.append(f"\n{'='*100}")
            report.append(f"📊 OTHER HIGH PROBABILITY SETUPS IN {zone_name}")
            report.append(f"{'='*100}\n")
            
            for i, setup in enumerate(setups_sorted[1:6], 2):  # Top 5 others
                rm = setup['risk_management']
                report.append(f"SETUP #{i}")
                report.append(f"Date: {setup['datetime'].strftime('%Y-%m-%d %H:%M')} | "
                            f"Score: {setup['probability_score']}/9 | "
                            f"Direction: {rm['direction']}")
                report.append(f"Entry: {rm['entry_price']:.2f} | "
                            f"SL Conservative: {rm['scenario_a_conservative']['stop_loss']:.2f} | "
                            f"SL Aggressive: {rm['scenario_b_aggressive']['stop_loss']:.2f}")
                report.append(f"")
        
        return "\n".join(report)


def main():
    """Main execution function."""
    print("\n" + "="*100)
    print("ICT RISK MANAGEMENT CALCULATOR WITH BACKTESTING")
    print("="*100)
    
    # Initialize calculator
    calculator = ICTRiskManagementCalculator()
    
    # Run analysis for 2024 on 15m timeframe
    print("\n🔍 Analyzing setups with risk management calculations...")
    setups = calculator.analyze_with_risk_management(year=2024, timeframe='15m')
    
    print(f"✓ Found {len(setups)} setups with complete risk management parameters\n")
    
    # Get dataframe for backtesting
    df = calculator.analyzer.nq_data['15m']
    
    # Generate separate reports for each killzone
    print("="*100)
    print("GENERATING KILLZONE-SPECIFIC REPORTS WITH BACKTEST RESULTS")
    print("="*100 + "\n")
    
    # London Killzone - Filter setups and backtest
    print("📍 Analyzing London Killzone (01:00-04:00 CSV time)...")
    london_setups = [s for s in setups if s['killzone'] == 'London Open']
    print(f"  Backtesting {len(london_setups)} London setups...")
    london_backtest = calculator.backtest_setups(london_setups, df)
    london_report = calculator.generate_risk_management_report(
        setups, 
        backtest_stats=london_backtest,
        london_only=True
    )
    print(london_report)
    
    with open("ICT_Risk_Management_London.txt", 'w', encoding='utf-8') as f:
        f.write(london_report)
    print("✅ London killzone report saved to: ICT_Risk_Management_London.txt\n")
    
    # New York Killzone - Filter setups and backtest
    print("📍 Analyzing New York Killzone (08:30-11:00 CSV time)...")
    ny_setups = [s for s in setups if s['killzone'] == 'NY Open']
    print(f"  Backtesting {len(ny_setups)} NY setups...")
    ny_backtest = calculator.backtest_setups(ny_setups, df)
    ny_report = calculator.generate_risk_management_report(
        setups,
        backtest_stats=ny_backtest,
        ny_only=True
    )
    print(ny_report)
    
    with open("ICT_Risk_Management_NewYork.txt", 'w', encoding='utf-8') as f:
        f.write(ny_report)
    print("✅ New York killzone report saved to: ICT_Risk_Management_NewYork.txt\n")
    
    # Combined Report (top setups from all)
    print("📍 Generating combined report...")
    print(f"  Backtesting all {len(setups)} setups...")
    combined_backtest = calculator.backtest_setups(setups, df)
    combined_report = calculator.generate_risk_management_report(
        setups,
        backtest_stats=combined_backtest,
        london_only=False,
        ny_only=False
    )
    
    with open("ICT_Risk_Management_Combined.txt", 'w', encoding='utf-8') as f:
        f.write(combined_report)
    print("✅ Combined report saved to: ICT_Risk_Management_Combined.txt\n")
    
    # Print summary statistics
    print("="*100)
    print("📊 BACKTEST SUMMARY")
    print("="*100 + "\n")
    
    print("LONDON KILLZONE:")
    print(f"  Scenario A: {london_backtest['scenario_a']['win_rate']:.2f}% WR | "
          f"{london_backtest['scenario_a']['total_trades']} trades | "
          f"${london_backtest['scenario_a']['total_profit_usd']:,.2f} profit")
    print(f"  Scenario B: {london_backtest['scenario_b']['win_rate']:.2f}% WR | "
          f"{london_backtest['scenario_b']['total_trades']} trades | "
          f"${london_backtest['scenario_b']['total_profit_usd']:,.2f} profit")
    
    print(f"\nNEW YORK KILLZONE:")
    print(f"  Scenario A: {ny_backtest['scenario_a']['win_rate']:.2f}% WR | "
          f"{ny_backtest['scenario_a']['total_trades']} trades | "
          f"${ny_backtest['scenario_a']['total_profit_usd']:,.2f} profit")
    print(f"  Scenario B: {ny_backtest['scenario_b']['win_rate']:.2f}% WR | "
          f"{ny_backtest['scenario_b']['total_trades']} trades | "
          f"${ny_backtest['scenario_b']['total_profit_usd']:,.2f} profit")
    
    print(f"\nCOMBINED:")
    print(f"  Scenario A: {combined_backtest['scenario_a']['win_rate']:.2f}% WR | "
          f"{combined_backtest['scenario_a']['total_trades']} trades | "
          f"${combined_backtest['scenario_a']['total_profit_usd']:,.2f} profit")
    print(f"  Scenario B: {combined_backtest['scenario_b']['win_rate']:.2f}% WR | "
          f"{combined_backtest['scenario_b']['total_trades']} trades | "
          f"${combined_backtest['scenario_b']['total_profit_usd']:,.2f} profit")
    
    print("\n" + "="*100)
    print("✅ RISK MANAGEMENT ANALYSIS WITH BACKTESTING COMPLETE")
    print("="*100 + "\n")



if __name__ == "__main__":
    main()
