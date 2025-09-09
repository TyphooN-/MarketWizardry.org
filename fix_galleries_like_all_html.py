#!/usr/bin/env python3

import os
import re

def convert_gallery_to_dynamic_loading(gallery_file):
    """Convert gallery to use dynamic image loading like all.html"""
    
    with open(gallery_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the image paths from the existing HTML
    img_pattern = r'<img class="thumbnail" src="([^"]*)"[^>]*onclick="openImage\((\d+)\)"[^>]*>'
    matches = re.findall(img_pattern, content)
    
    if not matches:
        print(f"No images found in {os.path.basename(gallery_file)}")
        return False
    
    # Create JavaScript array of image paths
    image_paths = [match[0] for match in matches]
    js_array = "const allImagePaths = [" + ",\\n            ".join([f"'{path}'" for path in image_paths]) + "];"
    
    # Clear the image grid HTML and make it empty like all.html
    empty_grid = '''    <!-- Image Grid -->
    <div class="image-grid" id="imageGrid">
        <!-- Images will be inserted here by JavaScript -->
    </div>'''
    
    # Replace the existing image grid with empty one
    grid_pattern = r'<!-- Image Grid -->[^<]*<div class="image-grid" id="imageGrid">.*?</div>\s*<!-- Modal -->'
    content = re.sub(grid_pattern, empty_grid + '\n    \n    <!-- Modal -->', content, flags=re.DOTALL)
    
    # Update the JavaScript section
    new_javascript = f'''    <script>
        {js_array}
        console.log("Image paths loaded:", allImagePaths.length);
        
        function loadImage(path, index) {{
            const imgContainer = document.createElement('div');
            imgContainer.className = 'image-container';
            const img = document.createElement('img');
            img.className = 'thumbnail';
            img.src = path;
            img.alt = path.split('/').pop();
            img.loading = 'lazy';
            img.onclick = function() {{ openImage(index); }};
            imgContainer.appendChild(img);
            document.getElementById('imageGrid').appendChild(imgContainer);
        }}
        
        function openImage(index) {{
            const modalImg = document.querySelector('.full-image');
            const modal = document.getElementById('fullscreenModal');
            const modalFilename = document.getElementById('modalFilename');
            
            modalImg.src = allImagePaths[index];
            modalFilename.textContent = allImagePaths[index].split('/').pop().replace(/'/g, '');
            modal.style.display = 'flex';
        }}
        
        function closeModal() {{
            const modal = document.getElementById('fullscreenModal');
            modal.style.display = 'none';
        }}
        
        // Load all images when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {{
            console.log("Loading", allImagePaths.length, "images");
            allImagePaths.forEach((path, index) => {{
                loadImage(path, index);
            }});
        }});
        
        // Keyboard navigation
        document.addEventListener('keydown', function(event) {{
            const modal = document.getElementById('fullscreenModal');
            if (modal.style.display === 'flex') {{
                if (event.key === 'Escape') {{
                    modal.style.display = 'none';
                }}
            }}
        }});
        
        // Click outside modal to close
        window.onclick = function(event) {{
            const modal = document.getElementById('fullscreenModal');
            if (event.target === modal) {{
                closeModal();
            }}
        }};
    </script>'''
    
    # Replace the existing script section
    script_pattern = r'<script>.*?</script>'
    content = re.sub(script_pattern, new_javascript, content, flags=re.DOTALL)
    
    with open(gallery_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Converted {os.path.basename(gallery_file)} to dynamic loading")
    return True

def main():
    """Convert all galleries to use dynamic loading like all.html"""
    
    gallery_dir = "/home/typhoon/git/MarketWizardry.org/nft-gallery"
    
    updated_count = 0
    total_count = 0
    
    for filename in os.listdir(gallery_dir):
        if filename.endswith("_gallery.html") and filename != "all.html":  # Skip all.html as it's working
            gallery_file = os.path.join(gallery_dir, filename)
            total_count += 1
            
            if convert_gallery_to_dynamic_loading(gallery_file):
                updated_count += 1
    
    print(f"\nCompleted: Converted {updated_count} out of {total_count} galleries to dynamic loading")

if __name__ == "__main__":
    main()