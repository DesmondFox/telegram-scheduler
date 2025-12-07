import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, Multi
from dotenv.main import logger
from entities.states import ChannelsSettingsStates, DashboardBotStates
from infrastructure.repo_holder import RepoHolder
from ui.dialogs.shared import done, go_back
from ui.getters import get_bot_info


async def go_settings(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(DashboardBotStates.SETTINGS, show_mode=ShowMode.EDIT)


PLATFORM_EMOJI = {
    "telegram": "📱",
    "discord": "🎮",
}


async def get_channels_data(
    dialog_manager: DialogManager,
    repo_holder: RepoHolder,
    **kwargs,
) -> dict:
    user = await repo_holder.user_repo.get_user_by_telegram_id(dialog_manager.event.from_user.id)
    channels = await repo_holder.channel_repo.get_channels_by_user_id(user.id)
    channels_count = len(channels)
    channels_list = [
        {
            "id": channel.id,
            "platform": channel.platform.value if hasattr(channel.platform, "value") else channel.platform,
            "platform_emoji": PLATFORM_EMOJI.get(
                channel.platform.value if hasattr(channel.platform, "value") else channel.platform, 
                "📢"
            ),
            "target_id": channel.target_id,
            "title": channel.title or "Untitled",
            "is_active": channel.is_active,
            "status_emoji": "✅" if channel.is_active else "❌",
        }
        for channel in channels
    ]

    return {
        "channels_count": channels_count,
        "channels_list": channels_list,
    }


async def go_to_add_channel(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(ChannelsSettingsStates.ADD_CHANNEL, show_mode=ShowMode.EDIT)


async def go_to_add_telegram_channel(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(ChannelsSettingsStates.ADD_TELEGRAM_CHANNEL, show_mode=ShowMode.EDIT)


async def go_to_add_discord_channel(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(ChannelsSettingsStates.ADD_DISCORD_CHANNEL, show_mode=ShowMode.EDIT)


async def on_channel_selected(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    item_id: str,
) -> None:
    logger.info(f"Channel selected: {item_id}")
    # TODO: Open channel info


channels_settings_dialog = Dialog(
    Window(
        Multi(
            Format("Channels settings\n"),
            Format("Channels count: {channels_count}\n"),
        ),
        ScrollingGroup(
            Select(
                Format("{item[status_emoji]} [{item[platform_emoji]} {item[platform]}] {item[title]}"),
                id="channel_select",
                items="channels_list",
                item_id_getter=lambda item: str(item["id"]),
                on_click=on_channel_selected,
            ),
            id="channels_scroll",
            width=1,
            height=5,
        ),
        Row(
            Button(Const("🔙 Go back"), "go_back", on_click=done),
            Button(Const("➕ Add channel"),
                   "add_channel",
                   on_click=go_to_add_channel),
        ),
        state=ChannelsSettingsStates.CHANNELS_LIST,
        getter=get_channels_data,
    ),
    Window(
        Const("Add channel"),
        Button(Const("🔙 Go back"), "go_back", on_click=go_back),
        Row(
            Button(Const("➕ Add Telegram channel"),
                   "add_telegram_channel",
                   on_click=go_to_add_telegram_channel),
            Button(Const("➕ Add Discord channel"),
                   "add_discord_channel",
                   on_click=go_to_add_discord_channel),
        ),
        state=ChannelsSettingsStates.ADD_CHANNEL,
    ),
    Window(
        Multi(
            Const("To add a Telegram channel, you need to:"),
            Const("1. Open the settings of your Telegram channel."),
            Format("2. Go to **Administrators -> Add Administrator**"),
            Format("3. In the search, enter my bot's name : @{bot_username}."),
            Format("4. Add me and grant me **permission to post messages**."),
        ),

        Button(Const("🔙 Go back"), "go_back", on_click=go_back),
        state=ChannelsSettingsStates.ADD_TELEGRAM_CHANNEL,
        getter=get_bot_info,
    ),
)
