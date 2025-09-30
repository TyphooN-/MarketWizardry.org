/**
 * Nuclear Explosion Effect for Calculator Remove Buttons
 * Triggers when nuke.webp button is clicked
 */

function triggerNuclearExplosion(clickX, clickY) {
    // Create flash overlay
    const flash = document.createElement('div');
    flash.className = 'nuke-flash';
    document.body.appendChild(flash);

    // Create mushroom cloud
    const mushroom = document.createElement('div');
    mushroom.className = 'nuke-mushroom';

    // Position mushroom at click location
    mushroom.style.left = clickX + 'px';
    mushroom.style.transform = 'translateX(-50%)';

    const stem = document.createElement('div');
    stem.className = 'nuke-stem';

    const cap = document.createElement('div');
    cap.className = 'nuke-cap';

    mushroom.appendChild(stem);
    mushroom.appendChild(cap);
    document.body.appendChild(mushroom);

    // Cleanup after animation
    setTimeout(() => {
        flash.remove();
        mushroom.remove();
    }, 2000);
}

// Attach to remove buttons
document.addEventListener('DOMContentLoaded', function() {
    // Use event delegation for dynamically added buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-btn') ||
            e.target.classList.contains('position-remove-btn')) {

            // Get click coordinates
            const rect = e.target.getBoundingClientRect();
            const clickX = rect.left + rect.width / 2;

            // Trigger explosion
            triggerNuclearExplosion(clickX, 0);
        }
    });
});
