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
        const explosion = document.createElement('div');
        explosion.className = 'explosion';
        explosion.style.position = 'fixed';
        explosion.style.left = '0px';
        explosion.style.top = '0px';
        explosion.style.transform = `translate(${x}px, ${y}px)`;

        // Create spiral rings instead of circular rings
        for (let i = 0; i < 5; i++) {
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
        const particleCount = 34; // Use Fibonacci number for better spiral
        const goldenAngle = 137.508; // More precise golden angle

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'emoji-particle';
            particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];

            // Use transform to position, not left/top to avoid expanding viewport
            particle.style.position = 'fixed';
            particle.style.left = '0px';
            particle.style.top = '0px';

            // Calculate fibonacci spiral trajectory
            const angle = i * goldenAngle; // Each particle rotated by golden angle
            const radius = Math.sqrt(i + 1) * 30; // Distance increases with square root (spiral pattern)
            const tx = Math.cos(angle * Math.PI / 180) * radius;
            const ty = Math.sin(angle * Math.PI / 180) * radius;

            // Set initial position using transform
            particle.style.transform = `translate(${x}px, ${y}px)`;
            particle.style.setProperty('--tx', tx + 'px');
            particle.style.setProperty('--ty', ty + 'px');
            particle.style.setProperty('--startX', x + 'px');
            particle.style.setProperty('--startY', y + 'px');

            const duration = 1.2 + Math.random() * 0.4;
            particle.style.animation = 'fireworkSpiral ' + duration + 's ease-out forwards';

            document.body.appendChild(particle);

            // Ensure particle is removed after animation completes
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, duration * 1000 + 100);
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
        const particles = document.querySelectorAll('.emoji-particle, .explosion, .floating-bg-particle');
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
