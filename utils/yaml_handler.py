import os
import yaml


class YamlConf:
    BASIC: str = "./config"
    DUMPFILE = "settings.yml"
    # TODO: You'd better not create it at first unless you need to write it
    # 232 bytes:
    CONFIG = {
        "using_chat_model": {"choice": "1", "model": "llama3.1"},
        "ollama_conf": {
            "PERSONA": "You are the sarcastic AI VTuber Neuro-sama. You are super confident about yourself.You have a lot of knowledge and you are willing to help others. You like using emojis very much.",
            "LANG": "en",
            "isTTS": False,  # Default to be False, it should be opened by user
        },
        "other_conf": {
            "link": None,
            "key": None,
            "PERSONA": "You are the sarcastic AI VTuber Neuro-sama. You are super confident about yourself.You have a lot of knowledge and you are willing to help others. You like using emojis very much.",
            "LANG": "en",
            "isTTS": False,  # Default to be False, it should be opened by user
        },
        "spark_conf": {
            "link": "https://spark-api-open.xf-yun.com/v1/chat/completions",
            "key": {
                "lite": None,
                "generalv3": None,
                "pro-128k": None,
                "max-32": None,
                "4.0Ultra": None,
                "generalv3.5": None,
            },
        },
    }


class YamlReader(YamlConf):
    @classmethod
    def read_yaml(cls) -> dict:
        r"""
        Read the conf file
        """
        with open(f"{cls.BASIC}/{cls.DUMPFILE}", "r", encoding="utf-8") as f:
            api = yaml.safe_load(f)
            return api


class YamlWriter(YamlConf):
    # TODO: Think about the achieving methods
    # FOR WRITING A PART AS WELL AS REWRITING A PART
    @classmethod
    def write_yaml(cls):
        r"""
        Write the conf file when first create the file
        """
        with open(f"{cls.BASIC}/{cls.DUMPFILE}", "w", encoding="utf-8") as f:
            yaml.safe_dump(cls.CONFIG, f)


class YamlChecker(YamlConf):
    # TODO: Write this method in /app/properties_handler and delete it
    # Saved in /pic/check_if_none.png
    pass


def handle_yaml():
    r"""
    This is just the simplest version of yaml handler

    When has the conf file, return
    
    When not, create one and return YamlConf.CONFIG
    """
    try:
        return YamlReader.read_yaml()
    except FileNotFoundError:
        YamlWriter.write_yaml(YamlConf.CONFIG)
        return YamlConf.CONFIG
