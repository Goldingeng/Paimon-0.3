from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback import *

def help_markup():

    inline_keyboard = [

        [
            InlineKeyboardButton(text="Канал",  url="https://t.me/genshintwist")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)