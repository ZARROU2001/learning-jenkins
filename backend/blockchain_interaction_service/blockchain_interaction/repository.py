from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from blockchain_interaction.model import TransactionHistory
from errors import DatabaseException

class TransactionRepository:
    async def add_transaction(self, transaction: TransactionHistory, db_session: AsyncSession) -> TransactionHistory:
        try:
            db_session.add(transaction)
            await db_session.commit()
            await db_session.refresh(transaction)
            return transaction
        except Exception as e:
            await db_session.rollback()
            raise DatabaseException(detail=f"Failed to add transaction: {e}")

    async def get_transaction_history(self, user_id: str, db_session: AsyncSession) -> list[TransactionHistory]:
        try:
            result = await db_session.execute(select(TransactionHistory).where(TransactionHistory.user_id == user_id))
            return result.scalars().all()
        except Exception as e:
            raise DatabaseException(detail=f"Failed to retrieve transaction history: {e}")
