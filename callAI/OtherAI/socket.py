import json
import time
import asyncio
import httpx
import utils
from langchain_community.llms import openai
import lib.data.aiData as AI  # 此导包方式只支持在main.py中运行


@utils.dcl.dataclass
class CallOherAI:
    """
    用于调用其他AI.
    使用时
    """
    model: str = "qwen-long"  # 如果有需要 请自行修改参数 默认为qwen-long

    def _get_logger(self) -> tuple[str, str, utils.logs.Logger]:
        """
        用于获取BASE_URL, API_KEY, logger
        """

        BASE_URL, API_KEY = AI.start("2", self.model)
        logger = utils.logs.Logger.setup_logger(fileposition=__name__)
        return BASE_URL, API_KEY, logger

    def callByLangchain(self) -> None:
        """
        用于调用AI。
        你需要输入你想提问的问题。
        """

        # 一些基础设定和日志 确保只有执行callByhttpx函数时才被执行 而不是导包后就被执行
        BASE_URL, API_KEY, logger = self._get_logger()

        # TODO: 需要把这个做出来到Qt中，成为输入框
        content = input("请输入您的问题：")

        response = openai(self.model, content)
        print(f'{self.model.upper()} : {response}')

    def callByhttpx(self) -> None:
        """
        用于调用AI。
        你需要输入你想提问的问题。
        """

        # 一些基础设定和日志 确保只有执行callByhttpx函数时才被执行 而不是导包后就被执行
        BASE_URL, API_KEY, logger = self._get_logger()

        # TODO: 需要把这个做出来到Qt中，成为输入框
        content = input("请输入您的问题：")

        headers = {"Authorization": API_KEY}
        data = {
            "messages": [{
                "role": "user",
                "content": content,
            }],
            "model": self.model,
        }
        response = httpx.post(BASE_URL, headers=headers, json=data)

        try:
            answer = response.json()["choices"][0]["message"][
                "content"]  # 获取回答 不知数据结构以后是否变动
            print(f'{self.model.upper()} : {answer}')
        except:
            logger.error("获取回答失败，请检查json结构是否变动")
