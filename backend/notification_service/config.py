import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
    KAFKA_TRANSACTION_TOPIC = os.getenv("KAFKA_TRANSACTION_TOPIC")
    KAFKA_USER_TOPIC = os.getenv("KAFKA_USER_TOPIC")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:4200")
    SMTP_CODE = os.getenv("SMTP_CODE")
    SMTP_EMAIL = os.getenv("SMTP_EMAIL", "<EMAIL>")
    SMTP_PORT = os.getenv("SMTP_PORT", "587")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")

# Create a settings instance
Config = Settings()
