from aiogram import Bot
from aiogram.types import Message
from core.utils.dbconnect import Request


async def get_start(message: Message, bot: Bot, request: Request):
    await request.add_data(message.from_user.id, message.from_user.first_name)
    await message.answer(f'Здравствуйте! Спасибо за то, что присоединились к нам!')
    await message.answer(
        f'Этот Бот будет отправлять Вам информацию о запланированных вебинарах, семинарах, курсах, чтобы Вы ничего не пропустили.')
