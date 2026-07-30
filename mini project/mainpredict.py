import joblib
import re
import string

# Load AI/Human model
ai_model = joblib.load("ai_model.pkl")
ai_vectorizer = joblib.load("ai_vectorizer.pkl")

# Load Fake/True model
news_model = joblib.load("model.pkl")
news_vectorizer = joblib.load("vectorizer.pkl")

# Text preprocessing
def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

# Input
news = input("Enter the news article:\n")

# Preprocess
news = preprocess(news)

# ---------- Step 1 : AI or Human ----------
ai_vector = ai_vectorizer.transform([news])
ai_prediction = ai_model.predict(ai_vector)

# Change these labels according to your AI model
# If AI model: 0 = Human, 1 = AI
if ai_prediction[0] == 1:
    print("\n🤖 AI Generated Content")

else:
    print("\n👤 Human Written Content")

    # ---------- Step 2 : Fake or True ----------
    news_vector = news_vectorizer.transform([news])
    news_prediction = news_model.predict(news_vector)

    # Fake/True labels
    # 0 = Real
    # 1 = Fake
    if news_prediction[0] == 0:
        print("✅ True News")
    else:
        print("❌ Fake News")