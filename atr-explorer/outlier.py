import pandas as pd
import numpy as np
import argparse
import re

MINIMUM_GROUP_SIZE = 5

def find_outliers_iqr(df, column_name):
    """
    Identifies outliers in a specific column of a DataFrame using the IQR method.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        column_name (str): The name of the column to check for outliers.

    Returns:
        pd.DataFrame: A DataFrame containing the outliers.
    """
    if column_name not in df.columns:
        print(f"Warning: Column '{column_name}' not found in DataFrame.")
        return pd.DataFrame(), None, None, None, None, None

    numeric_series = pd.to_numeric(df[column_name], errors='coerce')
    numeric_series.dropna(inplace=True)

    if numeric_series.empty:
        return pd.DataFrame(), None, None, None, None, None

    Q1 = numeric_series.quantile(0.25)
    Q3 = numeric_series.quantile(0.75)
    IQR = Q3 - Q1

    if IQR == 0:
        return pd.DataFrame(), Q1, Q3, IQR, None, None

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (pd.to_numeric(df[column_name], errors='coerce') < lower_bound) |
        (pd.to_numeric(df[column_name], errors='coerce') > upper_bound)
    ]
    
    return outliers, Q1, Q3, IQR, lower_bound, upper_bound

def print_outliers(df, column_name, group_name):
    """
    Prints the outliers in a formatted table.

    Args:
        df (pd.DataFrame): DataFrame containing the outliers.
        column_name (str): The name of the column for which outliers were calculated.
        group_name (str): The name of the group being analyzed.
    """
    if df.empty:
        return

    print(f"\n{'='*25} Outliers for {column_name} in {group_name} {'='*25}")
    
    headers = {
        'Symbol': 15,
        'Industry': 30,
        column_name: 20,
        'AskPrice': 12,
        'Spread': 22
    }

    header_line = " | ".join([f"{h:<{w}}" for h, w in headers.items()])
    print("-" * (sum(headers.values()) + len(headers) * 3))
    print(header_line)
    print("-" * (sum(headers.values()) + len(headers) * 3))

    for _, row in df.iterrows():
        spread_warning = " (High Spread!)" if row.get('RelativeSpread_%', 0) > 1.0 else ""
        
        symbol_str = f"{row['Symbol']:<{headers['Symbol']}}"
        industry_str = f"{row['IndustryName']:<{headers['Industry']}.{headers['Industry']}}"
        ratio_value_str = f"{row[column_name]:.4f}"
        ratio_value_str = f"{ratio_value_str:<{headers[column_name]}}"
        ask_price_str = f"${row['AskPrice']:.2f}"
        ask_price_str = f"{ask_price_str:<{headers['AskPrice']}}"
        spread_str = f"{row.get('RelativeSpread_%', 0):.2f}%{spread_warning}"
        spread_str = f"{spread_str:<{headers['Spread']}}"

        print(f"{symbol_str} | {industry_str} | {ratio_value_str} | {ask_price_str} | {spread_str}")

    print("-" * (sum(headers.values()) + len(headers) * 3))

def analyze_group(group_name, group_df, column_name):
    """
    Performs a statistical ATR outlier analysis on a given group of stocks.
    """
    if len(group_df) < MINIMUM_GROUP_SIZE:
        return

    outliers, q1, q3, iqr, lower_bound, upper_bound = find_outliers_iqr(group_df, column_name)

    if not outliers.empty:
        print(f"\n{'='*25} IQR Statistics for {column_name} in {group_name} {'='*25}")
        print(f"Q1 (25th percentile): {q1:.4f}")
        print(f"Q3 (75th percentile): {q3:.4f}")
        print(f"IQR (Interquartile Range): {iqr:.4f}")
        if lower_bound is not None and upper_bound is not None:
            print(f"Lower Outlier Bound: {lower_bound:.4f}")
            print(f"Upper Outlier Bound: {upper_bound:.4f}")
        print_outliers(outliers, column_name, group_name)

def find_atr_outliers(filename):
    """
    Main function to load data and find outliers in ATR columns.
    """
    try:
        df = pd.read_csv(filename, delimiter=';', encoding='latin1')
        
        file_type = "Unknown"
        if "Stocks" in filename:
            file_type = "Stocks"
        elif "CFD" in filename:
            file_type = "CFD"
        elif "Futures" in filename:
            file_type = "Futures"

        if 'AskPrice' in df.columns and 'BidPrice' in df.columns:
            df['AskPrice'] = pd.to_numeric(df['AskPrice'], errors='coerce')
            df['BidPrice'] = pd.to_numeric(df['BidPrice'], errors='coerce')
            df['Spread'] = df['AskPrice'] - df['BidPrice']
            df['RelativeSpread_%'] = (df['Spread'] / df['AskPrice']) * 100 if df['AskPrice'].ne(0).all() else 0

        atr_columns = ['ATR_D1', 'ATR_W1', 'ATR_MN1']
        ratio_columns = []
        for col in atr_columns:
            ratio_col_name = f'{col}/AskPrice'
            df[ratio_col_name] = pd.to_numeric(df[col], errors='coerce') / df['AskPrice']
            ratio_columns.append(ratio_col_name)

        for col in ratio_columns:
            # Global analysis
            analyze_group(f"Global ({file_type})", df, col)

            # Industry-level analysis
            industry_counts = df['IndustryName'].value_counts()
            large_industries = industry_counts[industry_counts >= MINIMUM_GROUP_SIZE].index.tolist()
            small_industries = industry_counts[industry_counts < MINIMUM_GROUP_SIZE].index.tolist()

            for industry in sorted(large_industries):
                industry_df = df[df['IndustryName'] == industry].copy()
                analyze_group(industry, industry_df, col)

            # Aggregated sector analysis for small industries
            if small_industries:
                small_industries_df = df[df['IndustryName'].isin(small_industries)].copy()
                sectors_with_small_industries = small_industries_df['SectorName'].unique().tolist()
                
                for sector in sorted(sectors_with_small_industries):
                    sector_aggregated_df = small_industries_df[small_industries_df['SectorName'] == sector].copy()
                    
                    if len(sector_aggregated_df) >= MINIMUM_GROUP_SIZE:
                        aggregated_group_name = f"AGGREGATED {sector.upper()} INDUSTRIES"
                        analyze_group(aggregated_group_name, sector_aggregated_df, col)

        df.to_csv(filename, sep=';', index=False, encoding='latin1')

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find ATR outliers in a given CSV file.')
    parser.add_argument('filename', type=str, help='The path to the CSV file to analyze.')
    
    args = parser.parse_args()
    
    find_atr_outliers(args.filename)