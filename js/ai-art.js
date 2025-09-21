// Event delegation for data-action attributes
document.addEventListener('click', function(e) {
    const action = e.target.getAttribute('data-action');
    if (action) {
        switch(action) {
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

const allImagePaths = [
    "/ai-art/00001.webp",
    "/ai-art/00002.webp",
    "/ai-art/00003.webp",
    "/ai-art/00004.webp",
    "/ai-art/00005.webp",
    "/ai-art/00006.webp",
    "/ai-art/00007.webp",
    "/ai-art/00008.webp",
    "/ai-art/00009.webp",
    "/ai-art/00010.webp",
    "/ai-art/00011.webp",
    "/ai-art/00012.webp",
    "/ai-art/00013.webp",
    "/ai-art/00014.webp",
    "/ai-art/00015.webp",
    "/ai-art/00016.webp",
    "/ai-art/00017.webp",
    "/ai-art/00018.webp",
    "/ai-art/00019.webp",
    "/ai-art/00020.webp",
    "/ai-art/00021.webp",
    "/ai-art/00022.webp",
    "/ai-art/00023.webp",
    "/ai-art/00024.webp",
    "/ai-art/00025.webp",
    "/ai-art/00026.webp",
    "/ai-art/00027.webp",
    "/ai-art/00028.webp",
    "/ai-art/00029.webp",
    "/ai-art/00030.webp",
    "/ai-art/00031.webp",
    "/ai-art/00032.webp",
    "/ai-art/00033.webp",
    "/ai-art/00034.webp",
    "/ai-art/00035.webp",
    "/ai-art/00036.webp",
    "/ai-art/00037.webp",
    "/ai-art/00038.webp",
    "/ai-art/00039.webp",
    "/ai-art/00040.webp",
    "/ai-art/00041.webp",
    "/ai-art/00042.webp",
    "/ai-art/00043.webp",
    "/ai-art/00044.webp",
    "/ai-art/00045.webp",
    "/ai-art/00046.webp",
    "/ai-art/00047.webp",
    "/ai-art/00048.webp",
    "/ai-art/00049.webp",
    "/ai-art/00050.webp",
    "/ai-art/00051.webp",
    "/ai-art/00052.webp",
    "/ai-art/00053.webp",
    "/ai-art/00054.webp",
    "/ai-art/00055.webp",
    "/ai-art/00056.webp",
    "/ai-art/00057.webp",
    "/ai-art/00058.webp",
    "/ai-art/00059.webp",
    "/ai-art/00060.webp",
    "/ai-art/00061.webp",
    "/ai-art/00062.webp",
    "/ai-art/00063.webp",
    "/ai-art/00064.webp",
    "/ai-art/00065.webp",
    "/ai-art/00066.webp",
    "/ai-art/00067.webp",
    "/ai-art/00068.webp",
    "/ai-art/00069.webp",
    "/ai-art/00070.webp",
    "/ai-art/00071.webp",
    "/ai-art/00072.webp",
    "/ai-art/00073.webp",
    "/ai-art/00074.webp",
    "/ai-art/00075.webp",
    "/ai-art/00076.webp",
    "/ai-art/00077.webp",
    "/ai-art/00078.webp",
    "/ai-art/00079.webp",
    "/ai-art/00080.webp",
    "/ai-art/00081.webp",
    "/ai-art/00082.webp",
    "/ai-art/00083.webp",
    "/ai-art/00084.webp",
    "/ai-art/00085.webp"
];
console.log("Image paths loaded:", allImagePaths.length);

let currentImageIndex = 0;

function openImage(index) {
    currentImageIndex = index;
    const modalImg = document.querySelector('.full-image');
    const modal = document.getElementById('fullscreenModal');
    const modalFilename = document.getElementById('modalFilename');

    modalImg.src = allImagePaths[index];
    modalFilename.textContent = allImagePaths[index].split('/').pop().replace(/'/g, '');

    // Update navigation buttons and counter
    updateNavigationButtons();

    modal.style.display = 'flex';
}

function updateNavigationButtons() {
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');
    const imageCounter = document.getElementById('imageCounter');

    if (prevButton && nextButton && imageCounter) {
        prevButton.disabled = currentImageIndex <= 0;
        nextButton.disabled = currentImageIndex >= allImagePaths.length - 1;
        imageCounter.textContent = `${currentImageIndex + 1} / ${allImagePaths.length}`;
    }
}

function previousImage() {
    if (currentImageIndex > 0) {
        openImage(currentImageIndex - 1);
    }
}

function nextImage() {
    if (currentImageIndex < allImagePaths.length - 1) {
        openImage(currentImageIndex + 1);
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
    modal.style.display = 'none';
}

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
                closeModal();
                break;
        }
    }
});

// Click outside modal to close
window.addEventListener('click', function(event) {
    const modal = document.getElementById('fullscreenModal');
    if (event.target === modal) {
        closeModal();
    }
});

// Populate image grid on load
document.addEventListener('DOMContentLoaded', () => {
    const imageGrid = document.getElementById('imageGrid');
    allImagePaths.forEach((path, index) => {
        const imgContainer = document.createElement('div');
        imgContainer.className = 'image-container';

        const img = document.createElement('img');
        img.className = 'thumbnail';
        img.src = path;
        img.alt = `AI Art ${index + 1}`;
        img.loading = 'lazy';
        img.addEventListener('click', () => openImage(index));

        imgContainer.appendChild(img);
        imageGrid.appendChild(imgContainer);
    });
});

// Make functions globally accessible for backward compatibility
window.openImage = openImage;
window.closeModal = closeModal;
window.previousImage = previousImage;
window.nextImage = nextImage;
window.downloadImage = downloadImage;