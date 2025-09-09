#!/usr/bin/env python3

import os

def add_debug_to_gallery(gallery_file):
    """Add debugging to see if onclick handlers are working"""
    
    with open(gallery_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add debug script right after the openImage function
    debug_script = '''
        // Debug: Test if functions are available
        console.log("openImage function available:", typeof openImage);
        console.log("closeModal function available:", typeof closeModal);
        
        // Debug: Add click listeners directly to images as backup
        document.addEventListener('DOMContentLoaded', function() {
            console.log("DOM loaded, attempting to add click listeners...");
            const thumbnails = document.querySelectorAll('.thumbnail');
            console.log("Found thumbnails:", thumbnails.length);
            
            thumbnails.forEach((img, index) => {
                console.log(`Adding listener to image ${index}`);
                img.addEventListener('click', function() {
                    console.log(`Clicked image ${index}`);
                    openImage(index);
                });
            });
        });'''
    
    # Insert debug script after the openImage function definition
    pattern = r'(function openImage\(index\) \{[^}]*?\})'
    
    import re
    match = re.search(pattern, content, re.DOTALL)
    if match:
        function_def = match.group(1)
        new_content = content.replace(function_def, function_def + debug_script)
        
        with open(gallery_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Added debugging to {os.path.basename(gallery_file)}")
        return True
    else:
        print(f"Could not find openImage function in {os.path.basename(gallery_file)}")
        return False

def main():
    """Add debugging to a test gallery"""
    test_gallery = "/home/typhoon/git/MarketWizardry.org/nft-gallery/0xDither_gallery.html"
    add_debug_to_gallery(test_gallery)

if __name__ == "__main__":
    main()