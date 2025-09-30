// 404 Page Animation Effects - CSP Compliant

(function() {
    const emojis = ['💰', '💸', '💵', '💴', '💶', '💷', '🔥', '💥', '⚡', '💣', '🚀', '📉', '📊', '💀', '🎰', '🎲', '❌', '⚠️', '🤑', '💎', '🏦', '📈', '🎯', '💔', '🌈', '✨', '💫', '🎪', '🎨'];
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ff6600', '#00ff88', '#ff0088', '#88ff00'];

    // Create floating particles in background
    function createFloatingParticle() {
        const particle = document.createElement('div');
        particle.className = 'floating-bg-particle';
        particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.fontSize = (0.5 + Math.random() * 1.5) + 'em';
        particle.style.animationDuration = (10 + Math.random() * 20) + 's';
        particle.style.animationDelay = Math.random() * 5 + 's';
        document.body.appendChild(particle);

        setTimeout(() => particle.remove(), 30000);
    }

    // Add CSS for floating particles
    const style = document.createElement('style');
    style.textContent = `
        .floating-bg-particle {
            position: fixed;
            pointer-events: none;
            z-index: 1;
            opacity: 0.3;
            animation: floatAround 15s ease-in-out infinite;
        }
        @keyframes floatAround {
            0%, 100% {
                transform: translate(0, 0) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 0.3;
            }
            50% {
                transform: translate(${Math.random() * 200 - 100}px, ${Math.random() * 200 - 100}px) rotate(360deg);
                opacity: 0.5;
            }
            90% {
                opacity: 0.3;
            }
        }
    `;
    document.head.appendChild(style);

    // Create initial floating particles
    for (let i = 0; i < 15; i++) {
        setTimeout(() => createFloatingParticle(), i * 200);
    }

    // Keep creating new particles
    setInterval(createFloatingParticle, 3000);

    function createExplosion(x, y) {
        // Create spiral trail visualization
        const spiralCount = 5;
        const goldenAngle = 137.508;

        for (let spiral = 0; spiral < spiralCount; spiral++) {
            const spiralEl = document.createElement('div');
            spiralEl.className = 'spiral-trail';
            spiralEl.style.position = 'fixed';
            spiralEl.style.left = '0px';
            spiralEl.style.top = '0px';
            spiralEl.style.width = '3px';
            spiralEl.style.height = '3px';
            spiralEl.style.borderRadius = '50%';
            spiralEl.style.pointerEvents = 'none';
            spiralEl.style.zIndex = '6';

            const color = colors[Math.floor(Math.random() * colors.length)];
            spiralEl.style.backgroundColor = color;
            spiralEl.style.boxShadow = `0 0 10px ${color}`;

            // Calculate spiral path
            const startAngle = (spiral / spiralCount) * 360;
            spiralEl.style.setProperty('--centerX', x + 'px');
            spiralEl.style.setProperty('--centerY', y + 'px');
            spiralEl.style.setProperty('--startAngle', startAngle + 'deg');
            spiralEl.style.setProperty('--goldenAngle', goldenAngle + 'deg');

            const duration = 1.5 + Math.random() * 0.5;
            spiralEl.style.animation = `spiralExpand ${duration}s ease-out forwards`;
            spiralEl.style.animationDelay = (spiral * 0.05) + 's';

            document.body.appendChild(spiralEl);

            setTimeout(() => {
                if (spiralEl.parentNode) {
                    spiralEl.remove();
                }
            }, (duration + spiral * 0.05) * 1000 + 100);
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
        const particleCount = 55; // Use more particles for better spiral visibility
        const goldenAngle = 137.508; // Golden angle in degrees

        for (let i = 1; i <= particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'emoji-particle';
            particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];

            // Use transform to position, not left/top to avoid expanding viewport
            particle.style.position = 'fixed';
            particle.style.left = '0px';
            particle.style.top = '0px';

            // Calculate fibonacci spiral positioning
            // The key is that particles start at spiral positions and expand outward
            const angle = i * goldenAngle; // Golden angle rotation
            const radiusStart = Math.sqrt(i) * 8; // Starting radius (tight spiral)
            const radiusEnd = Math.sqrt(i) * 45; // Ending radius (expanded spiral)

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
            particle.style.setProperty('--rotation', (angle * 2) + 'deg');

            const duration = 1.5 + (i / particleCount) * 0.5; // Outer particles take longer
            particle.style.animation = 'fireworkSpiralPath ' + duration + 's ease-out forwards';
            particle.style.animationDelay = (i / particleCount) * 0.15 + 's'; // Stagger for spiral effect

            document.body.appendChild(particle);

            // Ensure particle is removed after animation completes
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, (duration + 0.15 * (i / particleCount)) * 1000 + 100);
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
