#!/usr/bin/env python3
"""
Add CRT dividers underneath breadcrumb navigation in all HTML files
"""

import os
import glob
import re

def add_breadcrumb_divider(file_path):
    """Add CRT divider underneath breadcrumb navigation"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file has breadcrumb nav
        if '<nav class="breadcrumb"' not in content:
            return False

        original_content = content

        # Pattern to find the closing </nav> tag of breadcrumb
        breadcrumb_pattern = r'(<nav class="breadcrumb"[^>]*>.*?</nav>)'

        # Check if divider already exists after breadcrumb
        divider_check = r'</nav>\s*<div class="crt-divider"></div>'
        if re.search(divider_check, content, flags=re.DOTALL):
            return False  # Divider already exists

        # Find and replace breadcrumb nav with nav + divider
        def add_divider(match):
            nav_content = match.group(1)
            return nav_content + '\n    <div class="crt-divider"></div>'

        updated_content = re.sub(breadcrumb_pattern, add_divider, content, flags=re.DOTALL)

        if updated_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            print(f"✅ Added CRT divider to {file_path}")
            return True

        return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Add CRT dividers to all files with breadcrumb navigation"""
    print("🔧 Adding CRT dividers underneath breadcrumbs...")

    # Find all HTML files
    html_files = []
    for pattern in ['*.html', 'blog/*.html', 'nft-gallery/*.html']:
        html_files.extend(glob.glob(pattern))

    updated_files = 0
    total_files = 0

    for html_file in html_files:
        if os.path.isfile(html_file):
            total_files += 1
            if add_breadcrumb_divider(html_file):
                updated_files += 1

    print(f"\n📊 Summary:")
    print(f"   Total HTML files: {total_files}")
    print(f"   Files updated: {updated_files}")
    print(f"   Files unchanged: {total_files - updated_files}")

    print(f"\n✅ CRT divider addition complete!")
    print(f"   All breadcrumbs now have CRT dividers underneath")

if __name__ == "__main__":
    main()