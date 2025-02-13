from typing import Dict, Any, Optional
import requests
import json
import os
from app.services.file_handler import FileHandler


CONVERSATIONS_FILE = "data/conversations.json"

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
            elif message['type'] == 'image':
                message_data['media_id'] = message['image']['id']
                # Download and process image
                image_data = self._download_media(message_data['media_id'])
                if image_data:
                    message_data['file_data'] = image_data
            elif message['type'] == 'document':
                message_data['media_id'] = message['document']['id']
                # Download and process document
                doc_data = self._download_media(message_data['media_id'])
                if doc_data:
                    message_data['file_data'] = doc_data

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

    def _download_media(self, media_id: str) -> Optional[Dict[str, Any]]:
        """Download media from WhatsApp"""
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        # Get media URL
        response = requests.get(
            f"{self.base_url}/{media_id}",
            headers=headers
        )

        if response.status_code != 200:
            return None

        media_url = response.json().get('url')
        if not media_url:
            return None

        # Download media
        response = requests.get(media_url, headers=headers)
        if response.status_code != 200:
            return None

        # Process file using FileHandler
        # Note: You'll need to temporarily save the file or handle it in memory
        # This is a simplified version
        return {
            'content': response.content,
            'type': 'file',
            'metadata': {
                'mime_type': response.headers.get('content-type')
            }
        }
    
    def send_media(self, to: str, media_url: str, media_type: str, caption: Optional[str] = None) -> bool:
        """Envía un archivo a WhatsApp (imagen o documento)."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": media_type,
            media_type: {
                "link": media_url
            }
        }

        if caption:
            data[media_type]["caption"] = caption

        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=data
        )

        return response.status_code == 200
    
def save_message(phone_number, message):
    """Guarda los mensajes en un archivo JSON dentro de la carpeta 'data'."""
    file_path = "app/data/messages.json"

    # Crear el archivo si no existe
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump({}, f)

    # Leer los mensajes existentes
    with open(file_path, "r") as f:
        messages = json.load(f)

    # Agregar el nuevo mensaje
    if phone_number not in messages:
        messages[phone_number] = []
    messages[phone_number].append(message)

    # Guardar el archivo actualizado
    with open(file_path, "w") as f:
        json.dump(messages, f, indent=4)
