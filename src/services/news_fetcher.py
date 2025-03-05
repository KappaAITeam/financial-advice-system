import requests
from src.utils.logger import logger
from src.config import config

STOCKS = ["NVDA", "TSLA", "GOOG"]


def fetch_stock_news():
    """
    Fetches stock-related news from external APIs.
    """
    all_news = []
    for stock in STOCKS:
        # Example API call (dummy URL)
        response = requests.get(
            f"https://api.dummy.com/news?q={stock}&apiKey={config.NEWS_API_KEY}")
        if response.status_code == 200:
            news = response.json().get("articles", [])
            for article in news:
                article["stock"] = stock
                all_news.append(article)
        else:
            logger.error(f"Failed to fetch news for {stock}")
    return all_news
