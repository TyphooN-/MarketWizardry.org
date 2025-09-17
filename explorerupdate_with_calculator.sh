#!/bin/bash
source ~/venv/bin/activate
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <date>"
  exit 1
fi

DATE=$1

# --- Copy CSV files from MetaTrader directories ---
echo "Copying CSV files for $DATE from MetaTrader directories..."

# Copy Stocks CSV from mt5_9
STOCKS_FILE="/home/typhoon/.mt5_9/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-Stocks-$DATE.csv"
if [ -f "$STOCKS_FILE" ]; then
  cp "$STOCKS_FILE" var-explorer/
  echo "Copied Stocks CSV for $DATE"
else
  echo "Warning: Stocks CSV not found for $DATE in mt5_9"
fi

# Copy CFD CSV from mt5_10
CFD_FILE="/home/typhoon/.mt5_10/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-CFD-$DATE.csv"
if [ -f "$CFD_FILE" ]; then
  cp "$CFD_FILE" var-explorer/
  echo "Copied CFD CSV for $DATE"
else
  echo "Warning: CFD CSV not found for $DATE in mt5_10"
fi

# Copy Futures CSV from mt5_11
FUTURES_FILE="/home/typhoon/.mt5_11/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-Futures-$DATE.csv"
if [ -f "$FUTURES_FILE" ]; then
  cp "$FUTURES_FILE" var-explorer/
  echo "Copied Futures CSV for $DATE"
else
  echo "Warning: Futures CSV not found for $DATE in mt5_11"
fi

# --- Var Explorer ---
echo "Updating VaR Explorer..."
(cd var-explorer && bash run_outlier_analysis.sh)
python3 var-explorer.py

# --- EV Explorer ---
echo "Updating EV Explorer..."
cp "var-explorer/SymbolsExport-Darwinex-Live-Stocks-$DATE.csv" ev-explorer/
(cd ev-explorer && python3 evscrape.py "SymbolsExport-Darwinex-Live-Stocks-$DATE.csv")
(cd ev-explorer && python3 ev_outlier.py "SymbolsExport-Darwinex-Live-Stocks-$DATE-EV.csv")
(cd ev-explorer && python3 ev_var_outlier.py "SymbolsExport-Darwinex-Live-Stocks-$DATE-EV.csv")
python3 ev-explorer.py

# --- ATR Explorer ---
echo "Updating ATR Explorer..."
cp "var-explorer/SymbolsExport-Darwinex-Live-CFD-$DATE.csv" atr-explorer/
cp "var-explorer/SymbolsExport-Darwinex-Live-Stocks-$DATE.csv" atr-explorer/
cp "var-explorer/SymbolsExport-Darwinex-Live-Futures-$DATE.csv" atr-explorer/
(cd atr-explorer && bash run_outlier_analysis.sh)
python3 atr-explorer.py

# --- CALCULATOR UPDATE (NEW) ---
echo "🔄 Updating calculator with latest data..."
python3 update_calculator_with_latest_data.py

# --- VERIFICATION (NEW) ---
echo "✅ Verifying calculator synchronization..."
CALC_TIMESTAMP=$(grep -o "Auto-updated.*[0-9][0-9]:[0-9][0-9]" calculator.html | tail -1)
echo "Calculator last updated: $CALC_TIMESTAMP"

CSV_TIMESTAMP=$(ls -l var-explorer/*$DATE.csv | head -1 | awk '{print $6" "$7" "$8}')
echo "CSV files timestamp: $CSV_TIMESTAMP"

# Count symbols in calculator
SYMBOL_COUNT=$(grep -o "'[A-Z0-9_][A-Z0-9_]*':" calculator.html | wc -l)
echo "Symbols loaded in calculator: $SYMBOL_COUNT"

echo "🎯 Explorer update complete for $DATE with synchronized calculator!"