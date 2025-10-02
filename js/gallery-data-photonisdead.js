// Gallery data for photonisdead
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./photonisdead/webp/photonisdead-1922688991-Lost_All_Hope_Or_Oblivion_video2-lossy.webp','./photonisdead/webp/photonisdead-1912538200-someone_got_my_art_tattooed_on_them_video2-lossy.webp','./photonisdead/webp/photonisdead-1915082635-.1_reserve_video1-lossy.webp','./photonisdead/webp/photonisdead-1924859042-Ignorance_Is_Bliss_Or_Face_The_Monster_video1-lossy.webp','./photonisdead/webp/photonisdead-1924859042-Ignorance_Is_Bliss_Or_Face_The_Monster_video3-lossy.webp'];
    const imageData = [null,null,null,null,null];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});