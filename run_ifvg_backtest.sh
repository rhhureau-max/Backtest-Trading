#!/bin/bash
# IFVG Backtest Quick Start Script
# This script sets up and runs the IFVG backtest

echo "════════════════════════════════════════════════════════════════"
echo "  🚀 IFVG BACKTEST - QUICK START"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check Python version
echo "1️⃣  Checking Python version..."
python3 --version || { echo "❌ Python 3 not found!"; exit 1; }
echo "✅ Python OK"
echo ""

# Install dependencies
echo "2️⃣  Installing dependencies (pandas, numpy)..."
pip3 install pandas numpy --quiet || { echo "❌ Failed to install dependencies!"; exit 1; }
echo "✅ Dependencies installed"
echo ""

# Check data files
echo "3️⃣  Checking data files..."
data_files=("2018 5m.csv" "2019 5m.csv" "2020 5m.csv" "2021 5m.csv" "2022 5m.csv" "2023 5m.csv" "2024 5m.csv" "2025 5m.csv")
missing_files=0

for file in "${data_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -gt 0 ]; then
    echo "⚠️  Warning: $missing_files data file(s) missing. Backtest will continue with available data."
fi
echo ""

# Run backtest
echo "4️⃣  Running backtest..."
echo "════════════════════════════════════════════════════════════════"
echo ""
python3 ifvg_backtest.py

# Check results
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "5️⃣  Checking results..."

if [ -f "ifvg_trades_results.csv" ]; then
    trade_count=$(wc -l < ifvg_trades_results.csv)
    trade_count=$((trade_count - 1))  # Subtract header
    echo "✅ Results file created: ifvg_trades_results.csv"
    echo "   Total trades recorded: $trade_count"
else
    echo "❌ Results file not found!"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✨ QUICK START COMPLETE"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Files created:"
echo "   • ifvg_backtest.py (main script)"
echo "   • ifvg_trades_results.csv (trade results)"
echo "   • IFVG_STRATEGY_README.md (documentation)"
echo ""
echo "📖 Next steps:"
echo "   • Review the results in ifvg_trades_results.csv"
echo "   • Read IFVG_STRATEGY_README.md for detailed documentation"
echo "   • Adjust parameters in ifvg_backtest.py if needed"
echo "   • Run 'python3 ifvg_backtest.py' again to re-run backtest"
echo ""
