from flask import Flask, render_template, jsonify
from config import Config
from routes import main_bp
from utils import logger
from utils.constants import HTTP_PAYLOAD_TOO_LARGE, HTTP_INTERNAL_SERVER_ERROR

def create_app(config_class=Config) -> Flask:
    """Application factory creating and configuring Flask app instance."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Blueprints
    app.register_blueprint(main_bp)

    # Register Global Error Handlers
    @app.errorhandler(HTTP_PAYLOAD_TOO_LARGE)
    def payload_too_large(error):
        logger.warning(f"Request payload size limit exceeded: {error}")
        return render_template("index.html", error="Payload exceeds maximum allowed limit (10MB)."), HTTP_PAYLOAD_TOO_LARGE

    @app.errorhandler(HTTP_INTERNAL_SERVER_ERROR)
    def internal_server_error(error):
        logger.error(f"Internal server exception: {error}", exc_info=True)
        return render_template("index.html", error="An internal system error occurred."), HTTP_INTERNAL_SERVER_ERROR

    return app

app = create_app()

if __name__ == "__main__":
    logger.info(f"Starting Smart Fake News Identifier Application on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
