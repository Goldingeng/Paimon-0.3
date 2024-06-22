from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .callback import *

def menu_markup(user_id: int):
    callback_data_history = HistoryCallback(user_id=user_id)
    callback_data_banner = BannerCallback(user_id=user_id)
    callback_data_characters = CharactersCallbackc(user_id=user_id, page=0)
    callback_data_pumping = PumpingCallbackc(user_id=user_id)
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Баннер", callback_data=callback_data_banner.pack()),
            InlineKeyboardButton(text="Персонажи", callback_data=callback_data_characters.pack()),
        ],
        [
            InlineKeyboardButton(text="История", callback_data=callback_data_history.pack()),
            InlineKeyboardButton(text="Улучшение", callback_data=callback_data_pumping.pack()),
        ],
        [
            InlineKeyboardButton(text="Канал",  url="https://t.me/genshintwist")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)