from colorama import init, Fore, Back, Style

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
            return Fore.RED + text + Style.RESET
        elif color == "green":
            return Fore.GREEN + text + Style.RESET
        elif color == "yellow":
            return Fore.YELLOW + text + Style.RESET
        elif color == "blue":
            return Fore.BLUE + text + Style.RESET
    
    @classmethod
    def set_bgcolor(cls, *, text: str, color: str) -> str:
        """
        Maybe not useful
        """
        if color == "red":
            return Back.RED + text + Style.RESET
        elif color == "green":
            return Back.GREEN + text + Style.RESET
        elif color == "yellow":
            return Back.YELLOW + text + Style.RESET
        elif color == "blue":
            return Back.BLUE + text + Style.RESET
        