# Darwinex RADAR - Changelog

## [2.0.0] - 2025-10-06

### ✨ New Features

#### 1. **Specification Change Tracking**
- Track changes to symbol specifications across all CSV files
- **TradeMode changes**: Detect when symbols move to close-only or reopen for trading
- **Swap rate changes**: Track SwapLong and SwapShort modifications
- **Spread changes**: Detect significant spread changes (>10% threshold)

#### 2. **Close-Only vs Delisted Distinction**
- **Close-Only symbols**: Now properly tracked as spec changes, NOT delistings
  - Symbol remains in CSV with TradeMode=3
  - Traders can close positions but not open new ones
- **Delisted symbols**: Only count symbols fully removed from CSV
  - Symbol completely removed from platform
  - No longer available for any trading activity

#### 3. **Enhanced Summary Statistics**
Added new metrics to summary section:
- `Total Close-Only Changes`: Count of symbols moved to close-only mode
- `Total Spec Changes`: Total specification modifications detected

### 📊 Output Example

```
Total Symbols Delisted (Fully Removed): 36
Total Close-Only Changes: 26
Total Spec Changes: 87485

⚙️  SPECIFICATION CHANGES (Swap/Commission/Trade Mode)
Note: Close-only does NOT count as delisted. Symbol is still available for closing positions.

📅 2025.07.23 - 5 symbol(s) with spec changes:
   BPMC       → CLOSE-ONLY, Spread: 1.0→4.0
   IGT        → CLOSE-ONLY, Spread: 3.0→14.0
   AAPL       Spread: 9.0→3.0
   MSFT       SwapLong: -6.2→-5.8
```

### 🔧 Technical Improvements

#### Enhanced Data Processing
- New `load_symbol_details()` function to extract TradeMode, swap, and spread data
- Improved `analyze_symbol_changes()` to track spec modifications
- Enhanced `generate_report()` with new sections for spec changes

#### Code Structure
```python
# New tracking dictionaries
close_only_changes = {}  # Symbols moved to close-only
spec_changes = {}        # All specification changes

# TradeMode detection logic
if prev_mode == 4 and curr_mode == 3:
    changes.append('→ CLOSE-ONLY')
elif prev_mode == 3 and curr_mode == 4:
    changes.append('→ TRADING ENABLED')
```

### 📝 Report Sections (New Order)

1. **Summary Statistics** - Overview with new metrics
2. **New Symbols Listed** - Newly added instruments
3. **⚙️ Specification Changes** - Swap/Commission/TradeMode changes *(NEW!)*
4. **❌ Delisted / Fully Removed Symbols** - Only fully removed symbols

### 🎨 CSP Compliance

- ✅ No inline styles
- ✅ No inline scripts
- ✅ No inline event handlers
- ✅ All JavaScript in external files
- ✅ All CSS in shared-styles.css

### 📚 Documentation

- Added comprehensive README.md with usage examples
- Added this CHANGELOG.md to track version history
- Documented TradeMode values (0-4)
- Clear examples of close-only vs delisted

### 🐛 Bug Fixes

- Fixed issue where close-only symbols were incorrectly counted as delistings
- Improved date extraction from filename regex
- Better error handling for missing CSV columns

---

## [1.0.0] - 2025-10-05

### Initial Release

- Basic symbol tracking (new and delisted)
- Multi-asset support (Stocks, Futures, CFD, Crypto)
- Tab-based HTML interface
- Terminal aesthetic output
- CSV-based analysis
