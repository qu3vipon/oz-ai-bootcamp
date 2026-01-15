from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()

# Request Body: 데이터의 형식을 표현 -> Pydantic
# 예: 아이템 {name: "apple", price: 100}
class ItemCreateRequest(BaseModel):
    name: str
    price: int
    description: str | None = None

# FastAPI: return Python -> JSON

# 상품 등록 API
@app.post("/items")
def create_item_api(body: ItemCreateRequest):
    return {
        "name": body.name, 
        "price": body.price,
        "description": body.description,
    }
