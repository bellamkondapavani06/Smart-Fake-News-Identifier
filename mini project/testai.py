import joblib

model = joblib.load("ai_model.pkl")
vectorizer = joblib.load("ai_vectorizer.pkl")

print("Model Loaded Successfully")