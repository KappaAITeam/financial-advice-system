from fastapi import FastAPI
from ..db import init_db
from src.api.routes import auth, stock_advice, embeddings, rag

app = FastAPI(title="Financial Advice System for Stock Trading")

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(stock_advice.router, prefix="/stock", tags=["Stock Advice"])
app.include_router(embeddings.router, prefix="/embeddings",
                   tags=["Embeddings"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])


@app.on_event("startup")
async def startup_event():
    await init_db()
    # You could also schedule periodic tasks (e.g., news fetching) here


@app.get("/")
async def root():
    return {"message": "Welcome to the Financial Advice System API"}
