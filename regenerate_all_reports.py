#!/usr/bin/env python3
"""
Parallel report regeneration script for MarketWizardry.org
Regenerates all VaR, ATR, and EV outlier reports using multiprocessing
"""

import os
import subprocess
from multiprocessing import Pool, cpu_count
from pathlib import Path
import time

def process_var_csv(csv_file):
    """Process a single VaR CSV file"""
    try:
        result = subprocess.run(
            ['python3', 'outlier.py', csv_file],
            cwd='var-explorer',
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            output_file = csv_file.replace('.csv', '-outlier.txt')
            with open(f'var-explorer/{output_file}', 'w') as f:
                f.write(result.stdout)
            return (csv_file, 'success')
        else:
            return (csv_file, f'error: {result.stderr[:100]}')
    except Exception as e:
        return (csv_file, f'exception: {str(e)[:100]}')

def process_atr_csv(csv_file):
    """Process a single ATR CSV file"""
    try:
        result = subprocess.run(
            ['python3', 'outlier.py', csv_file],
            cwd='atr-explorer',
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            output_file = csv_file.replace('.csv', '-outlier.txt')
            with open(f'atr-explorer/{output_file}', 'w') as f:
                f.write(result.stdout)
            return (csv_file, 'success')
        else:
            return (csv_file, f'error: {result.stderr[:100]}')
    except Exception as e:
        return (csv_file, f'exception: {str(e)[:100]}')

def process_ev_file(date_info):
    """Process EV analysis for a specific date"""
    date_str, csv_file = date_info
    try:
        # Run EV outlier analysis
        result = subprocess.run(
            ['python3', 'ev_outlier.py', csv_file],
            cwd='ev-explorer',
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            base_name = csv_file.replace('.csv', '')
            output_file = f'{base_name}-ev_outlier.txt'
            with open(f'ev-explorer/{output_file}', 'w') as f:
                f.write(result.stdout)

        # Run EV VaR outlier analysis
        result2 = subprocess.run(
            ['python3', 'ev_var_outlier.py', csv_file],
            cwd='ev-explorer',
            capture_output=True,
            text=True,
            timeout=120
        )

        if result2.returncode == 0:
            base_name = csv_file.replace('.csv', '')
            output_file = f'{base_name}-ev_var_outlier.txt'
            with open(f'ev-explorer/{output_file}', 'w') as f:
                f.write(result2.stdout)
            return (csv_file, 'success')
        else:
            return (csv_file, f'error: {result2.stderr[:100]}')
    except Exception as e:
        return (csv_file, f'exception: {str(e)[:100]}')

def main():
    start_time = time.time()

    # Determine number of workers (use all available CPU cores)
    num_workers = cpu_count()
    print(f"🚀 Starting parallel report regeneration with {num_workers} workers")
    print(f"   Using all available CPU cores: {cpu_count()}")
    print()

    # Process VaR explorer
    print("📈 Processing VaR Explorer reports...")
    var_csvs = [f for f in os.listdir('var-explorer') if f.endswith('.csv')]
    print(f"   Found {len(var_csvs)} CSV files")

    with Pool(num_workers) as pool:
        results = pool.map(process_var_csv, var_csvs)

    var_success = sum(1 for _, status in results if status == 'success')
    var_failed = len(results) - var_success
    print(f"   ✅ Success: {var_success}, ❌ Failed: {var_failed}")
    print()

    # Process ATR explorer
    print("⚡ Processing ATR Explorer reports...")
    atr_csvs = [f for f in os.listdir('atr-explorer') if f.endswith('.csv')]
    print(f"   Found {len(atr_csvs)} CSV files")

    with Pool(num_workers) as pool:
        results = pool.map(process_atr_csv, atr_csvs)

    atr_success = sum(1 for _, status in results if status == 'success')
    atr_failed = len(results) - atr_success
    print(f"   ✅ Success: {atr_success}, ❌ Failed: {atr_failed}")
    print()

    # Process EV explorer
    print("💰 Processing EV Explorer reports...")
    ev_csvs = [f for f in os.listdir('ev-explorer') if f.endswith('-EV.csv')]
    print(f"   Found {len(ev_csvs)} EV CSV files")

    # Create date info tuples
    ev_date_info = [(f.split('-')[4], f) for f in ev_csvs]

    with Pool(num_workers) as pool:
        results = pool.map(process_ev_file, ev_date_info)

    ev_success = sum(1 for _, status in results if status == 'success')
    ev_failed = len(results) - ev_success
    print(f"   ✅ Success: {ev_success}, ❌ Failed: {ev_failed}")
    print()

    elapsed = time.time() - start_time
    print(f"🎉 All reports regenerated in {elapsed:.1f} seconds!")
    print(f"   Total files processed: {len(var_csvs) + len(atr_csvs) + len(ev_csvs)}")
    print(f"   Average time per file: {elapsed/(len(var_csvs) + len(atr_csvs) + len(ev_csvs)):.2f}s")

if __name__ == '__main__':
    main()
