#!/usr/bin/env python3

import os
import re
import glob

def fix_javascript_properly(file_path):
    """Properly fix all JavaScript syntax errors"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the redirect script structure - this is the main problem
        redirect_pattern = r'(// Redirect to index\.html if accessed directly.*?if \(window === window\.top\) \{.*?setTimeout\(\(\) => \{)(.*?)(}, 100\);\s*})'
        
        def fix_redirect(match):
            prefix = match.group(1)
            body = match.group(2)
            suffix = match.group(3)
            
            # Clean up the redirect body
            body = re.sub(r'\s*const currentPath.*?window\.location\.pathname;', '\n                const currentPath = window.location.pathname;', body, flags=re.DOTALL)
            body = re.sub(r'\s*if \(currentPath\.includes.*?\} else \{.*?window\.location\.href = `[^`]+`;\s*}.*?}, 100\);\s*.*?}, 100\);', 
                         '''
                if (currentPath.includes('/blog/') || currentPath.includes('/nft-gallery/')) {
                    // For blog posts and NFT galleries, pass full path
                    const fullPath = currentPath.startsWith('/') ? currentPath.substring(1) : currentPath;
                    window.location.href = `/?page=${encodeURIComponent(fullPath)}`;
                } else {
                    // For main pages, redirect with page parameter
                    const currentPage = currentPath.split('/').pop().replace('.html', '');
                    window.location.href = `/?page=${currentPage}`;
                }''', body, flags=re.DOTALL)
            
            return prefix + body + '\n            ' + suffix
        
        content = re.sub(redirect_pattern, fix_redirect, content, flags=re.DOTALL)
        
        # Fix gallery JavaScript event listeners
        content = re.sub(
            r'(document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{.*?loadMoreImages\(\);.*?if \(document\.body\.offsetHeight < window\.innerHeight\) \{.*?loadMoreImages\(\);.*?), 100\)\s*;\s*\}\);',
            r'\1\n            }\n        }, 100);\n        });',
            content,
            flags=re.DOTALL
        )
        
        content = re.sub(
            r'(window\.addEventListener\(\'scroll\', \(\) => \{.*?if \(window\.innerHeight.*?loadMoreImages\(\);.*?), 100\)\s*;\s*\}\);',
            r'\1\n        }\n        }, 100);\n        });',
            content,
            flags=re.DOTALL
        )
        
        # Fix function definitions that got broken
        content = re.sub(
            r'(function (?:previousImage|nextImage)\(\) \{.*?openImage\(currentImageIndex\);)\s*}, 100\)\s*;',
            r'\1\n        }',
            content,
            flags=re.DOTALL
        )
        
        # Fix keydown event handlers
        content = re.sub(
            r'(document\.addEventListener\(\'keydown\'.*?break;\s*}\s*), 100\)\s*;\s*\}\);',
            r'\1\n            }\n        }, 100);\n        });',
            content,
            flags=re.DOTALL
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    # Get all HTML files
    html_files = glob.glob("**/*.html", recursive=True)
    
    fixed_count = 0
    
    for file_path in html_files:
        if os.path.isfile(file_path):
            try:
                # Check if file contains JavaScript with potential issues
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '<script>' in content and ('setTimeout' in content or 'addEventListener' in content):
                    if fix_javascript_properly(file_path):
                        print(f"Fixed JavaScript in: {file_path}")
                        fixed_count += 1
                        
            except Exception as e:
                print(f"Error checking {file_path}: {e}")
    
    print(f"\nFixed JavaScript properly in {fixed_count} files")

if __name__ == "__main__":
    main()