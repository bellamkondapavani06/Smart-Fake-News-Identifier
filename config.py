import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    """Central configuration for Smart Fake News Identifier."""
    
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "127.0.0.1")

    # Model & Verification Settings
    CONFIDENCE_THRESHOLD = float(os.getenv("GEMINI_CONFIDENCE_THRESHOLD", 90.0))
    DEFAULT_MODEL_MODE = os.getenv("DEFAULT_MODEL_MODE", "AUTO")  # AUTO, TRANSFORMER, SKLEARN
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    MEDIASTACK_API_KEY = os.getenv("MEDIASTACK_API_KEY", "")

    # Input Validation & Limits
    MIN_INPUT_CHARS = 20
    MIN_INPUT_WORDS = 3
    MAX_INPUT_CHARS = 10000

    # Paths
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    AI_MODEL_PATH = os.path.join(MODELS_DIR, "ai_model.pkl")
    AI_VECTORIZER_PATH = os.path.join(MODELS_DIR, "ai_vectorizer.pkl")
    NEWS_MODEL_PATH = os.path.join(MODELS_DIR, "model.pkl")
    NEWS_VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.pkl")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.path.join(BASE_DIR, "app.log")
