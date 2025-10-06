"""
Static Chart Generator for MarketWizardry.org (CSP-Safe)

Generates static SVG/PNG charts using matplotlib instead of Plotly.
100% CSP-compliant - no JavaScript, no inline styles, no CDN dependencies.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import os

# MarketWizardry.org Color Scheme (CRT Terminal Aesthetic)
COLORS = {
    'background': '#000000',        # Black background
    'text': '#00ff00',              # Bright green text
    'grid': '#003300',              # Dark green grid
    'accent': '#00ff88',            # Light green accent
    'positive': '#00ff00',          # Green for gains
    'negative': '#ff0000',          # Red for losses
    'neutral': '#888888',           # Gray for neutral
    'highlight': 'rgba(0, 255, 0, 0.3)',  # Semi-transparent green
}

# Set global matplotlib style
plt.style.use('dark_background')
matplotlib.rcParams['font.family'] = 'monospace'
matplotlib.rcParams['font.size'] = 10
matplotlib.rcParams['text.color'] = COLORS['text']
matplotlib.rcParams['axes.labelcolor'] = COLORS['text']
matplotlib.rcParams['xtick.color'] = COLORS['text']
matplotlib.rcParams['ytick.color'] = COLORS['text']
matplotlib.rcParams['axes.edgecolor'] = COLORS['text']
matplotlib.rcParams['grid.color'] = COLORS['grid']
matplotlib.rcParams['figure.facecolor'] = COLORS['background']
matplotlib.rcParams['axes.facecolor'] = COLORS['background']


def save_chart_html(fig, output_path, title, base_url="https://marketwizardry.org"):
    """
    Save matplotlib figure as SVG embedded in HTML (CSP compliant).

    Args:
        fig: Matplotlib figure object
        output_path (str): Output HTML file path
        title (str): Chart title
        base_url (str): Base URL for canonical link
    """
    # Save SVG to string
    import io
    svg_buffer = io.StringIO()
    fig.savefig(svg_buffer, format='svg', bbox_inches='tight', facecolor=COLORS['background'])
    svg_content = svg_buffer.getvalue()
    svg_buffer.close()

    # Extract relative path for canonical URL
    filename = os.path.basename(output_path)
    dirname = os.path.basename(os.path.dirname(output_path)) if os.path.dirname(output_path) else 'charts'
    canonical_url = f"{base_url}/{dirname}/{filename}"

    # HTML template - 100% CSP compliant (no inline styles!)
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="TyphooN">
    <title>MarketWizardry.org Chart - {title}</title>
    <link rel="canonical" href="{canonical_url}">
    <link rel="stylesheet" href="/css/shared-styles.css">
</head>
<body class="chart-page-body">
    <div class="chart-header">
        <h1>📊 MarketWizardry.org Chart Viewer</h1>
    </div>

    <div class="chart-link-container">
        <button class="chart-back-link" data-action="chart-back">← Back to Report</button>
    </div>

    <div class="chart-container-static">
        {svg_content}
    </div>

    <div class="chart-link-container-bottom">
        <button class="chart-back-link" data-action="chart-back">← Back to Report</button>
    </div>

    <script src="/js/chart-navigation.js"></script>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

    plt.close(fig)


def create_price_trend_chart(df, output_path, title="Price Trend Analysis", lookback_days=[1, 7, 30]):
    """
    Create price trend bar chart showing gainers and decliners.

    Args:
        df: DataFrame with price change columns
        output_path: Output HTML file path
        title: Chart title
        lookback_days: List of lookback periods to display
    """
    fig, axes = plt.subplots(1, len(lookback_days), figsize=(18, 6))
    if len(lookback_days) == 1:
        axes = [axes]

    fig.suptitle(title, fontsize=16, color=COLORS['text'], family='monospace')

    for idx, days in enumerate(lookback_days):
        ax = axes[idx]
        col_name = f'Price_Change_{days}d_%'

        if col_name not in df.columns:
            continue

        # Sort and get top gainers/losers
        sorted_df = df.sort_values(col_name, ascending=False).head(20)

        colors = [COLORS['positive'] if x > 0 else COLORS['negative'] for x in sorted_df[col_name]]

        ax.barh(sorted_df['Symbol'], sorted_df[col_name], color=colors, edgecolor=COLORS['text'], linewidth=0.5)
        ax.set_xlabel(f'{days}-Day Change (%)', color=COLORS['text'], family='monospace')
        ax.set_title(f'{days}-Day Price Trends', color=COLORS['accent'], family='monospace')
        ax.grid(True, alpha=0.3, color=COLORS['grid'])
        ax.axvline(0, color=COLORS['text'], linewidth=1, linestyle='--')

        # Set background
        ax.set_facecolor(COLORS['background'])

    plt.tight_layout()
    save_chart_html(fig, output_path, title)


def create_risk_distribution_chart(df, risk_col, output_path, title="Risk Distribution"):
    """
    Create histogram of risk distribution.

    Args:
        df: DataFrame with risk column
        risk_col: Column name containing risk values
        output_path: Output HTML file path
        title: Chart title
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create histogram
    n, bins, patches = ax.hist(df[risk_col].dropna(), bins=50,
                                edgecolor=COLORS['text'], linewidth=0.5,
                                color=COLORS['accent'], alpha=0.7)

    # Color bars by value
    for i, patch in enumerate(patches):
        if bins[i] > df[risk_col].median():
            patch.set_facecolor(COLORS['negative'])
        else:
            patch.set_facecolor(COLORS['positive'])

    ax.set_xlabel(risk_col, color=COLORS['text'], family='monospace')
    ax.set_ylabel('Frequency', color=COLORS['text'], family='monospace')
    ax.set_title(title, color=COLORS['accent'], family='monospace', fontsize=14)
    ax.grid(True, alpha=0.3, color=COLORS['grid'])
    ax.set_facecolor(COLORS['background'])

    plt.tight_layout()
    save_chart_html(fig, output_path, title)


def create_scatter_plot(df, x_col, y_col, output_path, title="Scatter Plot",
                       color_col=None, hover_col='Symbol'):
    """
    Create scatter plot.

    Args:
        df: DataFrame
        x_col: X-axis column name
        y_col: Y-axis column name
        output_path: Output HTML file path
        title: Chart title
        color_col: Optional column for color coding
        hover_col: Column to use for point labels
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    if color_col and color_col in df.columns:
        # Color by category
        unique_vals = df[color_col].unique()
        colors_map = plt.cm.get_cmap('viridis', len(unique_vals))

        for idx, val in enumerate(unique_vals):
            mask = df[color_col] == val
            ax.scatter(df[mask][x_col], df[mask][y_col],
                      label=str(val), alpha=0.6, s=50,
                      color=colors_map(idx), edgecolors=COLORS['text'], linewidth=0.5)
        ax.legend(facecolor=COLORS['background'], edgecolor=COLORS['text'])
    else:
        ax.scatter(df[x_col], df[y_col], color=COLORS['accent'],
                  alpha=0.6, s=50, edgecolors=COLORS['text'], linewidth=0.5)

    ax.set_xlabel(x_col, color=COLORS['text'], family='monospace')
    ax.set_ylabel(y_col, color=COLORS['text'], family='monospace')
    ax.set_title(title, color=COLORS['accent'], family='monospace', fontsize=14)
    ax.grid(True, alpha=0.3, color=COLORS['grid'])
    ax.set_facecolor(COLORS['background'])

    plt.tight_layout()
    save_chart_html(fig, output_path, title)


def create_top_assets_chart(df, value_col, output_path, title="Top Assets", n=20, ascending=False):
    """
    Create horizontal bar chart of top assets.

    Args:
        df: DataFrame
        value_col: Column to sort/display by
        output_path: Output HTML file path
        title: Chart title
        n: Number of top assets to show
        ascending: Sort order
    """
    fig, ax = plt.subplots(figsize=(12, 10))

    # Sort and select top N
    sorted_df = df.sort_values(value_col, ascending=ascending).head(n)

    # Color based on positive/negative
    colors = [COLORS['positive'] if x > 0 else COLORS['negative']
             for x in sorted_df[value_col]]

    ax.barh(sorted_df['Symbol'], sorted_df[value_col],
           color=colors, edgecolor=COLORS['text'], linewidth=0.5, alpha=0.8)

    ax.set_xlabel(value_col, color=COLORS['text'], family='monospace')
    ax.set_title(title, color=COLORS['accent'], family='monospace', fontsize=14)
    ax.grid(True, alpha=0.3, color=COLORS['grid'], axis='x')
    ax.axvline(0, color=COLORS['text'], linewidth=1, linestyle='--')
    ax.set_facecolor(COLORS['background'])

    plt.tight_layout()
    save_chart_html(fig, output_path, title)


# Example usage
if __name__ == "__main__":
    # Test with sample data
    import numpy as np

    test_data = {
        'Symbol': [f'SYM{i}' for i in range(50)],
        'Price_Change_1d_%': np.random.randn(50) * 5,
        'Price_Change_7d_%': np.random.randn(50) * 10,
        'VaR_95': np.random.randn(50) * 2 + 5,
        'Volume': np.random.randint(1000, 100000, 50)
    }

    df = pd.DataFrame(test_data)

    print("Generating test charts...")
    create_price_trend_chart(df, 'test_price_trend.html', "Test Price Trends")
    create_risk_distribution_chart(df, 'VaR_95', 'test_risk_dist.html', "Test Risk Distribution")
    create_scatter_plot(df, 'VaR_95', 'Volume', 'test_scatter.html', "Test Scatter")
    create_top_assets_chart(df, 'Price_Change_1d_%', 'test_top_assets.html', "Test Top Movers")
    print("✅ Test charts generated!")
