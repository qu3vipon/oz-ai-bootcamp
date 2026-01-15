from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from connection import SessionFactory
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
def create_item_api(body: ItemCreateRequest) -> ItemResponse:
    with SessionFactory() as session:
        new_item = Item(name=body.name, price=body.price)
        session.add(new_item)
        session.commit()  # DB에 반영
        return new_item

# R: 전체 상품 조회 API
@app.get("/items", status_code=200)
def get_items_api() -> list[ItemResponse]:
    with SessionFactory() as session:
        stmt = select(Item)  # statement = SQL 구문
        items = session.scalars(stmt).all()
        return items

# R: 단일 상품 조회 API
@app.get("/items/{item_id}", status_code=200)
def get_item_api(item_id: int) -> ItemResponse:
    with SessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        item: Item | None = session.scalar(stmt)
        
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
def update_item_api(item_id: int, body: ItemUpdateRequest) -> ItemResponse:
    with SessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        item: Item | None = session.scalar(stmt)
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        # 객체의 값을 변경하고 commit()하면, 그대로 데이터가 DB에 반영됨
        if body.name:
            item.name = body.name
        if body.price:
            item.price = body.price
        
        session.commit()  # session에 등록된 데이터를 DB로 저장
        return item

# U: 상품 수정 API
class ItemReplaceUpdate(BaseModel):
    name: str
    price: int

@app.put("/items/{item_id}", status_code=200)
def replace_item_api(item_id: int, body: ItemReplaceUpdate) -> ItemResponse:
    with SessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        item: Item | None = session.scalar(stmt)
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        item.name = body.name
        item.price = body.price
        
        session.commit()
        return item


# D: 상품 삭제 API
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_api(item_id: int) -> None:
    with SessionFactory() as session:
        stmt = select(Item).where(Item.id == item_id)
        item: Item | None = session.scalar(stmt)
        
        if item is None:
            raise HTTPException(
                status_code=404, detail=f"Item Not Found(id: {item_id})",
            )
        
        session.delete(item)
        session.commit()
