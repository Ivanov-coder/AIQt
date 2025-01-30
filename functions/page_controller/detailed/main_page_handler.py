from utils import set_frcolor
from functions.page_controller.pages import MainPart
from functions.page_controller.detailed.page_register import PageRegister


class MainPageHandler(PageRegister):
    def for_self_part(self):
        r"""Return the current PageStatus [MAINPART]"""
        print(MainPart.main_page)
        choice = input(set_frcolor(text="\nPlease Enter the Key you want: "))
        current_page_status = self.update_status(
            current_page="MainPart",
            available_dict=MainPart.main_page_avaliable_func,
            choice=choice,
        )
        return current_page_status
