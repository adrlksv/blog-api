from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt 

from src.config import settings
from src.users.dao import UsersDAO
from src.database import get_db

from src.exceptions import (
    TokenAbsentException,
    IncorrectTokenFormatException,
    TokenExpiredException,
    UserIsNotPresentException,
)


def get_token(request: Request):
    token = request.cookies.get("refer_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(
        token: str = Depends(get_token),
        db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < int(datetime.utcnow().timestamp())):
        raise TokenExpiredException
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    
    user = await UsersDAO.find_by_id(
        model_id=int(user_id),
        session=db
    )
    if not user:
        raise UserIsNotPresentException
    
    return user
