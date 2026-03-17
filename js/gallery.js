// Gallery functionality for NFT galleries
// Event delegation handled by shared.js - functions exported to window scope below

let currentImageIndex = 0;
let allImagePaths = []; // Will be set by each gallery file

const imagesPerLoad = 50; // Increased number of images to load per scroll
const scrollThreshold = 1000; // Load more images when 1000px from bottom

function initializeGallery(imagePaths, skipDynamicLoading = false) {
    allImagePaths = imagePaths;

    // Reset current index
    currentImageIndex = 0;

    // If skipDynamicLoading is true, just set up click handlers on existing images
    if (skipDynamicLoading) {
        setupStaticImageClickHandlers();
        return;
    }

    // Initial load for dynamic galleries
    loadMoreImages();
    // Load more images immediately if the initial load doesn't fill the viewport
    if (document.body && document.body.offsetHeight < window.innerHeight) {
        loadMoreImages();
    }

    // Scroll event for lazy loading (throttled with rAF)
    let scrollTicking = false;
    window.addEventListener('scroll', () => {
        if (!scrollTicking) {
            requestAnimationFrame(() => {
                if (window.innerHeight + window.scrollY >= document.body.offsetHeight - scrollThreshold) {
                    loadMoreImages();
                }
                scrollTicking = false;
            });
            scrollTicking = true;
        }
    });
}

function setupStaticImageClickHandlers() {
    // Find all existing images in the DOM and attach click handlers
    const images = document.querySelectorAll('.image-container img, .grid-container img');
    images.forEach((img, index) => {
        img.addEventListener('click', function() {
            openImage(index);
        });
        img.classList.add('clickable-image'); // CSP-compliant cursor styling
    });
}

function loadImage(path, index) {
    const imageGrid = document.getElementById('imageGrid');
    if (!imageGrid) return;

    const imgContainer = document.createElement('div');
    imgContainer.className = 'image-container';
    const img = document.createElement('img');
    img.className = 'thumbnail clickable-image';
    img.loading = 'lazy';
    img.src = path;
    img.addEventListener('click', function() { openImage(index); });
    imgContainer.appendChild(img);
    imageGrid.appendChild(imgContainer);
}

function loadMoreImages() {
    if (currentImageIndex >= allImagePaths.length) {
        return; // No more images to load
    }

    const startIndex = currentImageIndex;
    const endIndex = Math.min(startIndex + imagesPerLoad, allImagePaths.length);

    for (let i = startIndex; i < endIndex; i++) {
        loadImage(allImagePaths[i], i);
    }
    currentImageIndex = endIndex;
}

function openImage(index) {
    currentImageIndex = index;
    const modalImg = document.querySelector('.full-image');
    const modal = document.getElementById('fullscreenModal');
    const modalFilename = document.getElementById('modalFilename');
    const twitterLinkContainer = document.getElementById('twitterLinkContainer');
    const twitterLink = document.getElementById('twitterLink');

    if (!modal || !modalImg) return;

    const imagePath = allImagePaths[index];
    if (!imagePath) return;

    const filename = imagePath.split('/').pop().replace(/'/g, ''); // Extract filename and clean quotes

    modalImg.src = imagePath;
    if (modalFilename) modalFilename.textContent = filename;

    // Extract Twitter info from filename (only if Twitter elements exist)
    if (twitterLinkContainer && twitterLink) {
        const tweetInfo = extractTweetInfoFromFilename(filename);
        if (tweetInfo.username && tweetInfo.tweetId) {
            const twitterUrl = `https://twitter.com/${tweetInfo.username}/status/${tweetInfo.tweetId}`;
            twitterLink.href = twitterUrl;
            twitterLinkContainer.style.display = 'block';
        } else {
            twitterLinkContainer.style.display = 'none';
        }
    }

    // Update navigation buttons and counter
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const imageCounter = document.getElementById('imageCounter');

    if (prevButton) prevButton.disabled = index === 0;
    if (nextButton) nextButton.disabled = index === allImagePaths.length - 1;
    if (imageCounter) imageCounter.textContent = `${index + 1} / ${allImagePaths.length}`;

    modal.style.display = 'flex'; // Use flex to center modal content
    document.body.classList.add('modal-open');
}

function extractTweetInfoFromFilename(filename) {
    try {
        // Remove file extension
        let baseName = filename.replace(/\.(webp|jpg|jpeg|png|gif)$/i, '');
        // Remove -lossy suffix if present
        baseName = baseName.replace('-lossy', '');

        // Split by dash and extract first two parts
        const parts = baseName.split('-');
        if (parts.length >= 2) {
            const username = parts[0];
            const tweetId = parts[1];
            // Verify tweet_id is numeric
            if (/^\d+$/.test(tweetId)) {
                return { username, tweetId };
            }
        }
    } catch (e) {
        // Parsing failed - return null values to indicate no tweet info available
    }
    return { username: null, tweetId: null };
}

function previousImage() {
    if (currentImageIndex > 0) {
        currentImageIndex--;
        openImage(currentImageIndex);
    }
}

function nextImage() {
    if (currentImageIndex < allImagePaths.length - 1) {
        currentImageIndex++;
        openImage(currentImageIndex);
    }
}

function downloadImage() {
    const currentImagePath = allImagePaths[currentImageIndex];
    if (currentImagePath) {
        const link = document.createElement('a');
        link.href = currentImagePath;
        link.download = currentImagePath.split('/').pop();
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

function closeModal() {
    const modal = document.getElementById('fullscreenModal');
    if (modal.style.display === 'flex') {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
    }
}

// Update the existing window.onclick handler to prevent modal closure when clicking inside the image
window.addEventListener('click', function(event) {
    const modal = document.getElementById('fullscreenModal');
    if (event.target === modal) {
        closeModal();
    }
});

// Keyboard navigation
document.addEventListener('keydown', function(event) {
    const modal = document.getElementById('fullscreenModal');
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

// Make functions globally accessible for backward compatibility
window.closeModal = closeModal;
window.previousImage = previousImage;
window.nextImage = nextImage;
window.downloadImage = downloadImage;
window.openImage = openImage;
window.initializeGallery = initializeGallery;