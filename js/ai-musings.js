// AI Musings data with flavor text
const musings = [
    {
        title: "ICT 1",
        filename: "ICT_1.txt",
        flavor: "Examining the Inner Circle Trader's methods of repackaging classical trading concepts with modern marketing flair",
        words: 427
    },
    {
        title: "ICT 2",
        filename: "ICT_2.txt",
        flavor: "A critical look at ICT's competition performance and the gap between promotional claims and actual results",
        words: 344
    },
    {
        title: "Elon Antichrist",
        filename: "elon_antichrist.txt",
        flavor: "A dystopian tale of NeuralLink, mind control, and the price of technological progress without ethical boundaries",
        words: 580
    },
    {
        title: "Financial Advice",
        filename: "financial_advice.txt",
        flavor: "Why 500x leverage on a second mortgage is a terrible idea - a comprehensive breakdown of crypto investment risks",
        words: 664
    },
    {
        title: "GPU Inferno",
        filename: "gpu_inferno.txt",
        flavor: "A tale of greed, corruption, and the GPU Inferno Cartel - where profit eclipses safety and morality burns",
        words: 657
    },
    {
        title: "Jensen Huang Goodguy",
        filename: "jensen_huang_goodguy.txt",
        flavor: "The price of ambition - when a CEO faces the consequences of prioritizing deadlines over safety",
        words: 406
    },
    {
        title: "Monero Adoption",
        filename: "monero_adoption.txt",
        flavor: "Why privacy-focused cryptocurrency struggles for mainstream acceptance despite Bitcoin paving the way",
        words: 1223
    },
    {
        title: "Nvidia Missing ROPs",
        filename: "nvidia_missing_ROPs.txt",
        flavor: "The mystery of Nvidia's disappearing ROPs and Jensen's dismissive quips about the RTX 5000 series shortcomings",
        words: 734
    },
    {
        title: "Nvidia Snake Oil",
        filename: "nvidia_snake_oil.txt",
        flavor: "While Nvidia users pray their 12VHPWR connectors don't combust, AMD quietly delivers stable, fire-free computing",
        words: 361
    },
    {
        title: "Snoop Fire Spaghetti",
        filename: "snoop_fire_spaghetti.txt",
        flavor: "Snoop Dogg's quest for fire spaghetti with special sauce - cooking with attitude from Japan",
        words: 818
    },
    {
        title: "Terry Davis Quest",
        filename: "terry_davis_quest.txt",
        flavor: "Terry Davis navigates the afterlife armed with HolyC code, seeking God through TempleOS and divine tuna",
        words: 575
    },
    {
        title: "The Cost Of Pixels",
        filename: "the_cost_of_pixels.txt",
        flavor: "When innovation becomes tragedy - lives lost to GPU fires while a CEO sips champagne above the city",
        words: 454
    },
    {
        title: "The Great Wall Showdown",
        filename: "the_great_wall_showdown.txt",
        flavor: "Dystopian battle royale at the Great Wall where warriors fight for survival and spark rebellion against the New World Order",
        words: 1148
    }
];

let currentMusingIndex = 0;

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    populateGrid();
    setupModalHandlers();
});

// Populate the grid with musing entries
function populateGrid() {
    const grid = document.getElementById('musingsGrid');

    musings.forEach((musing, index) => {
        const entry = document.createElement('div');
        entry.className = 'musing-card';
        entry.innerHTML = `
            <div class="musing-card-header">
                <h3>${musing.title}</h3>
                <span class="word-count">${musing.words} words</span>
            </div>
            <p class="flavor">${musing.flavor}</p>
        `;
        entry.addEventListener('click', () => openMusing(index));
        grid.appendChild(entry);
    });
}

// Open a musing in the modal
function openMusing(index) {
    currentMusingIndex = index;
    const musing = musings[index];

    document.getElementById('modalTitle').textContent = musing.title;
    updateCounter();

    // Set the download link
    const downloadLink = document.getElementById('downloadLink');
    downloadLink.href = `/ai-musings/${musing.filename}`;
    downloadLink.download = musing.filename;

    // Load the content
    fetch(`/ai-musings/${musing.filename}`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to load musing');
            return response.text();
        })
        .then(text => {
            document.getElementById('textContent').textContent = text;
            document.getElementById('textModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error loading musing:', error);
            document.getElementById('textContent').textContent = 'Error loading musing content. Please try again.';
            document.getElementById('textModal').style.display = 'block';
        });
}

// Close the modal
function closeModal() {
    document.getElementById('textModal').style.display = 'none';
}

// Navigate to previous musing
function previousMusing() {
    currentMusingIndex = (currentMusingIndex - 1 + musings.length) % musings.length;
    openMusing(currentMusingIndex);
}

// Navigate to next musing
function nextMusing() {
    currentMusingIndex = (currentMusingIndex + 1) % musings.length;
    openMusing(currentMusingIndex);
}

// Update the counter display
function updateCounter() {
    document.getElementById('navCounter').textContent = `${currentMusingIndex + 1} / ${musings.length}`;
}

// Setup modal event handlers
function setupModalHandlers() {
    // Close button
    document.querySelector('[data-action="close"]').addEventListener('click', closeModal);

    // Previous button
    document.getElementById('prevButton').addEventListener('click', previousMusing);

    // Next button
    document.getElementById('nextButton').addEventListener('click', nextMusing);

    // Click outside modal to close
    document.getElementById('textModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal();
        }
    });

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        const modal = document.getElementById('textModal');
        if (modal.style.display === 'block') {
            if (e.key === 'Escape') {
                closeModal();
            } else if (e.key === 'ArrowLeft') {
                previousMusing();
            } else if (e.key === 'ArrowRight') {
                nextMusing();
            }
        }
    });
}

// Make functions globally accessible
window.openMusing = openMusing;
window.closeModal = closeModal;
window.previousMusing = previousMusing;
window.nextMusing = nextMusing;