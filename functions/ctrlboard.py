from ._pages import *
from utils import os
from utils import asyncio
from utils import json
from utils import GenerateID
from utils import setup_ollama
from utils.settings import logger
from utils.colorful import SetColor

frcolor = SetColor.set_frcolor


class CtrlBoard:
    r"""
    Use the board to control the behavior of our user
    """

    @classmethod
    def run(cls):
        # cls._start()
        cls._choose()

    def _status_now(cls):
        # 用于记录是第几个页面
        pass

    @staticmethod
    def _write_into_conf(**kwargs) -> None:
        # 第一次使用时将选择和大模型写入文件 之后再通过设置界面更改
        pass

    @staticmethod
    def _choose():
        # 这里可能需要实现状态机功能，我们需要判断是哪个页面

        if (
            not input(
                frcolor(text="\nPress Any Key here")
                + frcolor(text="(E to exit): ", color="red")
            ).upper()
            == "E"
        ):
            print(MainPart.main_page)
            choice = input(frcolor(text="\nPlease enter the key you want: "))
            # 这里面的嵌套if想办法优化一下
            if choice == "1":
                Chat(choice="ollama", model="llama3.1").chat()

            elif choice.upper() == "E":
                exit()

        else:
            exit()


class Chat:
    randID = GenerateID.get_id()

    # 当生成wav时记录音频编号
    count_other_wav = 0
    count_ollama_wav = 0

    def __init__(self, choice: str = "ollama", model: str = "llama3.1"):
        r"""
        :param: choice: str -> Select the APP you want to use
        :param: model: str -> Select the model you want to use
        """
        self.choice = choice
        self.model = model

    def _switch(self, content: str):
        r"""
        做选择用的，后面估计得做到Qt选择框里面。
        """
        # TODO: 这里的实例化需要做成选择框给用户选择模型
        if self.choice == "spark":
            from webAI import spark

            return spark.CallSparkAI(model="lite").callByhttpx(
                content=content, random_id=self.randID
            )

        elif self.choice == "other":
            from webAI import other

            self.count_other_wav += 1

            return other.CallOtherAI(model="qwen-long").callByhttpx(
                content=content,
                random_id=self.randID,
                isTTS=True,
                count=self.count_other_wav,
                frcolor="lightblue",  # TODO: isTTS frcolor做出来
            )

        elif self.choice == "ollama":
            import localAI

            setup_ollama()

            self.count_ollama_wav += 1

            # TODO: 这里的实例化需要做成选择框给用户选择模型
            return localAI.ollamallm.CallOllamaAI(model="llama3.1").callByOllama(
                content=content,
                random_id=self.randID,
                isTTS=True,
                count=self.count_ollama_wav,
                frcolor="lightblue",  # TODO: isTTS frcolor做出来
            )

    async def _call(self):
        content = input(
            frcolor(text="\nPlease enter you questions: ") + "_____\b\b\b\b\b"
        )
        await self._switch(content)

    async def _main(self):
        try:
            await self._call()
        except EOFError:
            print(frcolor(text="Hey! Please Enter Something!\n", color="red"))
            await self._call()

    def chat(self):
        r"""
        Begin chatting
        """
        while True:
            try:
                asyncio.run(self._main())
            except KeyboardInterrupt:
                CtrlBoard.run()

            # XXX: 这是本地情况
            except ModuleNotFoundError as e:
                logger.warning(e)
                logger.info("Installing requirements...")
                stdstatus = os.system("pip install -r requirements.txt")

                if stdstatus == 0:
                    logger.info("Requirements installed successfully.")
                else:
                    logger.error("Failed to install requirements.")
                    break
            # PS 如果出了什么bug需要调试，请直接注释掉下面那一段
            # except Exception as e:
            #     logger.error(e)
            #     logger.info("Restarted")
