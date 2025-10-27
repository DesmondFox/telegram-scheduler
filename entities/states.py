from aiogram.fsm.state import State, StatesGroup

class SchedulerBotStates(StatesGroup):
    MAIN_MENU = State()
    CREATE_POST = State()
    CREATE_POST_WAITING_FOR_FILES = State()
    CREATE_POST_DESCRIPTION = State()
    CREATE_POST_DATE = State()
    CREATE_POST_TIME = State()
    CREATE_POST_DESTINATIONS = State()
    CREATE_POST_PREVIEW = State()
    CREATE_POST_SENT = State()