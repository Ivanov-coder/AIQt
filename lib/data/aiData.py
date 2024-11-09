import re
import utils

# 初始化日志 以备打印信息
logger = utils.logs.Logger.setup_logger(fileposition= __name__)


@utils.dcl.dataclass
class Spark:
    """"
    Spark AI 数据类
    目前 不可用 :/
    """
    model: str = "lite"
    link: str = "https://spark-api-open.xf-yun.com/v1/chat/completions"

    # 这里的"Bearer "不可省略！ key的格式应为 "Bearer " + key
    apiKey: str = utils.dcl.field(
        default="Bearer GpbCOeQkmowTpvxxyVcs:pdJpmahxnlZjysFDQBqS", repr=False)


@utils.dcl.dataclass
class OpenAI:
    """"
    ### 其他 AI 数据类。
    默认 使用镜像网站[aihubmix](www.aihubmix.com)调用AI模型 。
    默认使用GPT-3.5-turbo，
    传入名字以调用其他模型。
    例如：
    >>> model = "gpt-4" # 调用GPT-4
    """
    model: str = utils.dcl.field(default="gpt-3.5-turbo")
    link: str = utils.dcl.field(default="https://aihubmix.com/v1/chat/completions")
    apiKey: str = utils.dcl.field(
        default="sk-F0DaRiRQsNmDEYA016903c9dAb854b009c1cE4A234B5A129",
        repr=False)

    def __post_init__(self) -> None:
        if re.match(r"^(gpt){1}", self.model):
            pass
        else:
            self.link = "https://aihubmix.com/v1/chat/completions"


@utils.dcl.dataclass
class QwenLong:
    model: str = utils.dcl.field(default="qwen-long")
    link: str = utils.dcl.field(default="https://api.qwenlong.com/v1")
    apiKey: str = utils.dcl.field(default="", repr=False)


def start(*choice: str) -> tuple[str, str]:
    """
    ### 你传入的 参数必须有选择AI模型的值
    比如说你要调用Spark Pro API：
    >>> start("1", "Spark Pro")
    
    ### 返回值为一个元组，第一个元素是API的链接，第二个元素是API的密钥。
    >>> link, pwd = start("1", "Spark Pro")
    >>> "link", "pwd"
    """

    match choice:

        case ["1", str(model)]:  # 调用 Spark API
            logger.info(msg="Invoking Spark API...")
            spark = Spark(model=model)
            return spark.link, spark.apiKey

        case ["2", str(model)]:  # 调用 other API
            logger.info(f"Invoking {model} API...")
            Other = OpenAI(model=model)
            return Other.link, Other.apiKey

        case _:  # 如果传参错误，返回None
            logger.warning("Please enter the correct choice.")
            return None, None
