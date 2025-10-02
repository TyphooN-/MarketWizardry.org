// Gallery data for godlikepx
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./godlikepx/webp/godlikepx-1908539452-Journal-video1-lossy.webp','./godlikepx/webp/godlikepx-1937479899394277816-1bit_Pixel_art_I_made_a_while_back_for_http___guillotine.agency_video3-lossy.webp','./godlikepx/webp/godlikepx-1939010251472212420-_The_Collector__video3-lossy.webp','./godlikepx/webp/godlikepx-1930298508-Frozen_hour_video1-lossy.webp','./godlikepx/webp/godlikepx-1902670263-Advertise_your_account_with_one_animation_video2-lossy.webp'];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths);
    }
});