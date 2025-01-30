import os
import random
from .logs import Logger
from .set_color import SetColor
from .yaml_handler import handle_yaml

logger = Logger.setup_logger()
set_frcolor = SetColor.set_frcolor
set_bgcolor = SetColor.set_bgcolor

__all__ = [
    "logger",
    "generate_id",
    "handle_yaml",
    "set_frcolor",
    "set_bgcolor",
]

# 初始化cache文件夹
if not os.path.exists("./cache"):
    os.mkdir("./cache")
if not os.path.exists("./config"):
    os.mkdir("./config")


def generate_id(times: int = 4) -> str:
    r"""
    This is used to generate a random ID for chatlogs and audio waves.
    Generate a random ID in particular length
    :param:
        times: loop times for generating length
    """
    randID = "!"
    for _ in range(times):
        # Avoid generating the strings that Windows doesn't allows, and replace with "!"
        # when randint is subset of [48, 126], these are possible conditions
        # Check by: ` for i in range(48,127):print(chr(i), end="") if chr(i) in '\/:"?*<>|' else print("", end="")`
        random_str = chr(random.randint(48, 126))
        randID += random_str if random_str not in ":<>?\|" else "!"

    return randID
