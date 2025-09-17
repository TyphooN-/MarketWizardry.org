#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime
import json

def get_latest_date_str(directory):
    """Find the latest date string from CSV files in a directory."""
    latest_date = None
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            try:
                parts = filename.split('-')
                date_str = parts[-1].split('.')[0]
                dt = datetime.strptime(date_str, '%Y.%m.%d')
                if latest_date is None or dt > latest_date:
                    latest_date = dt
            except (IndexError, ValueError):
                continue
    return latest_date.strftime('%Y.%m.%d') if latest_date else None

def main():
    """Main function to update calculator data."""
    var_dir = 'var-explorer'
    atr_dir = 'atr-explorer'
    ev_dir = 'ev-explorer'

    date_str = get_latest_date_str(var_dir)
    if not date_str:
        print("No CSV files found to process.")
        return

    print(f"Processing data for date: {date_str}")

    var_data = {}

    # Process var-explorer files
    for asset_type in ['stocks', 'cfd', 'futures']:
        file_path = f"{var_dir}/SymbolsExport-Darwinex-Live-{asset_type.capitalize()}-{date_str}.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep=';')
            for _, row in df.iterrows():
                symbol = row['Symbol']
                var_data[symbol] = {
                    'var': row['VaR_1_Lot'],
                    'price': row['BidPrice'],
                    'sector': row['SectorName'],
                    'description': row['Description'],
                    'asset_class': asset_type,
                    'atr_d1': row['ATR_D1'],
                    'atr_w1': row['ATR_W1'],
                    'atr_mn1': row['ATR_MN1'],
                    'outliers': [],
                    'ev_data': {}
                }

    # Process ev-explorer file
    ev_file_path = f"{ev_dir}/SymbolsExport-Darwinex-Live-Stocks-{date_str}-EV.csv"
    if os.path.exists(ev_file_path):
        ev_df = pd.read_csv(ev_file_path, sep=';')
        for _, row in ev_df.iterrows():
            symbol = row['Symbol']
            if symbol in var_data:
                var_data[symbol]['ev_data'] = {
                    'market_cap': row['Market Cap'],
                    'enterprise_value': row['Enterprise Value'],
                    'mcap_ev_ratio': row['MCap/EV (%)']
                }


if __name__ == "__main__":
    main()
