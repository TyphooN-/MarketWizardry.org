#!/bin/bash
# Automated crypto analysis update script
# 1. Fetches latest market data from CoinGecko
# 2. Runs enhanced analysis combining Darwinex + CoinGecko data
# 3. Generates comprehensive report

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "Crypto Analysis Update Pipeline"
echo "========================================="
echo ""

# Check if CSV file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <csv_file>"
    echo "Example: $0 SymbolsExport-Darwinex-Live-Crypto-2025.09.30.csv"
    exit 1
fi

CSV_FILE="$1"
BASE_NAME="${CSV_FILE%.csv}"
MARKET_DATA_FILE="${BASE_NAME}-market-data.json"
ANALYSIS_FILE="${BASE_NAME}-enhanced-analysis.txt"

if [ ! -f "$CSV_FILE" ]; then
    echo "Error: CSV file '$CSV_FILE' not found!"
    exit 1
fi

echo "Input CSV: $CSV_FILE"
echo "Market data output: $MARKET_DATA_FILE"
echo "Analysis output: $ANALYSIS_FILE"
echo ""

# Step 1: Fetch market data from CoinGecko
echo "Step 1: Fetching cryptocurrency market data from CoinGecko..."
echo "This may take 30-60 seconds due to API rate limits..."
python3 fetch_crypto_data.py --output "$MARKET_DATA_FILE" --delay 1.5

if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch market data!"
    exit 1
fi

echo ""
echo "Step 2: Running enhanced analysis..."

# Step 2: Run enhanced analysis
python3 analyze_enhanced.py "$CSV_FILE" --market-data "$MARKET_DATA_FILE" > "$ANALYSIS_FILE"

if [ $? -ne 0 ]; then
    echo "Error: Analysis failed!"
    exit 1
fi

echo ""
echo "========================================="
echo "Analysis Complete!"
echo "========================================="
echo "Market data: $MARKET_DATA_FILE"
echo "Full report: $ANALYSIS_FILE"
echo ""
echo "You can now view the report:"
echo "  cat $ANALYSIS_FILE"
echo ""
