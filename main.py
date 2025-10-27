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

dotenv.load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


@dp.message(CommandStart())
async def start_command(message: Message):
    buttons = [
        [InlineKeyboardButton(text="Create post", callback_data="create_post")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Hello! I'm a scheduler bot. I can help you schedule your posts.", reply_markup=keyboard)


@dp.callback_query(F.data == "create_post")
async def create_post_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SchedulerBotStates.CREATE_POST)
    await callback.message.answer("Please enter the description of the post.")


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
