from fastapi import APIRouter, status, Response, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.exceptions import ToDoListException
from app.users.auth import get_password_hash, authenticate_user, create_access_token, check_tg_hash, \
    authenticate_tg_user
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.schemas import SProfile, SAuthUser, STgLogin, STgRegister, SLoginUser

router = APIRouter(
     prefix="/users",
     tags=["Users"],
)

limiter = Limiter(key_func=get_remote_address)


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("15/minute")
async def register(user_data: SAuthUser, request: Request) -> None: # noqa
    await UsersDAO.check_user_exists(user_data.username)

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        username=user_data.username,
        hashed_password=hashed_password,
        email=user_data.email,
    )


@router.post("/login")
@limiter.limit("15/minute")
async def login_user(user_data: SLoginUser, response: Response, request: Request) -> dict: # noqa
    user = await authenticate_user(user_data.username, user_data.password)
    access_token = create_access_token({"sub": user.username})
    response.set_cookie("to_do_list_access_token", access_token, httponly=True)
    return {"message": "successful login"}


@router.post("/logout")
@limiter.limit("15/minute")
async def logout_user(response: Response, request: Request) -> dict:
    await get_current_user(request)
    response.delete_cookie("to_do_list_access_token")
    return {"message": "successful logout"}


@router.get('/me', response_model=SProfile)
@limiter.limit("15/minute")
async def get_my_profile(request: Request, current_user: SProfile = Depends(get_current_user)): # noqa
    return current_user


@router.post("/tg_login")
@limiter.limit("15/minute")
async def get_user_by_tg_id(tg_user: STgLogin, request: Request) -> dict[str, str]: # noqa
    user = await UsersDAO.find_one_or_none(
        tg_id=tg_user.tg_id,
        tg_hash=tg_user.tg_hash
    )
    if user:
        return {"message": "successful login"}
    else:
        return {"message": "unsuccessful login"}


@router.post("/tg_register")
@limiter.limit("15/minute")
async def register_tg_user(tg_user: STgRegister, request: Request): # noqa
    try:
        user = await authenticate_tg_user(tg_user.username, tg_user.password)
        if user:
            await check_tg_hash(tg_user.tg_id, tg_user.tg_hash)
            await UsersDAO.add_tg_data(tg_user.username, tg_user.tg_id, tg_user.tg_hash)
            return {"message": "successful telegram integration"}
        else:
            await check_tg_hash(tg_user.tg_id, tg_user.tg_hash)
            hashed_password = get_password_hash(tg_user.password)
            await UsersDAO.add(
                username=tg_user.username,
                email=tg_user.email,
                hashed_password=hashed_password,
                tg_id=tg_user.tg_id,
                tg_hash=tg_user.tg_hash,
            )
            return {"message": "successful registration"}
    except Exception:
        raise ToDoListException
