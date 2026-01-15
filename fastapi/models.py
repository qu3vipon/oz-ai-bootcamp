from orm import Base

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


# Item 데이터를 저장할 DB 테이블 & ORM 객체
class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # 기본키(Primary Key)
    name: Mapped[str] = mapped_column(String(128))
    price: Mapped[int] = mapped_column(Integer)
