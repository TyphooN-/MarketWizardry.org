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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- Standard Meta Tags -->
    <meta name="description" content="{description}">
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="MarketWizardry.org | {title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="https://marketwizardry.org/blog/{filename}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Market Wizardry">
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:site" content="@MarketW1zardry">
    <meta name="twitter:creator" content="@MarketW1zardry">
    <script>
        // Redirect to index.html if accessed directly (not in iframe)
        if (window === window.top) {{
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
            <a id="downloadButton" href="#" download="{txt_filename}">Download Report</a>
            <span class="close-button" onclick="closeModal()">&times;</span>
        </div>
        <div class="modal-text" tabindex="0">{content}</div>
    </div>
</div>

<script>
    function openModal() {{
        const modal = document.getElementById("analysisModal");
        const modalText = modal.querySelector('.modal-text');
        const downloadButton = document.getElementById("downloadButton");
        
        // Create blob for download
        const textContent = modalText.textContent;
        const blob = new Blob([textContent], {{ type: 'text/plain' }});
        const url = URL.createObjectURL(blob);
        downloadButton.href = url;
        
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
        modal.focus();
    }}

    function closeModal() {{
        const modal = document.getElementById("analysisModal");
        const downloadButton = document.getElementById("downloadButton");
        
        modal.style.display = "none";
        document.body.style.overflow = "auto";
        
        // Clean up blob URL
        if (downloadButton.href && downloadButton.href.startsWith('blob:')) {{
            URL.revokeObjectURL(downloadButton.href);
        }}
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
    
    # Look for title patterns in content
    title = "Market Analysis"
    summary = "Financial analysis and market insights."
    section_title = "📊 MARKET ANALYSIS"
    
    for line in lines[:20]:  # Check first 20 lines
        line = line.strip()
        if not line:
            continue
            
        # Look for various title patterns
        if any(keyword in line.lower() for keyword in ['executive summary', 'comprehensive', 'analysis', 'investment']):
            if 'outlier' in line.lower() and 'darwinex' in line.lower():
                title = "Claude x Darwinex Outlier Analysis"
                summary = "Deep dive into Darwinex VaR/Ask outlier analysis - separating actionable opportunities from close-only traps in the statistical anomaly wasteland."
                section_title = "🎯 REVISED DARWINEX UNIVERSE INVESTMENT RECOMMENDATIONS"
            elif 'investment' in line.lower():
                title = f"Investment Analysis - {date_str}" if date_str else "Investment Analysis"
                summary = "Comprehensive market analysis with buy/sell recommendations based on statistical outliers and fundamental analysis."
                section_title = "📊 INVESTMENT RECOMMENDATIONS"
            break
        elif line.startswith('●') and len(line) > 10:
            # Use first bullet point as title
            clean_line = line.replace('●', '').strip()
            if len(clean_line) < 80:
                title = clean_line
                break
    
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


def update_blog_index(blog_entries):
    """Update blog.html with new entries"""
    
    # Read current blog.html
    with open(BLOG_INDEX, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Generate entries HTML
    entries_html = []
    for entry in sorted(blog_entries, key=lambda x: x['date'], reverse=True):
        entry_html = f'''            <div class="blog-entry">
                <a href="https://marketwizardry.org/blog/{entry['filename']}">{entry['title']}</a>
                <span class="date">Posted: {entry['date']}</span>
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
    
    print(f"Updated {BLOG_INDEX} with {len(blog_entries)} entries")


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
    
    # Update blog index
    update_blog_index(blog_entries)
    
    print("Blog generation complete!")


if __name__ == "__main__":
    main()