import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")  # Replace with a secret key
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry in minutes
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    DATABASE_URL= os.getenv("DATABASE_URL")
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', default="http://user-service:8000")
    API_KEY = os.getenv("API_KEY")
    GOOGLE_CLIENT_ID= os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    FRONTEND_URL= os.getenv("FRONTEND_URL")
    MIDDLEWARE_SECRET_KEY= os.getenv("MIDDLEWARE_SECRET_KEY")
# Create a settings instance
Config = Settings()
