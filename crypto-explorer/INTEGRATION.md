# Crypto Explorer - Integration with update_all_tools.py

## Overview

The crypto explorer has been integrated into the automated `update_all_tools.py` pipeline. Market data is now automatically fetched from CoinGecko during the daily update process.

## What Changed

### 1. Automated Data Pipeline

**File**: `update_all_tools.py`

**Method**: `process_crypto_data()`

The crypto processing now includes:

1. **Market Data Fetching** (NEW)
   - Automatically calls `fetch_crypto_data.py`
   - Fetches from CoinGecko API with rate limiting
   - Saves to `*-market-data.json`
   - 3-minute timeout for API calls

2. **Enhanced Analysis** (NEW)
   - Runs `analyze_enhanced.py` with market data
   - Creates `*-enhanced-analysis.txt` with full metrics
   - Includes: market cap, supply metrics, price performance, etc.

3. **Fallback to Basic Analysis**
   - If API fails, falls back to basic `analyze.py`
   - Creates `*-analysis.txt` without market data
   - Ensures analysis always completes

### 2. HTML Generation

**Method**: `generate_crypto_explorer()`

Now scans for both file types:
- Enhanced analysis files (`*-enhanced-analysis.txt`)
- Basic analysis files (`*-analysis.txt`)
- Prefers enhanced when available
- Displays most recent 60 files

### 3. File Scanning

**Method**: `_scan_historical_files()`

Updated to handle multiple patterns:
- `-outlier.txt` (VaR/ATR explorers)
- `-analysis.txt` (Basic crypto)
- `-enhanced-analysis.txt` (Enhanced crypto)

## Usage

### Normal Daily Update

```bash
python3 update_all_tools.py
```

This will:
1. Copy CSV from MetaTrader
2. Fetch CoinGecko market data (~30-60s)
3. Run enhanced crypto analysis
4. Generate crypto-explorer.html

### Force Regenerate

```bash
python3 update_all_tools.py --force
```

Forces regeneration of all files including crypto market data.

### HTML Only Mode

```bash
python3 update_all_tools.py --html-only
```

Skips data fetching, only regenerates HTML from existing analysis files.

## Output Files

For each date (e.g., 2025.09.30):

```
crypto-explorer/
  ├── SymbolsExport-Darwinex-Live-Crypto-2025.09.30.csv
  ├── SymbolsExport-Darwinex-Live-Crypto-2025.09.30-market-data.json  (NEW)
  ├── SymbolsExport-Darwinex-Live-Crypto-2025.09.30-enhanced-analysis.txt  (NEW)
  └── SymbolsExport-Darwinex-Live-Crypto-2025.09.30-analysis.txt  (fallback)
```

## Error Handling

### API Failures

If CoinGecko API fails:
- Logs warning with error details (first 200 chars)
- Falls back to basic analysis
- Processing continues without interruption

### Timeout

If API fetch takes >3 minutes:
- Times out automatically
- Falls back to basic analysis
- Error logged

### No CSV Available

If crypto CSV doesn't exist:
- Logs warning
- Skips crypto processing
- Other explorers still process normally

## Features Summary

✅ **Automated**: No manual intervention needed
✅ **Resilient**: Falls back gracefully on errors
✅ **Comprehensive**: Enhanced analysis when API works
✅ **Fast**: Uses caching, respects rate limits
✅ **Visible**: Clear logging at each step

## Monitoring Output

During `update_all_tools.py` execution, look for:

```
₿ Processing Crypto data...
  📡 Fetching cryptocurrency market data from CoinGecko...
  ✅ Market data fetched successfully
  📊 Running enhanced analysis with market data...
  ✅ Enhanced crypto analysis saved to ...
```

Or if API fails:

```
₿ Processing Crypto data...
  📡 Fetching cryptocurrency market data from CoinGecko...
  ⚠️ Warning: Market data fetch failed, will run basic analysis only
  📊 Running basic crypto analysis...
  ✅ Basic crypto analysis saved to ...
```

## Manual Override

If you want to manually fetch crypto data:

```bash
cd crypto-explorer
./update_crypto_analysis.sh SymbolsExport-Darwinex-Live-Crypto-2025.09.30.csv
```

This bypasses `update_all_tools.py` and runs the crypto pipeline directly.

## Dependencies

All dependencies already included in `update_all_tools.py`:
- `requests` - HTTP calls
- `pandas` - Data processing
- `numpy` - Numerical operations
- `subprocess` - Script execution

No additional packages needed.

## Rate Limiting

CoinGecko free tier limits:
- 10-30 calls per minute
- Default delay: 1.5 seconds between calls
- ~17 symbols = ~30-45 seconds total

The timeout is set to 3 minutes to accommodate:
- Network latency
- API response times
- Rate limiting delays

## Future Enhancements

Potential improvements:
- Cache market data for 24h (avoid daily refetch)
- Add --skip-crypto flag to bypass crypto processing
- Parallel API calls for faster fetching
- Retry logic on API failures
- Market data age validation

## Troubleshooting

### "Market data fetch failed"

Check:
1. Internet connection
2. CoinGecko API status (status.coingecko.com)
3. Rate limiting (too many recent calls)

Solution: Wait a few minutes and re-run.

### "Timeout expired"

API calls took >3 minutes.

Solution: Increase timeout in `update_all_tools.py`:
```python
timeout=300  # 5 minutes instead of 3
```

### Enhanced analysis not showing

Check if `*-enhanced-analysis.txt` exists.

If not, check logs for API fetch errors.

Run manual fetch to test:
```bash
cd crypto-explorer
python3 fetch_crypto_data.py
```

## Integration Testing

To verify integration works:

```bash
# Test with current date
python3 update_all_tools.py

# Check crypto was processed
ls crypto-explorer/*-enhanced-analysis.txt | tail -1

# View the latest enhanced analysis
cat crypto-explorer/*-enhanced-analysis.txt | tail -1 | less
```

## Success Criteria

✅ Enhanced analysis file created
✅ Market data JSON file saved
✅ Crypto explorer HTML updated
✅ Grid shows latest analysis
✅ Modal loads correctly
✅ No errors in console

The integration is complete and production-ready.
