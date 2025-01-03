import utils

api = utils.settings.SetYaml.read_yaml(filename="api.yaml")


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

    model: str = "lite"
    link: str = api["spark"][0]["Spark_Link"]
    # 这里不能直接定义为field 选择使用ClassVar类定义
    support: utils.typing.ClassVar[list[str]] = [
        "lite",
        "generalv3",
        "pro-128k",
        "generalv3.5",
        "max-32k",
        "4.0Ultra",
    ]
    # The formation of key should be: "Bearer " + key
    apiKey: str = utils.dcl.field(default=api["spark"][1]["lite_Key"], repr=False)

    def __post_init__(self):
        r"""
        For check the API_KEY of Spark
        """

        model = self.model.lower()
        if model in self.support:
            self.apiKey = utils.settings.SetYaml.check_if_none(api, 1, model)
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

    model: str = utils.dcl.field(default="gpt-3.5-turbo")
    link: str = utils.dcl.field(default=api["other"][1]["Link"])
    # 这里不能直接定义为field 选择使用ClassVar类定义
    # support: utils.typing.ClassVar[list[str]] = [
    #     "lite", "generalv3", "pro-128k", "generalv3.5", "max-32k", "4.0Ultra"
    # ]
    apiKey: str = utils.dcl.field(default=api["other"][0]["Key"], repr=False)

    def __post_init__(self):
        r"""
        Check the API Key of models
        """
        model = self.model.lower()
        # if model in self.support:
        #     self.apiKey = utils.settings.SetYaml().check_if_none(api, 2, model)
        # else:
        #     raise ValueError(f"Unsupported model: {self.model}")
        self.apiKey, self.link = utils.settings.SetYaml.check_if_none(api, 2, model)


def start(*choice: str) -> tuple[str, str]:
    r"""
    ### You must give the name of the model you want to use
    For example: Invoking "Spark Pro API":
    >>> start("1", "Spark Pro")

    ### Then it'll return a tuple[str, str], 1st is API Link, 2nd is API Key
    >>> link, pwd = start("1", "Spark Pro")
    >>> "link", "pwd"
    """
    try:
        match choice:
            
            case ["1", str(model)]:  # Invoke Spark API
                utils.settings.logger.info(msg=f"Invoking Spark {model.upper()} API...")
                spark = _Spark(model=model)
                return spark.link, spark.apiKey

            case ["2", str(model)]:  # Invoke other API
                utils.settings.logger.info(f"Invoking {model.upper()} API...")
                Other = _OtherAI(model=model)
                return Other.link, Other.apiKey

            case _:  # Return None IF params can't match the formation
                utils.settings.logger.warning("Please enter the correct choice.")
                raise ValueError("Please enter the correct choice.")

    except Exception as e:
        utils.settings.logger.error(f"An error occurred while invoking AI: {e}")
        raise ValueError(f"An error occurred while invoking AI: {e}")
