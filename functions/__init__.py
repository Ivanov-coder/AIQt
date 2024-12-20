from ._pages import MainPart
from . import ctrlboard
from .ctrlboard import CtrlBoard


__all__ = [
    "ctrlboard",
    "CtrlBoard"
]


print(MainPart.welcome_page)  # Welcome User when initialize
