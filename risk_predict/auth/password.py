import bcrypt


def hash_password(plain_password: str) -> str:
    password_hash: bytes = bcrypt.hashpw(
        plain_password.encode(), bcrypt.gensalt()
    )
    return password_hash.decode()

def verify_password(
    plain_password: str, password_hash: str
) -> bool:
    return bcrypt.checkpw(
        plain_password.encode(),
        password_hash.encode()
    )
