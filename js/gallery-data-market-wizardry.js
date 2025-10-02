// Gallery data for market-wizardry.html
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.image-container img, .grid-container img');
    const imagePaths = Array.from(images).map(img => img.src);
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths);
    }
});
