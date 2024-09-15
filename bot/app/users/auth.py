import hmac

import httpx
from httpx import Response

from app.config import auth_settings, settings, main_backend_settings


async def generate_tg_hash(tg_id: str) -> str:
    private_key = auth_settings.private_key_pass.read_text().encode()
    hash_result = hmac.new(private_key, tg_id.encode(), settings.TG_HASH_ALGORITHM).hexdigest()
    return hash_result


async def login_user(tg_id: str) -> Response:
    tg_hash = await generate_tg_hash(tg_id)
    tg_user_login = {
        "tg_id": tg_id,
        "tg_hash": tg_hash
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{main_backend_settings.COMMENTS_API_ROOT}users/tg_login",
            json=tg_user_login,
        )
        return response


async def register_user(
        tg_id: str,
        username: str,
        email: str,
        password: str,
) -> Response:
    tg_hash = await generate_tg_hash(tg_id)
    tg_user_register = {
        "username": username,
        "email": email,
        "password": password,
        "tg_id": tg_id,
        "tg_hash": tg_hash,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{main_backend_settings.COMMENTS_API_ROOT}users/tg_register",
            json=tg_user_register,
        )
        return response


async def get_tg_user_login(tg_id: int) -> dict[str, str]:
    tg_id = str(tg_id)
    tg_hash = await generate_tg_hash(tg_id)

    tg_user_login = {
        "tg_id": tg_id,
        "tg_hash": tg_hash,
    }
    return tg_user_login
