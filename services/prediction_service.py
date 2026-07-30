from typing import Dict, Any
from config import Config
from models import SKLearnPredictor, TransformerPredictor
from services.factcheck_service import FactCheckService
from utils.validators import validate_article_input
from utils.logger import logger
from utils.constants import GEMINI_STATUS_NOT_REQUIRED

class PredictionService:
    """
    Primary Prediction Service. Manages single-instance ML model lifecycle,
    executes predictions, and coordinates automatic secondary fact checking.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PredictionService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        logger.info("Initializing PredictionService & loading machine learning models into memory...")
        self.sklearn_predictor = SKLearnPredictor()
        self.transformer_predictor = TransformerPredictor()
        self.factcheck_service = FactCheckService()
        self._initialized = True
        logger.info("PredictionService initialized successfully.")

    def get_active_model(self):
        """Selects operational ML/DL predictor."""
        mode = Config.DEFAULT_MODEL_MODE.upper()
        
        if mode == "TRANSFORMER" and self.transformer_predictor.is_available():
            return self.transformer_predictor
        elif mode == "SKLEARN" and self.sklearn_predictor.is_available():
            return self.sklearn_predictor

        # AUTO mode: prefer Transformer if available, else SKLearn
        if self.transformer_predictor.is_available():
            return self.transformer_predictor
        elif self.sklearn_predictor.is_available():
            return self.sklearn_predictor
        else:
            raise RuntimeError("No operational prediction models available.")

    def analyze_news(self, raw_text: str, force_gemini: bool = False) -> Dict[str, Any]:
        """
        Executes full Fake News Analysis Workflow.
        """
        logger.info(f"Received prediction request. Text length: {len(raw_text) if raw_text else 0}")

        # 1. Input Validation
        is_valid, err_msg = validate_article_input(raw_text)
        if not is_valid:
            logger.warning(f"Input validation rejected request: {err_msg}")
            return {
                "success": False,
                "error": err_msg,
                "prediction": None
            }

        # 2. Prediction Execution
        try:
            model = self.get_active_model()
            logger.info(f"Executing prediction using model: {model.__class__.__name__}")
            prediction_res = model.predict(raw_text)
        except Exception as e:
            logger.error(f"Primary model inference error: {e}", exc_info=True)
            if self.sklearn_predictor.is_available():
                logger.info("Fallback: Executing prediction using SKLearn predictor...")
                prediction_res = self.sklearn_predictor.predict(raw_text)
            else:
                return {
                    "success": False,
                    "error": f"Prediction service failure: {str(e)}",
                    "prediction": None
                }

        confidence = prediction_res.get("confidence", 0.0)
        label = prediction_res.get("label", "Unknown")
        is_ai = prediction_res.get("is_ai", False)

        # 3. Secondary Fact-Checking Condition Evaluation
        should_trigger_gemini = (
            force_gemini or
            (confidence < Config.CONFIDENCE_THRESHOLD) or
            is_ai
        )

        gemini_result = None

        if should_trigger_gemini:
            if confidence < Config.CONFIDENCE_THRESHOLD:
                trigger_reason = f"Primary model confidence ({confidence}%) is below threshold ({Config.CONFIDENCE_THRESHOLD}%)."
            elif is_ai:
                trigger_reason = "Article identified as AI-generated content."
            else:
                trigger_reason = "Manual secondary verification requested."

            gemini_result = self.factcheck_service.perform_fact_check(raw_text, trigger_reason=trigger_reason)
        else:
            gemini_result = {
                "triggered": False,
                "status": GEMINI_STATUS_NOT_REQUIRED,
                "reason": f"Model prediction achieved high confidence ({confidence}% >= threshold {Config.CONFIDENCE_THRESHOLD}%). Secondary verification not required.",
                "confidence": f"{confidence}%",
                "trigger_reason": "High primary confidence"
            }

        logger.info(f"Prediction completed successfully. Result: '{label}', Confidence: {confidence}%")

        return {
            "success": True,
            "error": None,
            "prediction": {
                "result": label,
                "confidence": f"{confidence}%",
                "confidence_val": confidence,
                "is_fake": prediction_res.get("is_fake", False),
                "is_ai": is_ai,
                "model_type": prediction_res.get("model_type", "Standard Model"),
                "explanation": prediction_res.get("explanation", ""),
                "details": prediction_res.get("details", {}),
                "gemini_verification": gemini_result
            }
        }
