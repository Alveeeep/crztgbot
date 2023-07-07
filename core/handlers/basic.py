from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message
from core.utils.dbconnect import Request


async def add_trigger(message: Message, command: CommandObject, request: Request):
    name_trigger = command.args.replace(' ', '_')
    value_trigger = message.reply_to_message.message_id
    await request.add_trigger(name_trigger, value_trigger)
    await message.answer(f'Триггер {name_trigger} добавлен')
    print(message.chat.id)


async def get_triggers(message: Message, request: Request):
    msg = await request.get_triggers()
    await message.answer(msg, parse_mode="MARKDOWN")


async def get_values(message: Message, bot: Bot, request: Request):
    values = await request.get_values(message.text.replace('#', ''))
    list_values = values.split('\r\n')

    for value in list_values:
        await bot.copy_message(message.chat.id, message.chat.id, int(value))