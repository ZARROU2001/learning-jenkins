import httpx
from fastapi import HTTPException, status
from sqlalchemy.testing.pickleable import User

from config import Config
from user_token.schemas import UserCreateModel


# Dependency to call the User Management Service
async def verify_user_credentials(username: str, password: str):
    payload = {"email": username, "password": password}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{Config.USER_SERVICE_URL}/users/verify_credentials", json=payload
        )  # Assume this endpoint exists
        if response.status_code == 200:
            user = response.json()
            return user
        return None


async def check_user_exists(email: str):
    """
    Calls the User Management Service to check if a user exists by email.
    Args:
        email (str): The email address to check.
    Returns:
        None if the user exists.
    Raises:
        HTTPException if the user does not exist or if there is an error.
    """
    url = f"{Config.USER_SERVICE_URL}/existByEmail"
    payload = {"email": email}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)

        if response.status_code == status.HTTP_200_OK:
            # User exists
            return response.json()
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            return None
        else:
            # Handle other unexpected statuses
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected response from User Service: {response.status_code}"
            )
    except httpx.RequestError as exc:
        # Handle connection errors
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to connect to User Service: {exc}"
        )

async def create_user(user_model: UserCreateModel):
    """
    Calls the User Management Service to create a user.
    Args:
        user_model (UserCreateModel): The user model to create.
    Returns:
        None if the user exists.
    Raises:
        HTTPException if the user does not exist or if there is an error.
    """
    url = f"{Config.USER_SERVICE_URL}/register/google"
    payload = {
        "username": user_model.username,
        "email": user_model.email,
        "first_name": user_model.first_name,
        "last_name": user_model.last_name,
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)

        if response.status_code == status.HTTP_201_CREATED:
            # User exists
            return response.json()
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else:
            # Handle other unexpected statuses
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected response from User Service: {response.status_code}"
            )
    except httpx.RequestError as exc:
        # Handle connection errors
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to connect to User Service: {exc}"
        )