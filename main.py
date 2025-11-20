import logging
import os
import asyncio
import json
import dotenv
from aiogram.dispatcher.dispatcher import MemoryStorage
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import F, Bot, Dispatcher
from entities.states import SchedulerBotStates
from misc.keyboards import create_post_keyboard, main_menu_keyboard, date_picker_keyboard

dotenv.load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

WEBAPP_URL = "https://DesmondFox.github.io/telegram-scheduler/webapp/picker.html"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


@dp.message(CommandStart())
async def start_command(message: Message):
    keyboard = main_menu_keyboard()
    await message.answer("Hello! I'm a scheduler bot. I can help you schedule your posts.", reply_markup=keyboard)


##
# Create post flow
##

@dp.callback_query(F.data == "create_post")
async def create_post_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SchedulerBotStates.CREATE_POST_WAITING_FOR_POST)
    keyboard = create_post_keyboard()
    await callback.message.answer("Please send the post to schedule.", reply_markup=keyboard)


@dp.message(SchedulerBotStates.CREATE_POST_WAITING_FOR_POST)
async def create_post_waiting_for_post_message(message: Message, state: FSMContext):
    # Save the post content
    # if message.photo:
    #     await state.update_data(file_id=message.photo[-1].file_id, content_type="photo", caption=message.caption)
    # elif message.text:
    #     await state.update_data(text=message.text, content_type="text")
    
    await state.set_state(SchedulerBotStates.CREATE_POST_DATE)
    
    # Send the Date Picker WebApp Button (Reply Keyboard)
    keyboard = date_picker_keyboard(WEBAPP_URL)
    await message.answer("Please select the date and time for publication:", reply_markup=keyboard)


# Handle "Cancel" text from the Reply Keyboard
@dp.message(SchedulerBotStates.CREATE_POST_DATE, F.text == "Cancel")
async def cancel_create_post_text(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Creation cancelled.", reply_markup=main_menu_keyboard())


@dp.message(SchedulerBotStates.CREATE_POST_DATE, F.text == "Schedule now")
async def schedule_now_text(message: Message, state: FSMContext):
    await state.set_state(SchedulerBotStates.CREATE_POST_PREVIEW)
    await message.answer("Post will be sent right after push button is pressed.")


@dp.message(SchedulerBotStates.CREATE_POST_DATE, F.web_app_data)
async def process_date_webapp(message: Message, state: FSMContext):
    try:
        data = json.loads(message.web_app_data.data)
        datetime_str = data.get('datetime')
        user_timezone = data.get('timezone')
        
        await state.update_data(scheduled_time=datetime_str, user_timezone=user_timezone)

        await state.set_state(SchedulerBotStates.CREATE_POST_PREVIEW)
        await message.answer(f"📅 Picked date and time:\nDate: {datetime_str}\nTimezone: {user_timezone}")
        
    except Exception as e:
        logging.error("Error processing webapp data: %s", e)
        await message.answer("Error processing date. Please try again.")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
