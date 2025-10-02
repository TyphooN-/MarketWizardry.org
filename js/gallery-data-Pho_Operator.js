// Gallery data for Pho_Operator
// CSP-compliant gallery initialization
document.addEventListener('DOMContentLoaded', function() {
    const imagePaths = ['./Pho_Operator/webp/Pho_Operator-1891217809-LAST_20_HOURS_TO_MINT_video1-lossy.webp','./Pho_Operator/webp/Pho_Operator-1855440478-Here_s_a_little_piece_of_history_for_y_all___video3-lossy.webp','./Pho_Operator/webp/Pho_Operator-1886471280-ARCANA_video1-lossy.webp','./Pho_Operator/webp/Pho_Operator-1886973804-ARCANA_video2-lossy.webp','./Pho_Operator/webp/Pho_Operator-1889106520-The_Hermit_video1-lossy.webp','./Pho_Operator/webp/Pho_Operator-1871399691-All_I_want_for_Christmas_is_some_free_time_to_create_video2-lossy.webp','./Pho_Operator/webp/Pho_Operator-1859073789956333570-there_must_be_a_huge_unchecked_vulnerability_in_the_source_code_of_reality_for_this_to_have_happened_video2-lossy.webp','./Pho_Operator/webp/Pho_Operator-1889521407-_i___m___s_o___h_y_p_e_______video2-lossy.webp','./Pho_Operator/webp/Pho_Operator-1886972071-Already_56_editions_of_Arcana_pieces_minted__video1-lossy.webp','./Pho_Operator/webp/Pho_Operator-1890441833051808076-Only_three_days_left_to_mint_editions_of_my_Arcana_set_on_http___create.party.app_by_video1-lossy.webp'];
    const imageData = [null,null,null,null,null,null,{'twitterUrl': 'https://twitter.com/Pho_Operator/status/1859073789956333570'},null,null,{'twitterUrl': 'https://twitter.com/Pho_Operator/status/1890441833051808076'}];
    if (window.initializeGallery) {
        window.initializeGallery(imagePaths, imageData);
    }
});