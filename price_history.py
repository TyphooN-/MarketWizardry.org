"""
Price history tracking utilities for MarketWizardry.org explorers.

Provides functions to calculate price changes over time by comparing
current CSV data with historical CSV files.
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from pathlib import Path


def find_previous_csv(current_file, days_back=1):
    """
    Find a CSV file from N days ago in the same directory.

    Args:
        current_file (str): Path to current CSV file
        days_back (int): Number of days to look back

    Returns:
        str or None: Path to previous CSV file if found, None otherwise
    """
    # Parse the date from the filename (format: YYYY.MM.DD)
    filename = os.path.basename(current_file)
    date_pattern = r'(\d{4}\.\d{2}\.\d{2})'

    import re
    match = re.search(date_pattern, filename)
    if not match:
        return None

    current_date_str = match.group(1)
    current_date = datetime.strptime(current_date_str, '%Y.%m.%d')
    target_date = current_date - timedelta(days=days_back)
    target_date_str = target_date.strftime('%Y.%m.%d')

    # Build expected filename
    previous_filename = filename.replace(current_date_str, target_date_str)
    previous_file = os.path.join(os.path.dirname(current_file), previous_filename)

    if os.path.exists(previous_file):
        return previous_file

    return None


def load_price_history(current_file, lookback_days=[1, 7, 30]):
    """
    Load historical price data from previous CSV files.

    Args:
        current_file (str): Path to current CSV file
        lookback_days (list): List of days to look back (e.g., [1, 7, 30])

    Returns:
        dict: Dictionary mapping days_back to DataFrames with Symbol and AskPrice
    """
    history = {}

    for days in lookback_days:
        previous_file = find_previous_csv(current_file, days)
        if previous_file:
            try:
                df = pd.read_csv(previous_file, delimiter=';', usecols=['Symbol', 'AskPrice'], encoding='latin1')
                history[days] = df
            except Exception as e:
                print(f"⚠️  Could not load {days}-day history: {e}")

    return history


def calculate_price_changes(df, current_file, lookback_days=[1, 7, 30]):
    """
    Calculate price changes for symbols in the DataFrame.

    Args:
        df (pd.DataFrame): Current DataFrame with Symbol and AskPrice columns
        current_file (str): Path to current CSV file
        lookback_days (list): List of days to look back

    Returns:
        pd.DataFrame: DataFrame with added price change columns
    """
    history = load_price_history(current_file, lookback_days)

    df_with_changes = df.copy()

    for days in lookback_days:
        col_name = f'PriceChange{days}d%'

        if days in history:
            # Merge with historical data
            hist_df = history[days].rename(columns={'AskPrice': f'PrevPrice{days}d'})
            df_with_changes = df_with_changes.merge(
                hist_df,
                on='Symbol',
                how='left'
            )

            # Calculate percentage change
            df_with_changes[col_name] = (
                (df_with_changes['AskPrice'] - df_with_changes[f'PrevPrice{days}d']) /
                df_with_changes[f'PrevPrice{days}d'] * 100
            )

            # Drop the temporary previous price column
            df_with_changes = df_with_changes.drop(columns=[f'PrevPrice{days}d'])
        else:
            # No historical data available
            df_with_changes[col_name] = None

    return df_with_changes


def format_price_change(value, use_emojis=True):
    """
    Format a price change percentage with emoji indicators.

    Args:
        value (float): Price change percentage
        use_emojis (bool): Whether to use rocket/radioactive emojis

    Returns:
        str: Formatted price change string
    """
    if pd.isna(value):
        return "N/A"

    if use_emojis:
        if value > 0:
            emoji = "🚀"
        elif value < 0:
            emoji = "☢️"
        else:
            emoji = "⚪"
        return f"{emoji}{value:+.1f}%"
    else:
        return f"{value:+.1f}%"


def add_price_trend_section(df, current_file, top_n=20):
    """
    Generate a price trend analysis section for a report.

    Args:
        df (pd.DataFrame): DataFrame with Symbol, IndustryName, AskPrice
        current_file (str): Path to current CSV file
        top_n (int): Number of top movers to display

    Returns:
        str: Formatted text report section
    """
    df_with_changes = calculate_price_changes(df, current_file, lookback_days=[1, 7, 30])

    # Check if we have any price change data
    has_1d = df_with_changes['PriceChange1d%'].notna().any()
    has_7d = df_with_changes['PriceChange7d%'].notna().any()
    has_30d = df_with_changes['PriceChange30d%'].notna().any()

    if not (has_1d or has_7d or has_30d):
        return "\n⚠️  Price history not available for trend analysis\n"

    output = []
    output.append("\n" + "=" * 120)
    output.append("📊 PRICE TREND ANALYSIS")
    output.append("=" * 120)

    # Top gainers (1 day)
    if has_1d:
        gainers_1d = df_with_changes.nlargest(top_n, 'PriceChange1d%')
        if not gainers_1d.empty:
            output.append(f"\n🚀 Top {top_n} Gainers (1 Day)")
            output.append("-" * 135)
            output.append(f"{'Symbol':<10} | {'Industry':<40} | {'Current Price':<16} | {'1d Change':<12} | {'Weekly':<12} | {'Monthly':<12} | {'Quarterly':<12}")
            output.append("-" * 135)

            for _, row in gainers_1d.iterrows():
                symbol = row['Symbol'][:10]
                industry = row['IndustryName'][:40] if 'IndustryName' in row else 'N/A'
                price = f"${row['AskPrice']:.2f}" if row['AskPrice'] < 1000 else f"${row['AskPrice']:,.2f}"
                change_1d = format_price_change(row.get('PriceChange1d%'))
                change_7d = format_price_change(row.get('PriceChange7d%'))
                change_30d = format_price_change(row.get('PriceChange30d%'))
                # Monthly is same as 30d for now - can be enhanced later with actual monthly lookback
                change_monthly = change_30d

                output.append(f"{symbol:<10} | {industry:<40} | {price:<16} | {change_1d:<12} | {change_7d:<12} | {change_monthly:<12} | {change_30d:<12}")

    # Top decliners (1 day)
    if has_1d:
        decliners_1d = df_with_changes.nsmallest(top_n, 'PriceChange1d%')
        if not decliners_1d.empty:
            output.append(f"\n☢️  Top {top_n} Decliners (1 Day)")
            output.append("-" * 135)
            output.append(f"{'Symbol':<10} | {'Industry':<40} | {'Current Price':<16} | {'1d Change':<12} | {'Weekly':<12} | {'Monthly':<12} | {'Quarterly':<12}")
            output.append("-" * 135)

            for _, row in decliners_1d.iterrows():
                symbol = row['Symbol'][:10]
                industry = row['IndustryName'][:40] if 'IndustryName' in row else 'N/A'
                price = f"${row['AskPrice']:.2f}" if row['AskPrice'] < 1000 else f"${row['AskPrice']:,.2f}"
                change_1d = format_price_change(row.get('PriceChange1d%'))
                change_7d = format_price_change(row.get('PriceChange7d%'))
                change_30d = format_price_change(row.get('PriceChange30d%'))
                # Monthly is same as 30d for now - can be enhanced later with actual monthly lookback
                change_monthly = change_30d

                output.append(f"{symbol:<10} | {industry:<40} | {price:<16} | {change_1d:<12} | {change_7d:<12} | {change_monthly:<12} | {change_30d:<12}")

    output.append("\n")
    return "\n".join(output)
