from pydantic import BaseModel
from datetime import datetime

class GoldPriceResponse(BaseModel):
    price: float
    timestamp: datetime
