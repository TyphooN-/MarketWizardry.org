# Update Tools Changelog

## 2025-10-01: Fixed Mass Regeneration Issue

### Problem
When using `--force` flag, `update_all_tools.py` would regenerate ALL historical outlier files (hundreds of files) instead of just the current date's files. This happened because:

1. `run_outlier_analysis.sh` processes ALL CSV files in the directory when `--overwrite` is passed
2. The script doesn't have date filtering - it uses `find . -name '*.csv'`
3. This caused 300+ files to be regenerated unnecessarily

### Root Cause
```python
# OLD CODE (PROBLEMATIC)
cmd = ['bash', 'run_outlier_analysis.sh']
if self.force_regenerate:
    cmd.append('--overwrite')  # This regenerates EVERYTHING
```

The shell script would then run:
```bash
find . -maxdepth 1 -type f -name '*.csv' | xargs ...  # ALL CSV files!
```

### Solution
Changed to process ONLY current date's files directly in Python:

```python
# NEW CODE (FIXED)
# Find CSV files for the current date only
csv_files = [f for f in os.listdir('var-explorer')
            if f.endswith('.csv') and self.date_str in f]

# Process each CSV file individually
for csv_file in csv_files:
    result = subprocess.run(
        ['python3', 'outlier.py', csv_file],
        cwd='var-explorer',
        capture_output=True,
        text=True
    )
    # Save output...
```

### Changes Made

1. **`process_var_data()`** - Updated to only process current date's CSV files
   - Filters by `self.date_str in filename`
   - Calls `outlier.py` directly instead of shell script
   - Only regenerates files for specified date

2. **`process_atr_data()`** - Same fix applied
   - Filters by `self.date_str in filename`
   - Direct Python invocation
   - Date-scoped regeneration

3. **Removed dependency on `run_outlier_analysis.sh`** for date-specific processing
   - Shell script still exists but not used by update_all_tools.py
   - Can still be used manually for bulk processing if needed

### Impact

**Before:**
```
$ python3 update_all_tools.py --force --date 2025.09.30
# Regenerates 300+ historical files (everything in var-explorer/)
# Takes several minutes
# Git shows hundreds of modified files
```

**After:**
```
$ python3 update_all_tools.py --force --date 2025.09.30
# Regenerates ONLY 2025.09.30 files (3 files: CFD, Stocks, Futures)
# Takes seconds
# Git shows only current date files modified
```

### Benefits

✅ **Faster execution** - Only processes necessary files
✅ **Safer** - Won't accidentally regenerate historical data
✅ **Cleaner git diffs** - Only current date changes
✅ **Predictable** - --force now means "force regenerate current date" not "regenerate everything"

### Testing

Verified fix works correctly:
```bash
# Test 1: Normal run (no force)
python3 update_all_tools.py --date 2025.09.30
# ✅ Skips existing files

# Test 2: Force regenerate current date only
python3 update_all_tools.py --force --date 2025.09.30
# ✅ Only regenerates 2025.09.30 files

# Test 3: Different date
python3 update_all_tools.py --date 2025.10.01
# ✅ Only processes 2025.10.01 files
```

### Notes

- `run_outlier_analysis.sh` still exists and can be used manually
- For bulk historical regeneration, use the shell script directly:
  ```bash
  cd var-explorer
  bash run_outlier_analysis.sh --overwrite
  ```
- This is now separated from the daily update process

### Files Modified

- `update_all_tools.py`
  - `process_var_data()` - Direct Python processing, date-filtered
  - `process_atr_data()` - Direct Python processing, date-filtered

### Migration Notes

No action needed. The fix is backward compatible:
- Existing workflow unchanged
- Only behavior change: --force is now date-scoped (safer)
- Manual bulk processing still available via shell scripts
