import hmac
from datetime import datetime, UTC, timedelta

import bcrypt
from passlib.context import CryptContext
import jwt

from main_service.app.config import settings, auth_settings
from main_service.app.exceptions import IncorrectUsernameOrPasswordException, IncorrectTgHashException
from main_service.app.users.dao import UsersDAO
from main_service.app.users.schemas import STgRegister

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    secret_key = auth_settings.private_key_pass.read_text().encode()
    encoded_jwt = jwt.encode(to_encode, secret_key, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    user = await UsersDAO.find_one_or_none(username=username)
    if not user or not validate_password(password, user.hashed_password):
        raise IncorrectUsernameOrPasswordException
    return user


async def authenticate_tg_user(username: str, password: str) -> STgRegister | None:
    user = await UsersDAO.find_one_or_none(username=username)
    if not user or not validate_password(password, user.hashed_password):
        return None
    return user


async def check_tg_hash(tg_id: str, tg_hash: str) -> None:
    private_key = auth_settings.private_key_pass.read_text().encode()
    expected_hash = hmac.new(private_key, tg_id.encode(), settings.TG_HASH_ALGORITHM).hexdigest()
    if not hmac.compare_digest(expected_hash, tg_hash):
        raise IncorrectTgHashException


async def get_tg_user(tg_id: str, tg_hash: str) -> STgRegister:
    await check_tg_hash(tg_id, tg_hash)
    user = await UsersDAO.find_one_or_none(tg_hash=tg_hash)
    if not user:
        raise IncorrectTgHashException
    return user
