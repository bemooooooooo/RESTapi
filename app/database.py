from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr
from app.config import get_db_url

DB_URL = get_db_url()
engine = create_async_engine(DB_URL)
session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs ,DeclarativeBase):
    __abstract__ = True
    
    @declared_attr.directive
    def __tablename__(cls)->str:
        return f"{cls.__name__.lower()}s"
    