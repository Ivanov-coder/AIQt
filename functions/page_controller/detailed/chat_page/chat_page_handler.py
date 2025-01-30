from functions.page_controller.pages import Chat
from functions.page_controller.detailed.chat_page.chat import ChatWithAI
from functions.page_controller.detailed.page_register import PageRegister


class ForChatPart(PageRegister):
    def for_self_part(self):
        r"""Return the current PageStatus [CHAT]"""
        # num, model = self._get_num_and_model()
        # TODO: Now testing all functions, when debug end, use the above code.
        num, model = "1", "llama3.1"

        try:
            ChatWithAI(num, model).chat()
            current_page_status = self.update_status(
                current_page="Chat",
                available_dict=Chat.chat_page_avaliable_func,
                choice=num,
            )

        except KeyboardInterrupt:
            choice = "B"
            current_page_status = self.update_status(
                current_page="Chat",
                available_dict=Chat.chat_page_avaliable_func,
                choice=choice,
            )

        return current_page_status

    def _get_num_and_model(self):
        r"""Get the choice and model, if not, write into conf."""
        try:
            num, model = self._read_conf()
        except:
            print(Chat.chat_page)
            num, model = input(
                "Please enter your choice here(Use space to split 2 values): "
            ).split(" ")
            self._write_into_conf(choice=num, model=model)
        return num, model

    # TODO: Read conf by properties_handler.py
    # def _read_conf(self) -> dict:
    #     r"""
    #     Though no params here,
    #     It's neccessary to write down the relationship between choice and model

    #     :choices:
    #         "1" : "ollama",
    #         "2" : "spark",
    #         "3" : "other"
    #     """
    #     with open(self.CONF_FILE) as f:
    #         conf = yaml.safe_load(f)
    #         return (
    #             conf["using_chat_model"]["choice"],
    #             conf["using_chat_model"]["model"],
    #         )

    # def _write_into_conf(self, **kwargs) -> None:
    #     r"""
    #     kwargs: Give Params with the formation:
    #     choice : str
    #     model : str

    #     :choices:
    #         "1" : "ollama",
    #         "2" : "spark",
    #         "3" : "other"

    #     See those AI files to get the informations of supported models.
    #     """
    #     # TODO: However, the key should be updated by parameters
    #     # This function will be the inner interface of SettingsPart.
    #     key = "using_chat_model"  # This is the key in configuration
    #     # FIXME
    #     # SetYaml.rewrite_yaml(key, kwargs)
