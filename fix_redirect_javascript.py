#!/usr/bin/env python3

import os
import re

def fix_redirect_javascript(file_path):
    """Fix broken redirect JavaScript in HTML files"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match broken redirect JavaScript
    broken_pattern = re.compile(
        r'(if \(window === window\.top\) \{\s*'
        r'// Small delay to ensure viewport takes effect on mobile\s*'
        r'setTimeout\(\(\) => \{\s*'
        r'const currentPath = window\.location\.pathname;\s*'
        r'if \(currentPath\.includes\(\'/blog/\'\) \|\| currentPath\.includes\(\'/nft-gallery/\'\)\) \{\s*'
        r'// For blog posts and NFT galleries, pass full path\s*'
        r'const fullPath = currentPath\.startsWith\(\'/\'\) \? currentPath\.substring\(1\) : currentPath;\s*'
        r'window\.location\.href = `\/\?page=\$\{encodeURIComponent\(fullPath\)\}`;\s*'
        r'\} else \{\s*'
        r'// For main pages, redirect with page parameter\s*'
        r'const currentPage = currentPath\.split\(\'/\'\)\.pop\(\)\.replace\(\'\.html\', \'\'\);\s*'
        r'window\.location\.href = `\/\?page=\$\{currentPage\}`;\s*'
        r'\}\s*)'
        r'(\s*</script>)',
        re.DOTALL | re.MULTILINE
    )
    
    # Correct replacement with proper closing
    correct_replacement = r'''\1            }, 100);
        }
    \2'''
    
    original_content = content
    content = broken_pattern.sub(correct_replacement, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fix redirect JavaScript across all HTML files"""
    
    base_dir = '/home/typhoon/git/MarketWizardry.org'
    
    # Find all HTML files to process
    html_files = []
    
    # Check nft-gallery directory
    nft_gallery_dir = os.path.join(base_dir, 'nft-gallery')
    if os.path.exists(nft_gallery_dir):
        for file in os.listdir(nft_gallery_dir):
            if file.endswith('.html'):
                html_files.append(os.path.join(nft_gallery_dir, file))
    
    # Check root directory for other HTML files
    for file in os.listdir(base_dir):
        if file.endswith('.html') and file != 'index.html':  # Skip index.html as it's the main page
            html_files.append(os.path.join(base_dir, file))
    
    # Check blog directory if it exists
    blog_dir = os.path.join(base_dir, 'blog')
    if os.path.exists(blog_dir):
        for file in os.listdir(blog_dir):
            if file.endswith('.html'):
                html_files.append(os.path.join(blog_dir, file))
    
    fixed_count = 0
    total_count = len(html_files)
    
    for file_path in html_files:
        try:
            if fix_redirect_javascript(file_path):
                fixed_count += 1
                print(f"Fixed redirect JavaScript in: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nCompleted: Fixed {fixed_count} out of {total_count} HTML files")

if __name__ == "__main__":
    main()