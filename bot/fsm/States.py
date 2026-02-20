from aiogram.fsm.state import StatesGroup, State

class AddProductFSM(StatesGroup):
    name = State()
    description = State()
    price = State()
    filepath = State()