from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from db.main import get_session
from gold.kafka_producer import send_to_kafka
from gold.schemas import GoldPriceResponse
from gold.services import update_gold_price, fetch_gold_price

gold_router = APIRouter()


@gold_router.get("/gold-price", response_model=GoldPriceResponse)
async def get_current_gold_price(db: AsyncSession = Depends(get_session)):
    return await update_gold_price(db)


@gold_router.websocket("/ws/gold-price")
async def websocket_gold_price(websocket: WebSocket, db: AsyncSession = Depends(get_session)):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()  # Wait for a message from the client
            price = await fetch_gold_price()  # Fetch the latest price
            print(price)
            await send_to_kafka(price)  # Send price to Kafka
            await websocket.send_text(f"Current gold price: {price}")  # Send back to client
    except Exception as e:
        print(f"Error: {e}")
