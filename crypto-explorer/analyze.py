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

        # Calculate advanced ratio metrics
        # VaR/ATR ratio - regulatory risk vs volatility
        if 'VaR_1_Lot' in df.columns and 'ATR_D1' in df.columns:
            df['VaR/ATR_D1'] = df['VaR_1_Lot'] / df['ATR_D1']

        # Spread/VaR ratio - trading cost efficiency
        if 'Spread' in df.columns and 'VaR_1_Lot' in df.columns:
            df['Spread/VaR'] = (df['Spread'] / df['VaR_1_Lot']) * 100

        # ATR timeframe ratios - detect volatility acceleration
        if 'ATR_D1' in df.columns and 'ATR_W1' in df.columns:
            df['ATR_D1/W1_Ratio'] = df['ATR_D1'] / (df['ATR_W1'] / 5)  # Normalize weekly to daily

        if 'ATR_W1' in df.columns and 'ATR_MN1' in df.columns:
            df['ATR_W1/MN1_Ratio'] = df['ATR_W1'] / (df['ATR_MN1'] / 4.33)  # Normalize monthly to weekly

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

        # === 1. PERCENTILE-BASED RISK THRESHOLDS ===
        print(f"{'='*30} PERCENTILE-BASED RISK ANALYSIS {'='*30}")

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
        print(f"  25th Percentile: {var_q25:.4f} ({var_q25*100:.2f}%)")
        print(f"  50th Percentile (Median): {var_q50:.4f} ({var_q50*100:.2f}%)")
        print(f"  75th Percentile: {var_q75:.4f} ({var_q75*100:.2f}%)")

        print(f"\nATR_D1/Price Quartiles:")
        print(f"  25th Percentile: {atr_q25:.4f} ({atr_q25*100:.2f}%)")
        print(f"  50th Percentile (Median): {atr_q50:.4f} ({atr_q50*100:.2f}%)")
        print(f"  75th Percentile: {atr_q75:.4f} ({atr_q75*100:.2f}%)")

        # Classify each crypto
        print(f"\n{'Symbol':<12} {'VaR Tier':<15} {'ATR Tier':<15} {'Combined Assessment':<25}")
        print("-" * 75)
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
        print(f"{'='*30} Z-SCORE OUTLIER DETECTION {'='*30}")

        # Calculate z-scores
        df['VaR_ZScore'] = (df['VaR_to_Ask_Ratio'] - df['VaR_to_Ask_Ratio'].mean()) / df['VaR_to_Ask_Ratio'].std()
        df['ATR_D1_ZScore'] = (df['ATR_D1/AskPrice'] - df['ATR_D1/AskPrice'].mean()) / df['ATR_D1/AskPrice'].std()
        df['ATR_W1_ZScore'] = (df['ATR_W1/AskPrice'] - df['ATR_W1/AskPrice'].mean()) / df['ATR_W1/AskPrice'].std()

        print(f"\nZ-Score Analysis (values >2.0 or <-2.0 are statistically notable):\n")
        print(f"{'Symbol':<12} {'VaR Z-Score':<15} {'ATR_D1 Z-Score':<18} {'ATR_W1 Z-Score':<18} {'Notable':<10}")
        print("-" * 80)

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
        print(f"{'='*30} ADVANCED RATIO ANALYSIS {'='*30}")

        print(f"\n1. VaR/ATR Ratio (Regulatory Risk vs Market Volatility):")
        print(f"{'Symbol':<12} {'VaR/ATR':<12} {'Interpretation':<40}")
        print("-" * 70)
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

        print(f"\n2. Spread/VaR Ratio (Trading Cost Efficiency):")
        print(f"{'Symbol':<12} {'Spread/VaR %':<15} {'Interpretation':<40}")
        print("-" * 72)
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

        print(f"\n3. ATR Timeframe Ratios (Volatility Acceleration Detection):")
        print(f"{'Symbol':<12} {'D1/W1 Ratio':<15} {'W1/MN1 Ratio':<15} {'Trend':<30}")
        print("-" * 80)
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
