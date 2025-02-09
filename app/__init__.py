from flask import Flask
from app.views import webhook_blueprint

def create_app():
    app = Flask(__name__)

    # Configurar Flask con el archivo de configuración
    app.config.from_object("app.config.Config")

    # Registrar Blueprints
    app.register_blueprint(webhook_blueprint)

    return app

