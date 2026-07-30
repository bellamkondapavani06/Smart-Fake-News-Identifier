import joblib
import re
import string

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Text preprocessing
def preprocess(text):

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Get input from user
news = input("Enter the news article:\n")

# Preprocess
news = preprocess(news)

# Convert to TF-IDF
news_vector = vectorizer.transform([news])

# Predict
prediction = model.predict(news_vector)
print("Prediction:",prediction)

# Display result
if prediction[0] == 0:
    print("\n Real News")
if prediction[0] ==1:
    print("\n Fake News")