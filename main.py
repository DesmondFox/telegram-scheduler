import logging
import os
import asyncio
from aiogram_dialog import Dialog, DialogManager, ShowMode, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
import dotenv
from aiogram.dispatcher.dispatcher import MemoryStorage
from aiogram.types import CallbackQuery, ChatMemberUpdated, Message
from aiogram.filters import CommandStart
from aiogram import F, Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from entities.states import ChannelsSettingsStates, DashboardBotStates
from infrastructure.db_session_middleware import DbSessionMiddleware
from infrastructure.domain.models import ChannelModel, PlatformEnum
from infrastructure.repo_holder import RepoHolder
from infrastructure.utils.db import create_db_tables
from misc.constants import DATA_DIR
from ui.dialogs.channels_settings import channels_settings_dialog
from ui.dialogs.main_menu import main_dialog

dotenv.load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

# DB setup
engine = create_async_engine(f"sqlite+aiosqlite:///{DATA_DIR}/data.sqlite")
session = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession)

# Bot setup
bot = Bot(token=TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

dp.include_router(main_dialog)
dp.include_router(channels_settings_dialog)
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


@dp.my_chat_member()
async def my_chat_member(
    event: ChatMemberUpdated,
    dialog_manager: DialogManager,
    repo_holder: RepoHolder,
) -> None:
    # This event is triggered when the bot is added to a chat as an administrator
    # We need to check if the bot has the permission to post messages
    if event.new_chat_member.status != "administrator":
        return

    user_who_added_bot = event.from_user.id
    user = await repo_holder.user_repo.get_user_by_telegram_id(user_who_added_bot)
    if user is None:
        # If the user is not found, we need to leave the channel
        logging.info(
            f"User {user_who_added_bot} is not found, leaving the channel {event.chat.id}")
        await event.chat.leave()
        return

    channel_model = ChannelModel(
        user_id=user.id,
        platform=PlatformEnum.TELEGRAM,
        channel_id=str(event.chat.id),
        target_id=str(event.chat.id),
        title=event.chat.title,
        is_active=True,
    )
    added_channel = await repo_holder.channel_repo.create_channel(channel_model)
    logging.info(f"Channel {added_channel.id} added to the database")

    await dialog_manager.start(
        ChannelsSettingsStates.CHANNELS_LIST,
        show_mode=ShowMode.EDIT,
        data={"is_new_channel": True},
    )

if __name__ == "__main__":
    # Register middlewares
    dp.update.middleware.register(DbSessionMiddleware(session))

    # Create DB tables
    asyncio.run(create_db_tables(engine))

    # Start bot
    asyncio.run(dp.start_polling(bot))
