// Gallery data for Zoen_calega
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./Zoen_calega/webp/Zoen_calega-1931767787950833782-BOM_DIAAA_video2-lossy.webp','./Zoen_calega/webp/Zoen_calega-1941347048198111336-src___video2-lossy.webp','./Zoen_calega/webp/Zoen_calega-1934339367734227069-C_R_A_S_H_video2-lossy.webp'];
    const imageData = [{'twitterUrl': 'https://twitter.com/Zoen_calega/status/1931767787950833782'},{'twitterUrl': 'https://twitter.com/Zoen_calega/status/1941347048198111336'},{'twitterUrl': 'https://twitter.com/Zoen_calega/status/1934339367734227069'}];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});