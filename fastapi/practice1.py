from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class HelloRequest(BaseModel):
    name: str

class HelloResponse(BaseModel):
    message: str

@app.post("/hello")
def hello_api(body: HelloRequest) -> HelloResponse:
    if body.name.strip() == "":
        raise HTTPException(status_code=400, detail={"message": "이름을 입력하세요."})
    return {"message": f"안녕하세요, {body.name}님!"}
