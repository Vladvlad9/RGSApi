from datetime import datetime, timedelta
from jose import jwt

from config import CONFIG


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=3600)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(claims=to_encode,
                             key=CONFIG.AUTH.SECRET_KEY,
                             algorithm=CONFIG.AUTH.ALGORITHM)
    return encoded_jwt
