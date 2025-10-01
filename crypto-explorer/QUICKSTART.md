# Crypto Explorer - Quick Start Guide

## One-Command Analysis

```bash
./update_crypto_analysis.sh SymbolsExport-Darwinex-Live-Crypto-2025.09.30.csv
```

This single command will:
1. ✓ Fetch latest market data from CoinGecko (~30-60s)
2. ✓ Merge with your CSV data
3. ✓ Generate comprehensive analysis report

## Output Files

After running, you'll get:

- `*-market-data.json` - Raw market data from CoinGecko
- `*-enhanced-analysis.txt` - Full analysis report (this is what you want!)

## What You Get

### Market Intelligence
- **Market Cap Rankings** - See which coins dominate
- **Supply Metrics** - % minted, circulating vs max supply
- **Price Performance** - 24h/7d changes, distance from ATH
- **Liquidity Analysis** - Volume/MCap ratios, spread costs

### Trading Metrics
- **Volatility Rankings** - ATR/Price ratios (daily/weekly/monthly)
- **VaR Analysis** - Risk-adjusted position sizing
- **Spread Analysis** - Trading cost assessment

### Key Insights
- Most/least volatile pairs
- Supply inflation status (which coins are still heavily inflating)
- Best/worst recent performers
- Liquidity quality indicators

## Example Output Preview

```
MARKET CAP RANKINGS
Rank   Symbol       Market Cap      MCap Rank    Volume 24h
---------------------------------------------------------------
1      BTCUSD       $2.32T          1            $61.07B
2      ETHUSD       $518.34B        2            $40.84B
3      XRPUSD       $147.23B        3            $12.45B

SUPPLY METRICS & EMISSION STATUS
Symbol       % Minted    Circulating        Max Supply         Status
-------------------------------------------------------------------------
BTCUSD       94.90%      19.93M             21.00M             Near Max
DOGEUSD      94.95%      147.73B            155.55B            Near Max
LTCUSD       75.19%      75.73M             100.69M            High
ETHUSD       100.00%     120.70M            N/A                Near Max

PRICE PERFORMANCE
Symbol       24h Change   7d Change    ATH           From ATH
----------------------------------------------------------------
BTCUSD       +3.01%      +3.19%       $124.13K      -6.31%
ETHUSD       +3.34%      +2.64%       $4.95K        -13.39%
SOLUSD       +2.45%      -1.23%       $264.89       -42.15%
```

## Data Sources

### CoinGecko API (Free)
- Market cap, volume, supply metrics
- Price changes and ATH/ATL data
- Community and development metrics
- Liquidity scores

### Your CSV Data
- ATR (Average True Range) - volatility
- VaR (Value at Risk) - position risk
- Spreads - trading costs
- Current prices from your broker

## Common Use Cases

### 1. Daily Market Check
```bash
./update_crypto_analysis.sh latest.csv | grep "24h Change"
```

### 2. Find High Volatility Opportunities
Look for "DAILY VOLATILITY RANKING" section - high ATR/Price means more movement

### 3. Check Supply Inflation Risk
Look for "SUPPLY METRICS" - low % minted = more dilution coming

### 4. Liquidity Analysis
Check "Volume/MCap" ratio - higher = easier to trade without slippage

### 5. Risk Assessment
"VaR RANKING" section shows risk-adjusted position sizes

## Tips

1. **Run before major trading sessions** - Get latest market data
2. **Compare volatility vs liquidity** - High vol + low liquidity = danger zone
3. **Watch supply metrics** - Coins near max supply have less inflation pressure
4. **Monitor ATH distance** - Coins far from ATH may have recovery potential
5. **Check spread costs** - High spread + high volatility = expensive trading

## Troubleshooting

### Script fails to fetch data
```bash
# Check if you can reach CoinGecko
curl -I https://api.coingecko.com/api/v3/ping

# Try with longer delay
python3 fetch_crypto_data.py --delay 2.5
```

### Missing market data for a symbol
Edit `fetch_crypto_data.py` and add to `SYMBOL_TO_COINGECKO_ID` dict.

### Want basic analysis only (no API calls)
```bash
python3 analyze.py your-file.csv > output.txt
```

## Requirements

```bash
pip install requests pandas numpy
```

That's it! Python 3.6+ with three common libraries.

## Questions?

See `README.md` for detailed documentation.
