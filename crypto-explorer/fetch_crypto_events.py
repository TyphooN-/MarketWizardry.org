#!/usr/bin/env python3
"""
Fetch cryptocurrency upcoming events from CoinMarketCal API.
Only fetches events for cryptocurrencies listed in Darwinex reports.
"""

import requests
import json
import time
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional

# CoinMarketCal API endpoint
COINMARKETCAL_API_BASE = "https://developers.coinmarketcal.com/v1"

# Mapping of Darwinex symbols to CoinMarketCal coin names
# CoinMarketCal uses coin names, not symbols
SYMBOL_TO_COIN_NAME = {
    'BTCUSD': 'bitcoin',
    'ETHUSD': 'ethereum',
    'ADAUSD': 'cardano',
    'SOLUSD': 'solana',
    'DOGEUSD': 'dogecoin',
    'DOTUSD': 'polkadot',
    'MATICUSD': 'polygon',  # MATIC is now Polygon
    'UNIUSD': 'uniswap',
    'LTCUSD': 'litecoin',
    'LINKUSD': 'chainlink',
    'XLMUSD': 'stellar',
    'TRXUSD': 'tron',
    'AVAXUSD': 'avalanche',
    'XRPUSD': 'xrp',
    'BNBUSD': 'binance-coin',
    'BCHUSD': 'bitcoin-cash',
    'ETCUSD': 'ethereum-classic',
}


def fetch_events_for_coins(coin_names: List[str], api_key: str, max_events: int = 10) -> Optional[List[Dict]]:
    """
    Fetch upcoming events for specific coins from CoinMarketCal.

    Args:
        coin_names: List of coin names (e.g., ['bitcoin', 'ethereum'])
        api_key: CoinMarketCal API key
        max_events: Maximum number of events to fetch per request

    Returns:
        List of event dictionaries or None if failed
    """
    url = f"{COINMARKETCAL_API_BASE}/events"

    # Join coin names with comma
    coins_param = ','.join(coin_names)

    params = {
        'coins': coins_param,
        'max': max_events,
        'showOnly': 'hot_events'  # Only show important events
    }

    headers = {
        'x-api-key': api_key,
        'Accept': 'application/json',
        'Accept-Encoding': 'deflate, gzip'
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        # CoinMarketCal returns data in 'body' field
        if 'body' in data:
            return data['body']
        else:
            print(f"Unexpected API response format: {list(data.keys())}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text[:200]}")
        return None


def fetch_events_for_symbols(symbols: List[str], api_key: str, events_per_coin: int = 5) -> Dict[str, List[Dict]]:
    """
    Fetch events for multiple cryptocurrency symbols.
    Processes in batches to respect API limits.

    Args:
        symbols: List of trading symbols (e.g., ['BTCUSD', 'ETHUSD'])
        api_key: CoinMarketCal API key
        events_per_coin: Number of events to fetch per coin

    Returns:
        Dictionary mapping symbols to their upcoming events
    """
    all_events = {}

    # Get coin names for our symbols
    coin_names = []
    symbol_to_name_map = {}

    for symbol in symbols:
        coin_name = SYMBOL_TO_COIN_NAME.get(symbol)
        if coin_name:
            coin_names.append(coin_name)
            symbol_to_name_map[coin_name] = symbol

    if not coin_names:
        print("No valid symbols found")
        return {}

    print(f"Fetching events for coins: {', '.join(coin_names)}")

    # Fetch events in batches of 5 coins to avoid overwhelming the API
    batch_size = 5
    for i in range(0, len(coin_names), batch_size):
        batch = coin_names[i:i+batch_size]
        print(f"Fetching batch {i//batch_size + 1}: {', '.join(batch)}")

        events = fetch_events_for_coins(batch, api_key, max_events=50)

        if events:
            print(f"  Retrieved {len(events)} total events")

            # Organize events by coin
            for event in events:
                # Get coins associated with this event
                event_coins = event.get('coins', [])

                for event_coin in event_coins:
                    coin_name = event_coin.get('name', '').lower()

                    # Map back to our symbol
                    if coin_name in symbol_to_name_map:
                        symbol = symbol_to_name_map[coin_name]

                        if symbol not in all_events:
                            all_events[symbol] = []

                        # Only add if we haven't reached the limit
                        if len(all_events[symbol]) < events_per_coin:
                            all_events[symbol].append(event)
        else:
            print(f"  No events retrieved for batch")

        # Rate limiting - be nice to the API
        if i + batch_size < len(coin_names):
            time.sleep(0.5)

    # Sort events by date for each symbol
    for symbol in all_events:
        all_events[symbol] = sorted(
            all_events[symbol],
            key=lambda x: x.get('date_event', ''),
            reverse=False  # Oldest first (upcoming events)
        )[:events_per_coin]
        print(f"{symbol}: {len(all_events[symbol])} events")

    return all_events


def save_events_data(data: Dict[str, List[Dict]], output_file: str):
    """
    Save cryptocurrency events to JSON file.

    Args:
        data: Dictionary of cryptocurrency events
        output_file: Output JSON filename
    """
    # Add metadata
    output_data = {
        'fetch_timestamp': datetime.now().isoformat(),
        'total_symbols': len(data),
        'events': data
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"\nEvents data saved to {output_file}")


def print_summary(data: Dict[str, List[Dict]]):
    """Print summary of fetched events."""
    print(f"\n{'='*80}")
    print(f"CRYPTO EVENTS FETCH SUMMARY")
    print(f"{'='*80}")
    print(f"Total symbols: {len(data)}")
    print(f"Timestamp: {datetime.now()}")
    print()

    for symbol, events in sorted(data.items()):
        print(f"{symbol}: {len(events)} upcoming events")
        for i, event in enumerate(events, 1):
            event_date = event.get('date_event', 'N/A')
            title = event.get('title', {}).get('en', 'N/A')
            print(f"  {i}. {title[:60]}... ({event_date})")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Fetch cryptocurrency upcoming events from CoinMarketCal API'
    )
    parser.add_argument(
        '--output',
        default='crypto_events_data.json',
        help='Output JSON file (default: crypto_events_data.json)'
    )
    parser.add_argument(
        '--symbols',
        nargs='+',
        help='Specific symbols to fetch events for (default: all mapped symbols)'
    )
    parser.add_argument(
        '--events',
        type=int,
        default=5,
        help='Number of events per symbol (default: 5)'
    )
    parser.add_argument(
        '--api-key',
        help='CoinMarketCal API key (can also use COINMARKETCAL_API_KEY env var)'
    )

    args = parser.parse_args()

    # Get API key from argument or environment variable
    api_key = args.api_key or os.environ.get('COINMARKETCAL_API_KEY')

    if not api_key:
        print("ERROR: CoinMarketCal API key required!")
        print("Provide via --api-key argument or COINMARKETCAL_API_KEY environment variable")
        print("\nTo get an API key:")
        print("1. Sign up at https://coinmarketcal.com/en/developer/register")
        print("2. Copy your API key from the dashboard")
        print("3. Set it as an environment variable: export COINMARKETCAL_API_KEY='your-key-here'")
        return 1

    # Determine which symbols to fetch
    symbols = args.symbols if args.symbols else list(SYMBOL_TO_COIN_NAME.keys())

    print(f"Fetching events for {len(symbols)} cryptocurrencies...")
    print(f"Events per symbol: {args.events}\n")

    # Fetch events
    events_data = fetch_events_for_symbols(symbols, api_key, args.events)

    # Save to file
    if events_data:
        save_events_data(events_data, args.output)
        print_summary(events_data)
    else:
        print("No events data fetched!")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
