/**
 * MarketWizardry.org Calculator - Optimized Version
 * Clean, maintainable calculator functionality preserving all features
 */

console.log('🚀 MarketWizardry Calculator - Optimized Version Loading...');

// Global state
window.activeCalculator = null;
window.varData = window.varData || null;

// ===== CORE CALCULATOR SELECTION =====
window.selectCalculator = function(calculatorType, clickedElement) {
    console.log('🔄 selectCalculator called with:', calculatorType);

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
            console.log('✅ Calculator activated:', targetId);
        } else {
            console.error('❌ Calculator not found:', targetId);
        }

        // Add active class to selected card
        if (clickedElement) {
            clickedElement.classList.add('active');
        }

        // Update breadcrumb
        window.updateBreadcrumb(calculatorType);
        window.activeCalculator = calculatorType;

    } catch (error) {
        console.error('❌ Error in selectCalculator:', error);
    }
};

window.updateBreadcrumb = function(calculatorType) {
    const breadcrumbElement = document.getElementById('active-calculator-breadcrumb');
    const nameElement = document.getElementById('active-calculator-name');

    const calculatorNames = {
        'stoploss': '🛑 Stop Loss Calculator',
        'position': '⚖️ Position Size Calculator',
        'portfolio': '📊 Portfolio VaR Calculator',
        'lookup': '🔍 Symbol Lookup Tool',
        'compound': '💰 Compound Interest Calculator'
    };

    if (calculatorType && calculatorNames[calculatorType] && nameElement && breadcrumbElement) {
        nameElement.textContent = calculatorNames[calculatorType];
        breadcrumbElement.className = breadcrumbElement.className.replace(' display-none', '');
    } else if (breadcrumbElement) {
        breadcrumbElement.className += ' display-none';
    }
};

// ===== STOP LOSS CALCULATOR =====
window.calculateStopLoss = function() {
    console.log('🛑 calculateStopLoss called');

    try {
        const symbol = document.getElementById('sl-symbol')?.value.toUpperCase().trim() || '';
        const entryPrice = parseFloat(document.getElementById('sl-entry-price')?.value) || 0;
        const accountSize = parseFloat(document.getElementById('sl-account-size')?.value) || 0;
        const riskPercent = parseFloat(document.getElementById('sl-risk-percent')?.value) || 0;

        if (!symbol || !entryPrice || !accountSize || !riskPercent) {
            alert('Please fill in all required fields');
            return;
        }

        const riskAmount = accountSize * (riskPercent / 100);
        let stopLossPrice, stopLossDistance;

        // Use VaR data if available
        if (window.varData && window.varData[symbol]) {
            const data = window.varData[symbol];
            stopLossDistance = data.var;
            stopLossPrice = entryPrice - stopLossDistance;

            const maxShares = Math.floor(riskAmount / stopLossDistance);
            const positionValue = maxShares * entryPrice;

            const output = `
                <div class="result-section">
                    <h4>📊 Stop Loss Analysis for ${symbol}</h4>
                    <div class="result-grid">
                        <div class="result-item">
                            <span class="result-label">Entry Price:</span>
                            <span class="result-value">$${entryPrice.toFixed(2)}</span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Stop Loss Price:</span>
                            <span class="result-value">$${stopLossPrice.toFixed(2)}</span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Risk per Share:</span>
                            <span class="result-value">$${stopLossDistance.toFixed(2)}</span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Maximum Shares:</span>
                            <span class="result-value">${maxShares.toLocaleString()}</span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Position Value:</span>
                            <span class="result-value">$${positionValue.toLocaleString()}</span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Risk Amount:</span>
                            <span class="result-value">$${riskAmount.toFixed(2)} (${riskPercent}%)</span>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('sl-output').innerHTML = output;
        } else {
            // Fallback calculation
            const estimatedRisk = entryPrice * 0.02; // 2% estimate
            stopLossPrice = entryPrice - estimatedRisk;
            const maxShares = Math.floor(riskAmount / estimatedRisk);

            const output = `
                <div class="result-section">
                    <h4>⚠️ Estimated Stop Loss for ${symbol}</h4>
                    <p>Using 2% price estimate - real VaR data not available</p>
                    <div class="result-grid">
                        <div class="result-item">
                            <span class="result-label">Stop Loss Price:</span>
                            <span class="result-value">$${stopLossPrice.toFixed(2)}</span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Maximum Shares:</span>
                            <span class="result-value">${maxShares.toLocaleString()}</span>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('sl-output').innerHTML = output;
        }

        // Show results
        document.getElementById('sl-results').classList.add('show');

    } catch (error) {
        console.error('❌ Error in calculateStopLoss:', error);
        alert('Error calculating stop loss');
    }
};

window.autoFillStopLossData = function() {
    const symbol = document.getElementById('sl-symbol')?.value.toUpperCase().trim();
    if (symbol && window.varData && window.varData[symbol]) {
        const data = window.varData[symbol];
        const priceInput = document.getElementById('sl-entry-price');
        if (priceInput && !priceInput.value) {
            priceInput.value = data.price;
        }
    }
};

// ===== POSITION SIZE CALCULATOR =====
window.calculatePositionSize = function() {
    console.log('⚖️ calculatePositionSize called');

    try {
        const accountSize = parseFloat(document.getElementById('ps-account-size')?.value) || 0;
        const riskPercent = parseFloat(document.getElementById('ps-risk-percent')?.value) || 0;
        const entryPrice = parseFloat(document.getElementById('ps-entry-price')?.value) || 0;
        const stopPrice = parseFloat(document.getElementById('ps-stop-price')?.value) || 0;

        if (!accountSize || !riskPercent || !entryPrice || !stopPrice) {
            alert('Please fill in all required fields');
            return;
        }

        if (stopPrice >= entryPrice) {
            alert('Stop price must be lower than entry price');
            return;
        }

        const riskAmount = accountSize * (riskPercent / 100);
        const riskPerShare = entryPrice - stopPrice;
        const positionSize = Math.floor(riskAmount / riskPerShare);
        const positionValue = positionSize * entryPrice;
        const actualRisk = positionSize * riskPerShare;

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
                        <span class="result-value">$${positionValue.toLocaleString()}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Risk per Share:</span>
                        <span class="result-value">$${riskPerShare.toFixed(2)}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Total Risk:</span>
                        <span class="result-value">$${actualRisk.toFixed(2)} (${(actualRisk/accountSize*100).toFixed(2)}%)</span>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('ps-output').innerHTML = output;
        document.getElementById('ps-results').classList.add('show');

    } catch (error) {
        console.error('❌ Error in calculatePositionSize:', error);
        alert('Error calculating position size');
    }
};

// ===== COMPOUND INTEREST CALCULATOR =====
window.calculateCompoundInterest = function() {
    console.log('💰 calculateCompoundInterest called');

    try {
        const principal = parseFloat(document.getElementById('ci-principal')?.value) || 0;
        const rate = parseFloat(document.getElementById('ci-rate')?.value) || 0;
        const time = parseInt(document.getElementById('ci-time')?.value) || 0;
        const frequency = parseInt(document.getElementById('ci-frequency')?.value) || 1;

        if (!principal || !rate || !time) {
            alert('Please fill in all required fields');
            return;
        }

        const amount = principal * Math.pow((1 + (rate / 100) / frequency), frequency * time);
        const interest = amount - principal;

        const output = `
            <div class="result-section">
                <h4>💰 Compound Interest Results</h4>
                <div class="result-grid">
                    <div class="result-item">
                        <span class="result-label">Principal:</span>
                        <span class="result-value">$${principal.toLocaleString()}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Final Amount:</span>
                        <span class="result-value">$${amount.toLocaleString()}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Interest Earned:</span>
                        <span class="result-value">$${interest.toLocaleString()}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Total Return:</span>
                        <span class="result-value">${((interest / principal) * 100).toFixed(2)}%</span>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('ci-output').innerHTML = output;
        document.getElementById('ci-results').classList.add('show');

    } catch (error) {
        console.error('❌ Error in calculateCompoundInterest:', error);
        alert('Error calculating compound interest');
    }
};

console.log('✅ Core calculators loaded');/**
 * MarketWizardry.org Calculator - Portfolio & Symbol Functions
 * Part 2: Portfolio VaR Calculator and Symbol Lookup functionality
 */

console.log('📊 Loading Portfolio & Symbol functions...');

// ===== PORTFOLIO VaR CALCULATOR =====
window.calculatePortfolioVaR = function() {
    console.log('📊 calculatePortfolioVaR called');

    try {
        const confidence = parseFloat(document.getElementById('pf-confidence')?.value) || 95;
        const timeHorizon = parseInt(document.getElementById('pf-time-horizon')?.value) || 1;
        const rows = document.querySelectorAll('#portfolio-positions tr');

        let positions = [];
        let totalValue = 0;
        let totalVaR = 0;

        // Process each position
        rows.forEach(row => {
            const inputs = row.querySelectorAll('input');
            if (inputs.length >= 3) {
                const symbol = inputs[0].value.toUpperCase().trim();
                const shares = parseFloat(inputs[1].value) || 0;
                const price = parseFloat(inputs[2].value) || 0;

                if (symbol && shares && price) {
                    const value = shares * price;
                    let positionVaR = 0;
                    let hasRealData = false;

                    // Use real VaR data if available
                    if (window.varData && window.varData[symbol]) {
                        const varPerShare = window.varData[symbol].var;
                        positionVaR = shares * varPerShare;
                        hasRealData = true;
                    } else {
                        // 2% estimate for unknown symbols
                        positionVaR = value * 0.02;
                    }

                    positions.push({
                        symbol,
                        shares,
                        price,
                        value,
                        positionVaR,
                        hasRealData,
                        weight: 0 // Will be calculated after totalValue is known
                    });

                    totalValue += value;
                    totalVaR += positionVaR;
                }
            }
        });

        if (positions.length === 0) {
            alert('Please add at least one position');
            return;
        }

        // Calculate weights and confidence adjustment
        positions.forEach(pos => {
            pos.weight = ((pos.value / totalValue) * 100).toFixed(1);
        });

        const confidenceAdjustment = confidence === 99 ? 1.2 : confidence === 95 ? 1.0 : 0.8;
        const adjustedVaR = totalVaR * confidenceAdjustment;
        const timeAdjustedVaR = adjustedVaR * Math.sqrt(timeHorizon);

        // Portfolio risk analysis
        const portfolioRiskAnalysis = window.analyzePortfolioRisk();

        let output = `
            <div class="result-section">
                <h4>📊 Portfolio VaR Analysis</h4>
                <div class="result-grid">
                    <div class="result-item">
                        <span class="result-label">Portfolio Value:</span>
                        <span class="result-value">$${totalValue.toLocaleString()}</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">VaR (${confidence}%, ${timeHorizon}d):</span>
                        <span class="result-value">$${timeAdjustedVaR.toFixed(2)} (${(timeAdjustedVaR/totalValue*100).toFixed(2)}%)</span>
                    </div>
                    <div class="result-item">
                        <span class="result-label">Positions:</span>
                        <span class="result-value">${positions.length}</span>
                    </div>
                </div>
        `;

        // Add portfolio risk analysis if available
        if (portfolioRiskAnalysis) {
            const riskClass = portfolioRiskAnalysis.level || 'low';
            output += `
                <div class="calc-risk-assessment-box risk-${riskClass}">
                    <h4 class="calc-risk-title risk-${riskClass}">🎯 Portfolio Risk Assessment</h4>
                    <div class="calc-risk-message risk-${riskClass}">${portfolioRiskAnalysis.message}</div>
                    <div class="calc-risk-details">
                        High-risk positions: ${portfolioRiskAnalysis.highRiskCount}/${portfolioRiskAnalysis.totalCount}
                        (${((portfolioRiskAnalysis.highRiskCount / portfolioRiskAnalysis.totalCount) * 100).toFixed(1)}%)
                    </div>
                </div>
            `;
        }

        // Position breakdown
        output += `<h4 class="calc-result-title">Position Breakdown:</h4>`;
        positions.forEach(pos => {
            const dataSource = pos.hasRealData ? '📊 Real VaR data' : '⚠️ Estimated (2%)';
            const positionClass = pos.hasRealData ? 'position-real-data' : 'position-estimated-data';

            output += `
                <div class="calc-position-box ${positionClass}">
                    <strong class="calc-position-name">${pos.symbol}</strong> ${dataSource}<br>
                    ${pos.shares.toLocaleString()} shares × $${pos.price} = $${pos.value.toLocaleString()} (${pos.weight}%)<br>
                    Position VaR: $${pos.positionVaR.toFixed(2)}
                </div>
            `;
        });

        output += `</div>`;

        document.getElementById('pf-output').innerHTML = output;
        document.getElementById('pf-results').classList.add('show');

    } catch (error) {
        console.error('❌ Error in calculatePortfolioVaR:', error);
        alert('Error calculating portfolio VaR');
    }
};

window.analyzePortfolioRisk = function() {
    const rows = document.querySelectorAll('#portfolio-positions tr');
    let highRiskPositions = 0;
    let totalPositions = 0;

    rows.forEach(row => {
        const inputs = row.querySelectorAll('input');
        if (inputs.length >= 3) {
            const symbol = inputs[0].value.toUpperCase().trim();

            if (symbol && window.varData && window.varData[symbol]) {
                totalPositions++;
                const data = window.varData[symbol];
                if (data.outliers && data.outliers.length >= 2) {
                    highRiskPositions++;
                }
            }
        }
    });

    if (totalPositions > 0) {
        const riskPercentage = (highRiskPositions / totalPositions) * 100;
        let riskMessage, riskLevel;

        if (riskPercentage > 60) {
            riskMessage = '🚨 EXTREME PORTFOLIO RISK - Multiple high-risk outlier positions detected';
            riskLevel = 'extreme';
        } else if (riskPercentage > 30) {
            riskMessage = '⚠️ ELEVATED PORTFOLIO RISK - Several outlier positions in portfolio';
            riskLevel = 'elevated';
        } else if (riskPercentage > 0) {
            riskMessage = '⚡ MODERATE PORTFOLIO RISK - Some outlier positions detected';
            riskLevel = 'moderate';
        } else {
            riskMessage = '✅ LOW PORTFOLIO RISK - No high-risk outlier positions';
            riskLevel = 'low';
        }

        return {
            message: riskMessage,
            level: riskLevel,
            highRiskCount: highRiskPositions,
            totalCount: totalPositions
        };
    }

    return null;
};

// ===== PORTFOLIO POSITION MANAGEMENT =====
window.addPosition = function() {
    const tbody = document.getElementById('portfolio-positions');
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td><input type="text" placeholder="SYMBOL" class="table-input"></td>
        <td><input type="number" placeholder="100" class="table-input"></td>
        <td><input type="number" placeholder="150.00" step="0.01" class="table-input-price"></td>
        <td class="value-display">-</td>
        <td class="var-display">-</td>
        <td class="var-percent-display">-</td>
        <td class="weight-display">-</td>
        <td class="asset-class-display">-</td>
        <td><button class="remove-btn position-remove-btn" title="Remove Position"></button></td>
    `;
    tbody.appendChild(newRow);
};

window.removePosition = function(button) {
    const row = button.closest('tr');
    const tbody = document.getElementById('portfolio-positions');
    if (tbody.children.length > 1) {
        row.remove();
    }
};

window.addSymbolToPortfolio = function(symbol) {
    console.log('💼 addSymbolToPortfolio called with symbol:', symbol);

    if (!window.varData || !window.varData[symbol]) {
        console.error('❌ Symbol data not found:', symbol);
        alert(`Symbol ${symbol} not found in database`);
        return;
    }

    const data = window.varData[symbol];
    const tbody = document.getElementById('portfolio-positions');

    // Remove placeholder row if it exists
    const placeholderRow = tbody.querySelector('tr input[placeholder="AAPL"]');
    if (placeholderRow) {
        placeholderRow.closest('tr')?.remove();
        console.log('✅ Removed placeholder row');
    }

    // Create new row
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td><input type="text" value="${symbol}" class="table-input"></td>
        <td><input type="number" placeholder="100" class="table-input"></td>
        <td><input type="number" value="${data.price}" step="0.01" class="table-input-price"></td>
        <td class="value-display">-</td>
        <td class="var-display">$${data.var}</td>
        <td class="var-percent-display">-</td>
        <td class="weight-display">-</td>
        <td class="asset-class-display">${data.asset_class || 'Unknown'}</td>
        <td><button class="remove-btn position-remove-btn" title="Remove Position"></button></td>
    `;

    // Insert at the beginning
    if (tbody.children.length > 0) {
        tbody.insertBefore(newRow, tbody.firstChild);
        console.log('✅ Added symbol as first position');
    } else {
        tbody.appendChild(newRow);
        console.log('✅ Added symbol to empty portfolio');
    }

    // Hide symbol info and clear lookup
    const symbolInfo = document.getElementById('symbol-info');
    if (symbolInfo) {
        symbolInfo.className += ' display-none';
    }
    const symbolLookup = document.getElementById('symbol-lookup');
    if (symbolLookup) {
        symbolLookup.value = '';
    }
};

console.log('✅ Portfolio VaR functions loaded');/**
 * MarketWizardry.org Calculator - Symbol Lookup Functions
 * Part 3: Symbol lookup, search, and interaction functionality
 */

console.log('🔍 Loading Symbol lookup functions...');

// ===== SYMBOL LOOKUP FUNCTIONS =====
window.lookupSymbol = function() {
    console.log('🔍 lookupSymbol called');

    const symbolInput = document.getElementById('symbol-lookup');
    if (!symbolInput) {
        console.error('❌ symbol-lookup input not found');
        alert('Error: Symbol input field not found');
        return;
    }

    const symbol = symbolInput.value.toUpperCase().trim();
    if (!symbol) {
        alert('Please enter a symbol');
        return;
    }

    if (window.varData && window.varData[symbol]) {
        displaySymbolInfoInPortfolio(symbol, window.varData[symbol]);
    } else {
        document.getElementById('symbol-details').innerHTML = `
            <div class="calc-error-box">
                Symbol "${symbol}" not found in database.
            </div>
        `;
    }
};

window.lookupSymbolForPositionCalc = function() {
    console.log('🔍 lookupSymbolForPositionCalc called');

    const symbolInput = document.getElementById('ps-symbol');
    if (!symbolInput) {
        console.error('❌ ps-symbol input not found');
        alert('Error: Symbol input field not found');
        return;
    }

    const symbol = symbolInput.value.toUpperCase().trim();
    if (!symbol) {
        alert('Please enter a symbol');
        return;
    }

    if (!window.varData || !window.varData[symbol]) {
        alert(`Symbol "${symbol}" not found in database. Please check the symbol and try again.`);
        return;
    }

    const data = window.varData[symbol];

    // Auto-fill entry price
    const entryPriceInput = document.getElementById('ps-entry-price');
    if (entryPriceInput) {
        entryPriceInput.value = data.price;
    }

    // Auto-fill VaR per share
    const varPerShareInput = document.getElementById('ps-var-per-share');
    if (varPerShareInput) {
        varPerShareInput.value = data.var.toFixed(3);
    }

    // Show success message
    const outputDiv = document.getElementById('ps-output');
    if (outputDiv) {
        outputDiv.innerHTML = `
            <div class="calc-success-box">
                <h4>✅ Symbol Data Loaded: ${symbol}</h4>
                <div class="result-row">
                    <span class="result-label-inline">Description:</span>
                    <span class="result-value">${data.description || symbol}</span>
                </div>
                <div class="result-row">
                    <span class="result-label-inline">Current Price:</span>
                    <span class="result-value">$${data.price}</span>
                </div>
                <div class="result-row">
                    <span class="result-label-inline">VaR (per share):</span>
                    <span class="result-value">$${data.var.toFixed(3)}</span>
                </div>
                <div class="result-row">
                    <span class="result-label-inline">Sector:</span>
                    <span class="result-value">${data.sector || 'Unknown'}</span>
                </div>
                ${data.atr_d1 ? `
                <div class="result-row">
                    <span class="result-label-inline">ATR (Daily):</span>
                    <span class="result-value">$${data.atr_d1.toFixed(3)}</span>
                </div>
                ` : ''}
                <p style="margin-top: 10px; color: #00aa00;">Entry price and VaR have been auto-filled. Adjust values if needed and click Calculate.</p>
            </div>
        `;
    }

    console.log('✅ Symbol data auto-filled:', symbol);
};

function displaySymbolInfoInPortfolio(symbol, data) {
    // Determine which calculator is active to use correct div IDs
    const activeCalc = window.activeCalculator;
    const isLookupTool = activeCalc === 'lookup';

    // Use lookup-specific divs if in lookup tool, otherwise use portfolio divs
    const detailsDiv = document.getElementById(isLookupTool ? 'lookup-symbol-details' : 'symbol-details');

    if (!detailsDiv) {
        console.error('❌ Symbol display div not found');
        return;
    }

    // Generate risk assessment
    const riskAssessment = generateRiskAssessment(data);

    detailsDiv.innerHTML = `
        <div class="symbol-details-card">
            <div class="symbol-header">
                <h3>${symbol}</h3>
                <span class="symbol-price">$${data.price}</span>
            </div>

            <div class="symbol-info-summary">
                <p><strong>${data.description || symbol}</strong></p>
            </div>

            <div class="symbol-metrics">
                <div class="metric-item">
                    <span class="metric-label">Current Price (Ask):</span>
                    <span class="metric-value">$${data.price} USD per share</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">VaR (per share, 1-day, 95%):</span>
                    <span class="metric-value">$${data.var.toFixed(3)} USD</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">VaR/Ask Ratio:</span>
                    <span class="metric-value">${((data.var / data.price) * 100).toFixed(2)}% (risk per dollar invested)</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">VaR (1 lot = 100 shares):</span>
                    <span class="metric-value">$${(data.var * 100).toFixed(2)} USD</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Sector:</span>
                    <span class="metric-value">${data.sector || 'Unknown'}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Industry:</span>
                    <span class="metric-value">${data.industry || 'Unknown'}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Asset Class:</span>
                    <span class="metric-value">${data.asset_class || 'Unknown'}</span>
                </div>
            </div>

            <div class="symbol-metrics" style="margin-top: 15px;">
                <h4 style="color: #00ff00; margin-bottom: 10px;">📊 Average True Range (ATR) - Volatility Metrics</h4>
                ${data.atr_d1 ? `
                <div class="metric-item">
                    <span class="metric-label">ATR (Daily - D1):</span>
                    <span class="metric-value">$${data.atr_d1.toFixed(3)} USD per share</span>
                </div>
                ` : ''}
                ${data.atr_w1 ? `
                <div class="metric-item">
                    <span class="metric-label">ATR (Weekly - W1):</span>
                    <span class="metric-value">$${data.atr_w1.toFixed(3)} USD per share</span>
                </div>
                ` : ''}
                ${data.atr_mn1 ? `
                <div class="metric-item">
                    <span class="metric-label">ATR (Monthly - MN1):</span>
                    <span class="metric-value">$${data.atr_mn1.toFixed(3)} USD per share</span>
                </div>
                ` : ''}
            </div>

            <div class="symbol-metrics" style="margin-top: 15px;">
                ${data.outliers && data.outliers.length > 0 ? `
                <div class="metric-item warning">
                    <span class="metric-label">⚠️ Risk Outliers:</span>
                    <span class="metric-value">${data.outliers.join(', ')}</span>
                </div>
                ` : ''}
            </div>
            ${riskAssessment ? `
            <div class="risk-assessment risk-${riskAssessment.level || 'low'}">
                ${riskAssessment.recommendation}
            </div>
            ` : ''}
            <div class="symbol-actions">
                <button class="symbol-action-btn" data-action="use-in-stop-loss" data-symbol="${symbol}">
                    📊 Use in Stop Loss Calc
                </button>
                <button class="symbol-action-btn" data-action="add-to-portfolio" data-symbol="${symbol}">
                    💼 Add to Portfolio
                </button>
                <button class="symbol-action-btn" data-action="find-similar" data-symbol="${symbol}">
                    🔍 Find Similar
                </button>
            </div>
        </div>
    `;

    // Make result box visible
    const detailsResultBox = detailsDiv.closest('.result-box');
    if (detailsResultBox) detailsResultBox.classList.add('show');
};

function generateRiskAssessment(data) {
    if (!data.outliers || data.outliers.length === 0) {
        return {
            recommendation: '✅ Normal risk profile - no significant outliers detected',
            level: 'low'
        };
    }

    const outlierCount = data.outliers.length;
    if (outlierCount >= 3) {
        return {
            recommendation: '🚨 HIGH RISK - Multiple outliers detected. Exercise extreme caution.',
            level: 'extreme'
        };
    } else if (outlierCount === 2) {
        return {
            recommendation: '⚠️ ELEVATED RISK - Two outliers detected. Monitor closely.',
            level: 'elevated'
        };
    } else {
        return {
            recommendation: '⚡ MODERATE RISK - One outlier detected. Consider carefully.',
            level: 'moderate'
        };
    }
}

// ===== SYMBOL SEARCH FUNCTIONS =====
window.showAllSymbols = function() {
    console.log('🔍 showAllSymbols called');

    if (!window.varData) {
        document.getElementById('lookup-output').innerHTML = `
            <div class="calc-error-box">
                <h4>❌ Data Not Loaded</h4>
                <p>VaR data is not yet available. Please try again in a moment.</p>
            </div>
        `;
        return;
    }

    const symbols = Object.entries(window.varData);
    const filteredSymbols = symbols.filter(([symbol, data]) => data.asset_class === 'stocks');

    displaySymbolGrid(filteredSymbols, `Filtered Symbols (${filteredSymbols.length} stocks)`);
};

window.showAllSymbolsUnfiltered = function() {
    console.log('🔍 showAllSymbolsUnfiltered called');

    if (!window.varData) {
        document.getElementById('lookup-output').innerHTML = `
            <div class="calc-error-box">
                <h4>❌ Data Not Loaded</h4>
                <p>VaR data is not yet available. Please try again in a moment.</p>
            </div>
        `;
        return;
    }

    const symbols = Object.entries(window.varData);
    displaySymbolGrid(symbols, `All Symbols (${symbols.length} total)`);
};

window.performAdvancedSearch = function() {
    console.log('🔍 performAdvancedSearch called');

    const searchInput = document.getElementById('lookup-symbol');
    if (!searchInput) {
        console.error('❌ lookup-symbol input not found');
        return;
    }

    const query = searchInput.value.trim().toUpperCase();
    if (!query) {
        alert('Please enter a search term');
        return;
    }

    if (!window.varData) {
        document.getElementById('lookup-output').innerHTML = `
            <div class="calc-error-box">
                <h4>❌ Data Not Loaded</h4>
                <p>VaR data is not yet available. Please try again in a moment.</p>
            </div>
        `;
        return;
    }

    let results = [];

    // Handle sector search
    if (query.startsWith('SECTOR:')) {
        const sector = query.replace('SECTOR:', '').trim();
        results = Object.entries(window.varData).filter(([symbol, data]) =>
            data.sector && data.sector.toUpperCase().includes(sector)
        );
    }
    // Handle wildcard search
    else if (query.includes('*')) {
        const pattern = query.replace(/\*/g, '.*');
        const regex = new RegExp(`^${pattern}$`);
        results = Object.entries(window.varData).filter(([symbol]) => regex.test(symbol));
    }
    // Handle exact symbol search
    else {
        results = Object.entries(window.varData).filter(([symbol]) => symbol.includes(query));
    }

    displaySymbolGrid(results, `Search Results (${results.length} found for "${query}")`);
};

function displaySymbolGrid(symbols, title) {
    if (symbols.length === 0) {
        document.getElementById('lookup-output').innerHTML = `
            <div class="calc-error-box">
                <h4>❌ No Results</h4>
                <p>No symbols found matching your criteria.</p>
            </div>
        `;
        return;
    }

    let output = `
        <div class="calc-symbols-container">
            <h3 class="calc-symbols-title">${title}</h3>
            <div class="calc-symbols-grid">
    `;

    symbols.forEach(([symbol, data]) => {
        const riskClass = data.outliers && data.outliers.length >= 2 ? 'high-risk' : 'normal-risk';
        const outlierInfo = data.outliers && data.outliers.length > 0
            ? ` 🚨 ${data.outliers.length} outlier${data.outliers.length > 1 ? 's' : ''}`
            : '';

        output += `
            <div class="calc-symbol-item quick-lookup ${riskClass}" data-symbol="${symbol}" data-action="show-symbol-detail">
                <strong>${symbol}</strong><br>
                <small>$${data.price} | VaR: $${data.var.toFixed(3)}</small><br>
                <small class="calc-symbol-desc">${(data.description || '').length > 25
                    ? (data.description || '').substring(0, 25) + '...'
                    : (data.description || '')}</small>
                ${outlierInfo ? `<small class="outlier-warning">${outlierInfo}</small>` : ''}
            </div>
        `;
    });

    output += `</div></div>`;
    document.getElementById('lookup-output').innerHTML = output;

    // Make results visible
    const resultsElement = document.getElementById('lookup-results');
    if (resultsElement) {
        resultsElement.classList.add('show');
    }
}

// ===== SYMBOL INTERACTION FUNCTIONS =====
window.showSymbolDetail = function(symbol) {
    console.log('🎯 showSymbolDetail called for symbol:', symbol);

    if (!window.varData || !window.varData[symbol]) {
        console.error('❌ Symbol data not found:', symbol);
        return;
    }

    displaySymbolInfoInPortfolio(symbol, window.varData[symbol]);
};

window.useInStopLoss = function(symbol) {
    console.log('📊 useInStopLoss called for symbol:', symbol);

    if (!symbol) {
        console.error('❌ No symbol provided');
        alert('Error: No symbol provided');
        return;
    }

    if (window.selectCalculator) {
        window.selectCalculator('stoploss');
        setTimeout(() => {
            const symbolInput = document.getElementById('sl-symbol');
            if (symbolInput) {
                symbolInput.value = symbol;
                window.autoFillStopLossData();
            }
        }, 100);
    }
};

window.useInPortfolio = function(symbol) {
    console.log('💼 useInPortfolio called for symbol:', symbol);

    if (!symbol) {
        console.error('❌ No symbol provided');
        alert('Error: No symbol provided');
        return;
    }

    if (window.addSymbolToPortfolio) {
        window.addSymbolToPortfolio(symbol);
        console.log('✅ Symbol added to portfolio:', symbol);
    }
};

window.findSimilar = function(symbol) {
    console.log('🔍 findSimilar called for symbol:', symbol);

    if (!symbol || !window.varData || !window.varData[symbol]) {
        console.error('❌ Symbol data not found:', symbol);
        return;
    }

    const targetData = window.varData[symbol];
    const targetSector = targetData.sector;

    if (!targetSector) {
        alert('Cannot find similar symbols - sector information not available');
        return;
    }

    const similarSymbols = Object.entries(window.varData).filter(([sym, data]) =>
        sym !== symbol && data.sector === targetSector
    );

    displaySymbolGrid(similarSymbols, `Similar to ${symbol} (${targetSector} sector)`);
};

window.backToSymbolList = function() {
    console.log('🔙 backToSymbolList called');
    window.showAllSymbols();
};

console.log('✅ Symbol lookup functions loaded');/**
 * MarketWizardry.org Calculator - Initialization
 * Part 4: Event handlers and DOM initialization
 */

console.log('🔧 Loading Calculator initialization...');

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Calculator DOM ready - initializing...');

    // Button event handlers mapping
    const buttonHandlers = {
        'calculate-stop-loss-btn': () => window.calculateStopLoss(),
        'calculate-position-size-btn': () => window.calculatePositionSize(),
        'calculate-compound-interest-btn': () => window.calculateCompoundInterest(),
        'calculate-portfolio-var-btn': () => window.calculatePortfolioVaR(),
        'lookup-symbol-btn': () => window.lookupSymbol(),
        'ps-lookup-symbol-btn': () => window.lookupSymbolForPositionCalc(),
        'show-all-symbols-btn': () => window.showAllSymbols(),
        'show-all-symbols-unfiltered-btn': () => window.showAllSymbolsUnfiltered(),
        'advanced-search-btn': () => window.performAdvancedSearch(),
        'add-position-btn': () => window.addPosition()
    };

    // Set up button event listeners
    Object.entries(buttonHandlers).forEach(([buttonId, handler]) => {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                console.log(`🔘 Button clicked: ${buttonId}`);
                try {
                    handler();
                } catch (error) {
                    console.error(`❌ Error in ${buttonId}:`, error);
                    alert('An error occurred. Please try again.');
                }
            });
            console.log(`✅ Event handler attached: ${buttonId}`);
        } else {
            console.warn(`⚠️ Button not found: ${buttonId}`);
        }
    });

    // Set up input change handlers for auto-fill functionality
    const symbolInput = document.getElementById('sl-symbol');
    if (symbolInput) {
        symbolInput.addEventListener('blur', function() {
            if (this.value.trim()) {
                setTimeout(() => window.autoFillStopLossData(), 100);
            }
        });
    }

    // Set up portfolio position removal handlers (delegated)
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-btn') || e.target.classList.contains('position-remove-btn')) {
            e.preventDefault();
            console.log('🗑️ Remove position button clicked');
            window.removePosition(e.target);
            return;
        }

        // Handle data-action elements
        const actionElement = e.target.closest('[data-action]');
        if (actionElement) {
            const action = actionElement.getAttribute('data-action');
            const symbol = actionElement.getAttribute('data-symbol');

            console.log('🔘 Action element clicked:', action, 'symbol:', symbol);

            switch(action) {
                case 'select-calculator':
                    e.preventDefault();
                    const calculatorType = actionElement.getAttribute('data-calculator');
                    if (calculatorType) {
                        console.log('🎯 Selecting calculator:', calculatorType);
                        window.selectCalculator(calculatorType, actionElement);
                    }
                    break;
                case 'show-symbol-detail':
                    if (symbol) {
                        e.preventDefault();
                        console.log('🎯 Showing symbol detail for:', symbol);
                        window.showSymbolDetail(symbol);
                    }
                    break;
                case 'use-in-stop-loss':
                    if (symbol) {
                        e.preventDefault();
                        window.useInStopLoss(symbol);
                    }
                    break;
                case 'add-to-portfolio':
                    if (symbol) {
                        e.preventDefault();
                        window.useInPortfolio(symbol);
                    }
                    break;
                case 'find-similar':
                    if (symbol) {
                        e.preventDefault();
                        window.findSimilar(symbol);
                    }
                    break;
            }
        }
    });

    // Set up breadcrumb reset handler
    const breadcrumbReset = document.getElementById('calculator-breadcrumb-reset');
    if (breadcrumbReset) {
        breadcrumbReset.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('🔄 Breadcrumb reset clicked');

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
        'sl-symbol': () => window.autoFillStopLossData(),
        'sl-entry-price': () => window.calculateStopLoss(),
        'sl-account-size': () => window.calculateStopLoss(),
        'sl-risk-percent': () => window.calculateStopLoss(),
        'ps-account-size': () => window.calculatePositionSize(),
        'ps-risk-percent': () => window.calculatePositionSize(),
        'ps-entry-price': () => window.calculatePositionSize(),
        'ps-stop-price': () => window.calculatePositionSize(),
        'ci-principal': () => window.calculateCompoundInterest(),
        'ci-rate': () => window.calculateCompoundInterest(),
        'ci-time': () => window.calculateCompoundInterest(),
        'symbol-lookup': () => window.lookupSymbol(),
        'lookup-symbol': () => window.performAdvancedSearch()
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

    // Initialize dropdown options
    initializeDropdowns();

    console.log('✅ Calculator initialization complete');

    // Test that all functions are available
    const requiredFunctions = [
        'selectCalculator',
        'calculateStopLoss',
        'calculatePositionSize',
        'calculateCompoundInterest',
        'calculatePortfolioVaR',
        'lookupSymbol',
        'showAllSymbols',
        'addSymbolToPortfolio'
    ];

    const missingFunctions = requiredFunctions.filter(fn => typeof window[fn] !== 'function');
    if (missingFunctions.length > 0) {
        console.error('❌ Missing functions:', missingFunctions);
    } else {
        console.log('✅ All required functions available');
    }
});

// Initialize dropdown options
function initializeDropdowns() {
    // Stop Loss confidence levels
    const slConfidence = document.getElementById('sl-confidence');
    if (slConfidence) {
        const levels = [90, 95, 99];
        levels.forEach(level => {
            const option = document.createElement('option');
            option.value = level;
            option.textContent = level + '%';
            if (level === 95) option.selected = true;
            slConfidence.appendChild(option);
        });
    }

    // Position Size confidence levels
    const psConfidence = document.getElementById('ps-confidence');
    if (psConfidence) {
        const levels = [90, 95, 99];
        levels.forEach(level => {
            const option = document.createElement('option');
            option.value = level;
            option.textContent = level + '%';
            if (level === 95) option.selected = true;
            psConfidence.appendChild(option);
        });
    }

    // Portfolio VaR confidence levels
    const pfConfidence = document.getElementById('pf-confidence');
    if (pfConfidence) {
        const levels = [90, 95, 99];
        levels.forEach(level => {
            const option = document.createElement('option');
            option.value = level;
            option.textContent = level + '%';
            if (level === 95) option.selected = true;
            pfConfidence.appendChild(option);
        });
    }

    // Compound interest frequency
    const ciFrequency = document.getElementById('ci-frequency');
    if (ciFrequency) {
        const frequencies = [
            { value: 1, label: 'Annually' },
            { value: 4, label: 'Quarterly' },
            { value: 12, label: 'Monthly' },
            { value: 365, label: 'Daily' }
        ];
        frequencies.forEach(freq => {
            const option = document.createElement('option');
            option.value = freq.value;
            option.textContent = freq.label;
            if (freq.value === 12) option.selected = true;
            ciFrequency.appendChild(option);
        });
    }

    console.log('✅ Dropdown options initialized');
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('💥 Global error caught:', e.error);
    console.error('File:', e.filename, 'Line:', e.lineno, 'Column:', e.colno);
});

console.log('✅ Calculator initialization script loaded');