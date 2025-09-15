#!/usr/bin/env python3
"""
VaR Explorer Generator - MarketWizardry.org

VaR calculations for degenerates who need mathematical proof their portfolio is doomed.
Watch your money evaporate with scientific precision.

Turning Value at Risk theory into a weapon of mass portfolio destruction
since whenever this script was first written.
"""

import os
import re

# Define the directory containing CSV files and output HTML file path
directory = './var-explorer/'
output_html_file = 'var-explorer.html'

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

# Generate HTML content
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="TyphooN">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarketWizardry.org | VaR Explorer</title>
    <link rel="canonical" href="https://marketwizardry.org/var-explorer.html">
    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">
    <!-- Standard Meta Tags -->
    <meta name="description" content="Value at Risk calculations for degenerates who need mathematical proof their portfolio is doomed. Watch your money evaporate with scientific precision.">
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="VaR Explorer - MarketWizardry.org">
    <meta property="og:description" content="Value at Risk calculations for degenerates who need mathematical proof their portfolio is doomed. Watch your money evaporate with scientific precision.">
    <meta property="og:url" content="https://marketwizardry.org/var-explorer.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Market Wizardry">
    <meta property="og:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <meta property="og:image:alt" content="MarketWizardry.org - Financial Trading Tools">
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="VaR Explorer - MarketWizardry.org">
    <meta name="twitter:description" content="Value at Risk calculations for degenerates who need mathematical proof their portfolio is doomed. Watch your money evaporate with scientific precision.">
    <meta name="twitter:site" content="@MarketW1zardry">
    <meta name="twitter:creator" content="@MarketW1zardry">
    <meta name="twitter:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <script>
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
        .file-entry a {{
            color: inherit;
            text-decoration: none;
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }}
        .file-entry:hover a {{
            color: #00ff00;
        }}
        .modal {{
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.9);
        }}
        .modal-content {{
            background-color: #000;
            margin: 5% auto;
            padding: 20px;
            border: 2px solid #00ff00;
            border-radius: 5px;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            width: 90%;
            max-width: 800px;
            text-align: center;
        }}
        .close-button {{
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            background: none;
            border: none;
            margin-top: -10px;
            margin-right: -10px;
        }}
        .close-button:hover,
        .close-button:focus {{
            color: #00ff00;
            text-decoration: none;
        }}
        .modal-header {{
            margin-bottom: 20px;
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

        @media screen and (max-width: 768px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
            .modal-content {{
                width: 95%;
                margin: 2% auto;
                padding: 10px;
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
    </style>
</head>
<body>
    <div class="container">
        <h1>VaR Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Value at Risk calculations for degenerates who need mathematical proof their portfolio is doomed. Watch your money evaporate with scientific precision.</div>
        <div class="crt-divider"></div>
        <div class="grid">
"""

# Generate file entries
for filename, date_part, csv_filename, asset_type in files:
    # Format the date for display
    formatted_date = date_part.replace('.', '-')
    display_name = f"Darwinex-Live ({asset_type}) - {formatted_date}"

    html_content += f"""            <div class="file-entry" onclick="openModalWithFile('{filename}', 'var-explorer/{csv_filename}', '{display_name}')">
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
            <button class="close-button">&times;</button>
            <div class="modal-header">
                <h2 id="modalTitle"></h2>
                <div style="margin-top: 10px;">
                    <a id="downloadOutlierLink" download style="color: #00ff00; margin-right: 20px;">Download Report</a>
                    <a id="downloadCsvLink" download style="color: #00ff00;">Download CSV</a>
                </div>
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
            const outlierUrl = 'var-explorer/' + outlierFileName;
            const csvUrl = 'var-explorer/' + csvFileName;
            const fileName = link.textContent.trim();

            modalTitle.textContent = "VaR Report for " + fileName;
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