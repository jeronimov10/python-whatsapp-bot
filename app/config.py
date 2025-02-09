import os

class Config:
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    APP_ID = os.getenv("APP_ID")
    APP_SECRET = os.getenv("APP_SECRET")
    RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
    VERSION = os.getenv("VERSION", "v22.0")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
    OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")