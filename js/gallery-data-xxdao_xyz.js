// Gallery data for xxdao_xyz
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./xxdao_xyz/webp/xxdao_xyz-1935703026905301184-Thursday_Terraforms_video3-lossy.webp','./xxdao_xyz/webp/xxdao_xyz-1924903703-love_these_cute_lil_podGANs_video1-lossy.webp','./xxdao_xyz/webp/xxdao_xyz-1942624218107240490-Terraforms_by_video3-lossy.webp','./xxdao_xyz/webp/xxdao_xyz-1927052863-sorry_I_m_late_I_was_getting_my_beauty_sleep_video2-lossy.webp'];
    const imageData = [{'twitterUrl': 'https://twitter.com/xxdao_xyz/status/1935703026905301184'},null,{'twitterUrl': 'https://twitter.com/xxdao_xyz/status/1942624218107240490'},null];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});