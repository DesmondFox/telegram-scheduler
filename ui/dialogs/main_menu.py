from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format
from entities.states import ChannelsSettingsStates, DashboardBotStates
from ui.dialogs.shared import go_back
from ui.getters import get_user_data


async def go_settings(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(DashboardBotStates.SETTINGS, show_mode=ShowMode.EDIT)


async def go_channels_settings(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(ChannelsSettingsStates.CHANNELS_LIST, show_mode=ShowMode.EDIT)

main_dialog = Dialog(
    Window(
        Format("Hello, {first_name}!\nWelcome to the dashboard."),
        Button(Const("Go settings"), "go_settings", on_click=go_settings),
        state=DashboardBotStates.MAIN_MENU,
        getter=get_user_data,
    ),
    Window(
        Const("Settings"),
        Row(
            Button(Const("Go back"), "go_back", on_click=go_back),
            Button(Const("Channels settings"), "go_channels_settings",
                   on_click=go_channels_settings),
        ),
        state=DashboardBotStates.SETTINGS,
    ),
)
