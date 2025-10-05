"""
HTML Chart Generator for MarketWizardry.org Explorers

Creates interactive Plotly charts with terminal CRT aesthetic matching the website.
Outputs standalone HTML files that can be linked from text reports.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.utils
from plotly.subplots import make_subplots
import os
import json
import html


# MarketWizardry.org Color Scheme (CRT Terminal Aesthetic)
COLORS = {
    'background': '#000000',        # Black background
    'text': '#00ff00',              # Bright green text
    'grid': '#003300',              # Dark green grid
    'accent': '#00ff88',            # Light green accent
    'positive': '#00ff00',          # Green for gains (rocket 🚀)
    'negative': '#ff0000',          # Red for losses (radioactive ☢️)
    'neutral': '#888888',           # Gray for neutral
    'highlight': 'rgba(0, 255, 0, 0.3)',  # Semi-transparent green
}

# Font settings
FONT_FAMILY = 'Courier New, monospace'


def get_base_layout(title, width=1400, height=800):
    """
    Get base layout configuration matching MarketWizardry.org aesthetic.

    Args:
        title (str): Chart title
        width (int): Chart width in pixels
        height (int): Chart height in pixels

    Returns:
        dict: Plotly layout configuration
    """
    return {
        'title': {
            'text': title,
            'font': {
                'family': FONT_FAMILY,
                'size': 24,
                'color': COLORS['text']
            },
            'x': 0.5,
            'xanchor': 'center'
        },
        'plot_bgcolor': COLORS['background'],
        'paper_bgcolor': COLORS['background'],
        'font': {
            'family': FONT_FAMILY,
            'color': COLORS['text'],
            'size': 12
        },
        'xaxis': {
            'gridcolor': COLORS['grid'],
            'color': COLORS['text'],
            'linecolor': COLORS['text']
        },
        'yaxis': {
            'gridcolor': COLORS['grid'],
            'color': COLORS['text'],
            'linecolor': COLORS['text']
        },
        'width': width,
        'height': height,
        'hovermode': 'closest',
        'hoverlabel': {
            'bgcolor': COLORS['background'],
            'font': {
                'family': FONT_FAMILY,
                'color': COLORS['text']
            },
            'bordercolor': COLORS['text']
        }
    }


def save_html_chart(fig, output_path, base_url="https://marketwizardry.org"):
    """
    Save Plotly figure as standalone HTML with custom styling (CSP compliant).

    Args:
        fig: Plotly figure object
        output_path (str): Output file path
        base_url (str): Base URL for the site (default: https://marketwizardry.org)
    """
    # Determine the chart path relative to base
    # Convert /home/typhoon/git/MarketWizardry.org/var-explorer/chart.html
    # to var-explorer/chart.html
    import os
    filename = os.path.basename(output_path)
    dirname = os.path.basename(os.path.dirname(output_path))
    relative_path = f"{dirname}/{filename}"

    # Custom HTML template with CRT styling (CSP COMPLIANT - Plotly CDN allowed)
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="TyphooN">
    <title>MarketWizardry.org Chart - {chart_title}</title>
    <link rel="canonical" href="{canonical_url}">
    <link rel="stylesheet" href="/css/shared-styles.css">
    <script src="https://cdn.plotly.com/plotly-2.35.2.min.js" charset="utf-8"></script>
</head>
<body class="chart-page-body">
    <div class="chart-header">
        <h1>📊 MarketWizardry.org Chart Viewer</h1>
    </div>

    <div class="chart-link-container">
        <button class="chart-back-link" data-action="chart-back">← Back to Report</button>
    </div>

    <div class="chart-container">
        {plot_div}
    </div>

    <div class="chart-link-container-bottom">
        <button class="chart-back-link" data-action="chart-back">← Back to Report</button>
    </div>

    <script src="/js/chart-navigation.js"></script>
</body>
</html>
"""

    # Convert figure to JSON data (CSP compliant - no inline scripts!)
    import json
    import html

    # Extract data, layout, and config as JSON
    chart_data = json.dumps(fig.data, cls=plotly.utils.PlotlyJSONEncoder)
    chart_layout = json.dumps(fig.layout, cls=plotly.utils.PlotlyJSONEncoder)
    chart_config = json.dumps({
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'responsive': True
    })

    # Escape for HTML attributes (escape quotes and special chars)
    chart_data_escaped = html.escape(chart_data, quote=True)
    chart_layout_escaped = html.escape(chart_layout, quote=True)
    chart_config_escaped = html.escape(chart_config, quote=True)

    # Create div with data attributes (CSP compliant - no inline script)
    # Using double quotes for attribute values with proper escaping
    plot_div = f'''<div id="chart" class="plotly-graph-div"
        data-plotly-data="{chart_data_escaped}"
        data-plotly-layout="{chart_layout_escaped}"
        data-plotly-config="{chart_config_escaped}"></div>'''

    # Get chart title from figure
    chart_title = fig.layout.title.text if fig.layout.title and fig.layout.title.text else "Chart"

    # Build canonical URL (avoid double slashes, but preserve https://)
    canonical_url = f"{base_url}/{relative_path}"
    # Replace any double slashes except in https://
    canonical_url = canonical_url.replace('https://', 'HTTPS_PLACEHOLDER').replace('//', '/').replace('HTTPS_PLACEHOLDER', 'https://')

    # Write final HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template.format(
            plot_div=plot_div,
            chart_title=chart_title,
            canonical_url=canonical_url
        ))


def create_price_trend_chart(df, output_path, title="Price Trend Analysis", lookback_days=[1, 7, 30]):
    """
    Create price trend chart showing gainers and decliners.

    Args:
        df (pd.DataFrame): DataFrame with price change columns
        output_path (str): Output HTML file path
        title (str): Chart title
        lookback_days (list): List of lookback periods
    """
    # Get top gainers and decliners for primary lookback period
    primary_col = f'PriceChange{lookback_days[0]}d%'

    if primary_col not in df.columns or df[primary_col].notna().sum() == 0:
        print(f"⚠️  No price change data available for {primary_col}")
        return

    top_gainers = df.nlargest(20, primary_col)
    top_decliners = df.nsmallest(20, primary_col)

    # Create subplots - 2 rows x 2 cols for 1d and 30d charts
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f"🚀 Top 20 Gainers ({lookback_days[0]}d)",
            f"☢️ Top 20 Decliners ({lookback_days[0]}d)",
            f"🚀 Top 20 Gainers (30d - Quarterly)",
            f"☢️ Top 20 Decliners (30d - Quarterly)"
        ),
        horizontal_spacing=0.12,
        vertical_spacing=0.08
    )

    # Add 1-day gainers bar chart (row 1, col 1)
    fig.add_trace(
        go.Bar(
            x=top_gainers[primary_col],
            y=top_gainers['Symbol'],
            orientation='h',
            marker=dict(color=COLORS['positive'], line=dict(color=COLORS['text'], width=1)),
            hovertemplate='<b>%{y}</b><br>Change: %{x:.2f}%<extra></extra>',
            name='Gainers (1d)'
        ),
        row=1, col=1
    )

    # Add 1-day decliners bar chart (row 1, col 2)
    fig.add_trace(
        go.Bar(
            x=top_decliners[primary_col],
            y=top_decliners['Symbol'],
            orientation='h',
            marker=dict(color=COLORS['negative'], line=dict(color=COLORS['text'], width=1)),
            hovertemplate='<b>%{y}</b><br>Change: %{x:.2f}%<extra></extra>',
            name='Decliners (1d)'
        ),
        row=1, col=2
    )

    # Add 30-day (quarterly) charts if available
    quarterly_col = 'PriceChange30d%'
    if quarterly_col in df.columns and df[quarterly_col].notna().sum() > 0:
        top_gainers_30d = df.nlargest(20, quarterly_col)
        top_decliners_30d = df.nsmallest(20, quarterly_col)

        # Add 30-day gainers bar chart (row 2, col 1)
        fig.add_trace(
            go.Bar(
                x=top_gainers_30d[quarterly_col],
                y=top_gainers_30d['Symbol'],
                orientation='h',
                marker=dict(color=COLORS['positive'], line=dict(color=COLORS['text'], width=1)),
                hovertemplate='<b>%{y}</b><br>Change: %{x:.2f}%<extra></extra>',
                name='Gainers (30d)'
            ),
            row=2, col=1
        )

        # Add 30-day decliners bar chart (row 2, col 2)
        fig.add_trace(
            go.Bar(
                x=top_decliners_30d[quarterly_col],
                y=top_decliners_30d['Symbol'],
                orientation='h',
                marker=dict(color=COLORS['negative'], line=dict(color=COLORS['text'], width=1)),
                hovertemplate='<b>%{y}</b><br>Change: %{x:.2f}%<extra></extra>',
                name='Decliners (30d)'
            ),
            row=2, col=2
        )

    # Update layout
    layout = get_base_layout(title, width=1600, height=1400)
    layout['showlegend'] = False

    # Update all axes
    for i in range(1, 5):  # 4 subplots
        layout[f'xaxis{i if i > 1 else ""}'] = {'title': 'Price Change (%)', 'gridcolor': COLORS['grid'], 'color': COLORS['text']}
        layout[f'yaxis{i if i > 1 else ""}'] = {'title': 'Symbol', 'gridcolor': COLORS['grid'], 'color': COLORS['text'], 'autorange': 'reversed'}

    fig.update_layout(layout)

    save_html_chart(fig, output_path)


def create_risk_distribution_chart(df, risk_col, output_path, title="Risk Distribution"):
    """
    Create histogram showing risk ratio distribution.

    Args:
        df (pd.DataFrame): DataFrame with risk column
        risk_col (str): Name of risk ratio column
        output_path (str): Output HTML file path
        title (str): Chart title
    """
    if risk_col not in df.columns:
        print(f"⚠️  Column {risk_col} not found in DataFrame")
        return

    fig = go.Figure()

    # Add histogram
    fig.add_trace(go.Histogram(
        x=df[risk_col],
        nbinsx=50,
        marker=dict(
            color=COLORS['text'],
            line=dict(color=COLORS['background'], width=1)
        ),
        hovertemplate='Range: %{x}<br>Count: %{y}<extra></extra>',
        name='Distribution'
    ))

    # Add mean line
    mean_val = df[risk_col].mean()
    fig.add_vline(
        x=mean_val,
        line_dash="dash",
        line_color=COLORS['accent'],
        annotation_text=f"Mean: {mean_val:.2f}%",
        annotation_position="top"
    )

    # Update layout
    layout = get_base_layout(title)
    layout['xaxis'] = {'title': risk_col, 'gridcolor': COLORS['grid'], 'color': COLORS['text']}
    layout['yaxis'] = {'title': 'Count', 'gridcolor': COLORS['grid'], 'color': COLORS['text']}
    layout['showlegend'] = False

    fig.update_layout(layout)

    save_html_chart(fig, output_path)


def create_scatter_plot(df, x_col, y_col, output_path, title="Scatter Plot", color_col=None, hover_col='Symbol'):
    """
    Create scatter plot for two variables.

    Args:
        df (pd.DataFrame): DataFrame with data
        x_col (str): X-axis column name
        y_col (str): Y-axis column name
        output_path (str): Output HTML file path
        title (str): Chart title
        color_col (str): Optional column for color coding
        hover_col (str): Column to show in hover
    """
    if x_col not in df.columns or y_col not in df.columns:
        print(f"⚠️  Required columns not found in DataFrame")
        return

    fig = go.Figure()

    # Prepare hover text
    hover_text = df[hover_col] if hover_col in df.columns else df.index

    if color_col and color_col in df.columns:
        # Color-coded scatter
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(
                size=8,
                color=df[color_col],
                colorscale=[[0, COLORS['negative']], [0.5, COLORS['neutral']], [1, COLORS['positive']]],
                showscale=True,
                colorbar=dict(
                    title=color_col,
                    titlefont=dict(color=COLORS['text']),
                    tickfont=dict(color=COLORS['text']),
                    bgcolor=COLORS['background']
                ),
                line=dict(color=COLORS['text'], width=1)
            ),
            text=hover_text,
            hovertemplate='<b>%{text}</b><br>' + f'{x_col}: %{{x:.2f}}<br>{y_col}: %{{y:.2f}}<extra></extra>',
            name='Assets'
        ))
    else:
        # Simple scatter
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(
                size=8,
                color=COLORS['text'],
                line=dict(color=COLORS['accent'], width=1)
            ),
            text=hover_text,
            hovertemplate='<b>%{text}</b><br>' + f'{x_col}: %{{x:.2f}}<br>{y_col}: %{{y:.2f}}<extra></extra>',
            name='Assets'
        ))

    # Update layout
    layout = get_base_layout(title)
    layout['xaxis'] = {'title': x_col, 'gridcolor': COLORS['grid'], 'color': COLORS['text']}
    layout['yaxis'] = {'title': y_col, 'gridcolor': COLORS['grid'], 'color': COLORS['text']}
    layout['showlegend'] = False

    fig.update_layout(layout)

    save_html_chart(fig, output_path)


def create_top_assets_chart(df, value_col, output_path, title="Top Assets", n=20, ascending=False):
    """
    Create horizontal bar chart showing top N assets by value.

    Args:
        df (pd.DataFrame): DataFrame with data
        value_col (str): Column to sort by
        output_path (str): Output HTML file path
        title (str): Chart title
        n (int): Number of top assets to show
        ascending (bool): Sort ascending if True, descending if False
    """
    if value_col not in df.columns:
        print(f"⚠️  Column {value_col} not found in DataFrame")
        return

    # Get top N
    top_df = df.nlargest(n, value_col) if not ascending else df.nsmallest(n, value_col)

    # Determine color based on values
    colors = [COLORS['positive'] if v > 0 else COLORS['negative'] for v in top_df[value_col]]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=top_df[value_col],
        y=top_df['Symbol'] if 'Symbol' in top_df.columns else top_df.index,
        orientation='h',
        marker=dict(color=colors, line=dict(color=COLORS['text'], width=1)),
        hovertemplate='<b>%{y}</b><br>' + f'{value_col}: %{{x:.2f}}<extra></extra>',
        name='Assets'
    ))

    # Update layout
    layout = get_base_layout(title)
    layout['xaxis'] = {'title': value_col, 'gridcolor': COLORS['grid'], 'color': COLORS['text']}
    layout['yaxis'] = {'title': 'Symbol', 'gridcolor': COLORS['grid'], 'color': COLORS['text'], 'autorange': 'reversed'}
    layout['showlegend'] = False

    fig.update_layout(layout)

    save_html_chart(fig, output_path)


if __name__ == "__main__":
    print("Chart Generator Module for MarketWizardry.org")
    print("=" * 80)
    print("\nThis module provides functions to generate HTML charts with CRT aesthetic.")
    print("\nAvailable functions:")
    print("  - create_price_trend_chart()")
    print("  - create_risk_distribution_chart()")
    print("  - create_scatter_plot()")
    print("  - create_top_assets_chart()")
    print("\nAll charts use the MarketWizardry.org color scheme:")
    print(f"  Background: {COLORS['background']}")
    print(f"  Text:       {COLORS['text']}")
    print(f"  Positive:   {COLORS['positive']}")
    print(f"  Negative:   {COLORS['negative']}")
    print("=" * 80)
