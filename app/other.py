import json
import os
import httpx
from tts import check_if_need_tts
from utils import logger, set_frcolor
from app.properties_handler import GetOtherProperties


class CallOtherAI:
    r"""
    用于调用其他AI.
    """

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        self.model = model
        self.CONF = GetOtherProperties().get_properties()  # Get the Properties
        self.PERSONA = self.CONF["PERSONA"]
        self.LANG = self.CONF["LANG"]
        self.isTTS = self.CONF["isTTS"]
        self.BASE_URL, self.API_KEY = self.CONF["link"], self.CONF["key"]

    def _write_cache(
        self,
        filename: str,
        ID: str,
        content: str,
        role: str = "user",
        isRolePlay: bool = False,
    ) -> None:
        r"""
        写入缓存到.cache/chat.json文件中
        """
        cache = self._load_data(filename, ID)["messages"]  # Append into the message.
        log = {  # Ensure that log is list
            "role": role,
            "content": content,
            "content_type": "text",
        }

        if isRolePlay and len(cache) == 0:  # Append prompt and ensure no repetitions
            cache.append(
                {
                    "role": "system",
                    "content": self.PERSONA
                    + f"Though you can speak other languages, you always speak {self.LANG}",  # 这一部分用于加上人格及设置语言
                    "content_type": "text",
                },
            )
        cache.append(log)
        with open(filename, "w", encoding="utf-8") as jf:
            json.dump(cache, jf, indent=4, ensure_ascii=False)

    # TODO: 上传图片的计划只能先搁置了
    def _load_data(self, filename: str, ID: str) -> dict:
        """
        加载文字或图片。
        图片请传入二进制数据
        """
        with open(filename, "r", encoding="utf-8") as jf:
            contents = json.load(jf)

        data = {
            "model": self.model,  # 指定请求的模型
            "messages": contents,
            # TODO: Qt中做成滑动条
            "top_p": 0.7,  # 用于控制生成文本的随机性，值越小，生成的文本越随机
            # TODO: Qt中做成滑动条
            "max_tokens": 4096,  # 用于控制生成文本的最大长度
        }

        return data

    def _select_tts(self, *items: tuple[str]) -> None:
        r"""
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
        r"""
        调用Spark AI.
        """
        async with httpx.AsyncClient(timeout=60) as aclient:
            try:
                response = await aclient.post(url, headers=header, json=data)
                if response.status_code == 200:
                    answer = json.loads(response.text)["choices"][0]["message"][
                        "content"
                    ]  # 获取回答 请自行查阅API文档
                    print(f"{set_frcolor(text=answer,color=frcolor)}", flush=True)
                    return answer
                else:
                    logger.warning(
                        f"Failed to request, STATUS_CODE: {response.status_code}"
                    )

            except Exception as e:
                logger.error(e)

    async def call(
        self,
        content: str,
        random_id: str,
        frcolor: str,
        count: int = 1,
    ) -> None:
        r"""
        :param:
            content (str):
                The content of the chat.
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

        # TODO: 需要把这个做出来到Qt中，成为滚动条去选择

        filename = f"./cache/chat{self.model}-{random_id}.json"
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as jf:
                json.dump([], jf)  # Initialize the chatlog

        try:
            header = {
                "Content-Type": "application/json",
                "Authorization": self.API_KEY,
            }

            self._write_cache(
                filename=filename, ID=random_id, content=content, isRolePlay=True
            )
            data = self._load_data(filename=filename, ID=random_id)
            answer = await self._execute(
                url=self.BASE_URL, header=header, data=data, frcolor=frcolor
            )
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

        # TODO: Qt信号槽事件 需要更改模型之后重新生成聊天记录文件 => 也就是当选择框改变字段时，重新调用get_id()方法

        except Exception as e:
            raise e
