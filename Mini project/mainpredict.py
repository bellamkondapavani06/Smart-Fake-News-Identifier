import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.predictor_service import PredictorService

def main():
    service = PredictorService()
    print("=" * 60)
    print(" 📰 Smart Fake News Identifier - CLI Prediction Interface ")
    print("=" * 60)
    
    news = input("\nEnter the news article text:\n\n").strip()
    if not news:
        print("Empty input provided.")
        return

    result = service.analyze_news(news)
    
    if not result["success"]:
        print(f"\n❌ Error: {result['error']}")
        return

    pred = result["prediction"]
    print("\n" + "=" * 40)
    print(f"Prediction       : {pred['result']}")
    print(f"Confidence Score : {pred['confidence']}")
    print(f"Model Type       : {pred['model_type']}")
    print(f"Explanation      : {pred['explanation']}")
    
    gemini = pred.get("gemini_verification", {})
    if gemini and gemini.get("triggered"):
        print("\n--- Gemini Fact Checking Verification ---")
        print(f"Trigger Reason   : {gemini.get('trigger_reason')}")
        print(f"Fact Status      : {gemini.get('status')}")
        print(f"Evidence/Reason  : {gemini.get('reason')}")
    print("=" * 40)

if __name__ == "__main__":
    main()