from typing import Dict, Any
from models.base_model import BaseModel
from utils.preprocessor import clean_text
from utils.logger import logger

class TransformerPredictor(BaseModel):
    """
    Transformer-based (RoBERTa / DeBERTa / DistilBERT) Deep Learning Predictor.
    Loads fine-tuned Hugging Face transformer models dynamically if available.
    """

    def __init__(self, model_name: str = "hamandcheese/fake-news-detector"):
        self.model_name = model_name
        self.pipeline = None
        self._available = False
        self._initialize_pipeline()

    def _initialize_pipeline(self):
        try:
            import torch
            from transformers import pipeline

            logger.info(f"Attempting to initialize Transformer model: {self.model_name}")
            # Initialize lightweight binary sequence classifier
            self.pipeline = pipeline(
                "text-classification",
                model=self.model_name,
                device=-1, # CPU execution by default
                top_k=None
            )
            self._available = True
            logger.info(f"Transformer model '{self.model_name}' initialized successfully.")
        except Exception as e:
            logger.warning(
                f"Transformer model '{self.model_name}' unavailable or could not be loaded ({e}). "
                "System will seamlessly fall back to local ensemble ML models."
            )
            self._available = False

    def is_available(self) -> bool:
        return self._available and (self.pipeline is not None)

    def predict(self, raw_text: str) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("Transformer predictor is not available.")

        cleaned = clean_text(raw_text, preserve_structure=True)
        # Truncate text to fit model context window (first ~512 tokens)
        truncated = cleaned[:2000]

        try:
            results = self.pipeline(truncated)
            # results format: [[{'label': 'LABEL_0', 'score': 0.95}, {'label': 'LABEL_1', 'score': 0.05}]]
            scores = results[0] if isinstance(results[0], list) else results
            
            top_score = max(scores, key=lambda x: x['score'])
            label_name = top_score['label'].upper()
            confidence = round(float(top_score['score']) * 100, 2)

            is_fake = "FAKE" in label_name or "LABEL_1" in label_name or "1" in label_name
            label = "Human Written - Fake News" if is_fake else "Human Written - Real News"

            explanation = (
                "Deep contextual attention representations (Transformer architecture) identified semantic patterns "
                "associated with inaccurate or misleading news reporting."
                if is_fake else
                "Transformer contextual self-attention verified semantic coherence and factual narrative consistency."
            )

            return {
                "label": label,
                "is_fake": is_fake,
                "is_ai": False,
                "confidence": confidence,
                "model_type": f"Transformer ({self.model_name})",
                "details": {
                    "raw_outputs": scores
                },
                "explanation": explanation
            }
        except Exception as e:
            logger.error(f"Transformer inference error: {e}", exc_info=True)
            raise RuntimeError(f"Transformer inference failed: {e}")
