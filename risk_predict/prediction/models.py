from datetime import datetime

from database.orm import Base

from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import MappedColumn, mapped_column


# 당뇨/고혈압 위험도 예측 결과
class HealthRiskPrediction(Base):
    __tablename__ = "health_risk_prediction"

    id: MappedColumn[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: MappedColumn[int] = mapped_column(
        ForeignKey("user.id")
    )

    diabetes_probability: MappedColumn[float] = mapped_column(Float)
    hypertension_probability: MappedColumn[float] = mapped_column(Float)

    model_version: MappedColumn[str] = mapped_column(String(50)) 
    created_at: MappedColumn[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
