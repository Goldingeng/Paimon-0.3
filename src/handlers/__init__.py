from .menu_handler import menu_router
from .banner_handler import banner_router
from .moder_menu import moder_router
from .pumping_handler import pumping_router
from .nick_handler import nick_router
from .status_handler import status_router
from .help_handler import help_router


#message_router должен быть последним!
from .message_handler import message_router



all_routers = []

for var in globals().copy():
    if not var.endswith("router"):
        continue

    all_routers.append(globals()[var])