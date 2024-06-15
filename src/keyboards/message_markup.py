import logging
from typing import List, Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback import *

def message_markup(user_id: int):
    callback_data_banner = BannerCallback(user_id=user_id)
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Баннер", callback_data=callback_data_banner.pack()),
            InlineKeyboardButton(text="Улучшение", callback_data="11")
        ],

        [
            InlineKeyboardButton(text="Канал",  url="https://t.me/genshintwist")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)