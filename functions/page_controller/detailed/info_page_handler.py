from utils import set_frcolor
from functions.page_controller.pages import InfoPart
from functions.page_controller.detailed.page_register import PageRegister


class InfoPageHandler(PageRegister):
    def for_self_part(self):
        r"""Return the current PageStatus [INFOPART]"""

        print(InfoPart.select_page)
        choice = input(set_frcolor(text="\nPlease Enter the Key you want: "))

        print(InfoPart.about_page)
        current_page_status = self.update_status(
            current_page="InfoPart",
            available_dict=InfoPart.info_page_available_func,
            choice=choice,
        )

        return current_page_status
