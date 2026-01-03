"""
Main Script to Run Updated NQ ICT Backtesting Strategy
Simplified version with EMA filter and permissive FVG entries
"""

import sys
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# Import all modules
from data_loader import get_market_data
from updated_backtest_engine import run_backtest
from results_analyzer import ResultsAnalyzer


def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║            NQ ICT STRATEGY - SIMPLIFIED & PERMISSIVE VERSION                 ║
║                                                                              ║
║  Strategy Components:                                                        ║
║  • Trend Filter: EMA 200 on H1 (Price > EMA = Bullish, Price < EMA = Bear)  ║
║  • Liquidity Grab: Break of 08:30 opening range (Judas Swing)               ║
║  • Entry Setup: ANY FVG touch after liquidity grab (no complex inversion)   ║
║  • Risk Management: 25pt SL, TPs at 20/40 + runner until 15:45              ║
║  • Trading Window: 08:35-11:30 for entries, close all at 15:45              ║
║  • Minimum FVG Size: 2 points                                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main execution function"""
    
    print_banner()
    
    # Configuration
    STOP_LOSS_POINTS = 25.0
    MIN_FVG_SIZE = 2.0
    BASE_PATH = "."
    
    print(f"Run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Configuration:")
    print(f"  • Stop Loss: {STOP_LOSS_POINTS} points")
    print(f"  • Take Profits: 20 points, 40 points, + runner")
    print(f"  • Minimum FVG Size: {MIN_FVG_SIZE} points")
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
        
        # Step 2: Run backtest
        print("\nSTEP 2: Running Updated Backtest")
        print("-" * 80)
        tracker = run_backtest(
            data, 
            stop_loss_points=STOP_LOSS_POINTS,
            min_fvg_size=MIN_FVG_SIZE
        )
        
        print("\n✓ Backtest completed successfully\n")
        
        # Step 3: Analyze results
        print("\nSTEP 3: Analyzing Results")
        print("-" * 80)
        analyzer = ResultsAnalyzer(tracker.get_all_trades())
        
        # Generate and print report
        report = analyzer.generate_report()
        print("\n")
        print(report)
        
        # Export to CSV
        print("\nSTEP 4: Exporting Results")
        print("-" * 80)
        csv_filename = f"nq_updated_backtest_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        analyzer.export_to_csv(csv_filename)
        print(f"✓ Results exported to {csv_filename}")
        
        # Save text report
        report_filename = f"nq_updated_backtest_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to {report_filename}")
        
        # Check if we hit target trade count
        total_trades = len(tracker.get_all_trades())
        print(f"\n{'='*80}")
        print(f"TRADE COUNT ANALYSIS")
        print(f"{'='*80}")
        print(f"Total Trades: {total_trades}")
        if total_trades < 100:
            print(f"⚠️  WARNING: Trade count ({total_trades}) is below target (100)")
            print(f"   Consider further reducing FVG minimum size or relaxing filters")
        else:
            print(f"✓ Trade count target achieved!")
        
        print("\n" + "=" * 80)
        print("BACKTEST COMPLETE!")
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
