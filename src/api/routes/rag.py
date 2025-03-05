from fastapi import APIRouter

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/query/")
def query_rag():
    """
    Placeholder route for RAG-based financial advice.
    Returns a static response until the actual logic is implemented.
    """
    return {
        "status": "success",
        "message": "This is a placeholder for the RAG-based financial query system."
    }
