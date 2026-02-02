import asyncio
import logging
from aiogram import Bot, Dispatcher
from modular_quess_numb.config import config, logging_setup
from modular_quess_numb.handlers import user, other
from modular_quess_numb.database.init_db import init_db # инициализируем базу данных


async def main() -> None:
    logging_setup.setup_logging()
    logging.info("Бот запущен")

    bot = Bot(config.load_config().token)
    dp = Dispatcher()
    dp.include_router(user.router)
    dp.include_router(other.router)

    init_db() # создаем базу данных
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
