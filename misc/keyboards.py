from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Create post", callback_data="create_post")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def create_post_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Cancel", callback_data="cancel_create_post")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def date_picker_keyboard(url: str):
    # WebApp opened via Inline Button CANNOT send data back via sendData method.
    # We must use ReplyKeyboardMarkup (keyboard below input field) for sendData to work.
    
    buttons = [
        [KeyboardButton(text="📅 Pick Date & Time", web_app=WebAppInfo(url=url))],
        [KeyboardButton(text="Cancel")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
