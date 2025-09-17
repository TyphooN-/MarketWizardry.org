#!/bin/bash
source ~/venv/bin/activate
set -e

# Function to show usage
show_usage() {
    echo "Usage: $0 <date> [options]"
    echo ""
    echo "Options:"
    echo "  --force-calculator    Force calculator update even if data appears current"
    echo "  --skip-calculator     Skip calculator update entirely"
    echo "  --quiet              Reduce output verbosity"
    echo "  --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 2025.09.17                    # Normal update with auto calculator sync"
    echo "  $0 2025.09.17 --force-calculator # Force calculator update"
    echo "  $0 2025.09.17 --skip-calculator  # Skip calculator update"
    echo "  $0 2025.09.17 --quiet           # Minimal output"
}

# Parse command line arguments
DATE=""
FORCE_CALCULATOR=false
SKIP_CALCULATOR=false
QUIET=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --force-calculator)
            FORCE_CALCULATOR=true
            shift
            ;;
        --skip-calculator)
            SKIP_CALCULATOR=true
            shift
            ;;
        --quiet)
            QUIET=true
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        -*)
            echo "Unknown option $1"
            show_usage
            exit 1
            ;;
        *)
            if [ -z "$DATE" ]; then
                DATE=$1
            else
                echo "Multiple dates provided: $DATE and $1"
                show_usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate required date parameter
if [ -z "$DATE" ]; then
    echo "❌ Error: Date parameter is required"
    show_usage
    exit 1
fi

# Set output verbosity
if [ "$QUIET" = true ]; then
    QUIET_FLAG="--quiet"
    CALCULATOR_QUIET="--quiet"
else
    QUIET_FLAG=""
    CALCULATOR_QUIET=""
fi

# Validate date format (basic check)
if [[ ! "$DATE" =~ ^[0-9]{4}\.[0-9]{2}\.[0-9]{2}$ ]]; then
    echo "⚠️ Warning: Date format should be YYYY.MM.DD (e.g., 2025.09.17)"
fi

echo "🚀 ENHANCED EXPLORER UPDATE SCRIPT"
if [ "$QUIET" = false ]; then
    echo "📅 Date: $DATE"
    echo "⚡ Force Calculator: $FORCE_CALCULATOR"
    echo "⏭️ Skip Calculator: $SKIP_CALCULATOR"
    echo "🔇 Quiet Mode: $QUIET"
    echo "=" * 50
fi

# --- Copy CSV files from MetaTrader directories ---
[ "$QUIET" = false ] && echo "📂 Copying CSV files for $DATE from MetaTrader directories..."

FILES_COPIED=0

# Copy Stocks CSV from mt5_9
STOCKS_FILE="/home/typhoon/.mt5_9/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-Stocks-$DATE.csv"
if [ -f "$STOCKS_FILE" ]; then
    cp "$STOCKS_FILE" var-explorer/
    [ "$QUIET" = false ] && echo "✅ Copied Stocks CSV for $DATE"
    FILES_COPIED=$((FILES_COPIED + 1))
else
    echo "⚠️ Warning: Stocks CSV not found for $DATE in mt5_9"
fi

# Copy CFD CSV from mt5_10
CFD_FILE="/home/typhoon/.mt5_10/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-CFD-$DATE.csv"
if [ -f "$CFD_FILE" ]; then
    cp "$CFD_FILE" var-explorer/
    [ "$QUIET" = false ] && echo "✅ Copied CFD CSV for $DATE"
    FILES_COPIED=$((FILES_COPIED + 1))
else
    echo "⚠️ Warning: CFD CSV not found for $DATE in mt5_10"
fi

# Copy Futures CSV from mt5_11
FUTURES_FILE="/home/typhoon/.mt5_11/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-Futures-$DATE.csv"
if [ -f "$FUTURES_FILE" ]; then
    cp "$FUTURES_FILE" var-explorer/
    [ "$QUIET" = false ] && echo "✅ Copied Futures CSV for $DATE"
    FILES_COPIED=$((FILES_COPIED + 1))
else
    echo "⚠️ Warning: Futures CSV not found for $DATE in mt5_11"
fi

# Check if any files were copied
if [ "$FILES_COPIED" -eq 0 ]; then
    echo "❌ Error: No CSV files found for date $DATE"
    echo "💡 Check if MetaTrader has generated the files or if the date format is correct"
    exit 1
fi

[ "$QUIET" = false ] && echo "📊 Successfully copied $FILES_COPIED CSV file(s)"

# --- Var Explorer ---
[ "$QUIET" = false ] && echo "📈 Updating VaR Explorer..."
(cd var-explorer && bash run_outlier_analysis.sh)
python3 var-explorer.py

# --- EV Explorer ---
[ "$QUIET" = false ] && echo "💰 Updating EV Explorer..."
if [ -f "var-explorer/SymbolsExport-Darwinex-Live-Stocks-$DATE.csv" ]; then
    cp "var-explorer/SymbolsExport-Darwinex-Live-Stocks-$DATE.csv" ev-explorer/
    (cd ev-explorer && python3 evscrape.py "SymbolsExport-Darwinex-Live-Stocks-$DATE.csv")
    (cd ev-explorer && python3 ev_outlier.py "SymbolsExport-Darwinex-Live-Stocks-$DATE-EV.csv")
    (cd ev-explorer && python3 ev_var_outlier.py "SymbolsExport-Darwinex-Live-Stocks-$DATE-EV.csv")
    python3 ev-explorer.py
else
    echo "⚠️ Warning: No stocks CSV available for EV explorer"
fi

# --- ATR Explorer ---
[ "$QUIET" = false ] && echo "⚡ Updating ATR Explorer..."
# Copy available CSV files to ATR explorer
for file in "var-explorer/SymbolsExport-Darwinex-Live-CFD-$DATE.csv" \
           "var-explorer/SymbolsExport-Darwinex-Live-Stocks-$DATE.csv" \
           "var-explorer/SymbolsExport-Darwinex-Live-Futures-$DATE.csv"; do
    if [ -f "$file" ]; then
        cp "$file" atr-explorer/
        [ "$QUIET" = false ] && echo "  📋 Copied $(basename "$file") to ATR explorer"
    fi
done

(cd atr-explorer && bash run_outlier_analysis.sh)
python3 atr-explorer.py

# --- CALCULATOR UPDATE ---
if [ "$SKIP_CALCULATOR" = true ]; then
    [ "$QUIET" = false ] && echo "⏭️ Skipping calculator update as requested"
else
    [ "$QUIET" = false ] && echo "🧮 Updating calculator with latest data..."

    # Determine calculator update flags
    CALC_FLAGS="$CALCULATOR_QUIET"
    if [ "$FORCE_CALCULATOR" = true ]; then
        CALC_FLAGS="$CALC_FLAGS --force"
        [ "$QUIET" = false ] && echo "⚡ Using force mode for calculator update"
    fi

    # Check if enhanced update script exists
    if [ -f "update_calculator_validated.py" ]; then
        if python3 update_calculator_validated.py $CALC_FLAGS; then
            [ "$QUIET" = false ] && echo "✅ Calculator updated successfully"
        else
            echo "❌ Calculator update failed"
            exit 1
        fi
    elif [ -f "update_calculator_with_latest_data.py" ]; then
        if python3 update_calculator_with_latest_data.py; then
            [ "$QUIET" = false ] && echo "✅ Calculator updated with fallback script"
        else
            echo "❌ Calculator update failed"
            exit 1
        fi
    else
        echo "⚠️ Warning: No calculator update script found"
    fi
fi

# --- FINAL VERIFICATION ---
if [ "$QUIET" = false ]; then
    echo ""
    echo "🔍 FINAL VERIFICATION"
    echo "===================="

    # Show calculator timestamp if updated
    if [ "$SKIP_CALCULATOR" = false ] && [ -f "calculator.html" ]; then
        CALC_TIMESTAMP=$(grep -o "Auto-updated.*[0-9][0-9]:[0-9][0-9]" calculator.html 2>/dev/null | tail -1 || echo "No timestamp found")
        echo "🧮 Calculator: $CALC_TIMESTAMP"

        # Count symbols in calculator
        SYMBOL_COUNT=$(grep -o "'[A-Z0-9_][A-Z0-9_]*':" calculator.html 2>/dev/null | wc -l || echo "0")
        echo "📊 Symbols in calculator: $SYMBOL_COUNT"
    fi

    # Show CSV file timestamps
    echo "📈 Latest CSV files:"
    for file in var-explorer/*$DATE*.csv; do
        if [ -f "$file" ]; then
            FILE_TIME=$(ls -l "$file" | awk '{print $6" "$7" "$8}')
            echo "   $(basename "$file"): $FILE_TIME"
        fi
    done

    echo ""
    echo "🎯 Explorer update complete for $DATE!"
    echo "✅ All systems synchronized and ready"
else
    echo "✅ Explorer update complete for $DATE"
fi

# Return success
exit 0