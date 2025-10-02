#!/bin/bash
# Regenerate all explorer analysis files with new formatting

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "REGENERATING ALL EXPLORER ANALYSES"
echo "=========================================="
echo ""

# Counter for progress
total_files=0
processed_files=0
failed_files=0

# Function to process a single file
process_file() {
    local csv_file="$1"
    local script="$2"
    local output_file="$3"

    total_files=$((total_files + 1))

    echo "[$total_files] Processing: $(basename "$csv_file")"

    if python3 "$script" "$csv_file" > "$output_file" 2>&1; then
        processed_files=$((processed_files + 1))
        echo "    ✓ Success"
    else
        failed_files=$((failed_files + 1))
        echo "    ✗ Failed"
    fi
}

# ATR Explorer
echo ""
echo "=== ATR EXPLORER ==="
for csv in atr-explorer/*.csv; do
    [ -f "$csv" ] || continue
    base=$(basename "$csv" .csv)
    output="atr-explorer/${base}-outlier.txt"
    process_file "$csv" "atr-explorer/outlier.py" "$output"
done

# VaR Explorer
echo ""
echo "=== VAR EXPLORER ==="
for csv in var-explorer/*.csv; do
    [ -f "$csv" ] || continue
    base=$(basename "$csv" .csv)
    output="var-explorer/${base}-outlier.txt"
    process_file "$csv" "var-explorer/outlier.py" "$output"
done

# EV Explorer - These scripts generate their own output files, so we run them in the ev-explorer directory
echo ""
echo "=== EV EXPLORER ==="
cd ev-explorer
for csv in *.csv; do
    [ -f "$csv" ] || continue

    total_files=$((total_files + 1))
    echo "[$total_files] Processing: $csv"

    # Check if it has VaR_to_Ask_Ratio column to determine which script to use
    if head -1 "$csv" | grep -q "VaR_to_Ask_Ratio"; then
        if python3 ev_var_outlier.py "$csv" > /dev/null 2>&1; then
            processed_files=$((processed_files + 1))
            echo "    ✓ Success"
        else
            failed_files=$((failed_files + 1))
            echo "    ✗ Failed"
        fi
    else
        if python3 ev_outlier.py "$csv" > /dev/null 2>&1; then
            processed_files=$((processed_files + 1))
            echo "    ✓ Success"
        else
            failed_files=$((failed_files + 1))
            echo "    ✗ Failed"
        fi
    fi
done
cd ..

# Crypto Explorer
echo ""
echo "=== CRYPTO EXPLORER ==="
for csv in crypto-explorer/*.csv; do
    [ -f "$csv" ] || continue
    base=$(basename "$csv" .csv)
    output="crypto-explorer/${base}-enhanced-analysis.txt"

    # Check for companion data files
    market_data="crypto-explorer/crypto_market_data.json"
    news_data="crypto-explorer/crypto_news_data.json"
    events_data="crypto-explorer/crypto_events_data.json"

    args="$csv"
    [ -f "$market_data" ] && args="$args --market-data $market_data"
    [ -f "$news_data" ] && args="$args --news-data $news_data"
    [ -f "$events_data" ] && args="$args --events-data $events_data"

    total_files=$((total_files + 1))
    echo "[$total_files] Processing: $(basename "$csv")"

    if python3 crypto-explorer/analyze_enhanced.py $args > "$output" 2>&1; then
        processed_files=$((processed_files + 1))
        echo "    ✓ Success"
    else
        failed_files=$((failed_files + 1))
        echo "    ✗ Failed"
    fi
done

# Summary
echo ""
echo "=========================================="
echo "REGENERATION COMPLETE"
echo "=========================================="
echo "Total Files: $total_files"
echo "Successful: $processed_files"
echo "Failed: $failed_files"
echo ""

exit 0
