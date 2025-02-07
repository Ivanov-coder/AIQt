from app.properties.properties_handler import PropertiesHandler
from functions.page_controller.pages import Chat
from functions.page_controller.detailed.chat_page.chat import ChatWithAI
from functions.page_controller.detailed.page_register import PageRegister
from utils.conf_handler.yaml_handler import YamlWriter


class ForChatPart(PageRegister):
    def for_self_part(self):
        r"""Return the current PageStatus [CHAT]"""
        try:
            app, model = self._get_num_and_model()
            ChatWithAI(app, model).chat()
            current_page_status = self.update_status(
                current_page="Chat",
                available_dict=Chat.chat_page_avaliable_func,
                choice="M",
            )

        except KeyboardInterrupt:
            current_page_status = self.update_status(
                current_page="Chat",
                available_dict=Chat.chat_page_avaliable_func,
                choice="B",
            )

        return current_page_status

    def _get_num_and_model(self):
        r"""Get the choice and model, if not, write into conf."""
        try:
            choice, model = self._read_conf()
        except:
            print(Chat.chat_page)
            _num_to_model = {
                "1": "ollama",
                "2": "spark",
                "3": "other",
            }
            num, model = input(
                "Please enter your choice here(Use space to split 2 values): "
            ).split(" ")
            # This step is to transite the number into the name of app
            # If returned None, then the input is incorrect
            choice = _num_to_model.get(num, None)
            if not choice:
                raise RuntimeError(
                    "An error number entered, the value should be 1, 2 or 3"
                )

            self._write_into_conf(choice=choice, model=model)

        return choice, model

    def _read_conf(self) -> tuple[str, str]:
        r"""
        :choices:
            "1" : "ollama",
            "2" : "spark",
            "3" : "other"
        :returns:
            choice, model
        """
        data = PropertiesHandler.get_chat_model()
        return data["choice"], data["model"]

    def _write_into_conf(self, choice: str, model: str) -> None:
        r"""
        kwargs: Give Params with the formation:
        choice : str
        model : str

        :choices:
            "1" : "ollama",
            "2" : "spark",
            "3" : "other"

        See those AI files to get the informations of supported models.
        """
        key = "using_chat_model"  # This is the key in configuration
        YamlWriter.write_yaml(key)(choice, model)
