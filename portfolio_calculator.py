#!/usr/bin/env python3
"""
Portfolio Risk Calculator - MarketWizardry.org

Calculate portfolio VaR, ATR, and EV metrics using lots-based position sizing.
Because sometimes you need to know exactly how much you're about to lose.

Features:
- VaR Portfolio Calculator (Value at Risk)
- ATR Portfolio Calculator (Average True Range)
- EV Portfolio Calculator (Enterprise Value Analysis)
"""

import os
import csv
import glob
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import statistics

class SymbolLookupTool:
    """Advanced symbol lookup and outlier detection tool."""

    def __init__(self, calculator_instance):
        self.calc = calculator_instance
        self.outlier_data = self._load_outlier_data()

    def _load_outlier_data(self) -> Dict:
        """Load outlier data from text files."""
        outlier_files = {
            'var': glob.glob("var-explorer/*-outlier.txt"),
            'atr': glob.glob("atr-explorer/*-outlier.txt"),
            'ev': glob.glob("ev-explorer/*-ev_outlier.txt")
        }

        outliers = {'var': [], 'atr': [], 'ev': []}
        for data_type, files in outlier_files.items():
            if files:
                latest_file = max(files, key=lambda x: os.path.getctime(x))
                try:
                    with open(latest_file, 'r') as f:
                        content = f.read()
                        outliers[data_type] = self._parse_outlier_file(content, data_type)
                except Exception as e:
                    print(f"⚠️ Could not load {data_type} outliers: {e}")

        return outliers

    def _parse_outlier_file(self, content: str, data_type: str) -> List[Dict]:
        """Parse outlier file content to extract symbol data."""
        outliers = []
        lines = content.split('\n')

        for line in lines:
            if '|' in line and any(char.isalnum() for char in line.split('|')[0]):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 2:
                    symbol = parts[0].strip()
                    if symbol and symbol.replace('-', '').replace('_', '').isalnum():
                        outliers.append({
                            'symbol': symbol,
                            'reason': 'outlier_detected',
                            'data_type': data_type
                        })

        return outliers

    def lookup_symbol(self, symbol: str) -> Dict:
        """Comprehensive symbol lookup with outlier detection."""
        symbol = symbol.upper()
        result = {
            'symbol': symbol,
            'found_in': [],
            'data': {},
            'outlier_status': {},
            'recommendation': 'unknown'
        }

        # Check VaR data
        if symbol in self.calc.var_data:
            result['found_in'].append('var')
            result['data']['var'] = self.calc.var_data[symbol]
            result['outlier_status']['var'] = self._is_outlier(symbol, 'var')

        # Check ATR data
        if symbol in self.calc.atr_data:
            result['found_in'].append('atr')
            result['data']['atr'] = self.calc.atr_data[symbol]
            result['outlier_status']['atr'] = self._is_outlier(symbol, 'atr')

        # Check EV data
        if symbol in self.calc.ev_data:
            result['found_in'].append('ev')
            result['data']['ev'] = self.calc.ev_data[symbol]
            result['outlier_status']['ev'] = self._is_outlier(symbol, 'ev')

        # Generate recommendation
        result['recommendation'] = self._generate_recommendation(result)

        return result

    def _is_outlier(self, symbol: str, data_type: str) -> bool:
        """Check if symbol is flagged as outlier."""
        return any(outlier['symbol'] == symbol for outlier in self.outlier_data[data_type])

    def _generate_recommendation(self, result: Dict) -> str:
        """Generate trading recommendation based on data."""
        if not result['found_in']:
            return "❌ DATA_MISSING - Symbol not found in any dataset"

        outlier_count = sum(1 for status in result['outlier_status'].values() if status)

        if outlier_count >= 2:
            return "⚠️ HIGH_RISK - Multiple outlier indicators detected"
        elif outlier_count == 1:
            return "⚡ MODERATE_RISK - Single outlier indicator"
        elif len(result['found_in']) >= 2:
            return "✅ LOW_RISK - Complete data available, no outliers"
        else:
            return "📊 PARTIAL_DATA - Limited data available"

    def batch_lookup(self, symbols: List[str]) -> Dict[str, Dict]:
        """Lookup multiple symbols at once."""
        return {symbol: self.lookup_symbol(symbol) for symbol in symbols}

    def find_similar_symbols(self, partial_symbol: str, limit: int = 10) -> List[str]:
        """Find symbols that match partial input."""
        partial = partial_symbol.upper()
        all_symbols = set()

        all_symbols.update(self.calc.var_data.keys())
        all_symbols.update(self.calc.atr_data.keys())
        all_symbols.update(self.calc.ev_data.keys())

        matches = [s for s in all_symbols if partial in s]
        return sorted(matches)[:limit]

    def get_sector_analysis(self, sector: str) -> Dict:
        """Analyze all symbols in a specific sector."""
        sector_symbols = []

        # Find symbols in this sector
        for symbol, data in self.calc.var_data.items():
            if data.get('sector', '').lower() == sector.lower():
                sector_symbols.append(symbol)

        if not sector_symbols:
            return {'error': f"No symbols found in sector: {sector}"}

        # Get data for all symbols in sector
        sector_data = self.batch_lookup(sector_symbols)

        # Calculate sector statistics
        var_ratios = []
        atr_ratios = []

        for symbol, data in sector_data.items():
            if 'var' in data['data']:
                var_ratios.append(data['data']['var']['var_to_ask_ratio'])
            if 'atr' in data['data']:
                atr_ratios.append(data['data']['atr']['atr_d1_ratio'])

        return {
            'sector': sector,
            'symbol_count': len(sector_symbols),
            'symbols': sector_symbols,
            'avg_var_ratio': statistics.mean(var_ratios) if var_ratios else 0,
            'avg_atr_ratio': statistics.mean(atr_ratios) if atr_ratios else 0,
            'outlier_count': sum(1 for data in sector_data.values() if any(data['outlier_status'].values())),
            'data': sector_data
        }

class PortfolioCalculator:
    def __init__(self):
        self.var_data = {}
        self.atr_data = {}
        self.ev_data = {}
        self.latest_files = self._find_latest_files()
        self._load_data()
        self.lookup_tool = SymbolLookupTool(self)

    def _find_latest_files(self) -> Dict[str, List[str]]:
        """Find the latest CSV files for all asset types (Stocks, CFDs, Futures)."""
        latest_files = {}

        # VaR files - get latest for each asset type
        var_patterns = [
            "var-explorer/SymbolsExport-Darwinex-Live-Stocks-*.csv",
            "var-explorer/SymbolsExport-Darwinex-Live-CFD-*.csv",
            "var-explorer/SymbolsExport-Darwinex-Live-Futures-*.csv"
        ]

        var_files = []
        for pattern in var_patterns:
            files = glob.glob(pattern)
            if files:
                latest = max(files, key=lambda x: os.path.getctime(x))
                var_files.append(latest)

        if var_files:
            latest_files['var'] = var_files

        # ATR files - get latest for each asset type
        atr_patterns = [
            "atr-explorer/SymbolsExport-Darwinex-Live-Stocks-*.csv",
            "atr-explorer/SymbolsExport-Darwinex-Live-CFD-*.csv",
            "atr-explorer/SymbolsExport-Darwinex-Live-Futures-*.csv"
        ]

        atr_files = []
        for pattern in atr_patterns:
            files = glob.glob(pattern)
            if files:
                latest = max(files, key=lambda x: os.path.getctime(x))
                atr_files.append(latest)

        if atr_files:
            latest_files['atr'] = atr_files

        # EV files - only stocks available
        ev_files = glob.glob("ev-explorer/SymbolsExport-Darwinex-Live-Stocks-*-EV.csv")
        if ev_files:
            latest_files['ev'] = [max(ev_files, key=lambda x: os.path.getctime(x))]

        return latest_files

    def _load_data(self):
        """Load data from all latest CSV files (Stocks, CFDs, Futures)."""
        print("🔄 Loading latest market data...")

        # Load VaR data from all asset types
        if 'var' in self.latest_files:
            for filename in self.latest_files['var']:
                print(f"📊 Loading VaR data from: {os.path.basename(filename)}")
                self._load_var_data(filename)

        # Load ATR data from all asset types
        if 'atr' in self.latest_files:
            for filename in self.latest_files['atr']:
                print(f"📈 Loading ATR data from: {os.path.basename(filename)}")
                self._load_atr_data(filename)

        # Load EV data
        if 'ev' in self.latest_files:
            for filename in self.latest_files['ev']:
                print(f"💰 Loading EV data from: {os.path.basename(filename)}")
                self._load_ev_data(filename)

    def _load_var_data(self, filename: str):
        """Load VaR data from CSV."""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    symbol = row['Symbol']
                    self.var_data[symbol] = {
                        'ask_price': float(row['AskPrice']),
                        'var_1_lot': float(row['VaR_1_Lot']),
                        'var_to_ask_ratio': float(row['VaR_to_Ask_Ratio']),
                        'industry': row.get('IndustryName', 'Unknown'),
                        'sector': row.get('SectorName', 'Unknown')
                    }
        except Exception as e:
            print(f"❌ Error loading VaR data: {e}")

    def _load_atr_data(self, filename: str):
        """Load ATR data from CSV."""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    symbol = row['Symbol']
                    self.atr_data[symbol] = {
                        'ask_price': float(row['AskPrice']),
                        'atr_d1': float(row['ATR_D1']),
                        'atr_w1': float(row['ATR_W1']),
                        'atr_mn1': float(row['ATR_MN1']),
                        'atr_d1_ratio': float(row['ATR_D1/AskPrice']),
                        'atr_w1_ratio': float(row['ATR_W1/AskPrice']),
                        'atr_mn1_ratio': float(row['ATR_MN1/AskPrice']),
                        'industry': row.get('IndustryName', 'Unknown'),
                        'sector': row.get('SectorName', 'Unknown')
                    }
        except Exception as e:
            print(f"❌ Error loading ATR data: {e}")

    def _load_ev_data(self, filename: str):
        """Load EV data from CSV."""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    symbol = row['Symbol']
                    self.ev_data[symbol] = {
                        'ask_price': float(row['AskPrice']),
                        'enterprise_value': float(row['Enterprise Value']) if row['Enterprise Value'] else 0,
                        'market_cap': float(row['Market Cap']) if row['Market Cap'] else 0,
                        'mcap_ev_ratio': float(row['MCap/EV (%)']) if row['MCap/EV (%)'] else 0,
                        'industry': row.get('IndustryName', 'Unknown'),
                        'sector': row.get('SectorName', 'Unknown')
                    }
        except Exception as e:
            print(f"❌ Error loading EV data: {e}")

    def calculate_portfolio_var(self, positions: Dict[str, float]) -> Dict:
        """Calculate portfolio VaR based on positions (lots)."""
        print("\n🎲 PORTFOLIO VaR ANALYSIS")
        print("=" * 50)

        total_value = 0
        total_var = 0
        position_details = []

        for symbol, lots in positions.items():
            if symbol in self.var_data:
                data = self.var_data[symbol]
                position_value = lots * data['ask_price']
                position_var = lots * data['var_1_lot']

                total_value += position_value
                total_var += position_var

                # Check for outlier status
                lookup_result = self.lookup_tool.lookup_symbol(symbol)
                outlier_warning = " 🚨" if lookup_result['outlier_status'].get('var', False) else ""

                position_details.append({
                    'symbol': symbol,
                    'lots': lots,
                    'price': data['ask_price'],
                    'position_value': position_value,
                    'position_var': position_var,
                    'var_ratio': data['var_to_ask_ratio'],
                    'industry': data['industry'],
                    'sector': data['sector'],
                    'outlier_warning': outlier_warning,
                    'recommendation': lookup_result['recommendation']
                })
            else:
                # Use lookup tool to provide better error message
                lookup_result = self.lookup_tool.lookup_symbol(symbol)
                if 'atr' in lookup_result['found_in'] or 'ev' in lookup_result['found_in']:
                    print(f"⚠️  Symbol \"{symbol}\" not found in VaR database. Using VaR explorer data from latest market session.")
                    # Try to use ATR data as fallback for basic calculation
                    if 'atr' in lookup_result['found_in']:
                        atr_data = lookup_result['data']['atr']
                        estimated_var = lots * atr_data['ask_price'] * atr_data['atr_d1_ratio']
                        total_var += estimated_var
                        position_value = lots * atr_data['ask_price']
                        total_value += position_value

                        position_details.append({
                            'symbol': symbol,
                            'lots': lots,
                            'price': atr_data['ask_price'],
                            'position_value': position_value,
                            'position_var': estimated_var,
                            'var_ratio': atr_data['atr_d1_ratio'],
                            'industry': atr_data['industry'],
                            'sector': atr_data['sector'],
                            'outlier_warning': " 📊 (ATR estimated)",
                            'recommendation': lookup_result['recommendation']
                        })
                else:
                    print(f"❌ Symbol \"{symbol}\" not found in any database. {lookup_result['recommendation']}")

        # Sort by position size
        position_details.sort(key=lambda x: x['position_value'], reverse=True)

        print(f"Portfolio Value: ${total_value:,.2f}")
        print(f"Portfolio VaR (1-day): ${total_var:,.2f}")
        print(f"Portfolio VaR %: {(total_var/total_value)*100:.2f}%")
        print("\nPosition Breakdown:")
        print("-" * 80)

        for pos in position_details:
            print(f"{pos['symbol']:6} | {pos['lots']:8.1f} lots | "
                  f"${pos['position_value']:10,.2f} | VaR: ${pos['position_var']:8,.2f} | "
                  f"{pos['var_ratio']*100:5.2f}% | {pos['industry']}{pos.get('outlier_warning', '')}")

        return {
            'total_value': total_value,
            'total_var': total_var,
            'var_percentage': (total_var/total_value)*100 if total_value > 0 else 0,
            'positions': position_details
        }

    def calculate_portfolio_atr(self, positions: Dict[str, float]) -> Dict:
        """Calculate portfolio ATR metrics based on positions (lots)."""
        print("\n📊 PORTFOLIO ATR ANALYSIS")
        print("=" * 50)

        total_value = 0
        weighted_atr_d1 = 0
        weighted_atr_w1 = 0
        weighted_atr_mn1 = 0
        position_details = []

        for symbol, lots in positions.items():
            if symbol in self.atr_data:
                data = self.atr_data[symbol]
                position_value = lots * data['ask_price']

                total_value += position_value

                position_details.append({
                    'symbol': symbol,
                    'lots': lots,
                    'price': data['ask_price'],
                    'position_value': position_value,
                    'atr_d1': data['atr_d1'],
                    'atr_w1': data['atr_w1'],
                    'atr_mn1': data['atr_mn1'],
                    'atr_d1_ratio': data['atr_d1_ratio'],
                    'atr_w1_ratio': data['atr_w1_ratio'],
                    'atr_mn1_ratio': data['atr_mn1_ratio'],
                    'industry': data['industry'],
                    'sector': data['sector']
                })
            else:
                print(f"⚠️  Warning: {symbol} not found in ATR data")

        # Calculate weighted averages
        if total_value > 0:
            for pos in position_details:
                weight = pos['position_value'] / total_value
                weighted_atr_d1 += weight * pos['atr_d1_ratio']
                weighted_atr_w1 += weight * pos['atr_w1_ratio']
                weighted_atr_mn1 += weight * pos['atr_mn1_ratio']

        # Sort by ATR D1 ratio (highest volatility first)
        position_details.sort(key=lambda x: x['atr_d1_ratio'], reverse=True)

        print(f"Portfolio Value: ${total_value:,.2f}")
        print(f"Weighted ATR D1 %: {weighted_atr_d1*100:.3f}%")
        print(f"Weighted ATR W1 %: {weighted_atr_w1*100:.3f}%")
        print(f"Weighted ATR MN1 %: {weighted_atr_mn1*100:.3f}%")
        print("\nPosition Breakdown (by D1 ATR %):")
        print("-" * 90)

        for pos in position_details:
            print(f"{pos['symbol']:6} | {pos['lots']:8.1f} lots | "
                  f"${pos['position_value']:10,.2f} | "
                  f"D1: {pos['atr_d1_ratio']*100:5.2f}% | "
                  f"W1: {pos['atr_w1_ratio']*100:5.2f}% | "
                  f"MN1: {pos['atr_mn1_ratio']*100:5.2f}% | {pos['industry']}")

        return {
            'total_value': total_value,
            'weighted_atr_d1': weighted_atr_d1,
            'weighted_atr_w1': weighted_atr_w1,
            'weighted_atr_mn1': weighted_atr_mn1,
            'positions': position_details
        }

    def calculate_portfolio_ev(self, positions: Dict[str, float]) -> Dict:
        """Calculate portfolio EV analysis based on positions (lots)."""
        print("\n💼 PORTFOLIO EV ANALYSIS")
        print("=" * 50)

        total_value = 0
        total_market_cap = 0
        total_enterprise_value = 0
        position_details = []

        for symbol, lots in positions.items():
            if symbol in self.ev_data:
                data = self.ev_data[symbol]
                position_value = lots * data['ask_price']

                # Calculate proportional market cap and EV based on position size
                if data['market_cap'] > 0:
                    shares_per_lot = 1  # Assuming 1 share per lot for simplicity
                    total_shares_outstanding = data['market_cap'] / data['ask_price']
                    position_shares = lots * shares_per_lot
                    position_market_cap_weight = position_shares / total_shares_outstanding if total_shares_outstanding > 0 else 0

                    weighted_market_cap = position_market_cap_weight * data['market_cap']
                    weighted_enterprise_value = position_market_cap_weight * data['enterprise_value']
                else:
                    weighted_market_cap = 0
                    weighted_enterprise_value = 0

                total_value += position_value
                total_market_cap += weighted_market_cap
                total_enterprise_value += weighted_enterprise_value

                position_details.append({
                    'symbol': symbol,
                    'lots': lots,
                    'price': data['ask_price'],
                    'position_value': position_value,
                    'market_cap': data['market_cap'],
                    'enterprise_value': data['enterprise_value'],
                    'mcap_ev_ratio': data['mcap_ev_ratio'],
                    'weighted_market_cap': weighted_market_cap,
                    'weighted_enterprise_value': weighted_enterprise_value,
                    'industry': data['industry'],
                    'sector': data['sector']
                })
            else:
                print(f"⚠️  Warning: {symbol} not found in EV data")

        # Calculate portfolio EV metrics
        portfolio_mcap_ev_ratio = (total_market_cap / total_enterprise_value) * 100 if total_enterprise_value > 0 else 0

        # Sort by market cap (largest first)
        position_details.sort(key=lambda x: x['market_cap'], reverse=True)

        print(f"Portfolio Value: ${total_value:,.2f}")
        print(f"Weighted Market Cap: ${total_market_cap:,.0f}")
        print(f"Weighted Enterprise Value: ${total_enterprise_value:,.0f}")
        print(f"Portfolio MCap/EV Ratio: {portfolio_mcap_ev_ratio:.2f}%")
        print("\nPosition Breakdown (by Market Cap):")
        print("-" * 100)

        for pos in position_details:
            market_cap_b = pos['market_cap'] / 1_000_000_000  # Convert to billions
            print(f"{pos['symbol']:6} | {pos['lots']:8.1f} lots | "
                  f"${pos['position_value']:10,.2f} | "
                  f"MCap: ${market_cap_b:6.1f}B | "
                  f"MCap/EV: {pos['mcap_ev_ratio']:6.1f}% | {pos['industry']}")

        return {
            'total_value': total_value,
            'total_market_cap': total_market_cap,
            'total_enterprise_value': total_enterprise_value,
            'portfolio_mcap_ev_ratio': portfolio_mcap_ev_ratio,
            'positions': position_details
        }

    def get_available_symbols(self) -> Dict[str, List[str]]:
        """Get available symbols from each dataset."""
        return {
            'var': list(self.var_data.keys()),
            'atr': list(self.atr_data.keys()),
            'ev': list(self.ev_data.keys())
        }

    def interactive_calculator(self):
        """Interactive portfolio calculator."""
        print("🎯 PORTFOLIO RISK CALCULATOR WITH ADVANCED LOOKUP")
        print("=" * 70)
        print("Enter your positions as: SYMBOL LOTS (e.g., AAPL 10)")
        print("Type 'done' when finished, 'help' for commands")
        print("Advanced commands: 'lookup SYMBOL', 'find PARTIAL', 'sector SECTOR_NAME'")
        print()

        positions = {}

        while True:
            try:
                user_input = input("💰 Enter position (SYMBOL LOTS): ").strip()

                if user_input.lower() == 'done':
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'symbols':
                    self._show_available_symbols()
                    continue
                elif user_input.lower() == 'clear':
                    positions.clear()
                    print("🗑️  Positions cleared")
                    continue
                elif user_input.lower().startswith('lookup '):
                    symbol = user_input[7:].strip().upper()
                    self._show_symbol_lookup(symbol)
                    continue
                elif user_input.lower().startswith('find '):
                    partial = user_input[5:].strip()
                    self._show_symbol_search(partial)
                    continue
                elif user_input.lower().startswith('sector '):
                    sector_name = user_input[7:].strip()
                    self._show_sector_analysis(sector_name)
                    continue

                parts = user_input.split()
                if len(parts) != 2:
                    print("❌ Invalid format. Use: SYMBOL LOTS")
                    continue

                symbol = parts[0].upper()
                lots = float(parts[1])

                if lots <= 0:
                    print("❌ Lots must be positive")
                    continue

                positions[symbol] = lots
                print(f"✅ Added {symbol}: {lots} lots")

            except ValueError:
                print("❌ Invalid lots number")
            except KeyboardInterrupt:
                print("\n👋 Calculator interrupted")
                return
            except Exception as e:
                print(f"❌ Error: {e}")

        if not positions:
            print("⚠️  No positions entered")
            return

        print(f"\n📋 PORTFOLIO SUMMARY: {len(positions)} positions")
        for symbol, lots in positions.items():
            print(f"  {symbol}: {lots} lots")

        # Run all three calculations
        print("\n" + "="*60)
        var_results = self.calculate_portfolio_var(positions)

        print("\n" + "="*60)
        atr_results = self.calculate_portfolio_atr(positions)

        print("\n" + "="*60)
        ev_results = self.calculate_portfolio_ev(positions)

        return {
            'positions': positions,
            'var': var_results,
            'atr': atr_results,
            'ev': ev_results
        }

    def _show_help(self):
        """Show help commands."""
        print("\n🔧 AVAILABLE COMMANDS:")
        print("  SYMBOL LOTS     - Add position (e.g., AAPL 10)")
        print("  lookup SYMBOL   - Detailed symbol analysis with outlier detection")
        print("  find PARTIAL    - Find symbols matching partial name")
        print("  sector SECTOR   - Analyze entire sector performance")
        print("  symbols         - Show available symbols")
        print("  clear          - Clear all positions")
        print("  help           - Show this help")
        print("  done           - Calculate portfolio metrics")
        print()

    def _show_symbol_lookup(self, symbol: str):
        """Show detailed symbol analysis."""
        result = self.lookup_tool.lookup_symbol(symbol)

        print(f"\n🔍 SYMBOL ANALYSIS: {symbol}")
        print("=" * 50)
        print(f"Found in datasets: {', '.join(result['found_in']) if result['found_in'] else 'None'}")
        print(f"Recommendation: {result['recommendation']}")

        if result['data']:
            for data_type, data in result['data'].items():
                outlier_status = "🚨 OUTLIER" if result['outlier_status'].get(data_type, False) else "✅ Normal"
                print(f"\n{data_type.upper()} Data ({outlier_status}):")
                if data_type == 'var':
                    print(f"  Price: ${data['ask_price']:.2f}")
                    print(f"  VaR (1 lot): ${data['var_1_lot']:.2f}")
                    print(f"  VaR Ratio: {data['var_to_ask_ratio']*100:.2f}%")
                elif data_type == 'atr':
                    print(f"  Price: ${data['ask_price']:.2f}")
                    print(f"  ATR D1: {data['atr_d1_ratio']*100:.2f}%")
                    print(f"  ATR W1: {data['atr_w1_ratio']*100:.2f}%")
                    print(f"  ATR MN1: {data['atr_mn1_ratio']*100:.2f}%")
                elif data_type == 'ev':
                    print(f"  Price: ${data['ask_price']:.2f}")
                    print(f"  Market Cap: ${data['market_cap']/1e9:.1f}B")
                    print(f"  Enterprise Value: ${data['enterprise_value']/1e9:.1f}B")
                    print(f"  MCap/EV Ratio: {data['mcap_ev_ratio']:.1f}%")

                print(f"  Industry: {data.get('industry', 'Unknown')}")
                print(f"  Sector: {data.get('sector', 'Unknown')}")
        print()

    def _show_symbol_search(self, partial: str):
        """Show symbols matching partial input."""
        matches = self.lookup_tool.find_similar_symbols(partial)

        print(f"\n🔍 SYMBOLS MATCHING '{partial.upper()}':")
        print("=" * 40)
        if matches:
            for i, symbol in enumerate(matches, 1):
                # Quick lookup to show recommendation
                result = self.lookup_tool.lookup_symbol(symbol)
                status = "🚨" if any(result['outlier_status'].values()) else "✅"
                print(f"  {i:2}. {symbol:8} {status} - {result['recommendation']}")
        else:
            print(f"  No symbols found matching '{partial}'")
        print()

    def _show_sector_analysis(self, sector: str):
        """Show sector analysis."""
        analysis = self.lookup_tool.get_sector_analysis(sector)

        if 'error' in analysis:
            print(f"\n❌ {analysis['error']}")
            return

        print(f"\n📊 SECTOR ANALYSIS: {sector.upper()}")
        print("=" * 50)
        print(f"Total symbols: {analysis['symbol_count']}")
        print(f"Average VaR ratio: {analysis['avg_var_ratio']*100:.2f}%")
        print(f"Average ATR ratio: {analysis['avg_atr_ratio']*100:.2f}%")
        print(f"Outlier symbols: {analysis['outlier_count']}")

        print(f"\nTop 5 symbols in {sector}:")
        for i, symbol in enumerate(analysis['symbols'][:5], 1):
            data = analysis['data'][symbol]
            status = "🚨" if any(data['outlier_status'].values()) else "✅"
            print(f"  {i}. {symbol:8} {status} - {data['recommendation']}")

        if len(analysis['symbols']) > 5:
            print(f"  ... and {len(analysis['symbols']) - 5} more symbols")
        print()

    def _show_available_symbols(self):
        """Show sample of available symbols."""
        symbols = self.get_available_symbols()

        print("\n📊 AVAILABLE SYMBOLS (sample):")
        for data_type, symbol_list in symbols.items():
            if symbol_list:
                sample = symbol_list[:10]  # Show first 10
                print(f"  {data_type.upper()}: {', '.join(sample)}")
                if len(symbol_list) > 10:
                    print(f"       ... and {len(symbol_list) - 10} more")
        print()

def demo_portfolio():
    """Demo with your current holdings."""
    calculator = PortfolioCalculator()

    if not any([calculator.var_data, calculator.atr_data, calculator.ev_data]):
        print("❌ No data files found. Make sure CSV files exist in var-explorer/, atr-explorer/, and ev-explorer/ directories.")
        return

    print(f"✅ Loaded {len(calculator.var_data)} VaR symbols")
    print(f"✅ Loaded {len(calculator.atr_data)} ATR symbols")
    print(f"✅ Loaded {len(calculator.ev_data)} EV symbols")

    # Demo with your current holdings
    demo_positions = {
        'IRDM': 100,  # 100 lots
        'CC': 150,    # 150 lots
        'SRPT': 50,   # 50 lots
        'BILL': 75    # 75 lots
    }

    print(f"\n📋 DEMO PORTFOLIO: Your Current Holdings")
    for symbol, lots in demo_positions.items():
        print(f"  {symbol}: {lots} lots")

    # Run all three calculations
    print("\n" + "="*60)
    var_results = calculator.calculate_portfolio_var(demo_positions)

    print("\n" + "="*60)
    atr_results = calculator.calculate_portfolio_atr(demo_positions)

    print("\n" + "="*60)
    ev_results = calculator.calculate_portfolio_ev(demo_positions)

    return {
        'positions': demo_positions,
        'var': var_results,
        'atr': atr_results,
        'ev': ev_results
    }

def main():
    """Main function to run the portfolio calculator."""
    import sys

    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'demo':
            demo_portfolio()
        else:
            calculator = PortfolioCalculator()

            if not any([calculator.var_data, calculator.atr_data, calculator.ev_data]):
                print("❌ No data files found. Make sure CSV files exist in var-explorer/, atr-explorer/, and ev-explorer/ directories.")
                return

            print(f"✅ Loaded {len(calculator.var_data)} VaR symbols")
            print(f"✅ Loaded {len(calculator.atr_data)} ATR symbols")
            print(f"✅ Loaded {len(calculator.ev_data)} EV symbols")

            calculator.interactive_calculator()

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"💥 Fatal error: {e}")

if __name__ == "__main__":
    main()