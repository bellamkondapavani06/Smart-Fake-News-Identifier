import requests
from typing import Dict, Any, Optional
from config import Config
from utils.logger import logger

class NewsFetcherService:
    """Service to fetch live external news articles from MediaStack API for cross-referencing."""

    def __init__(self):
        self.api_key = Config.MEDIASTACK_API_KEY

    def fetch_live_news(self, query: str, limit: int = 3) -> Optional[Dict[str, Any]]:
        """Fetch live news from MediaStack API matching search query."""
        if not self.api_key:
            logger.warning("MediaStack API key not set.")
            return None

        url = "http://api.mediastack.com/v1/news"
        params = {
            "access_key": self.api_key,
            "keywords": query,
            "languages": "en",
            "limit": limit
        }

        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"MediaStack API returned status code {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching live news: {e}")
            return None
