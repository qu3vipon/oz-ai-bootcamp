from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, computed_field


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

class LogInResponse(BaseModel):
    access_token: str

class HealthProfileResponse(BaseModel):
    id: int
    user_id: int
    age: int
    height_cm: float
    weight_kg: float
    smoking: bool
    exercise_per_week: int

class HealthRiskPredictionResponse(BaseModel):
    id: int
    user_id: int
    diabetes_probability: float
    hypertension_probability: float
    # model_version -> 클라이언트에게 공개하지 않을 수 있음
    created_at: datetime
    
    @computed_field
    @property
    def created_at_kst(self) -> datetime:
        KST = timezone(timedelta(hours=9))
        # UTC 시간을 KST(+09:00)로 변환
        return self.created_at.astimezone(KST)
