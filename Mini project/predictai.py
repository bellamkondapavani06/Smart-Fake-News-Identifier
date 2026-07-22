import joblib
import re
import string

# ==========================
# Load Model and Vectorizer
# ==========================
model = joblib.load("ai_model.pkl")
vectorizer = joblib.load("ai_vectorizer.pkl")

# ==========================
# Text Preprocessing Function
# ==========================
def preprocess(text):
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

# ==========================
# Prediction Function
# ==========================
def predict_text(text):

    # Preprocess
    clean_text = preprocess(text)

    # Convert to TF-IDF
    text_vector = vectorizer.transform([clean_text])

    # Predict
    prediction = model.predict(text_vector)

    # Print Result
    if prediction[0] == 0:
        print("\nPrediction : Human Generated")
    else:
        print("\nPrediction : AI Generated")

    # Confidence Score (if available)
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(text_vector)
        confidence = max(probability[0]) * 100
        print("Confidence : {:.2f}%".format(confidence))

# ==========================
# User Input
# ==========================
article = input("Enter the article:\n\n")

predict_text(article)
