from fastapi import APIRouter, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from main_service.app.categories.dao import CategoriesDAO
from main_service.app.categories.schemas import SCategory
from main_service.app.users.dependencies import check_admin_role

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

limiter = Limiter(key_func=get_remote_address)


@router.get("/")
@limiter.limit("15/minute")
async def get_categories(request: Request) -> list[SCategory]: # noqa
    categories = await CategoriesDAO.find_all()
    return categories


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("15/minute")
async def create_category(
        category: SCategory,
        request: Request
) -> None:
    await check_admin_role(request)
    await CategoriesDAO.check_category_exists(category.title)
    await CategoriesDAO.add(**dict(category))


@router.delete("/{category_title}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("15/minute")
async def delete_category(category_title: str, request: Request) -> None:
    await check_admin_role(request)
    await CategoriesDAO.delete_category(category_title)


@router.put("/{category_title}")
@limiter.limit("15/minute")
async def put_category(
        category_title: str,
        new_category: SCategory,
        request: Request,
) -> None:
    await check_admin_role(request)
    await CategoriesDAO.update_category(category_title, new_category)
