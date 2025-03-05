from fastapi import APIRouter
from src.services.news_fetcher import fetch_stock_news

router = APIRouter(prefix="/stock-advice", tags=["Stock Advice"])


@router.get("/news/")
def get_stock_news():
    """Fetch the latest stock-related news from external APIs."""
    return fetch_stock_news()


@router.post("/query/")
def query_stock_advice():
    """
    Placeholder route for stock advice.
    Returns a static template instead of calling RAG engine or vector store.
    """
    return {
        "status": "success",
        "message": "This is a placeholder for stock advice. Implement logic here."
    }
