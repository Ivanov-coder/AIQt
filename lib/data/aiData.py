import utils

# 初始化日志 以备打印信息
logger = utils.logs.Logger.setup_logger(fileposition=__name__)

with open("./conf.yaml", "r", encoding="utf-8") as f:
    conf = utils.yaml.safe_load(f)


def _check_if_none(choice: int, model: str = None):
    """
    **检查conf.yaml中是否含有API KEY.**
    如果有，直接返回，没有，写入文件后再返回。
    内置函数，不要在外部调用。
    ## 1表示Spark AI，2表示其他AI
    >>>  _check_if_none(1, "lite") # 检查Spark AI的lite模型有没有API KEY
    >>>  _check_if_none(2, "qwen-long") # 检查qwen-long模型有没有API KEY
    如果choice是1 那么模型参数是必传的；如果是2，那就可以不传。
    """
    # 这一部分是为了Spark AI设置的
    match choice:
        case 1:
            # 将可能出现的情况建立字典映射 避免一堆if...elif...else...
            match_idx_dict = {
                "lite_Key": 1,
                "generalv3_Key": 2,
                "pro-128k_Key": 3,
                "max-32k_Key": 4,
                "4.0Ultra_Key": 5,
                "generalv3.5_Key": 6,
            }

            common = f"{model}_Key"
            idx = match_idx_dict.get(common)
            if not conf["spark"][idx][common]:
                logger.warning(f"API KEY for {model} is not set in conf.yaml")
                API_KEY = input("Please enter your API KEY here: ")

                with open("./conf.yaml", "w", encoding="utf-8") as f:
                    conf["spark"][idx][common] = API_KEY
                    utils.yaml.safe_dump(conf, f)

            return conf["spark"][idx][common]

        case 2:
            if not conf["other"]["Key"]:
                logger.warning(f"API KEY for {model} is not set in conf.yaml")
                API_KEY = input("Please enter your API KEY here: ")

                with open("./conf.yaml", "w", encoding="utf-8") as f:
                    conf["other"]["Key"] = API_KEY
                    utils.yaml.safe_dump(conf, f)

            return conf["other"]["Key"]


# 现在只有Lite是能用的...
@utils.dcl.dataclass
class _Spark:
    """"
    Spark AI 数据类.
    使用Spark API调用AI模型.
    默认使用Spark Lite API，
    请不要在外部调用该类。
    由于可以被导出的函数为start，所以请使用下面的方法
    例如：
    >>> model = "pro" 
    >>> start("2", model)    # 调用pro
    支持调用的模型如下:
    - lite
    - generalv3
    - pro-128k
    - generalv3.5
    - max-32k
    - 4.0Ultra
    """
    model: str = "lite"
    link: str = conf["spark"][0]["Spark_Link"]
    # 这里不能直接定义为field 选择使用ClassVar类定义
    support: utils.typing.ClassVar[list[str]] = [
        "lite", "generalv3", "pro-128k", "generalv3.5", "max-32k", "4.0Ultra"
    ]
    # key的格式应为 "Bearer " + key
    apiKey: str = utils.dcl.field(default=conf["spark"][1]["lite_Key"],
                                  repr=False)

    def __post_init__(self):
        """
        匹配模型的API_KEY
        """

        model = self.model.lower()
        if model in self.support:
            self.apiKey = _check_if_none(1, model)
        else:
            raise ValueError(f"Unsupported model: {self.model}")


# TODO: 这里的API KEY最好也得做出来
@utils.dcl.dataclass
class _OtherAI:
    """
    ### 其他 AI 数据类。
    使用镜像网站[aihubmix](www.aihubmix.com)调用AI模型 。
    默认使用GPT-3.5-turbo，
    传入名字以调用其他模型。
    由于可以被导出的函数为start，所以请使用下面的方法
    例如：
    >>> model = "qwen-long" 
    >>> start("2", model)    # 调用qwen-long
    """
    model: str = utils.dcl.field(default="gpt-3.5-turbo")
    link: str = utils.dcl.field(default=conf["other"][1]["Link"])
    # 这里不能直接定义为field 选择使用ClassVar类定义
    # support: utils.typing.ClassVar[list[str]] = [
    #     "lite", "generalv3", "pro-128k", "generalv3.5", "max-32k", "4.0Ultra"
    # ]
    apiKey: str = utils.dcl.field(default=conf["other"][0]["Key"], repr=False)

    # def __post_init__(self):
    #     """
    #     匹配模型的API_KEY
    #     """
    #     model = self.model.lower()
    #     if model in self.support:
    #         self.apiKey = _check_if_none(2, model)
    #     else:
    #         raise ValueError(f"Unsupported model: {self.model}")


def start(*choice: str) -> tuple[str, str]:
    """
    ### 你传入的 参数必须有选择AI模型的值
    比如说你要调用Spark Pro API：
    >>> start("1", "Spark Pro")
    
    ### 返回值为一个元组，第一个元素是API的链接，第二个元素是API的密钥。
    >>> link, pwd = start("1", "Spark Pro")
    >>> "link", "pwd"
    """
    try:
        match choice:
        # 这里可以的话加个处理第二个参数没传的情况
            case ["1", str(model)]:  # 调用 Spark API
                logger.info(msg=f"Invoking Spark {model.upper()} API...")
                spark = _Spark(model=model)
                return spark.link, spark.apiKey

            case ["2", str(model)]:  # 调用 other API
                logger.info(f"Invoking {model.upper()} API...")
                Other = _OtherAI(model=model)
                return Other.link, Other.apiKey

            case _:  # 如果传参错误，返回None
                logger.warning("Please enter the correct choice.")
                return None, None

    except Exception as e:
        logger.error(f"An error occurred while invoking AI: {e}")
        raise ValueError(f"An error occurred while invoking AI: {e}")
