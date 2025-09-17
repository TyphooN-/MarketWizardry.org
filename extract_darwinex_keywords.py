#!/usr/bin/env python3
"""
Extract all sectors, industries, and symbols from Darwinex CSV exports
to build comprehensive sector detection for the blog generator
"""

import pandas as pd
import glob
import os

# Find all Darwinex CSV files
csv_pattern = "*/SymbolsExport-Darwinex-Live-*.csv"
csv_files = glob.glob(csv_pattern)

all_symbols = set()
all_sectors = set() 
all_industries = set()

print(f"Found {len(csv_files)} Darwinex CSV files")

for csv_file in csv_files:
    print(f"Processing: {csv_file}")
    try:
        df = pd.read_csv(csv_file, delimiter=';')
        
        # Extract symbols
        if 'Symbol' in df.columns:
            symbols = df['Symbol'].dropna().unique()
            all_symbols.update(symbols)
        
        # Extract sectors  
        if 'SectorName' in df.columns:
            sectors = df['SectorName'].dropna().unique()
            all_sectors.update(sectors)
            
        # Extract industries
        if 'IndustryName' in df.columns:
            industries = df['IndustryName'].dropna().unique()
            all_industries.update(industries)
            
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")

print(f"\nExtracted:")
print(f"- {len(all_symbols)} unique symbols")
print(f"- {len(all_sectors)} unique sectors") 
print(f"- {len(all_industries)} unique industries")

# Group sectors and map to our existing categories
sector_mapping = {
    'biotech': ['Healthcare'],
    'tech': ['Technology'],
    'semiconductor': ['Technology'],  # Will be handled by industry keywords
    'energy': ['Energy'], 
    'finance': ['Financial'],
    'healthcare': ['Healthcare'],
    'retail': ['Consumer Cyclical', 'Consumer Defensive'],
    'automotive': [],  # Handle by symbol/industry
    'real_estate': ['Real Estate'],
    'telecom': ['Communication Services'],
    'industrials': ['Industrials']
}

# Create industry-specific mappings
industry_keywords = {
    'biotech': ['Biotechnology', 'Drugs Manufacturers', 'Medical Devices'],
    'semiconductor': ['Semiconductors', 'Semiconductor Equipment & Materials'],
    'energy': ['Oil & Gas', 'Solar', 'Utilities'],
    'finance': ['Banks', 'Insurance', 'Credit Services', 'Assets Management', 'Financial Data & Stock Exchanges'],
    'automotive': ['Auto Manufacturers', 'Auto Parts', 'Recreational Vehicles'],
    'real_estate': ['Real Estate', 'REITs']
}

print("\n=== SECTORS ===")
for sector in sorted(all_sectors):
    print(f"'{sector}'")

print("\n=== INDUSTRIES (first 50) ===") 
for industry in sorted(list(all_industries))[:50]:
    print(f"'{industry}'")

print("\n=== MAJOR STOCK SYMBOLS (first 100) ===")
for symbol in sorted(list(all_symbols))[:100]:
    print(f"'{symbol}'")

# Generate keyword lists for the blog script
print("\n=== SUGGESTED KEYWORD UPDATES ===")

print("\n# Finance symbols:")
finance_symbols = [s for s in all_symbols if s in ['C', 'JPM', 'BAC', 'WFC', 'GS', 'MS', 'BLK', 'ARCC', 'CME', 'CINF', 'CACC']]
print(f"Finance symbols: {sorted(finance_symbols)}")

print("\n# Tech symbols:")  
tech_symbols = [s for s in all_symbols if s in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'ADBE', 'CRM', 'ORCL', 'CRWD']]
print(f"Tech symbols: {sorted(tech_symbols)}")

print("\n# Biotech symbols:")
biotech_symbols = [s for s in all_symbols if s in ['SRPT', 'BIIB', 'GILD', 'AMGN', 'BMRN', 'ALNY', 'ARWR', 'APLS']]
print(f"Biotech symbols: {sorted(biotech_symbols)}")

print("\nAll unique sectors found:")
for sector in sorted(all_sectors):
    print(f"  - {sector}")
    
print("\nFinance-related industries:")
finance_industries = [i for i in all_industries if any(word in i.lower() for word in ['bank', 'finance', 'credit', 'insurance', 'asset', 'exchange'])]
for industry in sorted(finance_industries):
    print(f"  - {industry}")