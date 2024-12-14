from datetime import datetime, timedelta
from eth_account.messages import encode_defunct
from eth_account import Account
from config import Config
from nonce_metamask.repository import AuthRepository
from utils import create_access_token


class NonceService:
    @staticmethod
    async def generate_nonce(db, wallet_address: str):
        return await AuthRepository.create_nonce(db, wallet_address)

    @staticmethod
    async def verify_signature(db, wallet_address: str, signed_message: str):
        nonce_entry = await AuthRepository.get_nonce(db, wallet_address)
        if not nonce_entry or nonce_entry.used or nonce_entry.expires_at < datetime.now():
            raise ValueError("Nonce invalid or expired")

        # Recreate message
        message = nonce_entry.nonce
        encoded_message = encode_defunct(text=message)

        # Verify signature
        recovered_address = Account.recover_message(encoded_message, signature=signed_message)
        if recovered_address.lower() != wallet_address.lower():
            raise ValueError("Invalid signature")

        # Invalidate nonce after use
        await AuthRepository.invalidate_nonce(db, wallet_address)

        token = create_access_token({"sub": wallet_address, "exp": datetime.now() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)})
        return token
