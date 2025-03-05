from src.services.vector_store import retrieve_relevant_data
from src.utils.logger import logger


def process_financial_query(query: str) -> dict:
    """
    Processes a financial query by retrieving relevant stock news/discussions and generating insights.

    Args:
        query (str): The user's financial query.

    Returns:
        dict: A response containing relevant financial information.
    """
    logger.info(f"Processing financial query: {query}")

    # Step 1: Retrieve relevant documents (news & discussions)
    relevant_docs = retrieve_relevant_data(query)

    # Step 2: Generate financial insights using LLM (Mocked here)
    if not relevant_docs:
        return {"response": "No relevant financial data found.", "source": []}

    # TODO: Replace with actual LLM-based generation
    generated_response = f"Based on the latest financial news, here is what we found about '{query}':\n" + \
                         "\n".join([doc['content'][:200] +
                                   "..." for doc in relevant_docs[:3]])

    return {
        "response": generated_response,
        "source": [doc["source"] for doc in relevant_docs]
    }
