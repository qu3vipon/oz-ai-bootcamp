from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 데이터베이스 접속 정보
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# 엔진(Engine) = SQLAlchemy 사용시 DB와 연결관리
engine = create_async_engine(DATABASE_URL)

# 세션(Session) = DB 작업관리
# 세션을 만들 수 있는 세션 팩토리
AsyncSessionFactory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False, autoflush=False, expire_on_commit=False,  # 데이터를 다룰 때 사용되는 옵션
)

async def get_async_session():
    async with AsyncSessionFactory() as session:
        yield session
