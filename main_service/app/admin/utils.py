from datetime import datetime, UTC

from fastapi import Request
from jose import jwt, JWTError

from app.config import auth_settings, settings
from app.exceptions import NotEnoughRightsException, IncorrectTokenFormatException, TokenExpiredException, \
    UserIsNotPresentException, TokenAbsentException
from app.users.dao import UsersDAO
from app.users.schemas import SUser


async def check_admin_role_for_admin_panel(request: Request) -> SUser:
    current_user: SUser = await get_current_admin(request)
    if current_user.role != 'Admin':
        raise NotEnoughRightsException
    return current_user


async def get_current_admin(request: Request):
    token: str = await get_token_from_session(request)

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


async def get_token_from_session(request: Request):
    token = request.session.get("token")
    if not token:
        raise TokenAbsentException
    return token
