// 404 Page Animation Effects - CSP Compliant

(function() {
    const emojis = ['💰', '💸', '💵', '💴', '💶', '💷', '🔥', '💥', '⚡', '💣', '🚀', '📉', '📊', '💀', '🎰', '🎲', '❌', '⚠️', '🤑', '💎', '🏦', '📈', '🎯', '💔', '🌈', '✨', '💫', '🎪', '🎨'];
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ff6600', '#00ff88', '#ff0088', '#88ff00'];

    // Removed background floating particles as per user request

    // Draw a Fibonacci spiral using SVG
    function createFibonacciSpiral(x, y) {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.style.position = 'fixed';
        svg.style.left = '0px';
        svg.style.top = '0px';
        svg.style.width = '400px';
        svg.style.height = '400px';
        svg.style.pointerEvents = 'none';
        svg.style.zIndex = '7';
        svg.style.overflow = 'visible';

        // Create path for Fibonacci spiral
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');

        // Generate Fibonacci spiral path using parametric equations
        let pathData = 'M 200 200 '; // Start at center of SVG
        const goldenRatio = 1.618033988749;
        const turns = 3; // Number of spiral turns
        const steps = 200;

        for (let i = 0; i <= steps; i++) {
            const t = (i / steps) * turns * 2 * Math.PI;
            const r = 5 * Math.pow(goldenRatio, t / (Math.PI / 2)); // Fibonacci spiral equation
            const spiralX = 200 + r * Math.cos(t);
            const spiralY = 200 + r * Math.sin(t);
            pathData += `L ${spiralX} ${spiralY} `;
        }

        path.setAttribute('d', pathData);
        path.setAttribute('fill', 'none');

        const color = colors[Math.floor(Math.random() * colors.length)];
        path.setAttribute('stroke', color);
        path.setAttribute('stroke-width', '3');
        path.setAttribute('filter', `drop-shadow(0 0 8px ${color})`);

        svg.appendChild(path);
        document.body.appendChild(svg);

        // Animate the spiral with inline keyframes
        const spinSpeed = 1 + Math.random() * 2; // Random spin speed 1-3s
        const spinDirection = Math.random() > 0.5 ? 1 : -1;
        const rotation = spinDirection * (360 + Math.random() * 720); // 1-3 full rotations

        const keyframes = [
            {
                transform: `translate(${x - 200}px, ${y - 200}px) scale(0.1) rotate(0deg)`,
                opacity: 0
            },
            {
                transform: `translate(${x - 200}px, ${y - 200}px) scale(0.3) rotate(${rotation * 0.15}deg)`,
                opacity: 1,
                offset: 0.15
            },
            {
                transform: `translate(${x - 200}px, ${y - 200}px) scale(1.5) rotate(${rotation}deg)`,
                opacity: 0
            }
        ];

        svg.animate(keyframes, {
            duration: spinSpeed * 1000,
            easing: 'ease-out',
            fill: 'forwards'
        });

        setTimeout(() => {
            if (svg.parentNode) {
                svg.remove();
            }
        }, spinSpeed * 1000 + 100);
    }

    function createExplosion(x, y) {
        // Create 2-3 Fibonacci spirals spinning at different speeds
        const spiralCount = 2 + Math.floor(Math.random() * 2); // 2 or 3 spirals

        for (let i = 0; i < spiralCount; i++) {
            setTimeout(() => createFibonacciSpiral(x, y), i * 100);
        }
    }

    function createEmojiFirework(x, y) {
        const particleCount = 13; // Fibonacci number for performance
        const goldenAngle = 137.508; // Golden angle in degrees

        for (let i = 1; i <= particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'emoji-particle';
            particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];

            // Use transform to position, not left/top to avoid expanding viewport
            particle.style.position = 'fixed';
            particle.style.left = '0px';
            particle.style.top = '0px';

            // Create spiral arm trajectory
            const angle = i * goldenAngle;
            const scale = 22;
            const radius = Math.sqrt(i) * scale;

            // Final position on the spiral
            const endX = x + Math.cos(angle * Math.PI / 180) * radius;
            const endY = y + Math.sin(angle * Math.PI / 180) * radius;

            // Start from center
            particle.style.setProperty('--startX', x + 'px');
            particle.style.setProperty('--startY', y + 'px');
            particle.style.setProperty('--endX', endX + 'px');
            particle.style.setProperty('--endY', endY + 'px');

            const duration = 1.5;
            particle.style.animation = 'fireworkSpiralPath ' + duration + 's ease-out forwards';
            particle.style.animationDelay = (i * 0.05) + 's';

            document.body.appendChild(particle);

            // Ensure particle is removed after animation completes
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, (duration + i * 0.05) * 1000 + 100);
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
        const particles = document.querySelectorAll('.emoji-particle, .explosion, .floating-bg-particle, .spiral-trail, svg');
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
