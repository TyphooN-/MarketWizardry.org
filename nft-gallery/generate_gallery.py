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
    """Get unique flavor text for each artist based on their style and work"""
    # Curated unique descriptions for each artist
    artist_descriptions = {
        'XCOPYART': "Legendary digital artist and NFT pioneer whose glitchy, dystopian works capture the intersection of technology and human decay.",
        'xicojam': "Glitch art virtuoso creating mind-bending visual experiences through digital manipulation and noise aesthetics.",
        'spellamin': "Atmospheric digital artist crafting ethereal landscapes and surreal environments in the metaverse.",
        'desultor': "Dark digital surrealist exploring themes of isolation and technological alienation through haunting imagery.",
        'ALCrego_': "Contemporary digital artist blending traditional art techniques with modern blockchain technology.",
        'm0dest___': "Minimalist digital creator focusing on clean aesthetics and geometric precision in NFT art.",
        'PlayStationPark': "Nostalgic digital artist recreating and reimagining retro gaming culture through blockchain art.",
        'ManIcArt_': "Bold digital expressionist pushing boundaries of color and form in the NFT space.",
        'delta_sauce': "Experimental digital artist mixing psychedelic visuals with cutting-edge blockchain technology.",
        'hectoroz_': "Vibrant digital creator specializing in character design and fantastical creatures in NFT form.",
        'Zaharia_af': "Contemporary digital artist exploring identity and culture through blockchain-validated expressions.",
        'trapdaddyvoss': "Urban digital artist bringing street culture and hip-hop aesthetics to the NFT ecosystem.",
        'klazmandoo': "Surreal digital artist creating otherworldly landscapes and impossible architectures on-chain.",
        'psychofuturist': "Cyberpunk digital visionary crafting dystopian futures and technological nightmares.",
        'haydiroket': "Space-age digital artist exploring cosmic themes and interstellar aesthetics through NFTs.",
        'endless_mazin': "Abstract digital artist creating infinite loops and mesmerizing patterns in blockchain art.",
        'Nicolas_Sassoon': "Pixel art master bringing retro computing aesthetics to the modern NFT landscape.",
        'GenerativePunk': "Algorithmic artist using code and randomness to create unique punk-inspired digital collectibles.",
        'p1xelfool': "Retro digital artist celebrating 8-bit culture and early computer graphics in NFT form.",
        'trillobyteart': "Bio-digital artist exploring organic forms and evolutionary patterns through blockchain technology.",
        'underscoreX0': "Experimental coder-artist pushing the boundaries of generative art and smart contract creativity.",
        'rustnfteth': "Industrial digital artist creating mechanical and weathered aesthetics in the NFT space.",
        'hexeosis': "Geometric digital artist specializing in mathematical precision and algorithmic beauty.",
        'neomechanica': "Cybernetic artist blending organic and mechanical elements in futuristic NFT compositions.",
        'rightclickdead': "Meta-commentary artist challenging digital ownership concepts through provocative NFT works.",
        'YUDHO_XYZ': "Abstract digital expressionist creating emotional landscapes and color-driven narratives.",
        'Kirokaze': "Atmospheric pixel artist crafting moody scenes and nostalgic digital environments.",
        'nocturnmachine': "Dark ambient digital artist creating nocturnal soundscapes and mysterious visual experiences.",
        'AINTNOTHINxart': "Street-inspired digital artist bringing urban culture and raw expression to NFT galleries.",
        'xeriesjame_art': "Contemporary digital painter translating traditional art techniques to blockchain canvas.",
        'baladasathar': "Mystical digital artist exploring spiritual themes and ethereal beauty through NFT art.",
        '_1mposter': "Identity-questioning digital artist exploring authenticity and deception in the NFT world.",
        'louisdazy': "Dreamy digital artist creating soft, contemplative works that blur reality and imagination.",
        'obtainer': "Conceptual digital artist examining acquisition, possession, and value in the NFT ecosystem.",
        'RenatoxMarini': "Expressive digital artist bringing emotional depth and human connection to blockchain art.",
        'RJ16848519': "Numerical identity artist exploring anonymity and digital personas in the NFT space.",
        'FEELSxart': "Emotion-focused digital artist translating human feelings into vibrant NFT expressions.",
        'ripcache': "Glitch memory artist excavating and preserving digital artifacts from the internet's depths.",
        'adamfuhrer': "Provocative digital artist challenging conventions and expectations in contemporary NFT art.",
        'cemhah': "Cultural digital artist bridging traditional heritage with modern blockchain technology.",
        'RedruMxART': "Bold color experimentalist creating vivid, high-contrast works in the NFT medium.",
        'neurocolor': "Synesthetic digital artist translating neurological experiences into colorful blockchain art.",
        'vad_jpg': "Compression aesthetic artist exploring digital decay and file format beauty in NFTs.",
        'DarkenedM00d': "Atmospheric mood artist creating emotional landscapes and psychological depth through NFTs.",
        'bluretina': "Visual perception artist exploring optical illusions and eye-strain aesthetics in digital art.",
        'HughesMichi': "Portraiture digital artist bringing human connection and intimacy to the NFT gallery space.",
        'godlikepx': "Divine pixel artist elevating retro graphics to spiritual and transcendent experiences.",
        'Bombadiluss': "Whimsical digital storyteller creating narrative-driven works in the NFT ecosystem.",
        'Zoen_calega': "Calming digital artist focused on zen aesthetics and peaceful expressions through blockchain.",
        'hazedlockdown': "Isolation-themed digital artist documenting modern life and social distancing through NFTs.",
        'Polygon1993': "Retro-futuristic digital artist celebrating 90s culture and early internet aesthetics.",
        'PierceLilholt': "Portrait photographer transitioning traditional photography into NFT art collections.",
        'neural_divine': "AI-collaboration artist exploring human-machine creativity in blockchain art creation.",
        'fabrii2k': "Y2K nostalgia artist recreating millennium bug aesthetics and early 2000s digital culture.",
        'slava3ngl': "Angelic digital artist creating ethereal, heavenly works with spiritual undertones.",
        'beholdthe84': "Retro computing enthusiast bringing 1984 Orwellian aesthetics to contemporary NFT art.",
        '1337skulls': "Death-metal digital artist creating dark, skull-themed works in the NFT underground.",
        '5tr4n0': "Mysterious outsider artist creating cryptic and enigmatic works in the blockchain space.",
        'agniis_eg': "Fire-themed digital artist exploring passion, destruction, and rebirth through NFT expressions.",
        'armilk88': "Dairy-surreal digital artist creating unexpectedly wholesome and milk-themed NFT collections.",
        '6taccc': "Account-themed digital artist exploring financial identity and numerical existence through NFTs.",
        '0xEdwoods': "Hex-addressed digital artist embracing blockchain technology as both medium and message.",
        'ozbren_xyz': "Domain-extension artist exploring internet identity and web culture through NFT art.",
        'petersonsart': "Traditional artist embracing NFT technology to reach new audiences and collectors.",
        'cameron16tv': "Television-static digital artist recreating broadcast aesthetics in blockchain art form.",
        'chroma_visions': "Color-theory digital artist exploring spectrum relationships and chromatic harmony in NFTs.",
        'analogvidunion': "Analog-digital fusion artist bridging old video technology with new blockchain platforms.",
        '0xDither': "Dithering technique specialist creating pixelated beauty through algorithmic NFT art processes.",
        'scardecc': "Scar-aesthetic digital artist exploring healing, damage, and beauty through blockchain expression.",
        'michaelmicasso': "Classical-modern fusion artist bringing renaissance techniques to contemporary NFT galleries.",
        'jotta_rs': "Brazilian digital artist bringing South American culture and vibrant energy to NFT art.",
        'PunksDistorted': "Punk-culture digital artist distorting and reimagining counterculture through blockchain art.",
        'killeracid': "Acidic digital artist creating corrosive, intense works that burn through conventional NFT aesthetics.",
        'Pho_Operator': "Soup-themed surreal artist creating comfort-food aesthetics in unexpected NFT art contexts.",
        'Micah_Alhadeff': "Personal narrative digital artist sharing intimate stories and experiences through blockchain art.",
        's0mfay': "Fae-mystical digital artist bringing fairy tale magic and folklore to NFT collections.",
        'aaasonipse': "Sonic-visual digital artist exploring sound-to-image translation in blockchain art creation.",
        'alulasit': "Meditative digital artist creating contemplative, peaceful works for mindful NFT collecting.",
        'GrantYun2': "Numeric identity artist exploring digital personas and mathematical beauty in NFT form.",
        'Gogolitus': "Literary-inspired digital artist bringing narrative depth and storytelling to blockchain art.",
        'AcidSoupArt': "Corrosive cuisine digital artist mixing food culture with harsh digital aesthetics.",
        'uczine': "Underground magazine aesthetic artist bringing zine culture to the NFT art world.",
        'weirdnikita': "Weird digital artist embracing the strange, unusual, and delightfully uncomfortable in NFTs.",
        'photonisdead': "Light-death digital artist exploring the end of photons and darkness in blockchain art.",
        'mickrenders': "Rendering-focused digital artist showcasing technical mastery and computational beauty in NFTs.",
        'RemikzT': "Technical digital artist exploring precision, engineering, and mechanical beauty through NFT art.",
        'cudaoutofmemory': "GPU-error digital artist embracing computational failure and technical glitches as aesthetic.",
        'davidvnun': "Minimalist digital artist creating quiet, contemplative works in the busy NFT marketplace.",
        'LexDoomArt': "Apocalyptic digital artist envisioning end-times and dystopian futures through blockchain art.",
        'MilaAugustova': "Seasonal digital artist capturing temporal beauty and cyclical nature through NFT collections.",
        'RichardNadler1': "Portrait digital artist bringing human dignity and character studies to NFT galleries.",
        'PERFECTL00P': "Infinite loop digital artist creating endless, mesmerizing cycles in blockchain art form.",
        'acid_boy__': "Acidic youth digital artist bringing teen angst and chemical aesthetics to NFT culture.",
        'xxdao_xyz': "DAO-governance artist exploring decentralized creativity and collective art creation through NFTs.",
        'matheusfxavier': "Mathematical digital artist bringing algorithmic beauty and geometric precision to blockchain art.",
        'ex_mortal_': "Post-human digital artist exploring transcendence and digital immortality through NFT expression.",
        'natived_': "Indigenous-inspired digital artist honoring traditional culture through contemporary NFT technology.",
        'degenpain': "Degenerate digital artist embracing crypto culture's darker, more chaotic artistic expressions.",
        'kinx__': "Kinetic digital artist creating movement, energy, and dynamic motion in static NFT collections.",
        '_myujii': "Kawaii digital artist bringing Japanese cute culture and adorable aesthetics to NFT galleries."
    }

    # Return unique description or fallback
    return artist_descriptions.get(username, f"{username}'s unique digital art collection showcasing creative blockchain expressions.")

def generate_nft_gallery_html(output_file='nft-gallery.html', valid_user_names=[]):
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MarketWizardry.org | NFT Gallery</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="/js/redirect.js"></script>
    <script src="/js/shared.js"></script>
    <link rel="stylesheet" href="/css/shared-styles.css">
</head>
<body>
    <div class="container">
        <h1>NFT Gallery</h1>
        <div class="grid">
            <div class="file-entry">
                <a href="all.html">ALL USERS - WARNING, may cause lag!</a>
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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="TyphooN">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarketWizardry.org | NFT Gallery - USERNAME_PLACEHOLDER</title>
    <link rel="canonical" href="https://marketwizardry.org/nft-gallery/USERNAME_PLACEHOLDER_gallery.html">
    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">

    <!-- Enhanced Standard Meta Tags -->
    <meta name="description" content="FLAVOR_TEXT_PLACEHOLDER">
    <meta name="keywords" content="AI art, NFT gallery, digital art, generative art, creative technology, USERNAME_PLACEHOLDER, artist portfolio">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="language" content="en-US">
    <meta name="revisit-after" content="7 days">
    <meta name="distribution" content="global">
    <meta name="rating" content="general">
    <meta name="theme-color" content="#00ff00">

    <!-- Enhanced Open Graph Meta Tags -->
    <meta property="og:title" content="NFT Gallery - USERNAME_PLACEHOLDER - MarketWizardry.org">
    <meta property="og:description" content="FLAVOR_TEXT_PLACEHOLDER">
    <meta property="og:url" content="https://marketwizardry.org/nft-gallery/USERNAME_PLACEHOLDER_gallery.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Market Wizardry">
    <meta property="og:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <meta property="og:image:alt" content="MarketWizardry.org - Professional Financial Trading Tools">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="en_US">


    <!-- Enhanced Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="NFT Gallery - USERNAME_PLACEHOLDER - MarketWizardry.org">
    <meta name="twitter:description" content="FLAVOR_TEXT_PLACEHOLDER">
    <meta name="twitter:site" content="@MarketW1zardry">
    <meta name="twitter:creator" content="@MarketW1zardry">
    <meta name="twitter:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <meta name="twitter:image:alt" content="MarketWizardry.org Financial Tools">
    <meta name="twitter:domain" content="marketwizardry.org">
        <meta name="twitter:label1" content="Category">
    <meta name="twitter:data1" content="Digital Art">    <meta name="twitter:label2" content="Collection">
    <meta name="twitter:data2" content="Growing">
        <script src="/js/redirect.js"></script>
    <script src="/js/shared.js"></script>
    <link rel="stylesheet" href="/css/shared-styles.css">
</head>
<body>
    <!-- Enhanced Breadcrumb Navigation with Schema Markup -->
    <nav class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a href="../market-wizardry.html" itemprop="item">
                <span itemprop="name">🏠 Market Wizardry</span>
            </a>
            <meta itemprop="position" content="1" />
        </span>
        <span class="separator">→</span>
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a href="../nft-gallery.html" itemprop="item">
                <span itemprop="name">🎨 NFT Gallery</span>
            </a>
            <meta itemprop="position" content="2" />
        </span>
        <span class="separator">→</span>
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <span itemprop="name">👤 USERNAME_PLACEHOLDER</span>
            <meta itemprop="position" content="3" />
        </span>
    </nav>
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
            <div class="modal-header">
                <div class="filename-display" id="modalFilename"></div>
                <div class="modal-button-bar">
                    <button class="nav-button" id="prevButton" data-action="previous-image">← Previous</button>
                    <span id="imageCounter" class="image-counter"></span>
                    <button class="nav-button" id="nextButton" data-action="next-image">Next →</button>
                    <button class="nav-button" id="downloadButton" data-action="download-image">⬇ Download</button>
                    <div class="twitter-link-container" id="twitterLinkContainer">
                        <a id="twitterLink" href="#" target="_blank" rel="noopener noreferrer" class="twitter-link">
                            🐦 View Original Tweet
                        </a>
                    </div>
                    <button class="close-button" data-action="close-modal">✕</button>
                </div>
                <div class="crt-divider"></div>
            </div>
            <img src="" alt="Fullscreen image" class="full-image">
        </div>
    </div>
</div>
    <script src="/js/nft-gallery.js"></script>
    <script src="/js/gallery-data-GALLERY_ID.js"></script>
</body>
</html>
"""

    flavor_text = get_existing_flavor_text(username)
    html_template = html_template.replace("USERNAME_PLACEHOLDER", username)
    html_template = html_template.replace("FLAVOR_TEXT_PLACEHOLDER", flavor_text)

    image_paths = []
    image_data = []
    user_webp_dir = os.path.join(username, "webp")
    if os.path.isdir(user_webp_dir):
        for root, _, files in os.walk(user_webp_dir):
            for file in files:
                if fnmatch.fnmatch(file, search_pattern):
                    relative_path = os.path.relpath(os.path.join(root, file), '.')
                    image_paths.append(f"'./{relative_path.replace(os.sep, '/')}'")

                    # Extract tweet info from filename
                    tweet_username, tweet_id, is_shortened = extract_tweet_info(file)
                    twitter_url = generate_twitter_url(tweet_username, tweet_id, is_shortened)

                    if twitter_url:
                        image_data.append(f"{{'twitterUrl': '{twitter_url}'}}")
                    else:
                        image_data.append('null')

    # Create external JavaScript data file for CSP compliance
    gallery_id = username.replace(" ", "_").replace("-", "_")
    js_data_file = f"../js/gallery-data-{gallery_id}.js"

    # Generate external JavaScript file with image data
    js_content = f"""// Gallery data for {username}
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {{
    const imagePaths = [{','.join(image_paths)}];
    const imageData = [{','.join(image_data)}];
    if (window.initializeGallery) {{
        window.initializeGallery(imagePaths, imageData);
    }}
}});"""

    with open(js_data_file, 'w') as js_f:
        js_f.write(js_content)

    # Replace placeholders in HTML template
    final_html = html_template.replace("GALLERY_ID", gallery_id)

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
    <link rel="stylesheet" href="/css/shared-styles.css">
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
    <div class="modal" id="fullscreenModal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="filename-display" id="modalFilename"></div>
                <div class="modal-button-bar">
                    <button class="nav-button" id="prevButton" data-action="previous-image">← Previous</button>
                    <span id="imageCounter" class="image-counter"></span>
                    <button class="nav-button" id="nextButton" data-action="next-image">Next →</button>
                    <button class="nav-button" id="downloadButton" data-action="download-image">⬇ Download</button>
                    <div class="twitter-link-container" id="twitterLinkContainer">
                        <a id="twitterLink" href="#" target="_blank" rel="noopener noreferrer" class="twitter-link">
                            🐦 View Original Tweet
                        </a>
                    </div>
                    <button class="close-button" data-action="close-modal">✕</button>
                </div>
                <div class="crt-divider"></div>
            </div>
            <img src="" alt="Fullscreen image" class="full-image">
        </div>
    </div>
</div>
    <script src="/js/nft-gallery.js"></script>
    <script src="/js/gallery-data-GALLERY_ID.js"></script>
</body>
</html>
"""

    all_image_paths = []
    all_image_data = []
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

                        # Extract tweet info from filename
                        tweet_username, tweet_id, is_shortened = extract_tweet_info(file)
                        twitter_url = generate_twitter_url(tweet_username, tweet_id, is_shortened)

                        if twitter_url:
                            all_image_data.append(f"{{'twitterUrl': '{twitter_url}'}}")
                        else:
                            all_image_data.append('null')

    # Create external JavaScript data file for CSP compliance
    gallery_id = "all"
    js_data_file = f"../js/gallery-data-{gallery_id}.js"

    # Generate external JavaScript file with image data
    js_content = f"""// Gallery data for all images
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {{
    const imagePaths = [{','.join(all_image_paths)}];
    const imageData = [{','.join(all_image_data)}];
    if (window.initializeGallery) {{
        window.initializeGallery(imagePaths, imageData);
    }}
}});"""

    with open(js_data_file, 'w') as js_f:
        js_f.write(js_content)

    # Replace placeholders in HTML template
    final_html = html_template.replace("GALLERY_ID", gallery_id)

    with open(output_file, 'w') as f:
        f.write(final_html)
    print(f"Generated {output_file} with {len(all_image_paths)} images.")


if __name__ == "__main__":

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
