#!/usr/bin/env python3

import os
import re

def fix_python_redirect_template(file_path):
    """Fix broken redirect JavaScript templates in Python files"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match broken redirect JavaScript templates in Python strings
    # This handles both single {{ and double {{{{ bracket scenarios
    broken_patterns = [
        # Pattern 1: Basic broken redirect (from generate_gallery.py style)
        re.compile(
            r'(<script>\s*'
            r'// Redirect to index\.html if accessed directly \(not in iframe\)\s*'
            r'if \(window === window\.top\) \{\s*'
            r'const currentPath = window\.location\.pathname;\s*'
            r'if \(currentPath\.includes\(\'/blog/\'\) \|\| currentPath\.includes\(\'/nft-gallery/\'\)\) \{\s*'
            r'// For blog posts and NFT galleries.*?\s*'
            r'const fullPath = currentPath\.startsWith\(\'/\'\) \? currentPath\.substring\(1\) : currentPath;\s*'
            r'window\.location\.href = `\/\?page=\$\{[^}]+\}`;\s*'
            r'\} else \{\s*'
            r'// For main pages, redirect with page parameter\s*'
            r'const currentPage = currentPath\.split\(\'/\'\)\.pop\(\)\.replace\(\'\.html\', \'\'\);\s*'
            r'window\.location\.href = `\/\?page=\$\{[^}]+\}`;\s*'
            r'\}\s*'
            r'\}\s*'
            r'</script>)',
            re.DOTALL | re.MULTILINE
        ),
        # Pattern 2: Python template format with double braces {{
        re.compile(
            r'(<script>\s*'
            r'// Redirect to index\.html if accessed directly \(not in iframe\)\s*'
            r'if \(window === window\.top\) \{\{\s*'
            r'const currentPath = window\.location\.pathname;\s*'
            r'if \(currentPath\.includes\(\'/blog/\'\) \|\| currentPath\.includes\(\'/nft-gallery/\'\)\) \{\{\s*'
            r'// For blog posts and NFT galleries.*?\s*'
            r'const fullPath = currentPath\.startsWith\(\'/\'\) \? currentPath\.substring\(1\) : currentPath;\s*'
            r'window\.location\.href = `\/\?page=\$\{\{[^}]+\}\}`;\s*'
            r'\}\} else \{\{\s*'
            r'// For main pages, redirect with page parameter\s*'
            r'const currentPage = currentPath\.split\(\'/\'\)\.pop\(\)\.replace\(\'\.html\', \'\'\);\s*'
            r'window\.location\.href = `\/\?page=\$\{\{[^}]+\}\}`;\s*'
            r'\}\}\s*'
            r'\}\}\s*'
            r'</script>)',
            re.DOTALL | re.MULTILINE
        )
    ]
    
    # Determine if this is a double-brace template format
    uses_double_braces = '{{' in content and 'encodeURIComponent(fullPath)}}' in content
    
    # Correct replacement with proper closing - adjust braces based on file format
    if uses_double_braces:
        correct_replacement = '''<script>
        // Set viewport immediately for mobile scaling
        if (!document.querySelector('meta[name="viewport"]')) {{
            const viewport = document.createElement('meta');
            viewport.name = 'viewport';
            viewport.content = 'width=device-width, initial-scale=1.0';
            document.head.insertBefore(viewport, document.head.firstChild);
        }}
        
        // Redirect to index.html if accessed directly (not in iframe)
        if (window === window.top) {{
            // Small delay to ensure viewport takes effect on mobile
            setTimeout(() => {{
                const currentPath = window.location.pathname;
                if (currentPath.includes('/blog/') || currentPath.includes('/nft-gallery/')) {{
                    // For blog posts and NFT galleries, pass full path
                    const fullPath = currentPath.startsWith('/') ? currentPath.substring(1) : currentPath;
                    window.location.href = `/?page=${{encodeURIComponent(fullPath)}}`;
                }} else {{
                    // For main pages, redirect with page parameter
                    const currentPage = currentPath.split('/').pop().replace('.html', '');
                    window.location.href = `/?page=${{currentPage}}`;
                }}
            }}, 100);
        }}
    </script>'''
    else:
        correct_replacement = '''<script>
        // Set viewport immediately for mobile scaling
        if (!document.querySelector('meta[name="viewport"]')) {
            const viewport = document.createElement('meta');
            viewport.name = 'viewport';
            viewport.content = 'width=device-width, initial-scale=1.0';
            document.head.insertBefore(viewport, document.head.firstChild);
        }
        
        // Redirect to index.html if accessed directly (not in iframe)
        if (window === window.top) {
            // Small delay to ensure viewport takes effect on mobile
            setTimeout(() => {
                const currentPath = window.location.pathname;
                if (currentPath.includes('/blog/') || currentPath.includes('/nft-gallery/')) {
                    // For blog posts and NFT galleries, pass full path
                    const fullPath = currentPath.startsWith('/') ? currentPath.substring(1) : currentPath;
                    window.location.href = `/?page=${encodeURIComponent(fullPath)}`;
                } else {
                    // For main pages, redirect with page parameter
                    const currentPage = currentPath.split('/').pop().replace('.html', '');
                    window.location.href = `/?page=${currentPage}`;
                }
            }, 100);
        }
    </script>'''
    
    original_content = content
    
    # Try to apply fixes with each pattern
    for pattern in broken_patterns:
        content = pattern.sub(correct_replacement, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fix redirect JavaScript templates in Python scripts"""
    
    base_dir = '/home/typhoon/git/MarketWizardry.org'
    
    # Find all Python files that might contain redirect templates
    python_files = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                # Check if file contains redirect JavaScript
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'window === window.top' in content:
                            python_files.append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    fixed_count = 0
    total_count = len(python_files)
    
    for file_path in python_files:
        try:
            if fix_python_redirect_template(file_path):
                fixed_count += 1
                print(f"Fixed redirect JavaScript template in: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nCompleted: Fixed {fixed_count} out of {total_count} Python files")

if __name__ == "__main__":
    main()