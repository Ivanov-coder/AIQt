import tts
import httpx
import utils
import data.aiData as AI

OTHER_CONF = utils.settings.SetYaml.read_yaml("settings.yml")["other_conf"]
PERSONA = OTHER_CONF[2]["PERSONA"]
LANG = OTHER_CONF[3]["LANG"]
isTTS = OTHER_CONF[4]["isTTS"]
color = utils.colorful.SetColor


@utils.dcl.dataclass
class CallOtherAI:
    r"""
    用于调用其他AI.
    """

    model: str = "gpt-3.5-turbo"  # 如果有需要 请自行修改参数 默认为gpt-3.5-turbo

    def _write_cache(
        self, ID: str, content: str, role: str = "user", isRolePlay: bool = False
    ) -> None:
        """
        写入缓存到.cache/chat.json文件中
        """

        log = {
            "role": role,
            "content": content,
            "content_type": "text",
        }

        with open(f"./cache/chat{self.model}-{ID}.json", "a+", encoding="utf-8") as jf:

            cache = utils.json_repair.load(jf)

            if not isinstance(cache, list):
                if isRolePlay:
                    log = [log]
                    log.insert(
                        0,
                        {
                            "role": "system",
                            "content": PERSONA,
                            "content_type": "text",
                        },
                    )
                    cache = log
            else:
                cache.append(log)

        with open(f"./cache/chat{self.model}-{ID}.json", "w", encoding="utf-8") as jf:
            utils.json.dump(cache, jf, indent=4, ensure_ascii=False)

    # TODO: 上传图片的计划只能先搁置了
    def _load_data(self, ID: str) -> dict:
        """
        加载文字或图片。
        图片请传入二进制数据
        """
        with open(f"./cache/chat{self.model}-{ID}.json", "r", encoding="utf-8") as jf:
            contents = utils.json.load(jf)

        data = {
            "model": self.model,  # 指定请求的模型
            "messages": contents,
            # TODO: Qt中做成滑动条
            "top_p": 0.7,  # 用于控制生成文本的随机性，值越小，生成的文本越随机
            # TODO: Qt中做成滑动条
            "max_tokens": 4096,  # 用于控制生成文本的最大长度
        }

        return data

    def _get_logger(
        self,
    ) -> tuple[str, str, utils.logs.Logger] | utils.logs.Logger:
        """
        用于获取BASE_URL, API_KEY, logger。
        """
        BASE_URL, API_KEY = AI.start("2", self.model)

        return BASE_URL, API_KEY

    def _select_tts(self, *items: tuple[str]) -> None:
        """
        选择TTS引擎，默认是coquiTTS
        """
        # TODO: 做出来给人选
        # TODO: 配置一下如何搞定路径和语速
        match items:
            case ["coqui", str(lang), str(content), str(path)]:
                tts.check_if_need_tts()(lang=lang, text=content, output_path=path).get()
            # TODO: 看下pytts怎么修：
            case ["pytts", str(content), str(path)]:
                tts.check_if_need_tts("pytts")(text=content, output_path=path).get()
            case _:
                raise ValueError("Please Check your parameters!")

    # XXX: 上传图片的计划只能先搁置了

    # 调用的内部逻辑
    async def _execute(
        self, *, url: str, header: dict, data: dict, frcolor: str
    ) -> str:
        """
        调用Spark AI.

        """

        async with httpx.AsyncClient(timeout=60) as aclient:
            try:
                response = await aclient.post(url, headers=header, json=data)
                if response.status_code == 200:
                    answer = utils.json_repair.loads(response.text)["choices"][0][
                        "message"
                    ][
                        "content"
                    ]  # 获取回答 请自行查阅API文档
                    print(f"{color.set_frcolor(text=answer,color=frcolor)}")
                    return answer
                else:
                    utils.settings.logger.warning(
                        f"Failed to request, STATUS_CODE: {response.status_code}"
                    )

            except Exception as e:
                utils.settings.logger.error(e)

    async def callByhttpx(
        self,
        content: str,
        random_id: str,
        frcolor: str,
        count: int = 1,
    ) -> None:
        """
        调用其他的AI
        """
        
        # TODO: 需要把这个做出来到Qt中，成为滚动条去选择
        BASE_URL, API_KEY = AI.start("2", self.model)

        try:
            header = {
                "Content-Type": "application/json",
                "Authorization": API_KEY,
            }

            self._write_cache(ID=random_id, content=content, isRolePlay=True)
            data = self._load_data(ID=random_id)
            answer = await self._execute(
                url=BASE_URL, header=header, data=data, frcolor=frcolor
            )
            self._write_cache(
                ID=random_id, content=answer, role="assistant", isRolePlay=True
            )
            if isTTS:
                self._select_tts(
                    "coqui",
                    LANG,
                    answer,
                    f"./audio/chat{self.model}-{count}-{random_id}.wav",
                )

        # TODO: Qt信号槽事件 需要更改模型之后重新生成聊天记录文件 => 也就是当选择框改变字段时，重新调用get_id()方法

        except Exception as e:
            raise e
