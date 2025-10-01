#!/usr/bin/env python3
"""
Fetch cryptocurrency market data from CoinGecko API.
Collects: market cap, circulating supply, total supply, max supply, volume,
          price change %, all-time high, funding rate, and more.
"""

import requests
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# CoinGecko API endpoints (free tier, no API key needed)
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"

# Mapping of Darwinex symbols to CoinGecko IDs
SYMBOL_TO_COINGECKO_ID = {
    'BTCUSD': 'bitcoin',
    'ETHUSD': 'ethereum',
    'ADAUSD': 'cardano',
    'SOLUSD': 'solana',
    'DOGEUSD': 'dogecoin',
    'DOTUSD': 'polkadot',
    'MATICUSD': 'matic-network',
    'UNIUSD': 'uniswap',
    'LTCUSD': 'litecoin',
    'LINKUSD': 'chainlink',
    'XLMUSD': 'stellar',
    'TRXUSD': 'tron',
    'AVAXUSD': 'avalanche-2',
    'XRPUSD': 'ripple',
    'BNBUSD': 'binancecoin',
    'BCHUSD': 'bitcoin-cash',
    'ETCUSD': 'ethereum-classic',
}


def fetch_coin_data(coin_id: str) -> Optional[Dict]:
    """
    Fetch detailed coin data from CoinGecko API.

    Args:
        coin_id: CoinGecko coin identifier

    Returns:
        Dictionary with coin data or None if failed
    """
    url = f"{COINGECKO_API_BASE}/coins/{coin_id}"
    params = {
        'localization': 'false',
        'tickers': 'false',
        'community_data': 'true',
        'developer_data': 'true',
        'sparkline': 'false'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {coin_id}: {e}")
        return None


def extract_relevant_data(coin_data: Dict, symbol: str) -> Dict:
    """
    Extract relevant cryptocurrency metrics from CoinGecko response.

    Args:
        coin_data: Raw API response from CoinGecko
        symbol: Trading symbol (e.g., BTCUSD)

    Returns:
        Dictionary with processed metrics
    """
    if not coin_data:
        return {}

    market_data = coin_data.get('market_data', {})

    # Extract key metrics
    data = {
        'symbol': symbol,
        'name': coin_data.get('name', 'N/A'),
        'ticker': coin_data.get('symbol', 'N/A').upper(),

        # Market metrics
        'market_cap_usd': market_data.get('market_cap', {}).get('usd'),
        'market_cap_rank': coin_data.get('market_cap_rank'),
        'total_volume_24h': market_data.get('total_volume', {}).get('usd'),
        'current_price': market_data.get('current_price', {}).get('usd'),

        # Supply metrics
        'circulating_supply': market_data.get('circulating_supply'),
        'total_supply': market_data.get('total_supply'),
        'max_supply': market_data.get('max_supply'),
        'percent_minted': None,  # Calculate below

        # Price changes
        'price_change_24h_percent': market_data.get('price_change_percentage_24h'),
        'price_change_7d_percent': market_data.get('price_change_percentage_7d'),
        'price_change_30d_percent': market_data.get('price_change_percentage_30d'),
        'price_change_1y_percent': market_data.get('price_change_percentage_1y'),

        # All-time metrics
        'ath_usd': market_data.get('ath', {}).get('usd'),
        'ath_date': market_data.get('ath_date', {}).get('usd'),
        'ath_change_percent': market_data.get('ath_change_percentage', {}).get('usd'),
        'atl_usd': market_data.get('atl', {}).get('usd'),
        'atl_date': market_data.get('atl_date', {}).get('usd'),
        'atl_change_percent': market_data.get('atl_change_percentage', {}).get('usd'),

        # Trading metrics
        'fully_diluted_valuation': market_data.get('fully_diluted_valuation', {}).get('usd'),
        'market_cap_to_fdv_ratio': None,  # Calculate below

        # Community/Development metrics
        'github_commits_4w': coin_data.get('developer_data', {}).get('commit_count_4_weeks'),
        'github_stars': coin_data.get('developer_data', {}).get('stars'),
        'github_forks': coin_data.get('developer_data', {}).get('forks'),
        'reddit_subscribers': coin_data.get('community_data', {}).get('reddit_subscribers'),
        'twitter_followers': coin_data.get('community_data', {}).get('twitter_followers'),

        # Liquidity score (CoinGecko proprietary)
        'liquidity_score': coin_data.get('liquidity_score'),
        'public_interest_score': coin_data.get('public_interest_score'),

        # Date fetched
        'last_updated': market_data.get('last_updated'),
        'data_fetch_timestamp': datetime.now().isoformat(),
    }

    # Calculate percent minted
    if data['circulating_supply'] and data['max_supply']:
        data['percent_minted'] = (data['circulating_supply'] / data['max_supply']) * 100
    elif data['circulating_supply'] and data['total_supply']:
        # Use total supply as approximation if max supply not available
        data['percent_minted'] = (data['circulating_supply'] / data['total_supply']) * 100

    # Calculate market cap to FDV ratio
    if data['market_cap_usd'] and data['fully_diluted_valuation']:
        data['market_cap_to_fdv_ratio'] = data['market_cap_usd'] / data['fully_diluted_valuation']

    return data


def fetch_all_crypto_data(symbols: List[str], rate_limit_delay: float = 1.5) -> Dict[str, Dict]:
    """
    Fetch data for all cryptocurrency symbols.

    Args:
        symbols: List of trading symbols (e.g., ['BTCUSD', 'ETHUSD'])
        rate_limit_delay: Delay between API calls to respect rate limits

    Returns:
        Dictionary mapping symbols to their data
    """
    all_data = {}

    for symbol in symbols:
        coin_id = SYMBOL_TO_COINGECKO_ID.get(symbol)
        if not coin_id:
            print(f"Warning: No CoinGecko ID mapping for {symbol}")
            continue

        print(f"Fetching data for {symbol} ({coin_id})...")
        coin_data = fetch_coin_data(coin_id)

        if coin_data:
            all_data[symbol] = extract_relevant_data(coin_data, symbol)
            print(f"  ✓ Successfully fetched {symbol}")
        else:
            print(f"  ✗ Failed to fetch {symbol}")

        # Rate limiting - CoinGecko free tier: 10-30 calls/minute
        time.sleep(rate_limit_delay)

    return all_data


def save_crypto_data(data: Dict[str, Dict], output_file: str):
    """
    Save cryptocurrency data to JSON file.

    Args:
        data: Dictionary of cryptocurrency data
        output_file: Output JSON filename
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nData saved to {output_file}")


def print_summary(data: Dict[str, Dict]):
    """Print summary statistics of fetched data."""
    print(f"\n{'='*60}")
    print(f"CRYPTO DATA FETCH SUMMARY")
    print(f"{'='*60}")
    print(f"Total symbols fetched: {len(data)}")
    print(f"Timestamp: {datetime.now()}")
    print(f"\nTop 5 by Market Cap:")

    # Sort by market cap
    sorted_data = sorted(
        [(symbol, info) for symbol, info in data.items() if info.get('market_cap_usd')],
        key=lambda x: x[1]['market_cap_usd'],
        reverse=True
    )

    for i, (symbol, info) in enumerate(sorted_data[:5], 1):
        mc = info['market_cap_usd']
        rank = info.get('market_cap_rank', 'N/A')
        print(f"{i}. {info['name']} ({symbol}): ${mc:,.0f} (Rank: {rank})")

    print(f"\nTop 5 by 24h Volume:")
    sorted_vol = sorted(
        [(symbol, info) for symbol, info in data.items() if info.get('total_volume_24h')],
        key=lambda x: x[1]['total_volume_24h'],
        reverse=True
    )

    for i, (symbol, info) in enumerate(sorted_vol[:5], 1):
        vol = info['total_volume_24h']
        print(f"{i}. {info['name']} ({symbol}): ${vol:,.0f}")


def main():
    parser = argparse.ArgumentParser(
        description='Fetch cryptocurrency market data from CoinGecko API'
    )
    parser.add_argument(
        '--output',
        default='crypto_market_data.json',
        help='Output JSON file (default: crypto_market_data.json)'
    )
    parser.add_argument(
        '--symbols',
        nargs='+',
        help='Specific symbols to fetch (default: all mapped symbols)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.5,
        help='Delay between API calls in seconds (default: 1.5)'
    )

    args = parser.parse_args()

    # Determine which symbols to fetch
    symbols = args.symbols if args.symbols else list(SYMBOL_TO_COINGECKO_ID.keys())

    print(f"Fetching data for {len(symbols)} cryptocurrencies...")
    print(f"Rate limit delay: {args.delay} seconds\n")

    # Fetch data
    crypto_data = fetch_all_crypto_data(symbols, args.delay)

    # Save to file
    if crypto_data:
        save_crypto_data(crypto_data, args.output)
        print_summary(crypto_data)
    else:
        print("No data fetched!")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
