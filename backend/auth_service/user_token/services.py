from authlib.integrations.starlette_client import OAuth
from fastapi import HTTPException

from config import Config as Settings
from starlette.config import Config
from user_token.dependecy import verify_user_credentials
from user_token.schemas import UserLoginModel
from utils import create_access_token, create_refresh_token


async def authenticate_user(login_request: UserLoginModel):
    # Verify user credentials using User Management Service
    user = await verify_user_credentials(login_request.email, login_request.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print(user)
    # Create and return JWT tokens
    access_token = create_access_token(data={"sub": user["uid"]})
    refresh_token = create_refresh_token(data={"sub": user["uid"]})

    return access_token, refresh_token


config_data = {'GOOGLE_CLIENT_ID': Settings.GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': Settings.GOOGLE_CLIENT_SECRET}

starlette_config = Config(environ=config_data)

oauth = OAuth(starlette_config)

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)
