import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    """Centralized Production Configuration for Smart Fake News Identifier."""

    # Flask Core Configuration
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-production-secret-key-change-me")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "127.0.0.1")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))  # 10 MB

    # Model & Fact-Checking Configuration
    CONFIDENCE_THRESHOLD = float(os.getenv("GEMINI_CONFIDENCE_THRESHOLD", 90.0))
    DEFAULT_MODEL_MODE = os.getenv("DEFAULT_MODEL_MODE", "AUTO")  # AUTO, TRANSFORMER, SKLEARN

    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    MEDIASTACK_API_KEY = os.getenv("MEDIASTACK_API_KEY", "")

    # Input Validation Thresholds
    MIN_INPUT_CHARS = 20
    MIN_INPUT_WORDS = 3
    MAX_INPUT_CHARS = 10000

    # Paths
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    LOG_FILE_PATH = os.path.join(LOGS_DIR, "app.log")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    
    AI_MODEL_PATH = os.path.join(MODELS_DIR, "ai_model.pkl")
    AI_VECTORIZER_PATH = os.path.join(MODELS_DIR, "ai_vectorizer.pkl")
    NEWS_MODEL_PATH = os.path.join(MODELS_DIR, "model.pkl")
    NEWS_VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.pkl")

    # Logging Level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
