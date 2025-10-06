#!/usr/bin/env python3
"""
Generate or update SEO JSON-LD Article schema for blog posts.
Automatically extracts metadata from existing blog HTML files.
"""

import os
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup


def extract_blog_metadata(html_path):
    """Extract metadata from existing blog post HTML"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Extract from meta tags
        title_tag = soup.find('meta', property='og:title')
        title = title_tag['content'] if title_tag else soup.find('title').text

        desc_tag = soup.find('meta', {'name': 'description'})
        description = desc_tag['content'] if desc_tag else ''

        published_tag = soup.find('meta', property='article:published_time')
        published = published_tag['content'] if published_tag else datetime.now().isoformat()

        canonical_tag = soup.find('link', rel='canonical')
        url = canonical_tag['href'] if canonical_tag else ''

        # Extract keywords
        keywords_tag = soup.find('meta', {'name': 'keywords'})
        keywords = keywords_tag['content'].split(', ') if keywords_tag else []

        return {
            'title': title.replace(' - MarketWizardry.org', ''),
            'description': description,
            'datePublished': published,
            'url': url,
            'keywords': keywords
        }
    except Exception as e:
        print(f"Error extracting metadata from {html_path}: {e}")
        return None


def has_jsonld(file_path):
    """Check if file already has JSON-LD schema"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return 'application/ld+json' in content or 'jsonld-blog-' in content
    except FileNotFoundError:
        return False


def generate_article_schema(metadata):
    """Generate Article JSON-LD schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": metadata['title'],
        "description": metadata['description'],
        "url": metadata['url'],
        "datePublished": metadata['datePublished'],
        "dateModified": metadata['datePublished'],  # Use same as published unless we track mods
        "author": {
            "@type": "Person",
            "name": "TyphooN",
            "url": "https://twitter.com/MarketW1zardry"
        },
        "publisher": {
            "@type": "Organization",
            "name": "MarketWizardry.org",
            "url": "https://marketwizardry.org",
            "logo": {
                "@type": "ImageObject",
                "url": "https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp"
            }
        },
        "articleSection": "Financial Analysis",
        "keywords": metadata['keywords']
    }

    return schema


def generate_jsonld_script(file_name, schema):
    """Generate external JSON-LD script content"""
    schema_json = json.dumps(schema, indent=4)

    js_content = f"""// JSON-LD structured data for {file_name} - CSP compliant
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

    return js_content


def add_jsonld_to_page(page_path, script_name):
    """Add JSON-LD script reference to HTML page"""
    try:
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find </head> tag and insert script before it
        script_tag = f'    <script src="/js/jsonld-blog-{script_name}.js"></script>'

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
    """Main function to generate JSON-LD for blog posts"""
    print("Generating Article JSON-LD schemas for blog posts...")
    print("=" * 60)

    os.chdir('/home/typhoon/git/MarketWizardry.org')

    blog_dir = 'blog'
    if not os.path.exists(blog_dir):
        print(f"Blog directory not found: {blog_dir}")
        return

    # Find all blog HTML files
    blog_files = [f for f in os.listdir(blog_dir) if f.endswith('.html')]

    added_count = 0
    skipped_count = 0
    error_count = 0

    for blog_file in sorted(blog_files):
        blog_path = os.path.join(blog_dir, blog_file)

        if has_jsonld(blog_path):
            print(f"✓ {blog_file} - Already has JSON-LD, skipping")
            skipped_count += 1
            continue

        # Extract metadata from existing HTML
        metadata = extract_blog_metadata(blog_path)
        if not metadata:
            print(f"❌ {blog_file} - Failed to extract metadata")
            error_count += 1
            continue

        # Generate Article schema
        schema = generate_article_schema(metadata)

        # Generate external JS file
        script_name = blog_file.replace('.html', '')
        js_content = generate_jsonld_script(blog_file, schema)

        # Save external JS file
        js_path = f"js/jsonld-blog-{script_name}.js"
        os.makedirs('js', exist_ok=True)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)

        # Add script reference to HTML
        if add_jsonld_to_page(blog_path, script_name):
            print(f"✅ {blog_file} - Added Article schema")
            added_count += 1
        else:
            print(f"❌ {blog_file} - Failed to add JSON-LD")
            error_count += 1

    print("=" * 60)
    print(f"Summary: {added_count} blog posts updated, {skipped_count} already had JSON-LD, {error_count} errors")
    print(f"Total blog posts processed: {len(blog_files)}")


if __name__ == "__main__":
    main()
