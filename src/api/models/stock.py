# src/api/models/stock.py
from pydantic import BaseModel
from typing import Optional


class NewsArticle(BaseModel):
    """
    Model representing a news article or discussion related to a stock.
    """
    id: str                     # Unique identifier for the article
    title: str                  # Headline of the news article
    content: str                # Main text or summary of the article
    source: str                 # Source of the news (e.g., Reuters, Finnhub)
    published_at: str           # Publication timestamp in ISO format
    stock: str                  # Stock symbol (e.g., NVDA, TSLA, GOOG)
