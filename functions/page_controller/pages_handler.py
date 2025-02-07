from functions.page_controller.detailed.exit_handler import ExitHandler
from functions.page_controller.detailed.info_page_handler import InfoPageHandler
from functions.page_controller.detailed.main_page_handler import MainPageHandler
from functions.page_controller.detailed.settings_page_handler import SettingsPageHandler
from functions.page_controller.detailed.chat_page.chat_page_handler import ForChatPart
from timeit import default_timer


class PagesHandler:
    def start_handle(self) -> None:
        r"""
        Get the function of the particular page and execute it
        """
        current_page_status = "MainPart"  # Default PageStatus
        page_status_to_func_orm = {  # This is used to transfer the page status to the function, and then we can execute it successfully
            "MainPart": MainPageHandler().for_self_part,
            "Chat": ForChatPart().for_self_part,
            "settings_page_main": SettingsPageHandler().for_self_part,
            "InfoPart": InfoPageHandler().for_self_part,
            "Exit": ExitHandler().for_self_part,
        }
        while True:
            s = default_timer()
            try:
                if current_page_status in page_status_to_func_orm.keys():
                    current_page_status = page_status_to_func_orm.get(
                        current_page_status
                    )()
                else:  # Since We ONLY defined MAIN PAGE FOR SettingsPart here, we just use this way to call ForSettingsPart
                    current_page_status = page_status_to_func_orm.get(
                        "settings_page_main"
                    )(
                        current_page_status
                    )  # Give the current_pages it is now, in order to let FSM check if can transite to other pages
            except KeyboardInterrupt or EOFError:
                current_page_status = page_status_to_func_orm.get("Exit")()

            except Exception as e:
                raise e

            print(f"RUNNING TIME: {default_timer() - s}")