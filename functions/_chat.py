from utils import os
from utils import asyncio
from utils import GenerateID
from utils import setup_ollama
from utils.settings import logger
from utils.colorful import SetColor


frcolor = SetColor.set_frcolor


class ChatWithAI:
    randID = GenerateID.get_id()

    # 当生成wav时记录音频编号
    count_other_wav = 0
    count_ollama_wav = 0

    def __init__(self, choice: str = "1", model: str = "llama3.1"):
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
        if self.choice == "1":
            import localAI

            setup_ollama()

            self.count_ollama_wav += 1

            # TODO: 这里的实例化需要做成选择框给用户选择模型
            return localAI.ollamallm.CallOllamaAI(model=self.model).callByOllama(
                content=content,
                random_id=self.randID,
                isTTS=True,
                count=self.count_ollama_wav,
                frcolor="lightblue",  # TODO: isTTS frcolor做出来
            )
        # TODO: 这里的实例化需要做成选择框给用户选择模型

        elif self.choice == "2":
            from webAI import spark

            return spark.CallSparkAI(model=self.model).callByhttpx(
                content=content, random_id=self.randID
            )

        elif self.choice == "3":
            from webAI import other

            self.count_other_wav += 1

            return other.CallOtherAI(model=self.model).callByhttpx(
                content=content,
                random_id=self.randID,
                isTTS=True,
                count=self.count_other_wav,
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
                raise KeyboardInterrupt

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
