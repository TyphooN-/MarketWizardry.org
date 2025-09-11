import os
import fnmatch
import random
import re

def extract_tweet_info(filename):
    """Extract username and tweet ID from filename format: username-tweetid-description"""
    try:
        # Remove file extension
        base_name = os.path.splitext(filename)[0]
        # Remove -lossy suffix if present
        base_name = base_name.replace('-lossy', '')
        
        # Split by dash and extract first two parts
        parts = base_name.split('-')
        if len(parts) >= 2:
            username = parts[0]
            tweet_id = parts[1]
            # Verify tweet_id is numeric
            if tweet_id.isdigit():
                # Check if tweet ID is likely shortened (modern Twitter IDs are 19 digits)
                if len(tweet_id) < 15:
                    print(f"Warning: Tweet ID {tweet_id} appears to be shortened (only {len(tweet_id)} digits)")
                    return username, tweet_id, True  # Return flag indicating shortened ID
                return username, tweet_id, False  # Full-length ID
    except Exception as e:
        print(f"Error extracting tweet info from {filename}: {e}")
    
    return None, None, False

def generate_twitter_url(username, tweet_id, is_shortened=False):
    """Generate Twitter URL from username and tweet ID"""
    if username and tweet_id and not is_shortened:
        return f"https://twitter.com/{username}/status/{tweet_id}"
    return None

def get_existing_flavor_text(username):
    """Extract existing flavor text from the user's gallery HTML file meta description"""
    gallery_file = f"{username}_gallery.html"
    if os.path.exists(gallery_file):
        try:
            with open(gallery_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for meta description content
                import re
                match = re.search(r'<meta name="description" content="([^"]+)"', content)
                if match:
                    return match.group(1)
        except Exception as e:
            print(f"Error reading existing flavor text for {username}: {e}")
    
    # Fallback if no existing flavor text found
    return f"{username}'s digital art collection - NFT gallery showcasing blockchain-validated creative expressions."

def generate_nft_gallery_html(output_file='nft-gallery.html', valid_user_names=[]):
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MarketWizardry.org | NFT Gallery</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script>
        // Redirect to index.html if accessed directly (not in iframe)
        if (window === window.top) {
            const currentPath = window.location.pathname;
            if (currentPath.includes('/blog/') || currentPath.includes('/nft-gallery/')) {
                // For blog posts and NFT galleries, redirect to the actual file
                const fullPath = currentPath.startsWith('/') ? currentPath.substring(1) : currentPath;
                window.location.href = `/?page=${{encodeURIComponent(fullPath)}}`;
            } else {
                // For main pages, redirect with page parameter
                const currentPage = currentPath.split('/').pop().replace('.html', '');
                window.location.href = `/?page=${currentPage}`;
            }
        }
    </script>
    <style>
        body {
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            border-bottom: 2px solid rgba(0, 255, 0, 0.5);
            padding-bottom: 10px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .file-entry {
            background-color: #000;
            border: 2px solid rgba(0, 255, 0, 0.5);
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .file-entry:hover {
            background-color: #001100;
            color: #00ff00;
        }

        a {
            color: #00ff00;
            text-decoration: none;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }
        a:hover {
            text-decoration: underline;
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
        }
        .crt-divider {
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 10px 0;
        }
        @keyframes scan {
            0% { opacity: 1; width: 0%; }
            50% { opacity: 0.5; }
            100% { opacity: 1; width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>NFT (Not For Trade) Gallery</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Digital receipts for GIFs that'll survive longer than your retirement fund. Witness the intersection of art and financial delusion.</div>
        <div class="crt-divider"></div>
        <div class="grid">
            <div class="file-entry">
                <a href="nft-gallery/all.html">ALL USERS - WARNING, may cause lag!</a>
            </div>
            USER_LINKS_PLACEHOLDER
        </div>
    </div>
</body>
</html>
"""

    user_links = []
    for user in valid_user_names:
        user_gallery_file = f'{user}_gallery.html'
        if os.path.exists(user_gallery_file):
            user_links.append(f'<div class="file-entry"><a href="{user_gallery_file}">{user}</a></div>')
    
    user_links_str = '\n'.join(user_links)
    final_html = html_content.replace("USER_LINKS_PLACEHOLDER", user_links_str)

    with open(output_file, 'w') as f:
        f.write(final_html)
    print(f"Generated {output_file} with {len(user_links)} user links.")

def generate_user_gallery_html(username, output_file, search_pattern='*lossy*.webp'):
    html_template = """
<!-- user_gallery.html -->
<!DOCTYPE html>
<html>
<head>
    <title>MarketWizardry.org | NFT Gallery - USERNAME_PLACEHOLDER</title>
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
	    max-width: 90vw; /* Limit modal width */
	    max-height: 90vh; /* Limit modal height */
	    overflow: auto; /* Enable scrolling if content exceeds modal size */
	}
	.full-image {
	    max-width: 100%;
	    max-height: 80vh; /* Adjust as needed to leave space for filename */
	    display: block;
	    margin: 0 auto;
	    object-fit: contain;
	}
        .crt-divider {
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 10px 0;
        }
        @keyframes scan {
            0% { opacity: 1; width: 0%; }
            50% { opacity: 0.5; }
            100% { opacity: 1; width: 100%; }
        }
        .filename-display {
            color: #00ff00;
            margin-bottom: 10px;
            word-wrap: break-word;
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
        }
    </style>
</head>
<body>
    <h2>NFT Gallery - USERNAME_PLACEHOLDER</h2>
    <div class="crt-divider"></div>
    <div class="flavor-text">FLAVOR_TEXT_PLACEHOLDER</div>
    <div class="crt-divider"></div>
    <!-- Image Grid -->
    <div class="image-grid" id="imageGrid">
        <!-- Images will be inserted here by JavaScript -->
    </div>
    <!-- Modal -->
    <div class="modal" id="fullscreenModal" onclick="closeModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="filename-display" id="modalFilename"></div>
            <div class="twitter-link-container" id="twitterLinkContainer" style="display: none; text-align: center; margin: 10px 0;">
                <a id="twitterLink" href="#" target="_blank" rel="noopener noreferrer" style="color: #00ff00; text-decoration: none; font-weight: bold; border: 1px solid #00ff00; padding: 5px 10px; display: inline-block;">
                    🐦 View Original Tweet
                </a>
            </div>
            <div class="crt-divider"></div>
            <img src="" alt="Fullscreen image" class="full-image">
        </div>
    </div>
</div>
    <script>
        let currentImageIndex = 0;
        const allImagePaths = [IMAGE_PATHS_PLACEHOLDER]; // All image paths from Python
        console.log("All Image Paths:", allImagePaths);
        const imagesPerLoad = 50; // Increased number of images to load per scroll
        const scrollThreshold = 1000; // Load more images when 1000px from bottom
        const imageGrid = document.getElementById('imageGrid');

        function loadImage(path, index) {
            const imgContainer = document.createElement('div');
            imgContainer.className = 'image-container';
            const img = document.createElement('img');
            img.className = 'thumbnail';
            img.src = path;
            img.onerror = function() { console.error("Error loading image:", path); };
            img.onload = function() { console.log("Image loaded:", path); };
            img.onclick = function() { openImage(index); };
            imgContainer.appendChild(img);
            imageGrid.appendChild(imgContainer);
        }

        function loadMoreImages() {
            console.log("loadMoreImages called. currentImageIndex:", currentImageIndex, "allImagePaths.length:", allImagePaths.length);
            if (currentImageIndex >= allImagePaths.length) {
                console.log("No more images to load.");
                return; // No more images to load
            }

            const startIndex = currentImageIndex;
            const endIndex = Math.min(startIndex + imagesPerLoad, allImagePaths.length);

            for (let i = startIndex; i < endIndex; i++) {
                loadImage(allImagePaths[i], i);
            }
            currentImageIndex = endIndex;
            console.log("Loaded images up to index:", currentImageIndex);
        }

        // Initial load
        document.addEventListener('DOMContentLoaded', () => {
            loadMoreImages();
            // Load more images immediately if the initial load doesn't fill the viewport
            if (document.body.offsetHeight < window.innerHeight) {
                loadMoreImages();
            }
        });

        // Scroll event for lazy loading
        window.addEventListener('scroll', () => {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - scrollThreshold) {
                loadMoreImages();
            }
        });

        function openImage(index) {
            currentImageIndex = index;
            const modalImg = document.querySelector('.full-image');
            const modal = document.getElementById('fullscreenModal');
            const modalFilename = document.getElementById('modalFilename');
            const twitterLinkContainer = document.getElementById('twitterLinkContainer');
            const twitterLink = document.getElementById('twitterLink');
            
            const imagePath = allImagePaths[index];
            const filename = imagePath.split('/').pop().replace(/\'/g, ''); // Extract filename and clean quotes
            
            modalImg.src = imagePath;
            modalFilename.textContent = filename;
            
            // Extract Twitter info from filename
            const tweetInfo = extractTweetInfoFromFilename(filename);
            if (tweetInfo.username && tweetInfo.tweetId) {
                const twitterUrl = `https://twitter.com/${tweetInfo.username}/status/${tweetInfo.tweetId}`;
                twitterLink.href = twitterUrl;
                twitterLinkContainer.style.display = 'block';
            } else {
                twitterLinkContainer.style.display = 'none';
            }
            
            modal.style.display = 'flex'; // Use flex to center modal content
        }
        
        function extractTweetInfoFromFilename(filename) {
            try {
                // Remove file extension
                let baseName = filename.replace(/\\.(webp|jpg|jpeg|png|gif)$/i, '');
                // Remove -lossy suffix if present
                baseName = baseName.replace('-lossy', '');
                
                // Split by dash and extract first two parts
                const parts = baseName.split('-');
                if (parts.length >= 2) {
                    const username = parts[0];
                    const tweetId = parts[1];
                    // Verify tweet_id is numeric
                    if (/^\\d+$/.test(tweetId)) {
                        return { username, tweetId };
                    }
                }
            } catch (e) {
                console.log('Could not extract tweet info from filename:', filename);
            }
            return { username: null, tweetId: null };
        }
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
        }
    	function closeModal() {
        	const modal = document.getElementById('fullscreenModal');
        	if (modal.style.display === 'flex') {
            		modal.style.display = 'none';
        	}
    	}
    	// Update the existing window.onclick handler to prevent modal closure when clicking inside the image
   	 window.onclick = function(event) {
        	const modal = document.getElementById('fullscreenModal');
        	if (event.target === modal) {
            	closeModal();
        }
    };
        // Keyboard navigation
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
        });
    </script>
</body>
</html>
"""

    flavor_text = get_existing_flavor_text(username)
    html_template = html_template.replace("USERNAME_PLACEHOLDER", username)
    html_template = html_template.replace("FLAVOR_TEXT_PLACEHOLDER", flavor_text)

    image_paths = []
    user_webp_dir = os.path.join(username, "webp")
    if os.path.isdir(user_webp_dir):
        for root, _, files in os.walk(user_webp_dir):
            for file in files:
                if fnmatch.fnmatch(file, search_pattern):
                    relative_path = os.path.relpath(os.path.join(root, file), '.')
                    image_paths.append(f"'./{relative_path.replace(os.sep, '/')}'")

    image_paths_str = ',\n            '.join(image_paths)
    final_html = html_template.replace("IMAGE_PATHS_PLACEHOLDER", image_paths_str)

    if not image_paths:
        print(f"No .webp images found for user {username}. Deleting {output_file} if it exists.")
        if os.path.exists(output_file):
            os.remove(output_file)
        return False
    else:
        with open(output_file, 'w') as f:
            f.write(final_html)
        print(f"Generated {output_file} with {len(image_paths)} images for user {username}.")
        return True

def generate_all_html(output_file='all.html', search_pattern='*lossy*.webp'):
    html_template = """
<!-- all.html -->
<!DOCTYPE html>
<html>
<head>
    <title>MarketWizardry.org | NFT Gallery - All Images</title>
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
	    max-width: 90vw; /* Limit modal width */
	    max-height: 90vh; /* Limit modal height */
	    overflow: auto; /* Enable scrolling if content exceeds modal size */
	}
	.full-image {
	    max-width: 100%;
	    max-height: 80vh; /* Adjust as needed to leave space for filename */
	    display: block;
	    margin: 0 auto;
	    object-fit: contain;
	}
        .crt-divider {
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 10px 0;
        }
        @keyframes scan {
            0% { opacity: 1; width: 0%; }
            50% { opacity: 0.5; }
            100% { opacity: 1; width: 100%; }
        }
        .filename-display {
            color: #00ff00;
            margin-bottom: 10px;
            word-wrap: break-word;
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
        }
    </style>
</head>
<body>
    <h2>NFT Gallery - All Images</h2>
    <div class="crt-divider"></div>
    <div class="flavor-text">Every NFT collection on this digital wasteland aggregated into one glorious mess. For collectors who enjoy sensory overload and browser crashes.</div>
    <div class="crt-divider"></div>
    <!-- Image Grid -->
    <div class="image-grid" id="imageGrid">
        <!-- Images will be inserted here by JavaScript -->
    </div>
    <!-- Modal -->
    <div class="modal" id="fullscreenModal" onclick="closeModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="filename-display" id="modalFilename"></div>
            <div class="twitter-link-container" id="twitterLinkContainer" style="display: none; text-align: center; margin: 10px 0;">
                <a id="twitterLink" href="#" target="_blank" rel="noopener noreferrer" style="color: #00ff00; text-decoration: none; font-weight: bold; border: 1px solid #00ff00; padding: 5px 10px; display: inline-block;">
                    🐦 View Original Tweet
                </a>
            </div>
            <div class="crt-divider"></div>
            <img src="" alt="Fullscreen image" class="full-image">
        </div>
    </div>
</div>
    <script>
        let currentImageIndex = 0;
        const allImagePaths = [IMAGE_PATHS_PLACEHOLDER]; // All image paths from Python
        console.log("All Image Paths:", allImagePaths);
        const imagesPerLoad = 50; // Increased number of images to load per scroll
        const scrollThreshold = 1000; // Load more images when 1000px from bottom
        const imageGrid = document.getElementById('imageGrid');

        function loadImage(path, index) {
            const imgContainer = document.createElement('div');
            imgContainer.className = 'image-container';
            const img = document.createElement('img');
            img.className = 'thumbnail';
            img.src = path;
            img.onerror = function() { console.error("Error loading image:", path); };
            img.onload = function() { console.log("Image loaded:", path); };
            img.onclick = function() { openImage(index); };
            imgContainer.appendChild(img);
            imageGrid.appendChild(imgContainer);
        }

        function loadMoreImages() {
            console.log("loadMoreImages called. currentImageIndex:", currentImageIndex, "allImagePaths.length:", allImagePaths.length);
            if (currentImageIndex >= allImagePaths.length) {
                console.log("No more images to load.");
                return; // No more images to load
            }

            const startIndex = currentImageIndex;
            const endIndex = Math.min(startIndex + imagesPerLoad, allImagePaths.length);

            for (let i = startIndex; i < endIndex; i++) {
                loadImage(allImagePaths[i], i);
            }
            currentImageIndex = endIndex;
            console.log("Loaded images up to index:", currentImageIndex);
        }

        // Initial load
        document.addEventListener('DOMContentLoaded', () => {
            loadMoreImages();
            // Load more images immediately if the initial load doesn't fill the viewport
            if (document.body.offsetHeight < window.innerHeight) {
                loadMoreImages();
            }
        });

        // Scroll event for lazy loading
        window.addEventListener('scroll', () => {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - scrollThreshold) {
                loadMoreImages();
            }
        });

        function openImage(index) {
            currentImageIndex = index;
            const modalImg = document.querySelector('.full-image');
            const modal = document.getElementById('fullscreenModal');
            const modalFilename = document.getElementById('modalFilename');
            const twitterLinkContainer = document.getElementById('twitterLinkContainer');
            const twitterLink = document.getElementById('twitterLink');
            
            const imagePath = allImagePaths[index];
            const filename = imagePath.split('/').pop().replace(/\'/g, ''); // Extract filename and clean quotes
            
            modalImg.src = imagePath;
            modalFilename.textContent = filename;
            
            // Extract Twitter info from filename
            const tweetInfo = extractTweetInfoFromFilename(filename);
            if (tweetInfo.username && tweetInfo.tweetId) {
                const twitterUrl = `https://twitter.com/${tweetInfo.username}/status/${tweetInfo.tweetId}`;
                twitterLink.href = twitterUrl;
                twitterLinkContainer.style.display = 'block';
            } else {
                twitterLinkContainer.style.display = 'none';
            }
            
            modal.style.display = 'flex'; // Use flex to center modal content
        }
        
        function extractTweetInfoFromFilename(filename) {
            try {
                // Remove file extension
                let baseName = filename.replace(/\\.(webp|jpg|jpeg|png|gif)$/i, '');
                // Remove -lossy suffix if present
                baseName = baseName.replace('-lossy', '');
                
                // Split by dash and extract first two parts
                const parts = baseName.split('-');
                if (parts.length >= 2) {
                    const username = parts[0];
                    const tweetId = parts[1];
                    // Verify tweet_id is numeric
                    if (/^\\d+$/.test(tweetId)) {
                        return { username, tweetId };
                    }
                }
            } catch (e) {
                console.log('Could not extract tweet info from filename:', filename);
            }
            return { username: null, tweetId: null };
        }
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
        }
    	function closeModal() {
        	const modal = document.getElementById('fullscreenModal');
        	if (modal.style.display === 'flex') {
            		modal.style.display = 'none';
        	}
    	}
    	// Update the existing window.onclick handler to prevent modal closure when clicking inside the image
   	 window.onclick = function(event) {
        	const modal = document.getElementById('fullscreenModal');
        	if (event.target === modal) {
            	closeModal();
        }
    };
        // Keyboard navigation
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
        });
    </script>
</body>
</html>
"""

    all_image_paths = []
    current_directory = os.getcwd()
    all_entries = os.listdir(current_directory)

    for entry in all_entries:
        user_webp_dir = os.path.join(current_directory, entry, "webp")
        if os.path.isdir(user_webp_dir):
            for root, _, files in os.walk(user_webp_dir):
                for file in files:
                    if fnmatch.fnmatch(file, search_pattern):
                        relative_path = os.path.relpath(os.path.join(root, file), current_directory)
                        all_image_paths.append(f"'./{relative_path.replace(os.sep, '/')}'")

    image_paths_str = ',\n            '.join(all_image_paths)
    final_html = html_template.replace("IMAGE_PATHS_PLACEHOLDER", image_paths_str)

    with open(output_file, 'w') as f:
        f.write(final_html)
    print(f"Generated {output_file} with {len(all_image_paths)} images.")


if __name__ == "__main__":
    # Check if we're running from root directory
    if os.path.exists('nft-gallery') and os.path.isdir('nft-gallery'):
        # We're in root directory, change to nft-gallery subdirectory
        nft_gallery_dir = 'nft-gallery'
        print(f"Running NFT gallery generation in {nft_gallery_dir}/ directory")
        
        # Save current directory
        original_dir = os.getcwd()
        
        try:
            # Change to nft-gallery directory
            os.chdir(nft_gallery_dir)
            
            # Generate all.html first
            generate_all_html()

            # Dynamically find user directories
            current_directory = os.getcwd()
            all_entries = os.listdir(current_directory)
            
            user_directories = []
            for entry in all_entries:
                full_path = os.path.join(current_directory, entry)
                # Check if it's a directory and contains a 'webp' subdirectory
                if os.path.isdir(full_path) and os.path.isdir(os.path.join(full_path, "webp")):
                    user_directories.append(entry)

            # Generate user galleries and collect valid user links
            valid_user_links = []
            for user in user_directories:
                output_file = f'{user}_gallery.html'
                if generate_user_gallery_html(user, output_file):
                    valid_user_links.append(user) # Add user to list if gallery was generated

            # Generate nft-gallery.html with only valid user links
            generate_nft_gallery_html(output_file='nft-gallery.html', valid_user_names=valid_user_links)
            
            # Copy the main nft-gallery.html to root directory with corrected paths
            import shutil
            
            # Read the generated nft-gallery.html
            with open('nft-gallery.html', 'r') as f:
                content = f.read()
            
            # Update all gallery links to include nft-gallery/ prefix
            import re
            content = re.sub(r'href="([^/][^"]*_gallery\.html)"', r'href="nft-gallery/\1"', content)
            
            # Write to root directory with corrected paths
            with open('../nft-gallery.html', 'w') as f:
                f.write(content)
            
            print("Copied nft-gallery.html to root directory with corrected paths")
            
        finally:
            # Always return to original directory
            os.chdir(original_dir)
            
    else:
        # We're already in the nft-gallery directory, run normally
        print("Running NFT gallery generation in current directory")
        
        # Generate all.html first
        generate_all_html()

        # Dynamically find user directories
        current_directory = os.getcwd()
        all_entries = os.listdir(current_directory)
        
        user_directories = []
        for entry in all_entries:
            full_path = os.path.join(current_directory, entry)
            # Check if it's a directory and contains a 'webp' subdirectory
            if os.path.isdir(full_path) and os.path.isdir(os.path.join(full_path, "webp")):
                user_directories.append(entry)

        # Generate user galleries and collect valid user links
        valid_user_links = []
        for user in user_directories:
            output_file = f'{user}_gallery.html'
            if generate_user_gallery_html(user, output_file):
                valid_user_links.append(user) # Add user to list if gallery was generated

        # Generate nft-gallery.html with only valid user links
        generate_nft_gallery_html(output_file='nft-gallery.html', valid_user_names=valid_user_links)
