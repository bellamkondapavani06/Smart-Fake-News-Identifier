import os
import joblib
from typing import Dict, Any
from models.base_model import BaseModel
from utils.preprocessor import clean_text
from utils.logger import logger
from config import Config

class SKLearnPredictor(BaseModel):
    """Legacy/Fallback SKLearn TF-IDF classification pipeline."""

    def __init__(self):
        self.ai_model = None
        self.ai_vectorizer = None
        self.news_model = None
        self.news_vectorizer = None
        self._load_models()

    def _load_models(self):
        try:
            if os.path.exists(Config.AI_MODEL_PATH) and os.path.exists(Config.AI_VECTORIZER_PATH):
                self.ai_model = joblib.load(Config.AI_MODEL_PATH)
                self.ai_vectorizer = joblib.load(Config.AI_VECTORIZER_PATH)
                logger.info("Loaded SKLearn AI/Human classifier successfully.")

            if os.path.exists(Config.NEWS_MODEL_PATH) and os.path.exists(Config.NEWS_VECTORIZER_PATH):
                self.news_model = joblib.load(Config.NEWS_MODEL_PATH)
                self.news_vectorizer = joblib.load(Config.NEWS_VECTORIZER_PATH)
                logger.info("Loaded SKLearn Fake/Real classifier successfully.")
        except Exception as e:
            logger.error(f"Error loading SKLearn models: {e}", exc_info=True)

    def is_available(self) -> bool:
        return (
            self.ai_model is not None
            and self.ai_vectorizer is not None
            and self.news_model is not None
            and self.news_vectorizer is not None
        )

    def predict(self, raw_text: str) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("SKLearn models are not available or failed to load.")

        cleaned = clean_text(raw_text)

        # 1. AI vs Human Detection
        ai_vec = self.ai_vectorizer.transform([cleaned])
        ai_pred = self.ai_model.predict(ai_vec)[0]

        ai_confidence = 50.0
        if hasattr(self.ai_model, "predict_proba"):
            ai_probs = self.ai_model.predict_proba(ai_vec)[0]
            ai_confidence = float(max(ai_probs) * 100)

        # If detected as AI generated content
        if ai_pred == 1:
            return {
                "label": "AI Generated News",
                "is_fake": True,
                "is_ai": True,
                "confidence": round(ai_confidence, 2),
                "model_type": "TF-IDF + Scikit-Learn Classifier (AI Detector)",
                "details": {
                    "ai_detection_confidence": round(ai_confidence, 2),
                    "news_classification": "N/A (AI Generated)"
                },
                "explanation": "Statistical feature analysis indicates this text has stylometric patterns characteristic of AI-generated content."
            }

        # 2. Fake vs Real Detection (Human Written)
        news_vec = self.news_vectorizer.transform([cleaned])
        news_pred = self.news_model.predict(news_vec)[0]

        news_confidence = 50.0
        if hasattr(self.news_model, "predict_proba"):
            news_probs = self.news_model.predict_proba(news_vec)[0]
            news_confidence = float(max(news_probs) * 100)

        is_fake = (news_pred == 1)
        label = "Human Written - Fake News" if is_fake else "Human Written - Real News"
        explanation = (
            "Linguistic & vocabulary analysis indicates non-standard source patterns common in sensationalist/fake articles."
            if is_fake else
            "Text structure, vocabulary distribution, and stylistic markers align with verified real news articles."
        )

        return {
            "label": label,
            "is_fake": is_fake,
            "is_ai": False,
            "confidence": round(news_confidence, 2),
            "model_type": "TF-IDF + Scikit-Learn Classifier (Ensemble)",
            "details": {
                "ai_detection_confidence": round(ai_confidence, 2),
                "news_classification_confidence": round(news_confidence, 2)
            },
            "explanation": explanation
        }
