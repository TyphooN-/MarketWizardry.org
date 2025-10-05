#!/usr/bin/env python3
"""
Regenerate all chart HTML files with CSP-compliant template.

This script finds all outlier.py scripts in explorer directories and regenerates
their chart outputs using the updated chart_generator.py template.

Usage:
    python3 regenerate_charts.py [--all]       # Regenerate all charts
    python3 regenerate_charts.py --recent 30   # Regenerate last 30 days only
    python3 regenerate_charts.py --dry-run     # Show what would be done
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from multiprocessing import Pool, cpu_count

def find_chart_html_files(explorer_dir, days_filter=None):
    """Find all chart HTML files in an explorer directory."""
    chart_files = []

    if not os.path.exists(explorer_dir):
        return chart_files

    for filename in os.listdir(explorer_dir):
        if filename.endswith('-price-trends.html'):
            filepath = os.path.join(explorer_dir, filename)

            # Apply date filter if specified
            if days_filter:
                # Extract date from filename: SymbolsExport-Darwinex-Live-CFD-2025.10.01-price-trends.html
                parts = filename.split('-')
                if len(parts) >= 5:
                    try:
                        date_str = parts[4]  # 2025.10.01
                        file_date = datetime.strptime(date_str, '%Y.%m.%d')
                        cutoff_date = datetime.now() - timedelta(days=days_filter)

                        if file_date < cutoff_date:
                            continue  # Skip old files
                    except (ValueError, IndexError):
                        pass  # Keep the file if we can't parse date

            chart_files.append(filepath)

    return chart_files

def regenerate_chart(chart_file):
    """Regenerate a single chart file by running the outlier.py script."""
    try:
        # Extract info from filename
        # Format: atr-explorer/SymbolsExport-Darwinex-Live-CFD-2025.10.01-price-trends.html
        dirname = os.path.dirname(chart_file)
        filename = os.path.basename(chart_file)

        # Get CSV filename by removing -price-trends.html
        csv_filename = filename.replace('-price-trends.html', '.csv')
        csv_path = os.path.join(dirname, csv_filename)

        # Check if CSV exists
        if not os.path.exists(csv_path):
            return (chart_file, 'skipped', 'CSV not found')

        # Check if outlier.py exists in this directory
        outlier_script = os.path.join(dirname, 'outlier.py')
        if not os.path.exists(outlier_script):
            return (chart_file, 'skipped', 'No outlier.py script')

        # Run outlier.py to regenerate the chart
        result = subprocess.run(
            ['python3', 'outlier.py', csv_filename],
            cwd=dirname,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return (chart_file, 'success', 'Regenerated')
        else:
            error_msg = result.stderr[:100] if result.stderr else 'Unknown error'
            return (chart_file, 'failed', error_msg)

    except subprocess.TimeoutExpired:
        return (chart_file, 'failed', 'Timeout')
    except Exception as e:
        return (chart_file, 'failed', str(e)[:100])

def main():
    parser = argparse.ArgumentParser(
        description='Regenerate chart HTML files with CSP-compliant template'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Regenerate ALL chart files (default: recent only)'
    )
    parser.add_argument(
        '--recent',
        type=int,
        metavar='DAYS',
        help='Only regenerate charts from last N days'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--explorer',
        choices=['atr', 'var', 'ev', 'crypto'],
        help='Only regenerate charts for specific explorer'
    )

    args = parser.parse_args()

    # Determine date filter
    days_filter = None
    if not args.all:
        days_filter = args.recent if args.recent else 30  # Default: last 30 days

    # Find all chart files
    explorers = ['atr-explorer', 'var-explorer', 'ev-explorer', 'crypto-explorer']
    if args.explorer:
        explorers = [f'{args.explorer}-explorer']

    print("🔍 Scanning for chart HTML files...")
    all_chart_files = []
    for explorer in explorers:
        chart_files = find_chart_html_files(explorer, days_filter)
        all_chart_files.extend(chart_files)
        if chart_files:
            print(f"  📁 {explorer}: {len(chart_files)} charts found")

    if not all_chart_files:
        print("✅ No chart files found to regenerate")
        return

    print(f"\n📊 Total charts to regenerate: {len(all_chart_files)}")

    if days_filter:
        print(f"📅 Filter: Last {days_filter} days only")

    if args.dry_run:
        print("\n🔍 DRY RUN - No changes will be made\n")
        for chart_file in all_chart_files:
            print(f"  Would regenerate: {chart_file}")
        return

    # Confirm before proceeding (skip in non-interactive mode)
    if len(all_chart_files) > 100:
        import sys
        if sys.stdin.isatty():
            response = input(f"\n⚠️  This will regenerate {len(all_chart_files)} charts. Continue? (y/N): ")
            if response.lower() != 'y':
                print("❌ Cancelled")
                return
        else:
            print(f"\n⚠️  Non-interactive mode: Proceeding with {len(all_chart_files)} charts...")

    print(f"\n🔄 Regenerating charts using {cpu_count()} CPU cores...\n")

    # Process charts in parallel
    with Pool(cpu_count()) as pool:
        results = pool.map(regenerate_chart, all_chart_files)

    # Summarize results
    success_count = sum(1 for _, status, _ in results if status == 'success')
    failed_count = sum(1 for _, status, _ in results if status == 'failed')
    skipped_count = sum(1 for _, status, _ in results if status == 'skipped')

    print(f"\n{'='*60}")
    print(f"📈 Chart Regeneration Summary:")
    print(f"{'='*60}")
    print(f"  ✅ Success: {success_count}")
    print(f"  ⏭️  Skipped: {skipped_count}")
    print(f"  ❌ Failed:  {failed_count}")
    print(f"{'='*60}")

    # Show failures if any
    if failed_count > 0:
        print("\n❌ Failed charts:")
        for chart_file, status, msg in results:
            if status == 'failed':
                print(f"  {os.path.basename(chart_file)}: {msg}")

    if success_count > 0:
        print(f"\n✅ Successfully regenerated {success_count} charts with CSP-compliant template!")

    sys.exit(0 if failed_count == 0 else 1)

if __name__ == "__main__":
    main()
