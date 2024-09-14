import asyncio
import logging

from aiogram import Dispatcher

from bot.app.bot_instance import bot
from bot.app.users.handler import router as user_router
from bot.app.tasks.handler import router as tasks_router
from bot.app.comments.handler import router as comments_router


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
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
