from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, Integer, Float, Boolean, func, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, with_loader_criteria


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def soft_delete(self):
        self.email = f"deleted_user:{self.id}"
        self.deleted_at = datetime.now(tz=timezone.utc)

# User를 불러올 때, deleted_at != NULL인 데이터는 제외
@event.listens_for(Session, "do_orm_execute")
def _add_filtering_criteria(execute_state):
    if execute_state.is_select:
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                User,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )

class HealthProfile(Base):
    __tablename__ = "health_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),  # user(부모)가 삭제되면 profile(자식) 함께 삭제
        unique=True, 
        nullable=False
    )

    age: Mapped[int] = mapped_column(Integer)
    height_cm: Mapped[float] = mapped_column(Float)
    weight_kg: Mapped[float] = mapped_column(Float)
    smoking: Mapped[bool] = mapped_column(Boolean)
    exercise_per_week: Mapped[int] = mapped_column(Integer)


class HealthRiskPrediction(Base):
    __tablename__ = "health_risk_prediction"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), 
        nullable=False
    )

    # 당뇨병 / 고혈압 위험도
    diabetes_probability: Mapped[float] = mapped_column(Float)
    hypertension_probability: Mapped[float] = mapped_column(Float)

    model_version: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
