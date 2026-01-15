from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class UserSignUpRequest(BaseModel):
    email: str
    password: str

# pydantic -> 데이터의 형식을 보장
class UserSignUpResponse(BaseModel):
    id: int
    email: str

# 회원가입 API
@app.post(
    "/users/sign-up", 
    status_code=201,
    summary="회원가입 API",
    description="Request (email, password) -> Return (id, email)",
)
def sign_up_api(body: UserSignUpRequest) -> UserSignUpResponse:
    # 이메일 중복검사 & db 저장
    return {
        "id": 1,
        "email": body.email,
        "password": body.password
    }
