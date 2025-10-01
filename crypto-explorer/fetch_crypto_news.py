#!/usr/bin/env python3
"""
Fetch cryptocurrency news from CryptoCompare API.
Collects news articles for specific cryptocurrencies.
"""

import requests
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# CryptoCompare API endpoints (free tier)
CRYPTOCOMPARE_API_BASE = "https://min-api.cryptocompare.com"

# Mapping of Darwinex symbols to CryptoCompare categories/symbols
SYMBOL_TO_CATEGORY = {
    'BTCUSD': 'BTC',
    'ETHUSD': 'ETH',
    'ADAUSD': 'ADA',
    'SOLUSD': 'SOL',
    'DOGEUSD': 'DOGE',
    'DOTUSD': 'DOT',
    'MATICUSD': 'MATIC',
    'UNIUSD': 'UNI',
    'LTCUSD': 'LTC',
    'LINKUSD': 'LINK',
    'XLMUSD': 'XLM',
    'TRXUSD': 'TRX',
    'AVAXUSD': 'AVAX',
    'XRPUSD': 'XRP',
    'BNBUSD': 'BNB',
    'BCHUSD': 'BCH',
    'ETCUSD': 'ETC',
}


def fetch_general_news(limit: int = 50) -> Optional[List[Dict]]:
    """
    Fetch general cryptocurrency news.

    Args:
        limit: Number of articles to fetch (max 50 for free tier)

    Returns:
        List of news articles or None if failed
    """
    url = f"{CRYPTOCOMPARE_API_BASE}/data/v2/news/"
    params = {
        'lang': 'EN',
        'limit': limit
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('Type') == 100:
            return data.get('Data', [])
        else:
            print(f"API error: {data.get('Message')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None


def fetch_category_news(categories: List[str], limit: int = 50) -> Optional[List[Dict]]:
    """
    Fetch cryptocurrency news filtered by categories.

    Args:
        categories: List of cryptocurrency symbols (e.g., ['BTC', 'ETH'])
        limit: Number of articles to fetch

    Returns:
        List of news articles or None if failed
    """
    url = f"{CRYPTOCOMPARE_API_BASE}/data/v2/news/"
    params = {
        'lang': 'EN',
        'categories': ','.join(categories),
        'limit': limit
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('Type') == 100:
            return data.get('Data', [])
        else:
            print(f"API error: {data.get('Message')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None


def filter_news_by_coin(news_articles: List[Dict], coin_symbol: str) -> List[Dict]:
    """
    Filter news articles to only those mentioning a specific coin.

    Args:
        news_articles: List of news articles
        coin_symbol: Cryptocurrency symbol (e.g., 'BTC')

    Returns:
        Filtered list of news articles
    """
    filtered = []
    coin_symbol_upper = coin_symbol.upper()

    for article in news_articles:
        # Check if coin is in categories
        categories = article.get('categories', '').upper()
        tags = article.get('tags', '').upper()
        title = article.get('title', '').upper()
        body = article.get('body', '').upper()

        if (coin_symbol_upper in categories or
            coin_symbol_upper in tags or
            coin_symbol_upper in title or
            coin_symbol_upper in body):
            filtered.append(article)

    return filtered


def fetch_news_for_symbols(symbols: List[str], articles_per_symbol: int = 5) -> Dict[str, List[Dict]]:
    """
    Fetch news for multiple cryptocurrency symbols.

    Args:
        symbols: List of trading symbols (e.g., ['BTCUSD', 'ETHUSD'])
        articles_per_symbol: Number of articles to return per symbol

    Returns:
        Dictionary mapping symbols to their news articles
    """
    all_news = {}

    # Get categories for our symbols
    categories = []
    for symbol in symbols:
        category = SYMBOL_TO_CATEGORY.get(symbol)
        if category:
            categories.append(category)

    if not categories:
        print("No valid symbols found")
        return {}

    print(f"Fetching news for categories: {', '.join(categories)}")

    # Fetch news with all categories
    news_articles = fetch_category_news(categories, limit=50)

    if not news_articles:
        print("No news articles fetched")
        return {}

    print(f"Fetched {len(news_articles)} total articles")

    # Filter news for each symbol
    for symbol in symbols:
        category = SYMBOL_TO_CATEGORY.get(symbol)
        if not category:
            continue

        print(f"Filtering news for {symbol} ({category})...")
        filtered_news = filter_news_by_coin(news_articles, category)

        # Take only the requested number of articles
        all_news[symbol] = filtered_news[:articles_per_symbol]
        print(f"  Found {len(filtered_news)} articles, keeping {len(all_news[symbol])}")

    return all_news


def format_news_article(article: Dict) -> str:
    """
    Format a news article for display.

    Args:
        article: News article dictionary

    Returns:
        Formatted string
    """
    timestamp = datetime.fromtimestamp(article.get('published_on', 0))
    title = article.get('title', 'N/A')
    source = article.get('source', 'N/A')
    url = article.get('url', 'N/A')
    body = article.get('body', '')[:200] + '...' if len(article.get('body', '')) > 200 else article.get('body', '')

    return f"""
Title: {title}
Source: {source}
Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
URL: {url}
Summary: {body}
"""


def save_news_data(data: Dict[str, List[Dict]], output_file: str):
    """
    Save cryptocurrency news to JSON file.

    Args:
        data: Dictionary of cryptocurrency news
        output_file: Output JSON filename
    """
    # Add metadata
    output_data = {
        'fetch_timestamp': datetime.now().isoformat(),
        'total_symbols': len(data),
        'news': data
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"\nNews data saved to {output_file}")


def print_summary(data: Dict[str, List[Dict]]):
    """Print summary of fetched news."""
    print(f"\n{'='*80}")
    print(f"CRYPTO NEWS FETCH SUMMARY")
    print(f"{'='*80}")
    print(f"Total symbols: {len(data)}")
    print(f"Timestamp: {datetime.now()}")
    print()

    for symbol, articles in sorted(data.items()):
        print(f"{symbol}: {len(articles)} articles")
        for i, article in enumerate(articles, 1):
            timestamp = datetime.fromtimestamp(article.get('published_on', 0))
            print(f"  {i}. {article.get('title', 'N/A')[:60]}... ({timestamp.strftime('%Y-%m-%d')})")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Fetch cryptocurrency news from CryptoCompare API'
    )
    parser.add_argument(
        '--output',
        default='crypto_news_data.json',
        help='Output JSON file (default: crypto_news_data.json)'
    )
    parser.add_argument(
        '--symbols',
        nargs='+',
        help='Specific symbols to fetch news for (default: all mapped symbols)'
    )
    parser.add_argument(
        '--articles',
        type=int,
        default=5,
        help='Number of articles per symbol (default: 5)'
    )

    args = parser.parse_args()

    # Determine which symbols to fetch
    symbols = args.symbols if args.symbols else list(SYMBOL_TO_CATEGORY.keys())

    print(f"Fetching news for {len(symbols)} cryptocurrencies...")
    print(f"Articles per symbol: {args.articles}\n")

    # Fetch news
    news_data = fetch_news_for_symbols(symbols, args.articles)

    # Save to file
    if news_data:
        save_news_data(news_data, args.output)
        print_summary(news_data)
    else:
        print("No news data fetched!")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
