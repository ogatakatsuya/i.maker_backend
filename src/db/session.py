from lib.config import DB_CHARSET, env
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

ASYNC_DB_URL = f"mysql+aiomysql://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:3306/{env.DB_NAME}?charset={DB_CHARSET}"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
