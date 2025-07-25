import pandas as pd
import numpy as np
import re
import argparse

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
            print(f"\n{'='*30} Analysis for: {group_name.upper()} {'='*30}")
            
            print(f"Contains {len(group_df)} total instruments.")

            print(f"\n--- VaR Ratio Statistics ---")
            print(f"Q1 (25th percentile): {Q1:.4f}")
            print(f"Q3 (75th percentile): {Q3:.4f}")
            print(f"IQR (Interquartile Range): {IQR:.4f}")
            print(f"Lower Outlier Bound: {lower_bound:.4f}")
            print(f"Upper Outlier Bound: {upper_bound:.4f}")

            print(f"--- Found {len(all_outliers)} Total Statistical VaR Outliers ---")
            
            # Print details of each outlier
            if not all_outliers.empty:
                all_outliers['Note'] = all_outliers.apply(
                    get_outlier_note,
                    axis=1,
                    args=(bounds_dict, small_industries_list)
                )
                print("-" * 125)
                print(f"{'Symbol':<10} | {'Industry':<25} | {'VaR/Ask Ratio':<15} | {'Spread':<18} | {'AskPrice':<12} | {'Note'}")
                print("-" * 125)
                for index, row in all_outliers.iterrows():
                    spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                    print(f"{row['Symbol']:<10} | {row['IndustryName']:<25.25} | {row['VaR_to_Ask_Ratio']:.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['AskPrice']:.2f} | {row['Note']}")
                print("-" * 125)

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
        
        print(f"Detected file type: {file_type}. Displaying top/bottom {TOP_N_DISPLAY} assets at end.")

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

        print(f"\n{'='*25} Global VaR/Ask Ratio Statistics (Including ETFs) {'='*25}")
        print(f"Q1 (25th percentile): {global_Q1:.4f}")
        print(f"Q3 (75th percentile): {global_Q3:.4f}")
        print(f"IQR (Interquartile Range): {global_IQR:.4f}")
        print(f"Lower Outlier Bound: {global_lower_bound:.4f}")
        print(f"Upper Outlier Bound: {global_upper_bound:.4f}")

        print(f"\n{'='*25} Top {TOP_N_DISPLAY} Highest VaR/Ask Assets (Including ETFs) {'='*25}")
        top_n_highest_var = global_tradable_stocks_with_etfs.sort_values(by='VaR_to_Ask_Ratio', ascending=False).head(TOP_N_DISPLAY)
        if not top_n_highest_var.empty:
            top_n_highest_var['Note'] = top_n_highest_var.apply(get_outlier_note, axis=1, args=(industry_bounds, small_industries))
            print("-" * 125)
            print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Spread':<18} | {'AskPrice':<12} | {'Note'}")
            print("-" * 125)
            for index, row in top_n_highest_var.iterrows():
                spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['AskPrice']:.2f} | {row['Note']}")
            print("-" * 125)
        else:
            print("Could not identify any candidates in this category.")

        print(f"\n{'='*25} Bottom {TOP_N_DISPLAY} Lowest VaR/Ask Assets (Including ETFs) {'='*25}")
        bottom_n_lowest_var = global_tradable_stocks_with_etfs.sort_values(by='VaR_to_Ask_Ratio', ascending=True).head(TOP_N_DISPLAY)
        if not bottom_n_lowest_var.empty:
            bottom_n_lowest_var['Note'] = bottom_n_lowest_var.apply(get_outlier_note, axis=1, args=(industry_bounds, small_industries))
            print("-" * 125)
            print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Spread':<18} | {'AskPrice':<12} | {'Note'}")
            print("-" * 125)
            for index, row in bottom_n_lowest_var.iterrows():
                spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['AskPrice']:.2f} | {row['Note']}")
            print("-" * 125)
        else:
            print("Could not identify any candidates in this category.")

        if file_type == 'Stocks':
            print(f"\n{'='*25} Bottom {STOCKS_TOP} Lowest VaR/Ask Stocks (Excluding ETFs) {'='*25}")
            non_etf_stocks = df_for_analysis[(df_for_analysis['TradeMode'] != 3) & (df_for_analysis['IndustryName'] != 'Exchange Traded Fund')].copy()
            bottom_30_lowest_var_no_etf = non_etf_stocks.sort_values(by='VaR_to_Ask_Ratio', ascending=True).head(STOCKS_TOP)
            if not bottom_30_lowest_var_no_etf.empty:
                bottom_30_lowest_var_no_etf['Note'] = bottom_30_lowest_var_no_etf.apply(get_outlier_note, axis=1, args=(industry_bounds, small_industries))
                print("-" * 125)
                print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Spread':<18} | {'AskPrice':<12} | {'Note'}")
                print("-" * 125)
                for index, row in bottom_30_lowest_var_no_etf.iterrows():
                    spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                    print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['AskPrice']:.2f} | {row['Note']}")
                print("-" * 125)
            else:
                print("Could not identify any candidates in this category.")

        # Report on symbols with TradeMode == 3 (close only)
        close_only_symbols = df_for_analysis[df_for_analysis['TradeMode'] == 3]
        if not close_only_symbols.empty:
            print(f"\n{'='*30} Unactionable (Close-Only) Symbols {'='*30}")
            for index, row in close_only_symbols.iterrows():
                print(f"- {row['Symbol']} ({row['IndustryName']})")

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
