from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from nonce_metamask.model import WalletNonce


class AuthRepository:
    @staticmethod
    async def create_nonce(db: AsyncSession, wallet_address: str) -> WalletNonce:
        nonce = WalletNonce(wallet_address=wallet_address)
        db.add(nonce)
        await db.commit()
        await db.refresh(nonce)
        return nonce

    @staticmethod
    async def get_nonce(db: AsyncSession, wallet_address: str) -> WalletNonce:
        query = select(WalletNonce).where(WalletNonce.wallet_address == wallet_address)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def invalidate_nonce(db: AsyncSession, wallet_address: str):
        nonce = await AuthRepository.get_nonce(db, wallet_address)
        if nonce:
            nonce.used = True
            await db.commit()



