import pandas as pd
import numpy as np
import re
import argparse
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from explorer_utils import format_price, format_percentage, format_ratio, print_formatted_table, print_section_header, print_statistics
from price_history import add_price_trend_section, calculate_price_changes
from chart_generator import create_price_trend_chart, create_risk_distribution_chart, create_top_assets_chart

# This constant is used in multiple functions, so it's defined globally.
MINIMUM_GROUP_SIZE = 5
STOCKS_TOP = 30 # User-defined variable for top/bottom N display for Stocks
CFD_TOP = 40    # User-defined variable for top/bottom N display for CFDs
FUTURES_TOP = 5 # User-defined variable for top/bottom N display for Futures
TOP_N_DISPLAY = 20 # User-defined variable for top/bottom N display (will be set dynamically)

def get_outlier_note(row, bounds_dict, small_industries_list):
    """
    Determines the outlier status note for a given stock row.

    Args:
        row (pd.Series): A row from the DataFrame.
        bounds_dict (dict): A dictionary containing the outlier bounds for each industry.
        small_industries_list (list): A list of industries classified as small.

    Returns:
        str: A note indicating the stock's outlier status.
    """
    industry = row['IndustryName']
    sector = row['SectorName'] # Get the sector for the current row
    ratio = row['VaR_to_Ask_Ratio']

    # Determine which group the stock belongs to for bound checking
    if industry in small_industries_list:
        # If it's a small industry, its group name is its aggregated sector group
        group_name = f"AGGREGATED {sector.upper()} INDUSTRIES"
    else:
        # Otherwise, it's its own industry group
        group_name = industry

    # Check if bounds were successfully calculated for this group
    if group_name in bounds_dict:
        bounds = bounds_dict[group_name]
        if ratio < bounds['lower']:
            return '(LOW - Statistically Significant)'
        elif ratio > bounds['upper']:
            return '(HIGH - Statistically Significant)'
    
    # Default note if it's not a statistical outlier within its group
    return '(Low VaR/Ask)'


def analyze_group(group_name, group_df, bounds_dict=None, small_industries_list=None):
    """
    Performs a statistical VaR outlier analysis on a given group of stocks.
    This function will produce NO output unless at least one
    statistically significant outlier is found.

    Args:
        group_name (str): The name of the industry/group being analyzed.
        group_df (pd.DataFrame): The DataFrame containing the data.
        bounds_dict (dict, optional): A dictionary to store the calculated bounds.
    """
    # Silently exit if the group is too small for meaningful analysis
    if len(group_df) < MINIMUM_GROUP_SIZE:
        return

    # --- Perform calculations silently first ---
    Q1 = group_df['VaR_to_Ask_Ratio'].quantile(0.25)
    Q3 = group_df['VaR_to_Ask_Ratio'].quantile(0.75)
    IQR = Q3 - Q1

    # Only proceed if there is a statistical range to measure
    if IQR > 0:
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # MODIFICATION: Store the calculated bounds in the shared dictionary
        if bounds_dict is not None:
            bounds_dict[group_name] = {'lower': lower_bound, 'upper': upper_bound}

        all_outliers = group_df[
            (group_df['VaR_to_Ask_Ratio'] < lower_bound) |
            (group_df['VaR_to_Ask_Ratio'] > upper_bound)
        ].copy()

        # --- Only print a report if outliers were actually found ---
        if not all_outliers.empty:
            print_dataframe(all_outliers, bounds_dict, small_industries_list, f"Analysis for: {group_name.upper()}")


def print_dataframe(df, bounds_dict, small_industries_list, table_title):
    """Helper function to print DataFrame contents with aligned columns."""

    # Apply the get_outlier_note function to get the 'Note' for each row
    df_display = df.copy()
    df_display['Note'] = df_display.apply(get_outlier_note, axis=1, args=(bounds_dict, small_industries_list))

    # Add warning indicator for high spreads
    df_display['Spread_Display'] = df_display.apply(
        lambda row: f"{format_percentage(row.get('RelativeSpread_%', 0) / 100)} {'⚠️' if row.get('RelativeSpread_%', 0) > 1.0 else ''}",
        axis=1
    )

    # Configure columns for display
    columns_config = [
        ('Symbol', 'Symbol', None, 12),
        ('IndustryName', 'Industry', lambda x: x[:38] if len(x) > 38 else x, 38),
        ('VaR_to_Ask_Ratio', 'Risk Ratio', format_percentage, 12),
        ('Spread_Display', 'Spread', None, 12),
        ('AskPrice', 'Price', format_price, 14),
        ('Note', 'Status', None, 35)
    ]

    print_formatted_table(df_display, columns_config, table_title)

def find_var_outliers(filename, overwrite=False):
    """
    Main function to load and clean data, then orchestrate a tiered analysis that
    only reports on groups where significant outliers are found.
    """
    try:
        global TOP_N_DISPLAY
        file_type = "Unknown"
        if re.search(r'Stocks', filename, re.IGNORECASE):
            file_type = "Stocks"
            TOP_N_DISPLAY = STOCKS_TOP
        elif re.search(r'CFD', filename, re.IGNORECASE):
            file_type = "CFD"
            TOP_N_DISPLAY = CFD_TOP
        elif re.search(r'Futures', filename, re.IGNORECASE):
            file_type = "Futures"
            TOP_N_DISPLAY = FUTURES_TOP

        print_section_header("VALUE AT RISK (VAR) OUTLIER ANALYSIS")
        print(f"File: {filename}")
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"File Type: {file_type}")
        print(f"Displaying Top/Bottom {TOP_N_DISPLAY} Assets")
        print()

        df = pd.read_csv(filename, delimiter=';', encoding='latin1')

        # Check for symbols with invalid VaR value before cleaning
        if 'VaR_1_Lot' in df.columns and 'Symbol' in df.columns:
            # Using .astype(str).str.strip() to safely handle different dtypes and whitespace
            invalid_var_mask = df['VaR_1_Lot'].astype(str).str.strip() == '-nan(ind)'
            for symbol in df.loc[invalid_var_mask, 'Symbol']:
                print(f"WARNING: {symbol} has no VaR value detected!")

        required_columns = ['Symbol', 'VaR_1_Lot', 'AskPrice', 'BidPrice', 'TradeMode', 'IndustryName', 'SectorName']
        if not all(col in df.columns for col in required_columns):
            print(f"Warning: Some required columns are missing. Analysis might be incomplete. Missing: {[col for col in required_columns if col not in df.columns]}")

        if file_type == 'Stocks':
            df = df[df['SectorName'] != 'Currency'].copy()

        for col in ['VaR_1_Lot', 'AskPrice', 'BidPrice', 'TradeMode']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['TradeMode'] = df['TradeMode'].astype(int)

        if 'VaR_to_Ask_Ratio' not in df.columns or overwrite:
            df['VaR_to_Ask_Ratio'] = df.apply(lambda r: r['VaR_1_Lot'] / r['AskPrice'] if r['AskPrice'] != 0 else np.nan, axis=1)
            try:
                df.to_csv(filename, sep=';', index=False, encoding='latin1')
            except Exception as e:
                print(f"Error saving updated CSV {filename}: {e}")

        df['Spread'] = df['AskPrice'] - df['BidPrice']
        df['RelativeSpread_%'] = (df['Spread'] / df['AskPrice']) * 100
        df_for_analysis = df.dropna(subset=['VaR_to_Ask_Ratio']).copy()

        if df_for_analysis.empty: return print("No valid data to analyze after cleaning.")

        industry_counts = df_for_analysis['IndustryName'].value_counts()
        
        large_industries = industry_counts[industry_counts >= MINIMUM_GROUP_SIZE].index.tolist()
        small_industries = industry_counts[industry_counts < MINIMUM_GROUP_SIZE].index.tolist()

        industry_bounds = {}

        for industry in sorted(large_industries):
            industry_df = df_for_analysis[df_for_analysis['IndustryName'] == industry].copy()
            analyze_group(industry, industry_df, bounds_dict=industry_bounds, small_industries_list=small_industries)

        # New intelligent aggregation for small industries by sector
        if small_industries:
            small_industries_df = df_for_analysis[df_for_analysis['IndustryName'].isin(small_industries)].copy()
            sectors_with_small_industries = small_industries_df['SectorName'].unique().tolist()
            
            for sector in sorted(sectors_with_small_industries):
                sector_aggregated_df = small_industries_df[small_industries_df['SectorName'] == sector].copy()
                
                if len(sector_aggregated_df) >= MINIMUM_GROUP_SIZE:
                    aggregated_group_name = f"AGGREGATED {sector.upper()} INDUSTRIES"
                    analyze_group(aggregated_group_name, sector_aggregated_df, bounds_dict=industry_bounds, small_industries_list=small_industries)
                else:
                    print(f"Skipping aggregation for sector '{sector}': Not enough instruments ({len(sector_aggregated_df)}) to meet MINIMUM_GROUP_SIZE ({MINIMUM_GROUP_SIZE}).")

        global_tradable_stocks_with_etfs = df_for_analysis[df_for_analysis['TradeMode'] != 3].copy()

        global_Q1 = global_tradable_stocks_with_etfs['VaR_to_Ask_Ratio'].quantile(0.25)
        global_Q3 = global_tradable_stocks_with_etfs['VaR_to_Ask_Ratio'].quantile(0.75)
        global_IQR = global_Q3 - global_Q1
        global_lower_bound = global_Q1 - 1.5 * global_IQR
        global_upper_bound = global_Q3 + 1.5 * global_IQR

        stats = {
            'Q1 (25th percentile)': format_percentage(global_Q1),
            'Q3 (75th percentile)': format_percentage(global_Q3),
            'IQR (Interquartile Range)': format_percentage(global_IQR),
            'Lower Outlier Bound': format_percentage(global_lower_bound),
            'Upper Outlier Bound': format_percentage(global_upper_bound)
        }
        print_statistics(stats, "📊 Global VaR/Ask Ratio Statistics (Including ETFs)")

        top_n_highest_var = global_tradable_stocks_with_etfs.sort_values(by='VaR_to_Ask_Ratio', ascending=False).head(TOP_N_DISPLAY)
        if not top_n_highest_var.empty:
            print_dataframe(top_n_highest_var, industry_bounds, small_industries, f"Top {TOP_N_DISPLAY} Highest VaR/Ask Assets (Including ETFs)")
        else:
            print("Could not identify any candidates in this category.")

        bottom_n_lowest_var = global_tradable_stocks_with_etfs.sort_values(by='VaR_to_Ask_Ratio', ascending=True).head(TOP_N_DISPLAY)
        if not bottom_n_lowest_var.empty:
            print_dataframe(bottom_n_lowest_var, industry_bounds, small_industries, f"Bottom {TOP_N_DISPLAY} Lowest VaR/Ask Assets (Including ETFs)")
        else:
            print("Could not identify any candidates in this category.")

        if file_type == 'Stocks':
            non_etf_stocks = df_for_analysis[(df_for_analysis['TradeMode'] != 3) & (df_for_analysis['IndustryName'] != 'Exchange Traded Fund')].copy()
            bottom_30_lowest_var_no_etf = non_etf_stocks.sort_values(by='VaR_to_Ask_Ratio', ascending=True).head(STOCKS_TOP)
            if not bottom_30_lowest_var_no_etf.empty:
                print_dataframe(bottom_30_lowest_var_no_etf, industry_bounds, small_industries, f"Bottom {STOCKS_TOP} Lowest VaR/Ask Stocks (Excluding ETFs)")
            else:
                print("Could not identify any candidates in this category.")

        # Report on symbols with TradeMode == 3 (close only)
        close_only_symbols = df_for_analysis[df_for_analysis['TradeMode'] == 3]
        if not close_only_symbols.empty:
            print_section_header("⚠️  UNACTIONABLE (CLOSE-ONLY) SYMBOLS")
            for index, row in close_only_symbols.iterrows():
                print(f"  • {row['Symbol']:<12} ({row['IndustryName']})")

        # Add price trend analysis section
        print(add_price_trend_section(df_for_analysis, filename, top_n=TOP_N_DISPLAY))

        # Generate HTML charts
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        chart_dir = os.path.dirname(filename)
        explorer_name = os.path.basename(chart_dir)  # e.g., "var-explorer"

        print("\n" + "=" * 120)
        print("📊 INTERACTIVE HTML CHARTS")
        print("=" * 120)

        # Calculate price changes for chart generation
        df_with_changes = calculate_price_changes(df_for_analysis, filename, lookback_days=[1, 7, 30])

        # Generate price trend chart
        if 'PriceChange1d%' in df_with_changes.columns and df_with_changes['PriceChange1d%'].notna().sum() > 0:
            chart_filename = f"{base_filename}-price-trends.html"
            chart_path = os.path.join(chart_dir, chart_filename)
            create_price_trend_chart(df_with_changes, chart_path,
                                   title=f"Price Trends - {base_filename}",
                                   lookback_days=[1, 7, 30])
            print(f"   📈 Price Trends Chart: https://marketwizardry.org/{explorer_name}/{chart_filename}")

        # Generate risk distribution chart
        chart_filename = f"{base_filename}-risk-distribution.html"
        chart_path = os.path.join(chart_dir, chart_filename)
        create_risk_distribution_chart(df_for_analysis, 'VaR_to_Ask_Ratio', chart_path,
                                      title=f"VaR/Price Ratio Distribution - {base_filename}")
        print(f"   📊 Risk Distribution Chart: https://marketwizardry.org/{explorer_name}/{chart_filename}")

        # Generate top/bottom risk charts
        chart_filename = f"{base_filename}-top-bottom-risk.html"
        chart_path = os.path.join(chart_dir, chart_filename)
        create_top_assets_chart(df_for_analysis, 'VaR_to_Ask_Ratio', chart_path,
                               title=f"Top {TOP_N_DISPLAY} Highest/Lowest VaR Ratios - {base_filename}",
                               n=TOP_N_DISPLAY, ascending=False)
        print(f"   📊 Top/Bottom Volatility Chart: https://marketwizardry.org/{explorer_name}/{chart_filename}")
        print("=" * 120)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find VaR outliers in a given CSV file.')
    parser.add_argument('filename', type=str, help='The path to the CSV file to analyze.')
    parser.add_argument('--overwrite', action='store_true', help='Force recalculation and overwrite of the VaR/Ask Ratio column.')
    
    args = parser.parse_args()
    
    find_var_outliers(args.filename, args.overwrite)
