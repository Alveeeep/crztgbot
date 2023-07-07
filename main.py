import contextlib

from aiogram import Bot, Dispatcher, F
import asyncio
import logging

from aiogram.filters import Command

from core.settings import settings

#from core.utils.commands import set_commands
from core.middlewares.dbmiddleware import DbSession
from core.handlers import sender
import asyncpg

from core.handlers import basic
from core.utils.sender_state import Steps

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def start_bot(bot: Bot):
    #await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!')


async def create_pool():
    return await asyncpg.create_pool(user='postgres', password='qwerty', database='triggerbot',
                                     host='127.0.0.1', port=5432, command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    pool_connect = await create_pool()
    dp = Dispatcher()
    dp.update.middleware.register(DbSession(pool_connect))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(sender.get_sender, Command(commands='sender', magic=F.args), F.chat.id == settings.bots.admin_id)
    dp.message.register(sender.get_message, Steps.get_message, F.chat.id == settings.bots.admin_id)
    dp.callback_query.register(sender.q_button, Steps.q_button)
    dp.message.register(sender.get_text_button, Steps.get_text_button, F.chat.id == settings.bots.admin_id)
    dp.message.register(sender.get_url_button, Steps.get_url_button, F.chat.id == settings.bots.admin_id)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())