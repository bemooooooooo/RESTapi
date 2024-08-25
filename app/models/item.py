from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select as SELECT, update as UPDATE, delete as DELETE, insert as INSERT
from app.database import Base
from pydantic import BaseModel
from typing import List

class Item(Base):

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, cost={self.cost})\n{self.name}: {self.description}" 
    
    id: Mapped[int] = mapped_column(primary_key=True ,unique=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str]
    
class ResponseItem(BaseModel):
    id: int
    name: str
    cost: int
    description: str


async def insert(async_session: async_sessionmaker[AsyncSession], item: Item)->Item:
    async with async_session() as session:
        statement = INSERT(Item).values(name=item.name, cost=item.cost, description=item.description)
        result = await session.execute(statement=statement)
        await session.commit()
        return result
            
async def select(async_session: async_sessionmaker[AsyncSession], item_id: int)->Item:
    async with async_session() as session:
        statement = SELECT(Item).where(Item.id==item_id)
        result = await session.execute(statement=statement)
        await session.commit()
        return result

async def update(async_session: async_sessionmaker[AsyncSession], old_item_id: int, new_item: Item)->Item:
    async with async_session() as session:
        statement = UPDATE(Item).values(id=new_item.id, name=new_item.name, cost=new_item.cost, description=new_item.description).where(Item.id==old_item_id)
        result = await session.execute(statement=statement)
        await session.commit()
        return result

async def delete(async_session: async_sessionmaker[AsyncSession], item_id: int)->Item:
    async with async_session() as session:
        statement = DELETE(Item).where(Item.id==item_id)
        result = await session.execute(statement=statement)
        await session.commit()
        return result
    
async def sort(async_session: async_sessionmaker[AsyncSession], comparator)->List[Item]:
    async with async_session() as session:
        return List(sort(await session.scalars(statement=SELECT(Item)), comparator=comparator))
    
async def filter(async_session: async_sessionmaker[AsyncSession], condition: bool)->List[Item]:
    async with async_session() as session:
        return List(await session.scalars(statement=SELECT(Item).where(condition)))
    