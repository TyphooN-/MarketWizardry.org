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

    // Removed emoji fireworks - spirals only

    function randomExplosion() {
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;

        createExplosion(x, y);
    }

    // Cleanup function to remove any orphaned spirals
    function cleanupOrphanedParticles() {
        const spirals = document.querySelectorAll('svg');
        spirals.forEach(spiral => {
            const rect = spiral.getBoundingClientRect();
            // Remove if spiral is way off screen or invisible
            if (rect.bottom < -500 || rect.top > window.innerHeight + 500 ||
                rect.right < -500 || rect.left > window.innerWidth + 500) {
                spiral.remove();
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
    });

    // Initial burst of explosions (reduced)
    setTimeout(() => randomExplosion(), 1000);
    setTimeout(() => randomExplosion(), 2500);

    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        clearInterval(explosionInterval);
    });

    console.log('🌀 404 Effects loaded - Fibonacci spiral explosions activated!');
})();
