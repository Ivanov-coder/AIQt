from utils import set_frcolor
from functions.page_controller.pages import SettingsPart
from functions.page_controller.detailed.page_register import PageRegister
from app.properties.detailed.other_property_handler import GetOtherProperties
from app.properties.detailed.spark_property_handler import GetSparkProperties
from app.properties.detailed.ollama_property_handler import GetOllamaProperties


class SettingsPageHandler(PageRegister):
    def for_self_part(self, new_page_status: str = "settings_page_main"):
        r"""
        Return the current PageStatus [SETTINGS]
        :params:
        - new_page_status: (str) This is for the whole program
            can change to the proper pages the user needs,
            default to be settings_page_main
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

        if current_page_status != "SettingsPart":
            print(page_detail)
            choice = input(set_frcolor(text="\nPlease Enter the Key you want: "))

        else:  # TODO: 晚点完成这里的设置TTS和Prompt等逻辑
            print("Please enter the content you want to change", end=" ")
            content_input = input(
                set_frcolor(
                    text="Please enter the content you want to change (Split by space!):\n",
                    color="red",
                )
            )
            if content_input.strip():  # Check if input is not empty
                content = content_input.split(" ")

            print("Finished!")
            choice = "B"

        current_page_status = self.update_status(
            current_page=current_page_status,
            available_dict=avaliable_dict,
            choice=choice,
        )
        return current_page_status

