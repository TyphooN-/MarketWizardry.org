// GPU Buyers Guide Adventure Modal System
// Handles the interactive adventure grid with multiple content sources

document.addEventListener('DOMContentLoaded', function() {
    initializeGPUAdventureModal();
});

function initializeGPUAdventureModal() {
    const modal = document.getElementById("adventureModal");
    const adventureItems = document.querySelectorAll(".adventure-item");
    const modalImage = modal?.querySelector('.modal-image');
    const modalIntroText = modal?.querySelector('.modal-intro-text');
    const modalText = modal?.querySelector('.modal-text');
    const closeBtn = modal?.querySelector('.close');
    const prevBtn = document.getElementById('prevAdventure');
    const nextBtn = document.getElementById('nextAdventure');
    const counterDisplay = document.getElementById('adventureCounter');

    if (!modal || !modalImage || !modalIntroText || !modalText || !closeBtn) {
        console.error('GPU Adventure modal elements not found');
        return false;
    }

    modal.style.display = "none";
    let currentItemIndex = -1;

    function updateCounter() {
        if (counterDisplay && currentItemIndex >= 0) {
            counterDisplay.textContent = `${currentItemIndex + 1} / ${adventureItems.length}`;
        }
    }

    function navigatePrevious() {
        if (currentItemIndex > 0) {
            openAdventureModal(currentItemIndex - 1);
        }
    }

    function navigateNext() {
        if (currentItemIndex < adventureItems.length - 1) {
            openAdventureModal(currentItemIndex + 1);
        }
    }

    function loadTextFile(url, callback) {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.status}`);
                }
                return response.text();
            })
            .then(data => callback(null, data))
            .catch(error => {
                console.error('Fetch error:', error);
                callback(error, 'Failed to load content. Please try again.');
            });
    }

    function fitTextToIntroContainer(text) {
        const words = text.split(' ');
        let introText = '';
        let remainingText = '';

        modalIntroText.style.overflow = 'visible';
        modalIntroText.textContent = '';

        for (let i = 0; i < words.length; i++) {
            const testText = introText + (introText ? ' ' : '') + words[i];
            modalIntroText.textContent = testText;

            if (modalIntroText.scrollHeight > modalIntroText.clientHeight) {
                remainingText = words.slice(i).join(' ');
                break;
            }
            introText = testText;
        }

        modalIntroText.style.overflow = 'hidden';
        modalIntroText.textContent = introText;
        return { introText, remainingText };
    }

    function openAdventureModal(index) {
        if (index < 0 || index >= adventureItems.length) return;
        currentItemIndex = index;

        const item = adventureItems[currentItemIndex];
        const textFile = item.getAttribute('data-text');
        const imgSrc = item.getAttribute('data-image');

        modalImage.src = imgSrc;
        modalImage.alt = item.querySelector('.adventure-title')?.textContent || 'GPU Analysis';

        // Handle local vs remote text files
        const textUrl = textFile.startsWith('http') ? textFile : `/blog/${textFile}`;

        loadTextFile(textUrl, (error, data) => {
            if (error) {
                console.error('Failed to load text file:', error);
                modalIntroText.textContent = 'Failed to load content. Please try again.';
                modalText.textContent = '';
            } else {
                const paragraphs = data.split('\n\n');
                const firstParagraph = paragraphs[0] || '';
                const remainingParagraphs = paragraphs.slice(1).join('\n\n') || '';

                const { introText, remainingText } = fitTextToIntroContainer(firstParagraph);
                modalIntroText.textContent = introText;
                modalText.textContent = (remainingText ? remainingText + '\n\n' : '') + remainingParagraphs;
            }

            modal.style.display = "block";
            document.body.style.overflow = "hidden";
            updateCounter();
            modal.focus();
        });
    }

    function closeAdventureModal() {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
        currentItemIndex = -1;
    }

    // Event listeners for adventure items
    adventureItems.forEach((item, index) => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            openAdventureModal(index);
        });

        // Add keyboard support
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openAdventureModal(index);
            }
        });
    });

    // Close button event listener
    closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        closeAdventureModal();
    });

    // Modal background click to close
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeAdventureModal();
        }
    });

    // Navigation button event listeners
    if (prevBtn) {
        prevBtn.addEventListener('click', navigatePrevious);
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', navigateNext);
    }

    // Keyboard navigation
    modal.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAdventureModal();
        } else if (e.key === 'ArrowLeft') {
            navigatePrevious();
        } else if (e.key === 'ArrowRight') {
            navigateNext();
        }
    });

    // Touch support for mobile
    adventureItems.forEach((item, index) => {
        let touchStartTime = 0;
        let touchStartX = 0;
        let touchStartY = 0;

        item.addEventListener('touchstart', (e) => {
            touchStartTime = Date.now();
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        });

        item.addEventListener('touchend', (e) => {
            e.preventDefault();
            const touchEndTime = Date.now();
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            const touchDuration = touchEndTime - touchStartTime;
            const touchDistance = Math.sqrt(
                Math.pow(touchEndX - touchStartX, 2) + Math.pow(touchEndY - touchStartY, 2)
            );

            // Only trigger if it's a tap (short duration, minimal movement)
            if (touchDuration < 500 && touchDistance < 30) {
                openAdventureModal(index);
            }
        });
    });

    return true;
}