// Gallery data for killeracid
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./killeracid/webp/killeracid-1939051986483322939-Posters_for_video4-lossy.webp','./killeracid/webp/killeracid-1940881222101811428-Hell_Yes__I_m_Stressed_video4-lossy.webp','./killeracid/webp/killeracid-1901684491-Happy_St_Patrick_s_Day_video3-lossy.webp','./killeracid/webp/killeracid-1929934639-Glizzy_flip_video1-lossy.webp','./killeracid/webp/killeracid-1905032576-surfin__video1-lossy.webp'];
    const imageData = [{'twitterUrl': 'https://twitter.com/killeracid/status/1939051986483322939'},{'twitterUrl': 'https://twitter.com/killeracid/status/1940881222101811428'},null,null,null];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});