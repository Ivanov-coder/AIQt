import re
import yaml
import utils

# 初始化日志 以备打印信息
logger = utils.logs.Logger.setup_logger(fileposition= __name__)


# TODO: 想个办法把API KEY啥的统一丢到一个配置文件里面
# TODO: 现在有个大问题 BYD讯飞星火设置了好几个不同的API KEY 所以还得把它做出来给别人更改
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
    link: str = "https://spark-api-open.xf-yun.com/v1/chat/completions"

    # 这里的"Bearer "不可省略！ key的格式应为 "Bearer " + key
    apiKey: str = utils.dcl.field(
        default="Bearer GpbCOeQkmowTpvxxyVcs:pdJpmahxnlZjysFDQBqS", repr=False)


# TODO: 这里的API KEY最好也得做出来
@utils.dcl.dataclass
class _OtherAI:
    """"
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
    link: str = utils.dcl.field(default="https://aihubmix.com/v1/chat/completions")
    apiKey: str = utils.dcl.field(
        default="sk-F0DaRiRQsNmDEYA016903c9dAb854b009c1cE4A234B5A129",
        repr=False)

    def __post_init__(self) -> None:
        if re.match(r"^(gpt){1}", self.model):
            pass
        else:
            self.link = "https://aihubmix.com/v1/chat/completions"



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
            spark = _Spark(model=model)
            return spark.link, spark.apiKey

        case ["2", str(model)]:  # 调用 other API
            logger.info(f"Invoking {model} API...")
            Other = _OtherAI(model=model)
            return Other.link, Other.apiKey

        case _:  # 如果传参错误，返回None
            logger.warning("Please enter the correct choice.")
            return None, None