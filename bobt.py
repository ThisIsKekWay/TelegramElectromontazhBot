import asyncio
import logging
from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from config_reader import settings
from core.handlers import basic, user, admin
from core.utils.commands import set_commands
from db.model import create_db

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s -%(filename)s.%(funcName)s.%(lineno)d - %(message)s')

bot = Bot(token=settings.bot_token.get_secret_value())
dp = Dispatcher()


@dp.startup()
async def startup():
    if create_db():
        await bot.send_message(settings.admin_id, 'База данных создана!')
    else:
        await bot.send_message(settings.admin_id, 'База данных работает!')
    await set_commands(bot)
    await bot.send_message(settings.admin_id, 'Бот запущен!')


@dp.shutdown()
async def shutdown():
    await bot.send_message(settings.admin_id, 'Бот остановлен!')


async def main():
    dp.include_routers(basic.router, user.router, admin.router)
    try:
        await bot.delete_webhook()
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
