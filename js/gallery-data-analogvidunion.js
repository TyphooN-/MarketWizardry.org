// Gallery data for analogvidunion
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./analogvidunion/webp/analogvidunion-1859940461-Artist__video1-1-lossy.webp','./analogvidunion/webp/analogvidunion-1923016170-INSERT_COIN_video3-lossy.webp','./analogvidunion/webp/analogvidunion-1923752617-Artist__video3-1-lossy.webp','./analogvidunion/webp/analogvidunion-1923016170-INSERT_COIN_video2-lossy.webp','./analogvidunion/webp/analogvidunion-1922120369-INSERT_COIN_video1-lossy.webp','./analogvidunion/webp/analogvidunion-1913806077-TV_PARTY_by_video1-lossy.webp'];
    const imageData = [null,null,null,null,null,null];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});