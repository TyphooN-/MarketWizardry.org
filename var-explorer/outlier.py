import pandas as pd
import numpy as np

# This constant is used in multiple functions, so it's defined globally.
MINIMUM_GROUP_SIZE = 10
TOP_N_DISPLAY = 20 # User-defined variable for top/bottom N display

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
    ratio = row['VaR_to_Ask_Ratio']

    # Determine which group the stock belongs to for bound checking
    group_name = "AGGREGATED SMALL INDUSTRIES" if industry in small_industries_list else industry

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
            print(f"{'='*30} Analysis for: {group_name.upper()} {'='*30}")
            
            print(f"Contains {len(group_df)} total instruments.")

            print(f"\n--- VaR Ratio Statistics ---")
            print(f"Q1 (25th percentile): {Q1:.4f}")
            print(f"Q3 (75th percentile): {Q3:.4f}")
            print(f"IQR (Interquartile Range): {IQR:.4f}")
            print(f"Lower Outlier Bound: {lower_bound:.4f}")
            print(f"Upper Outlier Bound: {upper_bound:.4f}")

            print(f"Contains {len(group_df)} total instruments.")

            print("\n--- VaR Ratio Statistics ---")
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
                print("-" * 100)
                print(f"{'Symbol':<10} | {'Industry':<25} | {'VaR/Ask Ratio':<15} | {'Note'}")
                print("-" * 100)
                for index, row in all_outliers.iterrows():
                    print(f"{row['Symbol']:<10} | {row['IndustryName']:<25.25} | {row['VaR_to_Ask_Ratio']:.4f} | {row['Note']}")
                print("-" * 100)
            
        else:
            print("\nNo statistical outliers found in this group.")


def find_var_outliers(filename):
    """
    Main function to load and clean data, then orchestrate a tiered analysis that
    only reports on groups where significant outliers are found.
    """
    try:
        df = pd.read_csv(filename, delimiter=';', encoding='latin1')
        required_columns = ['Symbol', 'VaR_1_Lot', 'AskPrice', 'BidPrice', 'TradeMode', 'IndustryName', 'SectorName']
        if not all(col in df.columns for col in required_columns):
            print(f"Error: Required columns missing. Need: {required_columns}")
            return

        df = df[df['SectorName'] != 'Currency'].copy()
        df = df.dropna(subset=required_columns).copy()

        for col in ['VaR_1_Lot', 'AskPrice', 'BidPrice', 'TradeMode']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['VaR_1_Lot', 'AskPrice', 'BidPrice', 'TradeMode']).copy()
        df['TradeMode'] = df['TradeMode'].astype(int)

        df['VaR_to_Ask_Ratio'] = df.apply(lambda r: r['VaR_1_Lot'] / r['AskPrice'] if r['AskPrice'] != 0 else np.nan, axis=1)
        df['Spread'] = df['AskPrice'] - df['BidPrice']
        df['RelativeSpread_%'] = (df['Spread'] / df['AskPrice']) * 100
        df_cleaned = df.dropna(subset=['VaR_to_Ask_Ratio']).copy()

        if df_cleaned.empty: return print("No valid data to analyze after cleaning.")

        industry_counts = df_cleaned['IndustryName'].value_counts()
        
        large_industries = industry_counts[industry_counts >= MINIMUM_GROUP_SIZE].index.tolist()
        small_industries = industry_counts[industry_counts < MINIMUM_GROUP_SIZE].index.tolist()

        print(f"Processing {len(large_industries)} large industries and {len(small_industries)} small industries...")

        # Dictionary to store outlier bounds for each group.
        industry_bounds = {}

        # --- Run Analysis ---
        for industry in sorted(large_industries):
            industry_df = df_cleaned[df_cleaned['IndustryName'] == industry].copy()
            analyze_group(industry, industry_df, bounds_dict=industry_bounds, small_industries_list=small_industries)

        if small_industries:
            aggregated_df = df_cleaned[df_cleaned['IndustryName'].isin(small_industries)].copy()
            if len(aggregated_df) >= MINIMUM_GROUP_SIZE:
                analyze_group("AGGREGATED SMALL INDUSTRIES", aggregated_df, bounds_dict=industry_bounds, small_industries_list=small_industries)

        # --- Filter for Global Summaries (Including ETFs) ---
        global_tradable_stocks_with_etfs = df_cleaned[df_cleaned['TradeMode'] != 3].copy()

        # Calculate global statistics
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

        # --- Top 10 VaR/Ask Stocks ---
        print(f"\n{'='*25} Top {TOP_N_DISPLAY} Highest VaR/Ask Assets (Including ETFs) {'='*25}")
        top_n_highest_var = global_tradable_stocks_with_etfs.sort_values(by='VaR_to_Ask_Ratio', ascending=False).head(TOP_N_DISPLAY)
        if not top_n_highest_var.empty:
            top_n_highest_var['Note'] = top_n_highest_var.apply(
                get_outlier_note,
                axis=1,
                args=(industry_bounds, small_industries)
            )
            print("-" * 155)
            print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Relative Spread':<18} | {'VaR_1_Lot':<12} | {'AskPrice':<12} | {'Note'}")
            print("-" * 155)
            for index, row in top_n_highest_var.iterrows():
                spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['VaR_1_Lot']:.2f} | ${row['AskPrice']:.2f} | {row['Note']}")
            print("-" * 155)
        else:
            print("Could not identify any candidates in this category.")

        # --- Bottom 10 VaR/Ask Stocks ---
        print(f"\n{'='*25} Bottom {TOP_N_DISPLAY} Lowest VaR/Ask Assets (Including ETFs) {'='*25}")
        bottom_n_lowest_var = global_tradable_stocks_with_etfs.sort_values(by='VaR_to_Ask_Ratio', ascending=True).head(TOP_N_DISPLAY)
        if not bottom_n_lowest_var.empty:
            bottom_n_lowest_var['Note'] = bottom_n_lowest_var.apply(
                get_outlier_note,
                axis=1,
                args=(industry_bounds, small_industries)
            )
            print("-" * 155)
            print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Relative Spread':<18} | {'VaR_1_Lot':<12} | {'AskPrice':<12} | {'Note'}")
            print("-" * 155)
            for index, row in bottom_n_lowest_var.iterrows():
                spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['VaR_1_Lot']:.2f} | ${row['AskPrice']:.2f} | {row['Note']}")
            print("-" * 155)
        else:
            print("Could not identify any candidates in this category.")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_filename = sys.argv[1]
        find_var_outliers(csv_filename)
    else:
        print("Usage: python outlier.py <csv_filename>")
