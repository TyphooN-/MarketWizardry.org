#!/usr/bin/env python3

import os
import re

def fix_modal_css_in_gallery(gallery_file):
    """Fix modal CSS display flex issue in a gallery file"""
    
    if not os.path.exists(gallery_file):
        print(f"Gallery file not found: {gallery_file}")
        return False
    
    with open(gallery_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for the modal CSS block and ensure it has proper flexbox display
    # The issue is that the modal needs to be a flex container when displayed
    
    # Find the modal CSS block
    modal_css_pattern = r'(\.modal\s*{[^}]*?)(align-items:\s*center;[^}]*?justify-content:\s*center;[^}]*?)}'
    
    match = re.search(modal_css_pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        # Check if the modal already has the proper structure
        modal_block = match.group(0)
        
        # If it doesn't have the comment that indicates it's been fixed, fix it
        if "Use flexbox for centering" not in modal_block:
            # Replace the modal CSS to ensure proper flex display
            new_modal_css = modal_block.replace(
                'z-index: 1000;\n            align-items: center;',
                'z-index: 1000;\n            /* display: flex; Use flexbox for centering */\n            align-items: center;'
            )
            
            new_content = content.replace(modal_block, new_modal_css)
            
            if new_content != content:
                with open(gallery_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed modal CSS in {os.path.basename(gallery_file)}")
                return True
            else:
                print(f"No changes needed for {os.path.basename(gallery_file)}")
                return False
        else:
            print(f"Already fixed: {os.path.basename(gallery_file)}")
            return False
    else:
        print(f"No modal CSS found in {os.path.basename(gallery_file)}")
        return False

def main():
    """Fix modal CSS across all gallery files"""
    
    gallery_dir = "/home/typhoon/git/MarketWizardry.org/nft-gallery"
    
    updated_count = 0
    total_count = 0
    
    for filename in os.listdir(gallery_dir):
        if filename.endswith("_gallery.html"):
            gallery_file = os.path.join(gallery_dir, filename)
            total_count += 1
            
            if fix_modal_css_in_gallery(gallery_file):
                updated_count += 1
    
    print(f"\nCompleted: Fixed modal CSS in {updated_count} out of {total_count} galleries")

if __name__ == "__main__":
    main()