// Gallery data for neural_divine
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./neural_divine/webp/neural_divine-1930050708-_Dinner_Time__video4-lossy.webp','./neural_divine/webp/neural_divine-1929556979-You_transported_me_in_your_universe_video2-lossy.webp','./neural_divine/webp/neural_divine-1941161425604595719-Sitting_on_the_couch_video4-lossy.webp','./neural_divine/webp/neural_divine-1930050708-_Dinner_Time__video2-lossy.webp'];
    const imageData = [null,null,{'twitterUrl': 'https://twitter.com/neural_divine/status/1941161425604595719'},null];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});