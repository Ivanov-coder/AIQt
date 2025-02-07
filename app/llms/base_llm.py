from tts import get_tts_socket


class AICaller:
    def __init__(self, model: str):
        raise NotImplementedError(
            f"Subclass {self.__class__.__name__} must implement abstract method __init__"
        )

    def _execute(self, data: list[dict], frcolor: str) -> str:
        raise NotImplementedError(
            f"Subclass {self.__class__.__name__} must implement abstract method _execute"
        )


    def _load_data(self, filename: str, ID: str) -> dict:
        raise NotImplementedError(
            f"Subclass {self.__class__.__name__} must implement abstract method _load_data"
        )

    def _write_cache(
        self,
        *,
        filename: str,
        ID: str,
        content: str,
        role: str = "user",
        isRolePlay: bool = False,
        image: str | bytes = None,
    ) -> None:
        raise NotImplementedError(
            f"Subclass {self.__class__.__name__} must implement abstract method _write_cache"
        )

    def _select_tts(
        self, model: str, filename: str, answer: str, lang: str = "en"
    ) -> None:
        r"""
        Select TTS engine, default to CoquiTTS
        """
        # FIXME: The parameters for TTS depends on the type the function returns...
        engine = get_tts_socket(model)(
            text=answer,
            filename=filename,
            lang=lang,
            # TODO: Before a good solution, stop those API
            # rate=150,
            # volume=1.0,
            # emotion="Neutral",
            # speed=1.0,
        )
        engine.get()

    def call(
        self,
        content: str,
        random_id: str,
        frcolor: str,
        count: int = 1,
    ) -> None:
        r"""
        Invoking the model in ollama to chat.
        :param:
                content (str):
                        The content of the chat.
                random_id (str):
                        Randomly generated id.
                        The main function of it is to distinguish users by different id, in order to classfiy the chatlog of users.
                isTTS (bool):
                        Check if users need TTS.
                        When first call the function, it'll check what TTS the user needs, and then mainly by this TTS.
                frcolor (str):
                        Used to control the color of the output in the terminal.
                count (int, default is 1):
                        Used to sort the order of each .wav file.
        """
        raise NotImplementedError(
            f"Subclass {self.__class__.__name__} must implement abstract method call"
        )
