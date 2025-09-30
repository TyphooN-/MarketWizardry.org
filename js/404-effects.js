// 404 Page Animation Effects - CSP Compliant

(function() {
    const emojis = ['💰', '💸', '💵', '💴', '💶', '💷', '🔥', '💥', '⚡', '💣', '🚀', '📉', '📊', '💀', '🎰', '🎲', '❌', '⚠️', '🤑', '💎', '🏦', '📈', '🎯', '💔'];
    const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ff6600', '#00ff88'];

    function createExplosion(x, y) {
        const explosion = document.createElement('div');
        explosion.className = 'explosion';
        explosion.style.left = x + 'px';
        explosion.style.top = y + 'px';

        // Create multiple rings for explosion effect
        for (let i = 0; i < 3; i++) {
            const ring = document.createElement('div');
            ring.className = 'explosion-ring';
            ring.style.borderColor = colors[Math.floor(Math.random() * colors.length)];
            ring.style.animationDelay = (i * 0.1) + 's';
            explosion.appendChild(ring);
        }

        document.body.appendChild(explosion);

        setTimeout(() => explosion.remove(), 1000);
    }

    function createEmojiFirework(x, y) {
        const particleCount = 15;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'emoji-particle';
            particle.textContent = emojis[Math.floor(Math.random() * emojis.length)];
            particle.style.left = x + 'px';
            particle.style.top = y + 'px';

            // Calculate trajectory
            const angle = (360 / particleCount) * i;
            const distance = 100 + Math.random() * 150;
            const tx = Math.cos(angle * Math.PI / 180) * distance;
            const ty = Math.sin(angle * Math.PI / 180) * distance;

            particle.style.setProperty('--tx', tx + 'px');
            particle.style.setProperty('--ty', ty + 'px');
            particle.style.animation = 'firework ' + (0.8 + Math.random() * 0.6) + 's ease-out forwards';

            document.body.appendChild(particle);

            setTimeout(() => particle.remove(), 1500);
        }
    }

    function randomExplosion() {
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;

        createExplosion(x, y);
        createEmojiFirework(x, y);
    }

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
