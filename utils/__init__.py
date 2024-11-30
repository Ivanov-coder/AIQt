import dataclasses as dcl  # 用于数据类
import typing
from . import logs
import json_repair  # 用于修复可能有错误的json
import asyncio
import websockets
import json
import os
from . import settings
import yaml
from . import clean
from . import colorful
import random

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

id_to_random = {}


class GenerateID:
    """
    用于生成ID
    """

    @classmethod
    def _write_into_dict(cls) -> str:
        """
        对于每次调用，都写入日志当中。
        """
        log = ""
        for _ in range(10):
            log_num = random.randint(53, 72)
            log_key = available_encoding[log_num]
            log += log_key

        return log

    @classmethod
    def _check_if_in_dict(cls, log_id: str) -> bool:
        """
        检查是否在字典中
        """
        return log_id in id_to_random

    @classmethod
    def _generate_id(cls, times: int = 10) -> tuple[str, str]:
        """
        生成一个指定长度的随机字符串
        :param times: 长度
        """
        randId = "!"
        for _ in range(times):
            random_num = random.randint(1, 52)
            random_str = available_encoding[random_num]
            randId += random_str

        randKey = cls._write_into_dict()
        id_to_random[randKey] = randId
        return randKey, randId

    @typing.overload
    def get_id(self, randKey: str) -> str:
        ...

    @typing.overload
    def get_id(self, randKey: str = None) -> tuple[str, str]:
        ...

    @classmethod
    def get_id(cls, randKey: str = None) -> (str | tuple[str, str]):
        """
        当存在参数randKey使获取ID，
        否则两个都生成并返回。
        """
        if randKey:
            if cls._check_if_in_dict(randKey):
                return id_to_random[randKey]

        else:
            KEY, ID = cls._generate_id()
            return KEY, ID


def setup_ollama():
    """
    安装ollama
    """
    if os.system("winget list ollama") != 0:
        os.system("winget install ollama")

setup_ollama()
