import logging
import os
import asyncio
from aiogram_dialog import Dialog, DialogManager, ShowMode, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
import dotenv
from aiogram.dispatcher.dispatcher import MemoryStorage
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
from aiogram import F, Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from entities.states import DashboardBotStates
from infrastructure.db_session_middleware import DbSessionMiddleware
from infrastructure.repo_holder import RepoHolder
from infrastructure.utils.db import create_db_tables
from misc.constants import DATA_DIR
from ui.dialogs.main_menu import main_dialog
from ui.getters import get_user_data

dotenv.load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

# DB setup
engine = create_async_engine(f"sqlite+aiosqlite:///{DATA_DIR}/data.sqlite")
session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Bot setup
bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

dp.include_router(main_dialog)
setup_dialogs(dp)

@dp.message(CommandStart())
async def start_command(
    message: Message, 
    dialog_manager: DialogManager, 
    repo_holder: RepoHolder,
) -> None:
    user = await repo_holder.user_repo.get_or_create_user(message.from_user)
    
    await dialog_manager.start(
        DashboardBotStates.MAIN_MENU, 
        mode=StartMode.RESET_STACK, 
        show_mode=ShowMode.EDIT,
    )


if __name__ == "__main__":
    # Register middlewares
    dp.update.middleware.register(DbSessionMiddleware(session))

    # Create DB tables
    asyncio.run(create_db_tables(engine))

    # Start bot
    asyncio.run(dp.start_polling(bot))
