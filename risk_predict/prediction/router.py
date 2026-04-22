from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select

from auth.jwt import verify_user
from database.connection import get_session
from user.models import HealthProfile
from prediction.llm import predict_health_risk
from prediction.models import HealthRiskPrediction


router = APIRouter(tags=["Prediction"])

@router.post(
    "/predictions",
    summary="당뇨병/고혈압 위험도 예측 API",
    status_code=status.HTTP_201_CREATED,
)
async def predict_health_risk_handler(
    user_id = Depends(verify_user),
    session = Depends(get_session),
):
    # 1) 건강 프로필 조회
    stmt = (
        select(HealthProfile)
        .where(HealthProfile.user_id == user_id)
    )
    result = await session.execute(stmt)
    profile = result.scalar()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="건강 프로필이 없습니다."
        )

    # 2) 위험도 예측
    model_version = "gpt-5-mini"
    risk_prediction = await predict_health_risk(
        profile=profile, model_version=model_version
    )

    # 3) 결과를 저장
    new_prediction = HealthRiskPrediction(
        user_id=user_id,
        diabetes_probability=risk_prediction.diabetes_probability,
        hypertension_probability=risk_prediction.hypertension_probability,
        model_version=model_version
    )
    session.add(new_prediction)
    await session.commit()
    await session.refresh(new_prediction)

    return new_prediction
