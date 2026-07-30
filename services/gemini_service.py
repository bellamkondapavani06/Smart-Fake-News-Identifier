from typing import Dict, Any
from config import Config
from utils.logger import logger

class GeminiService:
    """Service wrapping Google Gemini API for news fact-checking and secondary verification."""

    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Initialized Gemini API client successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self.client = None
        else:
            logger.warning("Gemini API key is not configured. Secondary verification will be skipped.")

    def is_configured(self) -> bool:
        return self.client is not None

    def verify_news(self, article_text: str) -> Dict[str, Any]:
        """
        Invokes Gemini fact-checking model to verify news article veracity.
        """
        if not self.is_configured():
            return {
                "triggered": False,
                "status": "Skipped",
                "reason": "Gemini API key not configured in environment.",
                "confidence": "N/A",
                "raw_response": ""
            }

        prompt = f"""
You are an expert, objective fact-checking assistant.

Analyze the following news claim or article for authenticity, key facts, and potential misinformation.

News Text:
\"\"\"
{article_text[:3000]}
\"\"\"

Instructions:
1. Verify the claim using reliable real-world information.
2. If enough reliable evidence exists confirming the claim, return Status: Verified.
3. If the claim is false or fabricated, return Status: False.
4. If there is insufficient evidence, return Status: Unverified.
5. Provide a clear 1-2 sentence explanation under Reason.
6. Estimate fact-checking confidence (0-100%).

Reply strictly in this format:
Status: <Verified / False / Unverified>
Reason: <brief explanation>
Confidence: <0-100>%
"""

        try:
            logger.info("Calling Gemini API for secondary fact-checking verification...")
            response = self.client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )
            
            raw_text = response.text.strip() if response and response.text else "No response returned."
            
            # Parse structured response
            status = "Unverified"
            reason = raw_text
            confidence = "N/A"

            for line in raw_text.splitlines():
                if line.lower().startswith("status:"):
                    status = line.split(":", 1)[1].strip()
                elif line.lower().startswith("reason:"):
                    reason = line.split(":", 1)[1].strip()
                elif line.lower().startswith("confidence:"):
                    confidence = line.split(":", 1)[1].strip()

            return {
                "triggered": True,
                "status": status,
                "reason": reason,
                "confidence": confidence,
                "raw_response": raw_text
            }

        except Exception as e:
            logger.error(f"Gemini API verification error: {e}", exc_info=True)
            return {
                "triggered": True,
                "status": "Error",
                "reason": f"Gemini API Error: {str(e)}",
                "confidence": "N/A",
                "raw_response": ""
            }
