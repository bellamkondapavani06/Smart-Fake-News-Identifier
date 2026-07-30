from typing import Dict, Any
from services.gemini_service import GeminiService
from services.news_fetcher_service import NewsFetcherService
from utils.logger import logger

class FactCheckService:
    """Orchestrator for secondary fact-checking services (Gemini API & MediaStack)."""

    def __init__(self):
        self.gemini_service = GeminiService()
        self.news_fetcher = NewsFetcherService()

    def perform_fact_check(self, raw_text: str, trigger_reason: str = "") -> Dict[str, Any]:
        """Runs secondary fact-checking pipeline."""
        logger.info(f"FactCheckService triggered. Reason: {trigger_reason}")
        gemini_res = self.gemini_service.verify_news(raw_text)
        gemini_res["trigger_reason"] = trigger_reason
        return gemini_res
