"""
Main Script to Run NQ ICT Backtesting Strategy

This script orchestrates the complete backtest from data loading to results generation.
"""

import sys
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# Import all modules
from data_loader import get_market_data
from backtest_engine import run_backtest
from results_analyzer import ResultsAnalyzer


def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                   NQ ICT SMART MONEY BACKTESTING STRATEGY                    ║
║                                                                              ║
║  Strategy Components:                                                        ║
║  • Trend Filter: H1 & H4 market structure (HH/HL vs LH/LL)                  ║
║  • Opening Range: 08:30 Chicago time (5-minute candle)                      ║
║  • Entry Setup: FVG inversion after breakout & return                       ║
║  • Risk Management: 20-point SL, 3 TPs (20, 30, 40 points)                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main execution function"""
    
    print_banner()
    
    # Configuration
    STOP_LOSS_POINTS = 20.0
    BASE_PATH = "."
    
    print(f"Run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Configuration: SL = {STOP_LOSS_POINTS} points, TPs = [20, 30, 40] points\n")
    
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
        print("\nSTEP 2: Running Backtest")
        print("-" * 80)
        tracker = run_backtest(data, stop_loss_points=STOP_LOSS_POINTS)
        
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
        csv_filename = f"nq_backtest_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        analyzer.export_to_csv(csv_filename)
        print(f"✓ Results exported to {csv_filename}")
        
        # Save text report
        report_filename = f"nq_backtest_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to {report_filename}")
        
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
