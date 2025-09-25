/**
 * NFT Gallery JavaScript
 * CSP-compliant gallery functionality
 * Handles image gallery display, lazy loading, and modal interactions
 */

let currentImageIndex = 0;
let allImagePaths = [];
let currentImageData = [];

const imagesPerLoad = 20;
const scrollThreshold = 1000;

function initializeGallery(imagePaths, imageData = []) {
    allImagePaths = imagePaths;
    currentImageData = imageData;
    currentImageIndex = 0;

    console.log(`Gallery initialized with ${allImagePaths.length} images`);

    // Load initial images
    loadMoreImages();

    // Set up scroll listener for lazy loading
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        if (documentHeight - scrollTop - windowHeight < scrollThreshold) {
            loadMoreImages();
        }
    });

    // Set up modal event listeners
    setupModalEventListeners();
}

function loadImage(path, index, data = null) {
    const imageGrid = document.getElementById('imageGrid');
    if (!imageGrid) return;

    const imgContainer = document.createElement('div');
    imgContainer.className = 'image-container';

    const img = document.createElement('img');
    img.className = 'thumbnail';
    img.src = path;
    img.alt = data ? data.description || 'NFT artwork' : 'NFT artwork';
    img.loading = 'lazy';

    img.onerror = function() {
        console.error("Error loading image:", path);
        imgContainer.style.display = 'none';
    };

    img.onload = function() {
        console.log("Image loaded:", path);
    };

    // CSP-compliant event listener
    img.addEventListener('click', function() {
        openImage(index);
    });

    imgContainer.appendChild(img);

    // Add metadata if available
    if (data) {
        const metadata = document.createElement('div');
        metadata.className = 'image-metadata';

        if (data.title) {
            const title = document.createElement('div');
            title.className = 'image-title';
            title.textContent = data.title;
            metadata.appendChild(title);
        }

        if (data.description) {
            const desc = document.createElement('div');
            desc.className = 'image-description';
            desc.textContent = data.description;
            metadata.appendChild(desc);
        }

        imgContainer.appendChild(metadata);
    }

    imageGrid.appendChild(imgContainer);
}

function loadMoreImages() {
    if (currentImageIndex >= allImagePaths.length) {
        console.log("No more images to load");
        return;
    }

    const startIndex = currentImageIndex;
    const endIndex = Math.min(startIndex + imagesPerLoad, allImagePaths.length);

    for (let i = startIndex; i < endIndex; i++) {
        const imageData = currentImageData[i] || null;
        loadImage(allImagePaths[i], i, imageData);
    }

    currentImageIndex = endIndex;
    console.log(`Loaded images up to index: ${currentImageIndex}`);
}

function openImage(index) {
    if (index < 0 || index >= allImagePaths.length) return;

    const modal = document.getElementById('fullscreenModal');
    const fullImage = modal.querySelector('.full-image');
    const filenameDisplay = document.getElementById('modalFilename');

    if (!modal || !fullImage) return;

    const imagePath = allImagePaths[index];
    const filename = imagePath.split('/').pop();
    const imageData = currentImageData[index];

    fullImage.src = imagePath;

    if (filenameDisplay) {
        filenameDisplay.textContent = imageData?.title || filename;
    }

    modal.style.display = 'flex';
    document.body.classList.add('modal-open');

    // Store current index for navigation
    modal.dataset.currentIndex = index;

    console.log("Opening image:", imagePath);
}

function closeModal() {
    const modal = document.getElementById('fullscreenModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
        delete modal.dataset.currentIndex;
        console.log("Modal closed");
    }
}

function navigateImage(direction) {
    const modal = document.getElementById('fullscreenModal');
    if (!modal || modal.style.display !== 'flex') return;

    const currentIndex = parseInt(modal.dataset.currentIndex || '0');
    let newIndex = currentIndex;

    if (direction === 'prev' && currentIndex > 0) {
        newIndex = currentIndex - 1;
    } else if (direction === 'next' && currentIndex < allImagePaths.length - 1) {
        newIndex = currentIndex + 1;
    }

    if (newIndex !== currentIndex) {
        openImage(newIndex);
    }
}

function setupModalEventListeners() {
    const modal = document.getElementById('fullscreenModal');
    const modalContent = modal?.querySelector('.modal-content');

    if (!modal) return;

    // Close modal when clicking outside content
    modal.addEventListener('click', closeModal);

    // Prevent closing when clicking inside modal content
    if (modalContent) {
        modalContent.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(event) {
        if (modal.style.display === 'flex') {
            switch (event.key) {
                case 'Escape':
                    closeModal();
                    break;
                case 'ArrowLeft':
                    navigateImage('prev');
                    event.preventDefault();
                    break;
                case 'ArrowRight':
                    navigateImage('next');
                    event.preventDefault();
                    break;
            }
        }
    });
}

// Make functions globally available
window.initializeGallery = initializeGallery;
window.closeModal = closeModal;