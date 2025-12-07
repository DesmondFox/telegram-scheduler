from aiogram.fsm.state import State, StatesGroup


class DashboardBotStates(StatesGroup):
    MAIN_MENU = State()
    SETTINGS = State()


class SchedulerBotStates(StatesGroup):
    MAIN_MENU = State()
    CREATE_POST_WAITING_FOR_POST = State()
    CREATE_POST_DATETIME = State()
    # CREATE_POST_DESTINATIONS = State()
    # CREATE_POST_PREVIEW = State()
    # CREATE_POST_SENT = State()


class ChannelsSettingsStates(StatesGroup):
    CHANNELS_LIST = State()
    ADD_CHANNEL = State()       # Select platform [telegram, discord]
    ADD_TELEGRAM_CHANNEL = State()
    ADD_DISCORD_CHANNEL = State()