/**
 * MarketWizardry.org Calculator - Position Size & Compound Interest
 * Explorer data features sunset - now handled by TyphooN-Terminal
 */


// Global state
window.activeCalculator = null;

// ===== CORE CALCULATOR SELECTION =====
window.selectCalculator = function(calculatorType, clickedElement) {

    try {
        // Hide all calculators
        document.querySelectorAll('.calculator-content')
            .forEach(calc => calc.classList.remove('active'));

        // Remove active class from all cards
        document.querySelectorAll('.calculator-card')
            .forEach(card => card.classList.remove('active'));

        // Show selected calculator
        const targetId = calculatorType + '-calculator';
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.classList.add('active');
        }

        // Add active class to selected card
        if (clickedElement) {
            clickedElement.classList.add('active');
        }

        // Update breadcrumb
        window.updateBreadcrumb(calculatorType);
        window.activeCalculator = calculatorType;

    } catch (error) {
        // Calculator selection failed silently - UI remains unchanged
    }
};

window.updateBreadcrumb = function(calculatorType) {
    const breadcrumbElement = document.getElementById('active-calculator-breadcrumb');
    const nameElement = document.getElementById('active-calculator-name');

    const calculatorNames = {
        'position': '⚖️ Position Size Calculator',
        'compound': '💰 Compound Interest Calculator'
    };

    if (calculatorType && calculatorNames[calculatorType] && nameElement && breadcrumbElement) {
        nameElement.textContent = calculatorNames[calculatorType];
        breadcrumbElement.className = breadcrumbElement.className.replace(' display-none', '');
    } else if (breadcrumbElement) {
        breadcrumbElement.className += ' display-none';
    }
};

// ===== POSITION SIZE CALCULATOR =====
window.calculatePositionSize = function() {

    try {
        const accountSize = parseFloat(document.getElementById('ps-account-size')?.value) || 0;
        const riskPercent = parseFloat(document.getElementById('ps-risk-value')?.value) || 0;
        const entryPrice = parseFloat(document.getElementById('ps-entry-price')?.value) || 0;
        const stopPrice = parseFloat(document.getElementById('ps-stop-loss')?.value) || 0;

        if (!accountSize || !riskPercent || !entryPrice || !stopPrice) {
            alert('Please fill in all required fields: Account Size, Risk Amount, Entry Price, and Stop Loss Price');
            return;
        }

        if (stopPrice >= entryPrice) {
            alert('Stop Loss price must be lower than Entry price for a long position');
            return;
        }

        const riskAmount = accountSize * (riskPercent / 100);
        const riskPerShare = entryPrice - stopPrice;
        const positionSize = Math.floor(riskAmount / riskPerShare);
        const positionValue = positionSize * entryPrice;
        const actualRisk = positionSize * riskPerShare;
        const percentOfAccount = (positionValue / accountSize) * 100;

        const output = `
            <div class="result-section">
                <h4>📊 Position Size Analysis</h4>
                <div class="result-grid">
                    <div class="result-item">
                        <span class="result-label">Position Size:</span>
                        <span class="result-value">${positionSize.toLocaleString()} shares</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Position Value:</span>
                        <span class="result-value">$${positionValue.toLocaleString()} (${percentOfAccount.toFixed(1)}% of account)</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Risk per Share:</span>
                        <span class="result-value">$${riskPerShare.toFixed(2)}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Total Risk:</span>
                        <span class="result-value">$${actualRisk.toFixed(2)} (${(actualRisk/accountSize*100).toFixed(2)}%)</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Entry Price:</span>
                        <span class="result-value">$${entryPrice.toFixed(2)}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Stop Loss Price:</span>
                        <span class="result-value">$${stopPrice.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('ps-output').innerHTML = output;
        document.getElementById('ps-results').classList.add('show');

    } catch (error) {
        alert('Error calculating position size');
    }
};

// ===== COMPOUND INTEREST CALCULATOR =====
window.calculateCompoundInterest = function() {

    try {
        const principal = parseFloat(document.getElementById('ci-principal')?.value) || 0;
        const rate = parseFloat(document.getElementById('ci-rate')?.value) || 0;
        const time = parseInt(document.getElementById('ci-time')?.value) || 0;
        const compound = parseInt(document.getElementById('ci-compound')?.value) || 12;
        const monthly = parseFloat(document.getElementById('ci-monthly')?.value) || 0;

        if (!principal || !rate || !time) {
            alert('Please fill in all required fields');
            return;
        }

        // Calculate final amount with monthly contributions
        let amount;
        if (monthly > 0) {
            // Future value of initial principal
            const fvPrincipal = principal * Math.pow((1 + (rate / 100) / compound), compound * time);
            // Future value of monthly contributions (annuity)
            const monthlyRate = (rate / 100) / 12;
            const months = time * 12;
            const fvContributions = monthly * ((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate);
            amount = fvPrincipal + fvContributions;
        } else {
            amount = principal * Math.pow((1 + (rate / 100) / compound), compound * time);
        }

        const totalContributions = principal + (monthly * 12 * time);
        const interest = amount - totalContributions;

        // Generate wealth checkpoints
        const checkpoints = generateWealthCheckpoints(principal, rate, time, compound, monthly);

        // Generate yearly breakdown
        const yearlyBreakdown = generateYearlyBreakdown(principal, rate, time, compound, monthly);

        const output = `
            <div class="result-section">
                <h4>💰 Compound Interest Results</h4>
                <div class="result-grid">
                    <div class="result-item">
                        <span class="result-label">Initial Investment:</span>
                        <span class="result-value">$${principal.toLocaleString()}</span>
                    </div>
                    ${monthly > 0 ? `
                    <div class="result-item">
                        <span class="result-label">Monthly Contributions:</span>
                        <span class="result-value">$${monthly.toLocaleString()}/mo × ${time * 12} months</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Total Contributions:</span>
                        <span class="result-value">$${totalContributions.toLocaleString()}</span>
                    </div>
                    ` : ''}
                    <div class="result-item">
                        <span class="result-label">Final Amount:</span>
                        <span class="result-value">$${amount.toLocaleString(undefined, {maximumFractionDigits: 2})}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Interest Earned:</span>
                        <span class="result-value">$${interest.toLocaleString(undefined, {maximumFractionDigits: 2})}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Effective Return:</span>
                        <span class="result-value">${((interest / totalContributions) * 100).toFixed(2)}%</span>
                    </div>
                </div>

                ${checkpoints}
                ${yearlyBreakdown}
            </div>
        `;

        document.getElementById('ci-output').innerHTML = output;
        document.getElementById('ci-results').classList.add('show');

        // Update timeline visualization
        updateCompoundTimeline(principal, rate, time, compound, monthly);

    } catch (error) {
        alert('Error calculating compound interest');
    }
};

// Generate wealth checkpoint milestones
function generateWealthCheckpoints(principal, rate, time, compound, monthly) {
    const milestones = [
        { amount: 10000, emoji: '🎯', label: 'First $10K', message: 'The hardest $10K to save' },
        { amount: 25000, emoji: '🌟', label: 'Quarter Hundred', message: 'Solid emergency fund territory' },
        { amount: 50000, emoji: '💎', label: 'Half Century', message: 'Now compounding gets interesting' },
        { amount: 100000, emoji: '🚀', label: 'Six Figures', message: 'The magical first $100K' },
        { amount: 250000, emoji: '👑', label: 'Quarter Million', message: 'Serious wealth building' },
        { amount: 500000, emoji: '🏆', label: 'Half Million', message: 'Early retirement vibes' },
        { amount: 1000000, emoji: '💰', label: 'Millionaire', message: 'Welcome to the club' },
        { amount: 2000000, emoji: '🎰', label: 'Double Millionaire', message: 'Living the dream' },
        { amount: 5000000, emoji: '🏝️', label: 'Five Million', message: 'Private island money' },
        { amount: 10000000, emoji: '🛥️', label: 'Eight Figures', message: 'Yacht club approved' }
    ];

    let checkpointsHTML = '<div class="wealth-checkpoints"><h4 class="checkpoint-title">🎯 Wealth Checkpoints</h4>';
    let foundMilestones = 0;

    for (let year = 1; year <= time; year++) {
        let amount;
        if (monthly > 0) {
            const fvPrincipal = principal * Math.pow((1 + (rate / 100) / compound), compound * year);
            const monthlyRate = (rate / 100) / 12;
            const months = year * 12;
            const fvContributions = monthly * ((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate);
            amount = fvPrincipal + fvContributions;
        } else {
            amount = principal * Math.pow((1 + (rate / 100) / compound), compound * year);
        }

        // Check if we hit any milestones this year
        for (const milestone of milestones) {
            const prevYear = year - 1;
            let prevAmount = 0;

            if (prevYear > 0) {
                if (monthly > 0) {
                    const fvPrincipalPrev = principal * Math.pow((1 + (rate / 100) / compound), compound * prevYear);
                    const monthlyRate = (rate / 100) / 12;
                    const monthsPrev = prevYear * 12;
                    const fvContributionsPrev = monthly * ((Math.pow(1 + monthlyRate, monthsPrev) - 1) / monthlyRate);
                    prevAmount = fvPrincipalPrev + fvContributionsPrev;
                } else {
                    prevAmount = principal * Math.pow((1 + (rate / 100) / compound), compound * prevYear);
                }
            } else {
                prevAmount = principal;
            }

            if (prevAmount < milestone.amount && amount >= milestone.amount) {
                const totalInvested = principal + (monthly * 12 * year);
                checkpointsHTML += `
                    <div class="checkpoint-item">
                        <div class="checkpoint-header">
                            <span class="checkpoint-emoji">${milestone.emoji}</span>
                            <span class="checkpoint-label">${milestone.label}</span>
                            <span class="checkpoint-year">Year ${year}</span>
                        </div>
                        <div class="checkpoint-message">${milestone.message}</div>
                        <div class="checkpoint-stats">
                            Portfolio: $${amount.toLocaleString(undefined, {maximumFractionDigits: 0})}
                            | Invested: $${totalInvested.toLocaleString()}
                            | Gains: $${(amount - totalInvested).toLocaleString(undefined, {maximumFractionDigits: 0})}
                        </div>
                    </div>
                `;
                foundMilestones++;
            }
        }
    }

    if (foundMilestones === 0) {
        checkpointsHTML += '<div class="checkpoint-empty">No major milestones reached in this timeframe. Try increasing your investment period or contribution amount.</div>';
    }

    checkpointsHTML += '</div>';
    return checkpointsHTML;
}

// Generate yearly breakdown table
function generateYearlyBreakdown(principal, rate, time, compound, monthly) {
    let breakdownHTML = '<div class="yearly-breakdown"><h4 class="breakdown-title">📊 Year-by-Year Breakdown</h4><div class="breakdown-table">';

    breakdownHTML += `
        <div class="breakdown-header">
            <div class="breakdown-cell">Year</div>
            <div class="breakdown-cell">Balance</div>
            <div class="breakdown-cell">Contributions</div>
            <div class="breakdown-cell">Interest</div>
            <div class="breakdown-cell">Total Gain</div>
        </div>
    `;

    // Show first 5 years, then every 5 years, then last year
    const yearsToShow = new Set();
    for (let i = 1; i <= Math.min(5, time); i++) yearsToShow.add(i);
    for (let i = 10; i <= time; i += 5) yearsToShow.add(i);
    if (time > 5) yearsToShow.add(time);

    Array.from(yearsToShow).sort((a, b) => a - b).forEach(year => {
        let amount, prevAmount;

        if (monthly > 0) {
            const fvPrincipal = principal * Math.pow((1 + (rate / 100) / compound), compound * year);
            const monthlyRate = (rate / 100) / 12;
            const months = year * 12;
            const fvContributions = monthly * ((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate);
            amount = fvPrincipal + fvContributions;

            if (year > 1) {
                const fvPrincipalPrev = principal * Math.pow((1 + (rate / 100) / compound), compound * (year - 1));
                const monthsPrev = (year - 1) * 12;
                const fvContributionsPrev = monthly * ((Math.pow(1 + monthlyRate, monthsPrev) - 1) / monthlyRate);
                prevAmount = fvPrincipalPrev + fvContributionsPrev;
            } else {
                prevAmount = principal;
            }
        } else {
            amount = principal * Math.pow((1 + (rate / 100) / compound), compound * year);
            prevAmount = year > 1 ? principal * Math.pow((1 + (rate / 100) / compound), compound * (year - 1)) : principal;
        }

        const contributions = principal + (monthly * 12 * year);
        const yearlyContribution = monthly * 12;
        const yearlyInterest = amount - prevAmount - yearlyContribution;
        const totalGain = amount - contributions;

        breakdownHTML += `
            <div class="breakdown-row">
                <div class="breakdown-cell">${year}</div>
                <div class="breakdown-cell">$${amount.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
                <div class="breakdown-cell">$${contributions.toLocaleString()}</div>
                <div class="breakdown-cell">$${yearlyInterest.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
                <div class="breakdown-cell">$${totalGain.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
            </div>
        `;
    });

    breakdownHTML += '</div></div>';
    return breakdownHTML;
}

// Update compound interest timeline visualization
function updateCompoundTimeline(principal, rate, time, compound, monthly) {
    const timeline = document.getElementById('ci-timeline');
    if (!timeline) return;

    let timelineHTML = '';
    const steps = Math.min(time, 20); // Show max 20 data points
    const interval = Math.ceil(time / steps);

    for (let year = interval; year <= time; year += interval) {
        let amount;
        if (monthly > 0) {
            const fvPrincipal = principal * Math.pow((1 + (rate / 100) / compound), compound * year);
            const monthlyRate = (rate / 100) / 12;
            const months = year * 12;
            const fvContributions = monthly * ((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate);
            amount = fvPrincipal + fvContributions;
        } else {
            amount = principal * Math.pow((1 + (rate / 100) / compound), compound * year);
        }

        const contributions = principal + (monthly * 12 * year);
        const gains = amount - contributions;

        timelineHTML += `
            <div class="timeline-item">
                <div class="timeline-year">Year ${year}</div>
                <div class="timeline-bar-container">
                    <div class="timeline-bar timeline-bar-contributions"
                         style="width: ${(contributions / amount * 100)}%"
                         title="Contributions: $${contributions.toLocaleString()}">
                    </div>
                    <div class="timeline-bar timeline-bar-gains"
                         style="width: ${(gains / amount * 100)}%"
                         title="Gains: $${gains.toLocaleString()}">
                    </div>
                </div>
                <div class="timeline-amount">$${amount.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
            </div>
        `;
    }

    timeline.innerHTML = timelineHTML;
    document.getElementById('ci-chart-container')?.classList.add('show');
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {

    // Button event handlers mapping
    const buttonHandlers = {
        'calculate-position-size-btn': () => window.calculatePositionSize(),
        'calculate-compound-interest-btn': () => window.calculateCompoundInterest()
    };

    // Set up button event listeners
    Object.entries(buttonHandlers).forEach(([buttonId, handler]) => {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                try {
                    handler();
                } catch (error) {
                    alert('An error occurred. Please try again.');
                }
            });
        }
    });

    // Set up breadcrumb reset handler
    const breadcrumbReset = document.getElementById('calculator-breadcrumb-reset');
    if (breadcrumbReset) {
        breadcrumbReset.addEventListener('click', function(e) {
            e.preventDefault();

            // Hide all calculators
            document.querySelectorAll('.calculator-content')
                .forEach(calc => calc.classList.remove('active'));

            // Remove active class from all cards
            document.querySelectorAll('.calculator-card')
                .forEach(card => card.classList.remove('active'));

            // Hide breadcrumb
            this.closest('#active-calculator-breadcrumb')?.classList.add('display-none');

            window.activeCalculator = null;
        });
    }

    // Set up Enter key handlers for inputs
    const inputEnterHandlers = {
        'ps-account-size': () => window.calculatePositionSize(),
        'ps-risk-value': () => window.calculatePositionSize(),
        'ps-entry-price': () => window.calculatePositionSize(),
        'ps-stop-loss': () => window.calculatePositionSize(),
        'ci-principal': () => window.calculateCompoundInterest(),
        'ci-rate': () => window.calculateCompoundInterest(),
        'ci-time': () => window.calculateCompoundInterest()
    };

    Object.entries(inputEnterHandlers).forEach(([inputId, handler]) => {
        const input = document.getElementById(inputId);
        if (input) {
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    handler();
                }
            });
        }
    });
});

// Global error handler - prevent uncaught errors from breaking UI
window.addEventListener('error', function(e) {
    // Silently handle errors to maintain UI stability
    // Errors are logged to browser console automatically
});
