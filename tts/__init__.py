import os
from .coquiTTS import coquiTTS
from .pyTTS import pyTTS

__all__ = [
    "coquiTTS",
    "pyTTS",
]

# 初始化一下储存.wav的文件夹
if not os.path.exists("./audio"):
    os.mkdir("./audio")
