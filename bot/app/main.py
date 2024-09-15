import asyncio
import logging

from aiogram import Dispatcher

from app.bot_instance import bot
from app.users.handler import router as user_router
from app.tasks.handler import router as tasks_router
from app.comments.handler import router as comments_router


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(user_router)
    dp.include_router(tasks_router)
    dp.include_router(comments_router)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()

    register_routers(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await session.close()


if __name__ == '__main__':
    asyncio.run(main())
