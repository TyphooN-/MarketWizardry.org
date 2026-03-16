/**
 * Ghost Portal - Floating spectral image with matrix letter shower
 * CSP compliant - no inline styles in HTML
 */
(function() {
    'use strict';

    const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()';
    let portalEl = null;
    let posX = 0;
    let posY = 0;
    let velX = 0.4;
    let velY = 0.3;
    let driftAngle = Math.random() * Math.PI * 2;

    function createPortal() {
        portalEl = document.createElement('div');
        portalEl.className = 'ghost-portal';

        // Outer spinning ring
        const ringOuter = document.createElement('div');
        ringOuter.className = 'ghost-portal-ring';
        portalEl.appendChild(ringOuter);

        // Inner spinning ring (reverse direction via CSS)
        const ringInner = document.createElement('div');
        ringInner.className = 'ghost-portal-ring-inner';
        portalEl.appendChild(ringInner);

        // The ghost image
        const img = document.createElement('img');
        img.src = '/img/mickey.jpg';
        img.alt = 'Ghost in the matrix';
        portalEl.appendChild(img);

        document.body.appendChild(portalEl);

        // Start position: center of viewport
        posX = window.innerWidth / 2 - 90;
        posY = window.innerHeight / 2 - 90;
        portalEl.style.left = posX + 'px';
        portalEl.style.top = posY + 'px';
    }

    function spawnLetterShower() {
        const rect = portalEl.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;

        // Spawn 2-4 letters around the portal
        const count = Math.floor(Math.random() * 3) + 2;
        for (let i = 0; i < count; i++) {
            const letter = document.createElement('div');
            letter.className = 'ghost-letter';
            letter.textContent = CHARS[Math.floor(Math.random() * CHARS.length)];

            // Random position around the portal edge
            const angle = Math.random() * Math.PI * 2;
            const radius = rect.width / 2 + Math.random() * 20;
            const lx = cx + Math.cos(angle) * radius;
            const ly = cy + Math.sin(angle) * radius;

            letter.style.left = lx + 'px';
            letter.style.top = ly + 'px';

            const duration = 1.5 + Math.random() * 1.5;
            const rotation = (Math.random() - 0.5) * 180;
            letter.style.setProperty('--gl-duration', duration + 's');
            letter.style.setProperty('--gl-rotate', rotation + 'deg');

            document.body.appendChild(letter);

            setTimeout(() => letter.remove(), duration * 1000 + 100);
        }
    }

    function movePortal() {
        if (!portalEl) return;

        const w = window.innerWidth - 180;
        const h = window.innerHeight - 180;

        // Gentle organic drift with perlin-like wandering
        driftAngle += (Math.random() - 0.5) * 0.15;
        velX += Math.cos(driftAngle) * 0.05;
        velY += Math.sin(driftAngle) * 0.05;

        // Dampen velocity for smooth movement
        velX *= 0.98;
        velY *= 0.98;

        // Clamp velocity
        const maxSpeed = 1.5;
        velX = Math.max(-maxSpeed, Math.min(maxSpeed, velX));
        velY = Math.max(-maxSpeed, Math.min(maxSpeed, velY));

        posX += velX;
        posY += velY;

        // Bounce off edges softly
        if (posX < 20) { posX = 20; velX = Math.abs(velX) * 0.7; driftAngle = Math.random() * Math.PI * 0.5; }
        if (posX > w - 20) { posX = w - 20; velX = -Math.abs(velX) * 0.7; driftAngle = Math.PI + Math.random() * Math.PI * 0.5; }
        if (posY < 60) { posY = 60; velY = Math.abs(velY) * 0.7; driftAngle = Math.PI * 0.5 + (Math.random() - 0.5); }
        if (posY > h - 20) { posY = h - 20; velY = -Math.abs(velY) * 0.7; driftAngle = -Math.PI * 0.5 + (Math.random() - 0.5); }

        portalEl.style.left = posX + 'px';
        portalEl.style.top = posY + 'px';

        requestAnimationFrame(movePortal);
    }

    function init() {
        createPortal();
        requestAnimationFrame(movePortal);

        // Letter shower every 300-600ms
        setInterval(spawnLetterShower, 400);

        // Initial burst of letters
        setTimeout(spawnLetterShower, 500);
        setTimeout(spawnLetterShower, 800);
        setTimeout(spawnLetterShower, 1100);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
