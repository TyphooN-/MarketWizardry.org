#!/usr/bin/env python3
"""
MarketWizardry.org SEO Templates & Breadcrumb System
Centralized SEO management for consistent implementation across all generators
"""

from datetime import datetime
import json

class SEOManager:
    """Centralized SEO management for MarketWizardry.org"""

    def __init__(self):
        self.base_url = "https://marketwizardry.org"
        self.site_name = "Market Wizardry"
        self.twitter_handle = "@MarketW1zardry"
        self.author = "TyphooN"
        self.default_image = f"{self.base_url}/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp"
        self.favicon = "/img/favicon.ico"
        self.apple_icon = "/img/apple-touch-icon.png"

    def generate_enhanced_meta_tags(self, page_config):
        """Generate enhanced meta tags for any page with CSP compliant scripts"""
        return f'''    <meta charset="UTF-8">
    <meta name="author" content="{self.author}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_config['title']}</title>
    <link rel="canonical" href="{page_config['canonical_url']}">
    <link rel="icon" type="image/x-icon" href="{self.favicon}">
    <link rel="apple-touch-icon" sizes="180x180" href="{self.apple_icon}">

    <!-- Enhanced Standard Meta Tags -->
    <meta name="description" content="{page_config['description']}">
    <meta name="keywords" content="{page_config.get('keywords', '')}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="language" content="en-US">
    <meta name="revisit-after" content="7 days">
    <meta name="distribution" content="global">
    <meta name="rating" content="general">
    <meta name="theme-color" content="#00ff00">

    <!-- Enhanced Open Graph Meta Tags -->
    <meta property="og:title" content="{page_config['og_title']}">
    <meta property="og:description" content="{page_config['og_description']}">
    <meta property="og:url" content="{page_config['canonical_url']}">
    <meta property="og:type" content="{page_config.get('og_type', 'website')}">
    <meta property="og:site_name" content="{self.site_name}">
    <meta property="og:image" content="{page_config.get('og_image', self.default_image)}">
    <meta property="og:image:alt" content="{page_config.get('og_image_alt', 'MarketWizardry.org - Professional Financial Trading Tools')}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="en_US">
    {self._generate_og_article_tags(page_config) if page_config.get('is_article') else ''}

    <!-- Enhanced Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_config['twitter_title']}">
    <meta name="twitter:description" content="{page_config['twitter_description']}">
    <meta name="twitter:site" content="{self.twitter_handle}">
    <meta name="twitter:creator" content="{self.twitter_handle}">
    <meta name="twitter:image" content="{page_config.get('twitter_image', self.default_image)}">
    <meta name="twitter:image:alt" content="{page_config.get('twitter_image_alt', 'MarketWizardry.org Financial Tools')}">
    <meta name="twitter:domain" content="marketwizardry.org">
    {self._generate_twitter_labels(page_config)}

    <!-- CSP Compliant JavaScript Includes -->
    <script src="/js/redirect.js"></script>
    <script src="/js/shared.js"></script>'''

    def _generate_og_article_tags(self, page_config):
        """Generate Open Graph article-specific tags"""
        tags = f'''    <meta property="article:author" content="{self.author}">
    <meta property="article:section" content="{page_config.get('section', 'Finance')}">'''

        if page_config.get('article_tags'):
            for tag in page_config['article_tags']:
                tags += f'\n    <meta property="article:tag" content="{tag}">'

        if page_config.get('published_time'):
            tags += f'\n    <meta property="article:published_time" content="{page_config['published_time']}">'

        return tags

    def _generate_twitter_labels(self, page_config):
        """Generate Twitter Card custom labels"""
        labels = ""
        if page_config.get('twitter_label1'):
            labels += f'''    <meta name="twitter:label1" content="{page_config['twitter_label1']}">
    <meta name="twitter:data1" content="{page_config['twitter_data1']}">'''

        if page_config.get('twitter_label2'):
            labels += f'''    <meta name="twitter:label2" content="{page_config['twitter_label2']}">
    <meta name="twitter:data2" content="{page_config['twitter_data2']}">'''

        return labels

    def generate_breadcrumbs(self, breadcrumb_path):
        """Generate Schema.org compliant breadcrumb navigation

        Args:
            breadcrumb_path: List of dicts with 'name' and 'url' keys
            Example: [
                {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
                {'name': '📊 Blog', 'url': 'blog.html'},
                {'name': 'VaR Analysis', 'url': None}  # Current page
            ]
        """
        if not breadcrumb_path or len(breadcrumb_path) < 2:
            return ""

        breadcrumb_html = '''    <!-- Enhanced Breadcrumb Navigation with Schema Markup -->
    <nav class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">'''

        for i, crumb in enumerate(breadcrumb_path, 1):
            if crumb.get('url'):  # Not current page
                breadcrumb_html += f'''
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a href="{crumb['url']}" itemprop="item">
                <span itemprop="name">{crumb['name']}</span>
            </a>
            <meta itemprop="position" content="{i}" />
        </span>'''
            else:  # Current page
                breadcrumb_html += f'''
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <span itemprop="name">{crumb['name']}</span>
            <meta itemprop="position" content="{i}" />
        </span>'''

            # Add separator except for last item
            if i < len(breadcrumb_path):
                breadcrumb_html += '\n        <span class="separator">→</span>'

        breadcrumb_html += '''
    </nav>'''

        return breadcrumb_html

    def generate_json_ld_schema(self, schema_config, page_filename=None):
        """Generate CSP-compliant JSON-LD structured data via external script"""
        base_schema = {
            "@context": "https://schema.org",
            "@type": schema_config['type'],
            "name": schema_config['name'],
            "url": schema_config['url'],
            "description": schema_config['description'],
            "author": {
                "@type": "Person",
                "name": self.author
            },
            "publisher": {
                "@type": "Organization",
                "name": self.site_name,
                "url": self.base_url,
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{self.base_url}{self.apple_icon}"
                }
            },
            "inLanguage": "en-US"
        }

        # Merge additional schema properties
        if schema_config.get('additional_properties'):
            base_schema.update(schema_config['additional_properties'])

        # Generate external JSON-LD file for CSP compliance
        if page_filename:
            jsonld_filename = f"js/jsonld-{page_filename.replace('.html', '').replace('/', '-')}.js"
            self._generate_external_jsonld_file(base_schema, jsonld_filename)
            return f'    <!-- Enhanced JSON-LD Schema Markup - loaded via external script -->\n    <script src="/{jsonld_filename}"></script>'
        else:
            # Fallback to inline for backward compatibility (will cause CSP issues)
            return f'''    <!-- Enhanced JSON-LD Schema Markup -->
    <script type="application/ld+json">
    {json.dumps(base_schema, indent=4)}
    </script>'''

    def _generate_external_jsonld_file(self, schema_data, filename):
        """Generate external JavaScript file with JSON-LD data"""
        js_content = f'''// JSON-LD structured data - CSP compliant
(function() {{
    'use strict';

    const jsonLdData = {json.dumps(schema_data, indent=4)};

    function injectJsonLd() {{
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(jsonLdData);
        document.head.appendChild(script);
        console.log('JSON-LD structured data injected');
    }}

    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', injectJsonLd);
    }} else {{
        injectJsonLd();
    }}
}})();'''

        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(js_content)
            print(f"✓ Generated {filename}")
        except Exception as e:
            print(f"Error writing {filename}: {e}")

    def get_blog_post_jsonld_config(self, post_title, post_url, post_description, published_date=None):
        """Generate JSON-LD configuration for blog posts"""
        return {
            'type': ['BlogPosting', 'Article'],
            'name': post_title,
            'url': post_url,
            'description': post_description,
            'additional_properties': {
                'headline': post_title,
                'datePublished': published_date or datetime.now().strftime('%Y-%m-%d'),
                'dateModified': datetime.now().strftime('%Y-%m-%d'),
                'articleBody': post_description,
                'keywords': 'financial analysis, market data, trading insights, VaR analysis, risk management',
                'articleSection': 'Financial Analysis',
                'mainEntityOfPage': {
                    '@type': 'WebPage',
                    '@id': post_url
                }
            }
        }

    def get_gallery_jsonld_config(self, gallery_title, gallery_url, gallery_description, artist_name=None):
        """Generate JSON-LD configuration for NFT galleries"""
        config = {
            'type': ['Collection', 'CreativeWork'],
            'name': gallery_title,
            'url': gallery_url,
            'description': gallery_description,
            'additional_properties': {
                'collectionSize': 'Variable',
                'genre': 'Digital Art',
                'artMedium': 'Digital',
                'keywords': 'AI art, NFT gallery, digital art, generative art, creative technology'
            }
        }

        if artist_name:
            config['additional_properties']['creator'] = {
                '@type': 'Person',
                'name': artist_name
            }

        return config

    def get_web_application_jsonld_config(self, app_title, app_url, app_description, category="Finance"):
        """Generate JSON-LD configuration for web applications (explorers, calculators)"""
        return {
            'type': 'WebApplication',
            'name': app_title,
            'url': app_url,
            'description': app_description,
            'additional_properties': {
                'applicationCategory': category,
                'operatingSystem': 'Any',
                'browserRequirements': 'Requires JavaScript',
                'offers': {
                    '@type': 'Offer',
                    'price': '0',
                    'priceCurrency': 'USD'
                },
                'featureList': app_description
            }
        }

    def get_about_page_jsonld_config(self, person_name, person_url, person_description):
        """Generate JSON-LD configuration for about/profile pages"""
        return {
            'type': 'Person',
            'name': person_name,
            'url': person_url,
            'description': person_description,
            'additional_properties': {
                'jobTitle': 'Trader & Developer',
                'knowsAbout': ['Financial Markets', 'Algorithmic Trading', 'Risk Management', 'Market Analysis'],
                'sameAs': [
                    'https://twitter.com/MarketW1zardry'
                ]
            }
        }

    def get_image_gallery_jsonld_config(self, gallery_title, gallery_url, gallery_description):
        """Generate JSON-LD configuration for image galleries"""
        return {
            'type': 'ImageGallery',
            'name': gallery_title,
            'url': gallery_url,
            'description': gallery_description,
            'additional_properties': {
                'genre': 'Digital Art',
                'artform': 'AI Generated Art'
            }
        }

    def get_item_list_jsonld_config(self, list_title, list_url, list_description, items=None):
        """Generate JSON-LD configuration for item lists (affiliates, resources)"""
        config = {
            'type': 'ItemList',
            'name': list_title,
            'url': list_url,
            'description': list_description,
            'additional_properties': {
                'numberOfItems': len(items) if items else 0
            }
        }

        if items:
            config['additional_properties']['itemListElement'] = [
                {
                    '@type': 'ListItem',
                    'position': idx + 1,
                    'name': item['name'],
                    'url': item.get('url', '')
                } for idx, item in enumerate(items)
            ]

        return config

    def get_software_application_jsonld_config(self, app_title, app_url, app_description):
        """Generate JSON-LD configuration for software/code pages"""
        return {
            'type': 'SoftwareApplication',
            'name': app_title,
            'url': app_url,
            'description': app_description,
            'additional_properties': {
                'applicationCategory': 'DeveloperApplication',
                'operatingSystem': 'Any',
                'offers': {
                    '@type': 'Offer',
                    'price': '0',
                    'priceCurrency': 'USD'
                }
            }
        }

    def generate_breadcrumb_css(self):
        """Generate CSS for breadcrumb styling - matches var-cult.html standard"""
        return '''
    /* Breadcrumb Navigation Styles */
    .breadcrumb {
        font-size: 0.8em;
        color: #00aa00;
        margin-bottom: 20px;
        padding: 10px 0;
    }

    .breadcrumb a {
        color: #00ff00 !important;
        text-decoration: none;
        transition: all 0.2s ease;
    }

    .breadcrumb a:hover {
        color: #ffffff !important;
    }

    .breadcrumb .separator {
        margin: 0 8px;
        color: #004400;
    }

    /* Mobile breadcrumb optimization */
    @media screen and (max-width: 768px) {
        .breadcrumb {
            display: none;
        }
    }'''

# Page-specific configurations
PAGE_CONFIGS = {
    'blog_post': {
        'keywords_base': 'financial analysis, market data, trading insights, VaR analysis, risk management, market outliers, trading strategy',
        'og_type': 'article',
        'is_article': True,
        'section': 'Financial Analysis',
        'article_tags': ['Finance', 'Trading', 'Market Analysis', 'Risk Management'],
        'twitter_label1': 'Category',
        'twitter_data1': 'Financial Analysis',
        'twitter_label2': 'Reading Time',
        'twitter_data2': '3-5 min'
    },
    'calculator': {
        'keywords_base': 'financial calculator, risk calculator, trading tools, position sizing, VaR calculator, stop loss calculator',
        'twitter_label1': 'Tools',
        'twitter_data1': '5 Calculators',
        'twitter_label2': 'Price',
        'twitter_data2': 'Free'
    },
    'explorer': {
        'keywords_base': 'market explorer, financial data, volatility analysis, risk metrics, trading data, market analysis tools',
        'twitter_label1': 'Data Points',
        'twitter_data1': '900+ Symbols',
        'twitter_label2': 'Updates',
        'twitter_data2': 'Daily'
    },
    'gallery': {
        'keywords_base': 'AI art, NFT gallery, digital art, generative art, creative technology',
        'twitter_label1': 'Category',
        'twitter_data1': 'Digital Art',
        'twitter_label2': 'Collection',
        'twitter_data2': 'Growing'
    },
    'about': {
        'keywords_base': 'about MarketWizardry, financial trading platform, risk management tools, market analysis',
        'twitter_label1': 'Type',
        'twitter_data1': 'About Page',
        'twitter_label2': 'Focus',
        'twitter_data2': 'Financial Tools'
    },
    'affiliates': {
        'keywords_base': 'affiliate program, trading partnerships, financial services, market tools affiliate',
        'twitter_label1': 'Program',
        'twitter_data1': 'Affiliates',
        'twitter_label2': 'Benefits',
        'twitter_data2': 'Competitive'
    },
    'donate': {
        'keywords_base': 'support MarketWizardry, donate, fund development, trading tools support',
        'twitter_label1': 'Purpose',
        'twitter_data1': 'Support',
        'twitter_label2': 'Goal',
        'twitter_data2': 'Development'
    },
    'code': {
        'keywords_base': 'open source, trading code, financial algorithms, market analysis source code',
        'twitter_label1': 'License',
        'twitter_data1': 'Open Source',
        'twitter_label2': 'Language',
        'twitter_data2': 'Python/JS'
    },
    'var_cult': {
        'keywords_base': 'VaR cult, value at risk community, risk management philosophy, trading mindset',
        'twitter_label1': 'Community',
        'twitter_data1': 'VaR Cult',
        'twitter_label2': 'Focus',
        'twitter_data2': 'Risk Management'
    }
}

def get_breadcrumb_paths():
    """Define standard breadcrumb paths for the site"""
    return {
        'home': [{'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'}],
        'blog': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '📊 Blog', 'url': 'blog.html'}
        ],
        'calculator': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': 'Calculator Suite', 'url': 'calculator.html'}
        ],
        'var_explorer': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '🎯 VaR Explorer', 'url': 'var-explorer.html'}
        ],
        'atr_explorer': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '📈 ATR Explorer', 'url': 'atr-explorer.html'}
        ],
        'ev_explorer': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '💼 EV Explorer', 'url': 'ev-explorer.html'}
        ],
        'gallery': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '🎨 NFT Gallery', 'url': 'nft-gallery.html'}
        ],
        'about': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': 'ℹ️ About', 'url': 'about.html'}
        ],
        'affiliates': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '🤝 Affiliates', 'url': 'affiliates.html'}
        ],
        'donate': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '💰 Donate', 'url': 'donate.html'}
        ],
        'code': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '💻 Code', 'url': 'code.html'}
        ],
        'var_cult': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '🔮 VaR Cult', 'url': 'var-cult.html'}
        ],
        'blog': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '📊 Blog', 'url': 'blog.html'}
        ],
        'terms': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '📜 Terms', 'url': 'terms.html'}
        ],
        'ai_art': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '🎨 AI Art', 'url': 'ai-art.html'}
        ],
        'ai_musings': [
            {'name': '🏠 Market Wizardry', 'url': 'market-wizardry.html'},
            {'name': '🤖 AI Musings', 'url': 'ai-musings.html'}
        ]
    }

# Redirect script template (for iframe handling)
REDIRECT_SCRIPT_TEMPLATE = '''    <script src="/js/redirect.js"></script>'''