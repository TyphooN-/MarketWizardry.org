# Portfolio Risk Calculator - MarketWizardry.org

## Overview

The Portfolio Risk Calculator combines VaR (Value at Risk), ATR (Average True Range), and EV (Enterprise Value) analysis for lots-based position sizing. Now you can input just the number of lots and get comprehensive risk analysis using the latest market data.

## Key Features

### 📊 **VaR Portfolio Calculator**
- Calculate 1-day Value at Risk for entire portfolio
- Position-by-position VaR breakdown
- Portfolio VaR percentage
- Automatic lots-to-dollar conversion

### 📈 **ATR Portfolio Calculator**
- Weighted Average True Range analysis
- Daily (D1), Weekly (W1), Monthly (MN1) ATR metrics
- Volatility-ranked position breakdown
- Percentage-based volatility metrics

### 💼 **EV Portfolio Calculator**
- Enterprise Value vs Market Cap analysis
- Portfolio-weighted EV metrics
- Market capitalization breakdown
- Valuation ratio analysis

## Usage

### Quick Demo (Your Current Holdings)
```bash
cd MarketWizardry.org
python3 portfolio_calculator.py demo
```

### Interactive Mode
```bash
cd MarketWizardry.org
python3 portfolio_calculator.py
```

Then enter positions as:
```
💰 Enter position (SYMBOL LOTS): AAPL 100
💰 Enter position (SYMBOL LOTS): TSLA 50
💰 Enter position (SYMBOL LOTS): done
```

### Available Commands in Interactive Mode
- `SYMBOL LOTS` - Add position (e.g., AAPL 10)
- `symbols` - Show available symbols
- `clear` - Clear all positions
- `help` - Show help
- `done` - Calculate portfolio metrics

## Sample Output

```
🎲 PORTFOLIO VaR ANALYSIS
Portfolio Value: $9,158.00
Portfolio VaR (1-day): $644.96
Portfolio VaR %: 7.04%

📊 PORTFOLIO ATR ANALYSIS
Weighted ATR D1 %: 5.007%
Weighted ATR W1 %: 12.012%
Weighted ATR MN1 %: 36.327%

💼 PORTFOLIO EV ANALYSIS
Portfolio MCap/EV Ratio: 62.72%
Weighted Market Cap: $9,158
Weighted Enterprise Value: $14,602
```

## Data Sources

The calculator automatically uses the **latest** CSV files from:
- `var-explorer/` - VaR data and pricing
- `atr-explorer/` - Average True Range data
- `ev-explorer/` - Enterprise Value data

## Key Changes from Original

1. **Lots-Based Input**: Enter number of lots instead of dollar amounts
2. **Automatic Latest Data**: Always uses most recent CSV files
3. **Three Risk Metrics**: VaR, ATR, and EV in one tool
4. **Position Sizing**: Automatic conversion from lots to portfolio value
5. **Risk Ranking**: Positions sorted by risk metrics

## Risk Interpretation

- **VaR %**: Daily loss expectation (higher = riskier)
- **ATR D1 %**: Daily volatility (higher = more volatile)
- **MCap/EV %**: Valuation metric (>100% = premium, <100% = discount)

## Technical Notes

- 1 lot = 1 share for simplicity
- Uses semicolon-delimited CSV format
- Handles UTF-8 encoding issues automatically
- Supports CFD, Stocks, and Futures data