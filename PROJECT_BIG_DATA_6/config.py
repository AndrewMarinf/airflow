user="postgres"
password="9945"
host="127.0.0.1"
port="5432"
database="movies_"



from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Используем только реальные данные
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASS = "9945"
DB_NAME = "postgres"

# Создаем движок только один раз
DATABASE_URL = f'postgres+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(DATABASE_URL)

async_session_marker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass