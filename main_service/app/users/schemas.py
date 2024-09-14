from typing import Annotated, TypeAlias, Literal

from annotated_types import MinLen
from pydantic import BaseModel, EmailStr

Role: TypeAlias = Literal["User", "Admin"]
Password: TypeAlias = Annotated[str, MinLen(8)]


class SUser(BaseModel):
    username: str
    password: Password
    role: Role
    email: EmailStr


class SAuthUser(BaseModel):
    username: str
    password: Password
    email: EmailStr


class SLoginUser(BaseModel):
    username: str
    password: Password


class SProfile(BaseModel):
    username: str
    role: Role
    email: EmailStr


class STgLogin(BaseModel):
    tg_id: str | None
    tg_hash: str | None


class STgRegister(BaseModel):
    username: str
    email: EmailStr
    password: Password
    tg_id: str | None
    tg_hash: str | None
