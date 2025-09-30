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

    // Create barrel explosion flash
    const flash = document.createElement('div');
    flash.className = 'nuke-flash';
    parent.appendChild(flash);

    // Create debris particles
    const debrisContainer = document.createElement('div');
    debrisContainer.className = 'nuke-debris';

    // Create 8 debris particles flying in different directions
    const debrisColors = ['#ff8800', '#ff4400', '#ffaa00', '#ff6600'];
    for (let i = 1; i <= 8; i++) {
        const particle = document.createElement('div');
        particle.className = 'debris-particle';
        particle.style.background = debrisColors[Math.floor(Math.random() * debrisColors.length)];
        particle.style.animation = `debris-fly-${i} 0.5s steps(3) forwards`;
        particle.style.animationDelay = '0.1s'; // Start after initial flash
        debrisContainer.appendChild(particle);
    }

    parent.appendChild(debrisContainer);

    // Cleanup after animation
    setTimeout(() => {
        flash.remove();
        debrisContainer.remove();
        // Restore original styles
        if (!originalPosition || originalPosition === 'static') {
            parent.style.position = '';
        }
        parent.style.overflow = originalOverflow;
    }, 1000);
}

// Attach to remove buttons - let calculator.js handle removal, we just add the visual effect
document.addEventListener('DOMContentLoaded', function() {
    // Use event delegation for dynamically added buttons
    // Listen for click in capture phase to run before calculator.js
    document.addEventListener('click', function(e) {
        const button = e.target.closest('.remove-btn, .position-remove-btn');
        if (button) {
            // Trigger explosion localized to the button's container
            // Don't prevent default - let calculator.js handle the actual removal
            triggerNuclearExplosion(button);
        }
    }, true); // Capture phase to run before calculator.js
});
