// Gallery data for petersonsart
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./petersonsart/webp/petersonsart-1929713395-STATIC___ENCODING_video1-lossy.webp','./petersonsart/webp/petersonsart-1929283987-SUBSTANCE___CARRIER_1_video1-lossy.webp','./petersonsart/webp/petersonsart-1927765226-Collected__Faint__by_video1-lossy.webp'];
    const imageData = [null,null,null];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});