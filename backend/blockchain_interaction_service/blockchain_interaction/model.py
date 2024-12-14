from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class TransactionHistory(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False)
    amount: float = Field(nullable=False)
    tx_type: str = Field(nullable=False)  # Adjust according to your type
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        )
    )
