from .tts_handler import TTSHandler


class TTSRegister:
    r"""
    Class for registering TTS
    """

    def __init__(self):
        self._models = {}

    def register_model(self, name: str, model: TTSHandler) -> None:
        r"""
        :param:
            name: name of the model
            model: model class, now supports two:
                    - CoquiTTS
                    - PyTTS
                Here we will add more later
        """
        assert issubclass(model, TTSHandler), ValueError(
            "Model must be subclass of TTSHandler"
        )
        self._models[name] = model

    def unregister_model(self, name: str) -> bool:
        r"""
        When exist models and name in the models, delete the model

        :return:
            is_deleted (bool): Check if deleted and for the next step
        """
        if name in self._models:  # Avoid KeyError
            self._models.pop(name)
            return True

        return False

    def get_model(self, name):
        if name not in self._models:
            raise ValueError(f"Unknown model: {name}")

        return self._models[name]

    def get_models(self):
        return self._models.keys()
