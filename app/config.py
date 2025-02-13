import os
from dotenv import load_dotenv
import logging
import sys

def load_configurations(app):
    load_dotenv()
    app.config.update(
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
        WHATSAPP_ACCESS_TOKEN=os.getenv("WHATSAPP_ACCESS_TOKEN"),
        PHONE_NUMBER_ID=os.getenv("PHONE_NUMBER_ID"),
        APP_SECRET=os.getenv("APP_SECRET"),
        VERIFY_TOKEN=os.getenv("VERIFY_TOKEN"),
        VERSION=os.getenv("VERSION"),
        APP_ID=os.getenv("APP_ID"),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024
    )

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )