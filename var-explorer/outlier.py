import pandas as pd
import numpy as np

# This constant is used in multiple functions, so it's defined globally.
MINIMUM_GROUP_SIZE = 10

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


def analyze_group(group_name, group_df, bounds_dict=None):
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

            print("\n--- VaR Ratio Statistics ---")
            print(f"Q1 (25th percentile): {Q1:.4f}")
            print(f"Q3 (75th percentile): {Q3:.4f}")
            print(f"IQR (Interquartile Range): {IQR:.4f}")
            print(f"Lower Outlier Bound: {lower_bound:.4f}")
            print(f"Upper Outlier Bound: {upper_bound:.4f}")

            print(f"\n--- Found {len(all_outliers)} Total Statistical VaR Outliers ---")
            
            actionable_outliers = all_outliers[all_outliers['TradeMode'] != 3].copy()
            close_only_outliers = all_outliers[all_outliers['TradeMode'] == 3].copy()

            if not actionable_outliers.empty:
                print("\n>>> Actionable Outliers (Tradable):")
                actionable_outliers.sort_values(by='VaR_to_Ask_Ratio', inplace=True)
                print("-" * 105)
                print(f"{'Symbol':<10} | {'VaR/Ask Ratio':<15} | {'Relative Spread':<18} | {'VaR_1_Lot':<12} | {'AskPrice':<12} | {'Note'}")
                print("-" * 105)
                for index, row in actionable_outliers.iterrows():
                    note = "(LOW - Statistically Significant)" if row['VaR_to_Ask_Ratio'] < lower_bound else "(HIGH)"
                    spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                    print(f"{row['Symbol']:<10} | {row['VaR_to_Ask_Ratio']:<15.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['VaR_1_Lot']:<11.2f} | ${row['AskPrice']:<11.2f} | {note}")
                print("-" * 105)

            if not close_only_outliers.empty:
                print("\n>>> Non-Actionable Outliers (Close Only):")
                close_only_outliers.sort_values(by='VaR_to_Ask_Ratio', inplace=True)
                print("WARNING: The following outliers cannot be opened for new trades.")
                for index, row in close_only_outliers.iterrows():
                    note = "(LOW)" if row['VaR_to_Ask_Ratio'] < lower_bound else "(HIGH)"
                    print(f"  - Symbol: {row['Symbol']:<10} | VaR/Ask Ratio: {row['VaR_to_Ask_Ratio']:.4f} {note}")

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
            analyze_group(industry, industry_df, bounds_dict=industry_bounds)

        if small_industries:
            aggregated_df = df_cleaned[df_cleaned['IndustryName'].isin(small_industries)].copy()
            if len(aggregated_df) >= MINIMUM_GROUP_SIZE:
                analyze_group("AGGREGATED SMALL INDUSTRIES", aggregated_df, bounds_dict=industry_bounds)

        # --- Filter for Price-Based Summaries (Excluding ETFs) ---
        global_tradable_stocks_no_etf = df_cleaned[
            (df_cleaned['TradeMode'] != 3) &
            (df_cleaned['IndustryName'] != 'Exchange Traded Fund')
        ].copy()


        # --- NEW: Top 30 from Lowest Priced Stocks ---
        print(f"\n{'='*25} Top 30 Low VaR/Ask from Lowest Priced Stocks (Excluding ETFs) {'='*25}")
        
        lowest_priced_pool = global_tradable_stocks_no_etf.sort_values(by='AskPrice').head(100)
        top_30_from_lowest_price = lowest_priced_pool.sort_values(by='VaR_to_Ask_Ratio').head(30).copy()
        
        if not top_30_from_lowest_price.empty:
            top_30_from_lowest_price['Note'] = top_30_from_lowest_price.apply(
                get_outlier_note, axis=1, args=(industry_bounds, small_industries)
            )
            print("-" * 155)
            print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Relative Spread':<18} | {'VaR_1_Lot':<12} | {'AskPrice':<12} | {'Note'}")
            print("-" * 155)
            for index, row in top_30_from_lowest_price.iterrows():
                spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:<15.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['VaR_1_Lot']:<11.2f} | ${row['AskPrice']:<11.2f} | {row['Note']}")
            print("-" * 155)
        else:
            print("Could not identify any candidates in this category.")


        # --- NEW: Top 30 from Highest Priced Stocks ---
        print(f"\n{'='*25} Top 30 Low VaR/Ask from Highest Priced Stocks (Excluding ETFs) {'='*25}")
        
        highest_priced_pool = global_tradable_stocks_no_etf.sort_values(by='AskPrice', ascending=False).head(100)
        top_30_from_highest_price = highest_priced_pool.sort_values(by='VaR_to_Ask_Ratio').head(30).copy()
        
        if not top_30_from_highest_price.empty:
            top_30_from_highest_price['Note'] = top_30_from_highest_price.apply(
                get_outlier_note, axis=1, args=(industry_bounds, small_industries)
            )
            print("-" * 155)
            print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Relative Spread':<18} | {'VaR_1_Lot':<12} | {'AskPrice':<12} | {'Note'}")
            print("-" * 155)
            for index, row in top_30_from_highest_price.iterrows():
                spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:<15.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['VaR_1_Lot']:<11.2f} | ${row['AskPrice']:<11.2f} | {row['Note']}")
            print("-" * 155)
        else:
            print("Could not identify any candidates in this category.")


        # --- Filter for Global Summaries (Including ETFs) ---
        global_tradable_stocks_with_etfs = df_cleaned[df_cleaned['TradeMode'] != 3].copy()


        # --- Final Global Summary Section ---
        print(f"\n{'='*25} Top 30 Global Opportunities (Including ETFs) {'='*25}")
        
        top_n_global = 30
        
        global_top_candidates = global_tradable_stocks_with_etfs.sort_values(by='VaR_to_Ask_Ratio').head(top_n_global)
        
        if not global_top_candidates.empty:
            global_top_candidates['Note'] = global_top_candidates.apply(
                get_outlier_note, 
                axis=1, 
                args=(industry_bounds, small_industries)
            )

            print("-" * 155)
            print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Relative Spread':<18} | {'VaR_1_Lot':<12} | {'AskPrice':<12} | {'Note'}")
            print("-" * 155)
            for index, row in global_top_candidates.iterrows():
                spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:<15.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['VaR_1_Lot']:<11.2f} | ${row['AskPrice']:<11.2f} | {row['Note']}")
            print("-" * 155)
        else:
            print("Could not identify any global top candidates.")


        # --- NEW: Top 30 Highest VaR/Ask Stocks ---
        print(f"\n{'='*25} Top 30 Highest VaR/Ask Assets (Including ETFs) {'='*25}")
        
        top_n_highest_var = 30
        
        highest_var_candidates = global_tradable_stocks_with_etfs.sort_values(by='VaR_to_Ask_Ratio', ascending=False).head(top_n_highest_var)
        
        if not highest_var_candidates.empty:
            highest_var_candidates['Note'] = highest_var_candidates.apply(
                get_outlier_note, 
                axis=1, 
                args=(industry_bounds, small_industries)
            )

            print("-" * 155)
            print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Relative Spread':<18} | {'VaR_1_Lot':<12} | {'AskPrice':<12} | {'Note'}")
            print("-" * 155)
            for index, row in highest_var_candidates.iterrows():
                spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:<15.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['VaR_1_Lot']:<11.2f} | ${row['AskPrice']:<11.2f} | {row['Note']}")
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
