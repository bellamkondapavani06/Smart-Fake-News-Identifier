# 📰 Smart Fake News Identifier - Production Flask Architecture

An enterprise-grade **Fake News & AI-Generated Content Detection System** refactored into a production-ready Flask application architecture with **Transformer Deep Learning (RoBERTa / DeBERTa)**, **TF-IDF ML Ensembles**, and **Google Gemini API Automated Secondary Fact Verification**.

---

## 📁 Blueprint Folder Structure

```text
Smart-Fake-News-Identifier/
│
├── app.py                      # Application Factory & Global Error Handlers
├── config.py                   # Centralized Configuration loading from .env
├── requirements.txt            # Package Dependencies
├── README.md                   # Complete Documentation
├── .env.example                # Sample Environment Variables
├── .gitignore                  # Git Exclusion Rules
│
├── models/                     # ML / DL Models & Predictor Wrappers
│   ├── model.pkl
│   ├── vectorizer.pkl
│   ├── ai_model.pkl
│   ├── ai_vectorizer.pkl
│   ├── base_model.py
│   ├── sklearn_model.py
│   └── transformer_model.py
│
├── services/                   # Modular Business Logic Layer
│   ├── __init__.py
│   ├── prediction_service.py   # Primary Prediction Orchestrator & Model Manager
│   ├── gemini_service.py      # Google Gemini API Fact-Checking Integration
│   ├── factcheck_service.py   # Secondary Fact-Checking Pipeline
│   └── preprocessing_service.py # Centralized Text Preprocessing Service
│
├── routes/                     # Presentation / HTTP Routing Layer (Blueprint)
│   ├── __init__.py
│   └── main_routes.py         # Presentation endpoints (Zero business logic in routes)
│
├── utils/                      # Application Utilities & Helpers
│   ├── __init__.py
│   ├── logger.py              # Logging setup writing to logs/app.log
│   ├── validators.py          # Request validation & sanitization
│   ├── helpers.py             # Response formatting & helper functions
│   └── constants.py           # Constants, status codes, & prediction labels
│
├── templates/                  # HTML Templates
│   └── index.html             # Glassmorphic UI layout
├── static/                     # Static CSS & Images
│   ├── css/style.css
│   └── images/
├── logs/                       # Application Logs
│   └── app.log
└── tests/                      # Automated Unit & Integration Tests
    ├── __init__.py
    └── test_services.py
```

---

## ⚙️ Configuration & Environment Variables

All configurable settings are stored in `config.py` and `.env`.

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Example `.env` settings:
```env
FLASK_SECRET_KEY=production-secret-key-change-me
DEBUG=False
PORT=5000
HOST=127.0.0.1
MAX_CONTENT_LENGTH=10485760

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_CONFIDENCE_THRESHOLD=90.0
DEFAULT_MODEL_MODE=AUTO

LOG_LEVEL=INFO
```

---

## 🚀 Installation & How to Run

### 1. Install Dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run Application
```bash
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

### 3. Run Automated Tests
```bash
python -m unittest discover tests
```

---

## 📡 REST API Documentation

### 1. Fake News Detection
`POST /api/predict` (Headers: `Content-Type: application/json`)
```json
{
  "news": "BREAKING: NASA James Webb Telescope confirms discovery of liquid water on Mars equator...",
  "force_gemini": false
}
```

Response:
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
`GET /health`

---

## 🧠 Model Details

1. **Transformer Model (`TransformerPredictor`)**: Sequence classification model (`RoBERTa` / `DeBERTa`) analyzing contextual self-attention representations.
2. **TF-IDF ML Ensemble (`SKLearnPredictor`)**: Dual-stage classifier predicting:
   - **AI Generated** vs **Human Written**
   - **Real News** vs **Fake News**
3. **Secondary Fact-Checking (`GeminiService`)**: Automatically invoked when prediction confidence < 90% or when AI-generated text is detected.

---

## 🔮 Future Improvements

- Add caching layer (Redis) for repeated URL / claim lookups.
- Integrate multi-language news translation prior to classification.
- Support batch news prediction API endpoints.
