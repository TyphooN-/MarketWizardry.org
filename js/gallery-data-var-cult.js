// Gallery data for var-cult.html
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.image-container img, .inline-images img');
    const imagePaths = Array.from(images).map(img => img.src);
    if (window.initializeGallery) {
        // Pass true to skip dynamic loading since images are already in DOM
        window.initializeGallery(imagePaths, true);
    }
});
