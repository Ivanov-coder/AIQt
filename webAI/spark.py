import httpx
import utils
import data.aiData as AI


@utils.dcl.dataclass
class CallSparkAI:
    """
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

    model: str = utils.dcl.field(default="lite")  # 如果有需要 请自行修改参数 默认为lite

    # XXX: 讯飞星火lite不支持角色扮演
    def _write_cache(self, ID: str, content: str, role: str = "user") -> None:
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
                cache = [log]
            else:
                cache.append(log)

        with open(f"./cache/chat{self.model}-{ID}.json", "w", encoding="utf-8") as jf:
            utils.json.dump(cache, jf, indent=4, ensure_ascii=False)

    def _load_data(self, ID: str) -> dict:
        """
        加载文字或图片。
        图片请传入二进制数据
        ## 小尴尬 LLM不支持图片输入:/
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

    # 调用的内部逻辑
    async def _execute(self, *, url: str, header: dict, data: dict) -> str:
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
                    print(f"{self.model.upper()}: {answer}")
                    return answer
                else:
                    utils.settings.logger.warning(
                        f"Failed to request, STATUS_CODE: {response.status_code}"
                    )

            except Exception as e:
                utils.settings.logger.error(e)

    async def callByhttpx(self, content: str, random_id: str) -> None:
        """
        调用Spark AI
        [官方文档](https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E)
        """
        root = f"chat{self.model}-{random_id}"  # 删除的聊天记录的根命名

        try:
            # TODO: 需要把这个做出来到Qt中，成为滚动条去选择
            BASE_URL, API_KEY = AI.start("1", self.model)

            # TODO: 需要把这个做出来到Qt中，成为输入框
        except Exception:  # 由于Python多协程的特性，ctrl+c就直接不打印日志了
            return

        try:
            header = {
                "Content-Type": "application/json",
                "Authorization": API_KEY,
            }

            self._write_cache(ID=random_id, content=content)
            data = self._load_data(ID=random_id)
            answer = await self._execute(url=BASE_URL, header=header, data=data)
            self._write_cache(ID=random_id, content=answer, role="assistant")

        except Exception as e:
            raise e
