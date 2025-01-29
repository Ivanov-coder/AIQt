from utils import os
from utils import asyncio
from utils import GenerateID
from utils.settings import logger
from utils.colorful import SetColor

# TODO: frcolor的选择做出来
frcolor = SetColor.set_frcolor


class ChatWithAI:
    randID = GenerateID.get_id()

    # Record the id if generate .wav files
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
        For selecting models in the terminal,
        see _pages.SettingsPart, there has a page for selecting the model
        """
        # TODO: Hmm Can we just give the choice to a function in __init__.py? Just put those AI together I think
        # Though Spark AI don't support PERSONA, it'd be great if it can also support TTS.
        if self.choice == "1":
            import localAI

            self.count_ollama_wav += 1
            return localAI.ollamallm.CallOllamaAI(model=self.model).callByOllama(
                content=content,
                random_id=self.randID,
                count=self.count_ollama_wav,
                frcolor="lightblue",  # HERE
            )

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
                count=self.count_other_wav,
                frcolor="lightblue",  # HERE
            )

    async def _call(self):
        content = input(frcolor(text="\nPlease enter you questions") + ": ")
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
        try:
            asyncio.run(self._main())
        except KeyboardInterrupt:
            raise KeyboardInterrupt

        # This is the possible bug if the local environment hasn't proper module
        except ModuleNotFoundError as e:
            logger.warning(e)
            logger.info("Installing requirements...")
            stdstatus = os.system("pip install -r requirements.txt")

            if stdstatus == 0:
                logger.info("Requirements installed successfully.")
            else:
                raise RuntimeError("Failed to install requirements.")
