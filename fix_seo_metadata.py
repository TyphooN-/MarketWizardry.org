#!/usr/bin/env python3
"""
Script to add missing SEO metadata to HTML files
"""
import os
import re
from pathlib import Path

# Default Open Graph image
DEFAULT_OG_IMAGE = "https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp"

def add_canonical_and_og_image(html_file):
    """Add canonical URL and Open Graph image to HTML file if missing"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if file doesn't have proper HTML structure
        if '<head>' not in content:
            return False
            
        # Determine canonical URL based on file path
        file_path = Path(html_file)
        if file_path.name == 'index.html':
            canonical_url = "https://marketwizardry.org/"
        elif file_path.parent.name == 'blog':
            canonical_url = f"https://marketwizardry.org/blog/{file_path.name}"
        elif file_path.parent.name == 'nft-gallery':
            canonical_url = f"https://marketwizardry.org/nft-gallery/{file_path.name}"
        else:
            canonical_url = f"https://marketwizardry.org/{file_path.name}"
        
        # Check what's missing
        needs_canonical = 'rel="canonical"' not in content
        needs_og_image = 'property="og:image"' not in content
        needs_favicon = 'rel="icon"' not in content and file_path.name != 'index.html'
        
        if not (needs_canonical or needs_og_image or needs_favicon):
            return False  # Nothing to add
        
        # Find insertion point after <title> tag
        title_pattern = r'(<title>.*?</title>)'
        title_match = re.search(title_pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not title_match:
            return False  # No title tag found
        
        # Build additions
        additions = []
        
        if needs_canonical:
            additions.append(f'    <link rel="canonical" href="{canonical_url}">')
        
        if needs_favicon:
            additions.extend([
                '    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">',
                '    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">'
            ])
        
        # Insert after title tag
        insert_text = '\n' + '\n'.join(additions)
        new_content = content.replace(title_match.group(1), title_match.group(1) + insert_text)
        
        # Add Open Graph image if missing (after og:site_name or before Twitter cards)
        if needs_og_image:
            # Find insertion point for OG image
            og_site_pattern = r'(<meta property="og:site_name"[^>]*>)'
            twitter_pattern = r'(<!-- Twitter Card Meta Tags -->)'
            
            og_image_html = f'    <meta property="og:image" content="{DEFAULT_OG_IMAGE}">\n    <meta property="og:image:alt" content="MarketWizardry.org - Financial Trading Tools">'
            
            if re.search(og_site_pattern, new_content):
                new_content = re.sub(og_site_pattern, f'\\1\n{og_image_html}', new_content)
            elif re.search(twitter_pattern, new_content):
                new_content = re.sub(twitter_pattern, f'{og_image_html}\n    \\1', new_content)
            else:
                # Add before closing head tag as fallback
                new_content = new_content.replace('</head>', f'    {og_image_html}\n</head>')
        
        # Write updated content
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Updated: {html_file}")
        return True
        
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return False

def main():
    """Process all HTML files"""
    processed = 0
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip .git and other hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html') and not file.startswith('google-site-verification'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files to process")
    
    for html_file in html_files:
        if add_canonical_and_og_image(html_file):
            processed += 1
    
    print(f"Successfully updated {processed} files")

if __name__ == "__main__":
    main()