import pandas as pd
import numpy as np
import argparse
import re
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from explorer_utils import format_price, format_percentage, format_ratio, print_formatted_table, print_section_header, print_statistics
from price_history import add_price_trend_section, calculate_price_changes
from chart_generator import create_price_trend_chart, create_risk_distribution_chart, create_top_assets_chart

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

    # Add warning indicator for high spreads
    df_display = df.copy()
    df_display['Spread_Display'] = df_display.apply(
        lambda row: f"{format_percentage(row.get('RelativeSpread_%', 0) / 100)} {'⚠️' if row.get('RelativeSpread_%', 0) > 1.0 else ''}",
        axis=1
    )

    # Configure columns for display
    columns_config = [
        ('Symbol', 'Symbol', None, 12),
        ('IndustryName', 'Industry', lambda x: x[:35] if len(x) > 35 else x, 35),
        (column_name, 'ATR/Price', format_ratio, 12),
        ('AskPrice', 'Current Price', format_price, 14),
        ('Spread_Display', 'Spread', None, 15)
    ]

    print_formatted_table(df_display, columns_config, f"Outliers for {column_name} in {group_name}")

def analyze_group(group_name, group_df, column_name):
    """
    Performs a statistical ATR outlier analysis on a given group of stocks.
    """
    if len(group_df) < MINIMUM_GROUP_SIZE:
        return

    outliers, q1, q3, iqr, lower_bound, upper_bound = find_outliers_iqr(group_df, column_name)

    if not outliers.empty:
        stats = {
            'Q1 (25th percentile)': format_ratio(q1),
            'Q3 (75th percentile)': format_ratio(q3),
            'IQR (Interquartile Range)': format_ratio(iqr)
        }
        if lower_bound is not None and upper_bound is not None:
            stats['Lower Outlier Bound'] = format_ratio(lower_bound)
            stats['Upper Outlier Bound'] = format_ratio(upper_bound)

        print_statistics(stats, f"IQR Statistics for {column_name} in {group_name}")
        print_outliers(outliers, column_name, group_name)

def find_atr_outliers(filename):
    """
    Main function to load data and find outliers in ATR columns.
    """
    try:
        print_section_header("ATR OUTLIER ANALYSIS")
        print(f"File: {filename}")
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

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

        # Report on symbols with TradeMode == 3 (close only)
        close_only_symbols = df[df['TradeMode'] == 3]
        
        # Exclude close-only symbols from the analysis
        df_for_analysis = df[df['TradeMode'] != 3].copy()

        for col in ratio_columns:
            # Global analysis
            analyze_group(f"Global ({file_type})", df_for_analysis, col)

            # Industry-level analysis
            industry_counts = df_for_analysis['IndustryName'].value_counts()
            large_industries = industry_counts[industry_counts >= MINIMUM_GROUP_SIZE].index.tolist()
            small_industries = industry_counts[industry_counts < MINIMUM_GROUP_SIZE].index.tolist()

            for industry in sorted(large_industries):
                industry_df = df_for_analysis[df_for_analysis['IndustryName'] == industry].copy()
                analyze_group(industry, industry_df, col)

            # Aggregated sector analysis for small industries
            if small_industries:
                small_industries_df = df_for_analysis[df_for_analysis['IndustryName'].isin(small_industries)].copy()
                sectors_with_small_industries = small_industries_df['SectorName'].unique().tolist()
                
                for sector in sorted(sectors_with_small_industries):
                    sector_aggregated_df = small_industries_df[small_industries_df['SectorName'] == sector].copy()
                    
                    if len(sector_aggregated_df) >= MINIMUM_GROUP_SIZE:
                        aggregated_group_name = f"AGGREGATED {sector.upper()} INDUSTRIES"
                        analyze_group(aggregated_group_name, sector_aggregated_df, col)

        df.to_csv(filename, sep=';', index=False, encoding='latin1')

        if not close_only_symbols.empty:
            print_section_header("⚠️  UNACTIONABLE (CLOSE-ONLY) SYMBOLS")
            for index, row in close_only_symbols.iterrows():
                print(f"  • {row['Symbol']:<12} ({row['IndustryName']})")

        # Add price trend analysis section
        print(add_price_trend_section(df, filename, top_n=20))

        # Generate HTML charts
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        chart_dir = os.path.dirname(filename)
        explorer_name = os.path.basename(chart_dir)  # e.g., "atr-explorer"

        print("\n" + "=" * 120)
        print("📊 INTERACTIVE HTML CHARTS")
        print("=" * 120)

        # Calculate price changes for chart generation
        df_with_changes = calculate_price_changes(df, filename, lookback_days=[1, 7, 30])

        # Generate price trend chart
        if 'PriceChange1d%' in df_with_changes.columns and df_with_changes['PriceChange1d%'].notna().sum() > 0:
            chart_filename = f"{base_filename}-price-trends.html"
            chart_path = os.path.join(chart_dir, chart_filename)
            create_price_trend_chart(df_with_changes, chart_path,
                                   title=f"Price Trends - {base_filename}",
                                   lookback_days=[1, 7, 30])
            print(f"\n📈 Price Trends Chart: https://marketwizardry.org/{explorer_name}/{chart_filename}")

        # Generate ATR distribution chart
        chart_filename = f"{base_filename}-atr-distribution.html"
        chart_path = os.path.join(chart_dir, chart_filename)
        create_risk_distribution_chart(df, 'ATR_to_Ask_Ratio', chart_path,
                                      title=f"ATR/Price Ratio Distribution - {base_filename}")
        print(f"📊 ATR Distribution Chart: https://marketwizardry.org/{explorer_name}/{chart_filename}")

        # Generate top/bottom volatility charts
        chart_filename = f"{base_filename}-top-bottom-atr.html"
        chart_path = os.path.join(chart_dir, chart_filename)
        create_top_assets_chart(df, 'ATR_to_Ask_Ratio', chart_path,
                               title=f"Top 20 Highest/Lowest ATR Ratios - {base_filename}",
                               n=20, ascending=False)
        print(f"📊 Top/Bottom Volatility Chart: https://marketwizardry.org/{explorer_name}/{chart_filename}")
        print("=" * 120)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find ATR outliers in a given CSV file.')
    parser.add_argument('filename', type=str, help='The path to the CSV file to analyze.')
    
    args = parser.parse_args()
    
    find_atr_outliers(args.filename)