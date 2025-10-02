// Image Modal functionality for expanding and navigating images
(function() {
    let currentImageIndex = 0;
    let imagesList = [];
    let modal = null;

    function createModal() {
        // Create modal HTML structure
        const modalHTML = `
            <div id="image-modal" class="image-modal" style="display: none;">
                <div class="image-modal-content">
                    <div class="image-modal-header">
                        <div class="image-modal-buttons">
                            <button class="image-modal-nav" id="prev-image" title="Previous (←)">← Previous</button>
                            <span class="image-modal-counter" id="image-counter">1 of 1</span>
                            <button class="image-modal-nav" id="next-image" title="Next (→)">Next →</button>
                            <a class="image-modal-download" id="download-image" href="#" download title="Download Image">⬇ Download</a>
                            <button class="image-modal-close" id="close-modal" title="Close (Esc)">✕</button>
                        </div>
                        <div class="crt-divider"></div>
                    </div>
                    <div class="image-modal-body">
                        <img id="modal-image" src="" alt="">
                    </div>
                </div>
            </div>
        `;

        // Insert modal into body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        modal = document.getElementById('image-modal');

        // Add event listeners
        document.getElementById('close-modal').addEventListener('click', closeModal);
        document.getElementById('prev-image').addEventListener('click', previousImage);
        document.getElementById('next-image').addEventListener('click', nextImage);

        // Close modal when clicking outside image
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });

        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (modal.style.display === 'block') {
                switch(e.key) {
                    case 'ArrowLeft':
                        previousImage();
                        e.preventDefault();
                        break;
                    case 'ArrowRight':
                        nextImage();
                        e.preventDefault();
                        break;
                    case 'Escape':
                        closeModal();
                        e.preventDefault();
                        break;
                }
            }
        });
    }

    function initializeImages() {
        // Find all images that should be clickable (not in iframes, only actual img tags)
        const images = document.querySelectorAll('.image-container img, .grid-container img');

        imagesList = Array.from(images).map(img => ({
            src: img.src,
            alt: img.alt || 'Image'
        }));

        // Add click handlers to all images
        images.forEach((img, index) => {
            img.style.cursor = 'pointer';
            img.addEventListener('click', function() {
                openModal(index);
            });
        });
    }

    function openModal(index) {
        currentImageIndex = index;
        const image = imagesList[currentImageIndex];

        document.getElementById('modal-image').src = image.src;
        document.getElementById('modal-image').alt = image.alt;

        // Set download link
        const downloadLink = document.getElementById('download-image');
        downloadLink.href = image.src;
        const filename = image.src.split('/').pop();
        downloadLink.download = filename;

        updateCounter();
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    function closeModal() {
        modal.style.display = 'none';
        document.body.style.overflow = ''; // Restore scrolling
    }

    function previousImage() {
        if (currentImageIndex > 0) {
            currentImageIndex--;
            openModal(currentImageIndex);
        }
    }

    function nextImage() {
        if (currentImageIndex < imagesList.length - 1) {
            currentImageIndex++;
            openModal(currentImageIndex);
        }
    }

    function updateCounter() {
        document.getElementById('image-counter').textContent =
            `${currentImageIndex + 1} of ${imagesList.length}`;

        // Disable/enable navigation buttons
        document.getElementById('prev-image').disabled = currentImageIndex === 0;
        document.getElementById('next-image').disabled = currentImageIndex === imagesList.length - 1;
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            createModal();
            initializeImages();
        });
    } else {
        createModal();
        initializeImages();
    }
})();
