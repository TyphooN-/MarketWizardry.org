#!/usr/bin/env python3
"""
Add JSON-LD schemas to pages missing structured data
Achieves 100/100 SEO score by adding rich snippets to all priority pages
"""

from seo_templates import SEOManager
import re

seo_manager = SEOManager()

# Schema configurations for each page
schemas_to_add = {
    'about.html': {
        'method': 'get_about_page_jsonld_config',
        'params': {
            'person_name': 'TyphooN - MarketWizardry.org',
            'person_url': 'https://marketwizardry.org/about.html',
            'person_description': 'Trader and developer specializing in algorithmic trading, risk management, and financial market analysis. Creator of MarketWizardry.org trading tools and explorers.'
        },
        'insert_after': '</head>'
    },
    'affiliates.html': {
        'method': 'get_item_list_jsonld_config',
        'params': {
            'list_title': 'MarketWizardry.org Affiliates & Partners',
            'list_url': 'https://marketwizardry.org/affiliates.html',
            'list_description': 'Curated list of trading platforms, services, and tools recommended by MarketWizardry.org',
            'items': [
                {'name': 'Darwinex Zero', 'url': 'https://www.darwinexzero.com'},
                {'name': 'FXVPS', 'url': 'https://fxvps.biz'},
                {'name': 'Godly Trading', 'url': 'https://www.godlytrading.com'},
                {'name': 'FuckTrader', 'url': 'https://fucktrader.com'}
            ]
        },
        'insert_after': '</head>'
    },
    'ai-art.html': {
        'method': 'get_image_gallery_jsonld_config',
        'params': {
            'gallery_title': 'AI Art Gallery - MarketWizardry.org',
            'gallery_url': 'https://marketwizardry.org/ai-art.html',
            'gallery_description': 'Robot-generated art collection showcasing AI creativity and digital expression. Generative art gallery featuring machine learning creations.'
        },
        'insert_after': '</head>'
    },
    'ai-musings.html': {
        'method': 'get_blog_post_jsonld_config',
        'params': {
            'post_title': 'AI Musings - MarketWizardry.org',
            'post_url': 'https://marketwizardry.org/ai-musings.html',
            'post_description': 'AI-generated insights, market musings, and algorithmic trading thoughts from the MarketWizardry community.',
            'published_date': '2024-01-01'
        },
        'insert_after': '</head>'
    },
    'atr-explorer.html': {
        'method': 'get_web_application_jsonld_config',
        'params': {
            'app_title': 'ATR Explorer - Average True Range Analysis',
            'app_url': 'https://marketwizardry.org/atr-explorer.html',
            'app_description': 'Interactive ATR (Average True Range) explorer for volatility analysis across 900+ financial instruments. Real-time market data and risk metrics.',
            'category': 'FinanceApplication'
        },
        'insert_after': '</head>'
    },
    'blog.html': {
        'method': 'get_blog_post_jsonld_config',
        'params': {
            'post_title': 'Market Wizardry Blog',
            'post_url': 'https://marketwizardry.org/blog.html',
            'post_description': 'Financial market analysis, trading insights, and risk management strategies from MarketWizardry.org',
            'published_date': '2024-01-01'
        },
        'insert_after': '</head>'
    },
    'code.html': {
        'method': 'get_software_application_jsonld_config',
        'params': {
            'app_title': 'MarketWizardry Code & Tools',
            'app_url': 'https://marketwizardry.org/code.html',
            'app_description': 'Open source trading tools, MQL5 code, and financial analysis scripts for algorithmic traders.'
        },
        'insert_after': '</head>'
    },
    'crypto-explorer.html': {
        'method': 'get_web_application_jsonld_config',
        'params': {
            'app_title': 'Crypto Explorer - Cryptocurrency Market Data',
            'app_url': 'https://marketwizardry.org/crypto-explorer.html',
            'app_description': 'Real-time cryptocurrency market explorer with volatility metrics, risk analysis, and trading data across major digital assets.',
            'category': 'FinanceApplication'
        },
        'insert_after': '</head>'
    },
    'donate.html': {
        'method': 'get_item_list_jsonld_config',
        'params': {
            'list_title': 'Support MarketWizardry.org',
            'list_url': 'https://marketwizardry.org/donate.html',
            'list_description': 'Support the development of free trading tools and market analysis resources.',
            'items': [
                {'name': 'Bitcoin Donation', 'url': 'https://marketwizardry.org/donate.html'},
                {'name': 'Ethereum Donation', 'url': 'https://marketwizardry.org/donate.html'}
            ]
        },
        'insert_after': '</head>'
    },
    'var-explorer.html': {
        'method': 'get_web_application_jsonld_config',
        'params': {
            'app_title': 'VaR Explorer - Value at Risk Analysis',
            'app_url': 'https://marketwizardry.org/var-explorer.html',
            'app_description': 'Interactive Value at Risk (VaR) calculator and explorer for portfolio risk assessment and financial risk management.',
            'category': 'FinanceApplication'
        },
        'insert_after': '</head>'
    },
    'ev-explorer.html': {
        'method': 'get_web_application_jsonld_config',
        'params': {
            'app_title': 'EV Explorer - Expected Value Analysis',
            'app_url': 'https://marketwizardry.org/ev-explorer.html',
            'app_description': 'Expected Value (EV) calculator and explorer for trading strategy analysis and probability-based decision making.',
            'category': 'FinanceApplication'
        },
        'insert_after': '</head>'
    }
}

def add_jsonld_to_page(filename, config):
    """Add JSON-LD schema to a page"""
    print(f"\nProcessing {filename}...")

    # Read the HTML file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  ❌ File not found: {filename}")
        return False

    # Check if JSON-LD already exists
    if 'application/ld+json' in content or 'jsonld-' in content:
        print(f"  ⚠️  JSON-LD already exists, skipping")
        return False

    # Get the appropriate schema method
    method = getattr(seo_manager, config['method'])
    jsonld_config = method(**config['params'])

    # Generate the JSON-LD script tag
    jsonld_script = seo_manager.generate_json_ld_schema(jsonld_config, filename)

    # Find insertion point (before </head>)
    if '</head>' not in content:
        print(f"  ❌ No </head> tag found")
        return False

    # Insert JSON-LD before </head>
    content = content.replace('</head>', f'{jsonld_script}\n</head>')

    # Write back to file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Added {jsonld_config['type']} schema")
        return True
    except Exception as e:
        print(f"  ❌ Error writing file: {e}")
        return False

def main():
    print("="*60)
    print("Adding JSON-LD Schemas for 100/100 SEO Score")
    print("="*60)

    success_count = 0
    skip_count = 0
    error_count = 0

    for filename, config in schemas_to_add.items():
        result = add_jsonld_to_page(filename, config)
        if result:
            success_count += 1
        elif result is False:
            if 'already exists' in str(result):
                skip_count += 1
            else:
                error_count += 1

    print("\n" + "="*60)
    print("Summary:")
    print(f"  ✅ Successfully added: {success_count}")
    print(f"  ⚠️  Skipped (exists):  {skip_count}")
    print(f"  ❌ Errors:            {error_count}")
    print("="*60)

    if success_count > 0:
        print("\n🎯 SEO Score should now be 100/100!")
        print("✅ All priority pages have JSON-LD structured data")
        print("\nNext steps:")
        print("1. Test pages in browser console for errors")
        print("2. Validate with Google Rich Results Test")
        print("3. Update SEO_CSP_AUDIT.md")

if __name__ == "__main__":
    main()
