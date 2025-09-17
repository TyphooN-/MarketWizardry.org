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
from datetime import datetime, date
from seo_templates import SEOManager, get_breadcrumb_paths, PAGE_CONFIGS, REDIRECT_SCRIPT_TEMPLATE

class FinancialToolsUpdater:
    def __init__(self, date_str=None):
        self.seo_manager = SEOManager()
        self.breadcrumb_paths = get_breadcrumb_paths()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.date_str = date_str or datetime.now().strftime('%Y.%m.%d')
        self.data_summary = {}

    def copy_csv_files(self):
        """Copy CSV files from MetaTrader directories"""
        print(f"📂 Copying CSV files for {self.date_str} from MetaTrader directories...")

        files_copied = 0
        mt_paths = {
            'stocks': f"/home/typhoon/.mt5_9/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-Stocks-{self.date_str}.csv",
            'cfd': f"/home/typhoon/.mt5_10/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-CFD-{self.date_str}.csv",
            'futures': f"/home/typhoon/.mt5_11/drive_c/Program Files/Darwinex MetaTrader 5/MQL5/Files/SymbolsExport-Darwinex-Live-Futures-{self.date_str}.csv"
        }

        for asset_type, source_path in mt_paths.items():
            if os.path.exists(source_path):
                shutil.copy(source_path, 'var-explorer/')
                print(f"✅ Copied {asset_type.title()} CSV for {self.date_str}")
                files_copied += 1
            else:
                print(f"⚠️ Warning: {asset_type.title()} CSV not found for {self.date_str}")

        if files_copied == 0:
            print(f"❌ Error: No CSV files found for date {self.date_str}")
            return False

        print(f"📊 Successfully copied {files_copied} CSV file(s)")
        return True

    def process_var_data(self):
        """Process VaR data using outlier.py script"""
        print("📈 Processing VaR data...")

        try:
            # Run outlier analysis script
            result = subprocess.run(['bash', 'run_outlier_analysis.sh'],
                                  cwd='var-explorer', capture_output=True, text=True)

            if result.returncode != 0:
                print(f"⚠️ Warning: Outlier analysis script failed: {result.stderr}")

            # Count outlier files generated
            outlier_files = [f for f in os.listdir('var-explorer') if f.endswith('-outlier.txt') and self.date_str in f]
            self.data_summary['var_outliers'] = len(outlier_files)

            print(f"✅ VaR data processed, {len(outlier_files)} outlier files generated")
            return True

        except Exception as e:
            print(f"❌ Error processing VaR data: {e}")
            return False

    def process_ev_data(self):
        """Process EV data using evscrape.py within the ev-explorer directory"""
        print("💰 Processing EV data...")

        temp_csv_name = f"SymbolsExport-Darwinex-Live-Stocks-{self.date_str}.csv"
        source_csv_path = f"var-explorer/{temp_csv_name}"
        temp_csv_path = f"ev-explorer/{temp_csv_name}"

        if not os.path.exists(source_csv_path):
            print("⚠️ Warning: No stocks CSV available for EV processing")
            return False

        try:
            # Copy stocks file to ev-explorer directory for processing
            shutil.copy(source_csv_path, temp_csv_path)

            # Run EV scraping in ev-explorer directory
            result = subprocess.run(['python3', 'evscrape.py', temp_csv_name],
                                  cwd='ev-explorer', capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ EV scraping failed: {result.stderr}")
                # The temp file might still exist if evscrape fails before removing it
                if os.path.exists(temp_csv_path):
                    os.remove(temp_csv_path)
                return False

            # evscrape.py removes the source file (temp_csv_path), so no need to remove it here if successful

            # Run EV outlier analysis in ev-explorer directory
            ev_processed_name = f"SymbolsExport-Darwinex-Live-Stocks-{self.date_str}-EV.csv"
            ev_processed_path = f"ev-explorer/{ev_processed_name}"

            if os.path.exists(ev_processed_path):
                subprocess.run(['python3', 'ev_outlier.py', ev_processed_name],
                             cwd='ev-explorer', capture_output=True, text=True)
                subprocess.run(['python3', 'ev_var_outlier.py', ev_processed_name],
                             cwd='ev-explorer', capture_output=True, text=True)

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
        """Process ATR data"""
        print("⚡ Processing ATR data...")

        try:
            # Copy available CSV files to ATR explorer
            files_copied = 0
            for asset_type in ['CFD', 'Stocks', 'Futures']:
                csv_file = f"var-explorer/SymbolsExport-Darwinex-Live-{asset_type}-{self.date_str}.csv"
                if os.path.exists(csv_file):
                    shutil.copy(csv_file, 'atr-explorer/')
                    files_copied += 1

            if files_copied > 0:
                # Run ATR outlier analysis
                result = subprocess.run(['bash', 'run_outlier_analysis.sh'],
                                      cwd='atr-explorer', capture_output=True, text=True)

                self.data_summary['atr_files'] = files_copied

            print(f"✅ ATR data processed, {files_copied} files processed")
            return True

        except Exception as e:
            print(f"❌ Error processing ATR data: {e}")
            return False

    def fetch_financial_data(self):
        """Fetch and process financial data from all sources"""
        print("📊 Fetching and processing financial data...")

        # Copy CSV files from MetaTrader
        if not self.copy_csv_files():
            return None

        # Process each type of data
        self.process_var_data()
        self.process_ev_data()
        self.process_atr_data()

        # Compile data summary
        data = {
            'var_data': self.data_summary.get('var_outliers', 0),
            'atr_data': self.data_summary.get('atr_files', 0),
            'ev_data': self.data_summary.get('ev_processed', False),
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
                    # Format: SymbolsExport-Darwinex-Live-{AssetType}-{Date}-outlier.txt
                    parts = file.replace('-outlier.txt', '').split('-')
                    if len(parts) >= 5:
                        asset_type = parts[3]  # CFD, Stocks, Futures
                        date_str = parts[4]    # 2025.09.17

                        # Look for corresponding CSV file
                        csv_file = file.replace('-outlier.txt', '.csv')
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
            for file in os.listdir(directory):
                if 'ev_outlier.txt' in file and 'EV-' in file:
                    # EV files have format: SymbolsExport-Darwinex-Live-Stocks-{Date}-EV-ev_outlier.txt
                    parts = file.split('-')
                    if len(parts) >= 6:
                        date_str = parts[4]  # 2025.09.17
                        asset_type = parts[3]  # Stocks

                        # Look for corresponding CSV file
                        csv_file = file.replace('-ev_outlier.txt', '.csv').replace('-EV', '-EV')
                        csv_path = f"{directory}/{csv_file}"

                        # Also look for the var outlier file
                        var_file = file.replace('ev_outlier.txt', 'ev_var_outlier.txt')
                        var_path = f"{directory}/{var_file}"

                        files.append({
                            'outlier_file': file,
                            'csv_file': csv_file if os.path.exists(csv_path) else None,
                            'var_file': var_file if os.path.exists(var_path) else None,
                            'asset_type': asset_type,
                            'date': date_str,
                            'display_name': f"EV Analysis ({asset_type}) - {date_str}",
                            'directory': directory
                        })

            # Sort by date descending (newest first)
            files.sort(key=lambda x: x['date'], reverse=True)
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
            <div class="file-entry" onclick="openModalWithFile('{outlier_path}', '{csv_path}', '{file_info['display_name']}')">
                <a href="#" data-outlier-file="{outlier_path}" data-csv-file="{csv_path}" onclick="event.stopPropagation()">
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
            background-color: #001100;
            border: 2px solid rgba(0, 255, 0, 0.3);
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .file-entry:hover {
            background-color: #002200;
            border-color: rgba(0, 255, 0, 0.6);
            color: #00ff00;
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

    def _generate_modal_javascript(self):
        """Generate complete modal system JavaScript"""
        return '''
        let currentFileIndex = 0;
        let filesList = [];

        function openModalWithFile(outlierFile, csvFile, title) {
            // Find current file index
            for (let i = 0; i < filesList.length; i++) {
                if (filesList[i].outlier === outlierFile) {
                    currentFileIndex = i;
                    break;
                }
            }

            document.getElementById('modal-title').innerText = title;
            document.getElementById('csv-link').href = csvFile;
            document.getElementById('csv-link').style.display = csvFile ? 'inline' : 'none';
            document.getElementById('outlier-modal').style.display = 'block';
            updateNavCounter();

            // Load outlier file content
            fetch(outlierFile)
                .then(response => response.text())
                .then(data => {
                    document.getElementById('outlier-content').textContent = data;
                })
                .catch(error => {
                    document.getElementById('outlier-content').textContent = 'Error loading file: ' + error;
                });
        }

        function closeModal() {
            document.getElementById('outlier-modal').style.display = 'none';
        }

        function previousFile() {
            if (currentFileIndex > 0) {
                currentFileIndex--;
                const file = filesList[currentFileIndex];
                openModalWithFile(file.outlier, file.csv, file.title);
            }
        }

        function nextFile() {
            if (currentFileIndex < filesList.length - 1) {
                currentFileIndex++;
                const file = filesList[currentFileIndex];
                openModalWithFile(file.outlier, file.csv, file.title);
            }
        }

        function updateNavCounter() {
            document.getElementById('nav-counter').textContent =
                `${currentFileIndex + 1} of ${filesList.length}`;
        }

        // Initialize files list from grid entries
        document.addEventListener('DOMContentLoaded', function() {
            const entries = document.querySelectorAll('.file-entry a');
            filesList = Array.from(entries).map(entry => ({
                outlier: entry.getAttribute('data-outlier-file'),
                csv: entry.getAttribute('data-csv-file'),
                title: entry.textContent
            }));
        });

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('outlier-modal');
            if (event.target == modal) {
                closeModal();
            }
        }'''

    def generate_var_explorer(self, data):
        """Generate VaR Explorer page with full modal functionality"""
        print("🔧 Generating VaR Explorer...")

        # Scan for historical VaR files
        historical_files = self._scan_historical_files('var-explorer')
        grid_entries = self._generate_file_grid_entries(historical_files)
        modal_css = self._generate_modal_system_css()
        modal_js = self._generate_modal_javascript()

        var_breadcrumbs = self.breadcrumb_paths['var_explorer'][:-1] + [{'name': '📊 VaR Explorer', 'url': None}]
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

    {REDIRECT_SCRIPT_TEMPLATE}
    <style>
        body {{
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            border-bottom: 2px solid rgba(0, 255, 0, 0.5);
            padding-bottom: 10px;
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }}
        .crt-divider {{
            width: 80%;
            max-width: 600px;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 30px auto;
        }}
        @keyframes scan {{
            0% {{ opacity: 1; width: 0%; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; width: 100%; }}
        }}
        .flavor-text {{
            color: #00ff00;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            font-style: italic;
            font-weight: bold;
            opacity: 0.9;
            animation: flicker 1s infinite;
        }}
        @keyframes flicker {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 1; }}
        }}
{breadcrumb_css}
{modal_css}
    </style>
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
                <a id="csv-link" href="#" target="_blank">Download CSV</a>
                <span class="close-button" onclick="closeModal()">&times;</span>
            </div>
            <div class="modal-body">
                <pre id="outlier-content">Loading...</pre>
            </div>
            <div class="nav-buttons">
                <button class="nav-button" onclick="previousFile()">Previous</button>
                <span class="nav-counter" id="nav-counter">1 of 1</span>
                <button class="nav-button" onclick="nextFile()">Next</button>
            </div>
        </div>
    </div>

    <script>
        {modal_js}
    </script>
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
        modal_css = self._generate_modal_system_css()
        modal_js = self._generate_modal_javascript()

        atr_breadcrumbs = self.breadcrumb_paths['atr_explorer'][:-1] + [{'name': '📈 ATR Explorer', 'url': None}]
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
    <meta charset="UTF-8">
    <meta name="author" content="TyphooN">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ATR Explorer - MarketWizardry.org</title>
    <link rel="canonical" href="https://marketwizardry.org/atr-explorer.html">
    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">

{meta_tags}

    {REDIRECT_SCRIPT_TEMPLATE}
    <style>
        body {{
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            border-bottom: 2px solid rgba(0, 255, 0, 0.5);
            padding-bottom: 10px;
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }}
        .crt-divider {{
            width: 80%;
            max-width: 600px;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 30px auto;
        }}
        @keyframes scan {{
            0% {{ opacity: 1; width: 0%; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; width: 100%; }}
        }}
        .flavor-text {{
            color: #00ff00;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            font-style: italic;
            font-weight: bold;
            opacity: 0.9;
            animation: flicker 1s infinite;
        }}
        @keyframes flicker {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 1; }}
        }}
        .stats {{
            text-align: center;
            color: #00aa00;
            margin: 20px 0;
            font-size: 0.9em;
        }}
{breadcrumb_css}
{modal_css}
    </style>
</head>
<body>
{breadcrumbs_html}

    <div class="container">
        <h1>📈 ATR Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Average True Range analysis for those who want to measure market volatility with surgical precision before it eviscerates their account.</div>
        <div class="crt-divider"></div>

        <div class="stats">
            📊 {len(atr_files)} historical analysis files • 📈 ATR volatility tracking • 🎯 Outlier detection
        </div>

        <div class="grid">
            {file_grid_html}
        </div>
    </div>

    <!-- Modal for displaying file contents -->
    <div id="fileModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="modal-title" id="modalTitle">Loading...</span>
                <div class="modal-controls">
                    <button id="prevBtn" onclick="navigateFiles(-1)" disabled>◀ Previous</button>
                    <span id="fileCounter">1 of 1</span>
                    <button id="nextBtn" onclick="navigateFiles(1)" disabled>Next ▶</button>
                    <span class="close" onclick="closeModal()">&times;</span>
                </div>
            </div>
            <div class="modal-body" id="modalBody">
                Loading content...
            </div>
            <div class="modal-footer" id="modalFooter">
                <!-- CSV download link will be added here if available -->
            </div>
        </div>
    </div>

    <script>
{modal_js}
    </script>

</body>
</html>'''

        with open('atr-explorer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ ATR Explorer generated with {len(atr_files)} historical files")

    def generate_ev_explorer(self, data):
        """Generate EV Explorer page with full modal system and historical files"""
        print("🔧 Generating EV Explorer...")

        # Scan historical EV files with special naming pattern
        ev_files = self._scan_ev_historical_files('ev-explorer')
        file_grid_html = self._generate_file_grid_entries(ev_files)
        modal_css = self._generate_modal_system_css()
        modal_js = self._generate_modal_javascript()

        ev_breadcrumbs = self.breadcrumb_paths['ev_explorer'][:-1] + [{'name': '💰 EV Explorer', 'url': None}]
        breadcrumbs_html = self.seo_manager.generate_breadcrumbs(ev_breadcrumbs)
        breadcrumb_css = self.seo_manager.generate_breadcrumb_css()

        # Create page config for EV Explorer
        page_config = {
            'title': 'EV Explorer - MarketWizardry.org',
            'canonical_url': 'https://marketwizardry.org/ev-explorer.html',
            'description': 'Enterprise Value analysis for those who want to measure corporate worth before watching it evaporate in real-time.',
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
    <meta charset="UTF-8">
    <meta name="author" content="TyphooN">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EV Explorer - MarketWizardry.org</title>
    <link rel="canonical" href="https://marketwizardry.org/ev-explorer.html">
    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">

{meta_tags}

    {REDIRECT_SCRIPT_TEMPLATE}
    <style>
        body {{
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            border-bottom: 2px solid rgba(0, 255, 0, 0.5);
            padding-bottom: 10px;
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
        }}
        .crt-divider {{
            width: 80%;
            max-width: 600px;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 30px auto;
        }}
        @keyframes scan {{
            0% {{ opacity: 1; width: 0%; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; width: 100%; }}
        }}
        .flavor-text {{
            color: #00ff00;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            font-style: italic;
            font-weight: bold;
            opacity: 0.9;
            animation: flicker 1s infinite;
        }}
        @keyframes flicker {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 1; }}
        }}
        .stats {{
            text-align: center;
            color: #00aa00;
            margin: 20px 0;
            font-size: 0.9em;
        }}
{breadcrumb_css}
{modal_css}
    </style>
</head>
<body>
{breadcrumbs_html}

    <div class="container">
        <h1>💰 EV Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Enterprise Value analysis for those who want to measure corporate worth before watching it evaporate in real-time.</div>
        <div class="crt-divider"></div>

        <div class="stats">
            📊 {len(ev_files)} historical analysis files • 💰 Enterprise Value tracking • 🎯 Outlier detection
        </div>

        <div class="grid">
            {file_grid_html}
        </div>
    </div>

    <!-- Modal for displaying file contents -->
    <div id="fileModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="modal-title" id="modalTitle">Loading...</span>
                <div class="modal-controls">
                    <button id="prevBtn" onclick="navigateFiles(-1)" disabled>◀ Previous</button>
                    <span id="fileCounter">1 of 1</span>
                    <button id="nextBtn" onclick="navigateFiles(1)" disabled>Next ▶</button>
                    <span class="close" onclick="closeModal()">&times;</span>
                </div>
            </div>
            <div class="modal-body" id="modalBody">
                Loading content...
            </div>
            <div class="modal-footer" id="modalFooter">
                <!-- CSV download link will be added here if available -->
            </div>
        </div>
    </div>

    <script>
{modal_js}
    </script>

</body>
</html>'''

        with open('ev-explorer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ EV Explorer generated with {len(ev_files)} historical files")

    def update_calculator_data(self, data):
        """Update calculator with fresh financial data"""
        print("🔧 Updating calculator data...")

        try:
            result = subprocess.run(['python3', 'update_calculator_data.py'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Calculator data updated successfully.")
                print(result.stdout)
                self.data_summary['calculator_updated'] = True
            else:
                print(f"❌ Calculator data update failed: {result.stderr}")
                self.data_summary['calculator_updated'] = False

        except Exception as e:
            print(f"❌ Error updating calculator: {e}")

    def run_full_update(self):
        """Run complete update of all financial tools"""
        print("🚀 Starting unified financial tools update...")
        start_time = time.time()

        # Fetch fresh data
        data = self.fetch_financial_data()
        if not data:
            print("❌ Failed to fetch data, aborting update")
            return False

        # Update all tools
        self.generate_var_explorer(data)
        self.generate_atr_explorer(data)
        self.generate_ev_explorer(data)
        self.update_calculator_data(data)

        elapsed_time = time.time() - start_time
        print(f"\n✅ All financial tools updated successfully!")
        print(f"⏱️  Total time: {elapsed_time:.2f} seconds")
        print(f"📅 Update completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return True

def main():
    """Main execution function"""
    import sys

    # Accept date parameter from command line
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime('%Y.%m.%d')

    updater = FinancialToolsUpdater(date_str)
    success = updater.run_full_update()

    if success:
        print(f"\n🎯 All MarketWizardry.org financial tools are now up to date for {date_str}!")
    else:
        print(f"\n❌ Update failed for {date_str} - please check the errors above")
        exit(1)

if __name__ == "__main__":
    main()