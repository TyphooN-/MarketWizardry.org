import pandas as pd
import numpy as np

# This constant is used in the main function.
MINIMUM_INDUSTRY_SIZE = 10

def analyze_industry(industry_name, industry_df):
    """
    Performs a statistical VaR outlier analysis on a DataFrame for a single
    industry or aggregated group. Outliers are split into Actionable and Close Only lists.

    Args:
        industry_name (str): The name of the industry/group being analyzed.
        industry_df (pd.DataFrame): The DataFrame containing the data.
    """
    print(f"\n{'='*30} Analysis for: {industry_name.upper()} {'='*30}")
    print(f"Contains {len(industry_df)} total instruments.")

    # --- Statistical Outlier Analysis ---
    Q1 = industry_df['VaR_to_Ask_Ratio'].quantile(0.25)
    Q3 = industry_df['VaR_to_Ask_Ratio'].quantile(0.75)
    IQR = Q3 - Q1

    if IQR > 0:
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        print("\n--- VaR Ratio Statistics ---")
        print(f"Q1 (25th percentile): {Q1:.4f}")
        print(f"Q3 (75th percentile): {Q3:.4f}")
        print(f"IQR (Interquartile Range): {IQR:.4f}")
        print(f"Lower Outlier Bound: {lower_bound:.4f}")
        print(f"Upper Outlier Bound: {upper_bound:.4f}")

        all_outliers = industry_df[
            (industry_df['VaR_to_Ask_Ratio'] < lower_bound) |
            (industry_df['VaR_to_Ask_Ratio'] > upper_bound)
        ].copy()

        print(f"\n--- Found {len(all_outliers)} Total Statistical VaR Outliers ---")
        
        # --- MODIFICATION: Reverting to separate lists for outliers ---
        if not all_outliers.empty:
            actionable_outliers = all_outliers[all_outliers['TradeMode'] != 3].copy()
            close_only_outliers = all_outliers[all_outliers['TradeMode'] == 3].copy()

            # --- Section 1: Print Actionable (Tradable) Outliers ---
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

            # --- Section 2: Print Non-Actionable (Close Only) Outliers ---
            if not close_only_outliers.empty:
                print("\n>>> Non-Actionable Outliers (Close Only):")
                close_only_outliers.sort_values(by='VaR_to_Ask_Ratio', inplace=True)
                print("WARNING: The following outliers cannot be opened for new trades.")
                for index, row in close_only_outliers.iterrows():
                    note = "(LOW)" if row['VaR_to_Ask_Ratio'] < lower_bound else "(HIGH)"
                    print(f"  - Symbol: {row['Symbol']:<10} | VaR/Ask Ratio: {row['VaR_to_Ask_Ratio']:.4f} {note}")

        else:
            print("No statistical outliers found in this group.")
    else:
        print("\n--- All VaR/Ask Ratios in this group are identical or the group is too small for statistical analysis. ---")


def find_var_outliers_by_industry(filename):
    """
    Main function to load data and orchestrate the industry-by-industry analysis.
    """
    try:
        df = pd.read_csv(filename, delimiter=';')

        # MODIFICATION: Re-added 'SectorName' to required columns for filtering
        required_columns = ['Symbol', 'VaR_1_Lot', 'AskPrice', 'BidPrice', 'TradeMode', 'IndustryName', 'SectorName']
        if not all(col in df.columns for col in required_columns):
            print(f"Error: Required columns missing. Need: {required_columns}")
            return

        # MODIFICATION: Re-added filter to exclude Currency sector at the start
        df = df[df['SectorName'] != 'Currency'].copy()
        
        df = df.dropna(subset=required_columns).copy()

        for col in ['VaR_1_Lot', 'AskPrice', 'BidPrice', 'TradeMode']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['VaR_1_Lot', 'AskPrice', 'BidPrice', 'TradeMode']).copy()
        df['TradeMode'] = df['TradeMode'].astype(int)

        df['VaR_to_Ask_Ratio'] = df.apply(
            lambda row: row['VaR_1_Lot'] / row['AskPrice'] if row['AskPrice'] != 0 else np.nan,
            axis=1
        )
        df['Spread'] = df['AskPrice'] - df['BidPrice']
        df['RelativeSpread_%'] = (df['Spread'] / df['AskPrice']) * 100

        df_cleaned = df.dropna(subset=['VaR_to_Ask_Ratio']).copy()

        if df_cleaned.empty:
            print("No valid data to analyze after cleaning and filtering.")
            return

        industry_counts = df_cleaned['IndustryName'].value_counts()
        
        large_industries = industry_counts[industry_counts >= MINIMUM_INDUSTRY_SIZE].index.tolist()
        small_industries = industry_counts[industry_counts < MINIMUM_INDUSTRY_SIZE].index.tolist()

        print(f"Found {len(large_industries)} large industries to analyze individually.")
        print(f"Found {len(small_industries)} small industries to be aggregated into a single group.")

        for industry in sorted(large_industries):
            industry_df = df_cleaned[df_cleaned['IndustryName'] == industry].copy()
            analyze_industry(industry, industry_df)

        if small_industries:
            aggregated_df = df_cleaned[df_cleaned['IndustryName'].isin(small_industries)].copy()
            if len(aggregated_df) >= MINIMUM_INDUSTRY_SIZE:
                 analyze_industry("AGGREGATED SMALL INDUSTRIES", aggregated_df)
            else:
                 print(f"\n--- Aggregated group of {len(aggregated_df)} stocks is still too small for analysis. ---")

        # --- Final Global Summary Section ---
        print(f"\n{'='*25} Top 20 Global Opportunities (Excluding ETFs) {'='*25}")
        print("The stocks with the absolute lowest VaR/Ask ratio from the entire dataset.")
        
        top_n_global = 20
        
        global_tradable_stocks = df_cleaned[
            (df_cleaned['TradeMode'] != 3) &
            (df_cleaned['IndustryName'] != 'Exchange Traded Fund')
        ].copy()

        global_top_candidates = global_tradable_stocks.sort_values(by='VaR_to_Ask_Ratio').head(top_n_global)

        if not global_top_candidates.empty:
            print("-" * 125)
            print(f"{'Symbol':<10} | {'Industry':<40} | {'VaR/Ask Ratio':<15} | {'Relative Spread':<18} | {'VaR_1_Lot':<12} | {'AskPrice':<12}")
            print("-" * 125)

            for index, row in global_top_candidates.iterrows():
                spread_warning = " (High Spread!)" if row['RelativeSpread_%'] > 1.0 else ""
                print(f"{row['Symbol']:<10} | {row['IndustryName']:<40.40} | {row['VaR_to_Ask_Ratio']:<15.4f} | {row['RelativeSpread_%']:.2f}%{spread_warning:<18} | ${row['VaR_1_Lot']:<11.2f} | ${row['AskPrice']:<11.2f}")
            print("-" * 125)
        else:
            print("Could not identify any global top candidates after excluding ETFs.")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    csv_filename = input("Please enter the CSV filename (e.g., SymbolsExport-Darwinex-Live-Stocks-2025.06.25.csv): ")
    find_var_outliers_by_industry(csv_filename)
