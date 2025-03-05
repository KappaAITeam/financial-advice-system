import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # MONGO_URI = os.getenv(
    #     "mongodb+srv://development:development@kappa.jljq6.mongodb.net/?retryWrites=true&w=majority&appName=kappa")
    # MONGO_DB = os.getenv("MONGO_DB", "financial_advice")
    JWT_SECRET = os.getenv("JWT_SECRET")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")


config = Config()
