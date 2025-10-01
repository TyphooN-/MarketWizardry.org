#!/usr/bin/env python3
"""
Enhanced crypto analysis that combines Darwinex trading data with CoinGecko market data.
Provides comprehensive analysis including volatility, market cap, supply metrics, and more.
"""

import pandas as pd
import numpy as np
import json
import argparse
from datetime import datetime
from pathlib import Path

# Forex pairs to exclude
FOREX_PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'NZDUSD', 'USDCAD',
               'EURGBP', 'EURJPY', 'GBPJPY', 'EURCHF', 'AUDJPY', 'EURAUD', 'GBPAUD',
               'GBPCAD', 'GBPCHF', 'AUDCAD', 'AUDCHF', 'AUDNZD', 'NZDCHF', 'NZDJPY',
               'NZDCAD', 'CADJPY', 'CADCHF', 'CHFJPY', 'EURNZD', 'EURCAD']


def load_crypto_market_data(json_file: str) -> dict:
    """Load cryptocurrency market data from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {json_file} not found. Run fetch_crypto_data.py first.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {json_file}")
        return {}


def merge_data(df: pd.DataFrame, market_data: dict) -> pd.DataFrame:
    """Merge Darwinex CSV data with CoinGecko market data."""
    # Add market data columns
    df['MarketCap'] = None
    df['MarketCapRank'] = None
    df['Volume24h'] = None
    df['CirculatingSupply'] = None
    df['MaxSupply'] = None
    df['PercentMinted'] = None
    df['PriceChange24h%'] = None
    df['PriceChange7d%'] = None
    df['PriceChange30d%'] = None
    df['PriceChange1y%'] = None
    df['ATH'] = None
    df['ATHChange%'] = None
    df['FDV'] = None
    df['MCap/FDV'] = None
    df['LiquidityScore'] = None

    for idx, row in df.iterrows():
        symbol = row['Symbol']
        if symbol in market_data:
            md = market_data[symbol]
            df.at[idx, 'MarketCap'] = md.get('market_cap_usd')
            df.at[idx, 'MarketCapRank'] = md.get('market_cap_rank')
            df.at[idx, 'Volume24h'] = md.get('total_volume_24h')
            df.at[idx, 'CirculatingSupply'] = md.get('circulating_supply')
            df.at[idx, 'MaxSupply'] = md.get('max_supply')
            df.at[idx, 'PercentMinted'] = md.get('percent_minted')
            df.at[idx, 'PriceChange24h%'] = md.get('price_change_24h_percent')
            df.at[idx, 'PriceChange7d%'] = md.get('price_change_7d_percent')
            df.at[idx, 'PriceChange30d%'] = md.get('price_change_30d_percent')
            df.at[idx, 'PriceChange1y%'] = md.get('price_change_1y_percent')
            df.at[idx, 'ATH'] = md.get('ath_usd')
            df.at[idx, 'ATHChange%'] = md.get('ath_change_percent')
            df.at[idx, 'FDV'] = md.get('fully_diluted_valuation')
            df.at[idx, 'MCap/FDV'] = md.get('market_cap_to_fdv_ratio')
            df.at[idx, 'LiquidityScore'] = md.get('liquidity_score')

    return df


def format_large_number(num):
    """Format large numbers with B/M/K suffixes."""
    if pd.isna(num) or num is None:
        return "N/A"
    if num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    elif num >= 1e3:
        return f"${num/1e3:.2f}K"
    else:
        return f"${num:.2f}"


def format_supply(num):
    """Format supply numbers."""
    if pd.isna(num) or num is None:
        return "N/A"
    if num >= 1e9:
        return f"{num/1e9:.2f}B"
    elif num >= 1e6:
        return f"{num/1e6:.2f}M"
    elif num >= 1e3:
        return f"{num/1e3:.2f}K"
    else:
        return f"{num:.2f}"


def format_price(price):
    """Format price with appropriate precision based on magnitude."""
    if pd.isna(price) or price is None:
        return "N/A"
    if price >= 1000:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.4f}"
    elif price >= 0.01:
        return f"${price:.4f}"
    elif price >= 0.0001:
        return f"${price:.6f}"
    else:
        return f"${price:.8f}"


def format_percentage(ratio):
    """Format ratio as percentage."""
    if pd.isna(ratio) or ratio is None:
        return "N/A"
    return f"{ratio*100:.2f}%"


def analyze_crypto_enhanced(csv_file: str, market_data_file: str = None):
    """
    Enhanced cryptocurrency analysis with market data.
    """
    try:
        print(f"Enhanced Crypto Market Analysis")
        print(f"Report generated on: {datetime.now()}")
        print()

        # Load CSV data
        df = pd.read_csv(csv_file, delimiter=';', encoding='latin1')

        # Filter out forex pairs
        df = df[~df['Symbol'].isin(FOREX_PAIRS)].copy()

        # Load market data if available
        market_data = {}
        if market_data_file:
            market_data = load_crypto_market_data(market_data_file)
            if market_data:
                print(f"Loaded market data for {len(market_data)} cryptocurrencies")
                df = merge_data(df, market_data)

        # Convert numeric columns
        numeric_cols = ['AskPrice', 'BidPrice', 'Spread', 'ATR_D1', 'ATR_W1', 'ATR_MN1',
                       'VaR_1_Lot', 'RelativeSpread_%']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Calculate ATR ratios
        for atr_col in ['ATR_D1', 'ATR_W1', 'ATR_MN1']:
            ratio_col = f'{atr_col}/AskPrice'
            if ratio_col not in df.columns and atr_col in df.columns:
                df[ratio_col] = df[atr_col] / df['AskPrice']

        # Calculate VaR to Ask ratio
        if 'VaR_to_Ask_Ratio' not in df.columns and 'VaR_1_Lot' in df.columns:
            df['VaR_to_Ask_Ratio'] = df['VaR_1_Lot'] / df['AskPrice']

        print(f"{'='*80}")
        print(f"CRYPTO MARKET OVERVIEW")
        print(f"{'='*80}")
        print(f"Total Pairs Analyzed: {len(df)}")
        print(f"Symbols: {', '.join(df['Symbol'].tolist())}")
        print()

        # Market Cap Rankings (if available)
        if 'MarketCap' in df.columns and df['MarketCap'].notna().any():
            print(f"{'='*80}")
            print(f"MARKET CAP RANKINGS")
            print(f"{'='*80}")
            df_mc = df[df['MarketCap'].notna()].sort_values('MarketCap', ascending=False)
            print(f"{'Rank':<6} {'Symbol':<12} {'Name':<20} {'Market Cap':<15} {'MCap Rank':<12} {'Volume 24h':<15}")
            print("-" * 80)
            for idx, (i, row) in enumerate(df_mc.iterrows(), 1):
                mc_rank = int(row['MarketCapRank']) if pd.notna(row['MarketCapRank']) else 'N/A'
                print(f"{idx:<6} {row['Symbol']:<12} "
                      f"{format_large_number(row['MarketCap']):<15} "
                      f"{mc_rank:<12} "
                      f"{format_large_number(row['Volume24h']):<15}")
            print()

        # Supply Metrics (if available)
        if 'PercentMinted' in df.columns and df['PercentMinted'].notna().any():
            print(f"{'='*80}")
            print(f"SUPPLY METRICS & EMISSION STATUS")
            print(f"{'='*80}")
            df_supply = df[df['PercentMinted'].notna()].sort_values('PercentMinted', ascending=False)
            print(f"{'Symbol':<12} {'% Minted':<12} {'Circulating':<18} {'Max Supply':<18} {'Status':<20}")
            print("-" * 80)
            for i, row in df_supply.iterrows():
                pct = row['PercentMinted']
                status = "Near Max" if pct > 95 else "High" if pct > 80 else "Moderate" if pct > 50 else "Early"
                print(f"{row['Symbol']:<12} "
                      f"{pct:>10.2f}%  "
                      f"{format_supply(row['CirculatingSupply']):<18} "
                      f"{format_supply(row['MaxSupply']):<18} "
                      f"{status:<20}")
            print()

        # Volatility Rankings - Daily
        print(f"{'='*80}")
        print(f"DAILY VOLATILITY RANKING (ATR_D1/Price)")
        print(f"{'='*80}")
        df_sorted = df.sort_values('ATR_D1/AskPrice', ascending=False)
        print(f"{'Rank':<6} {'Symbol':<12} {'Volatility':<15} {'Daily ATR':<18} {'Price':<18}")
        print("-" * 80)
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            print(f"{idx:<6} {row['Symbol']:<12} "
                  f"{format_percentage(row['ATR_D1/AskPrice']):<15} "
                  f"{format_price(row['ATR_D1']):<18} "
                  f"{format_price(row['AskPrice']):<18}")
        print()

        # Volatility Rankings - Weekly
        print(f"{'='*80}")
        print(f"WEEKLY VOLATILITY RANKING (ATR_W1/Price)")
        print(f"{'='*80}")
        df_sorted = df.sort_values('ATR_W1/AskPrice', ascending=False)
        print(f"{'Rank':<6} {'Symbol':<12} {'Volatility':<15} {'Weekly ATR':<18} {'Price':<18}")
        print("-" * 80)
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            print(f"{idx:<6} {row['Symbol']:<12} "
                  f"{format_percentage(row['ATR_W1/AskPrice']):<15} "
                  f"{format_price(row['ATR_W1']):<18} "
                  f"{format_price(row['AskPrice']):<18}")
        print()

        # Volatility Rankings - Monthly
        if 'ATR_MN1/AskPrice' in df.columns and df['ATR_MN1/AskPrice'].notna().any():
            print(f"{'='*80}")
            print(f"MONTHLY VOLATILITY RANKING (ATR_MN1/Price)")
            print(f"{'='*80}")
            df_sorted = df.sort_values('ATR_MN1/AskPrice', ascending=False)
            print(f"{'Rank':<6} {'Symbol':<12} {'Volatility':<15} {'Monthly ATR':<18} {'Price':<18}")
            print("-" * 80)
            for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
                print(f"{idx:<6} {row['Symbol']:<12} "
                      f"{format_percentage(row['ATR_MN1/AskPrice']):<15} "
                      f"{format_price(row['ATR_MN1']):<18} "
                      f"{format_price(row['AskPrice']):<18}")
            print()

        # Price Performance (if available)
        if 'PriceChange24h%' in df.columns and df['PriceChange24h%'].notna().any():
            print(f"{'='*80}")
            print(f"PRICE PERFORMANCE")
            print(f"{'='*80}")
            df_perf = df[df['PriceChange24h%'].notna()].copy()
            print(f"{'Symbol':<12} {'Price':<18} {'24h':<10} {'7d':<10} {'30d':<10} {'1y':<10} {'ATH':<15} {'From ATH':<12}")
            print("-" * 80)
            for i, row in df_perf.iterrows():
                price = format_price(row['AskPrice'])
                change_24h = f"{row['PriceChange24h%']:+.2f}%" if pd.notna(row['PriceChange24h%']) else "N/A"
                change_7d = f"{row['PriceChange7d%']:+.2f}%" if pd.notna(row['PriceChange7d%']) else "N/A"
                change_30d = f"{row['PriceChange30d%']:+.2f}%" if pd.notna(row['PriceChange30d%']) else "N/A"
                change_1y = f"{row['PriceChange1y%']:+.2f}%" if pd.notna(row['PriceChange1y%']) else "N/A"
                ath = format_large_number(row['ATH']) if pd.notna(row['ATH']) else "N/A"
                ath_change = f"{row['ATHChange%']:+.2f}%" if pd.notna(row['ATHChange%']) else "N/A"
                print(f"{row['Symbol']:<12} {price:<18} {change_24h:<10} {change_7d:<10} {change_30d:<10} {change_1y:<10} {ath:<15} {ath_change:<12}")
            print()

        # Liquidity & Trading Metrics
        if 'LiquidityScore' in df.columns and df['LiquidityScore'].notna().any():
            print(f"{'='*80}")
            print(f"LIQUIDITY & TRADING METRICS")
            print(f"{'='*80}")
            df_liq = df[df['LiquidityScore'].notna()].sort_values('LiquidityScore', ascending=False)
            print(f"{'Symbol':<12} {'Liquidity':<12} {'Volume/MCap':<15} {'Spread %':<12}")
            print("-" * 80)
            for i, row in df_liq.iterrows():
                vol_to_mc = (row['Volume24h'] / row['MarketCap'] * 100) if pd.notna(row['Volume24h']) and pd.notna(row['MarketCap']) else None
                vol_mc_str = f"{vol_to_mc:.2f}%" if vol_to_mc else "N/A"
                spread = f"{row['RelativeSpread_%']:.3f}%" if pd.notna(row.get('RelativeSpread_%')) else "N/A"
                print(f"{row['Symbol']:<12} {row['LiquidityScore']:<12.2f} {vol_mc_str:<15} {spread:<12}")
            print()

        # VaR Rankings
        print(f"{'='*80}")
        print(f"VALUE AT RISK RANKING (VaR/Price)")
        print(f"{'='*80}")
        df_sorted = df.sort_values('VaR_to_Ask_Ratio', ascending=False)
        print(f"{'Rank':<6} {'Symbol':<12} {'Risk Ratio':<15} {'VaR (1 Lot)':<18} {'Price':<18}")
        print("-" * 80)
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            print(f"{idx:<6} {row['Symbol']:<12} "
                  f"{format_percentage(row['VaR_to_Ask_Ratio']):<15} "
                  f"{format_price(row['VaR_1_Lot']):<18} "
                  f"{format_price(row['AskPrice']):<18}")
        print()

        # Summary Statistics
        print(f"{'='*80}")
        print(f"SUMMARY STATISTICS")
        print(f"{'='*80}")
        print(f"Average Daily Volatility (ATR/Price): {df['ATR_D1/AskPrice'].mean():.4f} ({df['ATR_D1/AskPrice'].mean()*100:.2f}%)")
        print(f"Average Weekly Volatility (ATR/Price): {df['ATR_W1/AskPrice'].mean():.4f} ({df['ATR_W1/AskPrice'].mean()*100:.2f}%)")
        if 'ATR_MN1/AskPrice' in df.columns:
            print(f"Average Monthly Volatility (ATR/Price): {df['ATR_MN1/AskPrice'].mean():.4f} ({df['ATR_MN1/AskPrice'].mean()*100:.2f}%)")
        print(f"Average VaR/Price Ratio: {df['VaR_to_Ask_Ratio'].mean():.4f} ({df['VaR_to_Ask_Ratio'].mean()*100:.2f}%)")

        if 'MarketCap' in df.columns and df['MarketCap'].notna().any():
            total_mc = df['MarketCap'].sum()
            print(f"Total Market Cap (tracked): {format_large_number(total_mc)}")

        print()

        # Key Insights
        print(f"{'='*80}")
        print(f"KEY INSIGHTS")
        print(f"{'='*80}")

        most_volatile = df.loc[df['ATR_D1/AskPrice'].idxmax()]
        least_volatile = df.loc[df['ATR_D1/AskPrice'].idxmin()]
        print(f"Most Volatile (Daily): {most_volatile['Symbol']} ({most_volatile['ATR_D1/AskPrice']*100:.2f}%)")
        print(f"Least Volatile (Daily): {least_volatile['Symbol']} ({least_volatile['ATR_D1/AskPrice']*100:.2f}%)")

        if 'PercentMinted' in df.columns and df['PercentMinted'].notna().any():
            most_minted = df.loc[df['PercentMinted'].idxmax()]
            least_minted = df.loc[df['PercentMinted'].idxmin()]
            print(f"\nMost Minted: {most_minted['Symbol']} ({most_minted['PercentMinted']:.2f}%) - Limited supply growth")
            print(f"Least Minted: {least_minted['Symbol']} ({least_minted['PercentMinted']:.2f}%) - Significant inflation ahead")

        if 'PriceChange24h%' in df.columns and df['PriceChange24h%'].notna().any():
            best_24h = df.loc[df['PriceChange24h%'].idxmax()]
            worst_24h = df.loc[df['PriceChange24h%'].idxmin()]
            print(f"\nBest 24h Performance: {best_24h['Symbol']} ({best_24h['PriceChange24h%']:+.2f}%)")
            print(f"Worst 24h Performance: {worst_24h['Symbol']} ({worst_24h['PriceChange24h%']:+.2f}%)")

        print()

    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enhanced cryptocurrency market analysis.')
    parser.add_argument('csv_file', type=str, help='Path to the Darwinex CSV file')
    parser.add_argument(
        '--market-data',
        type=str,
        default='crypto_market_data.json',
        help='Path to CoinGecko market data JSON file (default: crypto_market_data.json)'
    )

    args = parser.parse_args()

    # Check if market data file exists
    market_data_file = args.market_data if Path(args.market_data).exists() else None
    if not market_data_file:
        print(f"Warning: Market data file '{args.market_data}' not found.")
        print("Run 'python fetch_crypto_data.py' first to fetch market data.")
        print("Proceeding with basic analysis only...\n")

    analyze_crypto_enhanced(args.csv_file, market_data_file)
