#!/bin/bash
# Complete Analysis Pipeline
# This script runs the complete backtest and RR analysis pipeline

echo "=================================================="
echo "Complete Backtest & RR Analysis Pipeline"
echo "=================================================="
echo ""

# Step 1: Run backtest strategy
echo "Step 1: Running backtest strategy..."
echo "This identifies trades where 8:30 AM candle breaks previous 5 candles"
echo ""
python3 backtest_strategy.py
if [ $? -ne 0 ]; then
    echo "Error: Backtest strategy failed!"
    exit 1
fi
echo ""

# Step 2: Run RR analysis
echo "Step 2: Running RR analysis..."
echo "This analyzes each trade with 36 different SL/RR combinations"
echo ""
python3 rr_analysis.py
if [ $? -ne 0 ]; then
    echo "Error: RR analysis failed!"
    exit 1
fi
echo ""

# Step 3: Summary
echo "=================================================="
echo "Analysis Complete!"
echo "=================================================="
echo ""
echo "Generated files:"
echo "  - backtest_results.csv           (identified trades)"
echo "  - rr_analysis_complete.csv       (all scenarios)"
echo "  - rr_analysis_SL_100.csv         (SL 100% results)"
echo "  - rr_analysis_SL_75.csv          (SL 75% results)"
echo "  - rr_analysis_SL_50.csv          (SL 50% results)"
echo "  - rr_analysis_SL_25.csv          (SL 25% results)"
echo "  - rr_analysis_summary.csv        (summary statistics)"
echo ""
echo "See RR_ANALYSIS_README.md for detailed documentation"
echo ""
