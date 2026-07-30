import os
from flask import Flask, render_template, request, jsonify
from config import Config
from services import PredictorService
from utils import logger

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Core Services
predictor_service = PredictorService()

@app.route("/", methods=["GET", "POST"])
def index():
    """Main Web Application UI Route."""
    result = None
    error = None

    if request.method == "POST":
        news_text = request.form.get("news", "").strip()
        force_gemini = request.form.get("force_gemini") == "true"

        logger.info(f"Received web prediction request. Text length: {len(news_text)}")
        
        response = predictor_service.analyze_news(news_text, force_gemini=force_gemini)

        if response.get("success"):
            result = response.get("prediction")
        else:
            error = response.get("error", "An unexpected error occurred.")

    return render_template("index.html", result=result, error=error)

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """REST API endpoint for programmatic Fake News Detection."""
    try:
        data = request.get_json(silent=True) or {}
        news_text = data.get("news", "").strip()
        force_gemini = bool(data.get("force_gemini", False))

        if not news_text:
            return jsonify({"success": False, "error": "Missing 'news' field in JSON payload."}), 400

        response = predictor_service.analyze_news(news_text, force_gemini=force_gemini)
        
        status_code = 200 if response.get("success") else 400
        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"API Endpoint Error: {e}", exc_info=True)
        return jsonify({"success": False, "error": f"Internal server error: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health():
    """Application Health Check endpoint."""
    return jsonify({
        "status": "healthy",
        "models": {
            "sklearn": predictor_service.sklearn_predictor.is_available(),
            "transformer": predictor_service.transformer_predictor.is_available()
        },
        "gemini_configured": predictor_service.gemini_service.is_configured()
    })

@app.errorhandler(413)
def request_entity_too_large(error):
    logger.warning(f"Payload size limit exceeded: {error}")
    return render_template("index.html", error="Payload exceeds maximum allowed limit (10MB)."), 413

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server exception: {error}", exc_info=True)
    return render_template("index.html", error="Internal system error occurred."), 500

if __name__ == "__main__":
    logger.info(f"Starting Smart Fake News Identifier on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
