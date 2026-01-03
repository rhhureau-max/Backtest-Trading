#!/bin/bash
# Quick Start Script for NQ ICT Backtesting

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                   NQ ICT Backtesting - Quick Start                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Validate components
echo ""
echo "Running component validation..."
python3 test_components.py

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                   All systems ready! Starting backtest...                    ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Run backtest
    python3 run_backtest.py
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                         Backtest Complete!                                   ║"
    echo "║                                                                              ║"
    echo "║  Results saved:                                                              ║"
    echo "║  - CSV file: nq_backtest_results_*.csv                                       ║"
    echo "║  - Text report: nq_backtest_report_*.txt                                     ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
else
    echo ""
    echo "❌ Component validation failed. Please check the error messages above."
    exit 1
fi
