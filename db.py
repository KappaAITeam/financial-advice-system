from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from src.api.models.user import User

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from src.api.models.user import User


async def init_db():
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri or not mongo_uri.startswith("mongodb"):
        print("⚠️ WARNING: Invalid or missing MONGO_URI. Skipping database initialization.")
        return  # Exit the function without initializing MongoDB

    try:
        client = AsyncIOMotorClient(mongo_uri)
        db_name = os.getenv("MONGO_DB", "financial_advice")
        await init_beanie(database=client[db_name], document_models=[User])
        print("MongoDB initialized successfully.")
    except Exception as e:
        print(f"ERROR: Failed to initialize MongoDB - {e}")
