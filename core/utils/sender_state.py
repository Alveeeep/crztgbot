from aiogram.fsm.state import State, StatesGroup


class Steps(StatesGroup):
    get_message = State()
    get_choose = State()
    choice_confirm = State()
    q_button = State()
    get_text_button = State()
    get_url_button = State()


class Users(StatesGroup):
    get_choice = State()

