from datetime import datetime, UTC
from typing import Annotated

from jose import jwt, JWTError
from fastapi import Cookie, Request

from main_service.app.config import settings, auth_settings
from main_service.app.exceptions import IncorrectTokenFormatException, TokenExpiredException, \
    UserIsNotPresentException, TokenAbsentException, NotEnoughRightsException
from main_service.app.users.dao import UsersDAO
from main_service.app.users.schemas import SUser


async def get_token(request: Request) -> Annotated[str, Cookie]:
    token = request.cookies.get("to_do_list_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(request: Request):
    token: str = await get_token(request)

    try:
        secret_key = auth_settings.private_key_pass.read_text().encode()
        payload = jwt.decode(token, secret_key, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise TokenExpiredException

    username: str = payload.get("sub")
    if not username:
        raise UserIsNotPresentException

    user = await UsersDAO.find_one_or_none(username=username)
    if not user:
        raise UserIsNotPresentException
    return user


async def check_admin_role(request: Request) -> SUser:
    current_user: SUser = await get_current_user(request)
    if current_user.role != 'Admin':
        raise NotEnoughRightsException
    return current_user
