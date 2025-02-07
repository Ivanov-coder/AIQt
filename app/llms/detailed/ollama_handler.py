import os
import json
import ollama
from tts import get_tts_socket
from utils import logger, set_frcolor
from ...properties.detailed.ollama_property_handler import GetOllamaProperties


class CallOllamaAI:
    r"""
    This model requires user to install Ollama and download local LLMs
    Theoretically, if those models exist in [ollama-library](https://ollama.com/library), the programme can run.

    Before using, ensure you run this code in terminal:
    >>> ollama pull <the_model_you_want>
    """

    _instance = None

    def __new__(cls, model):
        # XXX: Hmm there's no evidence prove that Sigleton Pattern does a good deal to the speed, but left here
        r"""Overloaded for Sigleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    # Defaults to llama3.1
    # if Pictures, get llama3.2-vision
    # But this model is a little bit slow, not reccommed
    def __init__(self, model="llama3.1"):
        self.model: str = model
        self.CONF: dict = GetOllamaProperties.get_properties()
        self.PERSONA: str = self.CONF["PERSONA"]
        self.LANG: str = self.CONF["LANG"]
        self.isTTS: str = self.CONF["isTTS"]

    def _write_cache(
        self,
        *,
        filename: str,
        ID: str,
        content: str,
        role: str = "user",
        isRolePlay: bool = False,
        image: str | bytes = None,
    ) -> None:
        r"""
        Writing chatlogs in the cache file
        """

        cache = self._load_data(filename, ID)
        # cache = []
        log = {  # Ensure that log is list
            "role": role,
            "content": content,
        }

        if isRolePlay and len(cache) == 0:  # Append prompt and ensure no repetitions
            cache.append(
                {
                    "role": "system",
                    "content": self.PERSONA
                    + f"Though you can speak other languages, you always speak {self.LANG}",  # 这一部分用于加上人格及设置语言
                },
            )
        cache.append(log)
        # print(cache)
        with open(filename, "w", encoding="utf-8") as jf:
            json.dump(cache, jf, indent=4, ensure_ascii=False)

    # XXX: 上传图片的计划只能先搁置了
    def _load_data(self, filename: str, ID: str) -> dict:
        r"""
        Load chatlog
        """
        with open(filename, "r", encoding="utf-8") as jf:
            contents = json.load(jf)

        return contents

    def _select_tts(
        self, model: str, filename: str, answer: str, lang: str = "en"
    ) -> None:
        r"""
        Select TTS engine, default to CoquiTTS
        """
        # FIXME: The parameters for TTS depends on the type the function returns...
        engine = get_tts_socket(model)(
            answer,
            output_path=filename,
            lang=lang,
            # TODO: Before a good solution, stop those API
            # rate=150,
            # volume=1.0,
            # emotion="Neutral",
            # speed=1.0,
        )
        engine.get()

    def _execute(self, data: list[dict], frcolor: str) -> str:
        r"""
        Inner logic
        """
        try:
            output = ""
            for part in ollama.Client(timeout=60).chat(
                model=self.model, messages=data, stream=True
            ):

                content = set_frcolor(text=part["message"]["content"], color=frcolor)
                print(content, end="", flush=True)
                output += part["message"]["content"]
            print()  # Used to print '\n'
            return output

        # TODO: If no LLM models, download
        # FIXME: Here we'd better avoid blocking MainThread, by `subprocess.run` may be good
        # While downloading the model, use other model to chat.
        # TODO: Do we need add the logic(del llm)

        except Exception as e:
            raise e

    def call(
        self,
        random_id: str,
        frcolor: str,
        count: int = 1,
    ) -> None:
        r"""
        Invoking the model in ollama to chat.
        :param:
            random_id (str):
                Randomly generated id.
                The main function of it is to distinguish users by different id, in order to classfiy the chatlog of users.
            isTTS (bool):
                Check if users need TTS.
                When first call the function, it'll check what TTS the user needs, and then mainly by this TTS.
            frcolor (str):
                Used to control the color of the output in the terminal.
            count (int, default is 1):
                Used to sort the order of each .wav file.
        """
        logger.info(f"Invoking {self.model.upper()} API...")

        pathdir = f"./cache/chat{self.model}"
        if not os.path.exists(pathdir):
            os.mkdir(pathdir)

        filename = os.path.join(pathdir, f"chat{self.model}-{random_id}.json")
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as jf:
                json.dump([], jf)  # Initialize the chatlog

        content = input(set_frcolor(text="\nPlease enter you questions") + ": ")
        self._write_cache(
            filename=filename, ID=random_id, content=content, isRolePlay=True
        )

        try:
            data = self._load_data(filename=filename, ID=random_id)
            answer = self._execute(data=data, frcolor=frcolor)
            self._write_cache(
                filename=filename,
                ID=random_id,
                content=answer,
                role="assistant",
                isRolePlay=True,
            )
            if self.isTTS:
                self._select_tts(
                    model="pytts",
                    lang=self.LANG,
                    answer=answer,
                    # FIXME: The step filename seems to be useless... The count is stuck at 1
                    filename=f"./audio/chat{self.model}/chat{self.model}-{count}-{random_id}.wav",
                )

        except Exception as e:
            raise e
