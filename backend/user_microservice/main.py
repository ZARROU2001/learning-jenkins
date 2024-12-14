from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.main import init_db
from errors import register_all_errors
from users.routes import auth_router
from fastapi.middleware.cors import CORSMiddleware

version = "v1"

description = """
A REST API for a book review web service.

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
- Add tags to Books e.t.c.
    """

version_prefix = f"/api/{version}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # Startup
    yield
    # Shutdown logic (if needed) goes here

origins = [
    "http://localhost:4200"
]




app = FastAPI(
    title='user',
    description='A RESTful API for a user web service',
    version=version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_all_errors(app)  # add this line

app.include_router(auth_router, prefix=f"/api/{version}/users", tags=['users'])
