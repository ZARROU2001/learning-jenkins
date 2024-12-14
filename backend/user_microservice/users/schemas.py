import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserSchema(BaseModel):
    uid: uuid.UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class UserCreateGoogleModel(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str

class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: EmailStr
    password: Optional[str] = Field(None, min_length=8)  # Make password optional

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "test",
                "last_name": "test",
                "username": "test",
                "email": "test@co.com",
                "password": "testpass123",  # Password is optional
            }
        }
    }


class UserUpdateModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    model_config = ConfigDict(
        str_max_length=40,
        str_min_length=2
    )


class UserResponse(BaseModel):
    uid: uuid.UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str


class PasswordModel(BaseModel):
    user: str
    password: str = Field(min_length=8)


class PasswordUpdateModel(BaseModel):
    password: str
    confirm_password: str
    old_password: str


class PasswordResetRequestModel(BaseModel):
    email: EmailStr


class WalletAddressRequest(BaseModel):
    wallet_address: str


class WalletAddressModel(BaseModel):
    wallet_address: str
    user_id: uuid.UUID


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
