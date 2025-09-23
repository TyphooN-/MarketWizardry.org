// ATR Explorer functionality

// Event delegation for data-action attributes
document.addEventListener('click', function(e) {
    const action = e.target.getAttribute('data-action');
    if (action) {
        switch(action) {
            case 'open-modal-with-file':
                e.preventDefault();
                const outlierFile = e.target.getAttribute('data-outlier-file');
                const csvFile = e.target.getAttribute('data-csv-file');
                const displayName = e.target.getAttribute('data-display-name');
                if (outlierFile && displayName) {
                    openModalWithFile(outlierFile, csvFile, displayName);
                }
                break;
            case 'close-modal':
                closeModal();
                break;
            case 'previous':
                previousFile();
                break;
            case 'next':
                nextFile();
                break;
        }
    }
});

let currentFileIndex = 0;
let filesList = [];

function openModalWithFile(outlierFile, csvFile, title) {
    // Find current file index
    for (let i = 0; i < filesList.length; i++) {
        if (filesList[i].outlier === outlierFile) {
            currentFileIndex = i;
            break;
        }
    }

    document.getElementById('modal-title').innerText = title;
    document.getElementById('csv-link').href = csvFile;
    document.getElementById('csv-link').style.display = csvFile ? 'inline' : 'none';
    document.getElementById('outlier-modal').style.display = 'block';
    updateNavCounter();

    // Load outlier file content
    fetch(outlierFile)
        .then(response => response.text())
        .then(data => {
            document.getElementById('outlier-content').textContent = data;
        })
        .catch(error => {
            document.getElementById('outlier-content').textContent = 'Error loading file: ' + error;
        });
}

function closeModal() {
    document.getElementById('outlier-modal').style.display = 'none';
}

function previousFile() {
    if (currentFileIndex > 0) {
        currentFileIndex--;
        const file = filesList[currentFileIndex];
        openModalWithFile(file.outlier, file.csv, file.display);
    }
}

function nextFile() {
    if (currentFileIndex < filesList.length - 1) {
        currentFileIndex++;
        const file = filesList[currentFileIndex];
        openModalWithFile(file.outlier, file.csv, file.display);
    }
}

function updateNavCounter() {
    const counter = document.getElementById('nav-counter');
    if (counter && filesList.length > 0) {
        counter.textContent = `${currentFileIndex + 1} of ${filesList.length}`;
    }
}

// Window click event to close modal
window.addEventListener('click', function(event) {
    const modal = document.getElementById('outlier-modal');
    if (event.target === modal) {
        closeModal();
    }
});

// Initialize files list on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeFilesList();
});

function initializeFilesList() {
    filesList = [];
    const links = document.querySelectorAll('[data-action="open-modal-with-file"]');
    links.forEach(link => {
        filesList.push({
            outlier: link.getAttribute('data-outlier-file'),
            csv: link.getAttribute('data-csv-file'),
            display: link.getAttribute('data-display-name')
        });
    });
}