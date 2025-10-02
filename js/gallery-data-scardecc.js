// Gallery data for scardecc
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./scardecc/webp/scardecc-1838207264-Looking_for_new_art__I_ll_help_you_here_are_5_unsold_pieces_on_video4-lossy.webp'];
    const imageData = [null];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});