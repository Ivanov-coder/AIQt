# 这个要求必要本地拥有ollama软件及大模型
# 不调用aiData.py文件
import utils
import ollama

# 读取人格设定
conf = utils.settings.SetYaml.read_yaml()
# 导入颜色模块
color = utils.colorful.SetColor


@utils.dcl.dataclass
class CallOllamaAI:
    """
    这玩意需要你本地有ollama软件及其大模型。<br/>
    理论上而言只要[ollama开源模型](https://ollama.com/library)有的，它都支持。<br/>
    ### 在使用之前确保在命令行执行如下命令：
    >>> ollama pull <the_model_you_want>

    做成Qt之后想办法让这个命令自己执行(可能又要写.bat脚本了)
    """

    # 默认是llama3.1:latest(主要是自己在用)
    model: str = utils.dcl.field(default="llama3.1")

    def _write_cache(self, content: str, role: str = "user") -> None:
        """
        写入缓存到.cache/chat.json文件中
        """

        log = {
            "role": role,
            "content": content,
        }

        # 由于json_repair库的问题 我们这里只能直接指定编码格式为gbk
        with open("./cache/chatOllama.json", "a+", encoding="gbk") as jf:
            wrapper = []  # 包装器 确保传入参数是列表
            # 读取文件内容
            cache = utils.json_repair.from_file("./cache/chatOllama.json")
            # 判断是否为列表
            if not isinstance(cache, list):
                # 否 确认是否为空字符串
                if cache == "":
                    # 是 则直接令cache为log
                    cache = log
                # 包进列表里面
                wrapper.append(cache)

            else:
                # 是 则让wrapper = cache
                wrapper = cache
                # 将log添加到wrapper中
                wrapper.append(log)

        # 由于json_repair库的问题 我们这里只能直接指定编码格式为gbk 重写一遍
        with open("./cache/chatOllama.json", "w", encoding="gbk") as jf:
            # 把wrapper写进去
            utils.json.dump(wrapper, jf, indent=4, ensure_ascii=False)

    # TODO: 上传图片的计划只能先搁置了
    def _load_data(self) -> dict:
        """
        加载文字或图片。
        图片请传入二进制数据
        ## 小尴尬 LLM不支持图片输入:/
        """
        contents = utils.json_repair.from_file("./cache/chatOllama.json")

        return contents

    async def _execute(self, data: dict) -> str:
        if not isinstance(data, list):
            data = [data]

        output = ""
        async for part in await ollama.AsyncClient().chat(model=self.model,
                                                 messages=data,
                                                stream=True):
            
            print(part["message"]["content"], end='', flush=True)
            output += part["message"]["content"]

        return output

    async def callByOllama(self) -> None:
        """
        调用ollama软件进行对话
        """
        utils.settings.logger.info(f"Invoking {self.model.upper()} API...")
        try:
            # TODO: 需要把这个做出来到Qt中，成为输入框
            content = input("请输入您的问题：")

        except Exception:  # 由于Python多协程的特性，ctrl+c就直接不打印日志了
            return  # 直接终止程序

        try:
            self._write_cache(content=content)
            data = self._load_data()
            answer = await self._execute(data=data)
            # print(answer, end='', flush=True)
            # self._write_cache(content=answer, role="assistant")

        except Exception as e:
            raise e
        