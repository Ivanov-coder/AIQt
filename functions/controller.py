from functions.page_controller.pages_handler import PagesHandler


class CtrlBoard:
    r"""
    Use the board to control the behavior of our user
    """

    def run(self):
        try:
            PagesHandler().start_handle()
        except KeyboardInterrupt:
            exit()
