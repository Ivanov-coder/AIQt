import os
from .tts_registor import TTSRegister


__all__ = []

# 初始化一下储存.wav的文件夹
if not os.path.exists("./audio"):
    os.mkdir("./audio")


# TODO: Use tts_register to get the tts models