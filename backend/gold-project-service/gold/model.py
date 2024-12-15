from sqlmodel import SQLModel, Field
from datetime import datetime

class GoldPrice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)