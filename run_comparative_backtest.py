"""
Main Script to Run Comparative Risk Management Backtest
Tests 3 different exit strategies on the same entry signals
"""

import sys
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

from data_loader import get_market_data
from comparative_backtest_engine import run_comparative_backtest
from comparative_results_analyzer import ComparativeResultsAnalyzer


def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           COMPARATIVE RISK MANAGEMENT STRATEGIES - NQ ICT                    ║
║                                                                              ║
║  Testing 3 exit strategies on the SAME entry signals:                       ║
║                                                                              ║
║  Strategy A: Scalper Fixe (SL 20pts, TP 25pts fixed)                        ║
║  Strategy B: ICT Liquidité Range (SL ±2pts candle, TP range)                ║
║  Strategy C: Standard Deviation (SL 20pts, TP 2x/4x H_Range + BE)           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main execution function"""
    
    print_banner()
    
    # Configuration
    MIN_FVG_SIZE = 2.0
    BASE_PATH = "."
    
    print(f"Run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Configuration:")
    print(f"  • Minimum FVG Size: {MIN_FVG_SIZE} points")
    print(f"  • Entry Logic: Same for all strategies (EMA 200 + FVG touch)")
    print()
    
    try:
        # Step 1: Load data
        print("STEP 1: Loading Market Data")
        print("-" * 80)
        data = get_market_data(BASE_PATH)
        
        if not data:
            print("\n❌ ERROR: No data loaded. Please check data files.")
            sys.exit(1)
        
        print("\n✓ Data loaded successfully\n")
        
        # Step 2: Run comparative backtest
        print("\nSTEP 2: Running Comparative Backtest")
        print("-" * 80)
        results = run_comparative_backtest(data, min_fvg_size=MIN_FVG_SIZE)
        
        print("\n✓ Comparative backtest completed successfully\n")
        
        # Step 3: Analyze and compare results
        print("\nSTEP 3: Analyzing and Comparing Results")
        print("-" * 80)
        analyzer = ComparativeResultsAnalyzer(results)
        
        # Generate comparison table
        comp_table = analyzer.generate_comparison_table()
        
        # Generate and print detailed report
        report = analyzer.generate_detailed_report()
        print("\n")
        print(report)
        
        # Step 4: Export results
        print("\nSTEP 4: Exporting Results")
        print("-" * 80)
        
        # Save comparison table
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f"comparative_strategies_{timestamp}.csv"
        analyzer.export_to_csv(csv_filename)
        print(f"✓ Detailed results exported to {csv_filename}")
        
        # Save summary table
        summary_filename = f"comparative_summary_{timestamp}.csv"
        comp_table.to_csv(summary_filename, index=False)
        print(f"✓ Summary table exported to {summary_filename}")
        
        # Save text report
        report_filename = f"comparative_report_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to {report_filename}")
        
        # Show best strategy
        print(f"\n{'='*80}")
        print("BEST STRATEGY BY METRIC")
        print(f"{'='*80}")
        
        best_pnl = comp_table.loc[comp_table['total_pnl'].idxmax()]
        print(f"Highest Total PnL: {best_pnl['strategy']} (+{best_pnl['total_pnl']:.2f} points)")
        
        best_wr = comp_table.loc[comp_table['win_rate'].idxmax()]
        print(f"Highest Win Rate:  {best_wr['strategy']} ({best_wr['win_rate']:.2f}%)")
        
        best_pf = comp_table.loc[comp_table['profit_factor'].idxmax()]
        pf_val = f"{best_pf['profit_factor']:.2f}" if best_pf['profit_factor'] != float('inf') else "∞"
        print(f"Best Profit Factor: {best_pf['strategy']} ({pf_val})")
        
        print("\n" + "=" * 80)
        print("COMPARATIVE BACKTEST COMPLETE!")
        print("=" * 80)
        print(f"\nRun completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Return success
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠ Backtest interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
