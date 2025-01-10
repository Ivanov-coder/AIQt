from ._pages import *
from utils import json
from ._chat import ChatWithAI
from abc import ABC, abstractmethod
from utils.colorful import SetColor
from utils.settings import logger
from ._status import PageStatusTransite


frcolor = SetColor.set_frcolor
page_status_transite = PageStatusTransite()


class ForPages(ABC):
    @abstractmethod
    def for_self_part(self):
        pass

    def update_status(
        self, *, available_dict: dict, choice: str, current_page: str
    ) -> str:
        r"""
        :params:
        - available_dict: (dict)
                                        The dictionary that contains the available page status and user action
        - choice: (str)
                                        The choice of the user
        - current_page: (str)
                                        The current page status
        :return:
        - current_page_status: (str)
        """
        new_page_status, user_action = available_dict.get(
            choice, [current_page, "Maintain"]
        )
        # if new_page_status != "settings_page_main":
        current_page_status = page_status_transite.transite_to(
            new_page_status, user_action
        )

        # current_page_status = settings_page_status_transite.transite_to(
        # 		new_page_status, user_action
        # 	)

        return current_page_status


class ForMainPart(ForPages):
    def for_self_part(self):
        r"""Return the current PageStatus [MAINPART]"""
        print(MainPart.main_page)
        choice = input(frcolor(text="\nPlease Enter the Key you want: "))
        current_page_status = self.update_status(
            current_page="MainPart",
            available_dict=MainPart.main_page_avaliable_func,
            choice=choice,
        )
        return current_page_status


class ForChatPart(ForPages):
    def for_self_part(self):
        r"""Return the current PageStatus [CHAT]"""
        try:
            num, model = self._read_conf()
        except:
            print(Chat.chat_page_for_the_first_time)
            num, model = input("Please enter your choice here: ").split(" ")
            self._write_into_conf(choice=num, model=model)

        try:
            ChatWithAI(num, model).chat()
            current_page_status = self.update_status(
                current_page="Chat",
                available_dict=Chat.chat_page_avaliable_func,
                choice=choice,
            )

        except KeyboardInterrupt:
            choice = "B"
            current_page_status = self.update_status(
                current_page="MainPart",
                available_dict=Chat.chat_page_for_backward_func,
                choice=choice,
            )

        return current_page_status

    def _write_into_conf(self, **kwargs) -> None:
        r"""
        kwargs: Give Params with the formation:
                        choice = str
                        model = str
        """
        # TODO: 第一次使用时将选择和大模型写入文件 之后再通过设置界面更改
        # TODO: 需要对三个方式都保存调用哪个模型
        with open("./config/conf.json", "w") as f:
            json.dump(kwargs, f)

    def _read_conf(self) -> dict:
        # 读取配置文件
        with open("./config/conf.json", "r") as f:
            data = json.load(f)
            return data["choice"], data["model"]


class ForSettingsPart(ForPages):
    def for_self_part(self, new_page_status: str = "settings_page_main"):
        # TODO: 目前的方案是新增加一个枚举和状态机来专门负责SettingsPart
        # 这样子的话可能就要改一下传入的transite函数了
        r"""Return the current PageStatus [SETTINGS]"""
        summary_orm = SettingsPart.Summary_ORM
        settings_pages_names = list(summary_orm.keys())

        current_page_status = new_page_status
        if current_page_status not in settings_pages_names:
            raise ValueError("Invalid option")

        page_detail, avaliable_dict = summary_orm.get(current_page_status, [])

        print(page_detail)
        choice = input(frcolor(text="\nPlease Enter the Key you want: "))

        current_page_status = self.update_status(
            current_page=current_page_status,
            available_dict=avaliable_dict,  # TODO: Here we need to check which page is in
            choice=choice,
        )
        return current_page_status


class ForInfoPart(ForPages):
    def for_self_part(self):
        r"""Return the current PageStatus [INFOPART]"""

        print(InfoPart.select_page)
        choice = input(frcolor(text="\nPlease Enter the Key you want: "))

        print(InfoPart.about_page)
        current_page_status = self.update_status(
            current_page="InfoPart",
            available_dict=InfoPart.info_page_available_func,
            choice=choice,
        )

        return current_page_status


class ForExit(ForPages):
    def for_self_part(self):
        r"""Since exited, we don't need PageStatus here"""
        logger.info("Off the program")
        exit()


class HandlePages:

    def start_handle(self) -> None:
        r"""
        Get the function of the particular page and execute it
        """
        current_page_status = "MainPart"  # Default PageStatus
        page_status_to_func_orm = {  # This is used to transfer the page status to the function, and then we can execute it successfully
            "MainPart": ForMainPart().for_self_part,
            "Chat": ForChatPart().for_self_part,
            "settings_page_main": ForSettingsPart().for_self_part,
            "InfoPart": ForInfoPart().for_self_part,
            "Exit": ForExit().for_self_part,
        }
        while True:
            try:
                if current_page_status in page_status_to_func_orm.keys():
                    current_page_status = page_status_to_func_orm.get(
                        current_page_status
                    )()
                else:
                    current_page_status = page_status_to_func_orm.get(
                        "settings_page_main"
                    )(current_page_status)
            except Exception as e:
                raise e
