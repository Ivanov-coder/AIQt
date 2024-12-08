import os

CACHE_PATH = "./cache/"
LOG_PATH = "./log/data.log"


def clean() -> None:
    """
    清除聊天记录。
    """

    if os.path.exists(CACHE_PATH):
        for file in os.listdir(CACHE_PATH):
            os.remove(os.path.join(CACHE_PATH, file))
