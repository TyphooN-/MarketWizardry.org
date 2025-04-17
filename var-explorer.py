import os

# Define the directory containing CSV files and output HTML file path
directory = './var-explorer/'
output_html_file = 'var-explorer.html'

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
    </style>
</head>
<body>
    <div class="container">
        <h1>VaR Explorer</h1>
        <div class="grid">"""

# Add each file as an entry in the HTML
for filename, date_str in files:
    if "Stocks" in filename:
        file_type = "Stocks"
    if "Futures" in filename:
        file_type = "Futures"
    if "CFD" in filename:
        file_type = "CFD"  # Or whatever the other type is

    file_entry = f"""
            <div class="file-entry">
                <a href="https://marketwizardry.org//var-explorer/{filename}">
                    Darwinex-Live ({file_type}) - {date_str}
                </a>
            </div>"""
    html_content += file_entry

# Close the HTML tags
html_content += """
        </div>
    </div>
</body>
</html>"""

# Write to the output HTML file
with open(output_html_file, 'w') as f:
    f.write(html_content)

print(f"HTML generated and saved to {output_html_file}")

