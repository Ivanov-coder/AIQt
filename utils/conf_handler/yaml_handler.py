import os
import yaml
from typing import Optional, Callable


class YamlConf:
    r"""
    Storing the basic configurations of yaml file
    """

    CONF_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "init.yml")

    def __init__(self):
        self.data = self._read_conf()
        self.ROOT = self.data["ROOT"]
        self.DUMPFILE = self.data["DUMPFILE"]
        self.CONFIG = self.data["CONFIG"]

    def _read_conf(self) -> dict:
        with open(self.CONF_ROOT, "r", encoding="utf-8"):
            return yaml.safe_load(self.CONF_ROOT)


class YamlReader(YamlConf):
    r"""
    Read settings.yml
    """

    def read_yaml(self) -> dict:
        r"""
        Read the conf file
        """
        with open(f"{self.ROOT}/{self.DUMPFILE}", "r", encoding="utf-8") as f:
            api = yaml.safe_load(f)
            return api


class YamlWriter(YamlConf):
    r"""
    Offer methods of some specific configurations of yaml file
    """

    # TODO: Think about the achieving methods
    # FOR WRITING A PART AS WELL AS REWRITING A PART

    def init_yaml(self) -> None:
        r"""
        Write the conf file when first create the file
        """
        with open(f"{self.ROOT}/{self.DUMPFILE}", "w", encoding="utf-8") as f:
            yaml.safe_dump(self.CONFIG, f)

    def write_yaml(self, step_in: str) -> Optional[Callable]:
        r"""
        This method is for writing a part of the conf file
        :param:
            step_in: This arg is for the first step when operating the dictionary

            step_in supports those parameters now:
            - using_chat_model
            - other_conf
            - spark_conf
            - ollama_conf

        :returns:
            actually this method will only return a Callable Object, which needs to be processed futher
        """
        assert step_in in self.CONFIG.keys(), ValueError(
            f"The step_in should be one of the value in {', '.join(self.CONFIG.keys())}"
        )

        _avaliable_func = {
            "using_chat_model": self._write_using_chat_model,
            "ollama_conf": self._write_ollama_conf,
            "other_conf": self._write_other_conf,
            "spark_conf": self._write_spark_conf,
        }

        return _avaliable_func.get(step_in, None)

    def _write_into_conf(self, new_conf: dict) -> None:
        r"""
        Write new configurations into files.
        Since in-place replacement, actually new_conf is "_original_conf" :/
        """
        with open(f"{self.ROOT}/{self.DUMPFILE}", "w", encoding="utf-8") as f:
            yaml.safe_dump(new_conf, f)

    def _write_using_chat_model(
        self, original_conf: dict, choice: str, model: str
    ) -> dict:
        r"""
        When the user choose to use the chat model, this method will be called
        :param:
            choice: This arg is for the choice of the user
        """
        original_conf["choice"] = choice
        original_conf["model"] = model
        self._write_into_conf(original_conf)

        return original_conf

    def _write_ollama_conf(
        self, original_conf: dict, key: str, value: str | bool
    ) -> dict:
        r"""
        When the user choose to customize ollama configurations, this method will be called
        :param:
            key: This arg is for the key of the ollama conf
            value: This arg is for the value of the ollama conf
        For example:
        >>> _write_ollama_conf("PERSONA", "I am a student")
        This step will change the PERSONA of ollama LLM

        When setting isTTS, value should be bool
        """

        assert key in original_conf["ollama_conf"].keys(), ValueError(
            f"The key should be one of the value in {', '.join(original_conf['ollama_conf'].keys())}"
        )
        original_conf["ollama_conf"][key] = value
        self._write_into_conf(original_conf)

        return original_conf

    def _write_other_conf(
        self, original_conf: dict, key: str, value: str | bool
    ) -> dict:
        r"""
        When the user choose to customize other configurations, this method will be called
        :param:
            key: This arg is for the key of the other conf
            value: This arg is for the value of the other conf
        For example:
        >>> _write_spark_conf("isTTS", True)

        When setting isTTS, value should be bool
        """
        assert key in original_conf["other_conf"].keys(), ValueError(
            f"The key should be one of the value in {', '.join(original_conf['other_conf'].keys())}"
        )
        original_conf["other_conf"][key] = value
        self._write_into_conf(original_conf)

        return original_conf

    def _write_spark_conf(
        self, original_conf: dict, key: str, value: str | bool, model: str = None
    ) -> dict:
        r"""
        When the user choose to customize spark configurations, this method will be called
        :param:
            original_conf: This stores all properties of the model
            key: This arg is for the key of the spark conf
            value: This arg is for the value of the spark conf
            model: When setting API key, it'll be necessary
        For example:
        >>> _write_spark_conf("isTTS", True)

        When setting isTTS, value should be bool

        When setting the API Key of a model, like this:
        >>> _write_spark_conf("key", "API_KEY", "model_name")
        """
        assert key in original_conf["spark_conf"].keys(), ValueError(
            f"The key should be one of the value in {', '.join(original_conf['spark_conf'].keys())}"
        )

        if key != "key":
            original_conf["spark_conf"][key] = value
            self._write_into_conf(original_conf)

        else:
            original_conf["spark_conf"][key][model] = value
            self._write_into_conf(original_conf)

        return original_conf


# class YamlChecker(YamlConf):
# TODO: Write this method in /app/properties_handler and delete it
# Saved in /pic/check_if_none.png
# r""" """


def read_properties_from_yaml():
    r"""
    This is just the simplest version of yaml handler

    When has the conf file, return

    When not, create one and return YamlConf.CONFIG
    """
    try:
        return YamlReader().read_yaml()
    except FileNotFoundError:
        YamlWriter().init_yaml()
        return YamlConf().CONFIG
