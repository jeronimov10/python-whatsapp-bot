from flask import Blueprint, request, jsonify, current_app
from app.utils.whatsapp_utils import WhatsAppHandler
from app.services.openai_service import OpenAIHandler
import logging

webhook_blueprint = Blueprint('webhook', __name__)

@webhook_blueprint.route('/webhook', methods=['GET'])
def verify():
    """Verify webhook connection"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == current_app.config["VERIFY_TOKEN"]:
            logging.info("Webhook verified successfully!")
            return challenge, 200
    return jsonify({"status": "error", "message": "Verification failed"}), 403

@webhook_blueprint.route('/webhook', methods=['POST'])
def webhook():
    """Process incoming messages"""
    try:
        data = request.get_json()

        # Verificar si hay mensajes
        if "messages" not in data["entry"][0]["changes"][0]["value"]:
            return jsonify({"status": "ok"}), 200  # No hay mensaje que procesar

        # Obtener datos del mensaje
        value = data["entry"][0]["changes"][0]["value"]
        message = value["messages"][0]

        if message["type"] == "text":  # ✅ Solo procesamos mensajes de texto
            phone_number = message["from"]
            text = message["text"]["body"]

            # Generar respuesta con OpenAI
            openai_handler = OpenAIHandler(api_key=current_app.config["OPENAI_API_KEY"])
            response_text = openai_handler.process_message(text)

            # Enviar respuesta a WhatsApp
            whatsapp_handler = WhatsAppHandler(
                access_token=current_app.config["WHATSAPP_ACCESS_TOKEN"],
                phone_number_id=current_app.config["PHONE_NUMBER_ID"],
                version=current_app.config["VERSION"]
            )
            whatsapp_handler.send_message(phone_number, response_text)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
