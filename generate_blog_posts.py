#!/usr/bin/env python3
"""
Script to generate HTML blog posts from text files and update blog.html
"""
import os
import re
import random
import pandas as pd
import glob
import json
import argparse
from datetime import datetime
from pathlib import Path

# Load symbol to sector/industry mapping
try:
    with open('symbol_sector_mapping.json', 'r') as f:
        SYMBOL_SECTOR_MAPPING = json.load(f)
    print(f"Loaded sector mapping for {len(SYMBOL_SECTOR_MAPPING)} symbols")
except FileNotFoundError:
    SYMBOL_SECTOR_MAPPING = {}
    print("Warning: symbol_sector_mapping.json not found, using fallback detection")

# Configuration
BLOG_DIR = "blog"
BLOG_INDEX = "blog.html"
FLAVOR_TEXT_CACHE = "flavor_text_used.json"
BLOG_FLAVOR_MAPPING = "blog_flavor_mapping.json"

# Global tracking for used flavor texts
used_flavor_texts = set()
blog_flavor_mapping = {}

def load_used_flavor_texts():
    """Load previously used flavor texts from cache file"""
    global used_flavor_texts, blog_flavor_mapping
    try:
        if os.path.exists(FLAVOR_TEXT_CACHE):
            with open(FLAVOR_TEXT_CACHE, 'r', encoding='utf-8') as f:
                used_flavor_texts = set(json.load(f))
        else:
            used_flavor_texts = set()
        print(f"Loaded {len(used_flavor_texts)} previously used flavor texts")
        
        # Load blog flavor mapping
        if os.path.exists(BLOG_FLAVOR_MAPPING):
            with open(BLOG_FLAVOR_MAPPING, 'r', encoding='utf-8') as f:
                blog_flavor_mapping = json.load(f)
        else:
            blog_flavor_mapping = {}
        print(f"Loaded flavor text mapping for {len(blog_flavor_mapping)} blog posts")
    except Exception as e:
        print(f"Error loading flavor text cache: {e}")
        used_flavor_texts = set()
        blog_flavor_mapping = {}

def save_used_flavor_texts():
    """Save used flavor texts to cache file"""
    try:
        with open(FLAVOR_TEXT_CACHE, 'w', encoding='utf-8') as f:
            json.dump(list(used_flavor_texts), f, indent=2, ensure_ascii=False)
        print(f"Saved {len(used_flavor_texts)} used flavor texts to cache")
        
        # Save blog flavor mapping
        with open(BLOG_FLAVOR_MAPPING, 'w', encoding='utf-8') as f:
            json.dump(blog_flavor_mapping, f, indent=2, ensure_ascii=False)
        print(f"Saved flavor text mapping for {len(blog_flavor_mapping)} blog posts")
    except Exception as e:
        print(f"Error saving flavor text cache: {e}")

def select_unused_flavor_text(flavor_list, fallback_text="Default flavor text for when all options are exhausted."):
    """Select a flavor text that hasn't been used before"""
    global used_flavor_texts
    
    # Find unused options
    available_options = [text for text in flavor_list if text not in used_flavor_texts]
    
    # If all options are used, reset the tracking and start over
    if not available_options:
        print(f"All {len(flavor_list)} flavor texts in this category have been used. Resetting...")
        # Remove all texts from this category from used_flavor_texts
        used_flavor_texts = used_flavor_texts - set(flavor_list)
        available_options = flavor_list.copy()
    
    # Select randomly from available options
    if available_options:
        selected_text = random.choice(available_options)
        used_flavor_texts.add(selected_text)
        return selected_text
    else:
        # Fallback in case something goes wrong
        return fallback_text

def get_consistent_flavor_text(filename, title):
    """Get or generate consistent flavor text for a blog post"""
    global blog_flavor_mapping
    
    # Check if we already have flavor text for this blog post
    if filename in blog_flavor_mapping:
        return blog_flavor_mapping[filename]
    
    # Generate new flavor text and store it
    flavor_text = generate_flavor_text(title, filename)
    blog_flavor_mapping[filename] = flavor_text
    return flavor_text

def load_darwinex_symbols():
    """Load all symbols from Darwinex CSV exports for position detection"""
    all_symbols = set()
    
    # Find all Darwinex CSV files
    csv_patterns = [
        "*/SymbolsExport-Darwinex-Live-*.csv",
        "var-explorer/SymbolsExport-Darwinex-Live-*.csv",
        "SymbolsExport-Darwinex-Live-*.csv"
    ]
    
    csv_files = []
    for pattern in csv_patterns:
        csv_files.extend(glob.glob(pattern))
    
    for csv_file in csv_files[:3]:  # Limit to first 3 files for performance
        try:
            df = pd.read_csv(csv_file, delimiter=';')
            if 'Symbol' in df.columns:
                symbols = df['Symbol'].dropna().unique()
                all_symbols.update(symbol.lower() for symbol in symbols)
        except Exception as e:
            print(f"Warning: Could not load {csv_file}: {e}")
            continue
    
    # Fallback list if CSV loading fails
    if not all_symbols:
        all_symbols = {
            'aapl', 'msft', 'googl', 'goog', 'amzn', 'meta', 'tsla', 'nvda', 'nflx', 'adbe',
            'jpm', 'bac', 'wfc', 'gs', 'ms', 'c', 'v', 'ma', 'pypl', 'skx', 'gtls', 'arcc',
            'roku', 'idxx', 'aal', 'chgg', 'clf', 'coty', 'srpt', 'biib', 'snap', 'mdb'
        }
    
    return list(all_symbols)

# Load symbols once at startup
DARWINEX_SYMBOLS = load_darwinex_symbols()

# HTML template for individual blog posts
BLOG_POST_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="TyphooN">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarketWizardry.org | {title}</title>
    <link rel="canonical" href="https://marketwizardry.org/blog/{filename}">
    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">
    <!-- Standard Meta Tags -->
    <meta name="description" content="{description}">
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="MarketWizardry.org | {title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="https://marketwizardry.org/blog/{filename}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Market Wizardry">
    <meta property="og:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <meta property="og:image:alt" content="MarketWizardry.org - Financial Trading Tools">
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:site" content="@MarketW1zardry">
    <meta name="twitter:creator" content="@MarketW1zardry">
    <meta name="twitter:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <script>
        // Set viewport immediately for mobile scaling
        if (!document.querySelector('meta[name="viewport"]')) {{
            const viewport = document.createElement('meta');
            viewport.name = 'viewport';
            viewport.content = 'width=device-width, initial-scale=1.0';
            document.head.insertBefore(viewport, document.head.firstChild);
        }}
        
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
        * {{
            box-sizing: border-box;
        }}
        body {{
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
            overflow-y: auto;
        }}
        .container {{
            max-width: 1200px;
            margin: auto;
            min-height: 100vh;
        }}
        header {{
            text-align: left;
            color: #00ff00;
            margin-bottom: 20px;
        }}
        h1 {{
            margin: 0;
        }}
        .content-section {{
            border: 2px solid rgba(0, 255, 0, 0.5);
            padding: 20px;
            margin: 20px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .content-section:hover {{
            background-color: #001100;
            transform: scale(1.02);
        }}
        .content-section h2 {{
            color: #00ff00;
            margin: 0 0 10px 0;
        }}
        .content-section .summary {{
            color: #00cc00;
            font-size: 0.9em;
        }}
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            z-index: 10000;
            overflow-y: auto;
        }}
        .modal-content {{
            margin: 20px auto;
            padding: 10px;
            width: 90%;
            max-width: 1200px;
            background-color: #000;
            border: 2px solid rgba(0, 255, 0, 0.5);
            touch-action: pan-y;
            max-height: calc(100vh - 40px);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }}
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(0, 255, 0, 0.5);
            padding-bottom: 5px;
            margin-bottom: 10px;
        }}
        .modal-header h2 {{
            margin: 0;
            color: #00ff00;
            font-size: 1.2em;
        }}
        .modal-header a {{
            color: #00ff00;
            text-decoration: none;
            font-weight: bold;
            border: 2px solid #00ff00;
            padding: 2px 5px;
            margin-left: 10px;
        }}
        .modal-header a:hover {{
            text-decoration: underline;
            background-color: #001100;
        }}
        .modal-text {{
            width: 100%;
            max-width: 100%;
            flex-grow: 1;
            overflow-y: scroll;
            overflow-x: hidden;
            font-family: "Courier New", monospace;
            white-space: pre-wrap;
            overflow-wrap: break-word;
            border: 2px solid #00ff00;
            padding: 20px;
            border-radius: 5px;
            color: #00ff00;
        }}
        .modal-text::-webkit-scrollbar {{
            width: 12px;
        }}
        .modal-text::-webkit-scrollbar-track {{
            background: #000;
        }}
        .modal-text::-webkit-scrollbar-thumb {{
            background: #00ff00;
            border: 2px solid #000;
        }}
        .modal-text::-webkit-scrollbar-thumb:hover {{
            background: #00cc00;
        }}
        .close-button {{
            color: #00ff00;
            font-size: 28px;
            font-weight: bold;
            border: 2px solid #00ff00;
            padding: 0 5px;
            line-height: 1;
        }}
        .close-button:hover,
        .close-button:focus {{
            color: #00ff00;
            text-decoration: none;
            cursor: pointer;
            background-color: #001100;
        }}
        .modal[tabindex="0"]:focus {{
            outline: none;
        }}
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            .modal-content {{
                width: 95%;
            }}
            .content-section {{
                padding: 15px;
            }}
        }}
        @media (max-width: 480px) {{
            body {{
                padding: 10px;
            }}
            .modal-content {{
                width: 95%;
                margin: 10px auto;
            }}
        }}
        .crt-divider {{
            width: 100%;
            height: 1px;
            background-color: #00ff00;
            animation: scan 1s infinite;
            margin: 30px 0;
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
    </style>
</head>
<body>
<div class="container">
    <header><h1>{title}</h1></header>
    <div class="crt-divider"></div>
    <div class="flavor-text">{description}</div>
    <div class="crt-divider"></div>
    
    <div class="content-section" onclick="openModal()">
        <h2>{section_title}</h2>
        <p class="summary">{summary}</p>
        <p class="summary"><strong>Click to read full analysis</strong></p>
    </div>

</div>

<div id="analysisModal" class="modal" tabindex="0">
    <div class="modal-content">
        <div class="modal-header">
            <h2>{title}</h2>
            <a id="downloadButton" href="{txt_filename}" download="{txt_filename}" onclick="forceDownload(event, this)">Download Report</a>
            <span class="close-button" onclick="closeModal()">&times;</span>
        </div>
        <div class="modal-text" tabindex="0" id="analysisContent"></div>
    </div>
</div>

<script>
    // Force download function
    function forceDownload(event, link) {{
        event.preventDefault();
        const url = link.href;
        const filename = link.download || url.split('/').pop();
        
        fetch(url)
            .then(response => response.blob())
            .then(blob => {{
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = downloadUrl;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(downloadUrl);
                document.body.removeChild(a);
            }})
            .catch(error => console.error('Download failed:', error));
    }}
    
    function openModal() {{
        const modal = document.getElementById("analysisModal");
        const analysisContent = document.getElementById("analysisContent");
        const txtUrl = "{txt_filename}";
        
        // Load content dynamically like explorers do
        fetch(txtUrl)
            .then(response => {{
                if (!response.ok) {{
                    throw new Error(`HTTP error! status: ${{response.status}}`);
                }}
                return response.text();
            }})
            .then(data => {{
                analysisContent.textContent = data;
                modal.style.display = "block";
                document.body.style.overflow = "hidden";
                modal.focus();
            }})
            .catch(error => {{
                console.error("Error fetching analysis:", error);
                analysisContent.textContent = "Error loading analysis content.";
                modal.style.display = "block";
                document.body.style.overflow = "hidden";
                modal.focus();
            }});
    }}

    function closeModal() {{
        const modal = document.getElementById("analysisModal");
        
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }}

    // Close modal when clicking outside content
    document.getElementById("analysisModal").addEventListener('click', (event) => {{
        if (event.target === event.currentTarget) {{
            closeModal();
        }}
    }});

    // Close modal with Escape key
    document.addEventListener('keydown', (event) => {{
        if (event.key === 'Escape' && document.getElementById("analysisModal").style.display === "block") {{
            closeModal();
        }}
    }});

    // Scroll controls for modal text
    const modalText = document.querySelector('.modal-text');
    modalText.addEventListener('keydown', (event) => {{
        const scrollAmount = 50;
        if (event.key === 'ArrowUp') {{
            event.preventDefault();
            modalText.scrollTop -= scrollAmount;
        }} else if (event.key === 'ArrowDown') {{
            event.preventDefault();
            modalText.scrollTop += scrollAmount;
        }}
    }});
</script>
</body>
</html>'''


def generate_witty_description(content, filename, title):
    """Generate witty Sam Hyde-esque meta descriptions for blog posts"""
    content_lower = content.lower()
    filename_lower = filename.lower()
    
    # Extract stock ticker from filename if present (e.g., SRPT from 09082025-SRPT.txt)
    import re
    stock_ticker = None
    upper_filename = filename.upper()
    
    # First try regex pattern
    ticker_match = re.search(r'-([A-Z]{2,5})\.txt$', upper_filename)
    if ticker_match:
        stock_ticker = ticker_match.group(1)
    else:
        # Fallback: manual parsing for patterns like 09082025-SRPT.txt
        if upper_filename.endswith('.TXT') and '-' in upper_filename:
            parts = upper_filename.split('-')
            if len(parts) >= 2:
                last_part = parts[-1].replace('.TXT', '')
                if last_part.isalpha() and 2 <= len(last_part) <= 5:
                    stock_ticker = last_part
    
    # Single stock analysis patterns
    single_stock_patterns = [
        "Deep-dive stock analysis for traders who confuse due diligence with gambling addiction. Your 401k's worst enemy.",
        "Individual stock analysis - because diversification is for cowards and your risk tolerance knows no bounds.",
        "Stock picking guide for aspiring Warren Buffetts who lack both the patience and capital. Delusions of grandeur included.",
        "Singular equity obsession - turning one ticker into your entire personality since market open. Side effects include financial ruin.",
        "Solo stock analysis for those who believe they can outsmart the market with pure autism and determination.",
        "Individual stock breakdown - because putting all your eggs in one basket makes the inevitable crash more dramatic.",
        "Transforming sound investment strategy into pure gambling since whenever this was written.",
        "Single stock deep-dive for people whose portfolio diversification strategy is buying the same stock across multiple brokers.",
        "Individual equity analysis proving that concentration builds character and bankruptcy builds humility.",
        "Solo ticker obsession for traders who think correlation equals causation and Reddit DD equals research.",
        "Stock-specific breakdown for those who mistake YOLO investing for legitimate financial planning.",
        "Individual company analysis for people whose risk management involves prayer and positive thinking.",
        "Single equity examination proving your stock-picking skills peaked in a high school economics simulation.",
        "Focused stock analysis for traders who confuse conviction with delusion and speculation with strategy.",
        "Individual ticker deep-dive for those whose investment thesis fits on a cocktail napkin with room to spare.",
        "Solo stock evaluation proving that your fundamental analysis consists of checking if the logo looks cool.",
        "Single company breakdown for investors whose due diligence involves reading the company name twice.",
        "Individual equity assessment demonstrating why your stock picks have the longevity of mayflies.",
        "Concentrated stock analysis for people who think diversification is a French word for weakness.",
        "Single ticker investigation proving your investment research methodology involves coin flips and astrology.",
        "Individual stock examination for traders whose portfolio allocation resembles Russian roulette with extra bullets.",
        "Solo equity analysis demonstrating that your stock selection process violates multiple laws of probability.",
        "Single company deep-dive for those who confuse market timing with being chronically late to everything.",
        "Individual ticker breakdown proving your investment strategy was conceived during a mental health episode.",
        "Focused stock evaluation for people whose idea of risk assessment is asking their barista for financial advice.",
        "Solo equity examination demonstrating that your stock picks age worse than milk in Death Valley.",
        "Individual company analysis for traders who think fundamental analysis means checking if the building still exists.",
        "Single stock deep-dive proving your investment decisions are influenced more by memes than metrics.",
        "Concentrated equity breakdown for those whose portfolio management resembles abstract expressionism.",
        "Individual ticker analysis demonstrating that your stock-picking intuition has the accuracy of a broken compass.",
        "Solo stock investigation for people whose investment timeline operates on geological scales.",
        "Single company evaluation proving your equity selection process involves more hope than analysis.",
        "Individual stock assessment for traders whose due diligence consists of googling the ticker symbol once.",
        "Focused equity deep-dive demonstrating that your stock picks have the predictability of quantum mechanics.",
        "Solo ticker breakdown for those who confuse market volatility with their own emotional instability.",
        "Individual company analysis proving your investment philosophy was inspired by lottery ticket strategies.",
        "Single stock examination for people whose portfolio concentration makes a black hole look diversified.",
        "Concentrated equity evaluation demonstrating that your stock selection has the precision of a shotgun blast.",
        "Individual ticker deep-dive for traders whose risk tolerance exceeds their understanding of basic math.",
        "Solo stock analysis proving your equity picks have the structural integrity of a house of cards in a hurricane.",
        "Single company breakdown for those whose investment research involves more wishful thinking than Warren Buffett.",
        "Individual stock investigation demonstrating that your ticker selection process defies logic and common sense.",
        "Focused equity analysis for people whose stock-picking method involves throwing darts at a spinning wheel blindfolded.",
        "Solo ticker evaluation proving your individual stock obsession makes cult members look mentally stable.",
        "Single company deep-dive for traders whose equity analysis involves more prayer than a Sunday service.",
        "Individual stock assessment demonstrating that your ticker selection has the randomness of radioactive decay.",
        "Concentrated equity breakdown for those whose stock picks require more faith than organized religion.",
        "Solo stock investigation proving your individual equity analysis makes tarot card readings look scientific.",
        "Single ticker examination for people whose investment conviction exceeds their actual knowledge by several orders of magnitude.",
        "Individual company evaluation demonstrating that your stock selection process was designed by caffeinated chimpanzees.",
        "Focused stock deep-dive for traders whose equity picks have the consistency of quantum superposition.",
        "Solo ticker analysis proving your individual stock obsession violates the Geneva Convention on financial cruelty.",
        "Single company breakdown for those whose stock selection methodology involves interpreting bird flight patterns.",
        "Individual equity investigation demonstrating that your ticker analysis makes conspiracy theories look peer-reviewed.",
        "Concentrated stock evaluation for people whose investment decisions are guided by fever dreams and bad mushrooms."
    ]
    
    # Biotech-specific commentary
    biotech_patterns = [
        "Biotech gambling for pharmaceutical degenerates who think FDA approval odds are better than casino blackjack. They're not.",
        "Gene therapy speculation - because traditional investing wasn't risky enough for your taste in financial suicide.",
        "Pharmaceutical stock analysis for biotech junkies who mistake clinical trial phases for investment strategies.",
        "Drug development lottery tickets masquerading as investment opportunities. Your portfolio's medical emergency.",
        "Biotech analysis for those who think playing roulette with regulatory approval is a sound investment thesis.",
        "Medical stock breakdown - turning healthcare innovation into speculative gambling since the FDA existed.",
        "Pharmaceutical investment guide for people who confuse 'compassionate use' with what their therapist provides.",
        "Biotech sector analysis proving your drug development picks have worse success rates than medieval medicine.",
        "Gene therapy evaluation for investors whose understanding of DNA rivals their portfolio's structural integrity.",
        "Medical device analysis for those who think 'clinical trial' means experimenting with their retirement fund.",
        "Pharmaceutical gambling that makes Russian roulette look like a conservative pension strategy.",
        "Biotech investment breakdown for people whose idea of due diligence is watching House MD reruns.",
        "Drug development analysis proving your biotech picks have the approval odds of a flat-earth petition.",
        "Medical sector deep-dive for investors who confuse 'peer review' with asking their dealer for stock tips.",
        "Pharmaceutical company evaluation demonstrating that your biotech investments spread faster than hospital infections.",
        "Biotech stock analysis for those whose medical knowledge comes from WebMD and investment strategy from Reddit.",
        "Gene therapy investment guide proving your biotech picks have less scientific basis than essential oils.",
        "Medical device breakdown for people who think 'FDA approval' is what their parole officer gives them.",
        "Pharmaceutical sector research that makes thalidomide look like sound investment advice.",
        "Biotech analysis for investors whose drug development timeline operates on geological scales.",
        "Medical stock evaluation proving your pharmaceutical picks have worse side effects than the diseases they treat.",
        "Drug development deep-dive for those who confuse 'molecule' with their dealer's latest product offering.",
        "Biotech investment assessment demonstrating that your medical picks require more faith than faith healing.",
        "Pharmaceutical company analysis for people whose biotech portfolio is sicker than their actual health conditions.",
        "Gene therapy breakdown proving your biotech investments have the stability of radioactive isotopes.",
        "Medical sector investigation for traders whose pharmaceutical knowledge peaked at aspirin commercials.",
        "Biotech stock deep-dive demonstrating that your drug development picks age worse than expired medications.",
        "Pharmaceutical investment evaluation for those whose medical research consists of googling symptoms once.",
        "Medical device analysis proving your biotech selections have the precision of medieval surgical instruments.",
        "Drug development breakdown for investors whose pharmaceutical timeline resembles archaeological dating methods.",
        "Biotech sector assessment that makes snake oil salesmen look like legitimate healthcare providers.",
        "Gene therapy analysis for people whose biotech investments require more miracles than Lourdes.",
        "Medical stock investigation proving your pharmaceutical picks have worse outcomes than placebo treatments.",
        "Biotech investment deep-dive for those who think 'double-blind study' means investing while intoxicated twice.",
        "Pharmaceutical company evaluation demonstrating that your medical picks have the efficacy of homeopathic remedies.",
        "Drug development analysis for investors whose biotech research methodology involves crystal healing techniques.",
        "Medical device breakdown proving your pharmaceutical investments have less scientific support than astrology.",
        "Biotech stock assessment for people whose gene therapy knowledge comes from science fiction movies.",
        "Pharmaceutical sector deep-dive demonstrating that your medical picks violate the Hippocratic Oath of investing.",
        "Gene therapy investment investigation for those whose biotech strategy involves more hope than actual medicine.",
        "Medical stock evaluation proving your pharmaceutical selections have the approval rate of perpetual motion machines.",
        "Biotech analysis for investors whose drug development picks make medieval bloodletting look evidence-based.",
        "Pharmaceutical company breakdown demonstrating that your medical investments have worse survival rates than their patients.",
        "Medical device deep-dive for people whose biotech portfolio requires intensive care more than they do.",
        "Drug development assessment proving your pharmaceutical picks have the longevity of mayflies with terminal illnesses.",
        "Biotech sector investigation for those whose gene therapy investments are more experimental than the treatments themselves."
    ]
    
    # Tech stock patterns  
    tech_patterns = [
        "Tech stock analysis for silicon valley worshippers who think disruption equals guaranteed returns. Plot twist: it doesn't.",
        "Technology company breakdown - because someone needs to validate your FAANG obsession with pseudo-intellectual analysis.",
        "Tech equity deep-dive for those who mistake venture capital FOMO for legitimate investment research.",
        "Digital transformation stock pick - turning technological buzzwords into portfolio destruction since the dot-com bubble.",
        "Software company evaluation for people who think 'cloud computing' means doing math while high on optimism.",
        "Technology sector analysis proving your startup picks have the longevity of TikTok trends and half the substance.",
        "Tech stock breakdown for investors whose coding knowledge stops at HTML and investment knowledge never starts.",
        "Silicon Valley deep-dive for those who confuse 'user experience' with their own existential crisis management.",
        "Technology company assessment proving your tech picks age faster than smartphone batteries.",
        "Software sector evaluation for people who think 'agile methodology' describes their mental gymnastics.",
        "Tech investment guide demonstrating that your digital transformation picks transform money into digital nothing.",
        "Technology market analysis for those whose idea of disruption is losing money in innovative ways.",
        "Software company research proving your SaaS investments are about as scalable as a paper airplane.",
        "Tech stock investigation for investors who think 'machine learning' describes their own inability to learn from mistakes.",
        "Silicon Valley breakdown for people whose understanding of blockchain rivals their grasp of quantum physics.",
        "Technology sector deep-dive proving your AI investments have less intelligence than the artificial kind.",
        "Software market evaluation for those who confuse 'big data' with their investment losses.",
        "Tech company analysis demonstrating that your platform plays have the stability of a house of cards in an earthquake.",
        "Technology investment assessment for people whose venture capital instincts have the accuracy of autocorrect.",
        "Silicon Valley stock evaluation proving your tech picks have worse compatibility than Windows Vista.",
        "Software sector breakdown for investors whose cloud investments evaporate faster than morning dew.",
        "Technology company deep-dive for those who think 'going viral' is an actual business model.",
        "Tech stock analysis proving your digital innovation picks are about as revolutionary as digital pet rocks.",
        "Software market investigation for people whose cybersecurity investments are less secure than public WiFi.",
        "Technology sector assessment demonstrating that your fintech picks are about as disruptive as a polite cough.",
        "Silicon Valley evaluation for investors whose social media stock picks are more antisocial than social.",
        "Tech company breakdown proving your cryptocurrency investments have the stability of a manic-depressive.",
        "Software sector deep-dive for those whose e-commerce picks have worse delivery than the postal service.",
        "Technology investment analysis demonstrating that your gaming stocks are more of a gamble than the games themselves.",
        "Tech stock evaluation for people whose semiconductor picks conduct electricity better than they conduct profits.",
        "Silicon Valley investigation proving your biotechnology investments are sicker than their target diseases.",
        "Software company assessment for investors whose telecommunications picks communicate losses more than data.",
        "Technology sector breakdown demonstrating that your renewable energy tech picks are about as sustainable as fossil fuels.",
        "Tech market deep-dive for those whose electric vehicle investments have less range than a golf cart.",
        "Software sector evaluation proving your autonomous driving picks are more autonomous from profits than from human drivers.",
        "Technology company analysis for people whose virtual reality investments exist only in virtual portfolios.",
        "Silicon Valley breakdown demonstrating that your augmented reality picks augment nothing but your disappointment.",
        "Tech stock investigation for investors whose internet-of-things picks connect to everything except profitability.",
        "Software market assessment proving your 5G investments have worse connectivity than dial-up modems.",
        "Technology sector deep-dive for those whose quantum computing picks exist in a superposition of loss and greater loss.",
        "Tech company evaluation demonstrating that your space technology investments are more spaced out than space-bound.",
        "Silicon Valley analysis proving your drone investments crash more often than actual drones.",
        "Software sector investigation for people whose robotics picks are more robotic than the actual robots.",
        "Technology investment breakdown demonstrating that your nanotechnology picks have macro-sized losses.",
        "Tech stock deep-dive for those whose 3D printing investments exist only in two dimensions: width and loss."
    ]
    
    # Base witty descriptions for general content
    general_descriptions = [
        "Market autism dissected with surgical precision for your viewing displeasure. Because someone needs to document the financial apocalypse in real-time.",
        "Statistical anomaly hunting for degenerate traders who think patterns in chaos make them Warren Buffett. Spoiler: they don't.",
        "VaR analysis for masochists who enjoy quantifying exactly how their portfolios will implode. Because ignorance was never bliss in finance.",
        "Investment recommendations from the digital wasteland where reality meets mathematical suffering. Your broker's nightmares made manifest.",
        "Darwinex outlier analysis that'll make your risk manager quit and your compliance officer weep. Not for the financially faint of heart.",
        "Deep dive into market mechanics for traders who mistake spreadsheet autism for genuine market insight. Results may vary drastically.",
        "Financial analysis weaponized for maximum psychological damage. Watch your investment thesis crumble in real-time algorithmic glory.",
        "Market wizardry that separates actionable opportunities from close-only traps in the statistical anomaly wasteland of modern trading.",
        "Investment strategy deconstruction for people whose portfolio allocation resembles abstract expressionist art.",
        "Financial market dissection proving that your trading algorithm was coded by caffeinated hamsters with commitment issues.",
        "Market analysis for degenerates who confuse correlation with causation and think backtesting equals prophecy.",
        "Investment research that makes peer review look like a popularity contest among the intellectually disabled.",
        "Trading strategy breakdown for people whose risk management consists of prayer and positive affirmations.",
        "Financial sector analysis demonstrating that your investment philosophy violates several laws of physics.",
        "Market evaluation for those whose portfolio diversification strategy involves different ways to lose money.",
        "Investment opportunity assessment proving your due diligence methodology involves coin flips and astrology.",
        "Trading analysis for people who think fundamental analysis means checking if the company name sounds familiar.",
        "Financial market research that makes conspiracy theories look peer-reviewed and evidence-based.",
        "Investment strategy evaluation for those whose market timing has the accuracy of a broken sundial.",
        "Market sector breakdown proving your asset allocation was determined by throwing darts at a spinning wheel.",
        "Financial analysis for investors whose economic forecasting involves reading tea leaves and chicken entrails.",
        "Trading opportunity investigation demonstrating that your investment decisions are guided by fever dreams.",
        "Market research for people whose portfolio rebalancing involves drinking until the numbers look better.",
        "Investment evaluation proving your financial planning makes a Ponzi scheme look structurally sound.",
        "Trading strategy assessment for those whose risk tolerance exceeds their understanding by several orders of magnitude.",
        "Financial sector deep-dive demonstrating that your market analysis involves more hope than actual analysis.",
        "Investment research breakdown for people whose economic theory was inspired by a lobotomized textbook.",
        "Market analysis for traders whose investment timeline operates on geological rather than fiscal years.",
        "Financial evaluation proving your trading strategy has the precision of a shotgun blast in complete darkness.",
        "Investment opportunity dissection for those whose portfolio management makes abstract art look structured.",
        "Trading analysis demonstrating that your market predictions have the accuracy of a blindfolded meteorologist.",
        "Financial research for people whose investment philosophy was conceived during a psychotic episode.",
        "Market sector evaluation proving your economic insights have the depth of a puddle in Death Valley.",
        "Investment strategy investigation for those whose financial decision-making process involves more coin flips than analysis.",
        "Trading opportunity breakdown demonstrating that your market research consists of asking your pet for advice.",
        "Financial analysis for investors whose economic understanding peaked at lemonade stand operations.",
        "Market evaluation proving your investment approach violates the Geneva Convention on financial cruelty.",
        "Trading strategy deep-dive for people whose portfolio allocation resembles a toddler's finger painting.",
        "Financial sector assessment demonstrating that your market timing has the effectiveness of a chocolate teapot.",
        "Investment research for those whose economic forecasting makes weather prediction look scientifically rigorous.",
        "Market analysis proving your trading decisions are influenced more by lunar cycles than market cycles.",
        "Financial evaluation for people whose investment strategy was outsourced to a committee of caffeinated squirrels.",
        "Trading opportunity investigation demonstrating that your market insights have the credibility of flat-earth theory.",
        "Investment strategy breakdown for those whose financial planning horizon extends to next week's lottery drawing.",
        "Market research proving your economic analysis makes medieval alchemy look like modern chemistry."
    ]
    
    # Smart content-specific detection
    if stock_ticker and len(stock_ticker) <= 5:
        # It's likely a single stock analysis
        if any(biotech_word in content_lower for biotech_word in ['gene therapy', 'fda', 'clinical trial', 'biotech', 'pharmaceutical', 'drug', 'therapy']):
            return select_unused_flavor_text(biotech_patterns, "Biotech analysis for pharmaceutical degenerates who think FDA approval odds are better than casino blackjack.")
        elif any(tech_word in content_lower for tech_word in ['software', 'saas', 'cloud', 'ai', 'artificial intelligence', 'tech', 'platform']):
            return select_unused_flavor_text(tech_patterns, "Tech stock analysis for silicon valley worshippers who think disruption equals guaranteed returns.")
        else:
            return select_unused_flavor_text(single_stock_patterns, "Individual stock analysis - because diversification is for cowards and your risk tolerance knows no bounds.")
    
    # Content-specific descriptions for non-single-stock analysis
    elif 'darwinex' in content_lower and 'outlier' in content_lower:
        return "Deep dive into Darwinex VaR/Ask outlier analysis - separating actionable opportunities from close-only traps in the statistical anomaly wasteland."
    elif 'investment' in content_lower and 'recommendation' in content_lower:
        return "Investment recommendations from the digital wasteland where mathematical precision meets portfolio carnage. Your risk manager's worst nightmare."
    elif 'var' in content_lower or 'value at risk' in content_lower:
        return "VaR analysis for masochists who enjoy quantifying exactly how their portfolios will implode. Because ignorance was never bliss in finance."
    elif 'analysis' in content_lower and 'market' in content_lower:
        return "Market autism dissected with surgical precision for your viewing displeasure. Because someone needs to document the financial apocalypse."
    elif 'trade' in content_lower or 'trading' in content_lower:
        return "Trading insights that'll make your broker weep and your compliance officer question their life choices. Not for the mentally stable."
    elif 'statistical' in content_lower or 'outlier' in content_lower:
        return "Statistical anomaly hunting for degenerate traders who think patterns in chaos make them Warren Buffett. Reality check included."
    else:
        # Fallback: pick a random general description
        return select_unused_flavor_text(general_descriptions, "Market autism dissected with surgical precision for your viewing displeasure.")


def extract_title_and_summary(content, filename):
    """Extract title and summary from content"""
    lines = content.split('\n')
    
    # Try to extract date from filename
    date_match = re.search(r'(\d{8})', filename)
    date_str = ""
    if date_match:
        date_raw = date_match.group(1)
        try:
            date_obj = datetime.strptime(date_raw, '%m%d%Y')
            date_str = date_obj.strftime('%B %d, %Y')
        except:
            date_str = date_raw
    
    # Extract stock ticker from filename if present (e.g., SRPT from 09082025-SRPT.txt)
    stock_ticker = None
    upper_filename = filename.upper()
    
    # First try regex pattern  
    ticker_match = re.search(r'-([A-Z]{2,5})\.txt$', upper_filename)
    if ticker_match:
        stock_ticker = ticker_match.group(1)
    else:
        # Fallback: manual parsing for patterns like 09082025-SRPT.txt
        if upper_filename.endswith('.TXT') and '-' in upper_filename:
            parts = upper_filename.split('-')
            if len(parts) >= 2:
                last_part = parts[-1].replace('.TXT', '')
                if last_part.isalpha() and 2 <= len(last_part) <= 5:
                    stock_ticker = last_part
    
    # Look for title patterns in content
    title = "Market Analysis"
    section_title = "📊 MARKET ANALYSIS"
    
    # Check the entire content for keywords, not just first 20 lines
    content_lower = content.lower()
    
    # Individual stock analysis detection (highest priority)
    if stock_ticker and len(stock_ticker) <= 5:
        # Look for company name in first few lines
        company_name = None
        for line in lines[:10]:
            line_clean = line.strip().upper()
            if stock_ticker in line_clean and '-' in line_clean:
                # Extract company name after ticker
                parts = line_clean.split('-', 1)
                if len(parts) > 1:
                    company_name = parts[1].strip().title()
                    # Clean up common formatting
                    company_name = company_name.replace(':', '').strip()
                    break
        
        if company_name:
            title = f"{stock_ticker} - {company_name} Analysis"
            # Determine sector-specific emoji and section title
            if any(biotech_word in content_lower for biotech_word in ['gene therapy', 'fda', 'clinical trial', 'biotech', 'pharmaceutical', 'drug', 'therapy']):
                section_title = f"🧬 {stock_ticker} BIOTECH DEEP DIVE"
            elif any(tech_word in content_lower for tech_word in ['software', 'saas', 'cloud', 'ai', 'artificial intelligence', 'tech', 'platform']):
                section_title = f"💻 {stock_ticker} TECH ANALYSIS"
            elif any(finance_word in content_lower for finance_word in ['bank', 'financial', 'credit', 'lending', 'fintech']):
                section_title = f"🏦 {stock_ticker} FINANCIAL BREAKDOWN"
            elif any(energy_word in content_lower for energy_word in ['oil', 'gas', 'energy', 'renewable', 'solar', 'wind']):
                section_title = f"⚡ {stock_ticker} ENERGY ANALYSIS"
            else:
                section_title = f"📈 {stock_ticker} INDIVIDUAL STOCK ANALYSIS"
        else:
            title = f"{stock_ticker} Stock Analysis - {date_str}" if date_str else f"{stock_ticker} Stock Analysis"
            section_title = f"📈 {stock_ticker} INDIVIDUAL STOCK ANALYSIS"
    
    # Darwinex outlier analysis
    elif 'darwinex' in filename.lower() and 'outlier' in filename.lower():
        title = "Claude x Darwinex Outlier Analysis"
        section_title = "🎯 REVISED DARWINEX UNIVERSE INVESTMENT RECOMMENDATIONS"
    elif 'investment' in filename.lower():
        title = f"Investment Analysis - {date_str}" if date_str else "Investment Analysis"  
        section_title = "📊 INVESTMENT RECOMMENDATIONS"
    # Then check content for patterns
    elif 'darwinex' in content_lower and 'outlier' in content_lower:
        title = "Claude x Darwinex Outlier Analysis"
        section_title = "🎯 REVISED DARWINEX UNIVERSE INVESTMENT RECOMMENDATIONS"
    elif 'investment' in content_lower and any(word in content_lower for word in ['recommendation', 'analysis', 'buying', 'selling']):
        title = f"Investment Analysis - {date_str}" if date_str else "Investment Analysis"
        section_title = "📊 INVESTMENT RECOMMENDATIONS"
    
    # Fallback: check first 20 lines for bullet points or other patterns
    if title == "Market Analysis":  # Only if we haven't found a better title yet
        for line in lines[:20]:
            line = line.strip()
            if not line:
                continue
                
            # Look for bullet points that could be titles (but skip commands)
            if line.startswith('●') and len(line) > 10:
                clean_line = line.replace('●', '').strip()
                # Skip if it looks like a command or technical output
                if not any(cmd in clean_line.lower() for cmd in ['bash(', 'read(', '⎿', 'ls -', 'find ', 'grep ', 'python ']):
                    if len(clean_line) < 80 and not clean_line.startswith('I'):
                        title = clean_line
                        break
    
    # Generate witty summary based on content
    summary = generate_witty_description(content, filename, title)
    
    return title, summary, section_title


def generate_html_from_txt(txt_path, force_regenerate=False):
    """Generate HTML file from text file"""
    txt_file = Path(txt_path)
    html_file = txt_file.with_suffix('.html')
    
    # Skip if HTML already exists and is newer (unless force regeneration)
    if not force_regenerate and html_file.exists() and html_file.stat().st_mtime > txt_file.stat().st_mtime:
        print(f"Skipping {txt_file.name} - HTML is up to date")
        return str(html_file)
    
    # Read text content
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata
    title, summary, section_title = extract_title_and_summary(content, txt_file.name)
    
    # Generate consistent flavor text for this blog post
    flavor_text = get_consistent_flavor_text(html_file.name, title)
    
    # Generate HTML
    html_content = BLOG_POST_TEMPLATE.format(
        title=title,
        description=flavor_text,  # Use position-specific flavor text instead of generic summary
        filename=html_file.name,
        section_title=section_title,
        summary=summary,
        txt_filename=txt_file.name
    )
    
    # Write HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated {html_file.name}")
    return str(html_file)


def parse_existing_blog_entries():
    """Parse existing blog entries from blog.html"""
    existing_entries = []
    
    try:
        with open(BLOG_INDEX, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract existing blog entries using regex
        pattern = r'<div class="blog-entry">\s*<a href="https://marketwizardry\.org/blog/([^"]+)">([^<]+)</a>\s*<span class="date">Posted: ([^<]+)</span>\s*</div>'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        for filename, title, date in matches:
            existing_entries.append({
                'filename': filename.strip(),
                'title': title.strip(),
                'date': date.strip(),
                'source': 'existing'
            })
        
        print(f"Found {len(existing_entries)} existing blog entries")
        return existing_entries
        
    except FileNotFoundError:
        print(f"{BLOG_INDEX} not found, will create new one")
        return []


def update_blog_index(all_new_entries):
    """Update blog.html with all entries (replaces existing ones with updated flavor text)"""
    
    # Sort by date (newest first)
    all_new_entries.sort(key=lambda x: x['date'], reverse=True)
    
    print(f"Updating blog with {len(all_new_entries)} total entries")
    
    # All entries now have flavor text, so we use them all
    all_entries = all_new_entries
    
    
    # Read current blog.html
    with open(BLOG_INDEX, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Generate entries HTML for all entries
    entries_html = []
    for entry in all_entries:
        # Add flavor text description for ALL entries
        description_html = ""
        if 'summary' in entry and entry['summary']:
            description_html = f'<div class="entry-description">{entry["summary"]}</div>'
        
        entry_html = f'''            <div class="blog-entry" onclick="window.open('https://marketwizardry.org/blog/{entry['filename']}', '_blank')">
                <a href="https://marketwizardry.org/blog/{entry['filename']}" onclick="event.stopPropagation()">{entry['title']}</a>
                <span class="date">Posted: {entry['date']}</span>{description_html}
            </div>'''
        entries_html.append(entry_html)
    
    entries_section = '\n'.join(entries_html)
    
    # Replace the grid content
    pattern = r'(<div class="grid">)(.*?)(</div>\s*</div>\s*</body>)'
    replacement = f'\\1\n{entries_section}\n        \\3'
    
    new_content = re.sub(pattern, replacement, current_content, flags=re.DOTALL)
    
    # Write updated blog.html
    with open(BLOG_INDEX, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {BLOG_INDEX} with {len(all_entries)} total entries (all with flavor text)")


def extract_title_from_html(html_file):
    """Extract title from existing HTML file, with enhanced company detection"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to extract title from <title> tag
        title_match = re.search(r'<title[^>]*>MarketWizardry\.org \| ([^<]+)</title>', content)
        if title_match:
            title = title_match.group(1)
            # Check if we have a generic title but specific ticker content
            if title == "Market Analysis":
                # Check for corresponding .txt file for more specific context
                txt_file = str(html_file).replace('.html', '.txt')
                if os.path.exists(txt_file):
                    try:
                        with open(txt_file, 'r', encoding='utf-8') as tf:
                            txt_content = tf.read()[:500]  # First 500 chars
                            # Look for company names in text content
                            if 'citigroup' in txt_content.lower() or 'CITIGROUP' in txt_content:
                                return "Citigroup Analysis"
                            elif 'sarepta' in txt_content.lower() or 'SRPT' in txt_content:
                                return "SRPT - Sarepta Therapeutics Analysis"  
                            # Add more company detection as needed
                    except:
                        pass
            return title
        
        # Fallback to h1 tag
        h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
        if h1_match:
            return h1_match.group(1)
        
        # Last resort - use filename
        return Path(html_file).stem.replace('-', ' ').title()
    except Exception as e:
        print(f"Error extracting title from {html_file}: {e}")
        return Path(html_file).stem.replace('-', ' ').title()

def detect_position_content(title, filename, txt_content=""):
    """Detect if blog post contains active position recommendations"""
    filename_lower = filename.lower()
    
    # Primary detection: Check for "Active_Positions" in filename
    if "active_positions" in filename_lower:
        return True
    
    # Secondary detection: Scan for stock symbols in content if we have txt content
    if txt_content:
        content_lower = txt_content.lower()
        # Use comprehensive Darwinex symbols for detection
        symbol_count = sum(1 for symbol in DARWINEX_SYMBOLS if symbol in content_lower)
        
        # If multiple symbols mentioned + position keywords, likely active positions
        position_keywords = [
            'actionable', 'buy', 'sell', 'target', 'upside', 'position', 'allocation',
            'entry', 'exit', 'recommendation', 'thesis', 'catalyst', 'price target'
        ]
        
        position_keyword_count = sum(1 for keyword in position_keywords if keyword in content_lower)
        
        # Multiple symbols + position language = active positions
        if symbol_count >= 3 and position_keyword_count >= 2:
            return True
    
    return False

def generate_flavor_text(title, filename):
    """Generate sarcastic flavor text based on content type with RNG variety"""
    title_lower = title.lower()
    filename_lower = filename.lower()
    
    # Check if we can read the txt content for better position detection
    txt_content = ""
    try:
        txt_file = str(filename).replace('.html', '.txt')
        if not txt_file.endswith('.txt'):
            txt_file = f"blog/{filename.replace('.html', '.txt')}"
        
        if os.path.exists(txt_file):
            with open(txt_file, 'r', encoding='utf-8') as f:
                txt_content = f.read()[:2000]  # First 2000 chars for detection
    except Exception:
        pass
    
    # Check for GPU content first (highest priority for hardware analysis)
    if 'gpu' in title_lower or 'gpu' in filename_lower or ('buyers' in title_lower and 'guide' in title_lower):
        return "Hardware analysis for degenerates who confuse graphics cards with investment vehicles. Your wallet's funeral service."
    
    # Check for active position content first (highest priority)
    if detect_position_content(title_lower, filename_lower, txt_content):
        position_texts = [
            "Trading signals for ICT cultists who think 'liquidity pools' are where their money goes to drown.",
            "Position analysis for YouTube signal followers whose risk management strategy is copying random Discord screenshots.",
            "Active positions for people who pay $2000 to learn that 'supply and demand' exists, then act surprised when they lose money.",
            "Investment signals for degenerates who think following Tori Trades makes them professional futures traders.",
            "Trading recommendations for signal sheep whose market analysis consists of waiting for uncle ICT's next tweet.",
            "Position management for fake guru disciples who believe 'market structure' is a mystical concept worth $5000 courses.",
            "Active trading strategies for people whose entire education comes from YouTube thumbnails with red arrows and shocked faces.",
            "Investment thesis for signal followers who think 'Smart Money' is an actual person sending them buy alerts.",
            "Trading opportunities for ICT zombies who recite 'order blocks' like religious mantras while hemorrhaging cash.",
            "Position analysis for course buyers who spent more on trading education than actual trading capital.",
            "Active positions for people who think copying signals from @FakeGuru69 on Telegram constitutes a business plan.",
            "Trading signals for degenerates who confuse backtested results on demo accounts with actual profitability.",
            "Investment recommendations for signal chasers whose portfolio performance makes lottery tickets look like sound investments.",
            "Position management for people who believe every 20-pip winner screenshot on Instagram represents sustainable trading.",
            "Active trading guide for signal followers who think 'risk management' means only risking money they can afford to lose to scammers.",
            "Trading thesis for ICT disciples whose understanding of market manipulation comes from YouTube conspiracy videos.",
            "Position analysis for fake guru victims who pay monthly subscriptions to lose money more efficiently.",
            "Investment signals for people who think 'order flow' is the queue at their local unemployment office.",
            "Active positions for signal sheep who mistake correlation between red arrows and account liquidation for causation.",
            "Trading recommendations for course addicts who collect more certificates than profitable trades.",
            "Position signals for algorithmic trading wannabes whose Python skills peaked at print('Hello World').",
            "Active trading analysis for people who think 'backtesting' means testing how far back their losses go.",
            "Investment positions for signal chasers who confuse Discord notifications with divine intervention.",
            "Trading opportunities for retail traders whose institutional knowledge comes from TikTok influencers.",
            "Position management for people who think 'drawdown' is what happens when they withdraw money.",
            "Active signals for forex degenerates who believe leverage is just another word for 'easy money'.",
            "Trading analysis for signal followers whose market timing has the accuracy of a broken stopwatch.",
            "Investment positions for course junkies who think 'paper trading' means trading on actual paper.",
            "Position signals for people whose trading psychology involves more therapy than their actual therapist provides.",
            "Active trading guide for signal sheep whose risk-reward ratio is consistently negative infinity.",
            "Trading opportunities for fake guru disciples who pay for signals like they're paying for salvation.",
            "Investment analysis for signal chasers whose portfolio diversification means following multiple scammers.",
            "Position management for people who think 'stop loss' is what happens when they run out of money.",
            "Active signals for trading addicts whose withdrawal symptoms involve checking charts every 30 seconds.",
            "Trading recommendations for signal followers who confuse volatility with opportunity and disaster with learning experience.",
            "Investment positions for people whose trading journal reads like a suicide note with charts.",
            "Position analysis for signal sheep whose market research involves reading YouTube comments sections.",
            "Active trading strategies for people who think 'diamond hands' is medical advice for arthritic grip strength.",
            "Trading signals for retail degenerates whose institutional connections extend to following banks on Twitter.",
            "Investment opportunities for signal chasers who mistake FOMO for fundamental analysis.",
            "Position management for people whose trading plan involves prayer and positive affirmations.",
            "Active signals for course buyers whose education costs exceed their net worth by several orders of magnitude.",
            "Trading analysis for signal followers whose market predictions have the accuracy of weather forecasting in chaos theory.",
            "Investment positions for people who think 'market makers' are the people who make markets at grocery stores.",
            "Position signals for trading enthusiasts whose understanding of economics peaked at supply and demand graphs.",
            "Active trading guide for signal sheep whose portfolio allocation resembles a toddler's crayon drawing.",
            "Trading opportunities for fake guru victims whose financial advisor is a YouTube algorithm.",
            "Investment analysis for signal chasers who confuse correlation with causation and luck with skill.",
            "Position management for people whose risk assessment involves asking Magic 8-Balls for financial advice.",
            "Active signals for trading degenerates whose market timing strategy involves astrological consultations.",
            "Trading recommendations for signal followers who think 'due diligence' is what they owe after being late.",
            "Investment positions for people whose trading education involves more YouTube ads than actual content.",
            "Position analysis for signal sheep whose market analysis involves interpreting candlestick patterns like tea leaves.",
            "Active trading strategies for people whose portfolio performance makes gambling addiction look profitable.",
            "Trading signals for signal chasers who mistake screenshots of profits for actual business plans.",
            "Investment opportunities for fake guru disciples whose trading account is smaller than their course payment receipts.",
            "Position management for people who think 'margin call' is when their dealer demands payment.",
            "Active signals for trading addicts whose investment timeline is measured in dopamine hits rather than fiscal quarters.",
            "Trading analysis for signal followers whose market research consists of copying and pasting from Telegram groups.",
            "Investment positions for people whose trading psychology requires more medication than their actual mental health.",
            "Position signals for signal sheep whose understanding of market manipulation comes from conspiracy theory forums.",
            "Active trading guide for people whose risk management strategy involves hiding money under different mattresses.",
            "Trading opportunities for signal chasers whose portfolio diversification means losing money in multiple currencies simultaneously.",
            "Investment analysis for fake guru victims whose trading education is more expensive than their actual trading capital.",
            "Position management for people who confuse 'bull market' with the livestock they're about to be financially slaughtered like."
        ]
        return select_unused_flavor_text(position_texts, "Trading signals for ICT cultists who think 'liquidity pools' are where their money goes to drown.")
    
    # Industry/Sector-specific Sam Hyde-esque flavor texts
    sector_texts = {
        'biotech': [
            "Biotech analysis for those who think playing roulette with regulatory approval is a sound investment thesis.",
            "Pharmaceutical gambling for people who confuse FDA rejection with personal validation.",
            "Drug development analysis for masochists who enjoy watching molecules burn through cash faster than a crackhead.",
            "Biotech investment guide for degenerates who think 'clinical trial' means experimenting with their life savings.",
            "Medical research funding analysis that makes Russian roulette look like a conservative retirement strategy.",
            "Biotechnology reports for people whose idea of diversification is losing money in multiple drug trials simultaneously.",
            "Pharmaceutical sector breakdown for those who think 'peer review' means asking their dealer for investment advice.",
            "Biotech market analysis for investors whose risk tolerance rivals a lab rat's survival instinct.",
            "Drug development metrics for people who confuse 'phase trials' with the stages of financial grief.",
            "Medical sector evaluation that proves your biotech picks have the success rate of a blindfolded surgeon.",
            "Pharmaceutical investment thesis for those who think 'compassionate use' refers to their broker's pity.",
            "Biotech analysis proving your due diligence involves reading WebMD and calling it research.",
            "Medical device evaluation for people who think 'regulatory approval' is what their therapist gives them.",
            "Pharmaceutical sector deep-dive for investors whose portfolio strategy resembles human experimentation.",
            "Biotech market research that makes gambling addiction look like responsible financial planning.",
            "Gene therapy investment guide for people whose DNA understanding rivals their portfolio's structural integrity.",
            "Pharmaceutical sector evaluation proving your biotech picks have worse side effects than the diseases they treat.",
            "Medical device analysis for investors whose surgical precision in stock picking resembles medieval bloodletting.",
            "Biotech company assessment that makes snake oil salesmen look like legitimate healthcare providers.",
            "Drug development deep-dive for those whose molecular knowledge comes from high school chemistry nightmares.",
            "Pharmaceutical market breakdown proving your biotech investments spread faster than antibiotic-resistant infections.",
            "Medical research analysis for people whose lab safety involves more hope than actual protective equipment.",
            "Biotech sector investigation for investors whose clinical understanding peaked at band-aid application.",
            "Pharmaceutical investment evaluation proving your drug picks have the approval odds of perpetual motion machines.",
            "Medical device sector analysis for those whose biotech strategy requires more miracles than faith healing.",
            "Gene therapy market research demonstrating that your pharmaceutical picks violate the Hippocratic Oath.",
            "Biotech investment breakdown for people whose medical knowledge comes from watching Grey's Anatomy reruns.",
            "Drug development sector evaluation proving your biotech selections have the efficacy of homeopathic remedies.",
            "Pharmaceutical company deep-dive for investors whose regulatory understanding involves crystal healing techniques.",
            "Medical device market analysis that makes medieval medical practices look evidence-based.",
            "Biotech sector assessment for people whose gene therapy investments are more experimental than the treatments.",
            "Pharmaceutical investment investigation proving your medical picks have worse survival rates than their patients.",
            "Drug development analysis for investors whose biotech portfolio requires intensive care units.",
            "Medical research sector breakdown demonstrating that your pharmaceutical timeline operates on archaeological scales.",
            "Biotech market evaluation for people whose clinical trials involve more gambling than actual science.",
            "Pharmaceutical sector deep-dive proving your drug development picks age worse than expired medications.",
            "Medical device investment analysis for those whose biotech research methodology involves tarot cards.",
            "Gene therapy sector evaluation demonstrating that your pharmaceutical investments have the stability of radioactive waste.",
            "Biotech company investigation for people whose medical device knowledge comes from horror movie props.",
            "Drug development market analysis proving your pharmaceutical picks have the precision of medieval surgical tools.",
            "Medical research investment breakdown for investors whose biotech education peaked at first aid certification."
        ],
        'tech': [
            "Technology sector analysis for people who think 'cloud computing' means doing math while high.",
            "Software company evaluation for degenerates who confuse 'user experience' with their own existential crisis.",
            "Tech stock breakdown for investors whose coding knowledge stops at HTML and their investment knowledge doesn't start.",
            "Technology market analysis proving your startup picks have the longevity of a TikTok trend.",
            "Software sector research for people who think 'agile methodology' describes their mental gymnastics.",
            "Tech investment guide for those whose idea of disruption is losing money in innovative ways.",
            "Technology company assessment for investors who think 'scalability' means how badly they can fuck up.",
            "Software market evaluation that demonstrates your tech picks age worse than milk in Arizona.",
            "Technology sector deep-dive for people who confuse 'machine learning' with their own inability to learn.",
            "Tech stock analysis for investors whose understanding of 'blockchain' rivals a boomer's grasp of Instagram.",
            "Software company research proving your venture capital instincts have the accuracy of autocorrect.",
            "Technology market breakdown for those who think 'artificial intelligence' describes their investment strategy.",
            "Tech sector evaluation for people whose portfolio diversification means losing money across different apps.",
            "Software investment analysis that makes dot-com bubble investors look like financial geniuses.",
            "Technology company metrics for those who think 'going viral' is an IPO strategy.",
            "Silicon Valley analysis for people whose platform plays have the stability of a house of cards in an earthquake.",
            "Software sector breakdown proving your SaaS investments are about as scalable as a paper airplane.",
            "Technology investment evaluation for those whose digital transformation picks transform money into digital nothing.",
            "Tech company deep-dive for investors who think 'big data' refers to their investment losses.",
            "Software market investigation proving your cybersecurity picks are less secure than public WiFi passwords.",
            "Technology sector assessment demonstrating that your fintech investments are about as disruptive as a polite cough.",
            "Silicon Valley breakdown for people whose social media stock picks are more antisocial than social.",
            "Software company analysis proving your cryptocurrency investments have the stability of a manic episode.",
            "Tech market evaluation for investors whose e-commerce picks have worse delivery than the postal service.",
            "Technology investment deep-dive demonstrating that your gaming stocks are more of a gamble than the games themselves.",
            "Software sector investigation for people whose semiconductor picks conduct electricity better than profits.",
            "Tech company assessment proving your telecommunications picks communicate losses more effectively than data.",
            "Technology market breakdown for investors whose renewable energy tech picks are about as sustainable as fossil fuels.",
            "Silicon Valley evaluation demonstrating that your electric vehicle investments have less range than golf cart batteries.",
            "Software sector deep-dive for people whose autonomous driving picks are more autonomous from profits than passengers.",
            "Technology company investigation proving your virtual reality investments exist only in virtual portfolios.",
            "Tech market analysis for investors whose augmented reality picks augment nothing but disappointment levels.",
            "Software investment breakdown demonstrating that your internet-of-things picks connect to everything except profitability.",
            "Technology sector evaluation for people whose 5G investments have worse connectivity than dial-up modems.",
            "Silicon Valley deep-dive proving your quantum computing picks exist in superposition of loss and greater loss.",
            "Software company assessment for investors whose space technology picks are more spaced out than space-bound.",
            "Tech sector investigation demonstrating that your drone investments crash more often than actual drones.",
            "Technology market evaluation for people whose robotics picks are more robotic than the actual robots.",
            "Software investment analysis proving your nanotechnology picks have macro-sized losses and nano-sized returns.",
            "Tech company breakdown for investors whose 3D printing picks exist only in two dimensions: width and loss.",
            "Silicon Valley assessment demonstrating that your biotech software picks are sicker than their target diseases."
        ],
        'energy': [
            "Energy sector analysis for people who think 'renewable' describes their ability to lose money repeatedly.",
            "Oil and gas evaluation for investors whose environmental consciousness stops at their portfolio's carbon footprint.",
            "Energy market breakdown proving your fossil fuel picks have the future prospects of a coal-powered iPhone.",
            "Renewable energy analysis for those who think 'solar power' refers to the brightness of their financial losses.",
            "Energy company assessment for investors who confuse 'fracking' with what they're doing to their retirement fund.",
            "Oil sector research that demonstrates your energy picks have less stability than a meth lab.",
            "Energy investment guide for people whose idea of green energy is the color of their portfolio losses.",
            "Power sector evaluation for those who think 'grid stability' describes their mental state during market crashes.",
            "Energy market analysis proving your utility investments are about as reliable as Texas power grid.",
            "Renewable sector breakdown for investors who think 'wind power' means the hot air from their financial advisor.",
            "Energy company research for those whose carbon footprint is smaller than their investment losses.",
            "Oil and gas metrics that make Enron executives look like ethical role models.",
            "Energy sector deep-dive for people who confuse 'pipeline' with their dealer's supply chain.",
            "Renewable energy evaluation proving your ESG investments are as sustainable as a paper straw in a hurricane.",
            "Power sector analysis for investors whose energy portfolio burns cleaner than their money.",
            "Solar energy investment guide for people whose renewable picks have less efficiency than actual photosynthesis.",
            "Oil company breakdown proving your petroleum investments leak value faster than the Exxon Valdez.",
            "Energy sector investigation for investors whose nuclear picks are more toxic than actual radioactive waste.",
            "Wind power analysis demonstrating that your renewable investments blow harder than hurricane-force losses.",
            "Energy market deep-dive for people whose utility picks have less power than a dying smartphone battery.",
            "Oil and gas sector evaluation proving your extraction investments extract losses more efficiently than crude.",
            "Renewable energy breakdown for investors whose green technology picks are about as eco-friendly as coal plants.",
            "Energy company assessment demonstrating that your power investments have less current than broken electrical outlets.",
            "Solar sector investigation for people whose photovoltaic picks convert sunlight to losses with remarkable efficiency.",
            "Energy investment analysis proving your hydroelectric selections have the flow rate of constipated rivers.",
            "Oil sector deep-dive for investors whose refinery picks process crude more slowly than their own mental processing.",
            "Energy market evaluation demonstrating that your geothermal investments are hotter garbage than actual geothermal vents.",
            "Renewable sector breakdown for people whose biofuel picks are more organic than their investment strategy.",
            "Energy company investigation proving your natural gas selections are more volatile than the actual commodity.",
            "Power sector analysis for investors whose energy storage picks hold value about as well as leaky batteries.",
            "Oil and gas market assessment demonstrating that your exploration investments discover losses more than oil reserves.",
            "Energy investment deep-dive for people whose clean energy picks are dirtier than the industries they replace."
        ],
        'finance': [
            "Financial sector analysis for people who think 'compound interest' is what banks charge for complicated questions.",
            "Banking evaluation for investors whose credit score has more stability than their stock picks.",
            "Financial services breakdown proving your fintech investments have the innovation of a rotary phone.",
            "Banking sector research for those who confuse 'liquid assets' with their drinking problem.",
            "Financial company assessment that demonstrates your bank picks have less security than a screen door.",
            "Insurance sector analysis for people whose risk management strategy is 'hope and pray'.",
            "Financial services evaluation proving your investment banking knowledge comes from Wolf of Wall Street.",
            "Banking market research for those who think 'derivatives' are what you get from calculus class.",
            "Financial sector deep-dive for investors whose portfolio diversification resembles a Ponzi scheme.",
            "Insurance company metrics that make AIG executives look like conservative risk managers.",
            "Banking analysis for people who confuse 'mortgage backed securities' with home improvement loans.",
            "Financial services breakdown for those whose credit union investments are union with poverty.",
            "Banking sector evaluation proving your fintech picks are as revolutionary as digital pet rocks.",
            "Financial company research for investors whose money laundering knowledge is purely theoretical.",
            "Insurance sector analysis that makes Bernie Madoff look like a legitimate financial advisor."
        ],
        'retail': [
            "Retail sector analysis for people who think 'brick and mortar' describes their investment foundation.",
            "Consumer goods evaluation for investors whose shopping addiction funds their portfolio losses.",
            "Retail market breakdown proving your e-commerce picks have the longevity of a mall in 2024.",
            "Consumer sector research for those who confuse 'market penetration' with their own financial violation.",
            "Retail company assessment demonstrating your fashion picks have less style than a Walmart clearance rack.",
            "Consumer goods analysis for people whose brand loyalty extends only to their loss-making stocks.",
            "Retail investment guide for those who think 'omnichannel' means losing money everywhere simultaneously.",
            "Consumer market evaluation proving your luxury brand picks are as exclusive as a Dollar Tree inventory.",
            "Retail sector deep-dive for investors whose consumer insight comes from TikTok shopping hauls.",
            "Consumer goods metrics that make retail apocalypse survivors look like Warren Buffett.",
            "Retail analysis for people who confuse 'supply chain disruption' with their own life choices.",
            "Consumer sector breakdown for those whose idea of market research is reading Yelp reviews.",
            "Retail company evaluation proving your department store picks have the future of a Blockbuster franchise.",
            "Consumer goods research for investors whose retail therapy bankrolls their investment trauma.",
            "Retail market analysis that makes GameStop squeeze participants look like seasoned professionals."
        ],
        'semiconductor': [
            "Semiconductor analysis for people who think 'chip shortage' describes their investment portfolio's intellectual capacity.",
            "Microprocessor market evaluation for investors whose understanding of silicon rivals their understanding of success.",
            "Semiconductor sector breakdown proving your chip picks have less processing power than a potato battery.",
            "Silicon valley analysis for those who confuse 'wafer fabrication' with cooking show terminology.",
            "Chip manufacturer assessment demonstrating your semiconductor investments are about as cutting-edge as a Nokia 3310.",
            "Microelectronics research for people whose idea of Moore's Law is 'more losses, more problems'.",
            "Semiconductor market deep-dive for investors who think 'nanometer process' describes their portfolio's growth trajectory.",
            "Silicon sector evaluation proving your tech hardware picks have the lifespan of a fruit fly.",
            "Chip industry analysis for those whose semiconductor knowledge comes from watching Iron Man movies.",
            "Microprocessor investment guide that makes Intel's Pentium FDIV bug look like a minor arithmetic error.",
            "Semiconductor company metrics for people who confuse 'yield' with what they're lacking in returns.",
            "Silicon market breakdown for investors whose chip investments are about as stable as overclocked hardware.",
            "Semiconductor sector research proving your foundry picks have less production value than a TikTok video.",
            "Microelectronics evaluation for those who think 'photolithography' is an Instagram filter.",
            "Chip manufacturer analysis that makes the dot-com crash look like a minor technical glitch."
        ],
        'healthcare': [
            "Healthcare analysis for people who think 'managed care' describes their portfolio's life support.",
            "Medical sector evaluation for investors whose health insurance costs less than their investment losses.",
            "Healthcare market breakdown proving your hospital picks have worse patient outcomes than your stock picks.",
            "Medical services research for those who confuse 'clinical trials' with their own investment experiments.",
            "Healthcare company assessment demonstrating your pharma investments spread faster than hospital infections.",
            "Medical sector deep-dive for people whose idea of preventive care is stop-loss orders.",
            "Healthcare investment guide for those who think 'healthcare reform' means reformatting their portfolio.",
            "Medical industry analysis proving your healthcare picks have less healing power than essential oils.",
            "Healthcare services evaluation for investors whose medical knowledge comes from WebMD searches.",
            "Medical sector breakdown that makes healthcare.gov's launch look like a smooth operation.",
            "Healthcare company metrics for people who confuse 'patient care' with their own need for financial therapy.",
            "Medical market research for those whose healthcare investments are sicker than their actual health.",
            "Healthcare sector analysis proving your medical picks have the prognosis of a terminal diagnosis.",
            "Medical services evaluation for investors whose healthcare portfolio needs more intensive care than they do.",
            "Healthcare industry breakdown for people whose medical investments have worse side effects than the drugs they produce."
        ],
        'automotive': [
            "Automotive analysis for people who think 'electric vehicle' describes the shock they get from their portfolio.",
            "Car manufacturer evaluation for investors whose driving skills exceed their stock-picking abilities.",
            "Automotive market breakdown proving your EV picks have less range than a golf cart with dead batteries.",
            "Vehicle sector research for those who confuse 'autonomous driving' with their own autopilot investment losses.",
            "Automotive company assessment demonstrating your car picks have more recalls than a defective memory.",
            "Auto industry deep-dive for people whose idea of fuel efficiency is burning money at a sustainable rate.",
            "Automotive investment guide for those who think 'hybrid technology' means mixing winning and losing strategies.",
            "Vehicle market evaluation proving your automotive picks accelerate losses faster than a Formula 1 car.",
            "Automotive sector analysis for investors whose car industry knowledge comes from Fast & Furious movies.",
            "Auto manufacturer metrics that make Volkswagen's emissions scandal look like a minor exhaust issue.",
            "Automotive company research for people who confuse 'crash test ratings' with their portfolio performance.",
            "Vehicle sector breakdown for those whose automotive investments have worse mileage than a Hummer H1.",
            "Automotive market analysis proving your car picks are about as reliable as a 1970s British Leyland vehicle.",
            "Auto industry evaluation for investors whose vehicle investments are always stuck in reverse.",
            "Automotive sector research that makes the Pinto's safety record look acceptable by comparison."
        ],
        'real_estate': [
            "Real estate analysis for people who think 'market bubble' describes their living situation.",
            "Property investment evaluation for those who confuse 'underwater mortgage' with their portfolio's current depth.",
            "Real estate market breakdown proving your REIT picks have less foundation than a house of cards.",
            "Property sector research for people whose idea of location is 'wherever the losses are'.",
            "Real estate company assessment demonstrating your property investments depreciate faster than a trailer park.",
            "Property market deep-dive for those who think 'closing costs' refer to their brokerage account's final moments.",
            "Real estate investment guide for people whose property knowledge comes from HGTV reruns.",
            "Property sector evaluation proving your real estate picks have less structural integrity than a sandcastle.",
            "Real estate analysis for investors whose property investments are as stable as a California hillside.",
            "Property market metrics that make the 2008 housing crisis look like a minor correction.",
            "Real estate company research for people who confuse 'property management' with damage control.",
            "Property sector breakdown for those whose real estate investments are always in need of major repairs.",
            "Real estate market analysis proving your property picks are about as valuable as swampland in Florida.",
            "Property investment evaluation for people whose real estate portfolio is zoned for disappointment.",
            "Real estate sector research that makes subprime mortgage lenders look like conservative bankers."
        ],
        'industrials': [
            "Industrial sector analysis for people who think 'manufacturing efficiency' describes their ability to produce consistent losses.",
            "Heavy machinery evaluation for investors whose construction knowledge comes from playing with Legos.",
            "Industrial market breakdown proving your aerospace picks have less lift than a lead balloon.",
            "Manufacturing sector research for those who confuse 'assembly line' with their series of investment mistakes.",
            "Industrial company assessment demonstrating your defense picks have less strategic value than a rubber knife.",
            "Heavy industry deep-dive for people whose idea of logistics is moving money from savings to losses.",
            "Industrial investment guide for those who think 'supply chain management' means managing their supply of excuses.",
            "Manufacturing market evaluation proving your industrial picks rust faster than a car in Detroit.",
            "Industrial sector analysis for investors whose machinery investments break down more than a 1980s Yugo.",
            "Construction company metrics that make the Leaning Tower of Pisa look structurally sound.",
            "Industrial research for people who confuse 'quality control' with their own lack of control.",
            "Manufacturing sector breakdown for those whose production investments have negative efficiency ratings.",
            "Industrial market analysis proving your construction picks have the stability of a house of cards in a earthquake.",
            "Heavy machinery evaluation for investors whose industrial knowledge comes from Discovery Channel reruns.",
            "Industrial sector research that makes Soviet-era manufacturing look like a model of efficiency."
        ]
    }
    
    # Check for sector-specific content and use appropriate flavor texts
    def detect_sector(title, filename):
        content = f"{title} {filename}".lower()
        
        # Comprehensive Darwinex-based symbol detection
        
        # Biotech/Pharmaceutical symbols and keywords
        biotech_symbols = ['srpt', 'biib', 'gild', 'amgn', 'bmrn', 'alny', 'arwr', 'apls', 'ions', 'rare', 'blue', 'fold', 'crsp', 'edit', 'ntla', 'beam', 'prime', 'fate', 'sgmo', 'xlrn']
        biotech_keywords = ['biotech', 'pharma', 'drug', 'clinical', 'fda', 'medical device', 'therapeutic', 'biotechnology', 'drugs manufacturers', 'gene therapy', 'clinical trial']
        if any(symbol in content for symbol in biotech_symbols) or any(word in content for word in biotech_keywords):
            return 'biotech'
        
        # Technology symbols and keywords
        tech_symbols = ['aapl', 'msft', 'googl', 'goog', 'amzn', 'meta', 'nflx', 'adbe', 'crm', 'orcl', 'nvda', 'amd', 'intc', 'crwd', 'snow', 'pltr', 'tsla']
        tech_keywords = ['tech', 'software', 'app', 'cloud', 'saas', 'ai', 'artificial intelligence', 'blockchain', 'crypto', 'technology', 'internet', 'computer']
        if any(symbol in content for symbol in tech_symbols) or any(word in content for word in tech_keywords):
            return 'tech'
            
        # Semiconductor symbols and keywords
        semiconductor_symbols = ['nvda', 'amd', 'intc', 'tsm', 'mu', 'avgo', 'qcom', 'txn', 'asml', 'lrcx', 'klac', 'amat', 'mrvl', 'mchp', 'swks']
        semiconductor_keywords = ['semiconductor', 'chip', 'silicon', 'processors', 'semiconductor equipment', 'materials']
        if any(symbol in content for symbol in semiconductor_symbols) or any(word in content for word in semiconductor_keywords):
            return 'semiconductor'
            
        # Energy symbols and keywords
        energy_symbols = ['xom', 'cvx', 'cop', 'slb', 'eog', 'pxd', 'mpc', 'vlo', 'hes', 'oxy', 'dvn', 'fang', 'mrg', 'hal', 'bkr']
        energy_keywords = ['energy', 'oil', 'gas', 'solar', 'renewable', 'wind', 'power', 'utility', 'petroleum', 'drilling', 'refining', 'utilities']
        if any(symbol in content for symbol in energy_symbols) or any(word in content for word in energy_keywords):
            return 'energy'
            
        # Finance symbols and keywords (comprehensive bank and finance tickers)
        finance_symbols = ['c', 'jpm', 'bac', 'wfc', 'gs', 'ms', 'blk', 'schw', 'usb', 'pnc', 'truist', 'cof', 'aig', 'met', 'pru', 'all', 'cme', 'ice', 'spgi', 'mcg', 'cb']
        finance_keywords = ['bank', 'finance', 'credit', 'loan', 'insurance', 'fintech', 'payment', 'citigroup', 'jpmorgan', 'wells fargo', 'goldman sachs', 'morgan stanley', 'blackrock', 'financial', 'banking', 'asset management']
        if any(symbol in content for symbol in finance_symbols) or any(word in content for word in finance_keywords) or '-c.html' in content:
            return 'finance'
            
        # Healthcare symbols and keywords
        healthcare_symbols = ['jnj', 'pfr', 'unh', 'mrk', 'abbv', 'tmo', 'dhr', 'abt', 'isrg', 'vrtx', 'ci', 'cvs', 'hum', 'antm', 'bmy', 'lly']
        healthcare_keywords = ['health', 'hospital', 'medical', 'diagnostic', 'care', 'hmo', 'healthcare', 'medical devices', 'pharmaceutical', 'medical care facilities']
        if any(symbol in content for symbol in healthcare_symbols) or any(word in content for word in healthcare_keywords):
            return 'healthcare'
            
        # Retail/Consumer symbols and keywords
        retail_symbols = ['amzn', 'wmt', 'hd', 'tgt', 'low', 'cost', 'dg', 'dltr', 'tjx', 'ross', 'gps', 'anf', 'rl', 'nke', 'sbux', 'mcd', 'yum']
        retail_keywords = ['retail', 'consumer', 'store', 'shopping', 'ecommerce', 'brand', 'consumer cyclical', 'consumer defensive', 'restaurants', 'specialty retail']
        if any(symbol in content for symbol in retail_symbols) or any(word in content for word in retail_keywords):
            return 'retail'
            
        # Automotive symbols and keywords
        automotive_symbols = ['tsla', 'f', 'gm', 'fcau', 'tm', 'hmc', 'aal', 'dal', 'ual', 'luv', 'jblu', 'save']
        automotive_keywords = ['auto', 'car', 'vehicle', 'electric vehicle', 'ev', 'tesla', 'ford', 'gm', 'automotive', 'auto manufacturers', 'auto parts', 'airlines']
        if any(symbol in content for symbol in automotive_symbols) or any(word in content for word in automotive_keywords):
            return 'automotive'
            
        # Real Estate symbols and keywords
        real_estate_symbols = ['are', 'pld', 'cxw', 'eqix', 'dlr', 'spg', 'o', 'eit', 'avb', 'eqr', 'ess', 'udr', 'cpr', 'hcp', 'ventas']
        real_estate_keywords = ['real estate', 'reit', 'property', 'housing', 'mortgage', 'construction', 'reits', 'residential', 'commercial']
        if any(symbol in content for symbol in real_estate_symbols) or any(word in content for word in real_estate_keywords):
            return 'real_estate'
        
        # Industrial symbols and keywords
        industrials_symbols = ['ba', 'cat', 'de', 'ge', 'mmm', 'hon', 'ups', 'fedx', 'rtx', 'lmt', 'noc', 'gd', 'etn', 'emr', 'itt']
        industrials_keywords = ['industrial', 'manufacturing', 'construction', 'machinery', 'aerospace', 'defense', 'transportation', 'logistics', 'industrials']
        if any(symbol in content for symbol in industrials_symbols) or any(word in content for word in industrials_keywords):
            return 'industrials'
            
        return None
    
    # Detect sector and use appropriate flavor text
    detected_sector = detect_sector(title, filename)
    if detected_sector and detected_sector in sector_texts:
        fallback_text = sector_texts[detected_sector][0] if sector_texts[detected_sector] else "Sector analysis for financial masochists."
        return select_unused_flavor_text(sector_texts[detected_sector], fallback_text)
    
    # Sam Hyde-esque outlier analysis flavor texts (100+ variations)
    outlier_texts = [
        "VaR analysis for degenerates who think risk management is just another word for 'hedging your bets on financial suicide'.",
        "Statistical validation that your portfolio is absolutely fucked, presented with the clinical precision of a medical examiner.",
        "Outlier detection for those who enjoy watching their life savings dance on the edge of mathematical oblivion.",
        "Risk metrics for people whose idea of diversification is losing money in multiple asset classes simultaneously.",
        "Mathematical proof that your trading strategy is about as effective as a chocolate teapot in a house fire.",
        "Quantitative analysis for masochists who need spreadsheets to confirm their financial death spiral.",
        "VaR calculations for the kind of person who thinks 'YOLO' is a legitimate investment philosophy.",
        "Statistical evidence that your portfolio management skills peaked in kindergarten sandbox trading.",
        "Risk assessment for degenerates who confuse 'high-frequency trading' with 'frequently losing money'.",
        "Outlier analysis proving that your investment decisions violate several laws of physics and common sense.",
        "Mathematical validation that your portfolio's performance makes a broken slot machine look profitable.",
        "VaR metrics for people who think 'cutting losses' means selling their remaining kidney.",
        "Risk analysis for the financially suicidal who mistake volatility for opportunity.",
        "Statistical proof that your trading algorithm was coded by a caffeinated hamster with commitment issues.",
        "Outlier detection for those whose investment strategy resembles a toddler throwing darts at a board blindfolded.",
        "VaR calculations confirming that your portfolio's trajectory violates basic laws of gravity and decency.",
        "Risk metrics for people who think 'diamond hands' is medical advice for arthritic grip strength.",
        "Mathematical evidence that your financial advisor is either incompetent or secretly your worst enemy.",
        "Statistical analysis proving your investment choices have the accuracy of a storm trooper's aim.",
        "Outlier assessment for degenerates who confuse market volatility with their own emotional instability.",
        "VaR analysis for those who believe 'buy high, sell low' is a revolutionary contrarian strategy.",
        "Risk calculations that make Russian roulette look like a conservative investment approach.",
        "Mathematical proof that your portfolio diversification strategy consists of losing money in different currencies.",
        "Statistical validation that your trading skills are surpassed only by your ability to rationalize failure.",
        "Outlier detection for people whose risk tolerance is inversely proportional to their actual income.",
        "VaR metrics proving that your investment timeline is measured in regret rather than returns.",
        "Risk analysis for those who think 'hedge fund' refers to gardening equipment financing.",
        "Mathematical evidence that your portfolio's performance makes a burning dumpster look like a sound investment.",
        "Statistical proof that your financial planning involves more hope than a terminal cancer patient.",
        "Outlier analysis for degenerates who mistake market manipulation for personal skill.",
        "VaR calculations demonstrating that your risk management strategy is about as effective as a screen door on a submarine.",
        "Risk metrics for people who think 'stop loss' is what happens when you run out of money.",
        "Mathematical validation that your investment philosophy was inspired by a fever dream and bad mushrooms.",
        "Statistical analysis proving your portfolio allocation resembles abstract art more than financial planning.",
        "Outlier detection for those whose trading decisions are influenced more by astrology than analytics.",
        "VaR analysis confirming that your risk-adjusted returns are negative in multiple dimensions.",
        "Risk calculations for people who confuse 'market timing' with 'being late to everything'.",
        "Mathematical proof that your investment strategy violates the Geneva Convention on financial cruelty.",
        "Statistical evidence that your portfolio management makes a blindfolded monkey throwing shit look professional.",
        "Outlier assessment for degenerates whose idea of due diligence is checking if the stock ticker is spelled correctly.",
        "VaR metrics proving that your financial decisions have the consistency of liquid nitrogen.",
        "Risk analysis for those who think 'compound interest' is what banks charge for complicated questions.",
        "Mathematical validation that your trading algorithm was written in crayon by a sugar-high 8-year-old.",
        "Statistical proof that your investment timeline operates in reverse chronological order.",
        "Outlier detection for people whose risk assessment skills peaked at evaluating playground equipment.",
        "VaR calculations demonstrating that your portfolio's volatility makes bipolar disorder look stable.",
        "Risk metrics for degenerates who think 'liquidity' refers to how much they've been drinking.",
        "Mathematical evidence that your financial planning involves more wishful thinking than a Disney movie.",
        "Statistical analysis proving your investment choices are guided by the same logic as flat-earth theory.",
        "Outlier analysis for those whose portfolio diversification means owning different colors of the same worthless stock.",
        "VaR metrics confirming that your risk tolerance is higher than your IQ.",
        "Risk calculations for people who confuse 'market correction' with their own need for psychological help.",
        "Mathematical proof that your investment strategy was conceived during a psychotic break.",
        "Statistical validation that your trading skills are surpassed only by your capacity for self-delusion.",
        "Outlier detection for degenerates whose financial advice comes from fortune cookies and Reddit comments.",
        "VaR analysis proving that your portfolio performance makes a trainwreck look like efficient transportation.",
        "Risk metrics for those who think 'asset allocation' means hiding money under different mattresses.",
        "Mathematical evidence that your investment philosophy was inspired by a lobotomized economics textbook.",
        "Statistical proof that your financial decision-making process involves more coin flips than analysis.",
        "Outlier assessment for people whose idea of risk management is wearing a helmet while trading.",
        "VaR calculations demonstrating that your portfolio's trajectory defies physics and common sense.",
        "Risk analysis for degenerates who mistake gambling addiction for investment enthusiasm.",
        "Mathematical validation that your trading strategy has the precision of a shotgun blast in the dark.",
        "Statistical evidence that your investment timeline is measured in stages of grief rather than quarters.",
        "Outlier detection for those whose portfolio allocation resembles a Pollock painting after a seizure.",
        "VaR metrics proving that your risk assessment skills make a blind person look like a sharpshooter.",
        "Risk calculations for people who think 'blue chip stocks' are colored gambling tokens.",
        "Mathematical proof that your investment decisions are influenced more by lunar cycles than market cycles.",
        "Statistical analysis proving your portfolio management makes a house fire look like controlled burning.",
        "Outlier analysis for degenerates whose financial planning horizon extends to next week's lottery drawing.",
        "VaR calculations confirming that your trading algorithm was coded by a drunk programmer having an existential crisis.",
        "Risk metrics for those who confuse 'market volatility' with their own emotional instability.",
        "Mathematical evidence that your investment strategy violates several international treaties on financial war crimes.",
        "Statistical validation that your portfolio diversification strategy involves different ways to lose the same money.",
        "Outlier detection for people whose risk tolerance is inversely related to their understanding of basic math.",
        "VaR analysis proving that your financial advisor either hates you or is secretly working for your enemies.",
        "Risk calculations that make playing chicken with freight trains look like conservative risk management.",
        "Mathematical proof that your investment philosophy was developed by someone who failed kindergarten counting.",
        "Statistical evidence that your trading decisions are guided by the same principles as reality TV.",
        "Outlier assessment for degenerates who think 'portfolio rebalancing' means drinking until the numbers look better.",
        "VaR metrics demonstrating that your risk management strategy has the effectiveness of a chocolate firewall.",
        "Risk analysis for those whose investment timeline is measured in units of regret and self-loathing.",
        "Mathematical validation that your financial planning makes a Ponzi scheme look legitimate.",
        "Statistical proof that your portfolio allocation was determined by a magic 8-ball with trust issues.",
        "Outlier detection for people whose investment strategy resembles a toddler's attempt at abstract art.",
        "VaR calculations proving that your risk-adjusted returns exist in a parallel universe where math doesn't work.",
        "Risk metrics for degenerates who confuse 'market research' with reading horoscopes.",
        "Mathematical evidence that your trading algorithm was inspired by a broken random number generator.",
        "Statistical analysis proving your investment choices have the logic of a fever-induced hallucination.",
        "Outlier analysis for those whose financial decision-making process involves more prayer than analysis.",
        "VaR metrics confirming that your portfolio's performance makes a dumpster fire look like a growth investment.",
        "Risk calculations for people who think 'due diligence' is what you owe after being late to meetings.",
        "Mathematical proof that your investment strategy was conceived by someone allergic to money.",
        "Statistical validation that your trading skills are exceeded only by your ability to rationalize catastrophic failure.",
        "Outlier detection for degenerates whose risk assessment involves asking their pet goldfish for financial advice.",
        "VaR analysis proving that your portfolio management makes abstract expressionism look structured.",
        "Risk metrics for those who confuse 'compound growth' with the interest on their therapy bills.",
        "Mathematical evidence that your financial planning was outsourced to a committee of caffeinated squirrels.",
        "Statistical proof that your investment timeline operates on geological rather than fiscal years.",
        "Outlier assessment for people whose idea of diversification is losing money in both stocks AND crypto.",
        "VaR calculations demonstrating that your trading strategy has the precision of a blindfolded surgeon.",
        "Risk analysis for degenerates who think 'liquidity management' refers to their drinking problem.",
        "Mathematical validation that your portfolio allocation was determined by throwing darts at a spinning wheel.",
        "Statistical evidence that your investment philosophy makes flat-earth theory look scientifically rigorous.",
        "Outlier detection for those whose financial advisor is either a complete fraud or suffering from severe head trauma.",
        "VaR metrics proving that your risk management approach makes Russian roulette look like a pension plan.",
        "Risk calculations for people who confuse 'market timing' with showing up late to their own financial funeral.",
        "Mathematical proof that your investment decisions violate the basic principles of logic and human decency.",
        "Statistical analysis proving your portfolio performance makes a controlled demolition look accidental.",
        "Outlier analysis for degenerates whose trading strategy was inspired by watching paint dry and finding it too exciting.",
        "VaR calculations confirming that your financial planning makes a house of cards look structurally sound.",
        "Risk metrics for those who think 'asset protection' means hiding under their desk during market hours."
    ]
    
    if 'srpt' in filename_lower or 'biotech' in title_lower:
        return "Biotech analysis for those who think playing roulette with regulatory approval is a sound investment thesis."
    elif 'outlier' in title_lower or 'var' in title_lower or 'claude' in title_lower:
        return select_unused_flavor_text(outlier_texts, "VaR analysis for degenerates who think risk management is just another word for 'hedging your bets on financial suicide'.")
    elif 'gpu' in title_lower or 'buyers' in title_lower:
        return "Hardware analysis for degenerates who confuse graphics cards with investment vehicles. Your wallet's funeral service."
    else:
        return "Financial analysis for masochists who enjoy watching their net worth evaporate with mathematical precision."

def main():
    """Main function to process all files and update blog"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate HTML blog posts from text files')
    parser.add_argument('--regenerate-html', action='store_true',
                      help='Force regeneration of all HTML files from .txt files (updates flavor text)')
    args = parser.parse_args()
    
    # Load previously used flavor texts
    load_used_flavor_texts()
    
    # Clear flavor text mapping if regenerating to get fresh flavor texts
    if args.regenerate_html:
        global blog_flavor_mapping
        blog_flavor_mapping = {}
        print("Regeneration mode: Clearing existing flavor text mappings for fresh generation")
    
    blog_entries = []
    blog_path = Path(BLOG_DIR)
    
    # Find all existing HTML files
    html_files = list(blog_path.glob('*.html'))
    print(f"Found {len(html_files)} existing HTML files")
    
    if args.regenerate_html:
        # Regeneration mode: Process all .txt files and force HTML regeneration
        print("REGENERATION MODE: Regenerating all HTML files from .txt files...")
        txt_files = list(blog_path.glob('*.txt'))
        print(f"Found {len(txt_files)} .txt files to process")
        
        for txt_file in txt_files:
            print(f"Regenerating HTML for {txt_file.name}")
            html_file = generate_html_from_txt(txt_file, force_regenerate=True)
            
            # Extract metadata for blog index
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            title, _, _ = extract_title_and_summary(content, txt_file.name)
            
            # Extract date from filename
            date_match = re.search(r'(\d{2})(\d{2})(\d{4})', txt_file.name)
            if date_match:
                month, day, year = date_match.groups()
                date_str = f"{year}-{month}-{day}"
            else:
                date_str = datetime.now().strftime("%Y-%m-%d")
            
            flavor_text = get_consistent_flavor_text(Path(html_file).name, title)
            
            blog_entries.append({
                'filename': Path(html_file).name,
                'title': title,
                'date': date_str,
                'summary': flavor_text
            })
    
    else:
        # Normal mode: Process existing HTML files and new .txt files
        # Process existing HTML files
        for html_file in html_files:
            title = extract_title_from_html(html_file)
            
            # Extract date from filename
            date_match = re.search(r'(\d{2})(\d{2})(\d{4})', html_file.name)
            if date_match:
                month, day, year = date_match.groups()
                date_str = f"{year}-{month}-{day}"
            elif 'gpu' in html_file.name:
                date_str = "2025-03-07"  # Set known date for GPU guide
            else:
                date_str = datetime.now().strftime("%Y-%m-%d")
            
            flavor_text = get_consistent_flavor_text(html_file.name, title)
            
            blog_entries.append({
                'filename': html_file.name,
                'title': title,
                'date': date_str,
                'summary': flavor_text
            })
        
        # Find .txt files that don't have corresponding HTML files
        txt_files = list(blog_path.glob('*.txt'))
        for txt_file in txt_files:
            html_name = txt_file.stem + '.html'
            html_path = blog_path / html_name
            
            if not html_path.exists():
                print(f"Generating HTML for {txt_file.name}")
                html_file = generate_html_from_txt(txt_file)
                
                # Extract metadata for blog index
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                title, _, _ = extract_title_and_summary(content, txt_file.name)
                
                # Extract date from filename
                date_match = re.search(r'(\d{2})(\d{2})(\d{4})', txt_file.name)
                if date_match:
                    month, day, year = date_match.groups()
                    date_str = f"{year}-{month}-{day}"
                else:
                    date_str = datetime.now().strftime("%Y-%m-%d")
                
                flavor_text = get_consistent_flavor_text(Path(html_file).name, title)
                
                blog_entries.append({
                    'filename': Path(html_file).name,
                    'title': title,
                    'date': date_str,
                    'summary': flavor_text
                })
    
    print(f"Total blog entries: {len(blog_entries)}")
    
    # Update blog index
    update_blog_index(blog_entries)
    
    # Save the updated flavor text cache
    save_used_flavor_texts()
    
    print("Blog generation complete!")


if __name__ == "__main__":
    main()