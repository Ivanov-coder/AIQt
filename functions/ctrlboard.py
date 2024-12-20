from ._pages import *
from utils import os
from utils import asyncio
from utils import GenerateID
from utils.settings import logger


class CtrlBoard:
    r"""
    Use the board to control the behavior of our user
    """

    @classmethod
    def run(cls):
        # cls._start()
        cls._choose()

    def _status_now(cls):
        pass

    # @staticmethod
    # def _start() -> None:

    @staticmethod
    def _choose():
        # 这里可能需要实现状态机功能，我们需要判断是哪个页面
        print(MainPart.main_page)
        choice = input("Please enter the key you want: ")
        if choice == "1":
            Chat.chat()

        if choice.upper() == "E":
            exit()


class Chat:
    randID = GenerateID.get_id()

    # 当生成wav时记录音频编号
    count_other_wav = 0
    count_ollama_wav = 0

    @classmethod
    def _switch(cls, choice: str):
        r"""
        做选择用的，后面估计得做到Qt选择框里面。
        """
        # TODO: 这里的实例化需要做成选择框给用户选择模型
        if choice == "web-spark":
            from webAI import spark

            return spark.CallSparkAI(model="lite").callByhttpx(random_id=cls.randID)

        elif choice == "web-other":
            from webAI import other

            cls.count_other_wav += 1

            return other.CallOtherAI(model="qwen-long").callByhttpx(
                random_id=cls.randID,
                isTTS=True,
                count=cls.count_other_wav,
                frcolor="lightblue",  # TODO: isTTS frcolor做出来
            )

        elif choice == "local":
            import localAI

            cls.count_ollama_wav += 1

            # TODO: 这里的实例化需要做成选择框给用户选择模型
            return localAI.ollamallm.CallOllamaAI(model="llama3.1").callByOllama(
                random_id=cls.randID,
                isTTS=True,
                count=cls.count_ollama_wav,
                frcolor="lightblue",  # TODO: isTTS frcolor做出来
            )

    @classmethod
    # TODO: 在Qt中可能会存在开了Spark之后又开其它的情况，所以这里我们可能需要当窗口焦点改变时，做个挂起操作。
    async def _run(cls):
        # TODO: 这里的实例化需要做成选择框给用户选择模型
        choice = "local"
        await cls._switch(choice)

    @classmethod
    async def _main(cls):
        await cls._run()

    @classmethod
    def chat(cls):
        r"""
        Begin chat
        """
        while True:
            try:
                asyncio.run(cls._main())
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
