#!/usr/bin/env python3
"""
ATR Explorer Generator - MarketWizardry.org
Enhanced with comprehensive SEO and breadcrumb navigation

ATR calculations for volatility junkies who mistake chaos for opportunity.
Turn market turbulence into a statistical weapon of financial self-destruction.

Converting average true range into averaged true devastation
since whenever this script was first written.
"""

import os
import re
from datetime import datetime

# Import the new SEO system
from seo_templates import SEOManager, PAGE_CONFIGS, get_breadcrumb_paths, REDIRECT_SCRIPT_TEMPLATE

# Define the directory containing CSV files and output HTML file path
directory = './atr-explorer/'
output_html_file = 'atr-explorer.html'

# --- Ensure the script is executable and run it ---
# Note: The outlier script execution part is removed as per user request.

# Pattern for matching file names
pattern = re.compile(r"SymbolsExport-Darwinex-Live-(CFD|Futures|Stocks)-(\d{4}\.\d{2}\.\d{2})-outlier\.txt")

# Collect all .txt files in the directory that match the naming patterns
files = []
for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        asset_type = match.group(1)
        date_part = match.group(2)
        csv_filename = f"SymbolsExport-Darwinex-Live-{asset_type}-{date_part}.csv"
        files.append((filename, date_part, csv_filename, asset_type))

# Sort files by the extracted dates for display order
files.sort(key=lambda x: x[1], reverse=True)

# Initialize SEO Manager and generate enhanced HTML
seo_manager = SEOManager()

# Configure page-specific SEO
page_config = PAGE_CONFIGS['explorer'].copy()
page_config.update({
    'title': 'MarketWizardry.org | ATR Explorer',
    'canonical_url': 'https://marketwizardry.org/atr-explorer.html',
    'description': 'Average True Range calculations for volatility junkies who mistake chaos for opportunity. Turn market turbulence into a statistical weapon of financial self-destruction.',
    'keywords': f"{page_config['keywords_base']}, ATR explorer, average true range, volatility analysis, market volatility, risk analysis, price volatility",
    'og_title': 'ATR Explorer - MarketWizardry.org',
    'og_description': 'Average True Range calculations for volatility junkies who mistake chaos for opportunity. Turn market turbulence into a statistical weapon of financial self-destruction.',
    'twitter_title': 'ATR Explorer - MarketWizardry.org',
    'twitter_description': 'ATR calculations with statistical precision. Real-time volatility analysis.'
})

# Generate breadcrumb navigation
breadcrumb_paths = get_breadcrumb_paths()
atr_breadcrumbs = breadcrumb_paths['atr_explorer']

# Generate schema.org data
schema_config = {
    'type': 'WebApplication',
    'name': 'ATR Explorer',
    'url': page_config['canonical_url'],
    'description': page_config['description'],
    'additional_properties': {
        'applicationCategory': 'FinanceApplication',
        'operatingSystem': 'Web Browser',
        'dateModified': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00'),
        'featureList': [
            'Average True Range calculations',
            'Real-time market volatility analysis',
            'Price volatility assessment',
            'Outlier detection',
            'Historical volatility analysis'
        ]
    }
}

# Generate all SEO components
seo_meta_tags = seo_manager.generate_enhanced_meta_tags(page_config)
breadcrumb_navigation = seo_manager.generate_breadcrumbs(atr_breadcrumbs)
breadcrumb_css = seo_manager.generate_breadcrumb_css()
json_ld_schema = seo_manager.generate_json_ld_schema(schema_config)

# Generate HTML content with enhanced SEO
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
{seo_meta_tags}

{json_ld_schema}

{REDIRECT_SCRIPT_TEMPLATE}
    <style>
        body {{
            background-color: #000;
            color: #00ff00;
            font-family: "Courier New", monospace;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
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
        .grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
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
            position: relative;
        }}
        .file-entry:hover {{
            background-color: #001100;
            color: #00ff00;
            transform: scale(1.02);
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
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

        /* Modal Styles */
        .modal {{
            display: none; /* Hidden by default */
            position: fixed; /* Stay in place */
            z-index: 1; /* Sit on top */
            left: 0;
            top: 0;
            width: 100%; /* Full width */
            height: 100%; /* Full height */
            overflow: auto; /* Enable scroll if needed */
            background-color: rgba(0,0,0,0.8); /* Black w/ opacity */
            padding-top: 60px;
        }}

        .modal-content {{
            background-color: #000;
            margin: 5% auto; /* 15% from the top and centered */
            padding: 10px; /* Reduced padding */
            border: 2px solid #00ff00; /* Green border */
            max-width: fit-content; /* Adjust width to content */
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            animation-name: animatetop;
            animation-duration: 0.4s
        }}

        .modal-header {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-bottom: 1px solid rgba(0, 255, 0, 0.5);
            padding-bottom: 5px; /* Reduced padding */
            margin-bottom: 5px; /* Reduced margin */
        }}

        .modal-header h2 {{
            margin: 0;
            color: #00ff00;
            font-size: 1.2em; /* Smaller header font size */
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

        .modal-body {{
            white-space: pre; /* Preserve whitespace, no text wrapping */
            max-height: 60vh; /* Reduced to leave space for navigation buttons */
            overflow-y: auto;
            overflow-x: auto; /* Enable horizontal scrolling */
            color: #00ff00;
            font-size: 1.2em;
            padding: 15px;
        }}

        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
            gap: 10px;
            padding: 0 15px;
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

        .nav-counter {{
            color: #00ff00;
            font-family: "Courier New", monospace;
            font-size: 0.9em;
        }}

        /* Add Animation */
        @-webkit-keyframes animatetop {{
            from {{top:-300px; opacity:0}}
            to {{top:0; opacity:1}}
        }}

        @keyframes animatetop {{
            from {{top:-300px; opacity:0}}
            to {{top:0; opacity:1}}
        }}

        @media screen and (max-width: 768px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
            .modal {{
                padding-top: 20px;
            }}
            .modal-content {{
                margin: 2% auto;
                width: 95%;
                max-height: 90vh;
                overflow-y: auto;
            }}
            .modal-header {{
                flex-wrap: wrap;
                gap: 8px;
            }}
            .modal-header h2 {{
                font-size: 1em;
                margin-bottom: 8px;
                flex: 1 0 100%;
            }}
            .modal-header a {{
                font-size: 0.7em;
                padding: 4px 8px;
                margin: 2px;
            }}
            .modal-body {{
                font-size: 0.65em;
                white-space: pre;
                overflow-x: auto;
                max-height: calc(90vh - 160px);
                padding: 10px;
            }}
            .nav-button {{
                padding: 8px 15px;
                font-size: 14px;
                min-width: 60px;
            }}
            .nav-counter {{
                font-size: 0.8em;
            }}
        }}

{breadcrumb_css}
    </style>
</head>
<body>
    <div class="container">
{breadcrumb_navigation}
        <h1>ATR Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">ATR calculations for volatility junkies who mistake chaos for opportunity. Turn market turbulence into a statistical weapon of financial self-destruction.</div>
        <div class="crt-divider"></div>
        <div class="grid">
"""

# Generate file entries
for filename, date_part, csv_filename, asset_type in files:
    # Format the date for display
    formatted_date = date_part.replace('.', '-')
    display_name = f"Darwinex-Live ({asset_type}) - {formatted_date}"

    html_content += f"""            <div class="file-entry" onclick="openModalWithFile('{filename}', 'atr-explorer/{csv_filename}', '{display_name}')">
                <a href="#" data-outlier-file="{filename}" data-csv-file="{csv_filename}" onclick="event.stopPropagation()">
                    {display_name}
                </a>
            </div>
"""

html_content += """        </div>
    </div>

    <!-- Modal -->
    <div id="outlierModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle"></h2>
                <a id="downloadOutlierLink" href="#" download onclick="forceDownload(event, this)">Download Report</a>
                <a id="downloadCsvLink" href="#" download onclick="forceDownload(event, this)">Download Original CSV</a>
                <span class="close-button">&times;</span>
            </div>
            <pre id="outlierContent" class="modal-body"></pre>
            <div class="nav-buttons">
                <button class="nav-button" id="prevButton" onclick="navigatePrevious()">← Previous</button>
                <span class="nav-counter" id="navCounter"></span>
                <button class="nav-button" id="nextButton" onclick="navigateNext()">Next →</button>
            </div>
        </div>
    </div>

    <script>
        function downloadData(url, filename) {
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.blob();
                })
                .then(blob => {
                    const downloadUrl = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = downloadUrl;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(downloadUrl);
                    document.body.removeChild(a);
                })
                .catch(error => console.error('Download failed:', error));
        }

        function openModalWithFile(outlierFile, csvUrl, linkText) {
            const outlierUrl = location.pathname.replace('.html', '/') + outlierFile;
            const csvFileName = csvUrl.split('/').pop();

            modalTitle.textContent = "Report for " + linkText;
            downloadOutlierLink.href = outlierUrl;
            downloadOutlierLink.download = outlierFile;
            downloadCsvLink.href = csvUrl;
            downloadCsvLink.download = csvFileName;

            fetch(outlierUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(data => {
                    outlierContent.textContent = data;
                    modal.style.display = "block";
                })
                .catch(error => {
                    console.error("Error fetching outlier report:", error);
                    outlierContent.textContent = "Error loading report.";
                    modal.style.display = "block";
                });
        }

        const modal = document.getElementById("outlierModal");
        const closeButton = document.getElementsByClassName("close-button")[0];
        const modalTitle = document.getElementById("modalTitle");
        const outlierContent = document.getElementById("outlierContent");
        const downloadOutlierLink = document.getElementById("downloadOutlierLink");
        const downloadCsvLink = document.getElementById("downloadCsvLink");
        const fileEntryLinks = document.querySelectorAll(".file-entry a");
        let currentIndex = 0;

        function openModalAtIndex(index) {
            const link = fileEntryLinks[index];
            const outlierFileName = link.dataset.outlierFile;
            const csvFileName = link.dataset.csvFile;
            const outlierUrl = 'atr-explorer/' + outlierFileName;
            const csvUrl = 'atr-explorer/' + csvFileName;
            const fileName = link.textContent.trim();

            modalTitle.textContent = "ATR Report for " + fileName;
            downloadOutlierLink.href = outlierUrl;
            downloadOutlierLink.download = outlierFileName;
            downloadCsvLink.href = csvUrl;
            downloadCsvLink.download = csvFileName;

            fetch(outlierUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(data => {
                    outlierContent.textContent = data;
                    modal.style.display = "block";
                    currentIndex = index;
                });
            updateNavigationButtons();
        }

        function updateNavigationButtons() {
            const prevButton = document.getElementById('prevButton');
            const nextButton = document.getElementById('nextButton');
            const navCounter = document.getElementById('navCounter');

            if (prevButton && nextButton && navCounter) {
                prevButton.disabled = currentIndex <= 0;
                nextButton.disabled = currentIndex >= fileEntryLinks.length - 1;
                navCounter.textContent = `${currentIndex + 1} / ${fileEntryLinks.length}`;
            }
        }

        function navigatePrevious() {
            if (currentIndex > 0) {
                currentIndex--;
                openModalAtIndex(currentIndex);
            }
        }

        function navigateNext() {
            if (currentIndex < fileEntryLinks.length - 1) {
                currentIndex++;
                openModalAtIndex(currentIndex);
            }
        }

        function forceDownload(event, link) {
            event.preventDefault();
            const url = link.href;
            const filename = link.download || url.split('/').pop();

            fetch(url)
                .then(response => response.blob())
                .then(blob => {
                    const downloadUrl = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = downloadUrl;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(downloadUrl);
                    document.body.removeChild(a);
                })
                .catch(err => console.error('Download failed:', err));
        }

        fileEntryLinks.forEach((link, index) => {
            link.addEventListener("click", (event) => {
                event.preventDefault();
                openModalAtIndex(index);
            });
        });

        closeButton.onclick = function() {
            modal.style.display = "none";
        };

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        };

        window.addEventListener("keydown", function(event) {
            if (modal.style.display === "block") {
                if (event.key === "Escape") {
                    modal.style.display = "none";
                } else if (event.key === "ArrowLeft") {
                    navigatePrevious();
                } else if (event.key === "ArrowRight") {
                    navigateNext();
                }
            }
        });
    </script>
</body>
</html>"""

# Write the HTML content to the file
with open(output_html_file, 'w') as file:
    file.write(html_content)

print(f"Generated {output_html_file} with {len(files)} files")