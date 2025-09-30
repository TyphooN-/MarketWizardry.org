/**
 * Matrix Rain Animation
 * Extracted from inline script for CSP compliance
 * Creates falling matrix-style text effects
 */

const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+-={}:<>?';
const container = document.querySelector('body');

function createMatrixText() {
    const char = characters[Math.floor(Math.random() * characters.length)];
    const element = document.createElement('div');
    element.className = 'matrix-text matrix-char';

    // Random position (within viewable area)
    element.style.left = Math.random() * 100 + '%';
    element.style.top = '-50px'; // Start above viewport

    // Random animation duration (speed)
    const duration = Math.random() * 3 + 2; // between 2-5 seconds

    // Apply styles
    element.style.setProperty('--duration', `${duration}s`);
    element.style.setProperty('--delay', '0s'); /* Immediate start */
    element.textContent = char;

    container.appendChild(element);

    // Remove element after animation
    setTimeout(() => {
        element.remove();
    }, duration * 1000 + 500);
}

// Initialize matrix animation
function initMatrixAnimation() {
    // Create periodic matrix text
    setInterval(createMatrixText, 50);

    // Initial burst of characters
    for (let i = 0; i < 69; i++) {
        setTimeout(createMatrixText, Math.random() * 5000);
    }
}

// Start animation when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMatrixAnimation);
} else {
    initMatrixAnimation();
}