# Crypto Explorer Enhanced Analysis

Comprehensive cryptocurrency analysis combining Darwinex trading data with real-time market data from CoinGecko.

## Features

### Data Sources
1. **Darwinex Trading Data** (CSV)
   - ATR (Daily, Weekly, Monthly)
   - VaR calculations
   - Spread metrics
   - Ask/Bid prices

2. **CoinGecko Market Data** (API)
   - Market cap & ranking
   - Trading volume (24h)
   - Circulating/Total/Max supply
   - Price changes (24h, 7d, 30d, 1y)
   - All-time high/low metrics
   - Fully diluted valuation
   - Liquidity scores
   - Community metrics (GitHub, Reddit, Twitter)

### Metrics Collected

#### Supply Metrics
- **Circulating Supply**: Current coins in circulation
- **Max Supply**: Maximum possible supply
- **Percent Minted**: How much of max supply is already minted
- **Emission Status**: Early/Moderate/High/Near Max based on % minted

#### Market Metrics
- **Market Cap**: Total market capitalization
- **Market Cap Rank**: Global ranking by market cap
- **24h Volume**: Trading volume in last 24 hours
- **Volume/MCap Ratio**: Liquidity indicator
- **FDV**: Fully diluted valuation (market cap if all tokens minted)
- **MCap/FDV Ratio**: How close to full dilution

#### Price Performance
- **ATH/ATL**: All-time high/low prices
- **Distance from ATH**: Percentage down from peak
- **24h/7d/30d/1y Changes**: Price performance over time periods

#### Volatility Metrics
- **ATR/Price Ratio**: Normalized volatility measure
- **VaR/Price Ratio**: Risk-adjusted volatility

#### Quality Indicators
- **Liquidity Score**: CoinGecko's proprietary metric
- **GitHub Activity**: Commits, stars, forks (development health)
- **Community Size**: Reddit subscribers, Twitter followers

## Usage

### Quick Start (Automated)

```bash
# Fetch market data and run full analysis in one command
./update_crypto_analysis.sh SymbolsExport-Darwinex-Live-Crypto-2025.09.30.csv
```

This will:
1. Fetch latest data from CoinGecko (~30-60 seconds)
2. Merge with Darwinex CSV data
3. Generate enhanced analysis report

### Manual Usage

#### Step 1: Fetch Market Data

```bash
# Fetch data for all configured cryptocurrencies
python3 fetch_crypto_data.py

# Fetch specific symbols only
python3 fetch_crypto_data.py --symbols BTCUSD ETHUSD SOLUSD

# Custom output file
python3 fetch_crypto_data.py --output my_data.json

# Adjust rate limiting (default: 1.5s between calls)
python3 fetch_crypto_data.py --delay 2.0
```

#### Step 2: Run Enhanced Analysis

```bash
# Basic analysis (Darwinex data only)
python3 analyze_enhanced.py SymbolsExport-Darwinex-Live-Crypto-2025.09.30.csv

# Enhanced analysis with market data
python3 analyze_enhanced.py SymbolsExport-Darwinex-Live-Crypto-2025.09.30.csv \
    --market-data crypto_market_data.json
```

#### Step 3: View Results

```bash
# View the generated analysis
cat SymbolsExport-Darwinex-Live-Crypto-2025.09.30-enhanced-analysis.txt

# Or the basic analysis
cat SymbolsExport-Darwinex-Live-Crypto-2025.09.30-analysis.txt
```

## Output Sections

The enhanced analysis includes:

1. **Market Cap Rankings** - Sorted by market cap with volume
2. **Supply Metrics & Emission Status** - % minted, circulating vs max supply
3. **Daily Volatility Ranking** - ATR/Price ratios
4. **Price Performance** - 24h/7d changes, distance from ATH
5. **Liquidity & Trading Metrics** - Volume/MCap ratios, spread analysis
6. **Value at Risk Rankings** - VaR-based risk assessment
7. **Summary Statistics** - Aggregated metrics across all coins
8. **Key Insights** - Notable highlights and outliers

## CoinGecko API

### Rate Limits
- **Free Tier**: 10-30 calls per minute
- **Default delay**: 1.5 seconds between calls
- Fetching all symbols takes ~30-60 seconds

### Supported Symbols

Currently mapped cryptocurrencies:
- BTC (Bitcoin)
- ETH (Ethereum)
- ADA (Cardano)
- SOL (Solana)
- DOGE (Dogecoin)
- DOT (Polkadot)
- MATIC (Polygon)
- UNI (Uniswap)
- LTC (Litecoin)
- LINK (Chainlink)
- XLM (Stellar)
- TRX (Tron)
- AVAX (Avalanche)
- XRP (Ripple)
- BNB (Binance Coin)
- BCH (Bitcoin Cash)
- ETC (Ethereum Classic)

To add more symbols, edit `SYMBOL_TO_COINGECKO_ID` in `fetch_crypto_data.py`.

## Dependencies

```bash
pip install requests pandas numpy
```

All scripts use only standard libraries plus:
- `requests` - HTTP API calls
- `pandas` - Data manipulation
- `numpy` - Numerical operations

## File Descriptions

- `fetch_crypto_data.py` - Fetches market data from CoinGecko API
- `analyze_enhanced.py` - Enhanced analysis combining all data sources
- `analyze.py` - Basic analysis (Darwinex data only)
- `update_crypto_analysis.sh` - Automated pipeline script
- `crypto_market_data.json` - Cached market data (generated)
- `*-enhanced-analysis.txt` - Enhanced analysis output
- `*-analysis.txt` - Basic analysis output

## Analysis Insights

### Why Percent Minted Matters
- **High % (>95%)**: Supply mostly fixed, less inflation risk
- **Low % (<50%)**: Significant new supply coming, potential selling pressure
- Examples: Bitcoin ~94% minted vs. Ethereum (no max supply)

### Volume/MCap Ratio
- **High ratio (>10%)**: Very liquid, easy to buy/sell
- **Low ratio (<1%)**: Less liquid, larger spreads, slippage risk

### MCap/FDV Ratio
- **Close to 1.0**: Most tokens already released
- **Much less than 1.0**: Large future dilution risk
- Important for understanding true valuation

### Liquidity Score
- CoinGecko's proprietary metric (0-100)
- Considers order book depth, spread, volume
- Higher = better trading conditions

## Troubleshooting

### "No CoinGecko ID mapping for XXXUSD"
Edit `SYMBOL_TO_COINGECKO_ID` in `fetch_crypto_data.py` to add the mapping.

### Rate Limit Errors
Increase the delay: `--delay 2.5`

### API Connection Errors
- Check internet connection
- CoinGecko may be down (check status.coingecko.com)
- Try again later

## Future Enhancements

Potential additions:
- Historical price data and trend analysis
- On-chain metrics (if available)
- Correlation analysis between coins
- Risk-adjusted returns calculation
- Fear & Greed index integration
- Exchange flow data
- Whale wallet tracking
- Network activity metrics (transactions, active addresses)
- Staking/yield metrics
- Token unlock schedules

## Notes

- Market data is cached to avoid repeated API calls
- Run `fetch_crypto_data.py` periodically to update cached data
- CoinGecko data typically updates every 5-10 minutes
- All times are in UTC
- Prices and market caps are in USD

## License

Part of MarketWizardry.org toolkit. Use at your own risk.
