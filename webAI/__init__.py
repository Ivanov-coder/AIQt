from . import spark
from . import other

__all__ = ["spark", "other"]

# TODO: May be useful
# def choose_which_to_import(choice: str = "2"):
#     if choice == "2":
#         from .spark import CallSparkAI

#         return CallSparkAI
#     elif choice == "3":
#         from .other import CallOtherAI

#         return CallOtherAI


# __all__ = ["choose_which_to_import"]
