import httpx
import utils
import base64  # 将图片二进制流编码成base64格式并上传
import lib.data.aiData as AI


# TODO: 目前只支持单轮对话，需要调试
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

    def _select_data(self, *, content: str, picture: bytes = None) -> dict:
        """
        选择数据 上传文字或图片。
        图片请传入二进制数据
        """
        if not picture:
            return {
                "model":
                self.model,  # 指定请求的模型
                "messages": [
                    {
                        "role": "user",
                        "content": content,
                        "content_type": "text",
                    },
                ],
            }
        else:
            return {
                "model":
                self.model,  # 指定请求的模型
                "messages": [
                    {
                        "role": "user",
                        "content": str(base64.b64decode(picture)),
                        "content_type": "image",
                    },
                    {
                        "role": "user",
                        "content": content,
                        "content_type": "text",
                    },
                ],
            }

    def callByhttpx(self) -> None:
        """
        调用Spark AI.
        [官方文档](https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E)
        """

        # 日志 确保只有执行callSparkAI函数时才被执行 而不是导包后就被执行
        logger = utils.logs.Logger.setup_logger(fileposition=__name__)

        # TODO: 需要把这个做出来到Qt中，成为滚动条去选择
        BASE_URL, API_KEY = AI.start("1", self.model)
        # 这里只支持调用Spark AI 请不要在这里调用其他AI

        # TODO: 需要把这个做出来到Qt中，成为输入框
        content = input("请输入您的问题：")

        data = self._select_data(content=content,
                                #  picture=open("pig.jpg", "rb").read()
                                )
        header = {
            "Content-Type": "application/json",
            "Authorization": API_KEY,
        }
        # 测试能否上传图片   TODO : 目前不能 继续debug

        with httpx.Client(timeout=60) as client:  # 使用Client建立Sessiom 避免多次请求服务器
            try:
                response = client.post(BASE_URL, headers=header,
                                       json=data)  # POST对BASE_URL发送请求
                if response.status_code == 200:
                    answer = response.json()["choices"][0]["message"][
                        "content"]  # 获取回答 请自行查阅API文档
                    print(answer)
                else:
                    logger.warning(
                        f"Failed to request, STATUS_CODE: {response.status_code}"
                    )

            except Exception as e:
                logger.error(e)
