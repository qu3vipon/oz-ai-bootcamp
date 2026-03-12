import jwt
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import settings


# JWT -> 형식
# access_token -> 역할
def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),  # subject: 사용자 식별 정보
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

def verify_access_token(access_token: str) -> dict:
    try:
        payload = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired")
    return payload


http_bearer = HTTPBearer()

def verify_user(
    auth_header: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> int:
    access_token = auth_header.credentials
    payload = verify_access_token(access_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid payload")
    return user_id
