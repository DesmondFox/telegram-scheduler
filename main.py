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
    # Kicked: ChatMemberUpdated(chat=Chat(id=-1001718926994, type='channel', title='nd', username=None, first_name=None, last_name=None, is_forum=None, is_direct_messages=None, accent_color_id=None, active_usernames=None, available_reactions=None, background_custom_emoji_id=None, bio=None, birthdate=None, business_intro=None, business_location=None, business_opening_hours=None, can_set_sticker_set=None, custom_emoji_sticker_set_name=None, description=None, emoji_status_custom_emoji_id=None, emoji_status_expiration_date=None, has_aggressive_anti_spam_enabled=None, has_hidden_members=None, has_private_forwards=None, has_protected_content=None, has_restricted_voice_and_video_messages=None, has_visible_history=None, invite_link=None, join_by_request=None, join_to_send_messages=None, linked_chat_id=None, location=None, message_auto_delete_time=None, permissions=None, personal_chat=None, photo=None, pinned_message=None, profile_accent_color_id=None, profile_background_custom_emoji_id=None, slow_mode_delay=None, sticker_set_name=None, unrestrict_boost_count=None), from_user=User(id=249560478, is_bot=False, first_name='arekusei', last_name=None, username='segmentation_fault', language_code='en', is_premium=True, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None, can_connect_to_business=None, has_main_web_app=None), date=datetime.datetime(2025, 12, 9, 22, 37, 18, tzinfo=TzInfo(UTC)), old_chat_member=ChatMemberAdministrator(status='administrator', user=User(id=6834918039, is_bot=True, first_name='dev-test', last_name=None, username='devtest12345bot', language_code=None, is_premium=None, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None, can_connect_to_business=None, has_main_web_app=None), can_be_edited=False, is_anonymous=False, can_manage_chat=True, can_delete_messages=True, can_manage_video_chats=True, can_restrict_members=True, can_promote_members=False, can_change_info=True, can_invite_users=True, can_post_stories=True, can_edit_stories=True, can_delete_stories=True, can_post_messages=True, can_edit_messages=True, can_pin_messages=None, can_manage_topics=None, can_manage_direct_messages=True, custom_title=None, can_manage_voice_chats=True), new_chat_member=ChatMemberBanned(status='kicked', user=User(id=6834918039, is_bot=True, first_name='dev-test', last_name=None, username='devtest12345bot', language_code=None, is_premium=None, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None, can_connect_to_business=None, has_main_web_app=None), until_date=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=TzInfo(UTC))), invite_link=None, via_join_request=None, via_chat_folder_invite_link=None)
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
