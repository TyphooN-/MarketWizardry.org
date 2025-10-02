#!/bin/bash
# Generator script for gallery-data JavaScript files
# Usage: ./scripts/generate-gallery-data.sh <html-file> [selector]
#
# Examples:
#   ./scripts/generate-gallery-data.sh market-wizardry.html
#   ./scripts/generate-gallery-data.sh affiliates.html ".affiliate-content img"
#   ./scripts/generate-gallery-data.sh var-cult.html ".image-container img, .inline-images img"

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <html-file> [selector]"
    echo ""
    echo "Generates a gallery-data JS file for pages with static images (non-gallery pages)."
    echo ""
    echo "Arguments:"
    echo "  html-file    The HTML file (e.g., market-wizardry.html, affiliates.html)"
    echo "  selector     Optional CSS selector for images (default: '.image-container img, .grid-container img')"
    echo ""
    echo "Examples:"
    echo "  $0 market-wizardry.html"
    echo "  $0 affiliates.html '.affiliate-content img'"
    echo "  $0 var-cult.html '.image-container img, .inline-images img'"
    exit 1
fi

HTML_FILE="$1"
SELECTOR="${2:-.image-container img, .grid-container img}"

# Extract base name without extension
BASE_NAME=$(basename "$HTML_FILE" .html)

# Output file path
OUTPUT_FILE="js/gallery-data-${BASE_NAME}.js"

echo "Generating gallery-data file: $OUTPUT_FILE"
echo "HTML file: $HTML_FILE"
echo "Selector: $SELECTOR"

# Generate the JavaScript file
cat > "$OUTPUT_FILE" << EOF
// Gallery data for ${HTML_FILE}
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('$SELECTOR');
    const imagePaths = Array.from(images).map(img => img.src);
    if (window.initializeGallery) {
        // Pass true to skip dynamic loading since images are already in DOM
        window.initializeGallery(imagePaths, true);
    }
});
EOF

echo "✓ Generated: $OUTPUT_FILE"
echo ""
echo "Make sure to include these scripts in $HTML_FILE:"
echo "  <script src=\"/js/gallery.js\"></script>"
echo "  <script src=\"/js/gallery-data-${BASE_NAME}.js\"></script>"
echo ""
echo "And ensure the modal HTML is present in the page:"
echo "  <div class=\"modal\" id=\"fullscreenModal\">...</div>"
