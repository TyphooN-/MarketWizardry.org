#!/usr/bin/env python3
"""
Generate Darwinex RADAR HTML page from symbol tracking data.
Displays symbol changes in the MarketWizardry.org terminal aesthetic.
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from seo_templates import SEOManager, PAGE_CONFIGS


def generate_radar_html():
    """Generate the main Darwinex RADAR HTML page with embedded symbol change data"""

    seo_manager = SEOManager()

    # Read the four RADAR reports
    reports = {}
    radar_dir = os.path.dirname(__file__)

    for report_type in ['stocks', 'futures', 'cfd', 'crypto']:
        report_path = os.path.join(radar_dir, f'{report_type}-radar.txt')
        if os.path.exists(report_path):
            with open(report_path, 'r', encoding='utf-8') as f:
                reports[report_type] = f.read()

    if not reports:
        print("⚠️  No RADAR reports found")
        return False

    # SEO configuration
    page_config = PAGE_CONFIGS['explorer'].copy()
    page_config.update({
        'title': 'Darwinex RADAR - Symbol Tracker | MarketWizardry.org',
        'canonical_url': 'https://marketwizardry.org/darwinex-radar.html',
        'description': 'Track Darwinex symbol additions, delistings, and market changes over time. Comprehensive historical analysis of new instruments and removed symbols.',
        'og_title': 'Darwinex RADAR - Symbol Tracker',
        'og_description': 'Track Darwinex symbol additions, delistings, and market changes over time. Comprehensive historical analysis of new instruments and removed symbols.',
        'twitter_title': 'Darwinex RADAR - Symbol Tracker',
        'twitter_description': 'Track Darwinex symbol additions, delistings, and market changes over time. Comprehensive historical analysis of new instruments and removed symbols.',
        'keywords': 'Darwinex, symbol tracker, market changes, symbol additions, delistings, market evolution, trading instruments'
    })

    meta_tags = seo_manager.generate_enhanced_meta_tags(page_config)

    breadcrumb_list = [
        {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
        {'name': '🎯 Darwinex RADAR', 'url': None}
    ]
    breadcrumbs = seo_manager.generate_breadcrumbs(breadcrumb_list)

    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{meta_tags}
    <link rel="stylesheet" href="/css/shared-styles.css">
</head>
<body>
{breadcrumbs}

    <div class="container">
        <h1>🎯 DARWINEX RADAR - SYMBOL TRACKER</h1>

        <div class="intro-section">
            <p>Real-time tracking of Darwinex symbol additions, delistings, and market evolution.</p>
            <p>📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="report-tabs">
            <button class="tab-button active" data-tab="stocks">📈 Stocks/ETF</button>
            <button class="tab-button" data-tab="futures">📊 Futures</button>
            <button class="tab-button" data-tab="cfd">💹 CFD</button>
            <button class="tab-button" data-tab="crypto">₿ Crypto</button>
        </div>

        <div id="stocks" class="tab-content active">
            <pre class="terminal-output">{reports.get('stocks', 'No data available')}</pre>
        </div>

        <div id="futures" class="tab-content">
            <pre class="terminal-output">{reports.get('futures', 'No data available')}</pre>
        </div>

        <div id="cfd" class="tab-content">
            <pre class="terminal-output">{reports.get('cfd', 'No data available')}</pre>
        </div>

        <div id="crypto" class="tab-content">
            <pre class="terminal-output">{reports.get('crypto', 'No data available')}</pre>
        </div>

        <div class="navigation-links">
            <p><a href="market-wizardry.html">← Back to Market Wizardry</a></p>
        </div>
    </div>

    <script src="/js/darwinex-radar.js"></script>
</body>
</html>'''

    # Write HTML file
    output_path = os.path.join(os.path.dirname(radar_dir), 'darwinex-radar.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Darwinex RADAR HTML generated: {output_path}")
    return True


if __name__ == "__main__":
    generate_radar_html()
