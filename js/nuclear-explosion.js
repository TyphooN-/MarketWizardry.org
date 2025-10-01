/**
 * Nuclear Explosion Effect for Calculator Remove Buttons
 * Triggers when nuke.webp button is clicked
 * Localized to the button's parent container
 */

// Helper function to create pixel explosion frames
function createExplosionFrame(lines, baseColor) {
    const frame = document.createElement('div');
    frame.className = 'explosion-frame';

    lines.forEach((line, rowIndex) => {
        const row = document.createElement('div');
        row.className = 'pixel-row';

        // Convert each character pair (██) to a pixel
        for (let i = 0; i < line.length; i += 2) {
            const char = line.substr(i, 2);
            const pixel = document.createElement('div');
            pixel.className = 'pixel';

            if (char === '██') {
                // Vary the color slightly for depth
                const colorVariations = [baseColor, shadeColor(baseColor, -20), shadeColor(baseColor, 20)];
                pixel.style.backgroundColor = colorVariations[Math.floor(Math.random() * colorVariations.length)];
                pixel.style.boxShadow = `0 0 2px ${baseColor}`;
            } else {
                pixel.style.backgroundColor = 'transparent';
            }

            row.appendChild(pixel);
        }

        frame.appendChild(row);
    });

    return frame;
}

// Helper to shade colors for variation
function shadeColor(color, percent) {
    const num = parseInt(color.replace('#', ''), 16);
    const amt = Math.round(2.55 * percent);
    const R = Math.max(0, Math.min(255, (num >> 16) + amt));
    const G = Math.max(0, Math.min(255, (num >> 8 & 0x00FF) + amt));
    const B = Math.max(0, Math.min(255, (num & 0x0000FF) + amt));
    return '#' + (0x1000000 + (R << 16) + (G << 8) + B).toString(16).slice(1);
}

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

    // Create pixel art barrel explosion (Metal Slug style)
    const barrelExplosion = document.createElement('div');
    barrelExplosion.className = 'pixel-explosion';

    // Frame 1: Initial flash
    const frame1 = createExplosionFrame([
        '    ██    ',
        '  ██████  ',
        '  ██████  ',
        '    ██    '
    ], '#ffff00');

    // Frame 2: Expanding blast
    const frame2 = createExplosionFrame([
        '  ██  ██  ',
        '██  ██  ██',
        '  ██████  ',
        '██  ██  ██',
        '  ██  ██  '
    ], '#ff8800');

    // Frame 3: Large explosion
    const frame3 = createExplosionFrame([
        '██    ██  ██',
        '  ████  ████',
        '██  ██████  ',
        '  ████████  ',
        '██  ██████  ',
        '  ████  ████',
        '██    ██  ██'
    ], '#ff4400');

    // Frame 4: Dissipating
    const frame4 = createExplosionFrame([
        '██      ██  ',
        '  ██  ██    ',
        '    ████    ',
        '  ██  ██    ',
        '██      ██  '
    ], '#ff2200');

    barrelExplosion.appendChild(frame1);
    barrelExplosion.appendChild(frame2);
    barrelExplosion.appendChild(frame3);
    barrelExplosion.appendChild(frame4);

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
        // Check if clicked element or any parent is a remove button
        const button = e.target.closest('.remove-btn') || e.target.closest('.position-remove-btn');
        if (button) {
            console.log('💥 Barrel explosion triggered for:', button.className);
            // Trigger explosion localized to the button's container
            // Don't prevent default - let calculator.js handle the actual removal
            triggerNuclearExplosion(button);
        }
    }, true); // Capture phase to run before calculator.js
});
