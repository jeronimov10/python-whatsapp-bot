from flask import Blueprint, request, jsonify, current_app
import logging
from app.utils.whatsapp_utils import process_whatsapp_message

# Crear el blueprint del webhook
webhook_blueprint = Blueprint("webhook_blueprint", __name__)

@webhook_blueprint.route("/webhook", methods=["GET", "POST"])
def webhook():
    """
    Webhook para recibir mensajes de WhatsApp.
    """
    if request.method == "GET":
        # Verificación inicial del webhook en Meta Developer
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if verify_token == current_app.config["VERIFY_TOKEN"]:
            return challenge, 200
        return "Verification token mismatch", 403

    if request.method == "POST":
        data = request.get_json()
        logging.info(f"📩 Mensaje recibido: {data}")

        if data and "entry" in data:
            # Procesar el mensaje entrante de WhatsApp
            process_whatsapp_message(data)

        return jsonify({"status": "received"}), 200
