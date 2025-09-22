// Add some retro terminal effects
document.addEventListener('DOMContentLoaded', function() {
    // Typewriter effect for error message (optional enhancement)
    const errorCode = document.querySelector('.error-code');

    // Add random glitch effect occasionally
    setInterval(() => {
        if (Math.random() < 0.1) { // 10% chance every interval
            errorCode.style.color = '#ffffff';
            setTimeout(() => {
                errorCode.style.color = '#ff0000';
            }, 100);
        }
    }, 2000);
});