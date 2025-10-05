#!/usr/bin/env python3
"""
Unified script to update all MarketWizardry.org financial tools:
- VaR Explorer
- ATR Explorer
- EV Explorer
- Calculator Suite

This replaces the individual var-explorer.py, atr-explorer.py, ev-explorer.py scripts
and includes calculator data updates.
"""

import os
import json
import requests
import time
import subprocess
import shutil
import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
from datetime import datetime, date
from seo_templates import SEOManager, get_breadcrumb_paths, PAGE_CONFIGS, REDIRECT_SCRIPT_TEMPLATE

# Parallel processing helper functions
def _process_single_var_csv(args):
    """Process a single VaR CSV file - used for parallel processing"""
    csv_file, date_str, force_regenerate = args
    output_file = csv_file.replace('.csv', '-outlier.txt')
    output_path = f"var-explorer/{output_file}"

    # Skip if exists and not force regenerating
    if os.path.exists(output_path) and not force_regenerate:
        return (csv_file, 'skipped')

    try:
        result = subprocess.run(
            ['python3', 'outlier.py', csv_file],
            cwd='var-explorer',
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            with open(output_path, 'w') as f:
                f.write(result.stdout)
            return (csv_file, 'success')
        else:
            return (csv_file, f'error: {result.stderr[:100]}')
    except Exception as e:
        return (csv_file, f'exception: {str(e)[:100]}')

def _process_single_atr_csv(args):
    """Process a single ATR CSV file - used for parallel processing"""
    csv_file, date_str, force_regenerate = args
    output_file = csv_file.replace('.csv', '-outlier.txt')
    output_path = f"atr-explorer/{output_file}"

    # Skip if exists and not force regenerating
    if os.path.exists(output_path) and not force_regenerate:
        return (csv_file, 'skipped')

    try:
        result = subprocess.run(
            ['python3', 'outlier.py', csv_file],
            cwd='atr-explorer',
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            with open(output_path, 'w') as f:
                f.write(result.stdout)
            return (csv_file, 'success')
        else:
            return (csv_file, f'error: {result.stderr[:100]}')
    except Exception as e:
        return (csv_file, f'exception: {str(e)[:100]}')

class FinancialToolsUpdater:
    def __init__(self, date_str=None, force_regenerate=False, html_only=False, force_explorers=None):
        self.seo_manager = SEOManager()
        self.breadcrumb_paths = get_breadcrumb_paths()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.date_str = date_str or datetime.now().strftime('%Y.%m.%d')
        # Only force regenerate if explicitly requested via force_regenerate parameter
        self.force_regenerate = force_regenerate
        # HTML-only mode skips data fetching and only regenerates HTML content
        self.html_only = html_only
        # Specific explorers to force regenerate (list of: 'var', 'atr', 'ev', 'crypto')
        self.force_explorers = force_explorers or []
        self.data_summary = {}

    def copy_csv_files(self):
        """Copy CSV files from MetaTrader directories"""
        print(f"📂 Copying CSV files for {self.date_str} from MetaTrader directories...")

        files_copied = 0
        mt_paths = {
            'stocks': f"/home/typhoon/.mt5_9/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-Stocks-{self.date_str}.csv",
            'cfd': f"/home/typhoon/.mt5_10/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-CFD-{self.date_str}.csv",
            'futures': f"/home/typhoon/.mt5_11/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-Futures-{self.date_str}.csv",
            'crypto': f"/home/typhoon/.mt5_8/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-Crypto-{self.date_str}.csv"
        }

        for asset_type, source_path in mt_paths.items():
            # Crypto goes to its own explorer
            if asset_type == 'crypto':
                dest_dir = 'crypto-explorer'
            else:
                dest_dir = 'var-explorer'

            dest_path = f'{dest_dir}/SymbolsExport-Darwinex-Live-{asset_type.title()}-{self.date_str}.csv'

            # Check if destination already exists
            if os.path.exists(dest_path):
                print(f"⏭️  {asset_type.title()} CSV already exists for {self.date_str}, skipping copy")
                files_copied += 1
            elif os.path.exists(source_path):
                shutil.copy(source_path, dest_dir + '/')
                print(f"✅ Copied {asset_type.title()} CSV for {self.date_str}")
                files_copied += 1
            else:
                print(f"⚠️ Warning: {asset_type.title()} CSV not found at source for {self.date_str}")

        if files_copied == 0:
            print(f"❌ Error: No CSV files found or copied for date {self.date_str}")
            return False

        print(f"📊 {files_copied} CSV file(s) available for processing")
        return True

    def process_var_data(self):
        """Process VaR data using outlier.py script - ONLY for current date"""
        print("📈 Processing VaR data...")

        try:
            # Check if outlier files already exist for this date
            existing_outlier_files = [f for f in os.listdir('var-explorer') if f.endswith('-outlier.txt') and self.date_str in f]

            force_var = 'var' in self.force_explorers or self.force_regenerate
            if existing_outlier_files and not force_var:
                print(f"⏭️ Skipping VaR processing - {len(existing_outlier_files)} outlier files already exist for {self.date_str}")
                print("   Use --force-var to regenerate VaR files")
                self.data_summary['var_outliers'] = len(existing_outlier_files)
                return True

            # IMPORTANT: Only process CSV files for current date to prevent mass regeneration
            # Find CSV files for the current date only
            csv_files = [f for f in os.listdir('var-explorer')
                        if f.endswith('.csv') and self.date_str in f]

            if not csv_files:
                print(f"⚠️ Warning: No CSV files found for {self.date_str}")
                return False

            print(f"  Processing {len(csv_files)} CSV files for {self.date_str} (parallel using {cpu_count()} cores)...")

            # Prepare arguments for parallel processing
            process_args = [(csv_file, self.date_str, force_var) for csv_file in csv_files]

            # Process files in parallel
            with Pool(cpu_count()) as pool:
                results = pool.map(_process_single_var_csv, process_args)

            # Count successes
            outliers_generated = sum(1 for _, status in results if status == 'success')
            skipped = sum(1 for _, status in results if status == 'skipped')
            failed = len(results) - outliers_generated - skipped

            if outliers_generated > 0:
                print(f"  ✅ Generated {outliers_generated} new files")
            if skipped > 0:
                print(f"  ⏭️  Skipped {skipped} existing files")
            if failed > 0:
                print(f"  ❌ Failed {failed} files")

            self.data_summary['var_outliers'] = outliers_generated + skipped
            print(f"✅ VaR data processed, {outliers_generated + skipped} total outlier files")
            return True

        except Exception as e:
            print(f"❌ Error processing VaR data: {e}")
            import traceback
            traceback.print_exc()
            return False

    def process_ev_data(self):
        """Process EV data using evscrape.py within the ev-explorer directory"""
        print("💰 Processing EV data...")

        temp_csv_name = f"SymbolsExport-Darwinex-Live-Stocks-{self.date_str}.csv"
        source_csv_path = f"var-explorer/{temp_csv_name}"
        temp_csv_path = f"ev-explorer/{temp_csv_name}"
        ev_processed_name = f"SymbolsExport-Darwinex-Live-Stocks-{self.date_str}-EV.csv"
        ev_processed_path = f"ev-explorer/{ev_processed_name}"

        # Check if EV-processed CSV already exists
        if os.path.exists(ev_processed_path):
            print(f"⏭️  EV-processed CSV already exists for {self.date_str}, skipping EV scraping")

            # Check if outlier files also exist
            ev_outlier_file = f"SymbolsExport-Darwinex-Live-Stocks-{self.date_str}-EV-ev_outlier.txt"
            ev_var_outlier_file = f"SymbolsExport-Darwinex-Live-Stocks-{self.date_str}-EV-ev_var_outlier.txt"

            existing_ev_files = []
            if os.path.exists(f"ev-explorer/{ev_outlier_file}"):
                existing_ev_files.append(ev_outlier_file)
            if os.path.exists(f"ev-explorer/{ev_var_outlier_file}"):
                existing_ev_files.append(ev_var_outlier_file)

            force_ev = 'ev' in self.force_explorers or self.force_regenerate
            if existing_ev_files and not force_ev:
                print(f"⏭️  {len(existing_ev_files)} EV outlier files already exist for {self.date_str}")
                print("   Use --force-ev to regenerate EV files")
            else:
                print("📊 Running EV outlier analysis...")
                subprocess.run(['python3', 'ev_outlier.py', ev_processed_name],
                             cwd='ev-explorer', capture_output=False, text=True)
                print("📈 Running EV VaR outlier analysis...")
                subprocess.run(['python3', 'ev_var_outlier.py', ev_processed_name],
                             cwd='ev-explorer', capture_output=False, text=True)

            self.data_summary['ev_processed'] = True
            return True

        if not os.path.exists(source_csv_path):
            print("⚠️ Warning: No stocks CSV available for EV processing")
            return False

        try:
            # Copy stocks file to ev-explorer directory for processing
            shutil.copy(source_csv_path, temp_csv_path)

            # Run EV scraping in ev-explorer directory
            print("🔍 Running EV scraping...")
            result = subprocess.run(['python3', 'evscrape.py', temp_csv_name],
                                  cwd='ev-explorer', capture_output=False, text=True)

            if result.returncode != 0:
                print(f"❌ EV scraping failed with return code: {result.returncode}")
                # The temp file might still exist if evscrape fails before removing it
                if os.path.exists(temp_csv_path):
                    os.remove(temp_csv_path)
                return False

            # evscrape.py removes the source file (temp_csv_path), so no need to remove it here if successful

            # Run EV outlier analysis in ev-explorer directory
            if os.path.exists(ev_processed_path):
                print("📊 Running EV outlier analysis...")
                subprocess.run(['python3', 'ev_outlier.py', ev_processed_name],
                             cwd='ev-explorer', capture_output=False, text=True)
                print("📈 Running EV VaR outlier analysis...")
                subprocess.run(['python3', 'ev_var_outlier.py', ev_processed_name],
                             cwd='ev-explorer', capture_output=False, text=True)

            self.data_summary['ev_processed'] = True
            print("✅ EV data processed successfully within ev-explorer/")
            return True

        except Exception as e:
            print(f"❌ Error processing EV data: {e}")
            # Clean up any temporary files
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)
            return False

    def process_atr_data(self):
        """Process ATR data - ONLY for current date"""
        print("⚡ Processing ATR data...")

        try:
            # Copy available CSV files to ATR explorer (exclude Crypto - it has its own explorer)
            files_copied = 0
            for asset_type in ['CFD', 'Stocks', 'Futures']:
                csv_file = f"var-explorer/SymbolsExport-Darwinex-Live-{asset_type}-{self.date_str}.csv"
                if os.path.exists(csv_file):
                    shutil.copy(csv_file, 'atr-explorer/')
                    files_copied += 1

            if files_copied > 0:
                # Check if ATR outlier files already exist for this date
                existing_atr_files = [f for f in os.listdir('atr-explorer') if f.endswith('-outlier.txt') and self.date_str in f]

                force_atr = 'atr' in self.force_explorers or self.force_regenerate
                if existing_atr_files and not force_atr:
                    print(f"⏭️ Skipping ATR processing - {len(existing_atr_files)} outlier files already exist for {self.date_str}")
                    print("   Use --force-atr to regenerate ATR files")
                    self.data_summary['atr_files'] = files_copied
                else:
                    # IMPORTANT: Only process CSV files for current date to prevent mass regeneration
                    # Find CSV files for the current date only
                    csv_files = [f for f in os.listdir('atr-explorer')
                                if f.endswith('.csv') and self.date_str in f]

                    print(f"  Processing {len(csv_files)} CSV files for {self.date_str} (parallel using {cpu_count()} cores)...")

                    # Prepare arguments for parallel processing
                    process_args = [(csv_file, self.date_str, force_atr) for csv_file in csv_files]

                    # Process files in parallel
                    with Pool(cpu_count()) as pool:
                        results = pool.map(_process_single_atr_csv, process_args)

                    # Count successes
                    outliers_generated = sum(1 for _, status in results if status == 'success')
                    skipped = sum(1 for _, status in results if status == 'skipped')
                    failed = len(results) - outliers_generated - skipped

                    if outliers_generated > 0:
                        print(f"  ✅ Generated {outliers_generated} new files")
                    if skipped > 0:
                        print(f"  ⏭️  Skipped {skipped} existing files")
                    if failed > 0:
                        print(f"  ❌ Failed {failed} files")

                self.data_summary['atr_files'] = files_copied

            print(f"✅ ATR data processed, {files_copied} files processed")
            return True

        except Exception as e:
            print(f"❌ Error processing ATR data: {e}")
            import traceback
            traceback.print_exc()
            return False

    def process_crypto_data(self):
        """Process Crypto data with crypto-specific analysis and CoinGecko market data"""
        print("₿ Processing Crypto data...")

        try:
            # Check if crypto CSV exists
            crypto_csv = f"crypto-explorer/SymbolsExport-Darwinex-Live-Crypto-{self.date_str}.csv"
            if not os.path.exists(crypto_csv):
                print("⚠️ Warning: No crypto CSV available for processing")
                return False

            # Check if enhanced analysis file already exists
            enhanced_analysis_file = f"crypto-explorer/SymbolsExport-Darwinex-Live-Crypto-{self.date_str}-enhanced-analysis.txt"
            basic_analysis_file = f"crypto-explorer/SymbolsExport-Darwinex-Live-Crypto-{self.date_str}-analysis.txt"
            market_data_file = f"crypto-explorer/SymbolsExport-Darwinex-Live-Crypto-{self.date_str}-market-data.json"
            news_data_file_check = f"crypto-explorer/SymbolsExport-Darwinex-Live-Crypto-{self.date_str}-news-data.json"
            events_data_file_check = f"crypto-explorer/SymbolsExport-Darwinex-Live-Crypto-{self.date_str}-events-data.json"

            force_crypto = 'crypto' in self.force_explorers or self.force_regenerate
            if os.path.exists(enhanced_analysis_file) and not force_crypto:
                print(f"⏭️ Skipping Crypto analysis - enhanced analysis already exists for {self.date_str}")
                print("   Use --force-crypto to regenerate crypto files")
                self.data_summary['crypto_processed'] = True
                self.data_summary['crypto_market_data'] = os.path.exists(market_data_file)
                self.data_summary['crypto_news_data'] = os.path.exists(news_data_file_check)
                self.data_summary['crypto_events_data'] = os.path.exists(events_data_file_check)
                return True

            # Step 1: Fetch market data from CoinGecko
            print("  📡 Fetching cryptocurrency market data from CoinGecko...")
            market_data_output = f"SymbolsExport-Darwinex-Live-Crypto-{self.date_str}-market-data.json"
            fetch_result = subprocess.run(
                ['python3', 'fetch_crypto_data.py', '--output', market_data_output, '--delay', '1.5'],
                cwd='crypto-explorer',
                capture_output=True,
                text=True,
                timeout=180  # 3 minutes timeout for API calls
            )

            market_data_fetched = False
            if fetch_result.returncode == 0:
                print(f"  ✅ Market data fetched successfully")
                market_data_fetched = True
                self.data_summary['crypto_market_data'] = True
            else:
                print(f"  ⚠️ Warning: Market data fetch failed, will run basic analysis only")
                print(f"     Error: {fetch_result.stderr[:200]}")
                self.data_summary['crypto_market_data'] = False

            # Step 1b: Fetch news data from CryptoCompare
            print("  📰 Fetching cryptocurrency news from CryptoCompare...")
            news_data_output = f"SymbolsExport-Darwinex-Live-Crypto-{self.date_str}-news-data.json"
            news_result = subprocess.run(
                ['python3', 'fetch_crypto_news.py', '--output', news_data_output, '--articles', '5'],
                cwd='crypto-explorer',
                capture_output=True,
                text=True,
                timeout=60  # 1 minute timeout for news API
            )

            news_data_file = f"crypto-explorer/{news_data_output}"
            news_data_fetched = False
            if news_result.returncode == 0:
                print(f"  ✅ News data fetched successfully")
                news_data_fetched = True
                self.data_summary['crypto_news_data'] = True
            else:
                print(f"  ⚠️ Warning: News data fetch failed, will proceed without news")
                print(f"     Error: {news_result.stderr[:200]}")
                self.data_summary['crypto_news_data'] = False

            # Step 1c: Fetch events data from CoinMarketCal (if API key available)
            events_data_output = f"SymbolsExport-Darwinex-Live-Crypto-{self.date_str}-events-data.json"
            events_data_file = f"crypto-explorer/{events_data_output}"
            events_data_fetched = False

            # Load API key from .env file if available
            api_key = os.environ.get('COINMARKETCAL_API_KEY')
            if not api_key or api_key == 'your_coinmarketcal_api_key_here':
                # Try to load from .env file
                env_file = '.env'
                if os.path.exists(env_file):
                    with open(env_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                key, value = line.split('=', 1)
                                if key.strip() == 'COINMARKETCAL_API_KEY':
                                    api_key = value.strip()
                                    break

            # Check if COINMARKETCAL_API_KEY is set and valid
            if api_key and api_key != 'your_coinmarketcal_api_key_here':
                # Read the CSV to get only the crypto symbols that are actually present
                csv_filename = f"SymbolsExport-Darwinex-Live-Crypto-{self.date_str}.csv"
                csv_filepath = f"crypto-explorer/{csv_filename}"

                crypto_symbols = []
                if os.path.exists(csv_filepath):
                    import csv
                    with open(csv_filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f, delimiter=';')
                        for row in reader:
                            symbol = row.get('Symbol', '')
                            # Only include crypto symbols (not forex like EURGBP, EURUSD)
                            if symbol.endswith('USD') and symbol not in ['EURUSD']:
                                crypto_symbols.append(symbol)

                if crypto_symbols:
                    print(f"  📅 Fetching cryptocurrency events from CoinMarketCal for {len(crypto_symbols)} symbols...")
                    events_cmd = ['python3', 'fetch_crypto_events.py', '--output', events_data_output, '--events', '5', '--symbols'] + crypto_symbols
                    events_result = subprocess.run(
                        events_cmd,
                        cwd='crypto-explorer',
                        capture_output=True,
                        text=True,
                        timeout=60,  # 1 minute timeout for events API
                        env={**os.environ, 'COINMARKETCAL_API_KEY': api_key}
                    )
                else:
                    print(f"  ⚠️ No crypto symbols found in CSV, skipping events fetch")
                    events_result = None

                if events_result and events_result.returncode == 0:
                    print(f"  ✅ Events data fetched successfully")
                    events_data_fetched = True
                    self.data_summary['crypto_events_data'] = True
                elif events_result:
                    print(f"  ⚠️ Warning: Events data fetch failed, will proceed without events")
                    if events_result.stderr:
                        print(f"     Error: {events_result.stderr[:500]}")
                    if "No events data fetched" in events_result.stdout or "No events retrieved" in events_result.stdout:
                        print(f"     Note: CoinMarketCal API returned no events. This may be due to:")
                        print(f"           - Invalid or expired API key")
                        print(f"           - API rate limiting")
                        print(f"           - Coin names not recognized by CoinMarketCal")
                        print(f"     Check your API key at: https://coinmarketcal.com/en/developer")
                    self.data_summary['crypto_events_data'] = False
                else:
                    self.data_summary['crypto_events_data'] = False
            else:
                print(f"  ℹ️  Skipping events fetch (no API key set)")
                print(f"     Set COINMARKETCAL_API_KEY in .env to enable events")
                self.data_summary['crypto_events_data'] = False

            # Step 2: Run enhanced analysis (if market data available) or basic analysis
            csv_filename = f"SymbolsExport-Darwinex-Live-Crypto-{self.date_str}.csv"

            if market_data_fetched and os.path.exists(market_data_file):
                print("  📊 Running enhanced analysis with market data, news, and events...")
                cmd_args = ['python3', 'analyze_enhanced.py', csv_filename, '--market-data', market_data_output]
                if news_data_fetched and os.path.exists(news_data_file):
                    cmd_args.extend(['--news-data', news_data_output])
                if events_data_fetched and os.path.exists(events_data_file):
                    cmd_args.extend(['--events-data', events_data_output])

                analysis_result = subprocess.run(
                    cmd_args,
                    cwd='crypto-explorer',
                    capture_output=True,
                    text=True
                )

                if analysis_result.returncode == 0:
                    with open(enhanced_analysis_file, 'w') as f:
                        f.write(analysis_result.stdout)
                    print(f"  ✅ Enhanced crypto analysis saved to {enhanced_analysis_file}")
                    self.data_summary['crypto_processed'] = True
                    return True
                else:
                    print(f"  ⚠️ Enhanced analysis failed, falling back to basic analysis")
                    print(f"     Error: {analysis_result.stderr[:200]}")

            # Fallback: Run basic analysis (now with enhanced features)
            print("  📊 Running crypto analysis (with percentile/z-score/ratio analysis)...")
            basic_result = subprocess.run(
                ['python3', 'analyze.py', csv_filename],
                cwd='crypto-explorer',
                capture_output=True,
                text=True
            )

            if basic_result.returncode == 0:
                with open(basic_analysis_file, 'w') as f:
                    f.write(basic_result.stdout)
                print(f"  ✅ Crypto analysis saved to {basic_analysis_file}")
                print(f"     (Includes: Percentile Risk Tiers, Z-Score Detection, Ratio Analysis)")
                self.data_summary['crypto_processed'] = True
                return True
            else:
                print(f"  ❌ Crypto analysis failed: {basic_result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"  ❌ Error: Market data fetch timed out (>3 minutes)")
            return False
        except Exception as e:
            print(f"  ❌ Error processing Crypto data: {e}")
            import traceback
            traceback.print_exc()
            return False

    def fetch_financial_data(self):
        """Fetch and process financial data from all sources"""
        print("📊 Fetching and processing financial data...")

        # Copy CSV files from MetaTrader (skip if force regenerate)
        if self.force_regenerate:
            print("🔄 Force regenerate mode: skipping CSV copy, using existing files")
        else:
            if not self.copy_csv_files():
                return None

        # Process each type of data
        self.process_var_data()
        self.process_ev_data()
        self.process_atr_data()
        self.process_crypto_data()

        # Compile data summary
        data = {
            'var_data': self.data_summary.get('var_outliers', 0),
            'atr_data': self.data_summary.get('atr_files', 0),
            'ev_data': self.data_summary.get('ev_processed', False),
            'crypto_data': self.data_summary.get('crypto_processed', False),
            'calculator_data': {},
            'last_updated': datetime.now().isoformat(),
            'date_processed': self.date_str
        }

        print("✅ Financial data processing completed")
        return data

    def _scan_historical_files(self, directory, pattern='-outlier.txt'):
        """Scan directory for historical analysis files and generate grid entries"""
        try:
            files = []
            for file in os.listdir(directory):
                if pattern in file:
                    # Extract date and asset type from filename
                    # Format: SymbolsExport-Darwinex-Live-{AssetType}-{Date}-{pattern}
                    # Remove the pattern suffix to parse the rest
                    base_name = file.replace(pattern, '')
                    parts = base_name.split('-')

                    if len(parts) >= 5:
                        asset_type = parts[3]  # CFD, Stocks, Futures, Crypto
                        date_str = parts[4]    # 2025.09.17

                        # Look for corresponding CSV file
                        csv_file = base_name + '.csv'
                        csv_path = f"{directory}/{csv_file}"

                        files.append({
                            'outlier_file': file,
                            'csv_file': csv_file if os.path.exists(csv_path) else None,
                            'asset_type': asset_type,
                            'date': date_str,
                            'display_name': f"Darwinex-Live ({asset_type}) - {date_str}",
                            'directory': directory
                        })

            # Sort by date descending (newest first)
            files.sort(key=lambda x: x['date'], reverse=True)
            return files[:60]  # Limit to 60 most recent files

        except Exception as e:
            print(f"Error scanning historical files: {e}")
            return []

    def _scan_ev_historical_files(self, directory):
        """Scan EV directory for historical analysis files with special EV naming pattern"""
        try:
            files = []
            processed_dates = set()

            for file in os.listdir(directory):
                if ('ev_outlier.txt' in file or 'ev_var_outlier.txt' in file) and 'EV-' in file:
                    # EV files have format: SymbolsExport-Darwinex-Live-Stocks-{Date}-EV-ev_outlier.txt
                    parts = file.split('-')
                    if len(parts) >= 6:
                        date_str = parts[4]  # 2025.09.17
                        asset_type = parts[3]  # Stocks

                        # Create a unique key for this date/asset combination
                        date_key = f"{date_str}_{asset_type}"

                        if date_key not in processed_dates:
                            processed_dates.add(date_key)

                            # Look for corresponding CSV file
                            csv_file = f"SymbolsExport-Darwinex-Live-{asset_type}-{date_str}-EV.csv"
                            csv_path = f"{directory}/{csv_file}"

                            # Look for both outlier files
                            ev_outlier_file = f"SymbolsExport-Darwinex-Live-{asset_type}-{date_str}-EV-ev_outlier.txt"
                            ev_var_outlier_file = f"SymbolsExport-Darwinex-Live-{asset_type}-{date_str}-EV-ev_var_outlier.txt"

                            ev_outlier_path = f"{directory}/{ev_outlier_file}"
                            ev_var_outlier_path = f"{directory}/{ev_var_outlier_file}"

                            # Add entry for EV outlier if it exists
                            if os.path.exists(ev_outlier_path):
                                files.append({
                                    'outlier_file': ev_outlier_file,
                                    'csv_file': csv_file if os.path.exists(csv_path) else None,
                                    'asset_type': asset_type,
                                    'date': date_str,
                                    'display_name': f"EV Analysis ({asset_type}) - {date_str}",
                                    'directory': directory
                                })

                            # Add entry for EV VaR outlier if it exists
                            if os.path.exists(ev_var_outlier_path):
                                files.append({
                                    'outlier_file': ev_var_outlier_file,
                                    'csv_file': csv_file if os.path.exists(csv_path) else None,
                                    'asset_type': asset_type,
                                    'date': date_str,
                                    'display_name': f"EV VaR Analysis ({asset_type}) - {date_str}",
                                    'directory': directory
                                })

            # Sort by date descending (newest first), then by type
            files.sort(key=lambda x: (x['date'], x['display_name']), reverse=True)
            return files[:60]  # Limit to 60 most recent files

        except Exception as e:
            print(f"Error scanning EV historical files: {e}")
            return []

    def _generate_file_grid_entries(self, files):
        """Generate HTML grid entries for file listings"""
        grid_html = ""
        for file_info in files:
            outlier_path = f"{file_info['directory']}/{file_info['outlier_file']}"
            csv_path = f"{file_info['directory']}/{file_info['csv_file']}" if file_info['csv_file'] else ""

            grid_html += f'''
            <div class="file-entry" data-action="open-modal-with-file" data-outlier-file="{outlier_path}" data-csv-file="{csv_path}" data-display-name="{file_info['display_name']}">
                <a href="#" data-action="open-modal-with-file" data-outlier-file="{outlier_path}" data-csv-file="{csv_path}" data-display-name="{file_info['display_name']}">
                    {file_info['display_name']}
                </a>
            </div>'''

        return grid_html

    def _generate_modal_system_css(self):
        """Generate complete modal system CSS"""
        return '''
        /* Grid Styles */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .file-entry {
            background-color: #000;
            border: 2px solid rgba(0, 255, 0, 0.5);
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .file-entry:hover {
            background-color: #001100;
            color: #00ff00;
            transform: scale(1.02);
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        }
        .file-entry a {
            color: #00ff00;
            text-decoration: none;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }
        .file-entry a:hover {
            text-decoration: underline;
        }

        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.8);
            padding-top: 60px;
        }
        .modal-content {
            background-color: #000;
            margin: 5% auto;
            padding: 10px;
            border: 2px solid #00ff00;
            max-width: fit-content;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            animation-name: animatetop;
            animation-duration: 0.4s
        }
        .modal-header {
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-bottom: 1px solid rgba(0, 255, 0, 0.5);
            padding-bottom: 5px;
            margin-bottom: 5px;
        }
        .modal-header h2 {
            margin: 0;
            color: #00ff00;
            font-size: 1.2em;
        }
        .modal-header a {
            color: #00ff00;
            text-decoration: none;
            font-weight: bold;
            border: 2px solid #00ff00;
            padding: 2px 5px;
            margin-left: 10px;
        }
        .modal-header a:hover {
            text-decoration: underline;
        }
        .close-button {
            color: #00ff00;
            font-size: 28px;
            font-weight: bold;
            border: 2px solid #00ff00;
            padding: 0 5px;
            line-height: 1;
        }
        .close-button:hover,
        .close-button:focus {
            color: #00ff00;
            text-decoration: none;
            cursor: pointer;
            background-color: #001100;
        }
        .modal-body {
            white-space: pre;
            max-height: 60vh;
            overflow-y: auto;
            overflow-x: auto;
            color: #00ff00;
            font-size: 1.2em;
            padding: 15px;
        }
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
            gap: 10px;
            padding: 0 15px;
        }
        .nav-button {
            background-color: #000;
            color: #00ff00;
            border: 2px solid #00ff00;
            padding: 10px 20px;
            cursor: pointer;
            font-family: "Courier New", monospace;
            transition: all 0.2s ease;
        }
        .nav-button:hover {
            background-color: #001100;
            transform: scale(1.02);
        }
        .nav-counter {
            color: #00ff00;
            font-family: "Courier New", monospace;
        }
        @keyframes animatetop {
            from {top: -300px; opacity: 0}
            to {top: 0; opacity: 1}
        }

        @media screen and (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            .modal {
                padding-top: 20px;
            }
            .modal-content {
                margin: 2% auto;
                width: 95%;
                max-height: 90vh;
                overflow-y: auto;
            }
            .modal-header {
                flex-wrap: wrap;
                gap: 8px;
            }
            .modal-header h2 {
                font-size: 1em;
                margin-bottom: 8px;
                flex: 1 0 100%;
            }
            .modal-header a {
                font-size: 0.7em;
                padding: 4px 8px;
                margin: 2px;
            }
            .modal-body {
                font-size: 0.65em;
                white-space: pre;
                overflow-x: auto;
                max-height: calc(90vh - 160px);
                padding: 10px;
            }
            .nav-button {
                padding: 8px 15px;
                font-size: 14px;
                min-width: 60px;
            }
            .nav-counter {
                font-size: 0.8em;
            }
        }'''

    def _generate_modal_javascript(self, explorer_type):
        """Generate script tag references to external JavaScript files"""
        js_file_map = {
            'var': '/js/var-explorer.js',
            'atr': '/js/atr-explorer.js',
            'ev': '/js/ev-explorer.js'
        }
        js_file = js_file_map.get(explorer_type, '/js/var-explorer.js')
        return f'<script src="{js_file}"></script>'

    def generate_var_explorer(self, data):
        """Generate VaR Explorer page with full modal functionality"""
        print("🔧 Generating VaR Explorer...")

        # Scan for historical VaR files
        historical_files = self._scan_historical_files('var-explorer')
        grid_entries = self._generate_file_grid_entries(historical_files)
        modal_js = self._generate_modal_javascript('var')

        var_breadcrumbs = self.breadcrumb_paths['var_explorer'][:-1] + [{'name': self.breadcrumb_paths['var_explorer'][-1]['name'], 'url': None}]
        breadcrumbs_html = self.seo_manager.generate_breadcrumbs(var_breadcrumbs)
        breadcrumb_css = self.seo_manager.generate_breadcrumb_css()

        # Create page config for VaR Explorer
        page_config = {
            'title': 'VaR Explorer - MarketWizardry.org',
            'canonical_url': 'https://marketwizardry.org/var-explorer.html',
            'description': 'Value at Risk calculations for degenerates who need mathematical proof their portfolio is doomed. Watch your money evaporate with scientific precision.',
            'keywords': PAGE_CONFIGS['explorer']['keywords_base'],
            'og_title': 'VaR Explorer - MarketWizardry.org',
            'og_description': 'Advanced Value at Risk analysis tools for professional traders and risk managers.',
            'twitter_title': 'VaR Explorer - MarketWizardry.org',
            'twitter_description': 'Professional VaR analysis tools and risk management.',
            'twitter_label1': PAGE_CONFIGS['explorer']['twitter_label1'],
            'twitter_data1': PAGE_CONFIGS['explorer']['twitter_data1'],
            'twitter_label2': PAGE_CONFIGS['explorer']['twitter_label2'],
            'twitter_data2': PAGE_CONFIGS['explorer']['twitter_data2']
        }
        meta_tags = self.seo_manager.generate_enhanced_meta_tags(page_config)

        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
{meta_tags}

    <link rel="stylesheet" href="/css/shared-styles.css">
</head>
<body>
{breadcrumbs_html}
    <div class="container">
        <h1>VaR Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Value at Risk calculations for degenerates who need mathematical proof their portfolio is doomed. Watch your money evaporate with scientific precision.</div>
        <div class="crt-divider"></div>

        <div class="grid">
            {grid_entries}
        </div>
    </div>

    <!-- Modal Structure -->
    <div id="outlier-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modal-title">File Analysis</h2>
                <div class="crt-divider"></div>
                <div class="modal-button-bar">
                    <a id="csv-link" href="#" target="_blank">Download CSV</a>
                    <button class="nav-button" data-action="previous">← Previous</button>
                    <span class="nav-counter" id="nav-counter">1 of 1</span>
                    <button class="nav-button" data-action="next">Next →</button>
                    <button class="close-button" data-action="close-modal">Close</button>
                </div>
            </div>
            <div class="modal-body">
                <pre id="outlier-content">Loading...</pre>
            </div>
        </div>
    </div>

    {modal_js}
</body>
</html>'''

        with open('var-explorer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ VaR Explorer generated with {len(historical_files)} historical files")

    def generate_atr_explorer(self, data):
        """Generate ATR Explorer page with full modal system and historical files"""
        print("🔧 Generating ATR Explorer...")

        # Scan historical ATR files
        atr_files = self._scan_historical_files('atr-explorer', '-outlier.txt')
        file_grid_html = self._generate_file_grid_entries(atr_files)
        modal_js = self._generate_modal_javascript('atr')

        atr_breadcrumbs = self.breadcrumb_paths['atr_explorer'][:-1] + [{'name': self.breadcrumb_paths['atr_explorer'][-1]['name'], 'url': None}]
        breadcrumbs_html = self.seo_manager.generate_breadcrumbs(atr_breadcrumbs)
        breadcrumb_css = self.seo_manager.generate_breadcrumb_css()

        # Create page config for ATR Explorer
        page_config = {
            'title': 'ATR Explorer - MarketWizardry.org',
            'canonical_url': 'https://marketwizardry.org/atr-explorer.html',
            'description': 'Average True Range analysis for those who want to measure market volatility with surgical precision before it eviscerates their account.',
            'keywords': PAGE_CONFIGS['explorer']['keywords_base'],
            'og_title': 'ATR Explorer - MarketWizardry.org',
            'og_description': 'Advanced Average True Range analysis tools for volatility measurement and risk management.',
            'twitter_title': 'ATR Explorer - MarketWizardry.org',
            'twitter_description': 'Professional ATR volatility analysis tools.',
            'twitter_label1': PAGE_CONFIGS['explorer']['twitter_label1'],
            'twitter_data1': PAGE_CONFIGS['explorer']['twitter_data1'],
            'twitter_label2': PAGE_CONFIGS['explorer']['twitter_label2'],
            'twitter_data2': PAGE_CONFIGS['explorer']['twitter_data2']
        }
        meta_tags = self.seo_manager.generate_enhanced_meta_tags(page_config)

        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
{meta_tags}

    <link rel="stylesheet" href="/css/shared-styles.css">
</head>
<body>
{breadcrumbs_html}
    <div class="container">
        <h1>ATR Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Average True Range analysis for those who want to measure market volatility with surgical precision before it eviscerates their account.</div>
        <div class="crt-divider"></div>


        <div class="grid">
            {file_grid_html}
        </div>
    </div>

    <!-- Modal Structure -->
    <div id="outlier-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modal-title">File Analysis</h2>
                <div class="crt-divider"></div>
                <div class="modal-button-bar">
                    <a id="csv-link" href="#" target="_blank">Download CSV</a>
                    <button class="nav-button" data-action="previous">← Previous</button>
                    <span class="nav-counter" id="nav-counter">1 of 1</span>
                    <button class="nav-button" data-action="next">Next →</button>
                    <button class="close-button" data-action="close-modal">Close</button>
                </div>
            </div>
            <div class="modal-body">
                <pre id="outlier-content">Loading...</pre>
            </div>
        </div>
    </div>

    {modal_js}
</body>
</html>'''

        with open('atr-explorer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ ATR Explorer generated with {len(atr_files)} historical files")

    def generate_crypto_explorer(self, data):
        """Generate Crypto Explorer page with crypto-specific analysis"""
        print("🔧 Generating Crypto Explorer...")

        # Scan historical crypto analysis files (prefer enhanced, fallback to basic)
        enhanced_files = self._scan_historical_files('crypto-explorer', '-enhanced-analysis.txt')
        basic_files = self._scan_historical_files('crypto-explorer', '-analysis.txt')

        # Merge files, preferring enhanced analysis when available
        crypto_files_dict = {}
        for file in basic_files:
            crypto_files_dict[file['date']] = file
        for file in enhanced_files:
            # Enhanced files take precedence
            crypto_files_dict[file['date']] = file

        # Convert back to list and sort by date
        crypto_files = sorted(crypto_files_dict.values(), key=lambda x: x['date'], reverse=True)[:60]

        file_grid_html = self._generate_file_grid_entries(crypto_files)

        # Reuse shared JS since crypto explorer uses similar modal structure
        modal_js = self._generate_modal_javascript('var')

        crypto_breadcrumbs = [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '₿ Crypto Explorer', 'url': None}
        ]
        breadcrumbs_html = self.seo_manager.generate_breadcrumbs(crypto_breadcrumbs)
        breadcrumb_css = self.seo_manager.generate_breadcrumb_css()

        # Create page config for Crypto Explorer
        page_config = {
            'title': 'Crypto Explorer - MarketWizardry.org',
            'canonical_url': 'https://marketwizardry.org/crypto-explorer.html',
            'description': 'Cryptocurrency market analysis with volatility rankings, correlation matrices, and risk metrics. For those who prefer their financial ruin to be decentralized.',
            'keywords': 'crypto explorer, cryptocurrency analysis, bitcoin volatility, crypto correlation, crypto risk metrics, digital assets',
            'og_title': 'Crypto Explorer - MarketWizardry.org',
            'og_description': 'Advanced cryptocurrency market analysis with volatility rankings and correlation analysis.',
            'twitter_title': 'Crypto Explorer - MarketWizardry.org',
            'twitter_description': 'Professional cryptocurrency market analysis and risk management.',
            'twitter_label1': 'Asset Class',
            'twitter_data1': 'Cryptocurrency',
            'twitter_label2': 'Updates',
            'twitter_data2': 'Daily'
        }
        meta_tags = self.seo_manager.generate_enhanced_meta_tags(page_config)

        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
{meta_tags}

    <link rel="stylesheet" href="/css/shared-styles.css">
</head>
<body>
{breadcrumbs_html}
    <div class="container">
        <h1>Crypto Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Cryptocurrency market analysis with volatility rankings, correlation matrices, and risk metrics. For those who prefer their financial ruin to be decentralized.</div>
        <div class="crt-divider"></div>

        <div class="grid">
            {file_grid_html}
        </div>
    </div>

    <!-- Modal Structure -->
    <div id="outlier-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modal-title">Crypto Analysis</h2>
                <div class="crt-divider"></div>
                <div class="modal-button-bar">
                    <a id="csv-link" href="#" target="_blank">Download CSV</a>
                    <a id="report-link" href="#" target="_blank" download>Download Report</a>
                    <button class="nav-button" data-action="previous">← Previous</button>
                    <span class="nav-counter" id="nav-counter">1 of 1</span>
                    <button class="nav-button" data-action="next">Next →</button>
                    <button class="close-button" data-action="close-modal">Close</button>
                </div>
            </div>
            <div class="modal-body">
                <pre id="outlier-content">Loading...</pre>
            </div>
        </div>
    </div>

    <script src="/js/crypto-explorer.js"></script>
</body>
</html>'''

        with open('crypto-explorer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Crypto Explorer generated with {len(crypto_files)} historical files")

    def generate_ev_explorer(self, data):
        """Generate EV Explorer page with full modal system and historical files"""
        print("🔧 Generating EV Explorer...")

        # Scan historical EV files with special naming pattern
        ev_files = self._scan_ev_historical_files('ev-explorer')
        file_grid_html = self._generate_file_grid_entries(ev_files)
        modal_js = self._generate_modal_javascript('ev')

        ev_breadcrumbs = self.breadcrumb_paths['ev_explorer'][:-1] + [{'name': self.breadcrumb_paths['ev_explorer'][-1]['name'], 'url': None}]
        breadcrumbs_html = self.seo_manager.generate_breadcrumbs(ev_breadcrumbs)
        breadcrumb_css = self.seo_manager.generate_breadcrumb_css()

        # Create page config for EV Explorer
        page_config = {
            'title': 'EV Explorer - MarketWizardry.org',
            'canonical_url': 'https://marketwizardry.org/ev-explorer.html',
            'description': 'Enterprise Value analysis for those who want to measure corporate worth before watching it rot in real-time.',
            'keywords': PAGE_CONFIGS['explorer']['keywords_base'],
            'og_title': 'EV Explorer - MarketWizardry.org',
            'og_description': 'Advanced Enterprise Value analysis tools for corporate valuation and fundamental analysis.',
            'twitter_title': 'EV Explorer - MarketWizardry.org',
            'twitter_description': 'Professional Enterprise Value analysis tools.',
            'twitter_label1': PAGE_CONFIGS['explorer']['twitter_label1'],
            'twitter_data1': PAGE_CONFIGS['explorer']['twitter_data1'],
            'twitter_label2': PAGE_CONFIGS['explorer']['twitter_label2'],
            'twitter_data2': PAGE_CONFIGS['explorer']['twitter_data2']
        }
        meta_tags = self.seo_manager.generate_enhanced_meta_tags(page_config)

        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
{meta_tags}

    <link rel="stylesheet" href="/css/shared-styles.css">
</head>
<body>
{breadcrumbs_html}
    <div class="container">
        <h1>EV Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Enterprise Value analysis for those who want to measure corporate worth before watching it evaporate in real-time.</div>
        <div class="crt-divider"></div>


        <div class="grid">
            {file_grid_html}
        </div>
    </div>

    <!-- Modal Structure -->
    <div id="outlier-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modal-title">File Analysis</h2>
                <div class="crt-divider"></div>
                <div class="modal-button-bar">
                    <a id="csv-link" href="#" target="_blank">Download CSV</a>
                    <button class="nav-button" data-action="previous">← Previous</button>
                    <span class="nav-counter" id="nav-counter">1 of 1</span>
                    <button class="nav-button" data-action="next">Next →</button>
                    <button class="close-button" data-action="close-modal">Close</button>
                </div>
            </div>
            <div class="modal-body">
                <pre id="outlier-content">Loading...</pre>
            </div>
        </div>
    </div>

    {modal_js}
</body>
</html>'''

        with open('ev-explorer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ EV Explorer generated with {len(ev_files)} historical files")

    def _get_latest_date_from_directory(self, directory):
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

    def _process_calculator_outliers(self, directory, date_str, var_data):
        """Process outlier files in a given directory."""
        if not os.path.exists(directory):
            return

        for filename in os.listdir(directory):
            if filename.endswith(f"-{date_str}-outlier.txt"):
                outlier_type = 'var'  # default
                if 'ev_outlier' in filename:
                    outlier_type = 'ev'
                elif 'atr' in directory:
                    outlier_type = 'atr'

                outlier_file_path = os.path.join(directory, filename)
                with open(outlier_file_path, 'r') as f:
                    for line in f:
                        symbol = line.strip()
                        if symbol in var_data:
                            if outlier_type not in var_data[symbol]['outliers']:
                                var_data[symbol]['outliers'].append(outlier_type)

    def update_calculator_data(self, data):
        """Update calculator with fresh financial data - integrated functionality"""
        print("🔧 Updating calculator data...")

        try:
            var_dir = 'var-explorer'
            atr_dir = 'atr-explorer'
            ev_dir = 'ev-explorer'

            # Use the current date_str or find latest
            date_str = self.date_str
            if not date_str:
                date_str = self._get_latest_date_from_directory(var_dir)
                if not date_str:
                    print("❌ No CSV files found to process.")
                    self.data_summary['calculator_updated'] = False
                    return

            print(f"📅 Processing calculator data for date: {date_str}")

            var_data = {}

            # Process var-explorer files
            symbols_processed = 0
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
                            'industry': row.get('IndustryName', 'Unknown'),
                            'description': row['Description'],
                            'asset_class': asset_type,
                            'atr_d1': row['ATR_D1'],
                            'atr_w1': row['ATR_W1'],
                            'atr_mn1': row['ATR_MN1'],
                            'outliers': [],
                            'ev_data': {}
                        }
                        symbols_processed += 1

            # Process crypto-explorer file
            crypto_file_path = f"crypto-explorer/SymbolsExport-Darwinex-Live-Crypto-{date_str}.csv"
            if os.path.exists(crypto_file_path):
                df = pd.read_csv(crypto_file_path, sep=';')
                for _, row in df.iterrows():
                    symbol = row['Symbol']
                    var_data[symbol] = {
                        'var': row['VaR_1_Lot'],
                        'price': row['BidPrice'],
                        'sector': 'Crypto Currency',
                        'industry': row.get('IndustryName', 'Cryptocurrency'),
                        'description': row['Description'],
                        'asset_class': 'crypto',
                        'atr_d1': row['ATR_D1'],
                        'atr_w1': row['ATR_W1'],
                        'atr_mn1': row['ATR_MN1'],
                        'outliers': [],
                        'ev_data': {}
                    }
                    symbols_processed += 1

            # Process ev-explorer file
            ev_file_path = f"{ev_dir}/SymbolsExport-Darwinex-Live-Stocks-{date_str}-EV.csv"
            ev_symbols_processed = 0
            if os.path.exists(ev_file_path):
                ev_df = pd.read_csv(ev_file_path, sep=';')
                for _, row in ev_df.iterrows():
                    symbol = row['Symbol']
                    if symbol in var_data:
                        var_data[symbol]['ev_data'] = {
                            'market_cap': row.get('Market Cap', None),
                            'enterprise_value': row.get('Enterprise Value', None),
                            'mcap_ev_ratio': row.get('MCap/EV (%)', None),
                            'next_earnings_date': row.get('Next Earnings Date', 'Not Available'),
                            'next_dividend_date': row.get('Next Dividend Date', 'Not Available'),
                            'var_to_ask_ratio': row.get('VaR_to_Ask_Ratio', None)
                        }
                        ev_symbols_processed += 1

            # Process outlier files
            self._process_calculator_outliers(var_dir, date_str, var_data)
            self._process_calculator_outliers(atr_dir, date_str, var_data)
            self._process_calculator_outliers(ev_dir, date_str, var_data)

            # Generate JS file with metadata
            js_content = f"""// Complete dataset generated on {datetime.now()}
// Total symbols: {len(var_data)}
const varData = {json.dumps(var_data, indent=12)};

// Make varData available globally
window.varData = varData;"""

            with open('calculator_complete_data.js', 'w') as f:
                f.write(js_content)

            print(f"✅ Calculator data updated successfully")
            print(f"📊 Processed {symbols_processed} total symbols")
            print(f"💰 Enhanced {ev_symbols_processed} symbols with EV data")
            print(f"📁 Generated calculator_complete_data.js ({len(var_data)} symbols)")

            self.data_summary['calculator_updated'] = True
            self.data_summary['calculator_symbols'] = len(var_data)
            self.data_summary['calculator_ev_symbols'] = ev_symbols_processed

        except Exception as e:
            print(f"❌ Error updating calculator: {e}")
            self.data_summary['calculator_updated'] = False

    def run_full_update(self):
        """Run complete update of all financial tools"""
        print("🚀 Starting unified financial tools update...")
        start_time = time.time()

        if self.html_only:
            print("📄 HTML-only mode: Regenerating HTML content using existing data...")
            # Create minimal data structure for HTML generation
            data = {
                'var_data': 0,
                'atr_data': 0,
                'ev_data': False,
                'calculator_data': {},
                'last_updated': datetime.now().isoformat(),
                'date_processed': self.date_str
            }
        else:
            # Fetch fresh data
            data = self.fetch_financial_data()
            if not data:
                print("❌ Failed to fetch data, aborting update")
                return False

        # Update all tools
        self.generate_var_explorer(data)
        self.generate_atr_explorer(data)
        self.generate_crypto_explorer(data)
        self.generate_ev_explorer(data)

        if not self.html_only:
            self.update_calculator_data(data)
        else:
            print("⏭️  Skipping calculator data update in HTML-only mode")

        elapsed_time = time.time() - start_time
        mode_text = "HTML content" if self.html_only else "financial tools"
        print(f"\n✅ All {mode_text} updated successfully!")
        print(f"⏱️  Total time: {elapsed_time:.2f} seconds")
        print(f"📅 Update completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return True

def main():
    """Main execution function"""
    import sys

    # Check for help flag
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
🚀 MarketWizardry.org Financial Tools Updater

Usage: python3 update_all_tools.py [DATE] [OPTIONS]

Arguments:
    DATE            Optional date in YYYY.MM.DD format (defaults to today)

Options:
    --force         Force regenerate ALL explorers (use with caution!)
    --force-var     Force regenerate VaR explorer only
    --force-atr     Force regenerate ATR explorer only
    --force-ev      Force regenerate EV explorer only
    --force-crypto  Force regenerate Crypto explorer only
    --html-only     Only regenerate HTML content using existing data files
                    (Skips data fetching and processing)

Examples:
    python3 update_all_tools.py                           # HTML-only mode when no date specified
    python3 update_all_tools.py 2025.09.24                # Update for specific date, skip existing files
    python3 update_all_tools.py 2025.09.24 --force-crypto # Update crypto only for specific date
    python3 update_all_tools.py --force-crypto            # Regenerate all crypto reports
    python3 update_all_tools.py --force                   # Force regenerate ALL explorers (not recommended)
    python3 update_all_tools.py --html-only               # HTML-only mode for today

Default behavior when no date specified: HTML-only mode (regenerate HTML using existing data)
Default behavior with date specified: Only generate missing files to preserve original creation timestamps.
        """)
        exit(0)

    # Accept date parameter from command line
    date_args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    date_specified = len(date_args) > 0
    date_str = date_args[0] if date_specified else datetime.now().strftime('%Y.%m.%d')

    # Parse force flags
    force_regenerate = '--force' in sys.argv
    force_explorers = []
    if '--force-var' in sys.argv:
        force_explorers.append('var')
    if '--force-atr' in sys.argv:
        force_explorers.append('atr')
    if '--force-ev' in sys.argv:
        force_explorers.append('ev')
    if '--force-crypto' in sys.argv:
        force_explorers.append('crypto')

    # HTML-only mode: explicit flag OR when no date is specified (default behavior)
    html_only = '--html-only' in sys.argv or not date_specified

    if html_only and date_specified:
        print(f"📄 HTML-only mode: Regenerating HTML content for {date_str}")
    elif html_only:
        print("📄 HTML-only mode: Regenerating HTML content using existing data")

    if force_explorers:
        print(f"🔄 Force regenerating: {', '.join(force_explorers)} explorer(s)")

    updater = FinancialToolsUpdater(date_str, force_regenerate=force_regenerate, html_only=html_only, force_explorers=force_explorers)
    success = updater.run_full_update()

    if success:
        print(f"\n🎯 All MarketWizardry.org financial tools are now up to date for {date_str}!")
    else:
        print(f"\n❌ Update failed for {date_str} - please check the errors above")
        exit(1)

if __name__ == "__main__":
    main()