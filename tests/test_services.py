import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from services import PreprocessingService, PredictionService
from utils.validators import validate_article_input

class TestFakeNewsIdentifier(unittest.TestCase):
    """Unit and Integration Tests for Fake News Detection Services & API."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.prediction_service = PredictionService()

    def test_preprocessor_cleaning(self):
        raw = "<h1>BREAKING:</h1> Test news article! Check out http://example.com 😁 #news"
        cleaned = PreprocessingService.clean_text(raw)
        self.assertNotIn("<h1>", cleaned)
        self.assertNotIn("http://example.com", cleaned)
        self.assertIn("breaking test news article check out news", cleaned)

    def test_input_validation(self):
        # Test empty input
        valid, msg = validate_article_input("")
        self.assertFalse(valid)
        self.assertIn("cannot be empty", msg)

        # Test short input
        valid, msg = validate_article_input("Short text")
        self.assertFalse(valid)
        self.assertIn("too short", msg)

        # Test valid input
        valid, msg = validate_article_input("This is a valid test news headline for verification purposes.")
        self.assertTrue(valid)

    def test_prediction_service(self):
        sample = "The NASA Webb Telescope has transmitted ultra high resolution images of distant galaxys."
        result = self.prediction_service.analyze_news(sample)
        self.assertTrue(result["success"])
        self.assertIn("result", result["prediction"])
        self.assertIn("confidence", result["prediction"])

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data["status"], "healthy")

    def test_api_predict_endpoint(self):
        payload = {"news": "Scientists discover ancient fossilized remains in Antarctica excavation expedition."}
        response = self.client.post("/api/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data["success"])

if __name__ == "__main__":
    unittest.main()
