from pydantic import BaseModel, Field

# Pydantic -> "내가 원하는 데이터 형식을 표현"
class Item(BaseModel):
    name: str
    price: int  # price가 int인지 보장

# 1. BaseModel을 이용해서 데이터를 class로 표현한다
# 2. 검증하고자 하는 데이터를 class에 넣어본다
    # class(...) / class.model_validate(dict)
# 3. 검증이 통과하면, 데이터를 사용
# 4. 실패하면, 에러처리

item = Item(name="apple", price="100")
item.model_dump()  # -> dict()
