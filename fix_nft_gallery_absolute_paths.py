#!/usr/bin/env python3

import os
import re

def fix_gallery_image_paths(file_path):
    """Fix NFT gallery image paths to be absolute from web root"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find image paths in JavaScript arrays
    # Look for paths that start with 'nft-gallery/' but don't start with '/'
    pattern = re.compile(r"'(nft-gallery/[^']+)'", re.MULTILINE)
    
    def add_leading_slash(match):
        path = match.group(1)
        if not path.startswith('/'):
            return f"'/{path}'"
        return match.group(0)
    
    original_content = content
    content = pattern.sub(add_leading_slash, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Fix image paths in all NFT galleries to be absolute"""
    
    base_dir = '/home/typhoon/git/MarketWizardry.org'
    nft_gallery_dir = os.path.join(base_dir, 'nft-gallery')
    
    if not os.path.exists(nft_gallery_dir):
        print(f"NFT gallery directory not found: {nft_gallery_dir}")
        return
    
    fixed_count = 0
    total_count = 0
    
    for file in os.listdir(nft_gallery_dir):
        if file.endswith('_gallery.html'):
            file_path = os.path.join(nft_gallery_dir, file)
            total_count += 1
            
            try:
                if fix_gallery_image_paths(file_path):
                    fixed_count += 1
                    print(f"Fixed image paths in: {file}")
            except Exception as e:
                print(f"Error processing {file}: {e}")
    
    # Also check the main nft-gallery.html files
    for filename in ['nft-gallery.html', 'all.html']:
        file_path = os.path.join(nft_gallery_dir, filename)
        if os.path.exists(file_path):
            total_count += 1
            try:
                if fix_gallery_image_paths(file_path):
                    fixed_count += 1
                    print(f"Fixed image paths in: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    print(f"\nCompleted: Fixed {fixed_count} out of {total_count} gallery files")

if __name__ == "__main__":
    main()