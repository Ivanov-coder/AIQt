from colorama import init, Fore, Back


# 背景和文字的颜色设置只能二选一，比较尴尬
class SetColor:
    r"""
    Set the color in the terminal
    """

    def __init__(self):
        init(autoreset=True)

    @classmethod
    def set_frcolor(cls, *, text: str, color: str = "green") -> str:
        r"""
        Default is green
        """
        if color == "red":
            return Fore.RED + text + Fore.RESET
        elif color == "green":
            return Fore.GREEN + text + Fore.RESET
        elif color == "yellow":
            return Fore.YELLOW + text + Fore.RESET
        elif color == "blue":
            return Fore.BLUE + text + Fore.RESET
        elif color == "lightred":
            return Fore.LIGHTRED_EX + text + Fore.RESET
        elif color == "lightgreen":
            return Fore.LIGHTGREEN_EX + text + Fore.RESET
        elif color == "lightyellow":
            return Fore.LIGHTYELLOW_EX + text + Fore.RESET
        elif color == "lightblue":
            return Fore.LIGHTBLUE_EX + text + Fore.RESET

    @classmethod
    def set_bgcolor(cls, *, text: str, color: str) -> str:
        r"""
        Maybe not useful
        """
        if color == "red":
            return Back.RED + text + Back.RESET
        elif color == "green":
            return Back.GREEN + text + Back.RESET
        elif color == "yellow":
            return Back.YELLOW + text + Back.RESET
        elif color == "blue":
            return Back.BLUE + text + Back.RESET
