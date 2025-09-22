#!/usr/bin/env python3
"""
AI Art Gallery Generator

Automatically generates ai-art.html by scanning the ai-art/ directory for images.
This replaces the need to manually maintain the image paths in the HTML file.
"""

import os
import glob
import re
from pathlib import Path
from seo_templates import SEOManager, get_breadcrumb_paths, PAGE_CONFIGS, REDIRECT_SCRIPT_TEMPLATE

def scan_ai_art_images(ai_art_dir='ai-art'):
    """Scan the ai-art directory for webp images and return sorted paths"""
    if not os.path.exists(ai_art_dir):
        print(f"Error: {ai_art_dir} directory not found!")
        return []

    # Find all .webp files in the ai-art directory
    pattern = os.path.join(ai_art_dir, '*.webp')
    image_files = glob.glob(pattern)

    # Sort them naturally (00001.webp, 00002.webp, etc.)
    def natural_sort_key(path):
        filename = os.path.basename(path)
        # Extract numbers from filename for proper sorting
        numbers = re.findall(r'\d+', filename)
        return [int(num) for num in numbers] if numbers else [0]

    image_files.sort(key=natural_sort_key)

    # Convert to relative paths with forward slashes
    relative_paths = []
    for file_path in image_files:
        # Convert to relative path and use forward slashes
        relative_path = file_path.replace(os.sep, '/')
        if not relative_path.startswith('/'):
            relative_path = '/' + relative_path
        relative_paths.append(relative_path)

    return relative_paths

def generate_ai_art_html(output_file='ai-art.html'):
    """Generate the complete ai-art.html file"""

    # Scan for images
    image_paths = scan_ai_art_images()

    if not image_paths:
        print("No images found in ai-art directory!")
        return False

    print(f"Found {len(image_paths)} images in ai-art directory")

    # Convert paths to JavaScript array format
    js_image_paths = ',\n            '.join(f'"{path}"' for path in image_paths)

    # Initialize SEO Manager and get breadcrumbs
    seo_manager = SEOManager()
    breadcrumb_paths = get_breadcrumb_paths()
    ai_art_breadcrumbs = breadcrumb_paths['ai_art']

    # Configure page settings
    page_config = PAGE_CONFIGS['gallery'].copy()
    page_config.update({
        'title': 'MarketWizardry.org | AI Art',
        'canonical_url': 'https://marketwizardry.org/ai-art.html',
        'description': 'Robot-generated \'art\' for humans who\'ve given up on actual creativity. Watch machines mock your artistic soul while you pretend it\'s profound.',
        'og_title': 'AI Art - MarketWizardry.org',
        'og_description': 'Robot-generated \'art\' for humans who\'ve given up on actual creativity. Watch machines mock your artistic soul while you pretend it\'s profound.',
        'twitter_title': 'AI Art - MarketWizardry.org',
        'twitter_description': 'Robot-generated \'art\' for humans who\'ve given up on actual creativity. Watch machines mock your artistic soul while you pretend it\'s profound.',
        'keywords': page_config['keywords_base']
    })

    # Generate SEO components
    enhanced_meta_tags = seo_manager.generate_enhanced_meta_tags(page_config)
    breadcrumbs_html = seo_manager.generate_breadcrumbs(ai_art_breadcrumbs)
    breadcrumb_css = seo_manager.generate_breadcrumb_css()

    # HTML template
    html_template = '''<!-- ai-art.html -->
<!DOCTYPE html>
<html lang="en">
<head>
{enhanced_meta_tags}
{REDIRECT_SCRIPT_TEMPLATE}
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
        }
        a {
            color: #00ff00;
            text-decoration: none;
            font-weight: bold;
        }
        h1 {
            text-align: center;
            padding-bottom: 10px;
        }
        /* Image grid styles */
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .image-container {
            position: relative;
            width: 100%;
            max-width: 500px; /* Maximum size of the container */
            cursor: pointer;
        }
        .thumbnail {
            width: 100%;
            height: auto;
            border-radius: 5px;
            border: 2px solid rgba(0, 255, 0, 0.5);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease-in-out;
        }
        .thumbnail:hover {
            transform: scale(1.05);
            filter: brightness(1.2);
        }
        /* Modal styles */
        .modal {
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
        }
	.modal-content {
	    position: relative;
	    background-color: #000;
	    padding: 20px;
	    border: 2px solid #00ff00;
	    border-radius: 5px;
	    box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
	    text-align: center;
	    max-width: 95vw; /* Increased modal width for mobile */
	    max-height: 95vh; /* Increased modal height for mobile */
	    overflow: auto; /* Enable scrolling if content exceeds modal size */
	}
	.full-image {
	    max-width: 100%;
	    max-height: 65vh; /* Reduced to leave space for navigation buttons */
	    display: block;
	    margin: 0 auto;
	    object-fit: contain;
	}
        .crt-divider {
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 30px auto;
        }
        @keyframes scan {
            0% { opacity: 1; width: 0%; }
            50% { opacity: 0.5; }
            100% { opacity: 1; width: 100%; }
        }
        @keyframes flicker {
            0% { opacity: 1; }
            50% { opacity: 0.8; }
            100% { opacity: 1; }
        }
        .flavor-text {
            color: #00ff00;
            font-family: "Courier New", monospace;
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            font-style: italic;
            font-weight: bold;
            opacity: 0.9;
            animation: flicker 1s infinite;
        }
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
            gap: 10px;
        }
        .nav-button {
            background-color: #000;
            color: #00ff00;
            border: 2px solid #00ff00;
            padding: 10px 20px;
            cursor: pointer;
            font-family: "Courier New", monospace;
            font-size: 16px;
            border-radius: 3px;
            transition: all 0.3s ease;
            min-width: 80px;
        }
        .nav-button:hover {
            background-color: #001100;
            color: #00ff00;
        }
        .nav-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .nav-button:disabled:hover {
            background-color: #000;
        }
        .close-button {
            position: absolute;
            top: 10px;
            right: 15px;
            background: none;
            border: 2px solid #00ff00;
            color: #00ff00;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            padding: 5px 10px;
            border-radius: 3px;
        }
        .close-button:hover {
            background-color: #001100;
        }
        .filename-display {
            color: #00ff00;
            margin-bottom: 10px;
            word-wrap: break-word;
            font-size: 0.9em;
        }
        .image-counter {
            color: #00ff00;
            font-family: 'Courier New', monospace;
        }
        .download-container {
            text-align: center;
            margin-top: 10px;
        }
        .modal.modal-open {
            display: flex;
        }

{breadcrumb_css}
        /* Mobile breadcrumb optimization */
        @media screen and (max-width: 768px) {
            .breadcrumb {
                display: none;
            }
            .modal-content {
                padding: 5px;
                max-width: 98vw;
                max-height: 98vh;
            }
            .full-image {
                max-height: 55vh;
            }
            .filename-display {
                font-size: 0.7em;
                margin-bottom: 5px;
            }
            .nav-button {
                padding: 8px 15px;
                font-size: 14px;
                min-width: 60px;
            }
            .close-button {
                font-size: 18px;
                padding: 3px 8px;
                top: 5px;
                right: 10px;
            }
            .nav-buttons {
                margin-top: 5px;
                gap: 5px;
            }
        }
    </style>
</head>
<body>
{breadcrumbs_html}

    <h1>AI Art</h1>
    <div class="crt-divider"></div>
    <div class="flavor-text">Robot-generated 'art' for humans who've given up on actual creativity. Watch machines mock your artistic soul while you pretend it's profound.</div>
    <div class="crt-divider"></div>
    <div class="image-grid" id="imageGrid">
        <!-- Images will be inserted here by JavaScript -->
    </div>

    <!-- Modal -->
    <div class="modal" id="fullscreenModal">
        <div class="modal-content">
            <button class="close-button" data-action="close-modal">&times;</button>
            <div class="filename-display" id="modalFilename"></div>
            <div class="crt-divider"></div>
            <img src="" alt="Fullscreen image" class="full-image" loading="lazy">
            <div class="nav-buttons">
                <button class="nav-button" id="prevButton" data-action="previous-image">← Previous</button>
                <span id="imageCounter" class="image-counter"></span>
                <button class="nav-button" id="nextButton" data-action="next-image">Next →</button>
            </div>
            <div class="download-container">
                <button class="nav-button" id="downloadButton" data-action="download-image">⬇ Download</button>
            </div>
        </div>
    </div>

    <script>
        // Event delegation for data-action attributes
        document.addEventListener('click', function(e) {
            const action = e.target.getAttribute('data-action');
            if (action) {
                switch(action) {
                    case 'close-modal':
                        closeModal();
                        break;
                    case 'previous-image':
                        previousImage();
                        break;
                    case 'next-image':
                        nextImage();
                        break;
                    case 'download-image':
                        downloadImage();
                        break;
                }
            }
        });

        const allImagePaths = [
            {IMAGE_PATHS_PLACEHOLDER}
        ];
        console.log("Image paths loaded:", allImagePaths.length);

        let currentImageIndex = 0;

        function openImage(index) {
            currentImageIndex = index;
            const modalImg = document.querySelector('.full-image');
            const modal = document.getElementById('fullscreenModal');
            const modalFilename = document.getElementById('modalFilename');

            modalImg.src = allImagePaths[index];
            modalFilename.textContent = allImagePaths[index].split('/').pop().replace(/'/g, '');

            // Update navigation buttons and counter
            updateNavigationButtons();

            modal.classList.add('modal-open');
        }

        function updateNavigationButtons() {
            const prevButton = document.getElementById('prevButton');
            const nextButton = document.getElementById('nextButton');
            const imageCounter = document.getElementById('imageCounter');

            if (prevButton && nextButton && imageCounter) {
                prevButton.disabled = currentImageIndex <= 0;
                nextButton.disabled = currentImageIndex >= allImagePaths.length - 1;
                imageCounter.textContent = `${currentImageIndex + 1} / ${allImagePaths.length}`;
            }
        }

        function previousImage() {
            if (currentImageIndex > 0) {
                openImage(currentImageIndex - 1);
            }
        }

        function nextImage() {
            if (currentImageIndex < allImagePaths.length - 1) {
                openImage(currentImageIndex + 1);
            }
        }
        function downloadImage() {
            const currentImagePath = allImagePaths[currentImageIndex];
            if (currentImagePath) {
                const link = document.createElement('a');
                link.href = currentImagePath;
                link.download = currentImagePath.split('/').pop();
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        }

        function closeModal() {
            const modal = document.getElementById('fullscreenModal');
            modal.classList.remove('modal-open');
        }

        // Keyboard navigation
        document.addEventListener('keydown', function(event) {
            const modal = document.getElementById('fullscreenModal');
            if (modal.classList.contains('modal-open')) {
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
                        closeModal();
                        break;
                }
            }
        });

        // Click outside modal to close
        window.addEventListener('click', function(event) {
            const modal = document.getElementById('fullscreenModal');
            if (event.target === modal) {
                closeModal();
            }
        });

        // Populate image grid on load
        document.addEventListener('DOMContentLoaded', () => {
            const imageGrid = document.getElementById('imageGrid');
            allImagePaths.forEach((path, index) => {
                const imgContainer = document.createElement('div');
                imgContainer.className = 'image-container';

                const img = document.createElement('img');
                img.className = 'thumbnail';
                img.src = path;
                img.alt = `AI Art ${index + 1}`;
                img.loading = 'lazy';
                img.addEventListener('click', () => openImage(index));

                imgContainer.appendChild(img);
                imageGrid.appendChild(imgContainer);
            });
        });

        // Make functions globally accessible for backward compatibility
        window.openImage = openImage;
        window.closeModal = closeModal;
        window.previousImage = previousImage;
        window.nextImage = nextImage;
        window.downloadImage = downloadImage;
    </script>
</body>
</html>'''

    # Replace the placeholders with actual content
    final_html = html_template.replace('{enhanced_meta_tags}', enhanced_meta_tags)
    final_html = final_html.replace('{REDIRECT_SCRIPT_TEMPLATE}', REDIRECT_SCRIPT_TEMPLATE)
    final_html = final_html.replace('{breadcrumb_css}', breadcrumb_css)
    final_html = final_html.replace('{breadcrumbs_html}', breadcrumbs_html)
    final_html = final_html.replace('{IMAGE_PATHS_PLACEHOLDER}', js_image_paths)

    # Write the file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"✓ Generated {output_file} with {len(image_paths)} images")
        return True
    except Exception as e:
        print(f"Error writing {output_file}: {e}")
        return False

def main():
    """Main function"""
    print("AI Art Gallery Generator")
    print("=" * 50)

    # Generate the HTML file
    success = generate_ai_art_html()

    if success:
        print("AI Art gallery generation complete!")
    else:
        print("AI Art gallery generation failed!")

if __name__ == "__main__":
    main()