from aiogram.fsm.state import State, StatesGroup

class SchedulerBotStates(StatesGroup):
    MAIN_MENU = State()
    CREATE_POST_WAITING_FOR_POST = State()
    CREATE_POST_DATETIME = State()
    # CREATE_POST_DESTINATIONS = State()
    # CREATE_POST_PREVIEW = State()
    # CREATE_POST_SENT = State()