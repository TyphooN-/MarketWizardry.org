#!/usr/bin/env python3
"""
Generate or update SEO components for root pages.
Adds JSON-LD structured data to pages that are missing it.
"""

import os
import re
from seo_templates import SEOManager

# Root pages that need JSON-LD with their specific configurations
ROOT_PAGES = {
    'var-explorer.html': {
        'schema_type': 'SoftwareApplication',
        'name': 'VaR Explorer - Value at Risk Calculator',
        'description': 'Professional Value at Risk (VaR) calculator and analysis tool for financial markets. Real-time risk assessment for stocks, ETFs, and trading portfolios.',
        'applicationCategory': 'FinanceApplication',
        'operatingSystem': 'Web Browser'
    },
    'atr-explorer.html': {
        'schema_type': 'SoftwareApplication',
        'name': 'ATR Explorer - Average True Range Calculator',
        'description': 'Advanced Average True Range (ATR) analysis tool for volatility measurement. Professional market analysis for traders and investors.',
        'applicationCategory': 'FinanceApplication',
        'operatingSystem': 'Web Browser'
    },
    'ev-explorer.html': {
        'schema_type': 'SoftwareApplication',
        'name': 'EV Explorer - Enterprise Value Calculator',
        'description': 'Enterprise Value (EV) calculator and analysis platform for fundamental stock analysis. Comprehensive valuation tools for equity research.',
        'applicationCategory': 'FinanceApplication',
        'operatingSystem': 'Web Browser'
    },
    'crypto-explorer.html': {
        'schema_type': 'SoftwareApplication',
        'name': 'Crypto Explorer - Cryptocurrency Analysis',
        'description': 'Cryptocurrency market analysis and tracking platform. Real-time crypto data, volatility metrics, and trading insights for digital assets.',
        'applicationCategory': 'FinanceApplication',
        'operatingSystem': 'Web Browser'
    },
    'darwinex-radar.html': {
        'schema_type': 'SoftwareApplication',
        'name': 'Darwinex RADAR - Symbol Tracker',
        'description': 'Real-time tracking of Darwinex symbol additions, delistings, close-only restrictions, and swap rate changes. Know before the notification email hits your spam folder.',
        'applicationCategory': 'FinanceApplication',
        'operatingSystem': 'Web Browser'
    },
    'blog.html': {
        'schema_type': 'Blog',
        'name': 'Market Wizardry Blog',
        'description': 'Trading insights, market analysis, and financial technology articles. Professional commentary on markets, algorithms, and trading strategies.'
    },
    'ai-musings.html': {
        'schema_type': 'Blog',
        'name': 'AI Musings - Artificial Intelligence Articles',
        'description': 'AI-generated market commentary and trading insights. Exploring the intersection of artificial intelligence and financial markets.'
    },
    'ai-art.html': {
        'schema_type': 'CreativeWork',
        'name': 'AI Art Gallery',
        'description': 'AI-generated art collection showcasing the intersection of artificial intelligence and creative expression. Digital art powered by machine learning.'
    },
    'market-wizardry.html': {
        'schema_type': 'WebSite',
        'name': 'Market Wizardry - Financial Trading Tools',
        'description': 'Professional financial trading tools, market analysis platforms, and quantitative research software. Free tools for traders and investors.'
    },
    'var-cult.html': {
        'schema_type': 'WebPage',
        'name': 'VaR Cult - Value at Risk Community',
        'description': 'Value at Risk (VaR) methodology, research, and community resources for quantitative risk management.'
    },
    'code.html': {
        'schema_type': 'SoftwareSourceCode',
        'name': 'Code & Projects',
        'description': 'Open-source trading tools, market analysis scripts, and financial software projects. Code repositories and development resources.'
    },
    'about.html': {
        'schema_type': 'AboutPage',
        'name': 'About Market Wizardry',
        'description': 'About TyphooN and MarketWizardry.org - Professional financial trading tools and market analysis platforms by an independent developer.'
    },
    '404.html': {
        'schema_type': 'WebPage',
        'name': '404 - Page Not Found',
        'description': 'Page not found on MarketWizardry.org. Navigate back to trading tools and market analysis platforms.'
    }
}


def has_jsonld(file_path):
    """Check if file already has JSON-LD schema"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return 'application/ld+json' in content or 'jsonld-' in content
    except FileNotFoundError:
        return False


def generate_jsonld_script(page_name, config):
    """Generate external JSON-LD script file for a page"""
    seo_manager = SEOManager()

    # Create schema based on type
    if config['schema_type'] == 'SoftwareApplication':
        schema = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": config['name'],
            "description": config['description'],
            "url": f"https://marketwizardry.org/{page_name}",
            "applicationCategory": config['applicationCategory'],
            "operatingSystem": config['operatingSystem'],
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
            },
            "author": {
                "@type": "Person",
                "name": "TyphooN",
                "url": "https://twitter.com/MarketW1zardry"
            }
        }
    elif config['schema_type'] == 'Blog':
        schema = {
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": config['name'],
            "description": config['description'],
            "url": f"https://marketwizardry.org/{page_name}",
            "author": {
                "@type": "Person",
                "name": "TyphooN",
                "url": "https://twitter.com/MarketW1zardry"
            },
            "publisher": {
                "@type": "Organization",
                "name": "MarketWizardry.org",
                "url": "https://marketwizardry.org"
            }
        }
    elif config['schema_type'] == 'CreativeWork':
        schema = {
            "@context": "https://schema.org",
            "@type": "CreativeWork",
            "name": config['name'],
            "description": config['description'],
            "url": f"https://marketwizardry.org/{page_name}",
            "author": {
                "@type": "Person",
                "name": "TyphooN"
            }
        }
    elif config['schema_type'] == 'SoftwareSourceCode':
        schema = {
            "@context": "https://schema.org",
            "@type": "SoftwareSourceCode",
            "name": config['name'],
            "description": config['description'],
            "url": f"https://marketwizardry.org/{page_name}",
            "author": {
                "@type": "Person",
                "name": "TyphooN",
                "url": "https://twitter.com/MarketW1zardry"
            }
        }
    elif config['schema_type'] == 'AboutPage':
        schema = {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "name": config['name'],
            "description": config['description'],
            "url": f"https://marketwizardry.org/{page_name}",
            "mainEntity": {
                "@type": "Person",
                "name": "TyphooN",
                "url": "https://twitter.com/MarketW1zardry"
            }
        }
    elif config['schema_type'] == 'WebSite':
        schema = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": config['name'],
            "description": config['description'],
            "url": f"https://marketwizardry.org/{page_name}",
            "author": {
                "@type": "Person",
                "name": "TyphooN"
            }
        }
    else:  # Default WebPage
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": config['name'],
            "description": config['description'],
            "url": f"https://marketwizardry.org/{page_name}"
        }

    # Generate external JS file
    import json
    script_name = page_name.replace('.html', '')
    schema_json = json.dumps(schema, indent=4)

    js_content = f"""// JSON-LD structured data for {page_name} - CSP compliant
(function() {{
    'use strict';

    const jsonLdData = {schema_json};

    // Inject JSON-LD into page
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(jsonLdData, null, 2);
    document.head.appendChild(script);
}})();
"""

    return script_name, js_content


def add_jsonld_to_page(page_path, script_name):
    """Add JSON-LD script reference to HTML page"""
    try:
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find </head> tag and insert script before it
        script_tag = f'    <script src="/js/jsonld-{script_name}.js"></script>'

        # Insert before </head>
        if '</head>' in content:
            content = content.replace('</head>', f'{script_tag}\n</head>', 1)

            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error updating {page_path}: {e}")
        return False


def main():
    """Main function to generate JSON-LD for root pages"""
    print("Generating JSON-LD schemas for root pages...")
    print("=" * 60)

    os.chdir('/home/typhoon/git/MarketWizardry.org')

    added_count = 0
    skipped_count = 0

    for page_name, config in ROOT_PAGES.items():
        page_path = page_name

        if not os.path.exists(page_path):
            print(f"⚠️  {page_name} - File not found, skipping")
            continue

        if has_jsonld(page_path):
            print(f"✓ {page_name} - Already has JSON-LD, skipping")
            skipped_count += 1
            continue

        # Generate JSON-LD script
        script_name, js_content = generate_jsonld_script(page_name, config)

        # Save external JS file
        js_path = f"js/jsonld-{script_name}.js"
        os.makedirs('js', exist_ok=True)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)

        # Add script reference to HTML
        if add_jsonld_to_page(page_path, script_name):
            print(f"✅ {page_name} - Added JSON-LD ({config['schema_type']})")
            added_count += 1
        else:
            print(f"❌ {page_name} - Failed to add JSON-LD")

    print("=" * 60)
    print(f"Summary: {added_count} pages updated, {skipped_count} already had JSON-LD")
    print(f"Total pages processed: {len(ROOT_PAGES)}")


if __name__ == "__main__":
    main()
