# 这个要求必要本地拥有ollama软件及大模型
# 已解决本地没有大模型报错的问题 但需要确保本地有ollama
# 不调用aiData.py文件
import utils
import ollama
import base64
import tts

# 读取人格设定
conf = utils.settings.SetYaml.read_yaml(filename="persona.yaml")
# 导入颜色模块
# color = utils.colorful.SetColor


@utils.dcl.dataclass
class CallOllamaAI:
    """
    这玩意需要你本地有ollama软件及其大模型。<br/>
    理论上而言只要[ollama开源模型](https://ollama.com/library)有的，它都支持。<br/>
    ### 在使用之前确保在命令行执行如下命令：
    >>> ollama pull <the_model_you_want>

    做成Qt之后想办法让这个命令自己执行(可能又要写.bat脚本了)
    """

    # 默认是llama3.1
    # 想要用图片的话请下载llama3.2-vision
    # 但是这个版本比较卡，不建议
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
        """
        写入缓存到.cache/chat.json文件中
        """

        # 出于性能方面的考虑 暂时决定不添加多模态功能
        if image and self.model == "llama3.2-vision":
            # 确保必须是列表
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

        # 由于json_repair库的问题 我们这里只能直接指定编码格式为gbk
        # Windows系统默认编码是gbk，这个库跟了它
        with open(f"./cache/chatOllama-{ID}.json", "a+", encoding="gbk") as jf:
            # 读取文件内容
            cache = utils.json_repair.from_file(f"./cache/chatOllama-{ID}.json")
            # 判断是否为列表
            if not isinstance(cache, list):
                # 否 确认是否为空字符串
                if cache == "":
                    if isRolePlay:
                        log = [log]
                        log.insert(0, {"role": "system", "content": conf["PERSONA"]})
                    # 是 则直接令cache为log
                    cache = log

            else:
                cache.append(log)

        # 由于json_repair库的问题 我们这里只能直接指定编码格式为gbk 重写一遍
        with open(f"./cache/chatOllama-{ID}.json", "w", encoding="gbk") as jf:
            # 把wrapper写进去
            utils.json.dump(cache, jf, indent=4, ensure_ascii=False)

    # TODO: 上传图片的计划只能先搁置了
    def _load_data(self, ID: str) -> dict:
        """
        加载文字或图片。
        """
        contents = utils.json_repair.from_file(f"./cache/chatOllama-{ID}.json")

        return contents

    def _select_tts(self, *items: tuple[str]) -> None:
        """
        选择TTS引擎，默认是coquiTTS
        """
        # TODO: 做出来给人选
        # TODO: 配置一下如何搞定路径和语速
        match items:
            case ["coqui", str(content), str(path)]:
                tts.coquiTTS(text=content, output_path=path).get()
            case ["pytts", str(content), str(path)]:
                tts.pyTTS(text=content, output_path=path).get()
            case _:
                raise ValueError("Please Check your parameters!")

    async def _execute(self, data: list[dict]) -> str:
        """
        内部逻辑
        """

        try:
            output = ""
            async for part in await ollama.AsyncClient().chat(
                model=self.model, messages=data, stream=True
            ):

                print(part["message"]["content"], end="", flush=True)
                output += part["message"]["content"]

            print()  # 最后打印空行
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

    async def callByOllama(self, random_id: str) -> None:
        """
        调用ollama软件进行对话
        :param random_id: 随机生成的id.
        主要用途是用于对每个用户生成独一无二的id，以便在缓存中区分不同用户的对话记录。
        """
        utils.settings.logger.info(f"Invoking {self.model.upper()} API...")

        # TODO: DEBUG 有时能看到图片有时不能 并且不支持图片之后只有文字输入
        try:
            if self.model == "llama3.2-vision":
                # TODO: 需要把这个做出来到Qt中，成为输入框
                meta_input = input("请输入您的问题和需要附带的图片路径，以->分割：")
                if meta_input.find("->") != -1:
                    content, IMG_PATH = meta_input.split("->")
                else:
                    content = meta_input
                image = base64.b64encode(open(IMG_PATH, "rb").read()).decode()
                self._write_cache(content=content, image=image)

            else:
                # TODO: 需要把这个做出来到Qt中，成为输入框
                content = input("请输入您的问题：")
                self._write_cache(ID=random_id, content=content, isRolePlay=True)

        except Exception:  # 由于Python多协程的特性，ctrl+c就直接不打印日志了
            return  # 直接终止程序

        try:
            data = self._load_data(ID=random_id)
            answer = await self._execute(data=data)
            self._write_cache(
                ID=random_id, content=answer, role="assistant", isRolePlay=True
            )
            # TODO: 需要做出来给人选择用什么TTS
            # TODO: 发现个问题，生成语音的速度太慢了，思考下怎么优化
            self._select_tts("coqui", answer, f"./audio/chatOllama-{random_id}.wav")

        except Exception as e:
            raise e
