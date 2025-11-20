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
    # WebApp buttons must be in ReplyKeyboardMarkup (keyboard attached to input field) 
    # OR InlineKeyboardMarkup.
    # Inline is generally preferred for "actions", but Reply is often used for WebApps 
    # replacing the keyboard. 
    # However, for a "Pick Date" action in a flow, Inline is better if supported?
    # Actually, InlineKeyboard supports WebApp since recently.
    # Let's use Inline for seamless experience.
    
    buttons = [
        [InlineKeyboardButton(text="📅 Pick Date & Time", web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton(text="Cancel", callback_data="cancel_create_post")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
