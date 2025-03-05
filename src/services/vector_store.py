from db import get_mongo_collection
from src.utils.logger import logger


def retrieve_relevant_data(query: str, top_k: int = 5) -> list:
    """
    Queries the MongoDB vector store to find relevant stock news and discussions.

    Args:
        query (str): The financial query for retrieving relevant documents.
        top_k (int): The number of top-matching documents to retrieve.

    Returns:
        list: A list of relevant documents with 'content' and 'source'.
    """
    logger.info(f"Retrieving relevant stock news for query: {query}")

    # Get MongoDB collection
    collection = get_mongo_collection("stock_news")

    # Perform a text-based search (Modify if using an actual vector DB)
    results = collection.find(
        {"content": {"$regex": query, "$options": "i"}}).limit(top_k)

    # Convert results to a list of dicts
    relevant_docs = [{"content": doc["content"], "source": doc.get(
        "source", "Unknown")} for doc in results]

    return relevant_docs
