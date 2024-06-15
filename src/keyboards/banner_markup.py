import logging
from typing import List, Sequence

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callback import *

def banner_markup(user_id: int):
    callback_data_profile = ProfileCallback(user_id=user_id)
    callback_data_history = HistoryCallback(user_id=user_id)
    callback_data_twist = TwistCallbackc(user_id=user_id, count=1)
    callback_data_twists = TwistCallbackc(user_id=user_id, count=10) #Ты че гений посмотри внимательнее на свой колбек
    inline_keyboard = [
        [
            InlineKeyboardButton(text="1", callback_data=callback_data_twist.pack()),
            InlineKeyboardButton(text="10", callback_data=callback_data_twists.pack())
        ],

        [
            InlineKeyboardButton(text="Профиль", callback_data=callback_data_profile.pack())
        ],
        [
            InlineKeyboardButton(text="История", callback_data=callback_data_history.pack())
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)