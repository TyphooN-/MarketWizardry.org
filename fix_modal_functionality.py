#!/usr/bin/env python3

import os
import re

def fix_modal_functionality_in_gallery(gallery_file):
    """Fix modal functionality to match the working all.html implementation"""
    
    if not os.path.exists(gallery_file):
        print(f"Gallery file not found: {gallery_file}")
        return False
    
    with open(gallery_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = False
    
    # 1. Fix the modal CSS to properly use flexbox when displayed
    # Find the modal CSS section and ensure it has the same structure as all.html
    modal_css_pattern = r'(\.modal\s*{[^}]*?align-items:\s*center;[^}]*?justify-content:\s*center;[^}]*?})'
    
    match = re.search(modal_css_pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        old_modal_css = match.group(0)
        # Replace with the working CSS structure from all.html
        new_modal_css = """.modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
            z-index: 1000;
            /* display: flex; Use flexbox for centering */
            align-items: center; /* Center vertically */
            justify-content: center; /* Center horizontally */
        }"""
        
        content = content.replace(old_modal_css, new_modal_css)
        changes_made = True
    
    # 2. Fix the closeModal function to match the working version
    close_modal_pattern = r'function closeModal\(\)\s*{[^}]*?modal\.style\.display\s*=\s*[\'"]none[\'"];[^}]*?}'
    
    match = re.search(close_modal_pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        old_close_function = match.group(0)
        # Replace with the working close function that checks for flex
        new_close_function = """function closeModal() {
            const modal = document.getElementById('fullscreenModal');
            if (modal.style.display === 'flex') {
                modal.style.display = 'none';
            }
        }"""
        
        content = content.replace(old_close_function, new_close_function)
        changes_made = True
    
    # 3. Improve the window.onclick handler to match the working version
    window_onclick_pattern = r'window\.onclick\s*=\s*function\([^)]*\)\s*{[^}]*?closeModal\(\);[^}]*?};'
    
    match = re.search(window_onclick_pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        old_onclick = match.group(0)
        # Replace with the improved onclick handler
        new_onclick = """window.onclick = function(event) {
            const modal = document.getElementById('fullscreenModal');
            if (event.target === modal) {
                closeModal();
            }
        };"""
        
        content = content.replace(old_onclick, new_onclick)
        changes_made = True
    
    if changes_made:
        with open(gallery_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed modal functionality in {os.path.basename(gallery_file)}")
        return True
    else:
        print(f"No modal functionality changes needed for {os.path.basename(gallery_file)}")
        return False

def main():
    """Fix modal functionality across all gallery files"""
    
    gallery_dir = "/home/typhoon/git/MarketWizardry.org/nft-gallery"
    
    updated_count = 0
    total_count = 0
    
    for filename in os.listdir(gallery_dir):
        if filename.endswith("_gallery.html") and filename != "all.html":  # Skip all.html as it's working
            gallery_file = os.path.join(gallery_dir, filename)
            total_count += 1
            
            if fix_modal_functionality_in_gallery(gallery_file):
                updated_count += 1
    
    print(f"\nCompleted: Fixed modal functionality in {updated_count} out of {total_count} individual galleries")

if __name__ == "__main__":
    main()