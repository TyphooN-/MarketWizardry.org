/**
 * Nuclear Explosion Effect for Calculator Remove Buttons
 * Triggers when nuke.webp button is clicked
 * Localized to the button's parent container
 */

function triggerNuclearExplosion(button) {
    // Find the parent container (table cell or container div)
    const parent = button.closest('td') || button.closest('.input-group') || button.parentElement;

    // Make sure parent has position context
    const originalPosition = parent.style.position;
    if (!originalPosition || originalPosition === 'static') {
        parent.style.position = 'relative';
    }

    // Store original overflow
    const originalOverflow = parent.style.overflow;
    parent.style.overflow = 'visible';

    // Create flash overlay
    const flash = document.createElement('div');
    flash.className = 'nuke-flash';
    parent.appendChild(flash);

    // Create mushroom cloud
    const mushroom = document.createElement('div');
    mushroom.className = 'nuke-mushroom';

    const stem = document.createElement('div');
    stem.className = 'nuke-stem';

    const cap = document.createElement('div');
    cap.className = 'nuke-cap';

    mushroom.appendChild(stem);
    mushroom.appendChild(cap);
    parent.appendChild(mushroom);

    // Cleanup after animation
    setTimeout(() => {
        flash.remove();
        mushroom.remove();
        // Restore original styles
        if (!originalPosition || originalPosition === 'static') {
            parent.style.position = '';
        }
        parent.style.overflow = originalOverflow;
    }, 1500);
}

// Attach to remove buttons
document.addEventListener('DOMContentLoaded', function() {
    // Use event delegation for dynamically added buttons
    document.addEventListener('click', function(e) {
        const button = e.target.closest('.remove-btn, .position-remove-btn');
        if (button) {
            // Trigger explosion localized to the button's container
            triggerNuclearExplosion(button);
        }
    });
});
