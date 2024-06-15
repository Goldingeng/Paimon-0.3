from aiogram.filters.callback_data import CallbackData


class ProfileCallback(CallbackData, prefix="menu"):
    user_id: int

class HistoryCallback(CallbackData, prefix="history"):
    user_id: int

class BannerCallback(CallbackData, prefix="banner"):
    user_id: int

class TwistCallbackc(CallbackData, prefix="twist"):
    user_id: int
    count: int

class BagCallbackc(CallbackData, prefix="bag"):
    user_id: int

class CharactersCallbackc(CallbackData, prefix="characters"):
    user_id: int
    page: int = 0

class PumpingCallbackc(CallbackData, prefix="pumping"):
    user_id: int


