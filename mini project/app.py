from flask import Flask, render_template, request
import joblib
import re
import string
from news_api import verify_news

app = Flask(__name__)

# Load AI Detection Model
ai_model = joblib.load("ai_model.pkl")
ai_vectorizer = joblib.load("ai_vectorizer.pkl")


def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    confidence = ""
    gemini_result = ""

    if request.method == "POST":

        news = request.form["news"]
        clean = preprocess(news)

        # AI Detection
        ai_vector = ai_vectorizer.transform([clean])
        ai_prediction = ai_model.predict(ai_vector)[0]

        if hasattr(ai_model, "predict_proba"):
            ai_confidence = round(
                max(ai_model.predict_proba(ai_vector)[0]) * 100, 2
            )
        else:
            ai_confidence = "N/A"

        if ai_prediction == 1:
            result = "AI Generated News"
            confidence = f"{ai_confidence}%"
            gemini_result = ""

        else:
            result = "Human Written"
            confidence = f"{ai_confidence}%"
            gemini_result=verify_news(news)

            try:
                gemini_result = verify_news(news)
                print(" Output:", gemini_result)
            except Exception as e:
                gemini_result = f"Gemini Error: {e}"

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        gemini_result=gemini_result
    )


if __name__ == "__main__":
    app.run(debug=True)