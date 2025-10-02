// Gallery data for s0mfay
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./s0mfay/webp/s0mfay-1932977495193575585-My_cozy_little_foundry_video2-lossy.webp','./s0mfay/webp/s0mfay-1831693772-Atomic_Steppe_video1-lossy.webp','./s0mfay/webp/s0mfay-1883580873003384862-Fermata_Positronics_now_bears_a_logo____video3-lossy.webp','./s0mfay/webp/s0mfay-1840881222836252736-A_new_Firefly_is_borne_video1-lossy.webp','./s0mfay/webp/s0mfay-1864788216189964598-I_made_Jester_Vision_for_all_the_kitty_enthusiasts_out_there__meow__thank_you_to_video2-lossy.webp','./s0mfay/webp/s0mfay-1937876868604060014-Archimedes__Window_video4-lossy.webp','./s0mfay/webp/s0mfay-1914313301468553719-I_am_delighted_to_share_Fermata_Positronics__Series_II_devices_The_Pleiades__video3-lossy.webp'];
    const imageData = [{'twitterUrl': 'https://twitter.com/s0mfay/status/1932977495193575585'},null,{'twitterUrl': 'https://twitter.com/s0mfay/status/1883580873003384862'},{'twitterUrl': 'https://twitter.com/s0mfay/status/1840881222836252736'},{'twitterUrl': 'https://twitter.com/s0mfay/status/1864788216189964598'},{'twitterUrl': 'https://twitter.com/s0mfay/status/1937876868604060014'},{'twitterUrl': 'https://twitter.com/s0mfay/status/1914313301468553719'}];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});