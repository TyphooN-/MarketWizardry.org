const files = {
    1: 'LICENSE',
    2: 'DISCLAIMER_AND_RISK_WARNING',
    3: 'MARKET_WIZARDS',
    4: 'GAMERS_NEXUS',
    5: 'DER8AUER',
    6: 'FINANCIAL_DISCLAIMERS',
    7: 'OVERCLOCKING_FORUMS',
    8: 'CRYPTOCURRENCY_DISCLAIMERS',
    9: 'OPEN_SOURCE_DISCLAIMERS',
    10: 'GAMING_INDUSTRY_DISCLAIMERS',
    11: 'AI_ML_PLATFORM_DISCLAIMERS',
    12: 'PRIVACY_COMMUNICATION_DISCLAIMERS',
};

let currentFileIndex = 0;
let currentFileContent = '';

// Initialize file grid
function initializeFileGrid() {
    const fileGrid = document.getElementById('fileGrid');
    let maxFileNameWidth = 0;

    // Create temporary elements to measure widths
    const tempDiv = document.createElement('div');
    tempDiv.style.position = 'absolute';
    tempDiv.style.visibility = 'hidden';
    document.body.appendChild(tempDiv);

    // Create file entries and measure widths
    Object.values(files).forEach(fileName => {
        const fileEntry = document.createElement('div');
        fileEntry.className = 'file-entry';
        fileEntry.textContent = fileName;
        fileGrid.appendChild(fileEntry);
        tempDiv.textContent = fileName;
        maxFileNameWidth = Math.max(maxFileNameWidth+1, tempDiv.offsetWidth);
    });

    // Clean up temporary element
    document.body.removeChild(tempDiv);

    // Set fixed width for all elements and update grid layout
    const fileEntries = document.querySelectorAll('.file-entry');
    const finalWidth = Math.max(maxFileNameWidth + 40, 280); // Minimum 280px width

    fileEntries.forEach(entry => {
        entry.style.width = `${finalWidth}px`;
    });

    // Update grid to use responsive multi-column layout
    // This will create 2-4 columns depending on screen width
    fileGrid.style.gridTemplateColumns = `repeat(auto-fit, ${finalWidth}px)`;
    fileGrid.style.justifyContent = 'center';

    // Add click event listeners to file entries
    fileEntries.forEach((entry, index) => {
        entry.addEventListener('click', () => {
            const fileName = entry.textContent;
            currentFileIndex = index;
            loadFile(fileName);
        });
    });
}

function loadFile(fileName) {
    // Update this path if needed
    const filePath = `./terms/${fileName}`;
    fetch(filePath)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load file');
            }
            return response.text();
        })
        .then(text => {
            displayText(text, fileName);
        })
        .catch(error => {
            console.error('Error loading file:', error);
            alert(`Failed to load file: ${fileName}`);
        });
}

function displayText(content, fileName) {
    currentFileContent = content;
    document.getElementById('textContent').textContent = content;
    document.getElementById('modalTitle').textContent = fileName;

    // Set up download link
    const downloadLink = document.getElementById('downloadLink');
    const blob = new Blob([content], { type: 'text/plain' });
    downloadLink.href = URL.createObjectURL(blob);
    downloadLink.download = fileName + '.txt';

    document.getElementById('textModal').style.display = 'block';
    updateNavCounter();
}

function navigatePrevious() {
    const fileKeys = Object.keys(files);
    currentFileIndex = currentFileIndex > 0 ? currentFileIndex - 1 : fileKeys.length - 1;
    loadFile(files[fileKeys[currentFileIndex]]);
}

function navigateNext() {
    const fileKeys = Object.keys(files);
    currentFileIndex = currentFileIndex < fileKeys.length - 1 ? currentFileIndex + 1 : 0;
    loadFile(files[fileKeys[currentFileIndex]]);
}

function updateNavCounter() {
    const fileKeys = Object.keys(files);
    const navCounter = document.getElementById('navCounter');
    if (navCounter) {
        navCounter.textContent = `${currentFileIndex + 1} / ${fileKeys.length}`;
    }
}

function closeModal() {
    document.getElementById('textModal').style.display = 'none';
    // Clean up blob URL
    const downloadLink = document.getElementById('downloadLink');
    if (downloadLink.href.startsWith('blob:')) {
        URL.revokeObjectURL(downloadLink.href);
    }
}

// Enhanced keyboard navigation
document.addEventListener('keydown', function(event) {
    const modal = document.getElementById('textModal');
    if (modal.style.display === 'block') {
        if (event.key === 'Escape') {
            closeModal();
        } else if (event.key === 'ArrowLeft') {
            navigatePrevious();
        } else if (event.key === 'ArrowRight') {
            navigateNext();
        } else if (event.key === 'd' && (event.ctrlKey || event.metaKey)) {
            // Ctrl+D or Cmd+D to download
            event.preventDefault();
            document.getElementById('downloadLink').click();
        }
    }
});

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('textModal');
    if (event.target === modal) {
        closeModal();
    }
});

// Event delegation for data-action attributes
document.addEventListener('click', function(e) {
    if (e.target.hasAttribute('data-action')) {
        const action = e.target.getAttribute('data-action');

        switch(action) {
            case 'navigatePrevious':
                navigatePrevious();
                break;
            case 'navigateNext':
                navigateNext();
                break;
        }
    }
});

// Set up close button and initialize after DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.close-button').addEventListener('click', closeModal);
    initializeFileGrid();
});

// Make functions globally accessible for backward compatibility
window.navigatePrevious = navigatePrevious;
window.navigateNext = navigateNext;
window.closeModal = closeModal;