# main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.main import init_db
from gold.kafka_producer import stop_kafka_producer, start_kafka_producer
from gold.routes import gold_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await start_kafka_producer()
    yield
    # Shutdown logic (if needed) goes here
    await stop_kafka_producer()


app = FastAPI(lifespan=lifespan)
# Include the gold price routes
app.include_router(gold_router, prefix="/api")
