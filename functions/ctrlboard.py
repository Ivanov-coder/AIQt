from ._pages import *
from utils import os
from utils import asyncio
from utils import json
from utils import GenerateID
from utils import setup_ollama
from utils.settings import logger
from utils.colorful import SetColor
from ._status import PageStatusTransite, UserAction


frcolor = SetColor.set_frcolor
page_status_transite = PageStatusTransite()


class CtrlBoard:

    r"""
    Use the board to control the behavior of our user
    """

    @classmethod
    def run(cls):
        # cls._start()
        cls._choose()

    def _update_status(self, available_func:dict, choice:str, default_page:str) -> str:
        new_page_status, user_action = available_func.get(
                choice, ["MainPart", "Maintain"]
            )
        current_page_status = page_status_transite.transite_to(new_page_status, user_action)

        return current_page_status

    def _write_into_conf(self, **kwargs) -> None:
        # 第一次使用时将选择和大模型写入文件 之后再通过设置界面更改
        with open("./config/conf.json", "w") as f:
            json.dump(kwargs, f)

    
    def _read_conf(self) -> dict:
        # 读取配置文件
        with open("./config/conf.json", "r") as f:
            data = json.load(f)

    def _choose(self):
        if (
            not input(
                frcolor(text="\nPress Any Key here")
                + frcolor(text="(E to exit): ", color="red")
            ).upper()
            == "E"
        ):
            print(MainPart.main_page)
            choice = input(frcolor(text="\nPlease enter the key you want: "))
            new_page_status, user_action = MainPart.main_page_avaliable_func.get(
                choice, ["MainPart", "Maintain"]
            )
            current_page_status = page_status_transite.transite_to(new_page_status, user_action)

            if current_page_status == "Chat":
                try:
                    num, model = self._read_conf()

                except:
                    print(MainPart.chat_page_for_the_first_time)
                    num, model = input("Please enter your choice here: ")
                    self._write_into_conf(choice=num, model=model)

                finally:
                    Chat(num, model).chat()
                    
            # if choice == "1":
            #     Chat(choice="ollama", model="llama3.1").chat()

            # elif choice.upper() == "E":
            #     exit()

        else:
            exit()


class Chat:
    randID = GenerateID.get_id()

    # 当生成wav时记录音频编号
    count_other_wav = 0
    count_ollama_wav = 0

    def __init__(self, choice: str = "1", model: str = "llama3.1"):
        r"""
        :param: choice: str -> Select the APP you want to use
        :param: model: str -> Select the model you want to use
        """
        self.choice = choice
        self.model = model

    def _switch(self, content: str):
        r"""
        做选择用的，后面估计得做到Qt选择框里面。
        """
        if self.choice == "1":
            import localAI

            setup_ollama()

            self.count_ollama_wav += 1

            # TODO: 这里的实例化需要做成选择框给用户选择模型
            return localAI.ollamallm.CallOllamaAI(model="llama3.1").callByOllama(
                content=content,
                random_id=self.randID,
                isTTS=True,
                count=self.count_ollama_wav,
                frcolor="lightblue",  # TODO: isTTS frcolor做出来
            )
        # TODO: 这里的实例化需要做成选择框给用户选择模型

        elif self.choice == "2":
            from webAI import spark

            return spark.CallSparkAI(model="lite").callByhttpx(
                content=content, random_id=self.randID
            )

        elif self.choice == "3":
            from webAI import other

            self.count_other_wav += 1

            return other.CallOtherAI(model="qwen-long").callByhttpx(
                content=content,
                random_id=self.randID,
                isTTS=True,
                count=self.count_other_wav,
                frcolor="lightblue",  # TODO: isTTS frcolor做出来
            )

        

    async def _call(self):
        content = input(
            frcolor(text="\nPlease enter you questions: ") + "_____\b\b\b\b\b"
        )
        await self._switch(content)

    async def _main(self):
        try:
            await self._call()
        except EOFError:
            print(frcolor(text="Hey! Please Enter Something!\n", color="red"))
            await self._call()

    def chat(self):
        r"""
        Begin chatting
        """
        while True:
            try:
                asyncio.run(self._main())
            except KeyboardInterrupt:
                CtrlBoard.run()

            # XXX: 这是本地情况
            except ModuleNotFoundError as e:
                logger.warning(e)
                logger.info("Installing requirements...")
                stdstatus = os.system("pip install -r requirements.txt")

                if stdstatus == 0:
                    logger.info("Requirements installed successfully.")
                else:
                    logger.error("Failed to install requirements.")
                    break
            # PS 如果出了什么bug需要调试，请直接注释掉下面那一段
            # except Exception as e:
            #     logger.error(e)
            #     logger.info("Restarted")
