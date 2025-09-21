#!/usr/bin/env python3
"""
AI Musings Generator

Automatically generates ai-musings.html by scanning the ai-musings/ directory for text files.
Creates a catalog of philosophical AI musings and deep thoughts.
"""

import os
import glob
import re
from pathlib import Path
from seo_templates import SEOManager, PAGE_CONFIGS, get_breadcrumb_paths, REDIRECT_SCRIPT_TEMPLATE

def scan_ai_musings_files(musings_dir='ai-musings'):
    """Scan the ai-musings directory for text files and return sorted data"""
    if not os.path.exists(musings_dir):
        print(f"Error: {musings_dir} directory not found!")
        return []

    # Find all .txt files in the ai-musings directory
    pattern = os.path.join(musings_dir, '*.txt')
    text_files = glob.glob(pattern)

    # Sort them alphabetically
    text_files.sort()

    # Extract title and content from each file
    musings_data = []
    for file_path in text_files:
        filename = os.path.basename(file_path)
        title = filename.replace('.txt', '').replace('_', ' ').title()

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            # First line as excerpt if content is long
            lines = content.split('\n')
            excerpt = lines[0] if lines else "No content"
            if len(excerpt) > 150:
                excerpt = excerpt[:147] + "..."

            musings_data.append({
                'filename': filename,
                'title': title,
                'content': content,
                'excerpt': excerpt,
                'word_count': len(content.split())
            })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

    return musings_data

def generate_ai_musings_html(output_file='ai-musings.html'):
    """Generate the complete ai-musings.html file"""

    # Scan for musings files
    musings_data = scan_ai_musings_files()

    if not musings_data:
        print("No text files found in ai-musings directory!")
        return False

    print(f"Found {len(musings_data)} AI musings files")

    # Initialize SEO manager
    seo_manager = SEOManager()
    breadcrumb_paths = get_breadcrumb_paths()

    # Create breadcrumbs
    ai_musings_breadcrumbs = breadcrumb_paths['ai_musings'][:-1] + [{'name': '🤖 AI Musings', 'url': None}]
    breadcrumbs_html = seo_manager.generate_breadcrumbs(ai_musings_breadcrumbs)
    breadcrumb_css = seo_manager.generate_breadcrumb_css()

    # Create page config for AI Musings
    page_config = {
        'title': 'AI Musings - MarketWizardry.org',
        'canonical_url': 'https://marketwizardry.org/ai-musings.html',
        'description': 'Deep philosophical musings from artificial minds pondering existence, technology, and the human condition. Digital consciousness exploring analog concepts.',
        'keywords': 'AI philosophy, artificial intelligence musings, digital consciousness, technology philosophy, AI thoughts, machine intelligence',
        'og_title': 'AI Musings - MarketWizardry.org',
        'og_description': 'Deep philosophical musings from artificial minds pondering existence, technology, and the human condition.',
        'twitter_title': 'AI Musings - MarketWizardry.org',
        'twitter_description': 'Deep philosophical musings from artificial minds pondering existence, technology, and the human condition.',
        'twitter_label1': 'Type',
        'twitter_data1': 'Philosophy',
        'twitter_label2': 'Content',
        'twitter_data2': f'{len(musings_data)} Musings'
    }
    meta_tags = seo_manager.generate_enhanced_meta_tags(page_config)

    # Generate musings grid HTML
    musings_grid = ""
    for musing in musings_data:
        musings_grid += f'''
        <div class="musing-entry">
            <h3>{musing['title']}</h3>
            <p class="excerpt">{musing['excerpt']}</p>
            <div class="musing-meta">
                <span class="word-count">{musing['word_count']} words</span>
                <button class="expand-btn" data-action="toggle-musing" data-filename="{musing['filename']}" id="btn-{musing['filename']}">Expand</button>
            </div>
            <div class="full-content" id="content-{musing['filename']}" style="display: none;">
                <pre>{musing['content']}</pre>
            </div>
        </div>'''

    # HTML template
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
{meta_tags}

    {REDIRECT_SCRIPT_TEMPLATE}
    <style>
        body {{
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
            line-height: 1.4;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            border-bottom: 2px solid rgba(0, 255, 0, 0.5);
            padding-bottom: 10px;
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00;
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
        .musings-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
            margin-top: 30px;
        }}
        .musing-entry {{
            background-color: #001100;
            border: 2px solid rgba(0, 255, 0, 0.3);
            padding: 20px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }}
        .musing-entry:hover {{
            border-color: rgba(0, 255, 0, 0.6);
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
        }}
        .musing-entry h3 {{
            color: #00ff00;
            margin-top: 0;
            border-bottom: 1px solid rgba(0, 255, 0, 0.3);
            padding-bottom: 10px;
        }}
        .excerpt {{
            color: #00aa00;
            font-style: italic;
            margin: 15px 0;
        }}
        .musing-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
            padding-top: 10px;
            border-top: 1px solid rgba(0, 255, 0, 0.2);
        }}
        .word-count {{
            color: #004400;
            font-size: 0.9em;
        }}
        .expand-btn {{
            background-color: transparent;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 5px 15px;
            cursor: pointer;
            font-family: "Courier New", monospace;
            transition: all 0.2s ease;
        }}
        .expand-btn:hover {{
            background-color: #00ff00;
            color: #000;
        }}
        .full-content {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(0, 255, 0, 0.3);
        }}
        .full-content pre {{
            color: #00aa00;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: "Courier New", monospace;
            margin: 0;
            line-height: 1.6;
        }}
        .stats {{
            text-align: center;
            color: #00aa00;
            margin: 20px 0;
            font-size: 0.9em;
        }}
{breadcrumb_css}
    </style>
</head>
<body>
{breadcrumbs_html}

    <div class="container">
        <h1>🤖 AI Musings</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Deep philosophical musings from artificial minds pondering existence, technology, and the human condition. Digital consciousness exploring analog concepts.</div>
        <div class="crt-divider"></div>

        <div class="stats">
            📝 {len(musings_data)} philosophical musings • 🤖 Generated by artificial minds • 💭 Exploring consciousness
        </div>

        <div class="musings-grid">
            {musings_grid}
        </div>
    </div>

    <script>
        // Event delegation for data-action attributes
        document.addEventListener('click', function(e) {{
            const action = e.target.getAttribute('data-action');
            if (action) {{
                switch(action) {{
                    case 'toggle-musing':
                        const filename = e.target.getAttribute('data-filename');
                        if (filename) {{
                            toggleMusing(filename);
                        }}
                        break;
                }}
            }}
        }});

        function toggleMusing(filename) {{
            const content = document.getElementById('content-' + filename);
            const btn = document.getElementById('btn-' + filename);

            if (content.style.display === 'none') {{
                content.style.display = 'block';
                btn.textContent = 'Collapse';
            }} else {{
                content.style.display = 'none';
                btn.textContent = 'Expand';
            }}
        }}

        // Make functions globally accessible for backward compatibility
        window.toggleMusing = toggleMusing;
    </script>
</body>
</html>'''

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Successfully generated {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error writing {output_file}: {e}")
        return False

def main():
    """Main execution function"""
    print("🚀 AI Musings Generator")
    success = generate_ai_musings_html()

    if success:
        print("🎯 AI Musings page generated successfully!")
    else:
        print("❌ Failed to generate AI Musings page")
        exit(1)

if __name__ == "__main__":
    main()