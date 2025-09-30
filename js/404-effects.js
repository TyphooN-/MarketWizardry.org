// 404 Page Animation Effects - CSP Compliant

(function() {
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ff6600', '#00ff88', '#ff0088', '#88ff00'];

    // Removed background floating particles as per user request

    // Draw a Fibonacci spiral using SVG (optimized)
    function createFibonacciSpiral(x, y) {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.style.position = 'fixed';
        svg.style.left = '0px';
        svg.style.top = '0px';
        svg.style.width = '300px';
        svg.style.height = '300px';
        svg.style.pointerEvents = 'none';
        svg.style.zIndex = '7';
        svg.style.overflow = 'visible';
        svg.style.willChange = 'transform, opacity';

        // Create path for Fibonacci spiral
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');

        // Generate Fibonacci spiral path - reduced steps for performance
        let pathData = 'M 150 150 '; // Start at center of SVG
        const goldenRatio = 1.618033988749;
        const turns = 2.5; // Reduced turns
        const steps = 80; // Reduced from 200 to 80 for better performance

        for (let i = 0; i <= steps; i++) {
            const t = (i / steps) * turns * 2 * Math.PI;
            const r = 5 * Math.pow(goldenRatio, t / (Math.PI / 2));
            const spiralX = 150 + r * Math.cos(t);
            const spiralY = 150 + r * Math.sin(t);
            pathData += `L ${spiralX} ${spiralY} `;
        }

        path.setAttribute('d', pathData);
        path.setAttribute('fill', 'none');

        const color = colors[Math.floor(Math.random() * colors.length)];
        path.setAttribute('stroke', color);
        path.setAttribute('stroke-width', '2.5');
        path.style.filter = `drop-shadow(0 0 6px ${color})`;

        svg.appendChild(path);
        document.body.appendChild(svg);

        // Animate with CSS class for better performance
        const spinSpeed = 1.2 + Math.random() * 0.8; // 1.2-2s (reduced range)
        const spinDirection = Math.random() > 0.5 ? 1 : -1;
        const rotation = spinDirection * (360 + Math.random() * 360); // 1-2 rotations (reduced)

        const keyframes = [
            {
                transform: `translate(${x - 150}px, ${y - 150}px) scale(0.1) rotate(0deg)`,
                opacity: 0
            },
            {
                transform: `translate(${x - 150}px, ${y - 150}px) scale(0.4) rotate(${rotation * 0.2}deg)`,
                opacity: 1,
                offset: 0.2
            },
            {
                transform: `translate(${x - 150}px, ${y - 150}px) scale(1.2) rotate(${rotation}deg)`,
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
        // Create 1-2 Fibonacci spirals (reduced for performance)
        const spiralCount = 1 + Math.floor(Math.random() * 2); // 1 or 2 spirals

        for (let i = 0; i < spiralCount; i++) {
            setTimeout(() => createFibonacciSpiral(x, y), i * 150);
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

    // Random explosions around the page (optimized timing)
    const explosionInterval = setInterval(randomExplosion, 3000);

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

    // Initial explosion
    setTimeout(() => randomExplosion(), 1500);

    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        clearInterval(explosionInterval);
    });

    console.log('🌀 404 Effects loaded - Fibonacci spiral explosions activated!');
})();
