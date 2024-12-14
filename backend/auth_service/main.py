from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from config import Config
from db.main import init_db
from user_token.routes import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # Startup
    yield
    # Shutdown logic (if needed) goes here


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=Config.MIDDLEWARE_SECRET_KEY)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
