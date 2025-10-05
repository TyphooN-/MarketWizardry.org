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


def load_crypto_news_data(json_file: str) -> dict:
    """Load cryptocurrency news data from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('news', {})
    except FileNotFoundError:
        print(f"Warning: {json_file} not found. Run fetch_crypto_news.py first.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {json_file}")
        return {}


def load_crypto_events_data(json_file: str) -> dict:
    """Load cryptocurrency events data from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('events', {})
    except FileNotFoundError:
        print(f"Warning: {json_file} not found. Run fetch_crypto_events.py first.")
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


def print_separator(char="═", width=120):
    """
    Print a separator line.

    Args:
        char: Character to use for separator (default: ═)
        width: Width of separator (default: 120 for better readability)
    """
    print(f"{char * width}")


def print_table_separator(char="─", width=120):
    """Print a table separator line."""
    print(f"{char * width}")


def analyze_crypto_enhanced(csv_file: str, market_data_file: str = None, news_data_file: str = None, events_data_file: str = None):
    """
    Enhanced cryptocurrency analysis with market data, news, and upcoming events.
    """
    try:
        print_separator()
        print(f"ENHANCED CRYPTO MARKET ANALYSIS")
        print_separator()
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
                print(f"✓ Loaded market data for {len(market_data)} cryptocurrencies")
                df = merge_data(df, market_data)

        # Load news data if available
        news_data = {}
        if news_data_file:
            all_news_data = load_crypto_news_data(news_data_file)
            # Filter news to only include symbols in our CSV
            news_data = {symbol: all_news_data[symbol] for symbol in df['Symbol'].tolist() if symbol in all_news_data}
            if news_data:
                print(f"✓ Loaded news for {len(news_data)} cryptocurrencies")

        # Load events data if available
        events_data = {}
        if events_data_file:
            all_events_data = load_crypto_events_data(events_data_file)
            # Filter events to only include symbols in our CSV
            events_data = {symbol: all_events_data[symbol] for symbol in df['Symbol'].tolist() if symbol in all_events_data}
            if events_data:
                print(f"✓ Loaded events for {len(events_data)} cryptocurrencies")

        print()

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

        print_separator()
        print(f"CRYPTO MARKET OVERVIEW")
        print_separator()
        print(f"Total Pairs Analyzed: {len(df)}")
        print(f"Symbols: {', '.join(df['Symbol'].tolist())}")
        print()

        # Market Cap Rankings (if available)
        if 'MarketCap' in df.columns and df['MarketCap'].notna().any():
            print_separator()
            print(f"💰 MARKET CAP RANKINGS")
            print_separator()
            df_mc = df[df['MarketCap'].notna()].sort_values('MarketCap', ascending=False)
            print(f"{'#':<4} {'Symbol':<10} {'Market Cap':<16} {'Global Rank':<13} {'24h Volume':<16}")
            print_table_separator()
            for idx, (i, row) in enumerate(df_mc.iterrows(), 1):
                mc_rank = f"#{int(row['MarketCapRank'])}" if pd.notna(row['MarketCapRank']) else 'N/A'
                print(f"{idx:<4} {row['Symbol']:<10} "
                      f"{format_large_number(row['MarketCap']):<16} "
                      f"{mc_rank:<13} "
                      f"{format_large_number(row['Volume24h']):<16}")
            print()

        # Supply Metrics (if available)
        if 'PercentMinted' in df.columns and df['PercentMinted'].notna().any():
            print_separator()
            print(f"🪙 SUPPLY METRICS & EMISSION STATUS")
            print_separator()
            df_supply = df[df['PercentMinted'].notna()].sort_values('PercentMinted', ascending=False)
            print(f"{'Symbol':<10} {'% Minted':<12} {'Circulating':<16} {'Max Supply':<16} {'Status':<20}")
            print_table_separator()
            for i, row in df_supply.iterrows():
                pct = row['PercentMinted']
                status_emoji = "🔴" if pct > 95 else "🟡" if pct > 80 else "🟢" if pct > 50 else "🔵"
                status = "Near Max" if pct > 95 else "High Emission" if pct > 80 else "Moderate" if pct > 50 else "Early Stage"
                print(f"{row['Symbol']:<10} "
                      f"{pct:>10.2f}%  "
                      f"{format_supply(row['CirculatingSupply']):<16} "
                      f"{format_supply(row['MaxSupply']):<16} "
                      f"{status_emoji} {status:<18}")
            print()

        # Volatility Rankings - Daily
        print_separator()
        print(f"📊 DAILY VOLATILITY RANKING (ATR/Price)")
        print_separator()
        df_sorted = df.sort_values('ATR_D1/AskPrice', ascending=False)
        print(f"{'#':<4} {'Symbol':<10} {'Volatility':<13} {'Daily ATR':<16} {'Current Price':<16}")
        print_table_separator()
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            vol_pct = row['ATR_D1/AskPrice'] * 100
            vol_indicator = "🔥" if vol_pct > 6 else "⚡" if vol_pct > 4 else "📈"
            print(f"{idx:<4} {row['Symbol']:<10} "
                  f"{vol_indicator} {format_percentage(row['ATR_D1/AskPrice']):<10} "
                  f"{format_price(row['ATR_D1']):<16} "
                  f"{format_price(row['AskPrice']):<16}")
        print()

        # Volatility Rankings - Weekly
        print_separator()
        print(f"📊 WEEKLY VOLATILITY RANKING (ATR/Price)")
        print_separator()
        df_sorted = df.sort_values('ATR_W1/AskPrice', ascending=False)
        print(f"{'#':<4} {'Symbol':<10} {'Volatility':<13} {'Weekly ATR':<16} {'Current Price':<16}")
        print_table_separator()
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            vol_pct = row['ATR_W1/AskPrice'] * 100
            vol_indicator = "🔥" if vol_pct > 15 else "⚡" if vol_pct > 10 else "📈"
            print(f"{idx:<4} {row['Symbol']:<10} "
                  f"{vol_indicator} {format_percentage(row['ATR_W1/AskPrice']):<10} "
                  f"{format_price(row['ATR_W1']):<16} "
                  f"{format_price(row['AskPrice']):<16}")
        print()

        # Volatility Rankings - Monthly
        if 'ATR_MN1/AskPrice' in df.columns and df['ATR_MN1/AskPrice'].notna().any():
            print_separator()
            print(f"📊 MONTHLY VOLATILITY RANKING (ATR/Price)")
            print_separator()
            df_sorted = df.sort_values('ATR_MN1/AskPrice', ascending=False)
            print(f"{'#':<4} {'Symbol':<10} {'Volatility':<13} {'Monthly ATR':<16} {'Current Price':<16}")
            print_table_separator()
            for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
                vol_pct = row['ATR_MN1/AskPrice'] * 100
                vol_indicator = "🔥" if vol_pct > 30 else "⚡" if vol_pct > 20 else "📈"
                print(f"{idx:<4} {row['Symbol']:<10} "
                      f"{vol_indicator} {format_percentage(row['ATR_MN1/AskPrice']):<10} "
                      f"{format_price(row['ATR_MN1']):<16} "
                      f"{format_price(row['AskPrice']):<16}")
            print()

        # Price Performance (if available)
        if 'PriceChange24h%' in df.columns and df['PriceChange24h%'].notna().any():
            print_separator()
            print(f"📈 PRICE PERFORMANCE")
            print_separator()
            df_perf = df[df['PriceChange24h%'].notna()].copy()
            print(f"{'Symbol':<10} {'Price':<16} {'24h %':<11} {'7d %':<11} {'30d %':<11} {'1y %':<11} {'ATH':<14} {'vs ATH':<11}")
            print_table_separator()
            for i, row in df_perf.iterrows():
                price = format_price(row['AskPrice'])

                # Format with rocket/nuke indicators
                def format_change(val):
                    if pd.isna(val):
                        return "N/A       "
                    emoji = "🚀" if val > 0 else "☢️" if val < 0 else "⚪"
                    return f"{emoji}{val:+.1f}%"

                change_24h = format_change(row['PriceChange24h%'])
                change_7d = format_change(row['PriceChange7d%'])
                change_30d = format_change(row['PriceChange30d%'])
                change_1y = format_change(row['PriceChange1y%'])
                ath = format_price(row['ATH']) if pd.notna(row['ATH']) else "N/A"
                ath_change = format_change(row['ATHChange%'])

                print(f"{row['Symbol']:<10} {price:<16} {change_24h:<11} {change_7d:<11} {change_30d:<11} {change_1y:<11} {ath:<14} {ath_change:<11}")
            print()

        # Liquidity & Trading Metrics
        if 'LiquidityScore' in df.columns and df['LiquidityScore'].notna().any():
            print_separator()
            print(f"💧 LIQUIDITY & TRADING METRICS")
            print_separator()
            df_liq = df[df['LiquidityScore'].notna()].sort_values('LiquidityScore', ascending=False)
            print(f"{'Symbol':<10} {'Liquidity':<13} {'Vol/MCap %':<13} {'Spread %':<12}")
            print_table_separator()
            for i, row in df_liq.iterrows():
                vol_to_mc = (row['Volume24h'] / row['MarketCap'] * 100) if pd.notna(row['Volume24h']) and pd.notna(row['MarketCap']) else None
                vol_mc_str = f"{vol_to_mc:.2f}%" if vol_to_mc else "N/A"
                spread = f"{row['RelativeSpread_%']:.4f}%" if pd.notna(row.get('RelativeSpread_%')) else "N/A"
                liq_score = row['LiquidityScore']
                liq_indicator = "🟢" if liq_score > 7 else "🟡" if liq_score > 5 else "🔴"
                print(f"{row['Symbol']:<10} {liq_indicator} {liq_score:<10.1f} {vol_mc_str:<13} {spread:<12}")
            print()

        # VaR Rankings
        print_separator()
        print(f"⚠️  VALUE AT RISK RANKING (VaR/Price)")
        print_separator()
        df_sorted = df.sort_values('VaR_to_Ask_Ratio', ascending=False)
        print(f"{'#':<4} {'Symbol':<10} {'Risk Ratio':<13} {'VaR (1 Lot)':<16} {'Current Price':<16}")
        print_table_separator()
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            risk_pct = row['VaR_to_Ask_Ratio'] * 100
            risk_indicator = "🔴" if risk_pct > 7 else "🟡" if risk_pct > 5 else "🟢"
            print(f"{idx:<4} {row['Symbol']:<10} "
                  f"{risk_indicator} {format_percentage(row['VaR_to_Ask_Ratio']):<10} "
                  f"{format_price(row['VaR_1_Lot']):<16} "
                  f"{format_price(row['AskPrice']):<16}")
        print()

        # Summary Statistics
        print_separator()
        print(f"📊 SUMMARY STATISTICS")
        print_separator()
        print(f"Average Daily Volatility:   {df['ATR_D1/AskPrice'].mean()*100:>6.2f}%")
        print(f"Average Weekly Volatility:  {df['ATR_W1/AskPrice'].mean()*100:>6.2f}%")
        if 'ATR_MN1/AskPrice' in df.columns:
            print(f"Average Monthly Volatility: {df['ATR_MN1/AskPrice'].mean()*100:>6.2f}%")
        print(f"Average VaR/Price Ratio:    {df['VaR_to_Ask_Ratio'].mean()*100:>6.2f}%")

        if 'MarketCap' in df.columns and df['MarketCap'].notna().any():
            total_mc = df['MarketCap'].sum()
            print(f"Total Market Cap (tracked): {format_large_number(total_mc)}")

        print()

        # Key Insights
        print_separator()
        print(f"💡 KEY INSIGHTS")
        print_separator()

        most_volatile_d1 = df.loc[df['ATR_D1/AskPrice'].idxmax()]
        least_volatile_d1 = df.loc[df['ATR_D1/AskPrice'].idxmin()]
        print(f"🔥 Most Volatile (Daily):   {most_volatile_d1['Symbol']:<8} {most_volatile_d1['ATR_D1/AskPrice']*100:>6.2f}%")
        print(f"📉 Least Volatile (Daily):  {least_volatile_d1['Symbol']:<8} {least_volatile_d1['ATR_D1/AskPrice']*100:>6.2f}%")

        most_volatile_w1 = df.loc[df['ATR_W1/AskPrice'].idxmax()]
        least_volatile_w1 = df.loc[df['ATR_W1/AskPrice'].idxmin()]
        print(f"\n🔥 Most Volatile (Weekly):  {most_volatile_w1['Symbol']:<8} {most_volatile_w1['ATR_W1/AskPrice']*100:>6.2f}%")
        print(f"📉 Least Volatile (Weekly): {least_volatile_w1['Symbol']:<8} {least_volatile_w1['ATR_W1/AskPrice']*100:>6.2f}%")

        if 'ATR_MN1/AskPrice' in df.columns and df['ATR_MN1/AskPrice'].notna().any():
            most_volatile_mn1 = df.loc[df['ATR_MN1/AskPrice'].idxmax()]
            least_volatile_mn1 = df.loc[df['ATR_MN1/AskPrice'].idxmin()]
            print(f"\n🔥 Most Volatile (Monthly):  {most_volatile_mn1['Symbol']:<8} {most_volatile_mn1['ATR_MN1/AskPrice']*100:>6.2f}%")
            print(f"📉 Least Volatile (Monthly): {least_volatile_mn1['Symbol']:<8} {least_volatile_mn1['ATR_MN1/AskPrice']*100:>6.2f}%")

        if 'PercentMinted' in df.columns and df['PercentMinted'].notna().any():
            most_minted = df.loc[df['PercentMinted'].idxmax()]
            least_minted = df.loc[df['PercentMinted'].idxmin()]
            print(f"\n🔴 Most Minted:  {most_minted['Symbol']:<8} {most_minted['PercentMinted']:>6.2f}% - Limited supply growth")
            print(f"🔵 Least Minted: {least_minted['Symbol']:<8} {least_minted['PercentMinted']:>6.2f}% - Significant inflation ahead")

        if 'PriceChange24h%' in df.columns and df['PriceChange24h%'].notna().any():
            best_24h = df.loc[df['PriceChange24h%'].idxmax()]
            worst_24h = df.loc[df['PriceChange24h%'].idxmin()]
            print(f"\n🚀 Best 24h Performance:  {best_24h['Symbol']:<8} {best_24h['PriceChange24h%']:>+6.2f}%")
            print(f"💥 Worst 24h Performance: {worst_24h['Symbol']:<8} {worst_24h['PriceChange24h%']:>+6.2f}%")

        print()

        # === 1. PERCENTILE-BASED RISK THRESHOLDS ===
        print_separator()
        print(f"PERCENTILE-BASED RISK ANALYSIS")
        print_separator()

        def get_risk_tier(value, q25, q50, q75):
            """Classify risk level based on quartile position."""
            if value <= q25:
                return "Low Risk"
            elif value <= q50:
                return "Medium Risk"
            elif value <= q75:
                return "High Risk"
            else:
                return "Extreme Risk"

        # Calculate quartiles for key metrics
        var_q25 = df['VaR_to_Ask_Ratio'].quantile(0.25)
        var_q50 = df['VaR_to_Ask_Ratio'].quantile(0.50)
        var_q75 = df['VaR_to_Ask_Ratio'].quantile(0.75)

        atr_q25 = df['ATR_D1/AskPrice'].quantile(0.25)
        atr_q50 = df['ATR_D1/AskPrice'].quantile(0.50)
        atr_q75 = df['ATR_D1/AskPrice'].quantile(0.75)

        print(f"\nVaR/Price Quartiles:")
        print(f"  25th Percentile: {format_percentage(var_q25)}")
        print(f"  50th Percentile (Median): {format_percentage(var_q50)}")
        print(f"  75th Percentile: {format_percentage(var_q75)}")

        print(f"\nATR_D1/Price Quartiles:")
        print(f"  25th Percentile: {format_percentage(atr_q25)}")
        print(f"  50th Percentile (Median): {format_percentage(atr_q50)}")
        print(f"  75th Percentile: {format_percentage(atr_q75)}")

        # Classify each crypto
        print(f"\n{'Symbol':<12} {'VaR Tier':<15} {'ATR Tier':<15} {'Combined Assessment':<25}")
        print_table_separator()
        for _, row in df.iterrows():
            var_tier = get_risk_tier(row['VaR_to_Ask_Ratio'], var_q25, var_q50, var_q75)
            atr_tier = get_risk_tier(row['ATR_D1/AskPrice'], atr_q25, atr_q50, atr_q75)

            # Combined assessment
            if var_tier == "Extreme Risk" or atr_tier == "Extreme Risk":
                combined = "⚠️  High Volatility Asset"
            elif var_tier == "Low Risk" and atr_tier == "Low Risk":
                combined = "✓ Stable Asset"
            else:
                combined = "Moderate Volatility"

            print(f"{row['Symbol']:<12} {var_tier:<15} {atr_tier:<15} {combined:<25}")
        print()

        # === 2. Z-SCORE ANALYSIS ===
        print_separator()
        print(f"Z-SCORE OUTLIER DETECTION")
        print_separator()

        # Calculate z-scores
        df['VaR_ZScore'] = (df['VaR_to_Ask_Ratio'] - df['VaR_to_Ask_Ratio'].mean()) / df['VaR_to_Ask_Ratio'].std()
        df['ATR_D1_ZScore'] = (df['ATR_D1/AskPrice'] - df['ATR_D1/AskPrice'].mean()) / df['ATR_D1/AskPrice'].std()
        df['ATR_W1_ZScore'] = (df['ATR_W1/AskPrice'] - df['ATR_W1/AskPrice'].mean()) / df['ATR_W1/AskPrice'].std()

        print(f"\nZ-Score Analysis (values >2.0 or <-2.0 are statistically notable):\n")
        print(f"{'Symbol':<12} {'VaR Z-Score':<15} {'ATR_D1 Z-Score':<18} {'ATR_W1 Z-Score':<18} {'Notable':<10}")
        print_table_separator()

        for _, row in df.iterrows():
            var_z = row['VaR_ZScore']
            atr_d1_z = row['ATR_D1_ZScore']
            atr_w1_z = row['ATR_W1_ZScore']

            # Flag if any z-score is notable (>2 or <-2)
            notable = "✓" if (abs(var_z) > 2 or abs(atr_d1_z) > 2 or abs(atr_w1_z) > 2) else ""

            print(f"{row['Symbol']:<12} {var_z:>13.2f}  {atr_d1_z:>16.2f}  {atr_w1_z:>16.2f}  {notable:<10}")

        print(f"\nInterpretation:")
        print(f"  Z-Score > 2.0:  Significantly above average (high volatility/risk)")
        print(f"  Z-Score < -2.0: Significantly below average (low volatility/risk)")
        print(f"  -2.0 to 2.0:    Within normal range")
        print()

        # === 3. RATIO COMPARISONS ===
        # Calculate advanced ratio metrics
        if 'VaR_1_Lot' in df.columns and 'ATR_D1' in df.columns:
            df['VaR/ATR_D1'] = df['VaR_1_Lot'] / df['ATR_D1']

        if 'Spread' in df.columns and 'VaR_1_Lot' in df.columns:
            df['Spread/VaR'] = (df['Spread'] / df['VaR_1_Lot']) * 100

        if 'ATR_D1' in df.columns and 'ATR_W1' in df.columns:
            df['ATR_D1/W1_Ratio'] = df['ATR_D1'] / (df['ATR_W1'] / 5)

        if 'ATR_W1' in df.columns and 'ATR_MN1' in df.columns:
            df['ATR_W1/MN1_Ratio'] = df['ATR_W1'] / (df['ATR_MN1'] / 4.33)

        print_separator()
        print(f"ADVANCED RATIO ANALYSIS")
        print_separator()

        print(f"\n1. VaR/ATR Ratio (Regulatory Risk vs Market Volatility):")
        print(f"{'Symbol':<12} {'VaR/ATR':<12} {'Interpretation':<40}")
        print_table_separator()
        if 'VaR/ATR_D1' in df.columns:
            df_sorted = df.sort_values('VaR/ATR_D1', ascending=False)
            avg_var_atr = df['VaR/ATR_D1'].mean()
            for _, row in df_sorted.iterrows():
                ratio = row['VaR/ATR_D1']
                if ratio > avg_var_atr * 1.2:
                    interp = "High regulatory risk relative to volatility"
                elif ratio < avg_var_atr * 0.8:
                    interp = "Low regulatory risk relative to volatility"
                else:
                    interp = "Balanced risk profile"
                print(f"{row['Symbol']:<12} {ratio:>10.2f}  {interp:<40}")
        print()

        print(f"2. Spread/VaR Ratio (Trading Cost Efficiency):")
        print(f"{'Symbol':<12} {'Spread/VaR %':<15} {'Interpretation':<40}")
        print_table_separator()
        if 'Spread/VaR' in df.columns:
            df_sorted = df.sort_values('Spread/VaR', ascending=True)
            for _, row in df_sorted.iterrows():
                ratio = row['Spread/VaR']
                if ratio < 0.01:
                    interp = "Excellent - Very low trading cost"
                elif ratio < 0.05:
                    interp = "Good - Reasonable trading cost"
                elif ratio < 0.1:
                    interp = "Fair - Moderate trading cost"
                else:
                    interp = "⚠️  High trading cost relative to VaR"
                print(f"{row['Symbol']:<12} {ratio:>13.4f}%  {interp:<40}")
        print()

        print(f"3. ATR Timeframe Ratios (Volatility Acceleration Detection):")
        print(f"{'Symbol':<12} {'D1/W1 Ratio':<15} {'W1/MN1 Ratio':<15} {'Trend':<30}")
        print_table_separator()
        if 'ATR_D1/W1_Ratio' in df.columns and 'ATR_W1/MN1_Ratio' in df.columns:
            for _, row in df.iterrows():
                d1_w1 = row['ATR_D1/W1_Ratio']
                w1_mn1 = row['ATR_W1/MN1_Ratio']

                # Interpret trend
                if d1_w1 > 1.2 and w1_mn1 > 1.2:
                    trend = "⚠️  Accelerating volatility"
                elif d1_w1 < 0.8 and w1_mn1 < 0.8:
                    trend = "✓ Declining volatility"
                elif d1_w1 > 1.2:
                    trend = "Recent spike in volatility"
                elif d1_w1 < 0.8:
                    trend = "Recent calm period"
                else:
                    trend = "Stable volatility trend"

                print(f"{row['Symbol']:<12} {d1_w1:>13.2f}  {w1_mn1:>13.2f}  {trend:<30}")
        print()

        # Latest News Section
        if news_data:
            print_separator()
            print(f"📰 LATEST CRYPTOCURRENCY NEWS")
            print_separator()
            for symbol in df['Symbol'].tolist():
                if symbol in news_data and news_data[symbol]:
                    print(f"\n{'-'*80}")
                    print(f"📌 {symbol} - Latest News ({len(news_data[symbol])} articles)")
                    print_table_separator()
                    for i, article in enumerate(news_data[symbol], 1):
                        timestamp = datetime.fromtimestamp(article.get('published_on', 0))
                        title = article.get('title', 'N/A')
                        source = article.get('source', 'N/A')
                        url = article.get('url', '')

                        print(f"\n  [{i}] {title}")
                        print(f"      📅 {timestamp.strftime('%Y-%m-%d %H:%M')} | 📝 {source}")
                        if url:
                            print(f"      🔗 {url}")

                        # Truncate body for readability
                        body = article.get('body', '')
                        if body:
                            summary = body[:250] + '...' if len(body) > 250 else body
                            print(f"      {summary}")
            print()
        else:
            print_separator()
            print(f"📰 NEWS DATA NOT AVAILABLE")
            print_separator()
            print("ℹ️  Run 'python fetch_crypto_news.py' to fetch latest cryptocurrency news.")
            print()

        # Upcoming Events Section
        if events_data:
            print_separator()
            print(f"📅 UPCOMING CRYPTOCURRENCY EVENTS")
            print_separator()
            for symbol in df['Symbol'].tolist():
                if symbol in events_data and events_data[symbol]:
                    print(f"\n{'-'*80}")
                    print(f"🔔 {symbol} - Upcoming Events ({len(events_data[symbol])} events)")
                    print_table_separator()
                    for i, event in enumerate(events_data[symbol], 1):
                        event_date = event.get('date_event', 'N/A')
                        title = event.get('title', {})
                        if isinstance(title, dict):
                            title_text = title.get('en', 'N/A')
                        else:
                            title_text = str(title)

                        # Parse event date for better formatting
                        try:
                            event_dt = datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')
                            formatted_date = event_dt.strftime('%Y-%m-%d %H:%M')
                        except:
                            formatted_date = event_date

                        # Get event categories/types
                        categories = event.get('categories', [])
                        if categories:
                            cat_names = [cat.get('name', '') for cat in categories if isinstance(cat, dict)]
                            category_str = ', '.join(cat_names[:2])  # Show first 2 categories
                        else:
                            category_str = 'General'

                        # Get proof/source
                        source_url = event.get('source', {}).get('url', '') if isinstance(event.get('source'), dict) else ''
                        proof = event.get('proof', '')
                        link = source_url or proof or 'N/A'

                        print(f"\n  [{i}] {title_text}")
                        print(f"      📅 {formatted_date} | 🏷️  {category_str}")
                        if link and link != 'N/A':
                            print(f"      🔗 {link}")

                        # Show description if available
                        description = event.get('description', {})
                        if isinstance(description, dict):
                            desc_text = description.get('en', '')
                        else:
                            desc_text = str(description) if description else ''

                        if desc_text:
                            # Truncate description for readability
                            summary = desc_text[:200] + '...' if len(desc_text) > 200 else desc_text
                            print(f"      {summary}")
            print()
        else:
            print_separator()
            print(f"📅 EVENTS DATA NOT AVAILABLE")
            print_separator()
            print("ℹ️  Run 'python fetch_crypto_events.py --api-key YOUR_KEY' to fetch upcoming events.")
            print("   Sign up at https://coinmarketcal.com/en/developer/register for a free API key.")
            print()

    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enhanced cryptocurrency market analysis with news and events.')
    parser.add_argument('csv_file', type=str, help='Path to the Darwinex CSV file')
    parser.add_argument(
        '--market-data',
        type=str,
        default='crypto_market_data.json',
        help='Path to CoinGecko market data JSON file (default: crypto_market_data.json)'
    )
    parser.add_argument(
        '--news-data',
        type=str,
        default='crypto_news_data.json',
        help='Path to crypto news data JSON file (default: crypto_news_data.json)'
    )
    parser.add_argument(
        '--events-data',
        type=str,
        default='crypto_events_data.json',
        help='Path to crypto events data JSON file (default: crypto_events_data.json)'
    )

    args = parser.parse_args()

    # Check if market data file exists
    market_data_file = args.market_data if Path(args.market_data).exists() else None
    if not market_data_file:
        print(f"Warning: Market data file '{args.market_data}' not found.")
        print("Run 'python fetch_crypto_data.py' first to fetch market data.")
        print("Proceeding with basic analysis only...\n")

    # Check if news data file exists
    news_data_file = args.news_data if Path(args.news_data).exists() else None
    if not news_data_file:
        print(f"Info: News data file '{args.news_data}' not found.")
        print("Run 'python fetch_crypto_news.py' to fetch latest cryptocurrency news.")
        print("Proceeding without news data...\n")

    # Check if events data file exists
    events_data_file = args.events_data if Path(args.events_data).exists() else None
    if not events_data_file:
        print(f"Info: Events data file '{args.events_data}' not found.")
        print("Run 'python fetch_crypto_events.py --api-key YOUR_KEY' to fetch upcoming events.")
        print("Proceeding without events data...\n")

    analyze_crypto_enhanced(args.csv_file, market_data_file, news_data_file, events_data_file)
