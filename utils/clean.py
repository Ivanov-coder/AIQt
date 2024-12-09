import os

CACHE_PATH = "./cache/"
AUDIO_PATH = "./audio"


def clean() -> None:
    """
    清除聊天记录/音频。
    """

    if os.path.exists(CACHE_PATH):
        for file in os.listdir(CACHE_PATH):
            os.remove(os.path.join(CACHE_PATH, file))
    
    if os.path.exists(AUDIO_PATH):
        for file in os.listdir(AUDIO_PATH):
            os.remove(os.path.join(AUDIO_PATH, file))
