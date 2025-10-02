// Gallery data for vad_jpg
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./vad_jpg/webp/vad_jpg-1919379851-losing_it_video2-lossy.webp','./vad_jpg/webp/vad_jpg-1934755347186724978-what_am_i_video4-lossy.webp','./vad_jpg/webp/vad_jpg-1925290142-that_feeling_video1-lossy.webp','./vad_jpg/webp/vad_jpg-1928486448-captive_within_video3-lossy.webp','./vad_jpg/webp/vad_jpg-1925932974-amor_fati_video1-lossy.webp','./vad_jpg/webp/vad_jpg-1938399611246301686-side_quest_video4-lossy.webp','./vad_jpg/webp/vad_jpg-1927785555-ominous_video3-lossy.webp','./vad_jpg/webp/vad_jpg-1919379851-losing_it_video3-lossy.webp'];
    const imageData = [null,{'twitterUrl': 'https://twitter.com/vad_jpg/status/1934755347186724978'},null,null,null,{'twitterUrl': 'https://twitter.com/vad_jpg/status/1938399611246301686'},null,null];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});