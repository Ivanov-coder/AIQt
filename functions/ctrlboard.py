from ._pages import *
from ._chat import ChatWithAI
from utils import json
from utils import typing
from utils.settings import logger
from utils.colorful import SetColor
from ._status import PageStatusTransite


frcolor = SetColor.set_frcolor
page_status_transite = PageStatusTransite()


class CtrlBoard:
    r"""
    Use the board to control the behavior of our user
    """

    def run(self):
        try:
            if (
                not input(
                    frcolor(text="\nPress Any Key here")
                    + frcolor(text="(E to exit): ", color="red")
                ).upper()
                == "E"
            ):
                self._choose()
            else:
                logger.info("Off the program")
                exit()

        except KeyboardInterrupt:
            logger.info("Off the program")
            exit()

        # except Exception as e:
        #     logger.error(e)
        #     logger.info("Restarted")
        #     self.run()

    def _update_status(
        self, *, available_dict: dict, choice: str, next_page: str
    ) -> str:
        new_page_status, user_action = available_dict.get(
            choice, [next_page, "Maintain"]
        )

        current_page_status = page_status_transite.transite_to(
            new_page_status, user_action
        )

        return current_page_status

    def _choose(self):
        current_page_status = "MainPart"  # Default PageStatus
        page_status_to_func_orm = {  # This is used to transfer the page status to the function, and then we can execute it successfully
            "MainPart": self._for_main_part,
            "Chat": self._for_chat,
            "SettingsPart": self._for_settings_part,
            "InfoPart": self._for_info_part,
            "Exit": self._for_exit,
        }
        while True:
            try:
                current_page_status = page_status_to_func_orm.get(current_page_status)()
            except Exception as e:
                raise e

    def _for_main_part(self) -> str:
        r"""Return the current PageStatus [MAINPART]"""
        print(MainPart.main_page)
        choice = input(frcolor(text="\nPlease Enter the Key you want: "))
        current_page_status = self._update_status(
            next_page="MainPart",
            available_dict=MainPart.main_page_avaliable_func,
            choice=choice,
        )
        return current_page_status

    def _for_chat(self) -> str:
        r"""Return the current PageStatus [CHAT]"""
        try:
            num, model = self._read_conf()
        except:
            print(Chat.chat_page_for_the_first_time)
            num, model = input("Please enter your choice here: ").split(" ")
            self._write_into_conf(choice=num, model=model)

        try:
            ChatWithAI(num, model).chat()
            current_page_status = self._update_status(
                next_page="Chat",
                available_dict=Chat.chat_page_avaliable_func,
                choice=choice,
            )

        except KeyboardInterrupt:

            print(Chat.chat_page_for_backward)
            choice = input(frcolor(text="\nPlease enter the key you want: "))
            current_page_status = self._update_status(
                next_page="MainPart",
                available_dict=Chat.chat_page_for_backward_func,
                choice=choice,
            )

        return current_page_status

    def _for_settings_part(self) -> str:
        r"""Return the current PageStatus [SETTINGSPART]"""
        pass

    def _for_info_part(self) -> str:
        r"""Return the current PageStatus [INFOPART]"""
        pass

    def _for_exit(self) -> None:
        r"""Since exited, we don't need PageStatus here"""
        logger.info("Off the program")
        exit()

    @staticmethod
    def _write_into_conf(**kwargs) -> None:
        r"""
        kwargs: Give Params with the formation:
            choice = str
            model = str
        """
        # TODO: 第一次使用时将选择和大模型写入文件 之后再通过设置界面更改
        # TODO: 需要对三个方式都保存调用哪个模型
        with open("./config/conf.json", "w") as f:
            json.dump(kwargs, f)

    @staticmethod
    def _read_conf() -> dict:
        # 读取配置文件
        with open("./config/conf.json", "r") as f:
            data = json.load(f)
            return data["choice"], data["model"]
