#!/bin/bash
# Quick start script for NQ London Session Backtest

echo "=========================================="
echo "NQ Futures Backtesting - Quick Start"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import pandas, numpy, pytz" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Installing required dependencies..."
    pip install -r requirements_backtest.txt
else
    echo "✓ All dependencies installed"
fi

echo ""
echo "Running NQ London Session Backtest..."
echo "This may take 30-90 seconds..."
echo ""

# Run the backtest
python3 nq_london_session_backtest.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Backtest completed successfully!"
    echo "=========================================="
    echo ""
    echo "Results saved to: nq_analysis_results.txt"
    echo ""
    echo "Key files created:"
    echo "  - nq_london_session_backtest.py (main script)"
    echo "  - nq_analysis_results.txt (results summary)"
    echo "  - BACKTEST_README.md (detailed documentation)"
    echo ""
else
    echo ""
    echo "Error: Backtest failed. Please check error messages above."
    exit 1
fi
