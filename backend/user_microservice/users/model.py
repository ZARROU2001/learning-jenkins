from datetime import datetime
from typing import Optional

from sqlalchemy import func, DateTime
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid


class User(SQLModel, table=True):
    __tablename__ = "user_accounts"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    )

    username: str = Field(max_length=25)
    first_name: str = Field(nullable=True, max_length=25)
    last_name: str = Field(nullable=True, max_length=25)
    is_verified: bool = Field(default=False)
    email: str = Field(max_length=40, unique=True)
    password_hash: str
    wallet_address: Optional[str] = Field(
        max_length=42,  # For Ethereum addresses
        nullable=True,
        unique=True
    )
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        )
    )
    updated_at: Optional[datetime] = Field(sa_column=Column(
            DateTime(timezone=True),insert_default=func.now(), onupdate=func.now(), nullable=True
        ))

    def __repr__(self) -> str:
        return f"<User {self.username}>"
