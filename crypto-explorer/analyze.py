import pandas as pd
import numpy as np
import argparse
from datetime import datetime

# Forex pairs to exclude (static list)
FOREX_PAIRS = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'NZDUSD', 'USDCAD',
               'EURGBP', 'EURJPY', 'GBPJPY', 'EURCHF', 'AUDJPY', 'EURAUD', 'GBPAUD',
               'GBPCAD', 'GBPCHF', 'AUDCAD', 'AUDCHF', 'AUDNZD', 'NZDCHF', 'NZDJPY',
               'NZDCAD', 'CADJPY', 'CADCHF', 'CHFJPY', 'EURNZD', 'EURCAD']

def calculate_correlation_matrix(df, atr_columns):
    """
    Calculate correlation matrix for ATR values across crypto pairs.
    """
    correlation_data = {}
    for col in atr_columns:
        if col in df.columns:
            correlation_data[col] = pd.to_numeric(df[col], errors='coerce')

    if not correlation_data:
        return None

    corr_df = pd.DataFrame(correlation_data, index=df['Symbol'])
    return corr_df.T.corr()

def analyze_crypto(filename):
    """
    Analyzes crypto currency pairs with metrics appropriate for crypto markets.
    """
    try:
        print(f"Crypto Market Analysis for {filename}")
        print(f"Report generated on: {datetime.now()}")
        print()

        df = pd.read_csv(filename, delimiter=';', encoding='latin1')

        # Filter out forex pairs (keep all crypto)
        df = df[~df['Symbol'].isin(FOREX_PAIRS)].copy()
        print(f"Filtered to {len(df)} crypto pairs (excluded {len(FOREX_PAIRS)} forex pairs)")
        print()

        # Convert numeric columns
        numeric_cols = ['AskPrice', 'BidPrice', 'Spread', 'ATR_D1', 'ATR_W1', 'ATR_MN1',
                       'VaR_1_Lot', 'RelativeSpread_%']

        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Calculate ATR ratios if not present
        for atr_col in ['ATR_D1', 'ATR_W1', 'ATR_MN1']:
            ratio_col = f'{atr_col}/AskPrice'
            if ratio_col not in df.columns and atr_col in df.columns:
                df[ratio_col] = df[atr_col] / df['AskPrice']

        # Calculate VaR to Ask ratio if not present
        if 'VaR_to_Ask_Ratio' not in df.columns and 'VaR_1_Lot' in df.columns:
            df['VaR_to_Ask_Ratio'] = df['VaR_1_Lot'] / df['AskPrice']

        print(f"{'='*30} CRYPTO MARKET OVERVIEW {'='*30}")
        print(f"Total Pairs Analyzed: {len(df)}")
        print(f"Symbols: {', '.join(df['Symbol'].tolist())}")
        print()

        # Volatility Rankings
        print(f"{'='*30} DAILY VOLATILITY RANKING (ATR_D1/Price) {'='*30}")
        df_sorted = df.sort_values('ATR_D1/AskPrice', ascending=False)
        print(f"{'Rank':<6} {'Symbol':<12} {'ATR/Price':<15} {'Daily ATR':<15} {'Price':<15} {'Spread %':<12}")
        print("-" * 90)
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            print(f"{idx:<6} {row['Symbol']:<12} {row['ATR_D1/AskPrice']:.4f} ({row['ATR_D1/AskPrice']*100:.2f}%)    "
                  f"${row['ATR_D1']:>12,.2f}    ${row['AskPrice']:>12,.2f}    {row.get('RelativeSpread_%', 0):.3f}%")
        print()

        # Weekly Volatility Rankings
        print(f"{'='*30} WEEKLY VOLATILITY RANKING (ATR_W1/Price) {'='*30}")
        df_sorted = df.sort_values('ATR_W1/AskPrice', ascending=False)
        print(f"{'Rank':<6} {'Symbol':<12} {'ATR/Price':<15} {'Weekly ATR':<15} {'Price':<15} {'Spread %':<12}")
        print("-" * 90)
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            print(f"{idx:<6} {row['Symbol']:<12} {row['ATR_W1/AskPrice']:.4f} ({row['ATR_W1/AskPrice']*100:.2f}%)    "
                  f"${row['ATR_W1']:>12,.2f}    ${row['AskPrice']:>12,.2f}    {row.get('RelativeSpread_%', 0):.3f}%")
        print()

        # Monthly Volatility Rankings
        if 'ATR_MN1/AskPrice' in df.columns:
            print(f"{'='*30} MONTHLY VOLATILITY RANKING (ATR_MN1/Price) {'='*30}")
            df_sorted = df.sort_values('ATR_MN1/AskPrice', ascending=False)
            print(f"{'Rank':<6} {'Symbol':<12} {'ATR/Price':<15} {'Monthly ATR':<15} {'Price':<15} {'Spread %':<12}")
            print("-" * 90)
            for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
                print(f"{idx:<6} {row['Symbol']:<12} {row['ATR_MN1/AskPrice']:.4f} ({row['ATR_MN1/AskPrice']*100:.2f}%)    "
                      f"${row['ATR_MN1']:>12,.2f}    ${row['AskPrice']:>12,.2f}    {row.get('RelativeSpread_%', 0):.3f}%")
            print()

        # VaR Rankings
        print(f"{'='*30} VALUE AT RISK RANKING (VaR/Price) {'='*30}")
        df_sorted = df.sort_values('VaR_to_Ask_Ratio', ascending=False)
        print(f"{'Rank':<6} {'Symbol':<12} {'VaR/Price':<15} {'VaR (1 Lot)':<15} {'Price':<15} {'Spread %':<12}")
        print("-" * 90)
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            print(f"{idx:<6} {row['Symbol']:<12} {row['VaR_to_Ask_Ratio']:.4f} ({row['VaR_to_Ask_Ratio']*100:.2f}%)    "
                  f"${row['VaR_1_Lot']:>12,.2f}    ${row['AskPrice']:>12,.2f}    {row.get('RelativeSpread_%', 0):.3f}%")
        print()

        # Note: Correlation analysis requires multiple time periods
        # Single-day snapshots cannot generate meaningful correlation data
        print(f"{'='*30} NOTE: CORRELATION ANALYSIS {'='*30}")
        print("Correlation analysis requires historical time-series data.")
        print("Single-day snapshots show current volatility rankings only.")
        print("For correlation analysis, multiple dates of ATR data are needed.")
        print()

        # Summary Statistics
        print(f"{'='*30} SUMMARY STATISTICS {'='*30}")
        print(f"Average Daily Volatility (ATR/Price): {df['ATR_D1/AskPrice'].mean():.4f} ({df['ATR_D1/AskPrice'].mean()*100:.2f}%)")
        print(f"Average Weekly Volatility (ATR/Price): {df['ATR_W1/AskPrice'].mean():.4f} ({df['ATR_W1/AskPrice'].mean()*100:.2f}%)")
        if 'ATR_MN1/AskPrice' in df.columns:
            print(f"Average Monthly Volatility (ATR/Price): {df['ATR_MN1/AskPrice'].mean():.4f} ({df['ATR_MN1/AskPrice'].mean()*100:.2f}%)")
        print(f"Average VaR/Price Ratio: {df['VaR_to_Ask_Ratio'].mean():.4f} ({df['VaR_to_Ask_Ratio'].mean()*100:.2f}%)")
        print(f"Average Spread: {df.get('RelativeSpread_%', pd.Series([0])).mean():.4f}%")
        print()

        # Insights
        print(f"{'='*30} KEY INSIGHTS {'='*30}")

        # Most/Least volatile
        most_volatile = df.loc[df['ATR_D1/AskPrice'].idxmax()]
        least_volatile = df.loc[df['ATR_D1/AskPrice'].idxmin()]
        print(f"Most Volatile (Daily): {most_volatile['Symbol']} ({most_volatile['ATR_D1/AskPrice']*100:.2f}%)")
        print(f"Least Volatile (Daily): {least_volatile['Symbol']} ({least_volatile['ATR_D1/AskPrice']*100:.2f}%)")

        # Highest/Lowest VaR
        highest_var = df.loc[df['VaR_to_Ask_Ratio'].idxmax()]
        lowest_var = df.loc[df['VaR_to_Ask_Ratio'].idxmin()]
        print(f"Highest VaR/Price: {highest_var['Symbol']} ({highest_var['VaR_to_Ask_Ratio']*100:.2f}%)")
        print(f"Lowest VaR/Price: {lowest_var['Symbol']} ({lowest_var['VaR_to_Ask_Ratio']*100:.2f}%)")

        # Spread warnings
        if 'RelativeSpread_%' in df.columns:
            high_spread = df[df['RelativeSpread_%'] > 0.1]
            if not high_spread.empty:
                print(f"\nHigh Spread Warning (>0.1%): {', '.join(high_spread['Symbol'].tolist())}")

        print()

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze cryptocurrency market data.')
    parser.add_argument('filename', type=str, help='The path to the CSV file to analyze.')

    args = parser.parse_args()

    analyze_crypto(args.filename)
