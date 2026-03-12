import bcrypt

# bytes = 0 또는 1

# 회원가입 할 때, 비밀번호 해시를 생성하는 함수
def hash_password(plain_password: str) -> str:
    password_hash_bytes: bytes = bcrypt.hashpw(
        plain_password.encode(), bcrypt.gensalt()
    )
    return password_hash_bytes.decode()


# 로그인 할 때, 비밀번호를 검증하는 함수
def verify_password(plain_password: str, password_hash: str) -> bool:
    # plain_password: 사용자가 입력한 평문 비밀번호
    # password_hash: 데이터베이스에 저장된 비밀번호 해시

    try:
        return bcrypt.checkpw(
            plain_password.encode(), password_hash.encode()
        )
    except Exception:
        return False
