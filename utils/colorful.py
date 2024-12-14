from colorama import init, Fore, Back


# 背景和文字的颜色设置只能二选一，比较尴尬
class SetColor:
    """
    设置在控制台中的颜色 ，也许有用。
    """

    def __init__(self):
        init(autoreset=True)

    @classmethod
    def set_frcolor(cls, *, text: str, color: str = "green") -> str:
        """
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

    @classmethod
    def set_bgcolor(cls, *, text: str, color: str) -> str:
        """
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