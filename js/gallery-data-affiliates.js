// Gallery data for affiliates.html
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.affiliate-content img');
    const imagePaths = Array.from(images).map(img => img.src);
    if (window.initializeGallery) {
        // Pass true to skip dynamic loading since images are already in DOM
        window.initializeGallery(imagePaths, true);
    }
});
