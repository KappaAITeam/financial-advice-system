# Financial Advice System

## Project Structure

This project is structured to ensure **scalability, modularity, and maintainability** while following best practices in API development using **FastAPI** and **MongoDB (Beanie ORM)**.

```
financial-advice-system/
├── .env                     # Environment variables (e.g., MONGO_URI, JWT_SECRET, API keys, etc.)
├── README.md                # Project documentation and overview
├── requirements.txt         # Dependencies list
├── .gitignore               # Files/folders to ignore in Git
├── main.py                  # FastAPI app entry point; initializes DB and registers routes
├── db.py                    # Database initialization using Beanie (MongoDB ORM)
├── config.py                # Global configuration management (loads .env values)
├── auth.py                  # (Optional) Top-level authentication utilities (or redirect to utils/jwt_handler.py)
└── src/
    ├── api/
    │   ├── routes/          # Folder for API endpoints (modularized by functionality)
    │   │   ├── auth.py            # Endpoints for user registration & login
    │   │   ├── stock_advice.py    # Endpoints for stock trading advice (RAG queries)
    │   │   ├── embeddings.py      # Endpoints for voice/video embedding operations
    │   │   ├── rag.py             # Handles RAG-based financial Q&A
    │   └── models/          # Folder for Pydantic models (data schemas)
    │       ├── user.py            # User models for registration, login, profile, etc.
    │       ├── stock.py           # Models for stock news and financial data
    │       ├── embedding.py       # Models for text, voice, and video embeddings
    │       └── rag.py             # Models for RAG queries and responses
    ├── services/            # Business logic and processing modules
    │   ├── user_service.py      # User-related operations (registration, login, profile management)
    │   ├── stock_service.py     # Stock news fetching and analysis logic
    │   ├── news_fetcher.py      # Fetches stock-related news from external APIs (every 6 hours)
    │   ├── temp_storage.py      # Manages temporary storage (news data expires after 24 hours)
    │   ├── vector_store.py      # Implements MongoDB Atlas Vector Search for storing/retrieving embeddings
    │   ├── rag_engine.py        # Implements the RAG pipeline (retrieval + LLM generation) for financial advice
    │   ├── voice_video.py       # Handles processing for voice and video input
    ├── utils/               # Utility functions and helpers
    │   ├── jwt_handler.py       # JWT token creation and verification functions
    │   ├── hashing.py           # Password hashing utilities using bcrypt
    │   ├── config_utils.py      # Functions for loading and managing configuration settings
    │   └── logger.py            # Centralized logging configuration
    └── embeddings/          # Modules for processing media into embeddings
        ├── voice_processing.py # Converts voice (speech) to embeddings
        └── video_processing.py # Processes video data into embeddings
```

## Why This Structure?

### 1️ eparation of Concerns (SoC)**
Each module has a **clear responsibility**, making the code easier to navigate, test, and maintain.

### 2️ Modular Design**
We use a modular folder structure to **group related functionalities together**, ensuring that the codebase remains scalable as new features are added.

### 3️ API Layer (`src/api/`)**
All API endpoints are located under `src/api/routes/`, making it easy to add new routes **without affecting the core business logic**.

### 4️ Business Logic Layer (`src/services/`)**
The **services** folder handles core logic, such as fetching stock news, executing RAG queries, and processing financial data. This ensures:
- Clear **separation between API endpoints and business logic**
- **Reusability** across multiple parts of the application

### 5️ Pydantic Models (`src/api/models/`)**
All data schemas are defined using **Pydantic**, making data validation and serialization consistent across the app.

### 6️ Utility Layer (`src/utils/`)**
A dedicated **utils** folder keeps helper functions like JWT handling, password hashing, and logging **centralized and reusable**.

### 7️ Embedding Processing (`src/embeddings/`)**
Since the app supports **voice and video-based** financial advice, we have a separate `embeddings/` folder to handle **media processing** and embedding generation.

### 8️ Database Layer (`db.py`)**
The database setup is handled via **Beanie** (MongoDB ORM) with an easy-to-configure **`.env`-based approach**.

## 🔹 Getting Started

### 1 Install dependencies**
```bash
pip install -r requirements.txt
```

### 2️ Set up environment variables**
Create a `.env` file and configure necessary values like `MONGO_URI`, `JWT_SECRET`, etc.

Example `.env`:
```env
MONGO_URI=mongodb+srv://your-db-url
MONGO_DB=financial_advice
JWT_SECRET=your-secret-key
```

### 3️ Run the FastAPI server**
```bash
uvicorn main:app --reload
```

### 4️ Access the API Docs**
Visit [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API via the interactive Swagger UI.


