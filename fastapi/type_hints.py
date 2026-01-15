# 변수 타입힌트
name: str = "alex"
price: int = 100
discount_ratio: float = 0.1
is_active: bool = True

score: int | float = 97.7

# 함수 타입힌트
def add(n1: int, n2: int) -> int:
    return n1 + n2

# 컬렉션 타입힌트
numbers: list[int] = [1, 2, 3]

scores: dict[str, int] = {"math": 90, "english": 80}

# 퀴즈
users: list[dict[str, int | str]] = [
    {"id": 1, "email": "alex@gmail.com"},
    {"id": 2, "email": "bob@gmail.com"},
    {"id": 3, "email": "chris@gmail.com"},
]

# 당첨자 결정
class User:
    pass


# Optional(=선택적) = 있을 수도 있고, 없을 수도 있다 <-> Required
당첨자: User | None = None

for u in users:
    if u.로그인횟수 >= 3:
        당첨자 = u
