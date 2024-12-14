from datetime import datetime

from pydantic import BaseModel, condecimal, field_validator


class TransactionSchema(BaseModel):
    user_id: str
    tx_type: str
    amount: condecimal(gt=0)  # Ensure amount is greater than 0
    created_at: datetime


class GoldPriceUpdateSchema(BaseModel):
    price: int  # Use float type for price

    @field_validator('price')
    def check_price_positive(cls, value: float):
        if value <= 0:
            raise ValueError('Price must be greater than 0')
        return value


class BuyTokensRequest(BaseModel):
    account: str
    value: int

class SellTokensRequest(BaseModel):
    account: str
    amount: int

class BalanceRequest(BaseModel):
    account: str

class GasFeeRequest(BaseModel):
    account: str
    eth_amount: float
    action: str  # "buy" or "sell"
