# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # This will load environment variables from .env file

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    GOLD_API_KEY = os.getenv("GOLD_API_KEY")
    GOLD_API_BASE_URL = "https://www.goldapi.io/api/XAU/USD"
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
