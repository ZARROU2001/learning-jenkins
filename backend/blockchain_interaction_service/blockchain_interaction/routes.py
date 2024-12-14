from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from blockchain_interaction.repository import TransactionRepository
from blockchain_interaction.schemas import GoldPriceUpdateSchema, TransactionSchema, BuyTokensRequest, \
    SellTokensRequest, GasFeeRequest, BalanceRequest
from blockchain_interaction.services import BlockchainService
from config import Config
from db.main import get_session
from errors import CustomHTTPException, BlockchainException, ValidationException, UnauthorizedException

blockchain_router = APIRouter()
transaction_repo = TransactionRepository()
blockchain_service = BlockchainService(transaction_repo)


@blockchain_router.post("/update-gold-price")
async def update_gold_price(
        price_update: GoldPriceUpdateSchema
):
    if price_update.price <= 0:
        raise ValidationException("Gold price must be greater than zero.")

    try:
        await blockchain_service.update_gold_price(price_update.price, Config.OWNER_ADDRESS)
        return {"status": "Gold price updated successfully"}
    except UnauthorizedException as e:
        raise e
    except BlockchainException as e:
        raise e
    except Exception:
        raise CustomHTTPException(status_code=500, detail="An unexpected error occurred.")


@blockchain_router.post("/buy-tokens")
async def buy_tokens(
        buy_token: BuyTokensRequest,
        db: AsyncSession = Depends(get_session)
):
    try:
        tx_hash = await blockchain_service.buy_tokens(buy_token.account, buy_token.value, db)
        return {"status": "Tokens purchased", "transaction_hash": tx_hash}
    except BlockchainException as e:
        raise CustomHTTPException(status_code=500, detail=str(e))



@blockchain_router.post("/sell-tokens")
async def sell_tokens(
        sell_token :SellTokensRequest,
        db: AsyncSession = Depends(get_session)
):
    try:
        tx_hash = await blockchain_service.sell_tokens(sell_token.amount, sell_token.account, db)
        return {"status": "Tokens sold", "transaction_hash": tx_hash}
    except BlockchainException as e:
        raise CustomHTTPException(status_code=500, detail=str(e))

@blockchain_router.get("/getGoldPrice")
async def get_gold_price():
    try:
        # Call the synchronous function here
        gold_price = blockchain_service.get_gold_price()
        return {"gold_price": gold_price}
    except BlockchainException as e:
        raise CustomHTTPException(status_code=500, detail=str(e))

@blockchain_router.post("/estimate-gas-fee")
async def estimate_gas_fee(gas_fee : GasFeeRequest):
    try:
        gas_fee = await blockchain_service.calculate_gas_fee(gas_fee.account, gas_fee.eth_amount,gas_fee.action)
        return {"gas_fee": gas_fee}
    except BlockchainException as e:
        raise CustomHTTPException(status_code=500, detail=str(e))

@blockchain_router.get("/getBalance")
async def get_balance(account:BalanceRequest):
    try:
        balance = await blockchain_service.get_user_balance(account.account)
        balance_in_tokens = round(balance / 1e18,2)
        return {"balance": balance_in_tokens}
    except BlockchainException as e:
        raise CustomHTTPException(status_code=500, detail=str(e))


@blockchain_router.get("/transaction-history/{user_id}", response_model=list[TransactionSchema])
async def get_transaction_history(
        user_id: str,
        db: AsyncSession = Depends(get_session)
):
    try:
        return await blockchain_service.get_transaction_history(user_id, db)
    except BlockchainException as e:
        raise HTTPException(status_code=500, detail=str(e))
