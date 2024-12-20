from utils import os
from ._check import check_if_need_tts

__all__ = [
    "check_if_need_tts",
]

# 初始化一下储存.wav的文件夹
if not os.path.exists("./audio"):
    os.mkdir("./audio")
