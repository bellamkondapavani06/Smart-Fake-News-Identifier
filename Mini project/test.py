import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

print("Model Loaded Successfully")