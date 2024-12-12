import httpx
import utils
import data.aiData as AI

# 读取人格设定
conf = utils.settings.SetYaml.read_yaml("otherpersona.yaml")


@utils.dcl.dataclass
class CallOtherAI:
    """
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
                            "content": conf["PERSONA"],
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

    def _get_logger(
        self,
    ) -> tuple[str, str, utils.logs.Logger] | utils.logs.Logger:
        """
        用于获取BASE_URL, API_KEY, logger。
        """
        BASE_URL, API_KEY = AI.start("2", self.model)

        return BASE_URL, API_KEY

    # TODO: 上传图片的计划只能先搁置了

    # 调用的内部逻辑
    async def _execute(self, *, url: str, header: dict, data: dict) -> str:
        """
        调用Spark AI.

        """

        # 日志 确保只有执行函数时才被执行 而不是导包后就被执行
        async with httpx.AsyncClient(
            timeout=60
        ) as aclient:  # 使用AsyncClient建立Sessiom 避免多次请求服务器
            try:
                response = await aclient.post(
                    url, headers=header, json=data
                )  # POST对BASE_URL发送请求
                if response.status_code == 200:
                    answer = utils.json_repair.loads(response.text)["choices"][0][
                        "message"
                    ][
                        "content"
                    ]  # 获取回答 请自行查阅API文档
                    print(f"{self.model}-> {answer}")
                    return answer
                else:
                    utils.settings.logger.warning(
                        f"Failed to request, STATUS_CODE: {response.status_code}"
                    )

            except Exception as e:
                utils.settings.logger.error(e)

    async def callByhttpx(self, random_id: str) -> None:
        """
        调用Spark AI
        [官方文档](https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E)
        """

        try:
            # TODO: 需要把这个做出来到Qt中，成为滚动条去选择
            BASE_URL, API_KEY = AI.start("2", self.model)
            # 这里只支持调用Spark AI 请不要在这里调用其他AI

            # TODO: 需要把这个做出来到Qt中，成为输入框
            content = input("请输入您的问题：")
        except Exception:  # 由于Python多协程的特性，ctrl+c就直接不打印日志了
            return  # 直接终止程序

        try:
            header = {
                "Content-Type": "application/json",
                "Authorization": API_KEY,
            }

            self._write_cache(ID=random_id, content=content, isRolePlay=True)
            data = self._load_data(ID=random_id)
            answer = await self._execute(url=BASE_URL, header=header, data=data)
            self._write_cache(
                ID=random_id, content=answer, role="assistant", isRolePlay=True
            )

        except Exception as e:
            raise e
