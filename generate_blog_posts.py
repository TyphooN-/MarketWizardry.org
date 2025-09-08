#!/usr/bin/env python3
"""
Script to generate HTML blog posts from text files and update blog.html
"""
import os
import re
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
            <a id="downloadButton" href="{txt_filename}">Download Report</a>
            <span class="close-button" onclick="closeModal()">&times;</span>
        </div>
        <div class="modal-text" tabindex="0">{content}</div>
    </div>
</div>

<script>
    function openModal() {{
        const modal = document.getElementById("analysisModal");
        
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
        modal.focus();
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
        content=content,
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


def update_blog_index(new_txt_entries):
    """Update blog.html with new entries, preserving existing ones"""
    
    # Get existing entries from blog.html
    existing_entries = parse_existing_blog_entries()
    
    # Create a set of existing filenames to avoid duplicates
    existing_filenames = {entry['filename'] for entry in existing_entries}
    
    # Add only new entries that don't already exist
    new_entries_added = []
    for entry in new_txt_entries:
        if entry['filename'] not in existing_filenames:
            entry['source'] = 'txt-generated'
            new_entries_added.append(entry)
            print(f"Adding new entry: {entry['title']}")
        else:
            print(f"Skipping duplicate entry: {entry['title']}")
    
    # Combine all entries
    all_entries = existing_entries + new_entries_added
    
    # Sort by date (newest first)
    all_entries.sort(key=lambda x: x['date'], reverse=True)
    
    if not new_entries_added:
        print("No new entries to add")
        return
    
    # Read current blog.html
    with open(BLOG_INDEX, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Generate entries HTML for all entries
    entries_html = []
    for entry in all_entries:
        # Check if this is a single stock analysis entry and add description
        description_html = ""
        if 'summary' in entry and entry['summary']:
            # For single stock analyses, include the witty commentary
            filename = entry['filename']
            if filename and ('-' in filename and filename.upper().endswith('.HTML')):
                # Check if it looks like a stock ticker pattern
                import re
                base_filename = filename.replace('.html', '.txt')
                upper_filename = base_filename.upper()
                ticker_match = re.search(r'-([A-Z]{2,5})\.txt$', upper_filename)
                if ticker_match or (upper_filename.endswith('.TXT') and '-' in upper_filename):
                    # This is likely a single stock analysis, add the description
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
    
    print(f"Updated {BLOG_INDEX}: {len(existing_entries)} existing + {len(new_entries_added)} new = {len(all_entries)} total entries")


def main():
    """Main function to process all text files and update blog"""
    blog_entries = []
    
    # Find all .txt files in blog directory
    blog_path = Path(BLOG_DIR)
    txt_files = list(blog_path.glob('*.txt'))
    
    if not txt_files:
        print("No .txt files found in blog directory")
        return
    
    print(f"Found {len(txt_files)} text files to process")
    
    # Process each text file
    for txt_file in txt_files:
        html_file = generate_html_from_txt(txt_file)
        
        # Extract metadata for blog index
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title, summary, _ = extract_title_and_summary(content, txt_file.name)
        
        # Extract date from filename
        date_match = re.search(r'(\d{2})(\d{2})(\d{4})', txt_file.name)
        if date_match:
            month, day, year = date_match.groups()
            date_str = f"{year}-{month}-{day}"
        else:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        blog_entries.append({
            'filename': Path(html_file).name,
            'title': title,
            'date': date_str,
            'summary': summary
        })
    
    # Update blog index (now preserves existing entries)
    update_blog_index(blog_entries)
    
    print("Blog generation complete!")


if __name__ == "__main__":
    main()