from fastapi import FastAPI, Path


app = FastAPI()

@app.get("/items")
def items_api():
    return {
        "items": [
            {"id": 1, "name": "apple"},
            {"id": 2, "name": "banana"},
            {"id": 3, "name": "cherry"},
        ]
    }

@app.get("/items/search")
def search_api():
    return {"msg": "search"}

# Path Parameter
@app.get("/items/{item_id}")
def item_api(item_id: int = Path(..., ge=1)):
    return {"item": item_id}


# GET /items/{item_name}
# item_name: 문자열(str) & 최대 글자수(max_length) 6자
# 함수: item_name 출력
@app.get("/items/{item_name}")
def get_item(item_name: str = Path(..., max_length=6)):
    return {"item_name": item_name}
