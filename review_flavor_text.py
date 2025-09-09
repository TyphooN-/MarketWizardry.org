
import os
import re

def review_flavor_text():
    gallery_dir = 'nft-gallery'
    files = [f for f in os.listdir(gallery_dir) if f.endswith('_gallery.html')]

    for file in files:
        filepath = os.path.join(gallery_dir, file)
        
        with open(filepath, 'r') as f:
            content = f.read()

        match = re.search(r'<div class="flavor-text">(.*?)</div>', content)
        if match:
            flavor_text = match.group(1)
            print(f"--- {file} ---")
            print(flavor_text)
            print("\n")

if __name__ == '__main__':
    review_flavor_text()
