from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from core.utils.sender_state import Steps
from core.keyboards.inline import get_confirm_button_keyboard


async def get_sender(message: Message, command: CommandObject, state: FSMContext):
    if not command.args:
        await message.answer(f'Введите команду /sender и имя расслыки для создания рассылки')
        return

    await message.answer(f'Имя рассылки - {command.args}\r\n\r\n'
                         f'Введите основной текст рассылки')
    await state.update_data(name_camp=command.args)
    await state.set_state(Steps.get_message)


async def get_message(message: Message, state: FSMContext):
    await message.answer(f'Готово. Добавить кнопку внизу рассылки?', reply_markup=get_confirm_button_keyboard())
    await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
    await state.set_state(Steps.q_button)


async def q_button(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data == 'add_button':
        await call.message.answer(f'Введите текст для кнопки', reply_markup=None)
        await state.set_state(Steps.get_text_button)
    elif call.data == 'no_button':
        await call.message.edit_reply_markup(reply_markup=None)
        #aaaa

    await call.answer()


async def get_text_button(message: Message, state: FSMContext):
    await state.update_data(text_button=message.text)
    await message.answer(f'Введите ссылку для кнопки')
    await state.set_state(Steps.get_url_button)


async def get_url_button(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(url_button=message.text)
    added_keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=(await state.get_data()).get('text_button'),
                url=f'{message.text}'
            )
        ]
    ])


async def confirm(message: Message, bot: Bot, state: FSMContext):
    pass
