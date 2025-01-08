from ._handlepages import HandlePages
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
                HandlePages().start_handle()
            else:
                logger.info("Off the program")
                exit()

        except KeyboardInterrupt:
            logger.info("Off the program")
            exit()
