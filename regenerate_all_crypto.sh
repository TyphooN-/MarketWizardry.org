#!/bin/bash

# Regenerate all crypto explorer reports with new analysis features
# This script finds all crypto CSV files and regenerates their analysis reports

echo "🔄 Regenerating all crypto explorer reports..."
echo ""

# Find all unique dates from crypto CSV files
dates=$(ls crypto-explorer/SymbolsExport-Darwinex-Live-Crypto-*.csv | \
        sed 's/.*Crypto-\(.*\)\.csv/\1/' | \
        sort -u)

total_dates=$(echo "$dates" | wc -l)
current=0

for date in $dates; do
    current=$((current + 1))
    echo "[$current/$total_dates] Processing date: $date"
    python3 update_all_tools.py "$date" --force-crypto
    echo ""
done

echo "✅ All crypto reports regenerated successfully!"
echo "📊 Processed $total_dates dates"
