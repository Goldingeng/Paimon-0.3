from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .callback import *

def pumping_markup(user_id: int):

    callback_data_bag = BagCallbackc(user_id=user_id)

    callback_data_profile = ProfileCallback(user_id=user_id)
    
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Мешок ⬆️", callback_data=callback_data_bag.pack())
        ],

        [
            InlineKeyboardButton(text="Профиль",  callback_data=callback_data_profile.pack())
        ],
        [
            InlineKeyboardButton(text="Канал",  url="https://t.me/genshintwist")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)