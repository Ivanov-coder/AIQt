import httpx
import utils
import data.aiData as AI


class CallSparkAI:
    r"""
    SparkAI类.
    通过实例化时传入参数来改变model。
    例如
    >>> spark = CallSparkAI(model="lite") # 调用lite模型
    支持调用的模型如下:
    - lite
    - generalv3
    - pro-128k
    - generalv3.5
    - max-32k
    - 4.0Ultra
    """

    def __init__(self, model: str = "lite"):
        self.model: str = model  # 如果有需要 请自行修改参数 默认为lite

    # XXX: 讯飞星火lite不支持角色扮演
    def _write_cache(
        self,
        filename: str,
        ID: str,
        content: str,
        role: str = "user",
        isRolePlay: bool = False,
    ) -> None:
        """
        写入缓存到.cache/chat.json文件中
        """

        cache = self._load_data(filename, ID)["messages"]  # Append into the message.
        log = {  # Ensure that log is list
            "role": role,
            "content": content,
            "content_type": "text",
        }
        cache.append(log)
        with open(filename, "w", encoding="utf-8") as jf:
            utils.json.dump(cache, jf, indent=4, ensure_ascii=False)

    def _load_data(self, filename: str, ID: str) -> dict:
        """
        加载文字或图片。
        图片请传入二进制数据
        ## 小尴尬 LLM不支持图片输入:/
        """

        with open(filename, "r", encoding="utf-8") as jf:
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

    # 调用的内部逻辑
    async def _execute(self, *, url: str, header: dict, data: dict) -> str:
        r"""
        调用Spark AI.

        """
        async with httpx.AsyncClient(timeout=60) as aclient:
            try:
                response = await aclient.post(url, headers=header, json=data)
                if response.status_code == 200:
                    answer = utils.json.loads(response.text)["choices"][0]["message"][
                        "content"
                    ]  # 获取回答 请自行查阅API文档
                    print(f"{self.model.upper()}: {answer}")
                    return answer
                else:
                    utils.settings.logger.warning(
                        f"Failed to request, STATUS_CODE: {response.status_code}"
                    )

            except Exception as e:
                utils.settings.logger.error(e)

    async def callByhttpx(self, content: str, random_id: str) -> None:
        r"""
        调用Spark AI
        [官方文档](https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E)
        """
        BASE_URL, API_KEY = AI.start("1", self.model)

        filename = f"./cache/chat{self.model}-{random_id}.json"
        if not utils.os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as jf:
                utils.json.dump([], jf)  # Initialize the chatlog

        try:
            header = {
                "Content-Type": "application/json",
                "Authorization": API_KEY,
            }

            self._write_cache(filename=filename, ID=random_id, content=content)
            data = self._load_data(filename=filename, ID=random_id)
            answer = await self._execute(url=BASE_URL, header=header, data=data)
            self._write_cache(
                filename=filename, ID=random_id, content=answer, role="assistant"
            )

        except Exception as e:
            raise e
