import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import decode_token
from src.auth.model import User
from src.auth.repository import UserRepository
from src.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证信息",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
    except jwt.InvalidTokenError as e:
        raise credentials_exception from e

    if payload.get("type") != "access":
        raise credentials_exception

    sub = payload.get("sub")
    if not sub:
        raise credentials_exception
    try:
        user_id = int(sub)
    except (TypeError, ValueError) as e:
        raise credentials_exception from e

    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)
    if not user or not user.is_active:
        raise credentials_exception

    return user
