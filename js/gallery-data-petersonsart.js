// Image paths for petersonsart gallery
const galleryImagePaths = [
    "./petersonsart/webp/petersonsart-1929713395-STATIC___ENCODING_video1-lossy.webp",    "./petersonsart/webp/petersonsart-1929283987-SUBSTANCE___CARRIER_1_video1-lossy.webp",    "./petersonsart/webp/petersonsart-1927765226-Collected__Faint__by_video1-lossy.webp"
];

// Initialize gallery when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeGallery(galleryImagePaths);
});