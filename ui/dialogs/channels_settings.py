import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, Jinja, Multi
from dotenv.main import logger
from entities.states import ChannelsSettingsStates, DashboardBotStates
from infrastructure.repo_holder import RepoHolder
from ui.dialogs.shared import PLATFORM_EMOJI, done, go_back
from ui.getters import get_bot_info


async def go_settings(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(DashboardBotStates.SETTINGS, show_mode=ShowMode.EDIT)


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
                channel.platform.value if hasattr(
                    channel.platform, "value") else channel.platform,
                "fallback"
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


async def get_channel_info(
    dialog_manager: DialogManager,
    repo_holder: RepoHolder,
    **kwargs,
) -> dict:
    channel = await repo_holder.channel_repo.get_channel_by_id(dialog_manager.dialog_data["selected_channel_id"])
    dialog_manager.dialog_data["selected_channel_is_active"] = channel.is_active
    return {
        "platform": (channel.platform.value if hasattr(channel.platform, "value") else channel.platform).capitalize(),
        "platform_emoji": PLATFORM_EMOJI.get(
            channel.platform.value if hasattr(
                channel.platform, "value") else channel.platform,
            "fallback"
        ),
        "target_id": channel.target_id,
        "title": channel.title or "Untitled",
        "is_active": "Active" if channel.is_active else "Inactive",
        "status_emoji": "✅" if channel.is_active else "❌",
        "created_at": channel.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": channel.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
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
    dialog_manager.dialog_data["selected_channel_id"] = item_id
    await dialog_manager.switch_to(ChannelsSettingsStates.CHANNEL_INFO, show_mode=ShowMode.EDIT)


async def delete_channel(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    repo_holder: RepoHolder = dialog_manager.middleware_data["repo_holder"]
    await repo_holder.channel_repo.remove_channel_by_id(dialog_manager.dialog_data["selected_channel_id"])
    await dialog_manager.switch_to(ChannelsSettingsStates.CHANNELS_LIST, show_mode=ShowMode.EDIT)

async def activate_deactivate_channel(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    repo_holder: RepoHolder = dialog_manager.middleware_data["repo_holder"]
    is_active = dialog_manager.dialog_data["selected_channel_is_active"]
    await repo_holder.channel_repo.set_channel_active(dialog_manager.dialog_data["selected_channel_id"], not is_active)
    await dialog_manager.switch_to(ChannelsSettingsStates.CHANNEL_INFO, show_mode=ShowMode.EDIT)

async def go_back_to_channels_list(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(ChannelsSettingsStates.CHANNELS_LIST, show_mode=ShowMode.EDIT)

channels_settings_dialog = Dialog(
    Window(
        Multi(
            Format("Channels settings\n"),
            Format("Channels count: {channels_count}\n"),
        ),
        ScrollingGroup(
            Select(
                Format(
                    "{item[status_emoji]} [{item[platform_emoji]} {item[platform]}] {item[title]}"),
                id="channel_select",
                items="channels_list",
                item_id_getter=lambda item: str(item["id"]),
                on_click=on_channel_selected,
            ),
            id="channels_scroll",
            width=1,
            hide_on_single_page=True,
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
        parse_mode="Markdown",
    ),
    Window(
        Multi(
            Format("**Channel info:** {title}"),
            Format("**Platform:** {platform_emoji} {platform}"),
            Format("**Target ID:** {target_id}"),
            Format("**Status:** {status_emoji} {is_active}"),
            Format("**Created at:** {created_at}"),
            Format("**Updated at:** {updated_at}"),
        ),
        Row(
            Button(Const("🔙 Go back"), "go_back", on_click=go_back_to_channels_list),
            Button(Const("❌ Delete channel"), "delete_channel", on_click=delete_channel),
        ),
        Button(Const("🔄 Activate/Deactivate channel"), "activate_deactivate_channel", on_click=activate_deactivate_channel),
        state=ChannelsSettingsStates.CHANNEL_INFO,
        getter=get_channel_info,
        parse_mode="Markdown",
    ),
)
