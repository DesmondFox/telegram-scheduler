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
from entities.states import SchedulerBotStates

dotenv.load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

WEBAPP_URL = "https://DesmondFox.github.io/telegram-scheduler/webapp/picker.html"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
user_router = Router()
dp = Dispatcher(bot=bot, storage=storage)
dp.include_router(user_router)


async def to_create_post_window(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
        **kwargs,
) -> None:
    await dialog_manager.switch_to(SchedulerBotStates.CREATE_POST_WAITING_FOR_POST)


async def go_back(
    _: CallbackQuery,
    __: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.back()


async def post_input_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager
) -> None:
    # Save the post content
    await dialog_manager.switch_to(SchedulerBotStates.CREATE_POST_DATETIME)
    pass


async def date_time_input_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager
) -> None:
    pass

dialog = Dialog(
    # Main menu window
    Window(
        Const("Hello! I'm a scheduler bot. I can help you schedule your posts."),
        Button(
            Const("Create post"),
            "create_post",
            on_click=to_create_post_window,
        ),
        state=SchedulerBotStates.MAIN_MENU,
    ),

    # Create post window
    Window(
        Const("Please send the post to schedule."),
        MessageInput(post_input_handler),
        Button(Const("Back"), "back", on_click=go_back),
        state=SchedulerBotStates.CREATE_POST_WAITING_FOR_POST,
    ),

    # Select date and time
    Window(
        Const("Please select the date and time for publication."),
        MessageInput(date_time_input_handler),
        state=SchedulerBotStates.CREATE_POST_DATETIME,
        markup_factory=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="📅 Pick Date & Time", web_app=WebAppInfo(url=WEBAPP_URL))],
            [KeyboardButton(text="Back")],
        ], resize_keyboard=True, one_time_keyboard=True),
    ),
)

dp.include_router(dialog)
setup_dialogs(dp)


@dp.message(CommandStart())
async def start_command(message: Message, dialog_manager: DialogManager):
    # keyboard = main_menu_keyboard()
    # await message.answer("Hello! I'm a scheduler bot. I can help you schedule your posts.", reply_markup=keyboard)
    await dialog_manager.start(SchedulerBotStates.MAIN_MENU, mode=StartMode.RESET_STACK)


##
# Create post flow
##

# @dp.callback_query(F.data == "create_post")
# async def create_post_callback(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(SchedulerBotStates.CREATE_POST_WAITING_FOR_POST)
#     keyboard = create_post_keyboard()
#     await callback.message.answer("Please send the post to schedule.", reply_markup=keyboard)


# @dp.message(SchedulerBotStates.CREATE_POST_WAITING_FOR_POST)
# async def create_post_waiting_for_post_message(message: Message, state: FSMContext):
    # Save the post content
    # attachments = []
    # if message.photo:
    #     attachments.append(message.photo[-1].file_id)
    # elif message.video:
    #     attachments.append(message.video.file_id)
    # elif message.document:
    #     attachments.append(message.document.file_id)
    # elif message.audio:
    #     attachments.append(message.audio.file_id)
    # await state.update_data(post_content=message.text, content_type=message.content_type, sent_date=message.date, attachments=attachments)

    # await state.set_state(SchedulerBotStates.CREATE_POST_DATE)

    # # Send the Date Picker WebApp Button (Reply Keyboard)
    # keyboard = date_picker_keyboard(WEBAPP_URL)
    # await message.answer("Please select the date and time for publication:", reply_markup=keyboard)


# # Handle "Cancel" text from the Reply Keyboard
# @dp.message(SchedulerBotStates.CREATE_POST_DATE, F.text == "Cancel")
# async def cancel_create_post_text(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer("Creation cancelled.", reply_markup=main_menu_keyboard())


# @dp.message(SchedulerBotStates.CREATE_POST_DATE, F.text == "Schedule now")
# async def schedule_now_text(message: Message, state: FSMContext):
#     await state.set_state(SchedulerBotStates.CREATE_POST_PREVIEW)
#     await message.answer("Post will be sent right after push button is pressed.")


# @dp.message(SchedulerBotStates.CREATE_POST_DATE, F.web_app_data)
# async def process_date_webapp(message: Message, state: FSMContext):
#     try:
#         data = json.loads(message.web_app_data.data)
#         datetime_str = data.get('datetime')
#         user_timezone = data.get('timezone')

#         await state.update_data(scheduled_time=datetime_str, user_timezone=user_timezone)

#         await state.set_state(SchedulerBotStates.CREATE_POST_PREVIEW)
#         await message.answer(f"📅 Picked date and time:\nDate: {datetime_str}\nTimezone: {user_timezone}")

#     except Exception as e:
#         logging.error("Error processing webapp data: %s", e)
#         await message.answer("Error processing date. Please try again.")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
