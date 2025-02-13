from typing import Dict, Any, Optional
import requests
import json
import os

class WhatsAppHandler:
    def __init__(self, access_token: str, phone_number_id: str, version: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.version = version
        self.base_url = f"https://graph.facebook.com/{version}/{phone_number_id}"

    def process_incoming_message(self, body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process incoming WhatsApp message"""
        try:
            entry = body['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            message = value['messages'][0]

            message_data = {
                'phone_number': message['from'],
                'message_id': message['id'],
                'timestamp': message['timestamp'],
                'type': message['type']
            }

            if message['type'] == 'text':
                message_data['content'] = message['text']['body']

            # ❌ Desactivamos el manejo de archivos adjuntos
            # elif message['type'] == 'image':
            #     message_data['media_id'] = message['image']['id']
            # elif message['type'] == 'document':
            #     message_data['media_id'] = message['document']['id']

            return message_data
        except Exception as e:
            print(f"Error processing message: {e}")
            return None

    def send_message(self, to: str, content: str) -> bool:
        """Send WhatsApp message"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"body": content}
        }

        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=data
        )

        return response.status_code == 200

