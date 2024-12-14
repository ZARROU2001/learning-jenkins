import uuid
from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from errors import UserNotFound, UserAlreadyExists, InvalidCredentials, PasswordMismatch
from producer.kafka_producer import send_email_notification
from users.model import User
from users.repository import UserRepository
from users.schemas import UserCreateModel, UserUpdateModel, PasswordUpdateModel, WalletAddressRequest, \
    WalletAddressModel, UserCreateGoogleModel
from users.utils import generate_password_hash, validate_password, verify_password, create_password_reset_token, \
    send_password_reset_email, validate_passwords_match, verify_password_reset_token, verify_token


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    # Get All Users
    async def get_all_users(self, session: AsyncSession, page: int = 1, page_size: int = 10):
        return await self.user_repository.get_all_users(session, page, page_size)

    # **Get a User**
    async def get_user_by_id(self, user_id: uuid.UUID, session: AsyncSession):
        user = await self.user_repository.get_user_by_id(user_id, session)
        if not user:
            raise UserNotFound(f"User with id {user_id} not found")
        return user

    # **Create A User**
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        validate_password(user_data.password)  # Validate password strength
        if await self.user_repository.user_exists(user_data.email, session):
            raise UserAlreadyExists("User with this email already exists")

        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password_hash = generate_password_hash(user_data_dict["password"])
        return await self.user_repository.create_user(new_user, session)

    async def create_user_with_google(self, user_data: UserCreateGoogleModel, session: AsyncSession):
        # Create user data, bypassing password as it’s not needed for Google login
        user_data_dict = user_data.model_dump()

        # Create a new user object (no password needed)
        new_user = User(**user_data_dict)

        # Set default password hash to None as password is not required for Google login
        new_user.password_hash = ""

        # Create the user record in the database
        return await self.user_repository.create_user(new_user, session)

    # **Update A User**
    async def update_user(self, user_id: uuid.UUID, user_data: UserUpdateModel, session: AsyncSession):
        user = await self.get_user_by_id(user_id, session)
        if await self.user_repository.user_exists(user_data.email, session):
            raise UserAlreadyExists("User with this email already exists")
        return await self.user_repository.update_user(user, user_data, session)

    # **Delete A User**
    async def delete_user(self, session: AsyncSession, user_id: uuid.UUID):
        user = await self.get_user_by_id(user_id, session)
        return await self.user_repository.remove_user(user, session)

    async def verify_user(self, username: str, password: str, session: AsyncSession):
        user = await self.user_repository.get_user_by_email(username, session)
        if not user:
            raise UserNotFound(f"User with username {username} not found")
        if verify_password(password, user.password_hash):
            return user
        else:
            raise InvalidCredentials()

    async def exist_user_by_wallet_address(self, wallet_address: str, session: AsyncSession) -> bool:
        """
        Service method to check if a user exists by email.
        """
        try:
            return await self.user_repository.user_exists_by_wallet_address(wallet_address, session)
        except Exception as e:
            # Log the error for debugging
            print(f"Error in UserService.exist_user_by_wallet_address: {e}")
            raise Exception("Service error while checking user existence")

    # Service function to reset user password
    async def update_password(self, token: str, password: PasswordUpdateModel, session: AsyncSession):
        """Reset the user's password by updating the hashed password in the database"""
        if not validate_passwords_match(password.password, password.confirm_password):
            raise PasswordMismatch("The new password and confirmation password do not match.")
        # Fetch the user from the repository
        user_id = verify_token(token)
        user = await self.user_repository.get_user_by_id(uuid.UUID(user_id.get("sub")), session)
        if not user:
            raise UserNotFound(f"User with ID {user_id} not found")
        if not verify_password(password.old_password, user.password_hash):
            raise InvalidCredentials("old password is not correct")
        # Hash the new password
        hashed_password = generate_password_hash(password.password)
        print("test service")
        # Update password in the repository
        success = await self.user_repository.update_password(user.uid, hashed_password, session)
        if not success:
            raise Exception("Failed to update password in the database")
        await send_email_notification("update_password",user.email,user.username)
        return {"message": "Password updated successfully"}

    async def forget_password(self, email: str, session: AsyncSession):
        user = await self.user_repository.get_user_by_email(email, session)
        if not user:
            raise UserNotFound(f"User with email {email} not found")
        reset_token = create_password_reset_token(user.uid, email)
        send_password_reset_email(email, reset_token)
        return {"message": "Password reset email sent successfully"}

    async def reset_password(self, password, token: str, session):
        if not validate_passwords_match(password.new_password, password.confirm_new_password):
            raise PasswordMismatch("The new password and confirmation password do not match.")

        user_id = verify_password_reset_token(token)
        if not user_id:
            raise InvalidCredentials("The password reset token is invalid or expired.")

        hash_pass = generate_password_hash(password.new_password)
        await self.user_repository.update_password(uuid.UUID(user_id), hash_pass, session)
        return {"message": "Password updated successfully"}

    async def assign_wallet_address(self, wallet_model: WalletAddressModel, session: AsyncSession):
        """
        Service method to assign a wallet address to a user.
        This method validates the user and the wallet address.

        Args:
            wallet_model (WalletAddressModel): The wallet address and user ID.
            session (AsyncSession): The database session.

        Returns:
            dict: A success message.
        """
        user = await self.user_repository.get_user_by_id(wallet_model.user_id, session)
        if not user:
            raise UserNotFound(f"User with ID {wallet_model.user_id} not found")

        # Call the repository to assign the wallet address
        try:
            result = await self.user_repository.assign_wallet_address(
                wallet_model.user_id, wallet_model.wallet_address, session
            )
            return result
        except ValueError as e:
            raise ValueError(f"Invalid wallet address: {e}")


    async def check_user_exists_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        try:
            user = await self.user_repository.get_user_by_email(email, session)
            if user:
                return user  # Return the User object if found
            return None  # Explicitly return None if the user does not exist
        except RuntimeError as e:
            # Add more context to the error for higher layers
            raise RuntimeError("Failed to check user existence") from e


