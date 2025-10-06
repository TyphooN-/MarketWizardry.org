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


def load_symbol_details(csv_file):
    """
    Load symbol details including specs (TradeMode, swap, commission).

    Args:
        csv_file (str): Path to CSV file

    Returns:
        dict: Dict mapping symbol -> {TradeMode, SwapLong, SwapShort, Spread}
    """
    try:
        df = pd.read_csv(csv_file, delimiter=';', encoding='latin1')
        if 'Symbol' not in df.columns:
            return {}

        symbol_data = {}
        for _, row in df.iterrows():
            symbol = row.get('Symbol')
            if pd.notna(symbol):
                symbol_data[symbol] = {
                    'TradeMode': row.get('TradeMode', ''),
                    'SwapLong': row.get('SwapLong', 0),
                    'SwapShort': row.get('SwapShort', 0),
                    'Spread': row.get('Spread', 0)
                }
        return symbol_data
    except Exception as e:
        print(f"Error loading details from {csv_file}: {e}")
        return {}


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
    Tracks: new symbols, delisted symbols, close-only symbols, and spec changes.

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

    # Track symbol sets and details by date
    symbol_history = {}
    symbol_details_history = {}

    for csv_file in csv_files:
        date = extract_date_from_filename(csv_file)
        if date:
            csv_path = os.path.join(csv_dir, csv_file)
            symbols = load_symbol_list(csv_path)
            details = load_symbol_details(csv_path)
            symbol_history[date] = symbols
            symbol_details_history[date] = details
            print(f"📅 {date}: {len(symbols)} symbols")

    if len(symbol_history) < 2:
        print("⚠️  Could not extract dates from filenames")
        return None

    # Sort dates
    sorted_dates = sorted(symbol_history.keys())

    # Find new symbols, delisted symbols, close-only changes, and spec changes
    new_symbols = {}
    delisted_symbols = {}
    close_only_changes = {}
    spec_changes = {}

    for i in range(1, len(sorted_dates)):
        prev_date = sorted_dates[i-1]
        curr_date = sorted_dates[i]

        prev_symbols = symbol_history[prev_date]
        curr_symbols = symbol_history[curr_date]
        prev_details = symbol_details_history[prev_date]
        curr_details = symbol_details_history[curr_date]

        # New symbols: in current but not in previous
        new = curr_symbols - prev_symbols
        if new:
            new_symbols[curr_date] = sorted(new)

        # Delisted symbols: in previous but not in current (fully removed)
        delisted = prev_symbols - curr_symbols
        if delisted:
            delisted_symbols[curr_date] = sorted(delisted)

        # Check for spec changes in symbols present in both dates
        common_symbols = prev_symbols & curr_symbols
        date_spec_changes = {}

        for symbol in common_symbols:
            if symbol in prev_details and symbol in curr_details:
                prev_spec = prev_details[symbol]
                curr_spec = curr_details[symbol]
                changes = []

                # Check TradeMode change (3=close-only, 4=full trading)
                if prev_spec['TradeMode'] != curr_spec['TradeMode']:
                    prev_mode = int(prev_spec['TradeMode']) if prev_spec['TradeMode'] else 0
                    curr_mode = int(curr_spec['TradeMode']) if curr_spec['TradeMode'] else 0

                    if prev_mode == 4 and curr_mode == 3:
                        changes.append('→ CLOSE-ONLY')
                    elif prev_mode == 3 and curr_mode == 4:
                        changes.append('→ TRADING ENABLED')
                    else:
                        changes.append(f'TradeMode: {prev_mode} → {curr_mode}')

                # Check swap changes (only meaningful changes, filter out garbage values)
                try:
                    prev_long = float(prev_spec['SwapLong'])
                    curr_long = float(curr_spec['SwapLong'])
                    # Filter out invalid/garbage values (extremely large numbers indicate data corruption)
                    if abs(prev_long) < 1000000 and abs(curr_long) < 1000000:
                        if prev_long != curr_long:
                            changes.append(f"SwapLong: {prev_long} → {curr_long}")
                except:
                    pass

                try:
                    prev_short = float(prev_spec['SwapShort'])
                    curr_short = float(curr_spec['SwapShort'])
                    # Filter out invalid/garbage values
                    if abs(prev_short) < 1000000 and abs(curr_short) < 1000000:
                        if prev_short != curr_short:
                            changes.append(f"SwapShort: {prev_short} → {curr_short}")
                except:
                    pass

                if changes:
                    date_spec_changes[symbol] = changes

        if date_spec_changes:
            spec_changes[curr_date] = date_spec_changes

        # Track close-only changes separately for summary
        for symbol, changes in date_spec_changes.items():
            for change in changes:
                if 'CLOSE-ONLY' in change:
                    if curr_date not in close_only_changes:
                        close_only_changes[curr_date] = []
                    close_only_changes[curr_date].append(symbol)

    # Track close-only → delisted timeline
    close_only_to_delisted = {}

    # Track close-only → trading enabled timeline
    close_only_to_enabled = {}

    # Build a map of when symbols went close-only (store all dates, not just first)
    close_only_dates = defaultdict(list)
    # Build a map of when symbols were enabled for trading
    trading_enabled_dates = defaultdict(list)

    for date, changes_dict in spec_changes.items():
        for symbol, changes in changes_dict.items():
            for change in changes:
                if 'CLOSE-ONLY' in change:
                    close_only_dates[symbol].append(date)
                elif 'TRADING ENABLED' in change:
                    trading_enabled_dates[symbol].append(date)

    # Check which close-only symbols were later delisted
    for date, delisted_list in delisted_symbols.items():
        for symbol in delisted_list:
            if symbol in close_only_dates:
                # Find the most recent close-only date BEFORE the delisting
                try:
                    from datetime import datetime
                    delist_date = datetime.strptime(date, '%Y.%m.%d')

                    valid_close_dates = []
                    for close_date_str in close_only_dates[symbol]:
                        close_date = datetime.strptime(close_date_str, '%Y.%m.%d')
                        # Only count if close-only happened BEFORE delisting
                        if close_date < delist_date:
                            valid_close_dates.append((close_date_str, close_date))

                    # Use the most recent valid close-only date
                    if valid_close_dates:
                        valid_close_dates.sort(key=lambda x: x[1], reverse=True)
                        close_only_date_str = valid_close_dates[0][0]
                        close_date = valid_close_dates[0][1]
                        days_diff = (delist_date - close_date).days

                        close_only_to_delisted[symbol] = {
                            'close_only_date': close_only_date_str,
                            'delisted_date': date,
                            'days_between': days_diff
                        }
                except:
                    pass

    # Check which close-only symbols were later re-enabled for trading
    for symbol in trading_enabled_dates:
        if symbol in close_only_dates:
            # Find the most recent close-only date BEFORE the trading enabled date
            try:
                from datetime import datetime

                for enabled_date_str in trading_enabled_dates[symbol]:
                    enabled_date = datetime.strptime(enabled_date_str, '%Y.%m.%d')

                    valid_close_dates = []
                    for close_date_str in close_only_dates[symbol]:
                        close_date = datetime.strptime(close_date_str, '%Y.%m.%d')
                        # Only count if close-only happened BEFORE trading enabled
                        if close_date < enabled_date:
                            valid_close_dates.append((close_date_str, close_date))

                    # Use the most recent valid close-only date
                    if valid_close_dates:
                        valid_close_dates.sort(key=lambda x: x[1], reverse=True)
                        close_only_date_str = valid_close_dates[0][0]
                        close_date = valid_close_dates[0][1]
                        days_diff = (enabled_date - close_date).days

                        # Only store the first (or update if shorter timeline)
                        if symbol not in close_only_to_enabled or days_diff < close_only_to_enabled[symbol]['days_between']:
                            close_only_to_enabled[symbol] = {
                                'close_only_date': close_only_date_str,
                                'enabled_date': enabled_date_str,
                                'days_between': days_diff
                            }
            except:
                pass

    # Track current close-only symbols and how long they've been in that status
    current_close_only = {}

    # Get the latest date's symbol data
    latest_date = sorted_dates[-1]
    latest_csv = os.path.join(csv_dir, csv_files[-1])
    latest_details = load_symbol_details(latest_csv)

    # Find symbols currently in close-only mode (TradeMode 3)
    for symbol, spec in latest_details.items():
        try:
            trade_mode = int(spec['TradeMode']) if spec['TradeMode'] else 0
            if trade_mode == 3:
                # Find the most recent date this symbol went close-only
                if symbol in close_only_dates:
                    # Get the most recent close-only date
                    from datetime import datetime

                    close_dates_parsed = []
                    for close_date_str in close_only_dates[symbol]:
                        close_date = datetime.strptime(close_date_str, '%Y.%m.%d')
                        close_dates_parsed.append((close_date_str, close_date))

                    close_dates_parsed.sort(key=lambda x: x[1], reverse=True)
                    most_recent_close_only = close_dates_parsed[0][0]

                    # Calculate days since close-only
                    close_date = datetime.strptime(most_recent_close_only, '%Y.%m.%d')
                    current_date = datetime.strptime(latest_date, '%Y.%m.%d')
                    days_in_close_only = (current_date - close_date).days

                    current_close_only[symbol] = {
                        'since_date': most_recent_close_only,
                        'days': days_in_close_only
                    }
        except:
            pass

    # Prepare report
    results = {
        'symbol_history': symbol_history,
        'sorted_dates': sorted_dates,
        'new_symbols': new_symbols,
        'delisted_symbols': delisted_symbols,
        'close_only_changes': close_only_changes,
        'spec_changes': spec_changes,
        'close_only_to_delisted': close_only_to_delisted,
        'close_only_to_enabled': close_only_to_enabled,
        'current_close_only': current_close_only,
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
    output.append(f"Total Symbols Delisted (Fully Removed): {sum(len(v) for v in results['delisted_symbols'].values())}")
    output.append(f"Total Close-Only Changes: {sum(len(v) for v in results.get('close_only_changes', {}).values())}")
    output.append(f"Total Spec Changes: {sum(len(v) for v in results.get('spec_changes', {}).values())}")
    output.append("")

    # Current close-only symbols section
    if results.get('current_close_only'):
        output.append("=" * 120)
        output.append("⚠️  CURRENT CLOSE-ONLY SYMBOLS")
        output.append("=" * 120)
        output.append(f"Symbols currently in close-only mode as of {results['sorted_dates'][-1]} ({len(results['current_close_only'])} total):")
        output.append("")

        # Sort by days in close-only (longest to shortest)
        close_only_sorted = sorted(results['current_close_only'].items(),
                                   key=lambda x: x[1]['days'], reverse=True)

        for symbol, info in close_only_sorted:
            days = info['days']
            output.append(f"   {symbol:<10} Close-Only since: {info['since_date']} ({days} days)")
    else:
        output.append("=" * 120)
        output.append("⚠️  CURRENT CLOSE-ONLY SYMBOLS")
        output.append("=" * 120)
        output.append(f"\n✅ No symbols currently in close-only mode as of {results['sorted_dates'][-1]}")

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

    # Spec changes section (NEW!)
    if results.get('spec_changes'):
        output.append("=" * 120)
        output.append("⚙️  SPECIFICATION CHANGES (Trade Mode / Swap Rates)")
        output.append("=" * 120)
        output.append("Note: Close-only does NOT count as delisted. Symbol is still available for closing positions.")
        output.append("")

        for date in sorted(results['spec_changes'].keys(), reverse=True):
            changes_dict = results['spec_changes'][date]
            output.append(f"\n📅 {date} - {len(changes_dict)} symbol(s) with spec changes:")
            output.append("-" * 120)

            # Group symbols by identical change strings
            change_to_symbols = defaultdict(list)
            for symbol, changes in changes_dict.items():
                change_str = ", ".join(changes)
                change_to_symbols[change_str].append(symbol)

            # Display grouped changes
            for change_str, symbols in sorted(change_to_symbols.items()):
                symbols_sorted = sorted(symbols)
                if len(symbols_sorted) == 1:
                    # Single symbol - display normally
                    output.append(f"   {symbols_sorted[0]:<10} {change_str}")
                else:
                    # Multiple symbols with same change - group them
                    # Display symbols in rows of 8, similar to new/delisted symbols
                    output.append(f"   [{len(symbols_sorted)} symbols] {change_str}")
                    symbols_per_row = 8
                    for i in range(0, len(symbols_sorted), symbols_per_row):
                        row_symbols = symbols_sorted[i:i+symbols_per_row]
                        output.append("      → " + "  ".join(f"{s:<10}" for s in row_symbols))
    else:
        output.append("=" * 120)
        output.append("⚙️  SPECIFICATION CHANGES (Trade Mode / Swap Rates)")
        output.append("=" * 120)
        output.append("\n✅ No spec changes during this period")

    output.append("")

    # Delisted symbols section
    if results['delisted_symbols']:
        output.append("=" * 120)
        output.append("❌ DELISTED / FULLY REMOVED SYMBOLS")
        output.append("=" * 120)
        output.append("Note: These symbols were completely removed from the platform (not just close-only).")
        output.append("")

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
        output.append("=" * 120)
        output.append("❌ DELISTED / FULLY REMOVED SYMBOLS")
        output.append("=" * 120)
        output.append("\n✅ No symbols delisted during this period")

    output.append("")

    # Close-only → Delisted timeline section
    if results.get('close_only_to_delisted'):
        output.append("=" * 120)
        output.append("⏱️  CLOSE-ONLY → DELISTED TIMELINE")
        output.append("=" * 120)
        output.append("Symbols that went close-only before being fully delisted (shows lifecycle timeline).")
        output.append("")

        # Sort by days between (shortest to longest)
        timeline_sorted = sorted(results['close_only_to_delisted'].items(),
                                key=lambda x: x[1]['days_between'])

        for symbol, timeline in timeline_sorted:
            days = timeline['days_between']
            output.append(f"   {symbol:<10} Close-Only: {timeline['close_only_date']} → Delisted: {timeline['delisted_date']} ({days} days)")
    else:
        output.append("=" * 120)
        output.append("⏱️  CLOSE-ONLY → DELISTED TIMELINE")
        output.append("=" * 120)
        output.append("\n✅ No close-only symbols were delisted during this period")

    output.append("")

    # Close-only → Trading Enabled timeline section
    if results.get('close_only_to_enabled'):
        output.append("=" * 120)
        output.append("⏱️  CLOSE-ONLY → TRADING ENABLED TIMELINE")
        output.append("=" * 120)
        output.append("Symbols that went close-only and were later re-enabled for full trading (shows recovery timeline).")
        output.append("")

        # Sort by days between (shortest to longest)
        timeline_sorted = sorted(results['close_only_to_enabled'].items(),
                                key=lambda x: x[1]['days_between'])

        for symbol, timeline in timeline_sorted:
            days = timeline['days_between']
            output.append(f"   {symbol:<10} Close-Only: {timeline['close_only_date']} → Enabled: {timeline['enabled_date']} ({days} days)")
    else:
        output.append("=" * 120)
        output.append("⏱️  CLOSE-ONLY → TRADING ENABLED TIMELINE")
        output.append("=" * 120)
        output.append("\n✅ No close-only symbols were re-enabled during this period")

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
        ('var-explorer', 'cfd', 'CFD', 'CFD'),
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
