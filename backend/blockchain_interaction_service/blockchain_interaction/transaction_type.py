from enum import Enum


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
