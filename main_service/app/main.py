import aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from sqladmin import Admin
from redis import asyncio as aioredis

from app.admin.auth import authentication_backend
from app.admin.views import UsersAdmin, TasksAdmin, CategoriesAdmin
from app.config import settings
from app.database import engine
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router
from app.categories.router import router as categories_router
from app.comments.router import router as comments_router

app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(categories_router)
app.include_router(comments_router)


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(TasksAdmin)
admin.add_view(CategoriesAdmin)


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")

