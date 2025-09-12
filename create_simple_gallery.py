#!/usr/bin/env python3

import os
import glob

def create_simple_gallery(artist_name):
    """Create a simple gallery without lazy loading"""
    
    # Get all webp files for the artist
    webp_pattern = f"/home/typhoon/git/MarketWizardry.org/nft-gallery/{artist_name}/webp/*.webp"
    webp_files = glob.glob(webp_pattern)
    webp_files.sort()
    
    if not webp_files:
        print(f"No webp files found for {artist_name}")
        return
    
    # Get existing flavor text if available
    existing_file = f"/home/typhoon/git/MarketWizardry.org/nft-gallery/{artist_name}_gallery.html"
    flavor_text = f"{artist_name}'s digital art collection"
    
    if os.path.exists(existing_file):
        with open(existing_file, 'r') as f:
            content = f.read()
            # Extract existing flavor text
            if 'flavor-text">' in content:
                start = content.find('flavor-text">') + len('flavor-text">')
                end = content.find('</div>', start)
                if start > 0 and end > start:
                    flavor_text = content[start:end].strip()
    
    # Generate image HTML directly
    image_html = ""
    for i, webp_file in enumerate(webp_files):
        filename = os.path.basename(webp_file)
        image_path = f"/nft-gallery/{artist_name}/webp/{filename}"
        
        image_html += f'''        <div class="image-container">
            <img class="thumbnail" src="{image_path}" alt="{filename}" onclick="openImage({i})" loading="lazy">
        </div>
'''
    
    # Create image paths array for modal
    image_paths = []
    for webp_file in webp_files:
        filename = os.path.basename(webp_file)
        image_paths.append(f"'/nft-gallery/{artist_name}/webp/{filename}'")
    
    image_paths_str = ',\n            '.join(image_paths)
    
    html_template = f'''<!-- Simple gallery.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>MarketWizardry.org | NFT (Not For Trade) Gallery - {artist_name}</title>
    <link rel="canonical" href="https://marketwizardry.org/nft-gallery/{artist_name}_gallery.html">
    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">
    <meta charset="UTF-8">
    <meta name="author" content="TyphooN">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{flavor_text}">
    <meta property="og:title" content="NFT Gallery - {artist_name}">
    <meta property="og:description" content="{flavor_text}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://marketwizardry.org/nft-gallery/{artist_name}_gallery.html">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="NFT Gallery - {artist_name}">
    <meta name="twitter:description" content="{flavor_text}">
    <script>
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
    </script>
    <style>
        body {{
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
        }}
        a {{
            color: #00ff00;
            text-decoration: none;
            font-weight: bold;
        }}
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .image-container {{
            position: relative;
            width: 100%;
            max-width: 500px;
            cursor: pointer;
        }}
        .thumbnail {{
            width: 100%;
            height: auto;
            border-radius: 5px;
            border: 2px solid rgba(0, 255, 0, 0.5);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease-in-out;
        }}
        .thumbnail:hover {{
            transform: scale(1.05);
            filter: brightness(1.2);
        }}
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }}
        .modal-content {{
            position: relative;
            background-color: #000;
            padding: 20px;
            border: 2px solid #00ff00;
            border-radius: 5px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            text-align: center;
            max-width: 90vw;
            max-height: 90vh;
            overflow: auto;
        }}
        .full-image {{
            max-width: 100%;
            max-height: 80vh;
            display: block;
            margin: 0 auto;
            object-fit: contain;
        }}
        .crt-divider {{
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 10px 0;
        }}
        @keyframes scan {{
            0% {{ opacity: 1; width: 0%; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; width: 100%; }}
        }}
        .filename-display {{
            color: #00ff00;
            margin-bottom: 10px;
            word-wrap: break-word;
        }}
        .flavor-text {{
            color: #00ff00;
            font-family: "Courier New", monospace;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            font-style: italic;
            font-weight: bold;
            opacity: 0.9;
            animation: flicker 1s infinite;
        }}
        @keyframes flicker {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 1; }}
        }}
    </style>
    <meta property="og:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <meta property="og:image:alt" content="MarketWizardry.org - Financial Trading Tools">
</head>
<body>
    <h2>NFT (Not For Trade) Gallery - {artist_name}</h2>
    <div class="crt-divider"></div>

    <div class="flavor-text">{flavor_text}</div>

    <div class="crt-divider"></div>

    <!-- Image Grid -->
    <div class="image-grid" id="imageGrid">
{image_html}    </div>
    
    <!-- Modal -->
    <div class="modal" id="fullscreenModal" onclick="closeModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="filename-display" id="modalFilename"></div>
            <div class="crt-divider"></div>
            <img src="" alt="Fullscreen image" class="full-image" loading="lazy">
        </div>
    </div>

    <script>
        const allImagePaths = [{image_paths_str}];
        console.log("Image paths loaded:", allImagePaths.length);
        
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
    </script>
</body>
</html>'''
    
    # Write the file
    output_file = f"/home/typhoon/git/MarketWizardry.org/nft-gallery/{artist_name}_gallery.html"
    with open(output_file, 'w') as f:
        f.write(html_template)
    
    print(f"Created simple gallery for {artist_name} with {len(webp_files)} images")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    # Test with natived_
    create_simple_gallery("natived_")