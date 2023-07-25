from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_confirm_button_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Добавить кнопку', callback_data='add_button')
    keyboard_builder.button(text='Продолжить без кнопки', callback_data='no_button')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_choose_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Заказчик', callback_data='zakazchik')
    keyboard_builder.button(text='Поставщик', callback_data='postavchik')
    keyboard_builder.button(text='Всё вместе', callback_data='oba')
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


def get_choose_sender_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Для заказчиков', callback_data='for_z')
    keyboard_builder.button(text='Для поставщиков', callback_data='for_p')
    keyboard_builder.button(text='Всем', callback_data='all')
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()
