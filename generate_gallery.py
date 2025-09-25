import os
import fnmatch
import random
import re
import json
import glob
from seo_templates import SEOManager, get_breadcrumb_paths, PAGE_CONFIGS, REDIRECT_SCRIPT_TEMPLATE

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
    """Get flavor text from JSON mapping, using replacement text if available"""
    try:
        # Use absolute path to ensure file is found regardless of working directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        flavors_file = os.path.join(script_dir, 'nft_gallery_flavors.json')
        with open(flavors_file, 'r', encoding='utf-8') as f:
            flavor_data = json.load(f)

        if username in flavor_data:
            data = flavor_data[username]
            # Use replacement text if available and status indicates replacement was applied
            if data.get('replacement_text') and data.get('status') in ['needs_replacement', 'replacement_applied']:
                return data['replacement_text']
            elif data.get('current_text'):
                return data['current_text']
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"Error reading flavor data for {username}: {e}")

    # Fallback if no existing flavor text found
    return f"{username}'s digital art collection - NFT gallery showcasing blockchain-validated creative expressions."


def generate_nft_gallery_html(output_file='nft-gallery.html', valid_user_names=[]):
    # Initialize SEO Manager and get breadcrumbs
    seo_manager = SEOManager()
    breadcrumb_paths = get_breadcrumb_paths()
    gallery_breadcrumbs = breadcrumb_paths['gallery']

    # Configure page settings
    page_config = PAGE_CONFIGS['gallery'].copy()
    page_config.update({
        'title': 'MarketWizardry.org | NFT Gallery',
        'canonical_url': 'https://marketwizardry.org/nft-gallery.html',
        'description': 'Blockchain-validated AI art collection showcasing generative creativity and digital expression. Explore the intersection of technology and art.',
        'og_title': 'NFT Gallery - MarketWizardry.org',
        'og_description': 'Blockchain-validated AI art collection showcasing generative creativity and digital expression. Explore the intersection of technology and art.',
        'twitter_title': 'NFT Gallery - MarketWizardry.org',
        'twitter_description': 'Blockchain-validated AI art collection showcasing generative creativity and digital expression. Explore the intersection of technology and art.',
        'keywords': page_config['keywords_base']
    })

    # Generate SEO components including JSON-LD schema
    jsonld_config = seo_manager.get_gallery_jsonld_config(
        'MarketWizardry.org NFT Gallery',
        page_config['canonical_url'],
        page_config['description']
    )
    json_ld_schema = seo_manager.generate_json_ld_schema(jsonld_config, 'nft-gallery.html')

    enhanced_meta_tags = seo_manager.generate_enhanced_meta_tags(page_config)
    breadcrumbs_html = seo_manager.generate_breadcrumbs(gallery_breadcrumbs)
    breadcrumb_css = seo_manager.generate_breadcrumb_css()

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
{enhanced_meta_tags}
{json_ld_schema}
    <style>
        body {{
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            padding-bottom: 10px;
            color: #00ff00;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .file-entry {{
            background-color: #000;
            border: 2px solid rgba(0, 255, 0, 0.5);
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .file-entry:hover {{
            background-color: #001100;
            color: #00ff00;
        }}

        a {{
            color: #00ff00;
            text-decoration: none;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .entry-description {{
            color: #00ff00;
            font-size: 0.75em;
            opacity: 0.7;
            margin-top: 8px;
            font-style: italic;
            font-weight: bold;
            line-height: 1.3;
            animation: flicker 1s infinite;
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
        }}
        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
            gap: 10px;
        }}
        .nav-button {{
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
        }}
        .nav-button:hover {{
            background-color: #001100;
            color: #00ff00;
        }}
        .nav-button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .nav-button:disabled:hover {{
            background-color: #000;
        }}
        .close-button {{
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
        }}
        .close-button:hover {{
            background-color: #001100;
        }}
        .twitter-link-container {{
            display: none;
            text-align: center;
            margin: 10px 0;
        }}
        .twitter-link {{
            color: #00ff00;
            text-decoration: none;
            font-weight: bold;
            border: 1px solid #00ff00;
            padding: 5px 10px;
            display: inline-block;
        }}
        .image-counter {{
            color: #00ff00;
            font-family: 'Courier New', monospace;
        }}
        .download-container {{
            text-align: center;
            margin-top: 10px;
        }}
        @media screen and (max-width: 768px) {{
            .modal-content {{
                padding: 5px;
                max-width: 98vw;
                max-height: 98vh;
            }}
            .full-image {{
                max-height: 55vh;
            }}
            .filename-display {{
                font-size: 0.7em;
                margin-bottom: 5px;
            }}
            .nav-button {{
                padding: 8px 15px;
                font-size: 14px;
                min-width: 60px;
            }}
            .close-button {{
                font-size: 18px;
                padding: 3px 8px;
                top: 5px;
                right: 10px;
            }}
            .twitter-link-container {{
                margin: 5px 0;
            }}
            .twitter-link {{
                font-size: 0.8em;
                padding: 3px 6px;
            }}
        }}
        .crt-divider {{
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 30px auto;
        }}
        @keyframes scan {{
            0% {{ opacity: 1; width: 0%; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; width: 100%; }}
        }}
        @keyframes flicker {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 1; }}
        }}

{breadcrumb_css}
    </style>
</head>
<body>
{breadcrumbs_html}
    <div class="container">
        <h1>NFT (Not For Trade) Gallery</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Digital receipts for GIFs that'll survive longer than your retirement fund. Witness the intersection of art and financial delusion.</div>
        <div class="crt-divider"></div>
        <div class="grid">
            <div class="file-entry" data-action="navigate" data-url="nft-gallery/all.html">
                <a href="nft-gallery/all.html">ALL USERS - WARNING, may cause lag!</a>
                <div class="entry-description">Every NFT collection on this digital wasteland aggregated into one glorious mess. For collectors who enjoy sensory overload and browser crashes.</div>
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
            description = get_existing_flavor_text(user)
            user_links.append(f'<div class="file-entry" data-action="navigate" data-url="nft-gallery/{user_gallery_file}"><a href="nft-gallery/{user_gallery_file}">{user}</a><div class="entry-description">{description}</div></div>')

    user_links_str = '\n'.join(user_links)
    final_html = html_content.replace("USER_LINKS_PLACEHOLDER", user_links_str)

    with open(output_file, 'w') as f:
        f.write(final_html)
    print(f"Generated {output_file} with {len(user_links)} user links.")

def generate_user_gallery_html(username, output_file, search_pattern='*lossy*.webp'):
    # Initialize SEO Manager and get breadcrumbs for individual galleries
    seo_manager = SEOManager()
    breadcrumb_paths = get_breadcrumb_paths()

    # Create breadcrumb path for individual user gallery
    user_gallery_breadcrumbs = [
        {'name': '🏠 Market Wizardry', 'url': '../market-wizardry.html'},
        {'name': '🎨 NFT Gallery', 'url': '../nft-gallery.html'},
        {'name': f'👤 {username}', 'url': None}  # Current page
    ]

    # Get existing flavor text before configuring page settings
    flavor_text = get_existing_flavor_text(username)

    # Configure page settings for user gallery
    page_config = PAGE_CONFIGS['gallery'].copy()
    page_config.update({
        'title': f'MarketWizardry.org | NFT Gallery - {username}',
        'canonical_url': f'https://marketwizardry.org/nft-gallery/{username}_gallery.html',
        'description': flavor_text,
        'og_title': f'NFT Gallery - {username} - MarketWizardry.org',
        'og_description': flavor_text,
        'twitter_title': f'NFT Gallery - {username} - MarketWizardry.org',
        'twitter_description': flavor_text,
        'keywords': f"{page_config['keywords_base']}, {username}, artist portfolio"
    })

    # Generate SEO components
    enhanced_meta_tags = seo_manager.generate_enhanced_meta_tags(page_config)
    breadcrumbs_html = seo_manager.generate_breadcrumbs(user_gallery_breadcrumbs)
    breadcrumb_css = seo_manager.generate_breadcrumb_css()

    # Generate JSON-LD schema for user gallery
    jsonld_config = seo_manager.get_gallery_jsonld_config(
        f'NFT Gallery - {username}',
        page_config['canonical_url'],
        flavor_text,
        artist_name=username
    )
    json_ld_schema = seo_manager.generate_json_ld_schema(jsonld_config, f'nft-gallery/{output_file}')

    html_template = f"""<!-- user_gallery.html -->
<!DOCTYPE html>
<html lang="en">
<head>
{enhanced_meta_tags}
{json_ld_schema}
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
        /* Image grid styles */
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .image-container {{
            position: relative;
            width: 100%;
            max-width: 500px; /* Maximum size of the container */
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
        /* Modal styles */
        .modal {{
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
        }}
	.modal-content {{
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
	}}
	.full-image {{
	    max-width: 100%;
	    max-height: 65vh; /* Reduced to leave space for navigation buttons */
	    display: block;
	    margin: 0 auto;
	    object-fit: contain;
	}}
        .crt-divider {{
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 30px auto;
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
        }}
        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
            gap: 10px;
        }}
        .nav-button {{
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
        }}
        .nav-button:hover {{
            background-color: #001100;
            color: #00ff00;
        }}
        .nav-button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .nav-button:disabled:hover {{
            background-color: #000;
        }}
        .close-button {{
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
        }}
        .close-button:hover {{
            background-color: #001100;
        }}
        @media screen and (max-width: 768px) {{
            .modal-content {{
                padding: 5px;
                max-width: 98vw;
                max-height: 98vh;
            }}
            .full-image {{
                max-height: 55vh;
            }}
            .filename-display {{
                font-size: 0.7em;
                margin-bottom: 5px;
            }}
            .nav-button {{
                padding: 8px 15px;
                font-size: 14px;
                min-width: 60px;
            }}
            .close-button {{
                font-size: 18px;
                padding: 3px 8px;
                top: 5px;
                right: 10px;
            }}
            .twitter-link-container {{
                margin: 5px 0;
            }}
            .twitter-link-container a {{
                font-size: 0.8em;
                padding: 3px 6px;
            }}
        }}

{breadcrumb_css}
    </style>
</head>
<body>
{breadcrumbs_html}
    <div class="container">
        <h2>NFT Gallery - USERNAME_PLACEHOLDER</h2>
        <div class="crt-divider"></div>
        <div class="flavor-text">FLAVOR_TEXT_PLACEHOLDER</div>
        <div class="crt-divider"></div>
        <!-- Image Grid -->
    <div class="image-grid" id="imageGrid">
        <!-- Images will be inserted here by JavaScript -->
    </div>
    <!-- Modal -->
    <div class="modal" id="fullscreenModal">
        <div class="modal-content">
            <button class="close-button" data-action="close-modal">&times;</button>
            <div class="filename-display" id="modalFilename"></div>
            <div class="twitter-link-container" id="twitterLinkContainer">
                <a id="twitterLink" href="#" target="_blank" rel="noopener noreferrer" class="twitter-link">
                    🐦 View Original Tweet
                </a>
            </div>
            <div class="crt-divider"></div>
            <img src="" alt="Fullscreen image" class="full-image">
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
</div>
    <script src="/js/gallery.js"></script>
    <script src="/js/gallery-data-USERNAME_PLACEHOLDER.js"></script>
    </div>
</body>
</html>
"""

    html_template = html_template.replace("USERNAME_PLACEHOLDER", username)
    html_template = html_template.replace("FLAVOR_TEXT_PLACEHOLDER", flavor_text)

    image_paths = []
    user_webp_dir = os.path.join(username, "webp")
    if os.path.isdir(user_webp_dir):
        for root, _, files in os.walk(user_webp_dir):
            for file in files:
                if fnmatch.fnmatch(file, search_pattern):
                    relative_path = os.path.relpath(os.path.join(root, file), '.')
                    image_paths.append(f'"./{relative_path.replace(os.sep, "/")}"')

    # Create external JavaScript data file for this user
    js_content = f'''// Image paths for {username} gallery
const galleryImagePaths = [
{",".join(f"    {path}" for path in image_paths)}
];

// Initialize gallery when page loads
document.addEventListener('DOMContentLoaded', function() {{
    initializeGallery(galleryImagePaths);
}});'''

    js_filename = f'../js/gallery-data-{username}.js'
    with open(js_filename, 'w') as f:
        f.write(js_content)

    if not image_paths:
        print(f"No .webp images found for user {username}. Deleting {output_file} if it exists.")
        if os.path.exists(output_file):
            os.remove(output_file)
        # Also remove the JS file if it exists
        if os.path.exists(js_filename):
            os.remove(js_filename)
        return False
    else:
        with open(output_file, 'w') as f:
            f.write(html_template)
        print(f"Generated {output_file} and {js_filename} with {len(image_paths)} images for user {username}.")
        return True

def generate_all_html(output_file='all.html', search_pattern='*lossy*.webp'):
    # Initialize SEO Manager and get breadcrumbs for all gallery
    seo_manager = SEOManager()

    # Create breadcrumb path for all gallery
    all_gallery_breadcrumbs = [
        {'name': '🏠 Market Wizardry', 'url': '../market-wizardry.html'},
        {'name': '🎨 NFT Gallery', 'url': '../nft-gallery.html'},
        {'name': '📁 All Images', 'url': None}  # Current page
    ]

    # Configure page settings for all gallery
    page_config = PAGE_CONFIGS['gallery'].copy()
    page_config.update({
        'title': 'MarketWizardry.org | NFT Gallery - All Images',
        'canonical_url': 'https://marketwizardry.org/nft-gallery/all.html',
        'description': 'Complete NFT collection aggregated into one comprehensive gallery. Browse all digital art pieces in the MarketWizardry collection.',
        'og_title': 'All NFT Images - MarketWizardry.org',
        'og_description': 'Complete NFT collection aggregated into one comprehensive gallery. Browse all digital art pieces in the MarketWizardry collection.',
        'twitter_title': 'All NFT Images - MarketWizardry.org',
        'twitter_description': 'Complete NFT collection aggregated into one comprehensive gallery. Browse all digital art pieces in the MarketWizardry collection.',
        'keywords': f"{page_config['keywords_base']}, complete collection, all images"
    })

    # Generate SEO components including JSON-LD schema
    jsonld_config = seo_manager.get_gallery_jsonld_config(
        'Complete NFT Gallery Collection',
        page_config['canonical_url'],
        page_config['description']
    )
    json_ld_schema = seo_manager.generate_json_ld_schema(jsonld_config, 'nft-gallery/all.html')

    enhanced_meta_tags = seo_manager.generate_enhanced_meta_tags(page_config)
    breadcrumbs_html = seo_manager.generate_breadcrumbs(all_gallery_breadcrumbs)
    breadcrumb_css = seo_manager.generate_breadcrumb_css()

    html_template = f"""<!-- all.html -->
<!DOCTYPE html>
<html lang="en">
<head>
{enhanced_meta_tags}
{json_ld_schema}
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
        /* Image grid styles */
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .image-container {{
            position: relative;
            width: 100%;
            max-width: 500px; /* Maximum size of the container */
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
        /* Modal styles */
        .modal {{
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
        }}
	.modal-content {{
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
	}}
	.full-image {{
	    max-width: 100%;
	    max-height: 65vh; /* Reduced to leave space for navigation buttons */
	    display: block;
	    margin: 0 auto;
	    object-fit: contain;
	}}
        .crt-divider {{
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 30px auto;
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
        }}
        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
            gap: 10px;
        }}
        .nav-button {{
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
        }}
        .nav-button:hover {{
            background-color: #001100;
            color: #00ff00;
        }}
        .nav-button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .nav-button:disabled:hover {{
            background-color: #000;
        }}
        .close-button {{
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
        }}
        .close-button:hover {{
            background-color: #001100;
        }}
        @media screen and (max-width: 768px) {{
            .modal-content {{
                padding: 5px;
                max-width: 98vw;
                max-height: 98vh;
            }}
            .full-image {{
                max-height: 55vh;
            }}
            .filename-display {{
                font-size: 0.7em;
                margin-bottom: 5px;
            }}
            .nav-button {{
                padding: 8px 15px;
                font-size: 14px;
                min-width: 60px;
            }}
            .close-button {{
                font-size: 18px;
                padding: 3px 8px;
                top: 5px;
                right: 10px;
            }}
            .twitter-link-container {{
                margin: 5px 0;
            }}
            .twitter-link-container a {{
                font-size: 0.8em;
                padding: 3px 6px;
            }}
        }}

{breadcrumb_css}
    </style>
</head>
<body>
{breadcrumbs_html}
    <div class="container">
        <h2>NFT Gallery - All Images</h2>
        <div class="crt-divider"></div>
        <div class="flavor-text">Every NFT collection on this digital wasteland aggregated into one glorious mess. For collectors who enjoy sensory overload and browser crashes.</div>
        <div class="crt-divider"></div>
        <!-- Image Grid -->
    <div class="image-grid" id="imageGrid">
        <!-- Images will be inserted here by JavaScript -->
    </div>
    <!-- Modal -->
    <div class="modal" id="fullscreenModal">
        <div class="modal-content">
            <button class="close-button" data-action="close-modal">&times;</button>
            <div class="filename-display" id="modalFilename"></div>
            <div class="twitter-link-container" id="twitterLinkContainer">
                <a id="twitterLink" href="#" target="_blank" rel="noopener noreferrer" class="twitter-link">
                    🐦 View Original Tweet
                </a>
            </div>
            <div class="crt-divider"></div>
            <img src="" alt="Fullscreen image" class="full-image">
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
    <script src="/js/redirect.js"></script>
    <script src="/js/shared.js"></script>
    <script src="/js/gallery.js"></script>
    <script src="/js/gallery-data-all.js"></script>
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
                        all_image_paths.append(f'"./{relative_path.replace(os.sep, "/")}"')

    # Create external JavaScript data file for all gallery
    js_content = f'''// Image paths for all gallery
const galleryImagePaths = [
{",".join(f"    {path}" for path in all_image_paths)}
];

// Initialize gallery when page loads
document.addEventListener('DOMContentLoaded', function() {{
    initializeGallery(galleryImagePaths);
}});'''

    js_filename = '../js/gallery-data-all.js'
    with open(js_filename, 'w') as f:
        f.write(js_content)

    with open(output_file, 'w') as f:
        f.write(html_template)
    print(f"Generated {output_file} and {js_filename} with {len(all_image_paths)} images.")


def generate_ai_art_html():
    """
    Generate ai-art.html with preserved unique content and working image grid.
    Scans ai-art/ directory for images and generates a functional gallery.
    """
    print("Generating ai-art.html with preserved unique content...")

    # Scan for AI art images
    ai_art_dir = 'ai-art'
    if not os.path.exists(ai_art_dir):
        print(f"Error: {ai_art_dir} directory not found!")
        return False

    # Find all .webp files in the ai-art directory
    pattern = os.path.join(ai_art_dir, '*.webp')
    image_files = glob.glob(pattern)

    if not image_files:
        print(f"No .webp images found in {ai_art_dir} directory!")
        return False

    # Sort them naturally (00001.webp, 00002.webp, etc.)
    def natural_sort_key(path):
        filename = os.path.basename(path)
        # Extract numbers from filename for proper sorting
        numbers = re.findall(r'\d+', filename)
        return [int(num) for num in numbers] if numbers else [0]

    image_files.sort(key=natural_sort_key)

    # Convert to relative paths with forward slashes
    image_paths = []
    for file_path in image_files:
        # Convert to relative path and use forward slashes
        relative_path = file_path.replace(os.sep, '/')
        if not relative_path.startswith('/'):
            relative_path = '/' + relative_path
        image_paths.append(relative_path)

    print(f"Found {len(image_paths)} AI art images")

    # Generate external JavaScript data file (CSP compliant)
    js_image_paths = ',\n    '.join(f'"{path}"' for path in image_paths)
    ai_art_js_content = f'''// Image paths for AI art gallery
const galleryImagePaths = [
    {js_image_paths}
];

// Initialize gallery when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {{
    console.log('AI Art gallery data loaded, initializing...');
    if (typeof initializeGallery === 'function') {{
        initializeGallery(galleryImagePaths);
    }} else {{
        console.error('initializeGallery function not found!');
    }}
}});'''

    # Write the external JS file
    try:
        with open('js/gallery-data-ai-art.js', 'w', encoding='utf-8') as f:
            f.write(ai_art_js_content)
        print(f"✓ Generated js/gallery-data-ai-art.js with {len(image_paths)} images")
    except Exception as e:
        print(f"Error writing ai-art JS file: {e}")
        return False

    # AI Art HTML template with preserved unique content (CSP compliant)
    ai_art_html = f'''<!-- ai-art.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="TyphooN">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarketWizardry.org | AI Art</title>
    <link rel="canonical" href="https://marketwizardry.org/ai-art.html">
    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">

    <!-- Enhanced Standard Meta Tags -->
    <meta name="description" content="Robot-generated 'art' for humans who've given up on actual creativity. Watch machines mock your artistic soul while you pretend it's profound.">
    <meta name="keywords" content="AI art, NFT gallery, digital art, generative art, creative technology">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="language" content="en-US">
    <meta name="revisit-after" content="7 days">
    <meta name="distribution" content="global">
    <meta name="rating" content="general">
    <meta name="theme-color" content="#00ff00">

    <!-- Enhanced Open Graph Meta Tags -->
    <meta property="og:title" content="AI Art - MarketWizardry.org">
    <meta property="og:description" content="Robot-generated 'art' for humans who've given up on actual creativity. Watch machines mock your artistic soul while you pretend it's profound.">
    <meta property="og:url" content="https://marketwizardry.org/ai-art.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Market Wizardry">
    <meta property="og:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <meta property="og:image:alt" content="MarketWizardry.org - Professional Financial Trading Tools">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="en_US">


    <!-- Enhanced Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="AI Art - MarketWizardry.org">
    <meta name="twitter:description" content="Robot-generated 'art' for humans who've given up on actual creativity. Watch machines mock your artistic soul while you pretend it's profound.">
    <meta name="twitter:site" content="@MarketW1zardry">
    <meta name="twitter:creator" content="@MarketW1zardry">
    <meta name="twitter:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <meta name="twitter:image:alt" content="MarketWizardry.org Financial Tools">
    <meta name="twitter:domain" content="marketwizardry.org">
        <meta name="twitter:label1" content="Category">
    <meta name="twitter:data1" content="Digital Art">    <meta name="twitter:label2" content="Collection">
    <meta name="twitter:data2" content="Growing">
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
        h1 {{
            text-align: center;
            padding-bottom: 10px;
            color: #00ff00;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        }}
        /* Image grid styles */
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .image-container {{
            position: relative;
            width: 100%;
            max-width: 500px; /* Maximum size of the container */
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
        /* Modal styles */
        .modal {{
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
        }}
	.modal-content {{
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
	}}
	.full-image {{
	    max-width: 100%;
	    max-height: 65vh; /* Reduced to leave space for navigation buttons */
	    display: block;
	    margin: 0 auto;
	    object-fit: contain;
	}}
        .crt-divider {{
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 30px auto;
        }}
        @keyframes scan {{
            0% {{ opacity: 1; width: 0%; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; width: 100%; }}
        }}
        @keyframes flicker {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 1; }}
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
        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
            gap: 10px;
        }}
        .nav-button {{
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
        }}
        .nav-button:hover {{
            background-color: #001100;
            color: #00ff00;
        }}
        .nav-button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .nav-button:disabled:hover {{
            background-color: #000;
        }}
        .close-button {{
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
        }}
        .close-button:hover {{
            background-color: #001100;
        }}
        .filename-display {{
            color: #00ff00;
            margin-bottom: 10px;
            word-wrap: break-word;
            font-size: 0.9em;
        }}
        .image-counter {{
            color: #00ff00;
            font-family: 'Courier New', monospace;
        }}
        .download-container {{
            text-align: center;
            margin-top: 10px;
        }}
        .modal.modal-open {{
            display: flex;
        }}


    /* Breadcrumb Navigation Styles */
    .breadcrumb {{
        font-size: 0.8em;
        color: #00aa00;
        margin-bottom: 20px;
        padding: 10px 0;
        text-align: left;
    }}

    .breadcrumb a {{
        color: #00ff00 !important;
        text-decoration: none;
        transition: all 0.2s ease;
    }}

    .breadcrumb a:hover {{
        color: #ffffff !important;
    }}

    .breadcrumb .separator {{
        margin: 0 8px;
        color: #004400;
    }}

    /* Mobile breadcrumb optimization */
    @media screen and (max-width: 768px) {{
        .breadcrumb {{
            display: none;
        }}
    }}
        /* Mobile breadcrumb optimization */
        @media screen and (max-width: 768px) {{
            .breadcrumb {{
                display: none;
            }}
            .modal-content {{
                padding: 5px;
                max-width: 98vw;
                max-height: 98vh;
            }}
            .full-image {{
                max-height: 55vh;
            }}
            .filename-display {{
                font-size: 0.7em;
                margin-bottom: 5px;
            }}
            .nav-button {{
                padding: 8px 15px;
                font-size: 14px;
                min-width: 60px;
            }}
            .close-button {{
                font-size: 18px;
                padding: 3px 8px;
                top: 5px;
                right: 10px;
            }}
            .nav-buttons {{
                margin-top: 5px;
                gap: 5px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Enhanced Breadcrumb Navigation with Schema Markup -->
    <nav class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a href="market-wizardry.html" itemprop="item">
                <span itemprop="name">🏠 Market Wizardry</span>
            </a>
            <meta itemprop="position" content="1" />
        </span>
        <span class="separator">→</span>
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a href="ai-art.html" itemprop="item">
                <span itemprop="name">🎨 AI Art</span>
            </a>
            <meta itemprop="position" content="2" />
        </span>
    </nav>

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
    </div>
    <script src="/js/redirect.js"></script>
    <script src="/js/shared.js"></script>
    <script src="/js/gallery.js"></script>
    <script src="/js/gallery-data-ai-art.js"></script>
</body>
</html>'''

    # Write the AI art HTML file
    try:
        with open('ai-art.html', 'w', encoding='utf-8') as f:
            f.write(ai_art_html)
        print(f"✓ Generated ai-art.html with {len(image_paths)} AI art images")
        return True
    except Exception as e:
        print(f"Error writing ai-art.html: {e}")
        return False


if __name__ == "__main__":
    # Check if we're running from root directory
    if os.path.exists('nft-gallery') and os.path.isdir('nft-gallery'):
        # We're in root directory, change to nft-gallery subdirectory
        nft_gallery_dir = 'nft-gallery'
        print(f"Running CSP-compliant NFT gallery generation in {nft_gallery_dir}/ directory")

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
            content = re.sub(r'href="([^"]*_gallery\.html)"', r'href="nft-gallery/\1"', content)
            # Fix double nft-gallery/ prefixes
            content = re.sub(r'href="nft-gallery/nft-gallery/', r'href="nft-gallery/', content)

            # Write to root directory with corrected paths
            with open('../nft-gallery.html', 'w') as f:
                f.write(content)

            # Remove the intermediate file from nft-gallery/ directory
            os.remove('nft-gallery.html')

            print("Generated CSP-compliant gallery files and copied nft-gallery.html to root directory")

        finally:
            # Always return to original directory
            os.chdir(original_dir)

        # Generate AI art gallery (from root directory)
        print("\n" + "="*50)
        generate_ai_art_html()

    else:
        # We're already in the nft-gallery directory, run normally
        print("Running CSP-compliant NFT gallery generation in current directory")

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

        # Generate AI art gallery (switch to parent directory first)
        print("\n" + "="*50)
        os.chdir('..')  # Go to root directory
        generate_ai_art_html()
        # Note: staying in root directory since this is the end of the script