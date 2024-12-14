from typing import List

from pydantic import BaseModel, Field, EmailStr


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=25)
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "test",
                "last_name": "test",
                "username": "test",
                "email": "test@co.com",
                "password": "testpass123",
            }
        }
    }


# Response schema for login
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class EmailModel(BaseModel):
    addresses: List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
    token : str

class PasswordUpdateModel(BaseModel):
    password: str
    confirm_password: str
    old_password: str