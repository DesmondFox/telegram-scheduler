import logging
import os
import asyncio
import json
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, WebApp
from aiogram_dialog.widgets.text import Const
import dotenv
from aiogram.dispatcher.dispatcher import MemoryStorage
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import F, Bot, Dispatcher, Router
from entities.states import DashboardBotStates, SchedulerBotStates

dotenv.load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

async def go_back(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.back()

dialog = Dialog(
    Window(
        Const("Hello, world!"),
        Button(Const("Go back"), go_back),
    )
)

dp.include_router(dialog)
setup_dialogs(dp)




@dp.message(CommandStart())
async def start_command(message: Message, dialog_manager: DialogManager):
    
    await dialog_manager.start(DashboardBotStates.MAIN_MENU, mode=StartMode.RESET_STACK)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
