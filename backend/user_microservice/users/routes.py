import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.logger import logger
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession

from db.main import get_session
from errors import UserNotFound, PasswordMismatch, InvalidCredentials
from users.schemas import UserCreateModel, UserSchema, UserUpdateModel, UserLoginModel, \
    PasswordUpdateModel, PasswordResetConfirmModel, WalletAddressRequest, WalletAddressModel, PasswordResetRequestModel, \
    UserCreateGoogleModel
from users.services import UserService

auth_router = APIRouter()
user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post(
    "/register",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_account(
        user_data: UserCreateModel,
        session: AsyncSession = Depends(get_session)
):
    return await user_service.create_user(user_data, session)

@auth_router.post(
    "/register/google",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_with_google_account(
        user_data: UserCreateGoogleModel,  # Frontend sends user data without password
        session: AsyncSession = Depends(get_session)
):
    return await user_service.create_user_with_google(user_data, session)


@auth_router.get(
    "/all",
    response_model=list[UserSchema],
    status_code=status.HTTP_200_OK
)
async def get_users(
        page: int = 1,
        page_size: int = 10,
        session: AsyncSession = Depends(get_session)
):
    return await user_service.get_all_users(session, page=page, page_size=page_size)


@auth_router.get(
    "/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK
)
async def get_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    return await user_service.get_user_by_id(user_id, session)


@auth_router.patch(
    "/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK
)
async def update_user(
        user_id: uuid.UUID,
        user_data: UserUpdateModel,
        session: AsyncSession = Depends(get_session)
):
    return await user_service.update_user(user_id, user_data, session)


@auth_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    return await user_service.delete_user(session, user_id)


@auth_router.post("/forget-password")
async def forget_password(email: PasswordResetRequestModel, session: AsyncSession = Depends(get_session)):
    try:
        return await user_service.forget_password(email.email, session)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The email address you entered does not exist. Please check your email or sign up for a new account."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while resetting the password. Please try again later."
        )

@auth_router.post("/reset-password")
async def reset_password(password: PasswordResetConfirmModel,token: Annotated[str, Depends(oauth2_scheme)] ,session:AsyncSession = Depends(get_session)):
    try:
        return await user_service.reset_password(password,token, session)
    except PasswordMismatch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The new password and confirmation password do not match. Please ensure both passwords are identical.",
        )
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The password reset token is invalid or expired. Please request a new password reset link.",
        )
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error in reset-password route: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while resetting your password. Please try again later.",
        )

@auth_router.post("/assign_wallet_address")
async def assign_wallet_address(
        wallet_model: WalletAddressModel,
        session: AsyncSession = Depends(get_session)
):
    """
    Endpoint to assign wallet address to a user.
    """
    try:
        result = await user_service.assign_wallet_address(wallet_model, session)
        return result  # Returning the result from the service
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail="An error occurred while assigning the wallet address")

@auth_router.post("/exist-by-wallet-address", status_code=status.HTTP_200_OK,response_model=UserSchema)
async def exist_by_wallet_address(
        model: WalletAddressRequest,
        session: AsyncSession = Depends(get_session)
):
    """
    Endpoint to check if a user exists by email.
    """
    try:
        user_exists = await user_service.exist_user_by_wallet_address(model.wallet_address, session)
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user_exists
    except HTTPException as e:
        # Re-raise the HTTPException for proper response formatting
        raise e
    except Exception as e:
        # Log unexpected errors for debugging
        print(f"Unexpected error in exist_by_email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while checking user existence"
        )


@auth_router.put("/update-password", status_code=status.HTTP_200_OK)
async def change_password(password: PasswordUpdateModel, session: AsyncSession = Depends(get_session),token : str = Depends(oauth2_scheme)):
    try:
        response = await user_service.update_password(token,password, session)
        return response
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidCredentials:
        raise InvalidCredentials("")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@auth_router.post("/users/verify_credentials",response_model=UserSchema)
async def verify_user_credentials(login_model: UserLoginModel, session: AsyncSession = Depends(get_session)):
    return await user_service.verify_user(login_model.email, login_model.password, session)


@auth_router.post("/existByEmail")
async def check_user_exists(
    email : PasswordResetRequestModel,
    db: AsyncSession = Depends(get_session),
):

    try:
        exists = await user_service.check_user_exists_by_email(email.email,db)
        return exists
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid email format")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="A database error occurred")