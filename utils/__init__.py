import random
import dataclasses as dcl  # 用于数据类
import json_repair  # 用于修复可能有错误的json
import yaml
import asyncio
import json
import os
import typing
from . import settings
from . import logs
from . import colorful


__all__ = [
    "settings",
    "logs",
    "colorful",
    "dcl",
    "json_repair",
    "yaml",
    "asyncio",
    "json",
    "os",
    "typing",
]

# 初始化cache文件夹
if not os.path.exists("./cache"):
    os.mkdir("./cache")
if not os.path.exists("./config"):
    os.mkdir("./config")

available_encoding = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "I",
    10: "J",
    11: "K",
    12: "L",
    13: "M",
    14: "N",
    15: "O",
    16: "P",
    17: "Q",
    18: "R",
    19: "S",
    20: "T",
    21: "U",
    22: "V",
    23: "W",
    24: "X",
    25: "Y",
    26: "Z",
    27: "a",
    28: "b",
    29: "c",
    30: "d",
    31: "e",
    32: "f",
    33: "g",
    34: "h",
    35: "i",
    36: "j",
    37: "k",
    38: "l",
    39: "m",
    40: "n",
    41: "o",
    42: "p",
    43: "q",
    44: "r",
    45: "s",
    46: "t",
    47: "u",
    48: "v",
    49: "w",
    50: "x",
    51: "y",
    52: "z",
    53: "0",
    54: "1",
    55: "2",
    56: "3",
    57: "4",
    58: "5",
    59: "6",
    60: "7",
    61: "8",
    62: "9",
    63: "@",
    64: "#",
    65: "$",
    66: "%",
    67: "^",
    68: "&",
    69: "(",
    70: ")",
    71: "_",
    72: "!",
}


class GenerateID:
    """
    用于生成ID
    """

    @classmethod
    def _generate_id(cls, times: int = 10) -> str:
        """
        生成一个指定长度的随机字符串
        :param times: 长度
        """
        randId = "!"
        for _ in range(times):
            random_num = random.randint(1, 52)
            random_str = available_encoding[random_num]
            randId += random_str

        return randId

    @classmethod
    def get_id(cls, randKey: str = None) -> str:
        """
        当存在参数randKey使获取ID，
        否则两个都生成并返回。
        """
        ID = cls._generate_id()
        return ID


def setup_ollama():
    """
    安装ollama.
    配Docker镜像的时候才发现原本代码有大问题，忘记支持linux了...
    """
    # TODO: 这里似乎可以根据输出情况提醒用户打开Ollama应用
    if os.system("ollama --version") != 0:
        if os.name == "nt":
            settings.logger.warning(
                "Ollama is not installed, please download it from https://ollama.com/download/OllamaSetup.exe"
            )
        # elif os.name == "posix":  # 针对Linux
        #     os.system("snap install ollama")