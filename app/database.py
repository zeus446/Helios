from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

sessionLocal = sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

Base = declarative_base()


async def get_db():
  async with sessionLocal() as db:
    yield db