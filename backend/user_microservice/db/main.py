from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.exc import SQLAlchemyError

from config import Config

# Initialize the asynchronous database engine
async_engine: AsyncEngine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

# Initialize the database (creates tables)
async def init_db() -> None:
    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

# Define a session factory for dependency injection in FastAPI
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency that provides a new session for each request
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

