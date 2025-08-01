import os
import stat

# Define the directory containing CSV files and output HTML file path
directory = './var-explorer/'
output_html_file = 'var-explorer.html'

# Path to the outlier analysis script
outlier_script_path = os.path.join(directory, 'run_outlier_analysis.sh')

# --- Ensure the script is executable and run it ---
if os.path.exists(outlier_script_path):
    # Check if the script has execute permissions
    if not os.access(outlier_script_path, os.X_OK):
        print(f"Script at {outlier_script_path} is not executable. Adding execute permissions...")
        # Add execute permissions (owner and group)
        os.chmod(outlier_script_path, os.stat(outlier_script_path).st_mode | stat.S_IXUSR | stat.S_IXGRP)
    
    # Run the outlier analysis script
    print(f"Running outlier analysis script: {outlier_script_path}")
    original_cwd = os.getcwd()
    os.chdir(directory) # Change to the directory where the script expects to find files
    os.system(f"bash {os.path.basename(outlier_script_path)}") # Execute the script by its name
    os.chdir(original_cwd) # Change back to the original working directory
    print("Outlier analysis script finished.")
else:
    print(f"Warning: Outlier script not found at {outlier_script_path}")

# Pattern for matching file names (e.g., start with "SymbolsExport-Darwinex-Live")
pattern_start = "SymbolsExport-Darwinex-Live"

# Collect all .csv files in the directory that match the naming pattern
files = []
for filename in os.listdir(directory):
    if filename.endswith(".csv") and filename.startswith(pattern_start):
        # Extract date from file name assuming format 'SymbolsExport-...YYYY.MM.DD.csv'
        parts = filename.split('-')
        try:
            date_part = '-'.join(parts[-1].split('.')[:3])  # Join YYYY, MM, DD
        except IndexError:
            continue
        
        files.append((filename, date_part))

# Sort files by the extracted dates for display order
files.sort(key=lambda x: x[1], reverse=True)

# Generate HTML content
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>VaR Explorer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
            border-bottom: 2px solid rgba(0, 255, 0, 0.5);
            padding-bottom: 10px;
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
            white-space: pre-wrap; /* Preserve whitespace and wrap text */
            word-wrap: break-word; /* Break long words */
            max-height: 70vh; /* Limit height and enable scrolling */
            overflow-y: auto;
            color: #00ff00;
            font-size: 1.2em;
            padding: 15px;
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

        @media screen and (max-width: 600px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
            .modal-content {{
                margin: 10% auto;
                width: 90%;
            }}
            .modal-body {{
                font-size: 0.6em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>VaR Explorer</h1>
        <div class="grid">"""

# Add each file as an entry in the HTML
for filename, date_str in files:
    file_type = ""
    if "Stocks" in filename:
        file_type = "Stocks"
    elif "Futures" in filename:
        file_type = "Futures"
    elif "CFD" in filename:
        file_type = "CFD"

    outlier_filename = f"{filename.replace('.csv', '')}-outlier.txt"
    
    file_entry = f'''
            <div class="file-entry">
                <a href="https://marketwizardry.org//var-explorer/{filename}" data-outlier-file="{outlier_filename}">
                    Darwinex-Live ({file_type}) - {date_str}
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
                <a id="downloadOutlierLink" href="#" download>Download Outlier Report</a>
                <a id="downloadCsvLink" href="#" download>Download Original CSV</a>
                <span class="close-button">&times;</span>
            </div>
            <pre id="outlierContent" class="modal-body"></pre>
        </div>
    </div>

    <script>
        const modal = document.getElementById("outlierModal");
        const closeButton = document.getElementsByClassName("close-button")[0];
        const modalTitle = document.getElementById("modalTitle");
        const outlierContent = document.getElementById("outlierContent");
        const downloadCsvLink = document.getElementById("downloadCsvLink");
        const downloadOutlierLink = document.getElementById("downloadOutlierLink");
        const fileEntryLinks = document.querySelectorAll(".file-entry a");
        let currentIndex = 0;

        function openModalAtIndex(index) {{
            const link = fileEntryLinks[index];
            const csvUrl = link.href;
            const outlierFileName = link.dataset.outlierFile;
            const outlierUrl = 'var-explorer/' + outlierFileName;
            const fileName = link.textContent.trim();

            modalTitle.textContent = "VaR Outlier Report for " + fileName;
            downloadCsvLink.href = csvUrl;
            downloadOutlierLink.href = outlierUrl;
            downloadOutlierLink.download = outlierFileName;

            fetch(outlierUrl)
                .then(response => {{
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }}
                    return response.text();
                }})
                .then(data => {{
                    outlierContent.textContent = data;
                    modal.style.display = "block";
                    currentIndex = index;
                }})
                .catch(error => {{
                    console.error("Error fetching outlier report:", error);
                    outlierContent.textContent = "Error loading report.";
                    modal.style.display = "block";
                }});
        }}

        fileEntryLinks.forEach((link, index) => {{
            link.addEventListener("click", function(event) {{
                event.preventDefault();
                openModalAtIndex(index);
            }});
        }});

        closeButton.addEventListener("click", function() {{
            modal.style.display = "none";
        }});

        window.addEventListener("click", function(event) {{
            if (event.target == modal) {{
                modal.style.display = "none";
            }}
        }});

        window.addEventListener("keydown", function(event) {{
            if (modal.style.display === "block") {{
                if (event.key === "Escape") {{
                    modal.style.display = "none";
                }} else if (event.key === "ArrowLeft") {{
                    currentIndex = (currentIndex > 0) ? currentIndex - 1 : fileEntryLinks.length - 1;
                    openModalAtIndex(currentIndex);
                }} else if (event.key === "ArrowRight") {{
                    currentIndex = (currentIndex < fileEntryLinks.length - 1) ? currentIndex + 1 : 0;
                    openModalAtIndex(currentIndex);
                }}
            }}
        }});
    </script>
</body>
</html>"""

# Write to the output HTML file
with open(output_html_file, 'w') as f:
    f.write(html_content)

print(f"HTML generated and saved to {output_html_file}")
