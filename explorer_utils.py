#!/usr/bin/env python3
"""
Shared utility functions for all explorer scripts.
Provides consistent formatting and table rendering across VaR, ATR, EV, and Crypto explorers.
"""

import pandas as pd


def format_price(price):
    """Format price with appropriate precision based on magnitude."""
    if pd.isna(price) or price is None:
        return "N/A"
    if price >= 1000:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.2f}"
    elif price >= 0.01:
        return f"${price:.4f}"
    elif price >= 0.0001:
        return f"${price:.6f}"
    else:
        return f"${price:.8f}"


def format_large_number(num):
    """Format large numbers with B/M/K suffixes."""
    if pd.isna(num) or num is None:
        return "N/A"
    if num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    elif num >= 1e3:
        return f"${num/1e3:.2f}K"
    else:
        return f"${num:.2f}"


def format_percentage(ratio):
    """Format ratio as percentage with 2 decimal places."""
    if pd.isna(ratio) or ratio is None:
        return "N/A"
    return f"{ratio*100:.2f}%"


def format_ratio(ratio, decimals=4):
    """Format ratio with specified decimal places."""
    if pd.isna(ratio) or ratio is None:
        return "N/A"
    return f"{ratio:.{decimals}f}"


def calculate_column_widths(df, columns_config):
    """
    Calculate optimal column widths based on header and data.

    Args:
        df: DataFrame with data
        columns_config: List of tuples (column_name, header_text, format_func, min_width)

    Returns:
        Dictionary mapping column names to widths
    """
    widths = {}

    for col_name, header, format_func, min_width in columns_config:
        if col_name not in df.columns:
            widths[col_name] = max(len(header), min_width)
            continue

        # Start with header length and minimum width
        max_len = max(len(header), min_width)

        # Check actual data lengths
        if format_func:
            formatted_data = df[col_name].apply(lambda x: format_func(x) if not pd.isna(x) else "N/A")
            data_max = formatted_data.str.len().max()
            max_len = max(max_len, data_max if not pd.isna(data_max) else 0)
        else:
            data_max = df[col_name].astype(str).str.len().max()
            max_len = max(max_len, data_max if not pd.isna(data_max) else 0)

        widths[col_name] = max_len

    return widths


def print_formatted_table(df, columns_config, title=None):
    """
    Print a beautifully formatted table with dynamic column widths.

    Args:
        df: DataFrame to print
        columns_config: List of tuples (column_name, header_text, format_func, min_width)
        title: Optional title for the table
    """
    if df.empty:
        if title:
            separator = "═" * 80
            print(f"\n{separator}")
            print(f"{title}")
            print(f"{separator}")
        print("No data to display.")
        return

    # Calculate column widths
    widths = calculate_column_widths(df, columns_config)

    # Build header line to calculate actual table width
    header_parts = []
    for col_name, header, _, _ in columns_config:
        header_parts.append(f"{header:<{widths[col_name]}}")
    header_line = " | ".join(header_parts)
    table_width = len(header_line)

    # Print title if provided
    if title:
        separator = "═" * table_width
        print(f"\n{separator}")
        print(f"{title}")
        print(f"{separator}")

    # Print header
    print(header_line)
    print("─" * table_width)

    # Print data rows
    for _, row in df.iterrows():
        row_parts = []
        for col_name, _, format_func, _ in columns_config:
            if col_name not in df.columns:
                value_str = "N/A"
            else:
                value = row[col_name]
                if pd.isna(value):
                    value_str = "N/A"
                elif format_func:
                    value_str = format_func(value)
                else:
                    value_str = str(value)

            row_parts.append(f"{value_str:<{widths[col_name]}}")

        print(" | ".join(row_parts))

    print("─" * table_width)


def print_section_header(title, char="═", width=None):
    """
    Print a formatted section header.

    Args:
        title: Header title text
        char: Character to use for separator line (default: ═)
        width: Width of separator. If None, uses length of title
    """
    if width is None:
        width = len(title)
    print(f"\n{char * width}")
    print(f"{title}")
    print(f"{char * width}")


def print_statistics(stats_dict, title=None):
    """Print formatted statistics."""
    if title:
        print_section_header(title)

    max_label_len = max(len(label) for label in stats_dict.keys())

    for label, value in stats_dict.items():
        print(f"{label:<{max_label_len + 2}}: {value}")

    print()
