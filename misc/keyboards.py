from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Create post", callback_data="create_post")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def create_post_without_files_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Post without files", callback_data="post_without_files")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

