import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., json_schema_extra={"example": "Password123"})

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("비밀번호는 8자리 이상이어야 합니다.")    
        if not re.search(r"[A-Z]", v):
            raise ValueError("비밀번호에는 반드시 대문자가 포함되어야 합니다.")
        if not re.search(r"[0-9]", v):
            raise ValueError("비밀번호에는 반드시 숫자가 포함되어야 합니다.")
        return v

class LogInRequest(BaseModel):
    email: EmailStr
    password: str

class HeathProfileCreateRequest(BaseModel):
    age: int
    height_cm: float
    weight_kg: float
    smoking: bool
    exercise_per_week: int
