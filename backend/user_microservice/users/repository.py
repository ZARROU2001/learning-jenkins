import uuid
from typing import Optional, List

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from users.model import User
from users.schemas import UserUpdateModel


class UserRepository:
    async def get_user_by_id(self, user_id: uuid.UUID, session: AsyncSession) -> Optional[User]:
        try:
            result = await session.execute(select(User).where(User.uid == user_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            print(f"Error retrieving user by id: {e}")
            return None

    async def create_user(self, user_data: User, session: AsyncSession) -> Optional[User]:
        try:
            session.add(user_data)
            await session.flush()
            await session.refresh(user_data)
            await session.commit()
            return user_data
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Error creating user: {e}")
            return None
        except Exception as e:
            print(f"Error creating user: {e}")


    async def update_user(self, user: User, user_data: UserUpdateModel, session: AsyncSession) -> Optional[User]:
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        try:
            await session.flush()
            await session.refresh(user)
            await session.commit()
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Error updating user: {e}")
            return None

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        """
        Check if a user exists in the database by email.
        """
        try:
            user = await self.get_user_by_email(email, session)
            return user is not None
        except SQLAlchemyError as e:
            # Log specific SQLAlchemy errors
            print(f"SQLAlchemy error in UserRepository.user_exists: {e}")
            raise Exception("Database error while checking user existence")
        except Exception as e:
            # Log unexpected errors
            print(f"Unexpected error in UserRepository.user_exists: {e}")
            raise Exception("Unexpected error in repository method")

    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        """
        Fetch a user by email. Return None if not found.
        """
        try:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            # Log specific SQLAlchemy errors
            print(f"SQLAlchemy error in UserRepository.get_user_by_email: {e}")
            raise Exception("Database error while fetching user by email")

    async def get_all_users(self, session: AsyncSession, page: int = 1, page_size: int = 10) -> Optional[List[User]]:
        try:
            statement = select(User).order_by(User.uid).offset((page - 1) * page_size).limit(page_size)
            result = await session.execute(statement)
            return result.scalars().all()
        except SQLAlchemyError as e:
            print(f"Error retrieving all users: {e}")
            return None

    async def remove_user(self, user: User, session: AsyncSession) -> bool:
        try:
            result = await session.execute(delete(User).where(User.uid == user.uid))
            await session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Error deleting user: {e}")
            return False

    async def update_password(self, user_id: uuid.UUID, hashed_password: str, session: AsyncSession) -> bool:
        try:
            # Fetch the user object by user_id
            user = await session.execute(select(User).filter(User.uid == user_id))
            user = user.scalar()

            if not user:
                return False
            # Update password
            user.password_hash = hashed_password
            session.add(user)
            await session.commit()
            return True
        except SQLAlchemyError as e:
            # Rollback transaction in case of error
            await session.rollback()
            print(e)
            raise Exception("Error updating password", e)

    async def user_exists_by_wallet_address(self, wallet_address, session):
        """
                Fetch a user by wallet address. Return None if not found.
                """
        try:
            result = await session.execute(
                select(User).where(User.wallet_address == wallet_address)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            # Log specific SQLAlchemy errors
            print(f"SQLAlchemy error in UserRepository.get_user_by_email: {e}")
            raise Exception("Database error while fetching user by email")

    async def assign_wallet_address(self, user_id: uuid.UUID, wallet_address: str, session: AsyncSession) -> Optional['User']:
        """
        Assign a wallet address to a user. This function validates and assigns the wallet address
        to a user identified by user_id, ensuring the address is unique.

        Args:
            user_id (UUID): The user ID for whom the wallet address is to be assigned.
            wallet_address (str): The wallet address to assign.
            session (AsyncSession): A database session.

        Returns:
            User: The updated user object with the assigned wallet address, or raises an exception if assignment fails.
        """

        # Step 1: Validate the wallet address (uncomment when validation is needed)
        # if not self._is_valid_wallet_address(wallet_address):
        #     raise ValueError("Invalid wallet address format")

        # Step 2: Check if the wallet address is already in use by another user
        stmt = select(User).filter(User.wallet_address == wallet_address)
        try:
            result = await session.execute(stmt)
            existing_user = result.scalars().first()  # This should return a User object or None

            if existing_user:
                raise ValueError("Wallet address already assigned to another user")
        except Exception as e:
            raise ValueError(f"Error checking wallet address availability: {str(e)}")

        # Step 3: Retrieve the user to whom we will assign the wallet address
        stmt = select(User).filter(User.uid == user_id)
        try:
            result = await session.execute(stmt)
            user = result.scalars().first()  # This should return a User object or None

            if user:
                # Step 4: Assign the wallet address to the user
                user.wallet_address = wallet_address
                try:
                    # Commit the changes to the database
                    await session.commit()
                    return user  # This is a User object now
                except IntegrityError:
                    # Rollback in case of any database constraints violation
                    await session.rollback()
                    raise ValueError("Failed to assign wallet address due to a database error.")
            else:
                raise ValueError("User not found")
        except Exception as e:
            raise ValueError(f"Error retrieving user: {str(e)}")

