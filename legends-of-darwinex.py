import os

def generate_html():
    # Define the base directory and image pattern
    base_dir = "legends-of-darwinex"
    
    # Generate image paths dynamically, checking for existence
    images = []
    for i in range(1, 100000):
        file_path = os.path.join(base_dir, f"{str(i).zfill(5)}.webp")
        if os.path.exists(file_path):
            images.append(file_path)

    # HTML template with dynamic content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Legends of Darwinex</title>
        <style>
            body {{
                background-color: #000;
                color: #00ff00;
                font-family: "Courier New", monospace;
                padding: 20px;
                margin: 0;
            }}
            a {{
                color: #00ff00;
                text-decoration: none;
                font-weight: bold;
            }}
            .image-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}
            .image-container {{
                position: relative;
                width: 100%;
                max-width: 500px; 
                cursor: pointer;
            }}
            .thumbnail {{
                width: 100%;
                height: auto;
                border-radius: 5px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: transform 0.3s ease-in-out;
            }}
            .thumbnail:hover {{
                transform: scale(1.05);
                filter: brightness(1.2);
            }}
            .modal {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.9);
                z-index: 1000;
            }}
            .modal-content {{
                position: relative;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                transform: none;
            }}
            .full-image {{
                width: auto;
                height: auto;
                max-width: 90vw;
                max-height: 90vh;
                margin: 0 auto;
                display: block;
            }}
        </style>
    </head>
    <body>
        <h2>Legends of Darwinex</h2>
        Some Darwins featured here are snake oil salesmen that cannot be saved. Others may merely be a lost soul that has not yet found their way to 
        <a href="https://help.darwinex.com/" target="_blank" rel="noopener noreferrer">Documentation</a> or 
        <a href="https://www.value-at-risk.net/history-of-value-at-risk/" target="_blank" rel="noopener noreferrer">holy VaR light</a>. For further information contact the author (TyphooN), in 
        <a href="http://marketwizardry.info" target="_blank" rel="noopener noreferrer">Discord</a>.
        <div class="image-grid" id="imageGrid">
            {''.join(f'<div class="image-container"><img src="{img}" alt="Image {i+1}" class="thumbnail" onclick="openModal(this.src)"></div>' for i, img in enumerate(images))}
        </div>
        <div class="modal" id="myModal">
            <span class="close" onclick="closeModal()">&times;</span>
            <img class="full-image" id="modal-content">
        </div>

        <script>
            function openModal(src) {{
                document.getElementById('modal-content').src = src;
                document.getElementById('myModal').style.display = 'block';
            }}

            function closeModal() {{
                document.getElementById('myModal').style.display = 'none';
            }}
            
            // Close modal on clicking outside the image
            window.onclick = function(event) {{
                var modal = document.getElementById('myModal');
                if (event.target === modal) {{
                    closeModal();
                }}
            }};
        </script>
    </body>
    </html>
    """

    # Write HTML content to a file
    with open("legends-of-darwinex.html", "w") as html_file:
        html_file.write(html_content)

# Call the function to generate the HTML file
generate_html()

