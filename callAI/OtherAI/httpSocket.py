import json
import time
import asyncio
import httpx
import utils
from langchain_community.llms import openai
import lib.data.aiData as AI  # 此导包方式只支持在main.py中运行

# 用于打印日志
logger = utils.logs.Logger.setup_logger(fileposition= __name__)

# 需要把这个做出来到Qt中，成为滚动条去选择
# 这里只支持调用其他AI 请不要在这里调用Spark AI



@utils.dcl.dataclass
class CallOherAI:
    model: str = "qwen-long"  # 如果有需要 请自行修改参数 默认为qwen-long
    BASE_URL, API_KEY = AI.start("2", model)

    def callByLangchain(self) -> None:
        """
        用于调用AI。
        你需要输入你想提问的问题。
        """

        # 需要把这个做出来到Qt中，成为输入框
        content = input("请输入您的问题：")

        response = openai(self.model, content)
        print(f'{self.model.upper()} : {response}')

    def callByhttpx(self) -> None:
        """
        用于调用AI。
        你需要输入你想提问的问题。
        """

        # 需要把这个做出来到Qt中，成为输入框
        content = input("请输入您的问题：")

        headers = {"Authorization": self.API_KEY}
        data = {
            "messages": [{
                "role": "user",
                "content": content,
            }],
            "model": self.model,
        }
        response = httpx.post(self.BASE_URL, headers=headers, json=data)

        try:
            answer = response.json()["choices"][0]["message"][
                "content"]  # 获取回答 不知数据结构以后是否变动
            print(f'{self.model.upper()} : {answer}')
        except:
            logger.error("获取回答失败，请检查json结构是否变动")