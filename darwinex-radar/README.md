# Darwinex RADAR - Symbol Tracker

Comprehensive tracking system for Darwinex symbol changes, spec modifications, and market evolution.

## Features

### 1. **Symbol Tracking**
- **New Symbols Listed**: Tracks when new instruments are added to the platform
- **Delisted Symbols**: Tracks when symbols are **fully removed** from the platform (not just close-only)

### 2. **Specification Changes** ⚙️ **NEW!**
- **Trade Mode Changes**:
  - `→ CLOSE-ONLY`: Symbol changed to close-only mode (TradeMode 3)
  - `→ TRADING ENABLED`: Symbol reopened for trading (TradeMode 4)
- **Swap Changes**: Tracks SwapLong and SwapShort modifications
  - Filters out invalid/garbage values (abs value > 1,000,000)
  - Only shows meaningful swap rate adjustments

**Note**: Spread and price changes are **not tracked** as they fluctuate too frequently and add noise.

**Smart Grouping**: When multiple symbols have identical spec changes, they're automatically grouped together to reduce report length. For example:
- `[815 symbols] SwapLong: -6.6 → -6.2` followed by the symbol list
- Individual symbols with unique changes are listed separately

### 3. **Close-Only vs Delisted** 🔍 **IMPORTANT!**
- **Close-Only**: Symbol still appears in CSV with TradeMode=3. You can close positions but not open new ones.
- **Delisted**: Symbol completely removed from CSV. Platform no longer offers this instrument.

### 4. **Close-Only → Delisted Timeline** ⏱️ **NEW!**
Tracks the lifecycle of symbols that went close-only before being delisted:
- Shows the date a symbol went close-only
- Shows the date it was fully delisted
- Calculates the number of days between these events
- Sorted by shortest to longest timeline

**Example:**
```
IGT        Close-Only: 2025.06.30 → Delisted: 2025.07.01 (1 days)
CHX        Close-Only: 2025.07.16 → Delisted: 2025.07.17 (1 days)
BPMC       Close-Only: 2025.07.10 → Delisted: 2025.07.23 (13 days)
ANSS       Close-Only: 2025.07.16 → Delisted: 2025.08.18 (33 days)
```

This helps identify patterns in how long symbols remain close-only before full delisting.

## Example Output

```
📋 SUMMARY STATISTICS
========================================================================================================================
Symbols on 2024.12.30: 832
Symbols on 2025.10.03: 808
Net Change: -24 symbols (-2.9%)
Total New Symbols Added: 12
Total Symbols Delisted (Fully Removed): 36
Total Close-Only Changes: 26
Total Spec Changes: 3291

⚙️  SPECIFICATION CHANGES (Trade Mode / Swap Rates)
========================================================================================================================
Note: Close-only does NOT count as delisted. Symbol is still available for closing positions.

📅 2025.07.23 - 3 symbol(s) with spec changes:
------------------------------------------------------------------------------------------------------------------------
   BPMC       → CLOSE-ONLY
   IGT        → CLOSE-ONLY
   MSFT       SwapLong: -6.2 → -5.8

📅 2025.07.07 - 815 symbol(s) with spec changes:
------------------------------------------------------------------------------------------------------------------------
   [815 symbols] SwapLong: -6.6 → -6.2
      → A           AA          AAL         AAP         AAPL        AAXJ        ABBV        ABT
      → ACHC        ACM         ACN         ADBE        ADI         ADM         ADP         ADSK
      ... (grouped for identical changes)

❌ DELISTED / FULLY REMOVED SYMBOLS
========================================================================================================================
Note: These symbols were completely removed from the platform (not just close-only).

📅 2025.07.23 - 1 delisted symbol(s):
------------------------------------------------------------------------------------------------------------------------
   BPMC
```

## Usage

### Generate All Reports

```bash
cd /home/typhoon/git/MarketWizardry.org/darwinex-radar
python3 symbol_tracker.py --all
```

This will:
1. Analyze all CSV files in var-explorer, atr-explorer, crypto-explorer
2. Generate radar reports: `stocks-radar.txt`, `futures-radar.txt`, `cfd-radar.txt`, `crypto-radar.txt`
3. Track new symbols, delisted symbols, and all spec changes

### Generate HTML Page

```bash
python3 generate_radar_html.py
```

This creates the CSP-compliant `darwinex-radar.html` page with tab navigation.

### Analyze Specific Directory

```bash
python3 symbol_tracker.py ../var-explorer output.txt
```

## Data Sources

- **Stocks/ETF**: `var-explorer/SymbolsExport-Darwinex-Live-Stocks-*.csv`
- **Futures**: `atr-explorer/SymbolsExport-Darwinex-Live-Futures-*.csv`
- **CFD**: `atr-explorer/SymbolsExport-Darwinex-Live-CFD-*.csv`
- **Crypto**: `crypto-explorer/SymbolsExport-Darwinex-Live-Crypto-*.csv`

## CSV Format

Required columns:
- `Symbol`: Instrument symbol
- `TradeMode`: Trading mode (3=close-only, 4=full trading)
- `SwapLong`: Long swap rate
- `SwapShort`: Short swap rate
- `Spread`: Spread in points

## TradeMode Values

- **0**: Unknown/Not set
- **1**: Disabled
- **2**: Long only
- **3**: Close only (can only close existing positions)
- **4**: Full trading (can open and close positions)

## Technical Details

- **CSP Compliant**: All generated HTML follows strict Content Security Policy
- **Terminal Aesthetic**: CRT-style green monospace output
- **Performance**: Processes 150+ days of data across 800+ symbols in seconds
- **Change Detection**: Compares consecutive CSV files to detect all changes

## License

Part of MarketWizardry.org - Professional Financial Trading Tools

## Author

TyphooN (@MarketW1zardry)
