# 📰 Smart Fake News Identifier

An enterprise-grade, multi-stage **Fake News & AI-Generated Content Detection** system combining **Transformer Deep Learning models (RoBERTa / DeBERTa)**, **TF-IDF ML Ensembles**, and **Google Gemini API Automated Secondary Fact-Checking**.

Designed with **Clean Architecture**, **Input Sanitization**, **Centralized Preprocessing**, and **Configurable Verification Thresholds** to maximize real-world prediction accuracy without making false claims of 100% accuracy.

---

## 🌟 Key Features

1. **Multi-Model Intelligence**:
   - **Transformer Pipeline**: Evaluates fine-tuned sequence classification models (`RoBERTa` / `DeBERTa`) for deep semantic context and self-attention feature extraction.
   - **TF-IDF + Scikit-Learn Ensemble**: Dual-stage classifier detecting both **AI-generated text** vs **Human-written text** and **Fake News** vs **Real News**.
   - **Automatic Model Selection**: Dynamically routes requests to the highest-performing operational model.

2. **Automated Secondary Verification (Gemini API)**:
   - When primary model prediction confidence drops below a configurable threshold (e.g. **< 90%**) or when AI-generated text is detected, the system **automatically triggers real-world fact verification** using the Google Gemini API.

3. **Centralized & Robust Preprocessing**:
   - Strips & unescapes HTML tags, sanitizes URLs/emails, strips non-text emojis, normalizes whitespace, and handles punctuation cleanly without corrupting context.

4. **Production Security & Clean Architecture**:
   - **Input Validation**: Rejects payload sizes over limit, enforces min/max word counts, and filters XSS/Script injection.
   - **Environment Security**: All secrets and API keys are managed securely via `.env`.
   - **Structured Logging**: Application-wide logging formatted with console and file output (`app.log`).

5. **Modern Glassmorphic UI & REST API**:
   - Dynamic web interface displaying prediction labels, confidence progress bars, analysis explanations, model type badges, and secondary fact-checking cards.
   - Includes JSON REST API endpoints (`/api/predict`) and system health checks (`/health`).

---

## 📂 Project Architecture

```
Smart-Fake-News-Identifier/
├── app.py                      # Main Flask Web Application & REST API entrypoint
├── config.py                   # Central configuration & environment variables
├── requirements.txt            # Python dependencies
├── .env.example                # Template for environment variables
├── .gitignore                  # Exclusion rules for git
├── README.md                   # Complete system documentation
├── services/
│   ├── __init__.py
│   ├── predictor_service.py    # Main orchestrator (Model selection & thresholding)
│   ├── gemini_service.py       # Google Gemini API fact-checking verification service
│   └── news_fetcher_service.py # Live news fetcher (MediaStack API)
├── utils/
│   ├── __init__.py
│   ├── preprocessor.py         # Centralized text cleaning (HTML, URLs, emojis, whitespace)
│   ├── logger.py               # Structured application logger
│   └── validator.py            # Input validation, sanitization, & payload limit rules
├── models/
│   ├── __init__.py
│   ├── base_model.py           # Abstract Base Model interface
│   ├── transformer_model.py    # RoBERTa / DeBERTa sequence classification pipeline
│   ├── sklearn_model.py        # TF-IDF + Scikit-Learn classifier wrapper
│   ├── ai_model.pkl            # Pre-trained AI vs Human classifier
│   ├── ai_vectorizer.pkl       # Pre-trained AI TF-IDF vectorizer
│   ├── model.pkl               # Pre-trained Fake vs Real classifier
│   └── vectorizer.pkl          # Pre-trained Fake/Real TF-IDF vectorizer
├── templates/
│   └── index.html              # Modern glassmorphism UI template
└── static/
    ├── css/
    │   └── style.css           # Modern CSS styling, themes, & responsive layouts
    └── images/
        ├── image.jpeg
        └── images.jpeg
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.9+
- Recommended: Virtual environment (`venv`)

### 2. Install Dependencies
```bash
git clone https://github.com/bellamkondapavani06/Smart-Fake-News-Identifier.git
cd Smart-Fake-News-Identifier

# Create & activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```env
FLASK_SECRET_KEY=your_custom_secret_key
FLASK_DEBUG=True
PORT=5000
HOST=127.0.0.1

GEMINI_API_KEY=your_actual_google_gemini_api_key
GEMINI_CONFIDENCE_THRESHOLD=90.0
DEFAULT_MODEL_MODE=AUTO
```

---

## 🚀 Running the Application

### Launch Web Server
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

### CLI Interface (Terminal Mode)
```bash
python "Mini project/mainpredict.py"
```

---

## 📡 REST API Documentation

### 1. Predict News Veracity
- **Endpoint**: `POST /api/predict`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "news": "BREAKING: Scientists discover water ice on Mars equator...",
  "force_gemini": false
}
```
- **Response**:
```json
{
  "success": true,
  "error": null,
  "prediction": {
    "result": "Human Written - Real News",
    "confidence": "96.4%",
    "confidence_val": 96.4,
    "is_fake": false,
    "is_ai": false,
    "model_type": "TF-IDF + Scikit-Learn Classifier (Ensemble)",
    "explanation": "Text structure, vocabulary distribution, and stylistic markers align with verified real news articles.",
    "gemini_verification": {
      "triggered": false,
      "status": "Not Required",
      "reason": "Model prediction achieved high confidence (96.4% >= threshold 90.0%). Secondary verification not required."
    }
  }
}
```

### 2. Health Check
- **Endpoint**: `GET /health`
- **Response**:
```json
{
  "status": "healthy",
  "models": {
    "sklearn": true,
    "transformer": false
  },
  "gemini_configured": true
}
```

---

## 📊 Model & Dataset Information

- **Traditional ML Model**: Scikit-learn TF-IDF Vectorization paired with Logistic Regression & Passive Aggressive Classifiers trained on Fake/Real news datasets.
- **Transformer Model**: Hugging Face Sequence Classification (RoBERTa / DeBERTa architecture) providing contextual representations.
- **Secondary Fact-Checking**: Google Gemini 1.5 Flash (`gemini-flash-latest`) for real-world verification of ambiguous claims.

---

## 🔒 Security & Privacy

- No hardcoded API keys in source code.
- XSS and Script Injection filtering built into `utils/validator.py`.
- Strict request character and word count bounds.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
