// Gallery data for 0xDither
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./0xDither/webp/0xDither-1929565152-_Lodge__by_video2-lossy.webp','./0xDither/webp/0xDither-1929565152086557028-_Lodge__by_video1-lossy.webp','./0xDither/webp/0xDither-1928184176475292040-I_have_just_collected__Covenant__by_video1-lossy.webp','./0xDither/webp/0xDither-1930286151-There_are_4_more_pieces_available_in_video2-lossy.webp','./0xDither/webp/0xDither-1930286151367037340-There_are_4_more_pieces_available_in_video1-lossy.webp','./0xDither/webp/0xDither-1919416735901389057-_The_Tube__by-video3-lossy.webp'];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths);
    }
});