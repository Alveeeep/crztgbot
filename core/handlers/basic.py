from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from core.utils.dbconnect import Request
from core.keyboards.inline import get_choose_keyboard
from core.utils.sender_state import Users


async def get_start(message: Message, bot: Bot, request: Request, state: FSMContext):
    # await request.add_data(message.from_user.id, message.from_user.first_name)
    await message.answer(f'Здравствуйте! Спасибо за то, что присоединились к нам!')
    await message.answer(
        f'Этот Бот будет отправлять Вам информацию о запланированных вебинарах, семинарах, курсах, чтобы Вы ничего не пропустили.')
    await message.answer(f'Пожалуйста выберите для кого Вы хотите получать сообщения.',
                         reply_markup=get_choose_keyboard())
    await state.update_data(user_id=message.from_user.id, user_name=message.from_user.first_name)
    await state.set_state(Users.get_choice)


async def get_choice(call: CallbackQuery, bot: Bot, request: Request, state: FSMContext):
    if call.data == 'zakazchik':
        await call.message.answer(f'Вам будут приходить сообщения только для заказчиков.', reply_markup=None)
    elif call.data == 'postavchik':
        await call.message.answer(f'Вам будут приходить сообщения только для поставщиков.', reply_markup=None)
    elif call.data == 'oba':
        await call.message.answer(f'Вам будут приходить сообщения и для заказчиков, и для поставщиков.',
                                  reply_markup=None)

    data = await state.get_data()
    await request.add_data(data.get('user_id'), data.get('user_name'), call.data)
    await call.answer()
