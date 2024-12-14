import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Default SQLite URL
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry in minutes
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:4200")
    SMTP_CODE = os.getenv("SMTP_CODE", "smtp.gmail.com:587")
    SMTP_EMAIL = os.getenv("SMTP_EMAIL", "<EMAIL>")
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
    KAFKA_USER_TOPIC = os.getenv("KAFKA_USER_TOPIC", "test")
    KAFKA_TRANSACTION_TOPIC = os.getenv("KAFKA_TRANSACTION_TOPIC", "test")




# Create a settings instance
Config = Settings()
