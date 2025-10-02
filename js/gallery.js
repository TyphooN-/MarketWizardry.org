// Gallery functionality for NFT galleries
// Event delegation for data-action attributes
document.addEventListener('click', function(e) {
    const action = e.target.getAttribute('data-action');
    if (action) {
        switch(action) {
            case 'navigate':
                const url = e.target.getAttribute('data-url');
                if (url) window.location.href = url;
                break;
            case 'close-modal':
                closeModal();
                break;
            case 'previous-image':
                previousImage();
                break;
            case 'next-image':
                nextImage();
                break;
            case 'download-image':
                downloadImage();
                break;
        }
    }
});

let currentImageIndex = 0;
let allImagePaths = []; // Will be set by each gallery file

const imagesPerLoad = 50; // Increased number of images to load per scroll
const scrollThreshold = 1000; // Load more images when 1000px from bottom

function initializeGallery(imagePaths, skipDynamicLoading = false) {
    allImagePaths = imagePaths;
    console.log("All Image Paths:", allImagePaths);

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
    if (document.body.offsetHeight < window.innerHeight) {
        loadMoreImages();
    }

    // Scroll event for lazy loading
    window.addEventListener('scroll', () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - scrollThreshold) {
            loadMoreImages();
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
        img.style.cursor = 'pointer'; // Make it clear images are clickable
    });
    console.log(`Set up click handlers for ${images.length} static images`);
}

function loadImage(path, index) {
    const imageGrid = document.getElementById('imageGrid');
    const imgContainer = document.createElement('div');
    imgContainer.className = 'image-container';
    const img = document.createElement('img');
    img.className = 'thumbnail';
    img.src = path;
    img.onerror = function() { console.error("Error loading image:", path); };
    img.addEventListener('load', function() { console.log("Image loaded:", path); });
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
    currentImageIndex = index;
    const modalImg = document.querySelector('.full-image');
    const modal = document.getElementById('fullscreenModal');
    const modalFilename = document.getElementById('modalFilename');
    const twitterLinkContainer = document.getElementById('twitterLinkContainer');
    const twitterLink = document.getElementById('twitterLink');

    const imagePath = allImagePaths[index];
    const filename = imagePath.split('/').pop().replace(/'/g, ''); // Extract filename and clean quotes

    modalImg.src = imagePath;
    modalFilename.textContent = filename;

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

    prevButton.disabled = index === 0;
    nextButton.disabled = index === allImagePaths.length - 1;
    imageCounter.textContent = `${index + 1} / ${allImagePaths.length}`;

    modal.style.display = 'flex'; // Use flex to center modal content
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
        console.log('Could not extract tweet info from filename:', filename);
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