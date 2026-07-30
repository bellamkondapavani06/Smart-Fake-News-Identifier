from typing import Dict, Any
from config import Config
from models import SKLearnPredictor, TransformerPredictor
from services.gemini_service import GeminiService
from utils.validator import validate_news_input
from utils.logger import logger

class PredictorService:
    """
    Core prediction orchestrator. Manages model selection, confidence thresholding,
    and automatic Gemini API secondary fact-checking verification.
    """

    def __init__(self):
        self.sklearn_predictor = SKLearnPredictor()
        self.transformer_predictor = TransformerPredictor()
        self.gemini_service = GeminiService()

    def get_active_model(self):
        """Selects the best available prediction model based on configuration & availability."""
        mode = Config.DEFAULT_MODEL_MODE.upper()
        
        if mode == "TRANSFORMER" and self.transformer_predictor.is_available():
            return self.transformer_predictor
        elif mode == "SKLEARN" and self.sklearn_predictor.is_available():
            return self.sklearn_predictor

        # AUTO mode: Prefer Transformer if available, else SKLearn
        if self.transformer_predictor.is_available():
            return self.transformer_predictor
        elif self.sklearn_predictor.is_available():
            return self.sklearn_predictor
        else:
            raise RuntimeError("No prediction models are currently operational.")

    def analyze_news(self, raw_text: str, force_gemini: bool = False) -> Dict[str, Any]:
        """
        Executes full Fake News Analysis Workflow.
        """
        # 1. Input Validation
        is_valid, err_msg = validate_news_input(raw_text)
        if not is_valid:
            return {
                "success": False,
                "error": err_msg,
                "prediction": None
            }

        # 2. Model Selection & Prediction Execution
        try:
            model = self.get_active_model()
            logger.info(f"Executing prediction using active model: {model.__class__.__name__}")
            prediction_res = model.predict(raw_text)
        except Exception as e:
            logger.error(f"Error during primary model inference: {e}", exc_info=True)
            # Fallback to SKLearn if Transformer failed
            if self.sklearn_predictor.is_available():
                logger.info("Falling back to SKLearn ensemble model...")
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

        # 3. Secondary Verification Condition Evaluation
        # Automatic trigger if confidence < CONFIDENCE_THRESHOLD (90%), AI generated, or forced
        should_trigger_gemini = (
            force_gemini or
            (confidence < Config.CONFIDENCE_THRESHOLD) or
            is_ai
        )

        gemini_result = None
        gemini_trigger_reason = ""

        if should_trigger_gemini:
            if confidence < Config.CONFIDENCE_THRESHOLD:
                gemini_trigger_reason = f"Primary model confidence ({confidence}%) is below verification threshold ({Config.CONFIDENCE_THRESHOLD}%)."
            elif is_ai:
                gemini_trigger_reason = "Article identified as AI-generated text."
            elif force_gemini:
                gemini_trigger_reason = "Manual secondary verification requested."

            logger.info(f"Triggering Gemini secondary verification. Reason: {gemini_trigger_reason}")
            gemini_res = self.gemini_service.verify_news(raw_text)
            gemini_res["trigger_reason"] = gemini_trigger_reason
            gemini_result = gemini_res
        else:
            gemini_result = {
                "triggered": False,
                "status": "Not Required",
                "reason": f"Model prediction achieved high confidence ({confidence}% >= threshold {Config.CONFIDENCE_THRESHOLD}%). Secondary verification not required.",
                "confidence": f"{confidence}%",
                "trigger_reason": "High primary confidence"
            }

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
