from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:password@db:3306/app_db"

engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)

def get_session():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
