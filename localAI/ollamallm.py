import tts
import utils
import ollama
import base64

OLLAMA_CONF = utils.settings.SetYaml.read_yaml("settings.yml")["ollama_conf"]
PERSONA = OLLAMA_CONF[0]["PERSONA"]
LANG = OLLAMA_CONF[1]["LANG"]
isTTS = OLLAMA_CONF[2]["isTTS"]
color = utils.colorful.SetColor


@utils.dcl.dataclass
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
    model: str = utils.dcl.field(default="llama3.1")

    @utils.typing.overload
    def _write_cache(self, *, ID: str, content: str, role: str = "user") -> None: ...

    @utils.typing.overload
    def _write_cache(
        self, *, ID: str, content: str, role: str = "user", image: str | bytes
    ) -> None: ...

    @utils.typing.overload
    def _write_cache(
        self, *, ID: str, content: str, role: str = "user", isRolePlay: bool
    ) -> None: ...

    @utils.typing.overload
    def _write_cache(
        self,
        *,
        ID: str,
        content: str,
        role: str = "user",
        isRolePlay: bool,
        image: str | bytes,
    ) -> None: ...

    def _write_cache(
        self,
        *,
        ID: str,
        content: str,
        role: str = "user",
        isRolePlay: bool = False,
        image: str | bytes = None,
    ) -> None:
        r"""
        Writing chatlogs in the cache file
        """

        # XXX: 出于性能方面的考虑 暂时决定不添加多模态功能
        if image and self.model == "llama3.2-vision":
            # Ensure for list
            if not isinstance(image, list):
                image = [image]

            log = {
                "role": role,
                "content": content,
                "images": image,
            }

        else:
            log = {
                "role": role,
                "content": content,
            }

        log = {
            "role": role,
            "content": content,
        }

        with open(f"./cache/chat{self.model}-{ID}.json", "a+", encoding="utf-8") as jf:

            cache = utils.json_repair.load(jf)

            if not isinstance(cache, list):
                if isRolePlay:
                    log = [log] # Ensure the log is list
                    log.insert( # Give prompts here
                        0,
                        {
                            "role": "system",
                            "content": PERSONA
                            + f"Though you can speak other languages, you always speak {LANG}",  # 这一部分用于加上人格及设置语言
                        },
                    )
                    print()
                    cache = log
            else:
                cache.append(log)

        with open(f"./cache/chat{self.model}-{ID}.json", "w", encoding="utf-8") as jf:
            utils.json.dump(cache, jf, indent=4, ensure_ascii=False)

    # XXX: 上传图片的计划只能先搁置了
    def _load_data(self, ID: str) -> dict:
        r"""
        Load chatlog
        """
        with open(f"./cache/chat{self.model}-{ID}.json", "r", encoding="utf-8") as jf:
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

        # FIXME: DEBUG 有时能看到图片有时不能 并且不支持图片之后只有文字输入
        try:
            if self.model == "llama3.2-vision":
                # TODO: 需要把这个做出来到Qt中，成为输入框
                if content.find("->") != -1:
                    ctn, IMG_PATH = content.split("->")
                else:
                    ctn = content
                image = base64.b64encode(open(IMG_PATH, "rb").read()).decode()
                self._write_cache(content=ctn, image=image)

            else:
                self._write_cache(ID=random_id, content=content, isRolePlay=True)

        except Exception:
            return

        try:
            data = self._load_data(ID=random_id)
            answer = await self._execute(data=data, frcolor=frcolor)
            self._write_cache(
                ID=random_id, content=answer, role="assistant", isRolePlay=True
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
