import utils


@utils.dcl.dataclass
class _Spark:
    r"""
    Spark AI

    Using Spark API to invoke LLMS.
    Default to "lite"

    Since the function "start()" is what I hope you to use.
    So Please use it like this:
    >>> model = "pro"
    >>> start("2", model)    # Invoke "pro"
    Avaliable Models:
    - lite
    - generalv3
    - pro-128k
    - generalv3.5
    - max-32k
    - 4.0Ultra
    """

    api: dict
    link: str
    apiKey: str
    model: str = "lite"
    support: utils.typing.ClassVar[list[str]] = [
        "lite",
        "generalv3",
        "pro-128k",
        "generalv3.5",
        "max-32k",
        "4.0Ultra",
    ]
    # The formation of key should be: "Bearer " + key

    def __post_init__(self):
        r"""
        For check the API_KEY of Spark
        """

        model = self.model.lower()
        if model in self.support:
            self.apiKey = utils.settings.SetYaml.check_if_none(self.api, 1, model)
        else:
            raise ValueError(f"Unsupported model: {self.model}")


@utils.dcl.dataclass
class _OtherAI:
    r"""
    ### Other AI

    Using the mirror website [aihubmix](www.aihubmix.com) to invoke LLMs.
    Default to gpt-3.5-turbo.

    Give the name of model to invoke other LLM.

    Since the function "start()" is what I hope you to use.
    So Please use it like this:
    >>> model = "qwen-long"
    >>> start("2", model)    # Invoke qwen-long
    """

    api: dict
    link: str = ""
    apiKey: str = ""
    model: str = utils.dcl.field(default="gpt-3.5-turbo")

    def __post_init__(self):
        r"""
        Check the API Key of models
        """
        model = self.model.lower()
        self.apiKey, self.link = utils.settings.SetYaml.check_if_none(
            self.api, 2, model
        )


def start(*choice: str) -> tuple[str, str]:
    r"""
    ### You must give the name of the model you want to use
    For example: Invoking "Spark Pro API":
    >>> start("1", "Spark Pro")

    ### Then it'll return a tuple[str, str], 1st is API Link, 2nd is API Key
    >>> link, pwd = start("1", "Spark Pro")
    >>> "link", "pwd"
    """
    api = utils.settings.SetYaml.read_yaml(filename="settings.yml")
    SPARK_LINK = api["spark_conf"][0]["Spark_Link"]
    SPARK_MODEL_KEYS = api["spark_conf"][1]["model_key"]
    OTHER_LINK = api["other_conf"][1]["Link"]
    OTHER_KEY = api["other_conf"][0]["Key"]
    match_idx_dict_for_spark = {
        "lite_Key": 0,
        "generalv3_Key": 1,
        "pro-128k_Key": 2,
        "max-32k_Key": 3,
        "4.0Ultra_Key": 4,
        "generalv3.5_Key": 5,
    }
    try:
        match choice:
            case ["1", str(model)]:  # Invoke Spark API
                utils.settings.logger.info(msg=f"Invoking Spark {model.upper()} API...")
                model_key = f"{model}_Key"
                model_idx = match_idx_dict_for_spark[model_key]
                spark = _Spark(
                    model=model,
                    api=api,
                    link=SPARK_LINK,
                    apiKey=SPARK_MODEL_KEYS[model_idx][model_key],
                )
                return spark.link, spark.apiKey

            case ["2", str(model)]:  # Invoke other API
                utils.settings.logger.info(f"Invoking {model.upper()} API...")
                Other = _OtherAI(
                    model=model, api=api, link=OTHER_LINK, apiKey=OTHER_KEY
                )
                return Other.link, Other.apiKey

            case _:  # Return None IF params can't match the formation
                utils.settings.logger.warning("Please enter the correct choice.")
                raise ValueError("Please enter the correct choice.")

    except Exception as e:
        raise ValueError(f"An error occurred while invoking AI: {e}")
