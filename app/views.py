from flask import Blueprint, request, jsonify, current_app
from .decorators.security import signature_required
import logging
import os
import json
from datetime import datetime

webhook_blueprint = Blueprint('webhook', __name__)

### 📌 FUNCIÓN PARA GUARDAR MENSAJES EN UN JSON ###
def save_message(phone_number, message, response):
    """Guarda cada conversación en un JSON dentro de la carpeta /data"""
    messages_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "phone_number": phone_number,
        "user_message": message,
        "bot_response": response
    }

    log_file = os.path.join("data", "messages.json")

    try:
        if not os.path.exists("data"):
            os.makedirs("data")

        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        else:
            data = []

        data.append(messages_log)

        with open(log_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    except Exception as e:
        logging.error(f"Error saving message: {e}")

### ✅ RUTA PARA VERIFICAR EL WEBHOOK ###
@webhook_blueprint.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == current_app.config["VERIFY_TOKEN"]:
            logging.info("Webhook verified successfully!")
            return challenge, 200
        return jsonify({"status": "error", "message": "Verification failed"}), 403
    return jsonify({"status": "error", "message": "Missing parameters"}), 400

### ✅ RUTA PARA PROCESAR LOS MENSAJES ENVIADOS A WHATSAPP ###
@webhook_blueprint.route('/webhook', methods=['POST'])
@signature_required
def webhook():
    try:
        data = request.get_json()

        # ✅ Manejo de actualizaciones de estado de WhatsApp
        if "statuses" in data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
            return jsonify({"status": "ok"}), 200

        # ✅ Obtener instancias de los servicios desde `current_app`
        whatsapp_service = current_app.whatsapp_service
        openai_handler = current_app.openai_handler

        # ✅ Procesar mensaje entrante
        message_data = whatsapp_service.process_incoming_message(data)
        if not message_data:
            return jsonify({"status": "error", "message": "Invalid message data"}), 400

        # ✅ Generar respuesta con OpenAI
        response = openai_handler.process_message(
            message_content=message_data.get('content', ''),
            file_data=message_data.get('file_data')
        )

        # ✅ Enviar respuesta por WhatsApp
        whatsapp_service.send_message(
            to=message_data['phone_number'],
            content=response
        )

        # ✅ Guardar la conversación en JSON
        save_message(message_data['phone_number'], message_data.get('content', ''), response)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
