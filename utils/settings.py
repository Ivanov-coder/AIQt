import os
import yaml
from . import logs

logger = logs.Logger.setup_logger()


class SetYaml:

    BASIC: str = "./config"
    DUMPFILE = "settings.yml"
    CONFIG = {
        "using_chat_model": [{"choice": "1"}, {"model": "llama3.1"}],
        "ollama_conf": [
            {
                "PERSONA": "You are the sarcastic AI VTuber Neuro-sama. You are super confident about yourself.You have a lot of knowledge and you are willing to help others. You like using emojis very much."
            },
            {"LANG": "en"},
            {"isTTS": False},  # Default to be False, it should be opened by user
        ],
        "other_conf": [
            {"Key": None},
            {"Link": None},
            {
                "PERSONA": "You are the sarcastic AI VTuber Neuro-sama. You are super confident about yourself.You have a lot of knowledge and you are willing to help others. You like using emojis very much."
            },
            {"LANG": "en"},
            {"isTTS": False},  # Default to be False, it should be opened by user
        ],
        "spark_conf": [
            {"Spark_Link": "https://spark-api-open.xf-yun.com/v1/chat/completions"},
            {
                "model_key": [
                    {"lite_Key": None},
                    {"generalv3_Key": None},
                    {"pro-128k_Key": None},
                    {"max-32_Key": None},
                    {"4.0Ultra_Key": None},
                    {"generalv3.5_Key": None},
                ]
            },
        ],
    }

    @classmethod
    def create_yaml(cls):
        r"""
        Create a configuration file when haven't
        """

        with open(f"{cls.BASIC}/{cls.DUMPFILE}", "w", encoding="utf-8") as f:
            yaml.safe_dump(cls.CONFIG, f)

    @classmethod
    def read_yaml(cls, filename: str) -> dict:
        r"""
        Read the conf file
        """
        if not filename:
            filename = cls.DUMPFILE

        if not os.path.exists(f"{cls.BASIC}/{filename}"):
            cls.create_yaml()
            return cls.read_yaml(filename)

        with open(f"{cls.BASIC}/{filename}", "r", encoding="utf-8") as f:
            api = yaml.safe_load(f)
            return api

    @classmethod
    def rewrite_yaml(cls, key: str, rewrite_data):
        r"""
        Rewrite the configuration
        :params:
        - key: the key of the configuration (the type of conf is a dictionary)
        - rewrite_data: things you want to rewrite, dictionary only
        """

        cls.CONFIG[key] = [rewrite_data]
        with open(f"{cls.BASIC}/{cls.DUMPFILE}", "w", encoding="utf-8") as f:
            yaml.safe_dump(cls.CONFIG, f)

    @classmethod
    def check_if_none(
        cls, api: str, choice: int, model: str = None
    ) -> str | tuple[str, str]:
        r"""
        Check if cls.DUMPFILE has API KEY.
        If have, return.
        Else, write and return.

        :params:
        - api: the configuration file
        - choice: 1 for Spark AI, 2 for other AI
        - model: the model name of Spark AI

        >>>  check_if_none(api, 1, "lite")
        >>>  check_if_none(api, 2, "qwen-long")

        :return:
        - Spark AI: return API KEY
        - other AI: return API KEY and Link
        """
        match choice:
            # For Spark
            case 1:
                match_idx_dict = {
                    "lite_Key": 0,
                    "generalv3_Key": 1,
                    "pro-128k_Key": 2,
                    "max-32k_Key": 3,
                    "4.0Ultra_Key": 4,
                    "generalv3.5_Key": 5,
                }

                selected_model = f"{model}_Key"
                idx = match_idx_dict.get(selected_model)
                spark_model_key = api["spark_conf"][1]["model_key"][idx][selected_model]

                if not spark_model_key:
                    logger.warning(f"API KEY for {model} is not set in {cls.DUMPFILE}")
                    # TODO: 在Qt中需要以输入框的形式存在
                    spark_model_key = input("Please enter your API KEY here: ")

                    with open(
                        f"{cls.BASIC}/{cls.DUMPFILE}", "w", encoding="utf-8"
                    ) as f:
                        # Change using_chat_model here
                        cls.CONFIG["using_chat_model"] = [
                            {"choice": "2"},
                            {"model": model},
                        ]
                        # Add Bearer when lack of it
                        if "Bearer " not in spark_model_key:
                            cls.CONFIG["spark_conf"][1]["model_key"][idx][
                                selected_model
                            ] = ("Bearer " + spark_model_key)
                        else:
                            cls.CONFIG["spark_conf"][1]["model_key"][idx][
                                selected_model
                            ] = spark_model_key

                        yaml.safe_dump(cls.CONFIG, f)

                return spark_model_key

            # For Others
            case 2:
                other_model_key = api["other_conf"][0]["Key"]
                other_model_link = api["other_conf"][1]["Link"]

                if not other_model_key:
                    logger.warning(f"API KEY for {model} is not set in {cls.DUMPFILE}")
                    # TODO: 在Qt中需要以输入框的形式存在
                    other_model_key = input("Please enter your API KEY here: ")

                    with open(
                        f"{cls.BASIC}/{cls.DUMPFILE}", "w", encoding="utf-8"
                    ) as f:
                        cls.CONFIG["using_chat_model"] = [
                            {"choice": "3"},
                            {"model": model},
                        ]
                        cls.CONFIG["other_conf"][0]["Key"] = other_model_key
                        yaml.safe_dump(cls.CONFIG, f)

                if not other_model_link:
                    logger.warning(f"API LINK for {model} is not set in {cls.DUMPFILE}")
                    # TODO: 在Qt中需要以输入框的形式存在
                    other_model_link = input("Please enter your API LINK here: ")

                    with open(
                        f"{cls.BASIC}/{cls.DUMPFILE}", "w", encoding="utf-8"
                    ) as f:
                        cls.CONFIG["other_conf"][1]["Link"] = other_model_link
                        yaml.safe_dump(cls.CONFIG, f)

                return other_model_key, other_model_link
