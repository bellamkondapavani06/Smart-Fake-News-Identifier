from flask import Flask, render_template, request
import joblib
import re
import string

app = Flask(__name__)

# Load AI/Human model
ai_model = joblib.load("ai_model.pkl")
ai_vectorizer = joblib.load("ai_vectorizer.pkl")

# Load True/Fake model
news_model = joblib.load("model.pkl")
news_vectorizer = joblib.load("vectorizer.pkl")


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

    if request.method == "POST":

        news = request.form["news"]

        clean = preprocess(news)

        # ---------------- AI/Human Prediction ----------------

        ai_vector = ai_vectorizer.transform([clean])

        ai_prediction = ai_model.predict(ai_vector)[0]

        # Confidence of AI model
        if hasattr(ai_model, "predict_proba"):
            ai_confidence = round(max(ai_model.predict_proba(ai_vector)[0]) * 100, 2)
        else:
            ai_confidence = None

        if ai_prediction == 1:

            result = " AI Generated News"
            confidence = ai_confidence

        else:

            # ---------------- Real/Fake Prediction ----------------

            news_vector = news_vectorizer.transform([clean])

            news_prediction = news_model.predict(news_vector)[0]

            if hasattr(news_model, "predict_proba"):
                news_confidence = round(max(news_model.predict_proba(news_vector)[0]) * 100, 2)
            else:
                news_confidence = None

            if news_prediction == 0:
                result = " Human Written - Real News"
            else:
                result = " Human Written - Fake News"

            confidence = news_confidence

    return render_template(
    "index.html",
    result=result,
    confidence=confidence
)


if __name__ == "__main__":
    app.run(debug=True)