from flask import Flask
from .config import load_configurations, configure_logging
from .views import webhook_blueprint
from .utils.whatsapp_utils import WhatsAppHandler
from .services.openai_service import OpenAIHandler

def create_app():
    app = Flask(__name__)
    load_configurations(app)
    configure_logging()
    app.register_blueprint(webhook_blueprint)

    # Inicializar servicios
    app.whatsapp_service = WhatsAppHandler(
        access_token=app.config["WHATSAPP_ACCESS_TOKEN"],
        phone_number_id=app.config["PHONE_NUMBER_ID"],
        version=app.config["VERSION"]
    )
    app.openai_handler = OpenAIHandler(
        api_key=app.config["OPENAI_API_KEY"]
    )

    return app


