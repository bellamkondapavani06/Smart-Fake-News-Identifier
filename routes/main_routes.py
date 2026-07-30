from flask import Blueprint, render_template, request, jsonify
from services import PredictionService
from utils import logger, format_api_response
from utils.constants import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INTERNAL_SERVER_ERROR

main_bp = Blueprint("main", __name__)
prediction_service = PredictionService()

@main_bp.route("/", methods=["GET", "POST"])
def index():
    """Renders main application Web UI."""
    result = None
    error = None

    if request.method == "POST":
        news_text = request.form.get("news", "").strip()
        force_gemini = request.form.get("force_gemini") == "true"

        logger.info(f"UI POST request received. Input size: {len(news_text)}")
        response = prediction_service.analyze_news(news_text, force_gemini=force_gemini)

        if response.get("success"):
            result = response.get("prediction")
        else:
            error = response.get("error", "An unexpected error occurred.")

    return render_template("index.html", result=result, error=error)

@main_bp.route("/api/predict", methods=["POST"])
def api_predict():
    """REST API endpoint for Fake News Prediction."""
    try:
        data = request.get_json(silent=True) or {}
        news_text = data.get("news", "").strip()
        force_gemini = bool(data.get("force_gemini", False))

        logger.info("API POST /api/predict request received.")
        
        if not news_text:
            payload, status = format_api_response(
                success=False,
                error="Missing required 'news' parameter in JSON payload.",
                status_code=HTTP_BAD_REQUEST
            )
            return jsonify(payload), status

        response = prediction_service.analyze_news(news_text, force_gemini=force_gemini)
        
        status_code = HTTP_OK if response.get("success") else HTTP_BAD_REQUEST
        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error in /api/predict route: {e}", exc_info=True)
        payload, status = format_api_response(
            success=False,
            error=f"Internal server error: {str(e)}",
            status_code=HTTP_INTERNAL_SERVER_ERROR
        )
        return jsonify(payload), status

@main_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint returning system component status."""
    return jsonify({
        "status": "healthy",
        "models": {
            "sklearn": prediction_service.sklearn_predictor.is_available(),
            "transformer": prediction_service.transformer_predictor.is_available()
        },
        "gemini_configured": prediction_service.factcheck_service.gemini_service.is_configured()
    }), HTTP_OK
