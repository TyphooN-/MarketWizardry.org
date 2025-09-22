console.log('Script loaded successfully');
let activeCalculator = null;

window.selectCalculator = function(calculatorType, clickedElement) {
    console.log('selectCalculator function called with:', calculatorType);
    try {
        // Hide all calculators
        const calculators = document.querySelectorAll('.calculator-content');
        // Hide calculators
        calculators.forEach(calc => calc.classList.remove('active'));
        // Remove active class from all cards
        const cards = document.querySelectorAll('.calculator-card');
        // Remove active classes
        cards.forEach(card => card.classList.remove('active'));
        // Show selected calculator
        const targetId = calculatorType + '-calculator';
        // Show selected calculator
        const targetElement = document.getElementById(targetId);
        // Found target element
        if (targetElement) {
            targetElement.classList.add('active');
            // Added active class
        } else {
            console.error('Could not find element with ID:', targetId);
        }
    } catch (error) {
        console.error('Error in selectCalculator:', error);
    }
    // Add active class to selected card
    if (clickedElement) {
        clickedElement.classList.add('active');
    }
    activeCalculator = calculatorType;
    // Show breadcrumb
    document.getElementById('active-calculator-breadcrumb').style.display = 'inline';
    document.getElementById('active-calculator-name').textContent =
        clickedElement ? clickedElement.querySelector('h2').textContent : calculatorType;
    // Hide grid and show calculator
    document.querySelector('.calculator-grid').style.display = 'none';
    // Scroll to calculator
    setTimeout(() => {
        const calculator = document.getElementById(calculatorType + '-calculator');
        if (calculator) {
            calculator.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }, 100);
};

function resetToCalculatorSelection() {
    console.log('Resetting to calculator selection');
    // Show calculator grid
    document.querySelector('.calculator-grid').style.display = 'grid';
    // Hide all calculators
    const calculators = document.querySelectorAll('.calculator-content');
    calculators.forEach(calc => calc.classList.remove('active'));
    // Remove active class from all cards
    const cards = document.querySelectorAll('.calculator-card');
    cards.forEach(card => card.classList.remove('active'));
    // Hide breadcrumb active calculator
    document.getElementById('active-calculator-breadcrumb').style.display = 'none';
    // Reset active calculator
    activeCalculator = null;
    // Scroll to top to show calculator selection
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Calculator functionality placeholder functions
function calculateStopLoss() {
    console.log('calculateStopLoss called');
    // Implementation would go here
}

function calculateEnhancedPositionSize() {
    console.log('calculateEnhancedPositionSize called');
    // Implementation would go here
}

function calculatePortfolioVaR() {
    console.log('calculatePortfolioVaR called');
    // Implementation would go here
}

function calculateCompoundInterest() {
    console.log('calculateCompoundInterest called');
    // Implementation would go here
}

// Initialize calculator functionality
function initializeCalculator() {
    console.log('initializeCalculator called');
    const debugOutput = document.getElementById('debugOutput');
    function addDebug(message) {
        console.log(message);
        if (debugOutput) {
            debugOutput.innerHTML += '<br>' + message;
        }
    }
    addDebug('initializeCalculator called');
    try {
        addDebug('Basic test - trying minimal functionality');

        // Set up calculator card click listeners
        addDebug('Setting up calculator card listeners...');
        const calculatorCards = document.querySelectorAll('.calculator-card[data-calculator]');
        addDebug(`Found ${calculatorCards.length} calculator cards`);
        calculatorCards.forEach((card, index) => {
            const calculatorType = card.getAttribute('data-calculator');
            addDebug(`Setting up card ${index}: ${calculatorType}`);
            card.addEventListener('click', function() {
                const clickedType = this.getAttribute('data-calculator');
                addDebug(`✓ Calculator card clicked: ${clickedType}`);
                console.log('Calculator card clicked:', clickedType);
                selectCalculator(clickedType, this);
            });
        });
        addDebug('Calculator card listeners enabled');
        console.log('selectCalculator function exists:', typeof window.selectCalculator);

        // Set up breadcrumb reset listener
        const breadcrumbReset = document.getElementById('calculator-breadcrumb-reset');
        if (breadcrumbReset) {
            breadcrumbReset.addEventListener('click', function(e) {
                e.preventDefault();
                resetToCalculatorSelection();
                return false;
            });
        }
        console.log('Calculator initialization complete');
    } catch (error) {
        console.error('Error in initializeCalculator:', error);
    }
}

// Try multiple initialization approaches
document.addEventListener('DOMContentLoaded', initializeCalculator);
// Fallback for SES extension blocking DOMContentLoaded
setTimeout(function() {
    console.log('Timeout fallback initialization');
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        initializeCalculator();
    }
}, 100);
// Another fallback
if (document.readyState === 'loading') {
    console.log('Document still loading, waiting...');
} else {
    console.log('Document ready, initializing immediately');
    initializeCalculator();
}