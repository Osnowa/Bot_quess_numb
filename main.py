import asyncio
import logging
from aiogram import Bot, Dispatcher
from modular_quess_numb.config import config, logging_setup
from modular_quess_numb.handlers import user, other


async def main():
    # настройка логирования
    logging_setup.setup_logging()
    logging.info("Начало работы")
    # Создаем объекты бота и диспетчера
    bot = Bot(config.load_config().token)
    dp = Dispatcher()
    # подключаем роутеры
    dp.include_router(user.router)
    dp.include_router(other.router)
    # пропускаем накопившиеся апдейты
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())