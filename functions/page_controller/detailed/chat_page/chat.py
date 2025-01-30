import os
import asyncio
from app import get_socket
from utils import generate_id
from utils import logger
from utils import set_frcolor


class ChatWithAI:
    # Record the id if generate .wav files
    # count_other_wav = 0
    # count_ollama_wav = 0
    count_wav = 0
    randID = generate_id()
    num_to_app_orm = {
        "1": "ollama",
        "2": "spark",
        "3": "other",
    }

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
        self.count_wav += 1
        CallAI = get_socket(
            self.num_to_app_orm.get(self.choice, "ollama"),
        )
        return CallAI(model=self.model).call(
            content=content,
            random_id=self.randID,
            count=self.count_wav,
            frcolor="lightblue",  # HERE
        )

    async def _call(self):
        content = input(set_frcolor(text="\nPlease enter you questions") + ": ")
        await self._switch(content)

    async def _main(self):
        try:
            await self._call()
        except EOFError:
            print(set_frcolor(text="Hey! Please Enter Something!\n", color="red"))
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
