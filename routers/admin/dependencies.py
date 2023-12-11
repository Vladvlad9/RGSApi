from datetime import datetime

from fastapi import HTTPException, Request, status, Depends
from jose import jwt, JWTError

from config import CONFIG
from exeptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException

from crud.AdminWeb import CRUDAdminWeb


def get_token(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token=token,
                             key=CONFIG.AUTH.SECRET_KEY,
                             algorithms=CONFIG.AUTH.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException

    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    get_admin = await CRUDAdminWeb.get_id(id=int(user_id))
    if not get_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return get_admin
