#!/usr/bin/env python3
"""
EV Explorer Generator - MarketWizardry.org

EV calculations for gambling addicts who pretend they're investors.
Statistically validate your financial suicide with mathematical precision.

Turning expected value theory into a weapon of mass portfolio destruction
since whenever this script was first written.
"""

import os
import re

# Define the directory containing CSV files and output HTML file path
directory = './ev-explorer/'
output_html_file = 'ev-explorer.html'

# --- Ensure the script is executable and run it ---
# Note: The outlier script execution part is removed as per user request.

# Pattern for matching file names
pattern = re.compile(r"SymbolsExport-Darwinex-Live-Stocks-(\d{4}\.\d{2}\.\d{2})-EV-(ev_outlier|ev_var_outlier)\.txt")

# Collect all .txt files in the directory that match the naming patterns
files = []
for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        date_part = match.group(1)
        report_type = match.group(2)
        csv_filename = f"SymbolsExport-Darwinex-Live-Stocks-{date_part}-EV.csv"
        files.append((filename, date_part, csv_filename, report_type))

# Sort files by the extracted dates for display order
files.sort(key=lambda x: x[1], reverse=True)

# Generate HTML content
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="author" content="TyphooN">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarketWizardry.org | EV Explorer</title>
    <link rel="canonical" href="https://marketwizardry.org/ev-explorer.html">
    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png">
    <!-- Standard Meta Tags -->
    <meta name="description" content="EV calculations for gambling addicts who pretend they're investors. Statistically validate your financial suicide with mathematical precision.">
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="EV Explorer - MarketWizardry.org">
    <meta property="og:description" content="EV calculations for gambling addicts who pretend they're investors. Statistically validate your financial suicide with mathematical precision.">
    <meta property="og:url" content="https://marketwizardry.org/ev-explorer.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Market Wizardry">
    <meta property="og:image" content="https://marketwizardry.org/img/xicojam-1924524951521853846-prompt-video1-mod-mod.webp">
    <meta property="og:image:alt" content="MarketWizardry.org - Financial Trading Tools">
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="EV Explorer - MarketWizardry.org">
    <meta name="twitter:description" content="EV calculations for gambling addicts who pretend they're investors. Statistically validate your financial suicide with mathematical precision.">
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
            white-space: pre-wrap; /* Preserve whitespace but allow text wrapping */
            max-height: 70vh; /* Limit height and enable scrolling */
            overflow-y: auto;
            color: #00ff00;
            font-size: 1.2em;
            padding: 15px;
            word-break: break-word;
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
                font-size: 0.8em;
                padding: 4px 8px;
                margin: 2px;
            }}
            .modal-body {{
                font-size: 0.75em;
                white-space: pre-wrap;
                word-break: break-word;
                max-height: calc(90vh - 120px);
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>EV Explorer</h1>
        <div class="crt-divider"></div>
        <div class="flavor-text">Enterprise Value calculations for gamblers who pretend they're investors. Because statistical delusions make losing money feel more professional.</div>
        <div class="crt-divider"></div>
        <div class="grid">"""

# Add each file as an entry in the HTML
for filename, date_str, csv_filename, report_type in files:
    file_type = ""
    if report_type == "ev_var_outlier":
        file_type = "EV VaR Outlier"
    elif report_type == "ev_outlier":
        file_type = "EV Outlier"

    formatted_date = date_str.replace('.', '-')
    link_text = f"Darwinex-Live (Stocks) - {formatted_date} ({file_type})"

    file_entry = f'''
            <div class="file-entry" onclick="openModalWithFile('{filename}', 'ev-explorer/{csv_filename}', '{link_text}')">
                <a href="#" data-outlier-file="{filename}" data-csv-file="{csv_filename}" onclick="event.stopPropagation()">
                    {link_text}
                </a>
            </div>'''
    html_content += file_entry

# Close the HTML tags and add modal structure and script
html_content += """
        </div>
    </div>

    <!-- The Modal -->
    <div id="outlierModal" class="modal">
        <!-- Modal content -->
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle"></h2>
                <a id="downloadOutlierLink" href="#" download onclick="forceDownload(event, this)">Download Report</a>
                <a id="downloadCsvLink" href="#" download onclick="forceDownload(event, this)">Download Original CSV</a>
                <span class="close-button">&times;</span>
            </div>
            <pre id="outlierContent" class="modal-body"></pre>
        </div>
    </div>

    <script>
        // Force download function
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
            const outlierUrl = 'ev-explorer/' + outlierFileName;
            const csvUrl = 'ev-explorer/' + csvFileName;
            const fileName = link.textContent.trim();

            modalTitle.textContent = "EV Report for " + fileName;
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
                })
                .catch(error => {
                    console.error("Error fetching outlier report:", error);
                    outlierContent.textContent = "Error loading report.";
                    modal.style.display = "block";
                });
        }

        fileEntryLinks.forEach((link, index) => {
            link.addEventListener("click", function(event) {
                event.preventDefault();
                openModalAtIndex(index);
            });
        });

        closeButton.addEventListener("click", function() {
            modal.style.display = "none";
        });

        window.addEventListener("click", function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        });

        window.addEventListener("keydown", function(event) {
            if (modal.style.display === "block") {
                if (event.key === "Escape") {
                    modal.style.display = "none";
                } else if (event.key === "ArrowLeft") {
                    currentIndex = (currentIndex > 0) ? currentIndex - 1 : fileEntryLinks.length - 1;
                    openModalAtIndex(currentIndex);
                } else if (event.key === "ArrowRight") {
                    currentIndex = (currentIndex < fileEntryLinks.length - 1) ? currentIndex + 1 : 0;
                    openModalAtIndex(currentIndex);
                }
            }
        });
    </script>
</body>
</html>"""

# Write to the output HTML file
with open(output_html_file, 'w') as f:
    f.write(html_content)

print(f"HTML generated and saved to {output_html_file}")