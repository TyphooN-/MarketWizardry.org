// Gallery data for HughesMichi
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./HughesMichi/webp/HughesMichi-1912972811-A__bzzz_in_fly_video1-lossy.webp','./HughesMichi/webp/HughesMichi-1915134739-City_of_Children_video1-lossy.webp','./HughesMichi/webp/HughesMichi-1915128391-Seamount_video1-lossy.webp'];
    const imageData = [null,null,null];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});