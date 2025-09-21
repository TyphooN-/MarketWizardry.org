// NFT Gallery JavaScript functionality
// This file handles image grid population, modal navigation, and infinite scrolling

let currentImageIndex = 0;
let allImagePaths = []; // Will be populated by the HTML page
const imagesPerLoad = 50; // Number of images to load per scroll
const scrollThreshold = 1000; // Load more images when 1000px from bottom
const imageGrid = document.getElementById('imageGrid');
const modal = document.getElementById('fullscreenModal');
const modalImage = document.querySelector('.full-image');
const prevButton = document.getElementById('prevButton');
const nextButton = document.getElementById('nextButton');
const imageCounter = document.getElementById('imageCounter');
const modalFilename = document.getElementById('modalFilename');
const twitterLinkContainer = document.getElementById('twitterLinkContainer');
const twitterLink = document.getElementById('twitterLink');
let imagesLoaded = 0;

function initializeGallery(imagePaths) {
    allImagePaths = imagePaths;
    console.log("All Image Paths:", allImagePaths);

    if (allImagePaths.length > 0) {
        loadMoreImages();
        setupInfiniteScroll();
    }
}

function loadMoreImages() {
    console.log("loadMoreImages called. currentImageIndex:", currentImageIndex, "allImagePaths.length:", allImagePaths.length);
    if (currentImageIndex >= allImagePaths.length) {
        console.log("All images have been loaded.");
        return;
    }

    const startIndex = imagesLoaded;
    const endIndex = Math.min(startIndex + imagesPerLoad, allImagePaths.length);

    for (let i = startIndex; i < endIndex; i++) {
        loadImage(allImagePaths[i], i);
    }

    imagesLoaded = endIndex;
    console.log("Loaded images up to index:", endIndex - 1);
}

function loadImage(imagePath, index) {
    const imageContainer = document.createElement('div');
    imageContainer.className = 'image-container';
    imageContainer.setAttribute('data-index', index);

    const img = document.createElement('img');
    img.className = 'thumbnail';
    img.src = imagePath;
    img.alt = `Gallery image ${index + 1}`;
    img.loading = 'lazy';

    // Extract filename from path for display
    const filename = imagePath.split('/').pop().replace(/'/g, '');
    img.setAttribute('data-filename', filename);

    img.addEventListener('click', () => {
        openModal(index);
    });

    img.addEventListener('load', () => {
        console.log(`Image ${index + 1} loaded successfully`);
    });

    img.addEventListener('error', (e) => {
        console.error(`Failed to load image ${index + 1}:`, imagePath);
        imageContainer.style.display = 'none';
    });

    imageContainer.appendChild(img);
    imageGrid.appendChild(imageContainer);
}

function setupInfiniteScroll() {
    function handleScroll() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - scrollThreshold) {
            loadMoreImages();
        }
    }

    window.addEventListener('scroll', handleScroll);
}

function openModal(index) {
    currentImageIndex = index;
    const imagePath = allImagePaths[index];
    console.log("Opening modal for image:", imagePath, "at index:", index);

    modalImage.src = imagePath;

    // Extract and display filename
    const filename = imagePath.split('/').pop().replace(/'/g, '');
    modalFilename.textContent = filename;

    // Handle Twitter link
    const tweetId = extractTweetId(filename);
    if (tweetId) {
        const twitterUrl = `https://twitter.com/i/status/${tweetId}`;
        twitterLink.href = twitterUrl;
        twitterLinkContainer.style.display = 'block';
    } else {
        twitterLinkContainer.style.display = 'none';
    }

    // Update navigation buttons
    prevButton.disabled = index === 0;
    nextButton.disabled = index === allImagePaths.length - 1;
    imageCounter.textContent = `${index + 1} / ${allImagePaths.length}`;

    modal.style.display = 'flex';
}

function closeModal() {
    modal.style.display = 'none';
}

function previousImage() {
    if (currentImageIndex > 0) {
        openModal(currentImageIndex - 1);
    }
}

function nextImage() {
    if (currentImageIndex < allImagePaths.length - 1) {
        openModal(currentImageIndex + 1);
    }
}

function downloadImage() {
    if (typeof currentImageIndex !== 'undefined' && typeof allImagePaths !== 'undefined') {
        const currentImagePath = allImagePaths[currentImageIndex];
        if (currentImagePath) {
            const link = document.createElement('a');
            link.href = currentImagePath.replace(/'/g, ''); // Remove quotes
            link.download = currentImagePath.split('/').pop().replace(/'/g, '');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

function extractTweetId(filename) {
    // Extract tweet ID from filename if it follows the pattern USERNAME-TWEETID-...
    const parts = filename.split('-');
    if (parts.length >= 2) {
        const potentialTweetId = parts[1];
        // Check if it's a valid tweet ID (numeric and reasonable length)
        if (/^\d+$/.test(potentialTweetId) && potentialTweetId.length >= 10) {
            return potentialTweetId;
        }
    }
    return null;
}

// Make functions globally accessible for backward compatibility
window.openModal = openModal;
window.closeModal = closeModal;
window.previousImage = previousImage;
window.nextImage = nextImage;
window.downloadImage = downloadImage;
window.initializeGallery = initializeGallery;

// Keyboard navigation
document.addEventListener('keydown', function(event) {
    if (modal.style.display === 'flex') {
        switch(event.key) {
            case 'ArrowLeft':
                previousImage();
                event.preventDefault();
                break;
            case 'ArrowRight':
                nextImage();
                event.preventDefault();
                break;
            case 'Escape':
                modal.style.display = 'none';
                break;
        }
    }
});