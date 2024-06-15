import logging
from typing import List, Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..database.users import User

from .callback import *

def history_markup(user_id: int):
    callback_data_profile = ProfileCallback(user_id=user_id)
    callback_data_banner = BannerCallback(user_id=user_id)
    callback_data_characters = CharactersCallbackc(user_id=user_id, page=0)
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Баннер", callback_data=callback_data_banner.pack()),
            InlineKeyboardButton(text="Персонажи", callback_data=callback_data_characters.pack()),
        ],
        [
            InlineKeyboardButton(text="Профиль", callback_data=callback_data_profile.pack()),
            InlineKeyboardButton(text="Канал",  url="https://t.me/genshintwist"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)