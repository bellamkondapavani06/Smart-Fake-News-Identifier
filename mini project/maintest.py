import joblib

# AI/Human model
ai_model = joblib.load("ai_model.pkl")
ai_vectorizer = joblib.load("ai_vectorizer.pkl")

# True/Fake model
news_model = joblib.load("model.pkl")
news_vectorizer = joblib.load("vectorizer.pkl")

print("Both models loaded successfully!")