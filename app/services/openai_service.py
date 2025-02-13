from openai import OpenAI
import os
from typing import Dict, Any, Optional

class OpenAIHandler:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model_gpt3 = "gpt-3.5-turbo"  # ✅ Cambiamos el modelo a GPT-3.5 Turbo

    def process_message(self, message_content: str) -> str:
        """Process text-only messages"""
        response = self.client.chat.completions.create(
            model=self.model_gpt3,  # ✅ Usamos GPT-3.5 Turbo
            messages=[{"role": "user", "content": message_content}],
            max_tokens=1024
        )
        return response.choices[0].message.content

    # ❌ Desactivamos el código relacionado con imágenes y archivos
    # def _process_image_message(self, message: str, file_data: Dict[str, Any]) -> str:
    #     pass  # ❌ Comentar esta función porque GPT-3.5 no procesa imágenes

    # def _prepare_file_content(self, message: str, file_data: Dict[str, Any]) -> str:
    #     pass  # ❌ Comentar también esto porque no leeremos archivos ahora
