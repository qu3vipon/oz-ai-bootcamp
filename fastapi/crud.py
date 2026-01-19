from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy import select

from connection_async import AsyncSessionFactory, get_async_session
from models import Item


app = FastAPI()

class ItemResponse(BaseModel):
    id: int
    name: str
    price: int

# C: 상품 등록 API
class ItemCreateRequest(BaseModel):
    name: str
    price: int

@app.post("/items", status_code=201)
async def create_item_api(
    body: ItemCreateRequest, 
    session = Depends(get_async_session),
) -> ItemResponse:
    new_item = Item(name=body.name, price=body.price)
    session.add(new_item) # DB에 저장할 애들을 선별 
    await session.commit()  # DB에 반영
    return new_item

# R: 전체 상품 조회 API
@app.get("/items", status_code=200)
async def get_items_api(session = Depends(get_async_session)) -> list[ItemResponse]:
    stmt = select(Item)  # statement = SQL 구문
    result = await session.execute(stmt) # 1) DB 조회
    items: list[Item] = result.scalars().all() # 2) Item 객체로 변환
    return items


# R: 단일 상품 조회 API
@app.get("/items/{item_id}", status_code=200)
async def get_item_api(item_id: int) -> ItemResponse:
    async with AsyncSessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        item: Item | None = result.scalar()
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        return item


# U: 상품 수정 API
class ItemUpdateRequest(BaseModel):
    name: str | None = None
    price: int | None = None

@app.patch("/items/{item_id}", status_code=200)
async def update_item_api(item_id: int, body: ItemUpdateRequest) -> ItemResponse:
    async with AsyncSessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        item: Item | None = result.scalar()
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        # 객체의 값을 변경하고 commit()하면, 그대로 데이터가 DB에 반영됨
        if body.name:
            item.name = body.name
        if body.price:
            item.price = body.price
        
        await session.commit()  # session에 등록된 데이터를 DB로 저장
        return item

# U: 상품 수정 API
class ItemReplaceUpdate(BaseModel):
    name: str
    price: int

@app.put("/items/{item_id}", status_code=200)
async def replace_item_api(item_id: int, body: ItemReplaceUpdate) -> ItemResponse:
    async with AsyncSessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        item: Item | None = result.scalar()
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        item.name = body.name
        item.price = body.price
        
        await session.commit()
        return item

# D: 상품 삭제 API
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_api(item_id: int) -> None:
    async with AsyncSessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
        item: Item | None = result.scalar()
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        await session.delete(item)
        await session.commit()
