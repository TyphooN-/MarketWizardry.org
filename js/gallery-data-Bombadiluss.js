// Gallery data for Bombadiluss
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./Bombadiluss/webp/Bombadiluss-1937803823877357930-GM__video4-lossy.webp','./Bombadiluss/webp/Bombadiluss-1923711684-GMeme__video1-lossy.webp','./Bombadiluss/webp/Bombadiluss-1924037728-GM__video3-lossy.webp','./Bombadiluss/webp/Bombadiluss-1921487408-GM__video1-1-lossy.webp','./Bombadiluss/webp/Bombadiluss-1915463706-Neural_Arcade__8-Bit_Dreams_video1-lossy.webp'];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths);
    }
});