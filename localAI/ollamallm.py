import tts
import utils
import ollama

color = utils.colorful.SetColor


class CallOllamaAI:
    r"""
    This model requires user to install Ollama and download local LLMs
    Theoretically ,if those models exist in [ollama-library](https://ollama.com/library), the programme can run.
    ### Before using, ensure you run this code in terminal:
    >>> ollama pull <the_model_you_want>
    """

    # Default to llama3.1
    # if Pictures, get llama3.2-vision
    # But this model is a little bit slow, not reccommed
    def __init__(self, model="llama3.1"):
        self.OLLAMA_CONF: dict = utils.settings.SetYaml.read_yaml("settings.yml")[
            "ollama_conf"
        ]
        self.PERSONA: str = self.OLLAMA_CONF["PERSONA"]
        self.LANG: str = self.OLLAMA_CONF["LANG"]
        self.isTTS: str = self.OLLAMA_CONF["isTTS"]
        self.model: str = model

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
            utils.json.dump(cache, jf, indent=4, ensure_ascii=False)

    # XXX: 上传图片的计划只能先搁置了
    def _load_data(self, filename: str, ID: str) -> dict:
        r"""
        Load chatlog
        """
        with open(filename, "r", encoding="utf-8") as jf:
            contents = utils.json.load(jf)

        return contents

    def _select_tts(self, *items: tuple[str]) -> None:
        r"""
        Select TTS engine, default to CoquiTTS
        """
        match items:
            case ["coqui", str(lang), str(content), str(path)]:
                tts.check_if_need_tts()(lang=lang, text=content, output_path=path).get()
            case ["pytts", str(content), str(path)]:  # 可以考虑放弃pytts？太难听了
                tts.check_if_need_tts("pytts")(text=content, output_path=path).get()
            case _:
                raise ValueError("Please Check your parameters!")

    async def _execute(self, data: list[dict], frcolor: str) -> str:
        r"""
        Inner logic
        """
        try:
            output = ""
            async for part in await ollama.AsyncClient().chat(
                model=self.model, messages=data, stream=True
            ):

                content = color.set_frcolor(
                    text=part["message"]["content"], color=frcolor
                )
                print(content, end="", flush=True)
                output += part["message"]["content"]
            print()  # Used to print '\n'
            return output

        # 本地没大模型就下载一个
        except ollama.ResponseError as re:
            utils.settings.logger.warning(f"ollama API error: {re}")
            utils.settings.logger.info("Now Downloading...")

            # FIXME: Here we'd better avoid blocking MainThread, by `subprocess.run` may be good
            # While downloading the model, use other model to chat.
            utils.os.system(f"ollama pull {self.model}")
            # TODO: 是否还需要考虑添加删除大模型的功能？

        except Exception as e:
            raise e

    async def callByOllama(
        self,
        content: str,
        random_id: str,
        frcolor: str,
        count: int = 1,
    ) -> None:
        r"""
        Invoking the model in ollama to chat
        :param random_id: randomly generated id.
        The main function of it is to distinguish users by different id, in order to classfiy the chatlog of users.
        :param isTTS: Check if users need TTS.
        :param count: Used to sort the order of each .wav file.
        """
        utils.settings.logger.info(f"Invoking {self.model.upper()} API...")

        filename = f"./cache/chat{self.model}-{random_id}.json"
        if not utils.os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as jf:
                utils.json.dump([], jf)  # Initialize the chatlog
        try:
            self._write_cache(
                filename=filename, ID=random_id, content=content, isRolePlay=True
            )

        except Exception:
            return

        try:
            data = self._load_data(filename=filename, ID=random_id)
            answer = await self._execute(data=data, frcolor=frcolor)
            self._write_cache(
                filename=filename,
                ID=random_id,
                content=answer,
                role="assistant",
                isRolePlay=True,
            )
            if self.isTTS:
                self._select_tts(
                    "coqui",
                    self.LANG,
                    answer,
                    f"./audio/chat{self.model}-{count}-{random_id}.wav",
                )

        except Exception as e:
            raise e
