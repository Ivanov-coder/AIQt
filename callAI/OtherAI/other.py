import httpx
import utils
from langchain_community.llms import openai
import lib.data.aiData as AI  # 此导包方式只支持在main.py中运行


@utils.dcl.dataclass
class CallOherAI:
    """
    用于调用其他AI.
    使用时
    """
    model: str = "gpt-3.5-turbo"  # 如果有需要 请自行修改参数 默认为gpt-3.5-turbo

    def _get_logger(self) -> tuple[str, str, utils.logs.Logger]:
        """
        用于获取BASE_URL, API_KEY, logger
        """

        BASE_URL, API_KEY = AI.start("2", self.model)
        logger = utils.logs.Logger.setup_logger(fileposition=__name__)
        return BASE_URL, API_KEY, logger

    # TODO: 上传图片的计划只能先搁置了
    def _select_data(self, *, content: str, picture: bytes = None) -> dict:
        """
        选择数据 上传文字或图片。
        图片请传入二进制数据。
        ## 小尴尬 LLM不支持图片输入:/
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
                        "content": str(picture),
                        "content_type": "image",
                    },
                    {
                        "role": "user",
                        "content": content,
                        "content_type": "text",
                    },
                ],
            }

    async def callByLangchain(self) -> None:
        """
        用于调用AI。
        你需要输入你想提问的问题。
        """

        # 一些基础设定和日志 确保只有执行callByhttpx函数时才被执行 而不是导包后就被执行
        BASE_URL, API_KEY, logger = self._get_logger()

        # TODO: 需要把这个做出来到Qt中，成为输入框
        content = input("请输入您的问题：")

        response = openai(self.model, content)
        print(f'{self.model.upper()} : {response}')

    async def callByhttpx(self) -> None:
        """
        用于调用AI。
        你需要输入你想提问的问题。
        """

        # 一些基础设定和日志 确保只有执行callByhttpx函数时才被执行 而不是导包后就被执行
        BASE_URL, API_KEY, logger = self._get_logger()

        try:
            # TODO: 需要把这个做出来到Qt中，成为输入框
            content = input("请输入您的问题：")
        except Exception:  # 由于Python多协程的特性，ctrl+c就直接不打印日志了
            return  # 直接终止程序

        headers = {
            "Authorization": API_KEY,
            "Content-Type": "application/json",
        }

        data = self._select_data(content=content
                                 #  ,picture=open("pig.jpg","rb").read()
                                 )
        async with httpx.AsyncClient(
                timeout=60) as aclient:  # 使用Client建立Sessiom 避免多次请求服务器
            response = await aclient.post(BASE_URL, headers=headers, json=data)
            try:
                answer = utils.json_repair.loads(
                    response.text)["choices"][0]["message"][
                        "content"]  # 获取回答 不知数据结构以后是否变动
                print(f'{self.model.upper()} : {answer}')
            except:
                logger.error("获取回答失败，请检查json结构是否变动")
