# API Keys Setup

This guide explains how to securely store API keys for MarketWizardry.org without exposing them to git.

## Quick Setup

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`:**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Get your CoinMarketCal API key:**
   - Sign up at: https://coinmarketcal.com/en/developer/register
   - Copy your API key from the dashboard
   - Paste it in `.env`:
     ```
     COINMARKETCAL_API_KEY=your_actual_key_here
     ```

4. **That's it!** The `.env` file is automatically loaded by `update_all_tools.py`

## How It Works

The `update_all_tools.py` script automatically reads the `.env` file when processing crypto data. You don't need to manually load environment variables - just make sure your `.env` file exists with the correct API key.

## Alternative: Direct Command Line

If you want to run the events script standalone:

```bash
# Method 1: Using environment variable
export COINMARKETCAL_API_KEY="your_key_here"
python3 crypto-explorer/fetch_crypto_events.py

# Method 2: Using command line argument
python3 crypto-explorer/fetch_crypto_events.py --api-key "your_key_here"
```

## Security Notes

✅ **`.env` is in `.gitignore`** - Your keys won't be committed to git
✅ **`.env.example` is tracked** - Shows what keys are needed without exposing secrets
✅ **Automatic loading** - No manual steps required when running `update_all_tools.py`

## Files

- **`.env.example`** - Template file (tracked in git, no secrets)
- **`.env`** - Your actual keys (NOT tracked in git)
- **`.gitignore`** - Prevents `.env` from being committed

## Regenerating Crypto Explorer with Events

Once your API key is set in `.env`:

```bash
# Regenerate all crypto reports with events data
./regenerate_all_crypto.sh
```

Or for a specific date:
```bash
python3 update_all_tools.py 2025.10.03 --force-crypto
```

The script will automatically detect and use your API key from the `.env` file.
