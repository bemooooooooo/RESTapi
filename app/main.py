from fastapi import FastAPI
from app.models.item import *
from app.database import session, engine
from typing import List

app = FastAPI()

@app.get("/api/getItemById/{item_id}", response_model=ResponseItem)
async def getItemById(item_id: int): 
    return await select(session, item_id)

@app.post("/api/postItem", response_model=ResponseItem)
async def postItem(posting_item: ResponseItem):
    return await insert(session, posting_item)

@app.delete("/api/deleteItemById", response_model=ResponseItem)
async def deleteItemById(item_id: int):
    return await delete(session, item_id)
    
@app.put("/api/updateItemById", response_model=ResponseItem)
async def updateItemById(item_id: int, new_item: ResponseItem):
    return await update(session, item_id, new_item)

@app.get("/api/sortItems", response_model=List[ResponseItem])
async def sortItems(comparator):
    return await sort(session, comparator)

@app.get("/api/filterItems", response_model=List[ResponseItem])
async def filterItems(condition: bool):
    return await filter(session, condition)

@app.get("/api/")
async def restApiHome():
    return {"message": "Hello on api, check home)"}

@app.get("/")
async def home():
    return {"message": "Hello!"}

async def init_models():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all())

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)