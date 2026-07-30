from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModel(ABC):
    """Abstract base class for Fake News & AI detection models."""

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if model is loaded and ready for predictions."""
        pass

    @abstractmethod
    def predict(self, raw_text: str) -> Dict[str, Any]:
        """
        Executes prediction on input text.

        Returns dict with keys:
            - label (str): e.g. "Human Written - Real News", "Human Written - Fake News", "AI Generated News"
            - confidence (float): 0.0 to 100.0
            - raw_score (float): model prediction probability
            - model_type (str): Name of model architecture used
            - details (dict): Detailed score breakdown
        """
        pass
