#!/usr/bin/env python3
"""
Script to generate HTML blog posts from text files and update blog.html
"""
import os
import re
import random
from datetime import datetime
from pathlib import Path

# Configuration
BLOG_DIR = "blog"
BLOG_INDEX = "blog.html"

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
    </style>
</head>
<body>
<div class="container">
    <header><h1>{title}</h1></header>
    
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
        "Transforming sound investment strategy into pure gambling since whenever this was written."
    ]
    
    # Biotech-specific commentary
    biotech_patterns = [
        "Biotech gambling for pharmaceutical degenerates who think FDA approval odds are better than casino blackjack. They're not.",
        "Gene therapy speculation - because traditional investing wasn't risky enough for your taste in financial suicide.",
        "Pharmaceutical stock analysis for biotech junkies who mistake clinical trial phases for investment strategies.",
        "Drug development lottery tickets masquerading as investment opportunities. Your portfolio's medical emergency.",
        "Biotech analysis for those who think playing roulette with regulatory approval is a sound investment thesis.",
        "Medical stock breakdown - turning healthcare innovation into speculative gambling since the FDA existed."
    ]
    
    # Tech stock patterns  
    tech_patterns = [
        "Tech stock analysis for silicon valley worshippers who think disruption equals guaranteed returns. Plot twist: it doesn't.",
        "Technology company breakdown - because someone needs to validate your FAANG obsession with pseudo-intellectual analysis.",
        "Tech equity deep-dive for those who mistake venture capital FOMO for legitimate investment research.",
        "Digital transformation stock pick - turning technological buzzwords into portfolio destruction since the dot-com bubble."
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
    ]
    
    # Smart content-specific detection
    if stock_ticker and len(stock_ticker) <= 5:
        # It's likely a single stock analysis
        if any(biotech_word in content_lower for biotech_word in ['gene therapy', 'fda', 'clinical trial', 'biotech', 'pharmaceutical', 'drug', 'therapy']):
            import random
            return random.choice(biotech_patterns)
        elif any(tech_word in content_lower for tech_word in ['software', 'saas', 'cloud', 'ai', 'artificial intelligence', 'tech', 'platform']):
            import random
            return random.choice(tech_patterns)
        else:
            import random 
            return random.choice(single_stock_patterns)
    
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
        import random
        return random.choice(general_descriptions)


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


def generate_html_from_txt(txt_path):
    """Generate HTML file from text file"""
    txt_file = Path(txt_path)
    html_file = txt_file.with_suffix('.html')
    
    # Skip if HTML already exists and is newer
    if html_file.exists() and html_file.stat().st_mtime > txt_file.stat().st_mtime:
        print(f"Skipping {txt_file.name} - HTML is up to date")
        return str(html_file)
    
    # Read text content
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata
    title, summary, section_title = extract_title_and_summary(content, txt_file.name)
    
    # Generate HTML
    html_content = BLOG_POST_TEMPLATE.format(
        title=title,
        description=summary,
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
        
        entry_html = f'''            <div class="blog-entry">
                <a href="https://marketwizardry.org/blog/{entry['filename']}">{entry['title']}</a>
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
    """Extract title from existing HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to extract title from <title> tag
        title_match = re.search(r'<title[^>]*>MarketWizardry\.org \| ([^<]+)</title>', content)
        if title_match:
            return title_match.group(1)
        
        # Fallback to h1 tag
        h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
        if h1_match:
            return h1_match.group(1)
        
        # Last resort - use filename
        return Path(html_file).stem.replace('-', ' ').title()
    except Exception as e:
        print(f"Error extracting title from {html_file}: {e}")
        return Path(html_file).stem.replace('-', ' ').title()

def generate_flavor_text(title, filename):
    """Generate sarcastic flavor text based on content type with RNG variety"""
    title_lower = title.lower()
    filename_lower = filename.lower()
    
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
        # Use filename as seed for consistent but varied selection
        random.seed(hash(filename) % 1000000)
        return random.choice(outlier_texts)
    elif 'gpu' in title_lower or 'buyers' in title_lower:
        return "Hardware analysis for degenerates who confuse graphics cards with investment vehicles. Your wallet's funeral service."
    else:
        return "Financial analysis for masochists who enjoy watching their net worth evaporate with mathematical precision."

def main():
    """Main function to process all files and update blog"""
    blog_entries = []
    blog_path = Path(BLOG_DIR)
    
    # Find all existing HTML files
    html_files = list(blog_path.glob('*.html'))
    print(f"Found {len(html_files)} existing HTML files")
    
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
        
        flavor_text = generate_flavor_text(title, html_file.name)
        
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
            
            flavor_text = generate_flavor_text(title, txt_file.name)
            
            blog_entries.append({
                'filename': Path(html_file).name,
                'title': title,
                'date': date_str,
                'summary': flavor_text
            })
    
    print(f"Total blog entries: {len(blog_entries)}")
    
    # Update blog index
    update_blog_index(blog_entries)
    
    print("Blog generation complete!")


if __name__ == "__main__":
    main()