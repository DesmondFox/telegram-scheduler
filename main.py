import asyncio
import dotenv
import os
import logging
from aiogram.dispatcher.dispatcher import MemoryStorage
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.filters import CommandStart
from aiogram import F, Bot, Dispatcher
from entities.states import SchedulerBotStates
from aiogram.fsm.context import FSMContext
from misc.keyboards import create_post_without_files_keyboard, main_menu_keyboard

dotenv.load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


@dp.message(CommandStart())
async def start_command(message: Message):
    keyboard = main_menu_keyboard()
    await message.answer("Hello! I'm a scheduler bot. I can help you schedule your posts.", reply_markup=keyboard)


@dp.callback_query(F.data == "create_post")
async def create_post_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SchedulerBotStates.CREATE_POST_WAITING_FOR_FILES)
    keyboard = create_post_without_files_keyboard()
    await callback.message.answer("Please send the files for the post.", reply_markup=keyboard)


@dp.callback_query(F.data == "post_without_files")
async def post_without_files_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SchedulerBotStates.CREATE_POST_DESCRIPTION)
    await callback.message.answer("Please enter the description of the post.")


@dp.message(SchedulerBotStates.CREATE_POST_DESCRIPTION)
async def create_post_description_message(message: Message, state: FSMContext):
    await state.update_data(post_description=message.text)
    await state.set_state(SchedulerBotStates.CREATE_POST_DATE)
    await message.answer("Please enter the date of the post.")



if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
