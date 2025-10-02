# Crypto Explorer Setup

The crypto explorer provides enhanced analysis by combining Darwinex trading data with cryptocurrency market data from CoinGecko and event data from CoinMarketCal.

## Data Sources

### CoinGecko Market Data (No API Key Required)
Fetches market cap, volume, supply metrics, price changes, and ATH data.

```bash
python3 fetch_crypto_data.py
```

This creates `crypto_market_data.json` with market data for all tracked cryptocurrencies.

### CoinMarketCal Events Data (API Key Required)
Fetches upcoming cryptocurrency events like hard forks, mainnet launches, etc.

#### Getting Your API Key

1. Sign up at https://coinmarketcal.com/en/developer/register
2. Copy your API key from the dashboard
3. Set it as an environment variable:

```bash
export COINMARKETCAL_API_KEY='your-api-key-here'
```

Or add to your `~/.bashrc` or `~/.zshrc` to make it permanent:

```bash
echo "export COINMARKETCAL_API_KEY='your-api-key-here'" >> ~/.bashrc
source ~/.bashrc
```

#### Fetching Events

```bash
# Using environment variable
python3 fetch_crypto_events.py

# Or pass directly via command line
python3 fetch_crypto_events.py --api-key YOUR_API_KEY
```

This creates `crypto_events_data.json` with upcoming events for all tracked cryptocurrencies.

## Running the Enhanced Analysis

Once you've fetched the market and event data, run the enhanced analysis:

```bash
python3 analyze_enhanced.py SymbolsExport-Darwinex-Live-Crypto-2025.10.01.csv \
    --market-data crypto_market_data.json \
    --news-data crypto_news_data.json \
    --events-data crypto_events_data.json
```

The analysis will work without the API key data, but will provide less comprehensive insights.

## Output

The enhanced analysis generates a detailed report including:
- Daily, Weekly, and Monthly volatility rankings
- Market cap rankings and comparisons
- Supply metrics and emission status
- Price performance across multiple timeframes
- Liquidity and trading metrics
- Value at Risk (VaR) analysis
- Latest cryptocurrency news (if available)
- Upcoming events and milestones (if API key is configured)
- Key insights and outliers
