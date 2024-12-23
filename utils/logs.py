import logging
import colorlog
import dataclasses as dcl


# 定义与日志有关的类
@dcl.dataclass(frozen=True)
class Logger:
    """
    这是一个关于日志的类。
    你可以根据需要更改日志级别和日志格式。
    - level: 日志级别
    - format_type: 日志格式
    """

    level: int = dcl.field(default=logging.INFO)
    format_type: str = dcl.field(
        default="%(asctime)s %(log_color)s| [%(levelname)s] | %(message)s"
    )

    @classmethod
    def setup_logger(cls) -> logging.Logger:
        """
        定义为类方法，
        可以通过Logger().setup_logger()来设置日志等级和输出格式。
        - level: 日志等级，默认为INFO， 定义在Logger中
        - format_type: 日志格式，默认为'asctime' | 'levelname' | 'name' | 'message'，定义在Logger中。
        - fileposition: 日志文件位置，定义在setup_logger中。
        返回logger对象。
        """
        # 感觉没有必要把日志写入文件中，不做了

        # 设置日志等级和格式
        logger = logging.getLogger()
        # 设置日志颜色
        handler = logging.StreamHandler()  # 初始化handler 并且加入自己的设置
        logger.setLevel(cls.level)  # 必须设置等级 否则不会输出日志信息
        # 自定义格式
        formatter = colorlog.ColoredFormatter(
            fmt=cls.format_type,
            datefmt="%Y-%m-%d %w %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
            style="%",
        )
        handler.setFormatter(formatter)
        # 去除原本的handler
        for h in logger.handlers:
            logger.removeHandler(h)

        # 添加自己的handler
        logger.addHandler(handler)

        # 返回logger对象
        return logger
