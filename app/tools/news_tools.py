import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from loguru import logger
import yfinance as yf


def get_company_news(ticker: str, company_name: str | None = None) -> list[dict]:
    """
    Fetches the latest curated financial news articles for a company from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol (e.g. 'AAPL', 'GOOGL', 'NVDA').
        company_name (str, optional): The common name of the company (e.g. 'Apple', 'Alphabet', 'NVIDIA').

    Returns:
        list[dict]: A list of recent news articles with title, publisher, publish date, and URL.
    """
    logger.info(f"Calling get_company_news(ticker='{ticker}', company_name='{company_name}')")
    search_term = company_name if company_name else ticker
    articles = []

    try:
        s = yf.Search(search_term, news_count=8)
        raw_news = getattr(s, "news", []) or []
        for item in raw_news:
            pub_time = item.get("providerPublishTime")
            dt_str = (
                datetime.fromtimestamp(pub_time).strftime("%Y-%m-%d %H:%M:%S")
                if pub_time
                else "Recent"
            )
            articles.append(
                {
                    "title": item.get("title", ""),
                    "publisher": item.get("publisher", "Unknown"),
                    "published_at": dt_str,
                    "link": item.get("link", ""),
                }
            )
    except Exception as e:
        logger.warning(f"Error fetching Yahoo Finance news for {ticker}: {e}")

    logger.info(f"Retrieved {len(articles)} articles for {ticker}")
    return articles


def search_market_news(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches Google News RSS for real-time news articles on specific corporate events,
    regulatory investigations, legal actions, earnings surprises, or partnerships.

    Args:
        query (str): The search query (e.g. 'Alphabet DOJ antitrust', 'NVIDIA Blackwell chip delay').
        max_results (int): Maximum number of search results to return (default: 5).

    Returns:
        list[dict]: List of matching articles with title, publisher source, pubDate, and link.
    """
    logger.info(f"Calling search_market_news(query='{query}', max_results={max_results})")
    encoded_q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-US&gl=US&ceid=US:en"
    articles = []

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        for item in root.findall(".//item")[:max_results]:
            title_elem = item.find("title")
            pubdate_elem = item.find("pubDate")
            link_elem = item.find("link")
            source_elem = item.find("source")

            articles.append(
                {
                    "title": title_elem.text if title_elem is not None else "",
                    "publisher": source_elem.text if source_elem is not None else "Google News",
                    "published_at": pubdate_elem.text if pubdate_elem is not None else "Recent",
                    "link": link_elem.text if link_elem is not None else "",
                }
            )
    except Exception as e:
        logger.warning(f"Error querying Google News RSS for '{query}': {e}")

    logger.info(f"Retrieved {len(articles)} search results for query '{query}'")
    return articles
