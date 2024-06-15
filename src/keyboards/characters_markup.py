import logging
from typing import List, Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback import *

from aiogram.filters.callback_data import CallbackData

class CharactersCallbackc(CallbackData, prefix="characters"):
    user_id: int
    page: int = 0

def characters_markup(user_id: int, page: int = 0):
    if page != 0:
        prev_page = CharactersCallbackc(user_id=user_id, page=page - 1).pack()
    else:
        prev_page = CharactersCallbackc(user_id=user_id, page=-404).pack()

    next_page = CharactersCallbackc(user_id=user_id, page=page + 1).pack()

    inline_keyboard = [
        [
            InlineKeyboardButton(text="<", callback_data=prev_page),
            InlineKeyboardButton(text=">", callback_data=next_page)
        ],
        [
            InlineKeyboardButton(text="Профиль", callback_data=ProfileCallback(user_id=user_id).pack())
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

