#!/usr/bin/env python3

import os
import re

def add_keyboard_navigation_to_gallery(gallery_file):
    """Add full keyboard navigation like all.html to individual galleries"""
    
    with open(gallery_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if keyboard navigation is already complete
    if 'previousImage()' in content and 'ArrowLeft' in content:
        print(f"Keyboard navigation already complete in {os.path.basename(gallery_file)}")
        return False
    
    # Add currentImageIndex variable and update openImage function
    if 'let currentImageIndex = 0;' not in content:
        # Add currentImageIndex variable after allImagePaths
        pattern = r'(const allImagePaths = \[.*?\];)'
        replacement = r'\1\n        let currentImageIndex = 0;'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Update openImage function to track currentImageIndex
    old_open_function = r'function openImage\(index\) \{([^}]*?modal\.style\.display = \'flex\';\s*)'
    new_open_function = r'''function openImage(index) {
            currentImageIndex = index;
            const modalImg = document.querySelector('.full-image');
            const modal = document.getElementById('fullscreenModal');
            const modalFilename = document.getElementById('modalFilename');
            
            modalImg.src = allImagePaths[index];
            modalFilename.textContent = allImagePaths[index].split('/').pop().replace(/'/g, '');
            modal.style.display = 'flex';
        '''
    
    content = re.sub(old_open_function, new_open_function, content, flags=re.DOTALL)
    
    # Add previousImage and nextImage functions after openImage function
    navigation_functions = '''
        function previousImage() {
            if (currentImageIndex > 0) {
                currentImageIndex--;
                openImage(currentImageIndex);
            }
        }
        
        function nextImage() {
            if (currentImageIndex < allImagePaths.length - 1) {
                currentImageIndex++;
                openImage(currentImageIndex);
            }
        }'''
    
    # Insert navigation functions before closeModal function
    pattern = r'(\s+function closeModal\(\))'
    replacement = navigation_functions + r'\1'
    content = re.sub(pattern, replacement, content)
    
    # Update closeModal function to match all.html
    old_close_function = r'function closeModal\(\) \{\s*const modal = document\.getElementById\(\'fullscreenModal\'\);\s*modal\.style\.display = \'none\';\s*\}'
    new_close_function = '''function closeModal() {
            const modal = document.getElementById('fullscreenModal');
            if (modal.style.display === 'flex') {
                modal.style.display = 'none';
            }
        }'''
    
    content = re.sub(old_close_function, new_close_function, content, flags=re.DOTALL)
    
    # Update keyboard navigation to include arrow keys
    old_keyboard = r'// Keyboard navigation\s*document\.addEventListener\(\'keydown\', function\(event\) \{[^}]*?if \(event\.key === \'Escape\'\) \{[^}]*?\}\s*\}\s*\}\);'
    new_keyboard = '''// Keyboard navigation
        document.addEventListener('keydown', function(event) {
            const modal = document.getElementById('fullscreenModal');
            if (modal.style.display === 'flex') {
                switch(event.key) {
                    case 'ArrowLeft':
                        previousImage();
                        event.preventDefault();
                        break;
                    case 'ArrowRight':
                        nextImage();
                        event.preventDefault();
                        break;
                    case 'Escape':
                        modal.style.display = 'none';
                        break;
                }
            }
        });'''
    
    content = re.sub(old_keyboard, new_keyboard, content, flags=re.DOTALL)
    
    # Update window.onclick to match all.html
    old_onclick = r'// Click outside modal to close\s*window\.onclick = function\(event\) \{[^}]*?closeModal\(\);\s*\}\s*\};'
    new_onclick = '''// Click outside modal to close
        window.onclick = function(event) {
            const modal = document.getElementById('fullscreenModal');
            if (event.target === modal) {
                closeModal();
            }
        };'''
    
    content = re.sub(old_onclick, new_onclick, content, flags=re.DOTALL)
    
    with open(gallery_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Added full keyboard navigation to {os.path.basename(gallery_file)}")
    return True

def main():
    """Add keyboard navigation to all individual galleries"""
    
    gallery_dir = "/home/typhoon/git/MarketWizardry.org/nft-gallery"
    
    updated_count = 0
    total_count = 0
    
    for filename in os.listdir(gallery_dir):
        if filename.endswith("_gallery.html") and filename != "all.html":  # Skip all.html
            gallery_file = os.path.join(gallery_dir, filename)
            total_count += 1
            
            if add_keyboard_navigation_to_gallery(gallery_file):
                updated_count += 1
    
    print(f"\nCompleted: Added keyboard navigation to {updated_count} out of {total_count} galleries")

if __name__ == "__main__":
    main()