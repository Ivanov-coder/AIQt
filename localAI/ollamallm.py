import tts
import utils
import ollama


OLLAMA_CONF = utils.settings.SetYaml.read_yaml("settings.yml")["ollama_conf"]
PERSONA = OLLAMA_CONF[0]["PERSONA"]
LANG = OLLAMA_CONF[1]["LANG"]
isTTS = OLLAMA_CONF[2]["isTTS"]
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
        log = {  # Ensure that log is list
            "role": role,
            "content": content,
        }

        if isRolePlay and len(cache) == 0:  # Append prompt and ensure no repetitions
            cache.append(
                {
                    "role": "system",
                    "content": PERSONA
                    + f"Though you can speak other languages, you always speak {LANG}",  # 这一部分用于加上人格及设置语言
                },
            )
        cache.append(log)
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
        # TODO: 做出来给人选
        match items:
            case ["coqui", str(lang), str(content), str(path)]:
                tts.check_if_need_tts()(lang=lang, text=content, output_path=path).get()
            # TODO: 看下pytts怎么修：
            case ["pytts", str(content), str(path)]:
                tts.check_if_need_tts("pytts")(text=content, output_path=path).get()
            case _:
                raise ValueError("Please Check your parameters!")

    async def _execute(self, data: list[dict], frcolor: str) -> str:
        r"""
        内部逻辑
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

            print()
            return output

        # 本地没大模型就下载一个
        except ollama.ResponseError as re:
            utils.settings.logger.warning(f"ollama API error: {re}")
            utils.settings.logger.info("Now Downloading...")

            # TODO: 可能需要考虑把它可视化到Qt中, 毕竟这是控制台输出
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
            # if self.model == "llama3.2-vision":
            #     # TODO: 需要把这个做出来到Qt中，成为输入框
            #     if content.find("->") != -1:
            #         ctn, IMG_PATH = content.split("->")
            #     else:
            #         ctn = content
            #     image = base64.b64encode(open(IMG_PATH, "rb").read()).decode()
            #     self._write_cache(content=ctn, image=image)

            # else:
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
            # TODO: Give users a chance to choose for what TTS engine they want to use
            if isTTS:
                self._select_tts(
                    "coqui",
                    LANG,
                    answer,
                    f"./audio/chat{self.model}-{count}-{random_id}.wav",
                )

        except Exception as e:
            raise e
