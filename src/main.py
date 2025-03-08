from fastapi import FastAPI
from ..db import init_db
from src.api.routes import auth, stock_advice, embeddings, rag, voice_chat_websocket

app = FastAPI(title="Financial Advice System for Stock Trading")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(stock_advice.router, prefix="/stock", tags=["Stock Advice"])
app.include_router(embeddings.router, prefix="/embeddings",
                   tags=["Embeddings"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])
app.include_router(voice_chat_websocket.router, prefix="", tags=["Voice Chat"])


@app.on_event("startup")
async def startup_event():
    await init_db()
    # You could also schedule periodic tasks (e.g., news fetching) here


@app.get("/")
async def root():
    return {"message": "Welcome to the Financial Advice System API"}
