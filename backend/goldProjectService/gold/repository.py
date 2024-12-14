from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from gold.model import GoldPrice

async def save_gold_price(db: AsyncSession, price: float) -> GoldPrice:
    db_price = GoldPrice(price=price)
    db.add(db_price)
    await db.commit()
    await db.refresh(db_price)
    return db_price

async def get_latest_gold_price(db: AsyncSession) -> GoldPrice | None:
    result = await db.execute(select(GoldPrice).order_by(GoldPrice.timestamp.desc()).limit(1))
    return result.scalar_one_or_none()