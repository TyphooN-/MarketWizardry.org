#!/usr/bin/env python3

import os
import re
import glob

def fix_nft_gallery_paths(gallery_html_path):
    """Fix NFT gallery paths to work correctly in iframe context"""
    try:
        # Extract artist name from filename
        filename = os.path.basename(gallery_html_path)
        artist_name = filename.replace('_gallery.html', '')
        
        # Check if corresponding image directory exists
        image_dir = f"nft-gallery/{artist_name}/webp"
        if not os.path.exists(image_dir):
            print(f"Warning: Image directory not found: {image_dir}")
            return False
            
        # Get all actual webp images in the directory
        actual_images = []
        webp_files = glob.glob(f"{image_dir}/*.webp")
        
        for webp_file in sorted(webp_files):
            # Convert to path relative to website root (not gallery file)
            rel_path = f"nft-gallery/{artist_name}/webp/" + os.path.basename(webp_file)
            actual_images.append(rel_path)
        
        if not actual_images:
            print(f"Warning: No webp images found in {image_dir}")
            return False
            
        print(f"Found {len(actual_images)} images for {artist_name}")
        
        # Read the HTML file
        with open(gallery_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the allImagePaths array and replace it
        # Look for the pattern: const allImagePaths = ['...', '...'];
        pattern = r"const allImagePaths = \[(.*?)\]; // All image paths from Python"
        
        # Create the new image paths string
        formatted_paths = []
        for img_path in actual_images:
            formatted_paths.append(f"'{img_path}'")
        
        new_paths_str = ',\n            '.join(formatted_paths)
        replacement = f"const allImagePaths = [{new_paths_str}]; // All image paths from Python"
        
        # Replace the old array with the new one
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if new_content != content:
            # Write the updated content back
            with open(gallery_html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {gallery_html_path} with absolute paths for {len(actual_images)} images")
            return True
        else:
            print(f"No changes needed for {gallery_html_path}")
            return False
            
    except Exception as e:
        print(f"Error processing {gallery_html_path}: {e}")
        return False

def main():
    """Fix all NFT galleries with absolute paths"""
    gallery_files = glob.glob("nft-gallery/*_gallery.html")
    fixed_count = 0
    
    print(f"Found {len(gallery_files)} gallery HTML files to process")
    print("Converting relative paths to absolute paths for iframe compatibility...")
    
    for gallery_file in sorted(gallery_files):
        if fix_nft_gallery_paths(gallery_file):
            fixed_count += 1
    
    print(f"\nSuccessfully updated {fixed_count} NFT galleries with absolute paths")

if __name__ == "__main__":
    main()