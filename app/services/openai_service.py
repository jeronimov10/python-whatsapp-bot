from openai import OpenAI
import os
from typing import Dict, Any, Optional
import base64


MAX_FILE_SIZE = 5 * 1024 * 1024

class OpenAIHandler:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model_gpt4 = "gpt-3.5-turbo"
        self.model_vision = "gpt-4-vision-preview"

    def process_message(self, message_content: str, file_data: Optional[Dict[str, Any]] = None) -> str:
        """Process message with or without file attachment"""
        if file_data is None:
            return self._process_text_message(message_content)
        else:
            return self._process_file_message(message_content, file_data)

    def _process_text_message(self, message: str) -> str:
        """Process text-only messages"""
        response = self.client.chat.completions.create(
            model=self.model_gpt4,
            messages=[{"role": "user", "content": message}],
            max_tokens=4096
        )
        return response.choices[0].message.content

    def _process_file_message(self, message: str, file_data: Dict[str, Any]) -> str:
        """Procesa mensajes con archivos adjuntos, validando el tamaño."""
        if len(file_data['content']) > MAX_FILE_SIZE:
            return "❌ El archivo es demasiado grande. Solo se permiten archivos de hasta 5MB."

        if file_data['type'] == 'image':
            return self._process_image_message(message, file_data)

        content = self._prepare_file_content(message, file_data)
        response = self.client.chat.completions.create(
            model=self.model_gpt4,
            messages=[{"role": "user", "content": content}],
            max_tokens=4096
        )
        return response.choices[0].message.content

    def _process_image_message(self, message: str, file_data: Dict[str, Any]) -> str:
        """Process messages with image attachments"""
        image_b64 = base64.b64encode(file_data['content']).decode('utf-8')
        response = self.client.chat.completions.create(
            model=self.model_vision,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/{file_data['metadata']['format'].lower()};base64,{image_b64}"
                        }
                    ]
                }
            ],
            max_tokens=4096
        )
        return response.choices[0].message.content

    def _prepare_file_content(self, message: str, file_data: Dict[str, Any]) -> str:
        """Prepare content string based on file type and content"""
        file_content = file_data['content']
        if file_data['type'] == 'spreadsheet':
            file_content = str(file_data['content'])  # Convert dict to string
        
        return f"{message}\n\nFile Content:\n{file_content}"