from sqlmodel import SQLModel, Field
from datetime import datetime, timedelta
import secrets

class WalletNonce(SQLModel, table=True):
    wallet_address: str = Field(primary_key=True, index=True)
    nonce: str = Field(default_factory=lambda: secrets.token_hex(16), nullable=False)
    expires_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(minutes=10), nullable=False)
    used: bool = Field(default=False)


