/**
 * Blac AI Gallery JavaScript
 * Extracted from inline script for CSP compliance
 * Handles image gallery functionality, lazy loading, and modal display
 */

let currentImageIndex = 0;
const allImagePaths = [
    './blac_ai/webp/blac_ai-1927475398-SOLD_video1-lossy.webp',
    './blac_ai/webp/blac_ai-1942045151767273817-sunday_night__gn_video4-lossy.webp',
    './blac_ai/webp/blac_ai-1940767483738177538-gm__wake_up_video4-lossy.webp',
    './blac_ai/webp/blac_ai-1942223829847212178-gm__monday_vibes_video4-lossy.webp',
    './blac_ai/webp/blac_ai-1926092032-at_the_end..._gn_video2-lossy.webp',
    './blac_ai/webp/blac_ai-1940837193083138199-deep_rooted_video3-lossy.webp',
    './blac_ai/webp/blac_ai-1927430100-as_above_video2-lossy.webp',
    './blac_ai/webp/blac_ai-1934424689172156708-gn_video4-lossy.webp',
    './blac_ai/webp/blac_ai-1938661355319415191-Syncretica_propaganda_in_NYC_video3-lossy.webp',
    './blac_ai/webp/blac_ai-1927722023-wake_up_video2-lossy.webp',
    './blac_ai/webp/blac_ai-1926998255-GM_video2-lossy.webp',
    './blac_ai/webp/blac_ai-1936054679601115167-wake_up__gm_video4-lossy.webp',
    './blac_ai/webp/blac_ai-1929352768-gn_video2-lossy.webp'
];

console.log("All Image Paths:", allImagePaths);

const imagesPerLoad = 50; // Increased number of images to load per scroll
const scrollThreshold = 1000; // Load more images when 1000px from bottom
const imageGrid = document.getElementById('imageGrid');

function loadImage(path, index) {
    const imgContainer = document.createElement('div');
    imgContainer.className = 'image-container';
    const img = document.createElement('img');
    img.className = 'thumbnail';
    img.src = path;
    img.onerror = function() { console.error("Error loading image:", path); };
    img.onload = function() { console.log("Image loaded:", path); };

    // Use addEventListener instead of onclick for CSP compliance
    img.addEventListener('click', function() { openImage(index); });

    imgContainer.appendChild(img);
    imageGrid.appendChild(imgContainer);
}

function loadMoreImages() {
    console.log("loadMoreImages called. currentImageIndex:", currentImageIndex, "allImagePaths.length:", allImagePaths.length);
    if (currentImageIndex >= allImagePaths.length) {
        console.log("No more images to load.");
        return; // No more images to load
    }

    const startIndex = currentImageIndex;
    const endIndex = Math.min(startIndex + imagesPerLoad, allImagePaths.length);

    for (let i = startIndex; i < endIndex; i++) {
        loadImage(allImagePaths[i], i);
    }
    currentImageIndex = endIndex;
    console.log("Loaded images up to index:", currentImageIndex);
}

function openImage(index) {
    const modal = document.getElementById('fullscreenModal');
    const fullImage = modal.querySelector('.full-image');
    const filenameDisplay = document.getElementById('modalFilename');

    if (index >= 0 && index < allImagePaths.length) {
        const imagePath = allImagePaths[index];
        const filename = imagePath.split('/').pop();

        fullImage.src = imagePath;
        filenameDisplay.textContent = filename;
        modal.style.display = 'flex';
        document.body.classList.add('modal-open');

        console.log("Opening image:", imagePath);
    } else {
        console.error("Invalid image index:", index);
    }
}

function closeModal() {
    const modal = document.getElementById('fullscreenModal');
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');
    console.log("Modal closed");
}

// Initialize gallery functionality
function initGallery() {
    // Load initial images
    loadMoreImages();

    // Set up scroll-based lazy loading
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        if (documentHeight - scrollTop - windowHeight < scrollThreshold) {
            loadMoreImages();
        }
    });

    // Set up modal event listeners (CSP compliant)
    const modal = document.getElementById('fullscreenModal');
    const modalContent = modal.querySelector('.modal-content');

    // Close modal when clicking outside content
    modal.addEventListener('click', closeModal);

    // Prevent closing when clicking inside modal content
    modalContent.addEventListener('click', function(event) {
        event.stopPropagation();
    });

    // Close modal with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });

    console.log("Gallery initialized with", allImagePaths.length, "total images");
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGallery);
} else {
    initGallery();
}

// Make closeModal globally available for any remaining inline references
window.closeModal = closeModal;