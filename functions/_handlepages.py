from ._pages import *
from utils import yaml
from ._chat import ChatWithAI
from utils.colorful import SetColor
from utils.settings import logger
from utils.settings import SetYaml
from ._status import PageStatusTransite


frcolor = SetColor.set_frcolor
page_status_transite = PageStatusTransite()


class ForPages:
    def for_self_part(self):
        raise NotImplementedError(
            # Avoiding not rewriting since each subclass needs to handle different conditions
            f"Subclass <{self.__class__.__name__}> must rewrite the method <for_self_part()>"
        )

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

        current_page_status = page_status_transite.transite_to(
            new_page_status, user_action
        )

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
            num, model = input(
                "Please enter your choice here(Use space to split 2 values): "
            ).split(" ")
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
                current_page="Chat",
                available_dict=Chat.chat_page_for_backward_func,
                choice=choice,
            )

        return current_page_status

    def _write_into_conf(self, **kwargs) -> None:
        r"""
        kwargs: Give Params with the formation:
        choice : str
        model : str
        """
        key = "using_chat_model"  # This is the key in configuration
        SetYaml.rewrite_yaml(key, kwargs)

    def _read_conf(self) -> dict:
        with open("./config/settings.yml") as f:
            conf = yaml.safe_load(f)

            return (
                conf["using_chat_model"][0]["choice"],
                conf["using_chat_model"][1]["model"],
            )


class ForSettingsPart(ForPages):
    def for_self_part(self, new_page_status: str = "settings_page_main"):
        r"""
        Return the current PageStatus [SETTINGS]
        :params:
        - new_page_status: (str) This is for the whole program can change to the proper pages the user needs
        """
        summary_orm = SettingsPart.Summary_ORM

        current_page_status = new_page_status
        page_detail, avaliable_dict = summary_orm.get(
            current_page_status,
            [
                SettingsPart.settings_page_main,
                {"B": ("settings_page_main", "Backward")},
            ],
        )

        if (
            current_page_status != "SettingsPart"
        ):  # FIXME: 晚点完成这里的设置TTS和Prompt等逻辑
            print(page_detail)
            choice = input(frcolor(text="\nPlease Enter the Key you want: "))

        else:
            print("Please enter the content you want to change", end=" ")
            content = input(frcolor(text="(Split by space!):\n", color="red")).split(
                " "
            )
            if self._check_if_need_rewrite(current_page_status):
                print(content)

                # self._rewrite_into_conf()
            print("Finished!")
            choice = "B"

        current_page_status = self.update_status(
            current_page=current_page_status,
            available_dict=avaliable_dict,
            choice=choice,
        )
        return current_page_status

    def _check_if_need_rewrite(self, current_page: str):
        r"""Check if the current page allow user to write into the yaml file"""
        if current_page == "SettingsPart":  # See _status.py, the class PageStatus
            return True

        return False

    def _rewrite_into_conf(self, **kwargs):
        r"""Write the params into the yaml file"""
        # SetYaml.rewrite_yaml(**kwargs)
        pass


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
                else:  # Since some setting pages haven't defined here, we just use this way to call ForSettingsPart
                    current_page_status = page_status_to_func_orm.get(
                        "settings_page_main"
                    )(
                        current_page_status
                    )  # Give the current_pages it is now, in order to let FSM check if can transite to other pages
            except KeyboardInterrupt:
                current_page_status = page_status_to_func_orm.get("Exit")()

            except Exception as e:
                raise e
