// 404 Page Animation Effects - CSP Compliant

(function() {
    const emojis = ['💰', '💸', '💵', '💴', '💶', '💷', '🔥', '💥', '⚡', '💣', '🚀', '📉', '📊', '💀', '🎰', '🎲', '❌', '⚠️', '🤑', '💎', '🏦', '📈', '🎯', '💔', '🌈', '✨', '💫', '🎪', '🎨'];
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ff6600', '#00ff88', '#ff0088', '#88ff00'];

    // Removed background floating particles as per user request

    function createExplosion(x, y) {
        // Simple central flash only
        const explosion = document.createElement('div');
        explosion.className = 'explosion';
        explosion.style.position = 'fixed';
        explosion.style.left = '0px';
        explosion.style.top = '0px';
        explosion.style.transform = `translate(${x}px, ${y}px)`;

        // Just 2 simple expanding rings
        for (let i = 0; i < 2; i++) {
            const ring = document.createElement('div');
            ring.className = 'explosion-ring';
            ring.style.borderColor = colors[Math.floor(Math.random() * colors.length)];
            ring.style.animationDelay = (i * 0.1) + 's';
            ring.style.borderRadius = '50%';
            ring.style.animation = `explodeSpiral ${0.6 + i * 0.1}s ease-out forwards`;
            explosion.appendChild(ring);
        }

        document.body.appendChild(explosion);

        setTimeout(() => {
            if (explosion.parentNode) {
                explosion.remove();
            }
        }, 1000);
    }

    function createEmojiFirework(x, y) {
        const particleCount = 21; // Smaller Fibonacci number for performance
        const goldenAngle = 137.508; // Golden angle in degrees

        for (let i = 1; i <= particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'emoji-particle';
            particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];

            // Use transform to position, not left/top to avoid expanding viewport
            particle.style.position = 'fixed';
            particle.style.left = '0px';
            particle.style.top = '0px';

            // Create clear Fibonacci spiral arms
            // Each particle follows a spiral path outward
            const angle = i * goldenAngle; // Golden angle rotation

            // Use logarithmic spiral equation: r = a * e^(b*theta)
            // Simplified: r = scale * sqrt(i) for Fibonacci-like growth
            const scale = 18; // Adjust spacing
            const radius = Math.sqrt(i) * scale;

            // Final position on the spiral
            const endX = x + Math.cos(angle * Math.PI / 180) * radius;
            const endY = y + Math.sin(angle * Math.PI / 180) * radius;

            // Start from center
            particle.style.setProperty('--startX', x + 'px');
            particle.style.setProperty('--startY', y + 'px');
            particle.style.setProperty('--endX', endX + 'px');
            particle.style.setProperty('--endY', endY + 'px');

            const duration = 1.2;
            particle.style.animation = 'fireworkSpiralPath ' + duration + 's ease-out forwards';
            particle.style.animationDelay = (i * 0.03) + 's'; // Sequential release

            document.body.appendChild(particle);

            // Ensure particle is removed after animation completes
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, (duration + i * 0.03) * 1000 + 100);
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

    // Random explosions around the page (less frequent for performance)
    const explosionInterval = setInterval(randomExplosion, 2500);

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

    // Initial burst of explosions (reduced)
    setTimeout(() => randomExplosion(), 1000);
    setTimeout(() => randomExplosion(), 2500);

    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        clearInterval(explosionInterval);
    });

    console.log('🎆 404 Effects loaded - Financial salvation explosions activated!');
})();
