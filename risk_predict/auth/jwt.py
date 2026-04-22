import jwt
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer

from config import settings


# accesss_token 발급 
def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    return jwt.encode(
        payload=payload, key=settings.JWT_SECRET, algorithm="HS256"
    )

# access_token의 위변조 여부 확인 & payload 읽는 함수
def verify_access_token(access_token: str) -> dict:
    try:
        payload = jwt.decode(
            access_token, settings.JWT_SECRET, algorithms=["HS256"]
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 토큰 형식입니다.",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="만료된 토큰입니다.",
        )
    return payload


def verify_user(
    auth_header = Depends(HTTPBearer())
):
    access_token = auth_header.credentials
    payload = verify_access_token(access_token=access_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="sub 값이 없습니다."
        )
    return user_id
