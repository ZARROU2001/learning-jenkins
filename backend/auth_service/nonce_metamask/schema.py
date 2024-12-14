from pydantic import BaseModel

class LoginRequest(BaseModel):
    wallet_address: str

class VerifySignatureRequest(BaseModel):
    wallet_address: str
    signed_message: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
