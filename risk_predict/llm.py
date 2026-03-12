from openai import AsyncOpenAI
from pydantic import BaseModel

from config import settings
from database.orm import HealthProfile

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class RiskPredictionResult(BaseModel):
    diabetes_probability: float
    hypertension_probability: float

async def predict_health_risk(profile: HealthProfile, model_version: str) -> RiskPredictionResult:
    prompt = f"""
    다음 건강 정보를 기반으로 당뇨와 고혈압 위험도를 0과 1 사이로 계산하라.

    age: {profile.age}
    height_cm: {profile.height_cm}
    weight_kg: {profile.weight_kg}
    smoking: {profile.smoking}
    exercise_per_week: {profile.exercise_per_week}
    """

    response = await client.responses.parse(
        model=model_version,
        input=prompt,
        text_format=RiskPredictionResult,
    )
    return response.output_parsed
