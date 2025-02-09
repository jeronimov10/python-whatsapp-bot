from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = OPENAI_API_KEY

def generate_gpt4_response(user_message):
    """
    Envía un mensaje a GPT-4 Turbo y devuelve la respuesta generada.
    """
    try:
        response = OpenAI.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error con OpenAI: {e}")
        return "Hubo un error procesando tu solicitud."