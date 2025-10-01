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

    // Create barrel explosion graphic
    const barrelExplosion = document.createElement('div');
    barrelExplosion.className = 'barrel-explosion';
    barrelExplosion.innerHTML = `
        <img src="/img/barrel-explosion.svg" alt="explosion" class="barrel-explosion-img">
    `;
    parent.appendChild(barrelExplosion);

    // Create barrel explosion flash
    const flash = document.createElement('div');
    flash.className = 'nuke-flash barrel-flash';
    parent.appendChild(flash);

    // Create debris particles
    const debrisContainer = document.createElement('div');
    debrisContainer.className = 'nuke-debris';

    // Create 12 debris particles flying in different directions - Barrel chunks
    const debrisColors = ['#555555', '#666666', '#888888', '#cc0000', '#ff6600', '#ff8800'];
    const debrisChars = ['▪', '▫', '■', '□', '●', '○'];
    for (let i = 1; i <= 12; i++) {
        const particle = document.createElement('div');
        particle.className = 'debris-particle';
        const color = debrisColors[Math.floor(Math.random() * debrisColors.length)];
        const char = debrisChars[Math.floor(Math.random() * debrisChars.length)];
        particle.textContent = char;
        particle.style.color = color;
        particle.style.textShadow = `0 0 2px ${color}`;
        particle.style.fontSize = Math.random() > 0.5 ? '12px' : '8px';
        particle.style.animation = `debris-fly-${(i % 8) + 1} ${0.3 + Math.random() * 0.2}s steps(${Math.floor(3 + Math.random() * 3)}) forwards`;
        particle.style.animationDelay = '0.1s';
        debrisContainer.appendChild(particle);
    }

    parent.appendChild(debrisContainer);

    // Create smoke puffs
    const smokeContainer = document.createElement('div');
    smokeContainer.className = 'barrel-smoke';
    for (let i = 0; i < 3; i++) {
        const smoke = document.createElement('div');
        smoke.className = 'smoke-puff';
        smoke.style.left = `${20 + Math.random() * 20}px`;
        smoke.style.animationDelay = `${i * 0.1}s`;
        smokeContainer.appendChild(smoke);
    }
    parent.appendChild(smokeContainer);

    // Cleanup after animation
    setTimeout(() => {
        barrelExplosion.remove();
        flash.remove();
        debrisContainer.remove();
        smokeContainer.remove();
        // Restore original styles
        if (!originalPosition || originalPosition === 'static') {
            parent.style.position = '';
        }
        parent.style.overflow = originalOverflow;
    }, 1200);
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
