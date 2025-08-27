#!/bin/bash
source ~/venv/bin/activate
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <date>"
  exit 1
fi

DATE=$1

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

echo "Explorer update complete for $DATE."
