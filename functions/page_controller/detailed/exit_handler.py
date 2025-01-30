from functions.page_controller.detailed.page_register import PageRegister


class ExitHandler(PageRegister):
    def for_self_part(self):
        r"""Since exited, we don't need PageStatus here"""
        # logger.info("Off the program")
        exit()
