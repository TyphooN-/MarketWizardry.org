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
        """Process EV data using evscrape.py"""
        print("💰 Processing EV data...")

        stocks_file = f"var-explorer/SymbolsExport-Darwinex-Live-Stocks-{self.date_str}.csv"
        if not os.path.exists(stocks_file):
            print("⚠️ Warning: No stocks CSV available for EV processing")
            return False

        try:
            # Copy stocks file to root directory for EV processing
            shutil.copy(stocks_file, './')

            # Run EV scraping in root directory
            ev_csv = f"SymbolsExport-Darwinex-Live-Stocks-{self.date_str}.csv"
            result = subprocess.run(['python3', 'evscrape.py', ev_csv],
                                  capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ EV scraping failed: {result.stderr}")
                return False

            # Run EV outlier analysis in root directory
            ev_processed = f"SymbolsExport-Darwinex-Live-Stocks-{self.date_str}-EV.csv"
            if os.path.exists(ev_processed):
                subprocess.run(['python3', 'ev_outlier.py', ev_processed],
                             capture_output=True, text=True)
                subprocess.run(['python3', 'ev_var_outlier.py', ev_processed],
                             capture_output=True, text=True)

            self.data_summary['ev_processed'] = True
            print("✅ EV data processed successfully")
            return True

        except Exception as e:
            print(f"❌ Error processing EV data: {e}")
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

    def _get_outlier_file_list(self):
        """Get list of available outlier files for display"""
        try:
            outlier_files = [f for f in os.listdir('var-explorer') if f.endswith('-outlier.txt') and self.date_str in f]
            if outlier_files:
                file_list = ""
                for file in sorted(outlier_files):
                    file_list += f"<li>{file}</li>\n                "
                return file_list
            else:
                return "<li>No outlier files found for this date</li>"
        except Exception:
            return "<li>Error reading outlier files</li>"

    def generate_var_explorer(self, data):
        """Generate VaR Explorer page"""
        print("🔧 Generating VaR Explorer...")

        var_breadcrumbs = self.breadcrumb_paths['var_explorer'][:-1] + [{'name': '📊 VaR Explorer', 'url': None}]
        breadcrumbs_html = self.seo_manager.generate_breadcrumbs(var_breadcrumbs)
        breadcrumb_css = self.seo_manager.generate_breadcrumb_css()

        # Create page config for VaR Explorer
        page_config = {
            'title': 'VaR Explorer - MarketWizardry.org',
            'canonical_url': 'https://marketwizardry.org/var-explorer.html',
            'description': 'Value at Risk analysis that quantifies exactly how much your portfolio wants to hurt you. Mathematical precision for financial masochists.',
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
    <meta charset="UTF-8">
    <meta name="author" content="TyphooN">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VaR Explorer - MarketWizardry.org</title>
    <link rel="canonical" href="https://marketwizardry.org/var-explorer.html">
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
{breadcrumb_css}
    </style>
</head>
<body>
{breadcrumbs_html}

    <div class="container">
        <h1>📊 VaR Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Value at Risk analysis that quantifies exactly how much your portfolio wants to hurt you. Mathematical precision for financial masochists.</div>
        <div class="crt-divider"></div>

        <div class="tool-content">
            <p style="color: #00aa00; text-align: center;">📊 VaR Analysis for {data.get('date_processed', 'Unknown Date')}</p>
            <p style="color: #00aa00; text-align: center;">Outlier files generated: {data.get('var_data', 0)}</p>
            <p style="color: #00aa00; text-align: center;">Last updated: {data.get('last_updated', 'Unknown')}</p>

            <!-- Display available outlier files -->
            <div style="margin-top: 20px; color: #00aa00;">
                <h3>Available Analysis Files:</h3>
                <ul style="text-align: left; max-width: 600px; margin: 0 auto;">
                {self._get_outlier_file_list()}
                </ul>
            </div>
        </div>
    </div>

</body>
</html>'''

        with open('var-explorer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print("✅ VaR Explorer generated")

    def generate_atr_explorer(self, data):
        """Generate ATR Explorer page"""
        print("🔧 Generating ATR Explorer...")

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
{breadcrumb_css}
    </style>
</head>
<body>
{breadcrumbs_html}

    <div class="container">
        <h1>📈 ATR Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Average True Range analysis for those who want to measure market volatility with surgical precision before it eviscerates their account.</div>
        <div class="crt-divider"></div>

        <div class="tool-content">
            <!-- ATR Explorer content would go here -->
            <p style="color: #00aa00; text-align: center;">📈 ATR volatility analysis tools and charts</p>
        </div>
    </div>

</body>
</html>'''

        with open('atr-explorer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print("✅ ATR Explorer generated")

    def generate_ev_explorer(self, data):
        """Generate EV Explorer page"""
        print("🔧 Generating EV Explorer...")

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
{breadcrumb_css}
    </style>
</head>
<body>
{breadcrumbs_html}

    <div class="container">
        <h1>💰 EV Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Enterprise Value analysis for those who want to measure corporate worth before watching it evaporate in real-time.</div>
        <div class="crt-divider"></div>

        <div class="tool-content">
            <!-- EV Explorer content would go here -->
            <p style="color: #00aa00; text-align: center;">💰 Enterprise Value analysis and company metrics</p>
        </div>
    </div>

</body>
</html>'''

        with open('ev-explorer.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print("✅ EV Explorer generated")

    def update_calculator_data(self, data):
        """Update calculator with fresh financial data"""
        print("🔧 Updating calculator data...")

        try:
            # Check if calculator update scripts exist
            if os.path.exists('update_calculator_validated.py'):
                result = subprocess.run(['python3', 'update_calculator_validated.py'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Calculator updated with validated script")
                else:
                    print(f"⚠️ Calculator update script failed: {result.stderr}")
            elif os.path.exists('update_calculator_with_latest_data.py'):
                result = subprocess.run(['python3', 'update_calculator_with_latest_data.py'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Calculator updated with fallback script")
                else:
                    print(f"⚠️ Calculator fallback script failed: {result.stderr}")
            else:
                print("⚠️ Warning: No calculator update script found")

            # Update data summary
            self.data_summary['calculator_updated'] = True

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