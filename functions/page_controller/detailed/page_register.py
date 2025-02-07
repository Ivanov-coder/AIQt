from functions.page_controller.detailed.status import PageStatusTransite


class PageRegister:
    page_status_transite = PageStatusTransite()  # Init the transite function for pages.

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

        current_page_status = self.page_status_transite.transite_to(
            new_page_status, user_action
        )

        return current_page_status
