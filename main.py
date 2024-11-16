from aiogram import Bot, Dispatcher
import asyncio
import logging
from config import bot, ADMIN
from handlers import router
from aiogram.types import BotCommand

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp = Dispatcher()


async def bot_start():
    await bot.send_message(ADMIN, '🏁Bot ishlayapti')


async def bot_stop():
    await bot.send_message(ADMIN, '⚠️ Bot to\'xtadi')


async def start():
    dp.startup.register(bot_start)
    dp.shutdown.register(bot_stop)
    await bot.set_my_commands([
        BotCommand(command='/start', description='Bot ni ishga tushurish'),
        BotCommand(command='/help', description='Yordam uchun'),
        BotCommand(command='/stop', description='Statedan chiqish'),
        BotCommand(command='/new', description='Boshidan boshlash'),
    ])
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())
