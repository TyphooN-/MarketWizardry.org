// 404 Page Animation Effects - CSP Compliant

(function() {
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ff6600', '#00ff88', '#ff0088', '#88ff00'];

    // Detect mobile device for performance optimization
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth < 768;

    // Draw a Fibonacci spiral using SVG (mobile optimized)
    function createFibonacciSpiral(x, y) {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.style.position = 'fixed';
        svg.style.left = '0px';
        svg.style.top = '0px';

        // Smaller size for mobile
        const size = isMobile ? 200 : 300;
        svg.style.width = size + 'px';
        svg.style.height = size + 'px';
        svg.style.pointerEvents = 'none';
        svg.style.zIndex = '7';
        svg.style.overflow = 'visible';
        svg.style.willChange = 'transform, opacity';

        // Create path for Fibonacci spiral
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');

        // Generate Fibonacci spiral path - further reduced for mobile
        const center = size / 2;
        let pathData = `M ${center} ${center} `;
        const goldenRatio = 1.618033988749;
        const turns = isMobile ? 2 : 2.5; // Fewer turns on mobile
        const steps = isMobile ? 40 : 80; // Fewer steps on mobile (50% reduction)

        for (let i = 0; i <= steps; i++) {
            const t = (i / steps) * turns * 2 * Math.PI;
            const r = 5 * Math.pow(goldenRatio, t / (Math.PI / 2));
            const spiralX = center + r * Math.cos(t);
            const spiralY = center + r * Math.sin(t);
            pathData += `L ${spiralX} ${spiralY} `;
        }

        path.setAttribute('d', pathData);
        path.setAttribute('fill', 'none');

        const color = colors[Math.floor(Math.random() * colors.length)];
        path.setAttribute('stroke', color);
        path.setAttribute('stroke-width', isMobile ? '2' : '2.5');

        // Remove drop-shadow on mobile for better performance
        if (!isMobile) {
            path.style.filter = `drop-shadow(0 0 6px ${color})`;
        }

        svg.appendChild(path);
        document.body.appendChild(svg);

        // Simpler animation for mobile
        const spinSpeed = isMobile ? 1.0 : (1.2 + Math.random() * 0.8);
        const spinDirection = Math.random() > 0.5 ? 1 : -1;
        const rotation = spinDirection * (isMobile ? 360 : (360 + Math.random() * 360));

        const keyframes = [
            {
                transform: `translate(${x - center}px, ${y - center}px) scale(0.1) rotate(0deg)`,
                opacity: 0
            },
            {
                transform: `translate(${x - center}px, ${y - center}px) scale(${isMobile ? 0.6 : 0.4}) rotate(${rotation * 0.2}deg)`,
                opacity: 1,
                offset: 0.2
            },
            {
                transform: `translate(${x - center}px, ${y - center}px) scale(${isMobile ? 1 : 1.2}) rotate(${rotation}deg)`,
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
        // Create fewer spirals on mobile
        const spiralCount = isMobile ? 1 : (1 + Math.floor(Math.random() * 2));

        for (let i = 0; i < spiralCount; i++) {
            setTimeout(() => createFibonacciSpiral(x, y), i * (isMobile ? 200 : 150));
        }
    }

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

    // Run cleanup less frequently on mobile
    setInterval(cleanupOrphanedParticles, isMobile ? 10000 : 5000);

    // Random explosions - less frequent on mobile
    const explosionInterval = setInterval(randomExplosion, isMobile ? 5000 : 3000);

    // Random glitch effect on the floating text - disabled on mobile
    if (!isMobile) {
        const errorText = document.getElementById('floatingError');
        if (errorText) {
            setInterval(() => {
                errorText.classList.add('glitch-effect');
                setTimeout(() => errorText.classList.remove('glitch-effect'), 300);
            }, 3000 + Math.random() * 2000);
        }
    }

    // Rotating error code animation - optimized with CSS variable
    const errorCode = document.getElementById('errorCode');
    if (errorCode) {
        function rotateErrorCode() {
            // Random rotation parameters
            const duration = 1500 + Math.random() * 1500; // 1.5-3 seconds
            const angle = (Math.random() > 0.5 ? 1 : -1) * (8 + Math.random() * 12); // ±8° to ±20°

            const keyframes = [
                { transform: 'rotate(0deg)' },
                { transform: `rotate(${angle}deg)` },
                { transform: 'rotate(0deg)' }
            ];

            const animation = errorCode.animate(keyframes, {
                duration: duration,
                easing: 'ease-in-out'
            });

            // Schedule next rotation after this one finishes
            animation.onfinish = () => {
                const nextDelay = 3000 + Math.random() * 2000; // 3-5 seconds
                setTimeout(rotateErrorCode, nextDelay);
            };
        }

        // Start rotating after initial load
        setTimeout(rotateErrorCode, 1500);
    }

    // Click anywhere to create explosion
    document.addEventListener('click', (e) => {
        createExplosion(e.clientX, e.clientY);
    });

    // Initial explosion - skip on mobile for faster load
    if (!isMobile) {
        setTimeout(() => randomExplosion(), 1500);
    }

    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        clearInterval(explosionInterval);
    });

    console.log('🌀 404 Effects loaded - Fibonacci spiral explosions activated!' + (isMobile ? ' (Mobile optimized)' : ''));
})();
