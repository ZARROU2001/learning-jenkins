import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from blockchain_interaction.kafka_consumer import consume_gold_price
from blockchain_interaction.routes import blockchain_router
from config import Config
from db.main import init_db
from errors import CustomHTTPException

# Ensure the environment is properly configured
if not Config.is_configured():
    raise EnvironmentError("Environment variables are not set correctly.")

async def on_price_received(price):
    # Update the smart contract when a new gold price is received
    #tx_hash = await update_gold_price(price)
    print(f"Transaction sent with hash: {price}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # Startup
    print("test3")
    asyncio.create_task(consume_gold_price(on_price_received))
    print("test")
    yield
    # Shutdown logic (if needed) goes here


app = FastAPI(lifespan=lifespan)



@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "message": exc.detail},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the error details for internal use
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": "An unexpected error occurred."},
    )
app.include_router(blockchain_router)