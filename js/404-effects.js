// 404 Page Animation Effects - CSP Compliant

(function() {
    const emojis = ['💰', '💸', '💵', '💴', '💶', '💷', '🔥', '💥', '⚡', '💣', '🚀', '📉', '📊', '💀', '🎰', '🎲', '❌', '⚠️', '🤑', '💎', '🏦', '📈', '🎯', '💔', '🌈', '✨', '💫', '🎪', '🎨'];
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ff6600', '#00ff88', '#ff0088', '#88ff00'];

    // Removed background floating particles as per user request

    function createExplosion(x, y) {
        // Create tighter spiral trail visualization with more arms
        const spiralCount = 8; // More spiral arms
        const goldenAngle = 137.508;

        for (let spiral = 0; spiral < spiralCount; spiral++) {
            // Create multiple dots per spiral arm for visible trail
            for (let j = 0; j < 20; j++) {
                const spiralEl = document.createElement('div');
                spiralEl.className = 'spiral-trail';
                spiralEl.style.position = 'fixed';
                spiralEl.style.left = '0px';
                spiralEl.style.top = '0px';
                spiralEl.style.width = '4px';
                spiralEl.style.height = '4px';
                spiralEl.style.borderRadius = '50%';
                spiralEl.style.pointerEvents = 'none';
                spiralEl.style.zIndex = '6';

                const color = colors[Math.floor(Math.random() * colors.length)];
                spiralEl.style.backgroundColor = color;
                spiralEl.style.boxShadow = `0 0 15px ${color}`;

                // Calculate tighter spiral path
                const baseAngle = (spiral / spiralCount) * 360;
                const angleOffset = j * goldenAngle / 4; // Tighter angle progression
                const radius = Math.sqrt(j + 1) * 15; // Tighter radius

                const spiralX = x + Math.cos((baseAngle + angleOffset) * Math.PI / 180) * radius;
                const spiralY = y + Math.sin((baseAngle + angleOffset) * Math.PI / 180) * radius;

                spiralEl.style.setProperty('--startX', x + 'px');
                spiralEl.style.setProperty('--startY', y + 'px');
                spiralEl.style.setProperty('--endX', spiralX + 'px');
                spiralEl.style.setProperty('--endY', spiralY + 'px');

                const duration = 1.8 + (j / 20) * 0.4;
                spiralEl.style.animation = `spiralTrailExpand ${duration}s ease-out forwards`;
                spiralEl.style.animationDelay = (j * 0.03 + spiral * 0.02) + 's';

                document.body.appendChild(spiralEl);

                setTimeout(() => {
                    if (spiralEl.parentNode) {
                        spiralEl.remove();
                    }
                }, (duration + j * 0.03 + spiral * 0.02) * 1000 + 100);
            }
        }

        // Create central burst
        const explosion = document.createElement('div');
        explosion.className = 'explosion';
        explosion.style.position = 'fixed';
        explosion.style.left = '0px';
        explosion.style.top = '0px';
        explosion.style.transform = `translate(${x}px, ${y}px)`;

        // Create colorful expanding rings
        for (let i = 0; i < 3; i++) {
            const ring = document.createElement('div');
            ring.className = 'explosion-ring';
            ring.style.borderColor = colors[Math.floor(Math.random() * colors.length)];
            ring.style.animationDelay = (i * 0.08) + 's';
            ring.style.borderRadius = '50%';
            ring.style.animation = `explodeSpiral ${0.8 + i * 0.1}s ease-out forwards`;
            explosion.appendChild(ring);
        }

        document.body.appendChild(explosion);

        setTimeout(() => {
            if (explosion.parentNode) {
                explosion.remove();
            }
        }, 1500);
    }

    function createEmojiFirework(x, y) {
        const particleCount = 89; // Fibonacci number for better spiral
        const goldenAngle = 137.508; // Golden angle in degrees

        for (let i = 1; i <= particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'emoji-particle';
            particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];

            // Use transform to position, not left/top to avoid expanding viewport
            particle.style.position = 'fixed';
            particle.style.left = '0px';
            particle.style.top = '0px';

            // Calculate fibonacci spiral positioning with TIGHTER spiral
            // The key is that particles start at spiral positions and expand outward
            const angle = i * goldenAngle; // Golden angle rotation
            const radiusStart = Math.sqrt(i) * 3; // Much tighter starting radius
            const radiusEnd = Math.sqrt(i) * 25; // Tighter ending radius for more compact spiral

            // Starting position (on the spiral)
            const startX = x + Math.cos(angle * Math.PI / 180) * radiusStart;
            const startY = y + Math.sin(angle * Math.PI / 180) * radiusStart;

            // Ending position (further out on the spiral)
            const endX = x + Math.cos(angle * Math.PI / 180) * radiusEnd;
            const endY = y + Math.sin(angle * Math.PI / 180) * radiusEnd;

            // Set CSS variables for animation
            particle.style.setProperty('--startX', startX + 'px');
            particle.style.setProperty('--startY', startY + 'px');
            particle.style.setProperty('--endX', endX + 'px');
            particle.style.setProperty('--endY', endY + 'px');
            particle.style.setProperty('--rotation', (angle * 3) + 'deg'); // More rotation

            const duration = 2.0 + (i / particleCount) * 0.8; // Longer duration for tighter spiral
            particle.style.animation = 'fireworkSpiralPath ' + duration + 's ease-out forwards';
            particle.style.animationDelay = (i / particleCount) * 0.2 + 's'; // More stagger

            document.body.appendChild(particle);

            // Ensure particle is removed after animation completes
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, (duration + 0.2 * (i / particleCount)) * 1000 + 100);
        }
    }

    function randomExplosion() {
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;

        createExplosion(x, y);
        createEmojiFirework(x, y);
    }

    // Cleanup function to remove any orphaned particles
    function cleanupOrphanedParticles() {
        const particles = document.querySelectorAll('.emoji-particle, .explosion, .floating-bg-particle, .spiral-trail');
        particles.forEach(particle => {
            const rect = particle.getBoundingClientRect();
            // Remove if particle is way off screen or invisible
            if (rect.bottom < -500 || rect.top > window.innerHeight + 500 ||
                rect.right < -500 || rect.left > window.innerWidth + 500) {
                particle.remove();
            }
        });
    }

    // Run cleanup every 5 seconds
    setInterval(cleanupOrphanedParticles, 5000);

    // Random explosions around the page
    const explosionInterval = setInterval(randomExplosion, 1200);

    // Random glitch effect on the floating text
    const errorText = document.getElementById('floatingError');
    if (errorText) {
        setInterval(() => {
            errorText.classList.add('glitch-effect');
            setTimeout(() => errorText.classList.remove('glitch-effect'), 300);
        }, 3000 + Math.random() * 2000);
    }

    // Click anywhere to create explosion
    document.addEventListener('click', (e) => {
        createExplosion(e.clientX, e.clientY);
        createEmojiFirework(e.clientX, e.clientY);
    });

    // Initial burst of explosions
    setTimeout(() => randomExplosion(), 500);
    setTimeout(() => randomExplosion(), 1000);
    setTimeout(() => randomExplosion(), 1500);
    setTimeout(() => randomExplosion(), 2000);

    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        clearInterval(explosionInterval);
    });

    console.log('🎆 404 Effects loaded - Financial salvation explosions activated!');
})();
