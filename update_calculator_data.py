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

def process_outliers(directory, date_str, var_data):
    """Process outlier files in a given directory."""
    for filename in os.listdir(directory):
        if filename.endswith(f"-{date_str}-outlier.txt"):
            outlier_type = 'var' # default
            if 'ev_outlier' in filename:
                outlier_type = 'ev'
            elif 'atr' in directory:
                outlier_type = 'atr'

            with open(os.path.join(directory, filename), 'r') as f:
                for line in f:
                    symbol = line.strip()
                    if symbol in var_data:
                        if outlier_type not in var_data[symbol]['outliers']:
                            var_data[symbol]['outliers'].append(outlier_type)

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

    # Process outlier files
    process_outliers(var_dir, date_str, var_data)
    process_outliers(atr_dir, date_str, var_data)
    process_outliers(ev_dir, date_str, var_data)

    # Generate JS file
    js_content = f"const varData = {json.dumps(var_data, indent=4)};"
    with open('calculator_complete_data.js', 'w') as f:
        f.write(js_content)

    print("Successfully updated calculator_complete_data.js")


if __name__ == "__main__":
    main()
