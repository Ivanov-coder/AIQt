import json
import os
import httpx
from tts import get_tts_socket
from utils import logger
from utils import set_frcolor
from ...properties.detailed.spark_property_handler import GetSparkProperties


class CallSparkAI:
    r"""
    The Class is for Spark AI
    >>> spark = CallSparkAI(model="lite") # Invoking lite model
    Supported models are as follows:
    - lite
    - generalv3
    - pro-128k
    - generalv3.5
    - max-32k
    - 4.0Ultra
    """

    def __init__(self, model: str = "lite"):
        self.model: str = model
        self.CONF = GetSparkProperties().get_properties()
        self.LANG = self.CONF["LANG"]
        self.isTTS = self.CONF["isTTS"]
        self.BASE_URL, self.API_KEY = self.CONF["link"], self.CONF["key"][self.model]

    # XXX: 讯飞星火lite不支持角色扮演
    def _write_cache(
        self,
        filename: str,
        ID: str,
        content: str,
        role: str = "user",
        isRolePlay: bool = False,
    ) -> None:
        r"""
        Write chatlog into the files.
        """

        cache = self._load_data(filename, ID)["messages"]  # Append into the message.
        log = {  # Ensure that log is list
            "role": role,
            "content": content,
            "content_type": "text",
        }
        cache.append(log)
        with open(filename, "w", encoding="utf-8") as jf:
            json.dump(cache, jf, indent=4, ensure_ascii=False)

    def _load_data(self, filename: str, ID: str) -> dict:
        r"""
        Load chatlog from the files.
        """

        with open(filename, "r", encoding="utf-8") as jf:
            contents = json.load(jf)

        # Probably these are unnessary:
        data = {
            "model": self.model,
            "messages": contents,
            # TODO: Qt中做成滑动条
            "top_p": 0.7,  # 用于控制生成文本的随机性，值越小，生成的文本越随机
            # TODO: Qt中做成滑动条
            "max_tokens": 4096,  # 用于控制生成文本的最大长度
        }
        #   ----------------------------------------------------------  #

        return data

    def _select_tts(
        self, model: str, filename: str, answer: str, lang: str = "en"
    ) -> None:
        r"""
        Select TTS engine
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

    def _execute(self, *, url: str, header: dict, data: dict, frcolor: str) -> str:
        r"""
        The inner logic for invoking Spark AI
        :param:
            url (str):
                The API link for Spark, However this is stored in config/settings.yml
            header (dict):
                The header for Spark API
            data (dict):
                The data for Spark API
            frcolor (str):
                The color for the response
        """
        with httpx.Client(timeout=60) as client:
            try:
                response = client.post(url, headers=header, json=data)
                if response.status_code == 200:
                    answer = json.loads(response.text)["choices"][0]["message"][
                        "content"
                    ]  # 获取回答 请自行查阅API文档
                    print(f"{set_frcolor(text=answer,color=frcolor)}")
                    return answer
                else:
                    logger.warning(
                        f"Failed to request, STATUS_CODE: {response.status_code}"
                    )

            except Exception as e:
                logger.error(e)

    def call(
        self,
        content: str,
        random_id: str,
        frcolor: str,
        count: int = 1,
    ) -> None:
        r"""
        The socket for invoking Spark AI
        [Doc](https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E)
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

        filename = f"./cache/chat{self.model}-{random_id}.json"
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as jf:
                json.dump([], jf)  # Initialize the chatlog

        try:
            header = {
                "Content-Type": "application/json",
                "Authorization": self.API_KEY,
            }

            self._write_cache(filename=filename, ID=random_id, content=content)
            data = self._load_data(filename=filename, ID=random_id)
            answer = self._execute(
                url=self.BASE_URL, header=header, data=data, frcolor=frcolor
            )
            self._write_cache(
                filename=filename, ID=random_id, content=answer, role="assistant"
            )

            if self.isTTS:
                self._select_tts(
                    model="coqui",
                    lang=self.LANG,
                    answer=answer,
                    filename=f"./audio/chat{self.model}/chat{self.model}-{count}-{random_id}.wav",
                )

        except Exception as e:
            raise e
