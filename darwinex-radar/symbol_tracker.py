#!/usr/bin/env python3
"""
Darwinex RADAR - Symbol Tracker
Tracks new symbols, delisted symbols, and Darwinex-exclusive symbols over time.
"""

import pandas as pd
import os
import sys
from datetime import datetime
from collections import defaultdict


def load_symbol_list(csv_file):
    """
    Load symbol list from a CSV file.

    Args:
        csv_file (str): Path to CSV file

    Returns:
        set: Set of symbol names
    """
    try:
        df = pd.read_csv(csv_file, delimiter=';', encoding='latin1')
        if 'Symbol' in df.columns:
            return set(df['Symbol'].dropna().unique())
        return set()
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")
        return set()


def extract_date_from_filename(filename):
    """
    Extract date from filename like 'SymbolsExport-Darwinex-Live-Stocks-2025.10.03.csv'

    Args:
        filename (str): CSV filename

    Returns:
        str: Date string (YYYY.MM.DD) or None
    """
    import re
    match = re.search(r'(\d{4}\.\d{2}\.\d{2})', filename)
    if match:
        return match.group(1)
    return None


def analyze_symbol_changes(csv_dir, output_file=None, instrument_filter=None):
    """
    Analyze symbol changes across all CSV files in a directory.

    Args:
        csv_dir (str): Directory containing CSV files
        output_file (str): Optional output file path
        instrument_filter (str): Optional filter for instrument type (e.g., 'Stocks', 'Futures', 'CFD')

    Returns:
        dict: Analysis results
    """
    # Get all CSV files, optionally filtered by instrument type
    all_csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

    if instrument_filter:
        csv_files = sorted([f for f in all_csv_files if instrument_filter in f])
    else:
        csv_files = sorted(all_csv_files)

    if len(csv_files) < 2:
        print("⚠️  Need at least 2 CSV files to track changes")
        return None

    # Track symbol sets by date
    symbol_history = {}

    for csv_file in csv_files:
        date = extract_date_from_filename(csv_file)
        if date:
            csv_path = os.path.join(csv_dir, csv_file)
            symbols = load_symbol_list(csv_path)
            symbol_history[date] = symbols
            print(f"📅 {date}: {len(symbols)} symbols")

    if len(symbol_history) < 2:
        print("⚠️  Could not extract dates from filenames")
        return None

    # Sort dates
    sorted_dates = sorted(symbol_history.keys())

    # Find new and delisted symbols
    new_symbols = {}
    delisted_symbols = {}

    for i in range(1, len(sorted_dates)):
        prev_date = sorted_dates[i-1]
        curr_date = sorted_dates[i]

        prev_symbols = symbol_history[prev_date]
        curr_symbols = symbol_history[curr_date]

        # New symbols: in current but not in previous
        new = curr_symbols - prev_symbols
        if new:
            new_symbols[curr_date] = sorted(new)

        # Delisted symbols: in previous but not in current
        delisted = prev_symbols - curr_symbols
        if delisted:
            delisted_symbols[curr_date] = sorted(delisted)

    # Prepare report
    results = {
        'symbol_history': symbol_history,
        'sorted_dates': sorted_dates,
        'new_symbols': new_symbols,
        'delisted_symbols': delisted_symbols,
        'latest_symbols': symbol_history[sorted_dates[-1]],
        'earliest_symbols': symbol_history[sorted_dates[0]],
    }

    # Generate report
    report = generate_report(results, csv_dir)

    # Save to file if specified
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ Report saved to: {output_file}")
    else:
        print(report)

    return results


def generate_report(results, csv_dir):
    """
    Generate a formatted text report of symbol changes.

    Args:
        results (dict): Analysis results
        csv_dir (str): Source directory name

    Returns:
        str: Formatted report
    """
    output = []
    output.append("=" * 120)
    output.append("DARWINEX RADAR - SYMBOL TRACKER")
    output.append("=" * 120)
    output.append(f"📁 Data Source: {csv_dir}")
    output.append(f"📊 Date Range: {results['sorted_dates'][0]} to {results['sorted_dates'][-1]}")
    output.append(f"📈 Total Tracking Period: {len(results['sorted_dates'])} trading days")
    output.append("")

    # Summary statistics
    output.append("=" * 120)
    output.append("📋 SUMMARY STATISTICS")
    output.append("=" * 120)

    earliest_count = len(results['earliest_symbols'])
    latest_count = len(results['latest_symbols'])
    net_change = latest_count - earliest_count

    output.append(f"Symbols on {results['sorted_dates'][0]}: {earliest_count}")
    output.append(f"Symbols on {results['sorted_dates'][-1]}: {latest_count}")
    output.append(f"Net Change: {net_change:+d} symbols ({net_change/earliest_count*100:+.1f}%)")
    output.append(f"Total New Symbols Added: {sum(len(v) for v in results['new_symbols'].values())}")
    output.append(f"Total Symbols Delisted: {sum(len(v) for v in results['delisted_symbols'].values())}")
    output.append("")

    # New symbols section
    if results['new_symbols']:
        output.append("=" * 120)
        output.append("🆕 NEW SYMBOLS LISTED")
        output.append("=" * 120)

        for date in sorted(results['new_symbols'].keys(), reverse=True):
            symbols = results['new_symbols'][date]
            output.append(f"\n📅 {date} - {len(symbols)} new symbol(s):")
            output.append("-" * 120)

            # Display symbols in columns
            symbols_per_row = 8
            for i in range(0, len(symbols), symbols_per_row):
                row_symbols = symbols[i:i+symbols_per_row]
                output.append("   " + "  ".join(f"{s:<10}" for s in row_symbols))
    else:
        output.append("\n✅ No new symbols listed during this period")

    output.append("")

    # Delisted symbols section
    if results['delisted_symbols']:
        output.append("=" * 120)
        output.append("❌ DELISTED / REMOVED SYMBOLS")
        output.append("=" * 120)

        for date in sorted(results['delisted_symbols'].keys(), reverse=True):
            symbols = results['delisted_symbols'][date]
            output.append(f"\n📅 {date} - {len(symbols)} delisted symbol(s):")
            output.append("-" * 120)

            # Display symbols in columns
            symbols_per_row = 8
            for i in range(0, len(symbols), symbols_per_row):
                row_symbols = symbols[i:i+symbols_per_row]
                output.append("   " + "  ".join(f"{s:<10}" for s in row_symbols))
    else:
        output.append("\n✅ No symbols delisted during this period")

    output.append("")
    output.append("=" * 120)
    output.append(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 120)

    return "\n".join(output)


def generate_comprehensive_report(base_dir='.'):
    """
    Generate comprehensive Darwinex RADAR report from all explorer directories.

    Args:
        base_dir (str): Base directory containing explorer folders

    Returns:
        bool: Success status
    """
    # Define reports to generate: (directory, output_name, display_name, filter)
    reports = [
        ('var-explorer', 'stocks', 'Stocks', 'Stocks'),
        ('atr-explorer', 'futures', 'Futures', 'Futures'),
        ('atr-explorer', 'cfd', 'CFD', 'CFD'),
        ('crypto-explorer', 'crypto', 'Crypto', None)
    ]

    radar_dir = os.path.join(base_dir, 'darwinex-radar')
    os.makedirs(radar_dir, exist_ok=True)

    all_results = {}

    for explorer_dir, output_name, display_name, instrument_filter in reports:
        explorer_path = os.path.join(base_dir, explorer_dir)

        if not os.path.isdir(explorer_path):
            print(f"⚠️  Skipping {display_name} (directory {explorer_dir} not found)")
            continue

        output_file = os.path.join(radar_dir, f"{output_name}-radar.txt")

        print(f"🔍 Analyzing {display_name}...")
        result = analyze_symbol_changes(explorer_path, output_file, instrument_filter=instrument_filter)

        if result:
            all_results[display_name] = result

    if all_results:
        print(f"\n✅ Darwinex RADAR reports generated: {len(all_results)}")
        return True
    else:
        print("❌ No RADAR reports generated")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 symbol_tracker.py <csv_directory> [output_file]")
        print("   or: python3 symbol_tracker.py --all (generate all reports)")
        print("Example: python3 symbol_tracker.py ../var-explorer var-radar.txt")
        sys.exit(1)

    if sys.argv[1] == '--all':
        # Generate all reports from parent directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_dir)
        generate_comprehensive_report(parent_dir)
    else:
        csv_dir = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        if not os.path.isdir(csv_dir):
            print(f"Error: '{csv_dir}' is not a directory")
            sys.exit(1)

        analyze_symbol_changes(csv_dir, output_file)
