import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import Config
from consumers.sse_consumer import TransactionConsumer
from consumers.user_consumer import consume_user_events

consumer = TransactionConsumer(kafka_broker=Config.KAFKA_BROKER, kafka_topic=Config.KAFKA_TRANSACTION_TOPIC)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("test3")
    asyncio.create_task(consume_user_events())
    asyncio.create_task(consumer.start())
    print("test")
    yield
    # Shutdown logic (if needed) goes here


app = FastAPI(lifespan=lifespan)
