import logging
import colorlog
import dataclasses as dcl


# 定义日志格式
@dcl.dataclass
class Logger:
    """
    这是一个关于日志的类。
    你可以根据需要更改日志级别和日志格式。
    - level: 日志级别
    - format_type: 日志格式
    """
    level: int = dcl.field(default=logging.INFO)
    format_type: str = dcl.field(
        default='%(asctime)s | %(levelname)s | %(name)s | %(message)s')

    @classmethod
    def setup_logger(cls, fileposition: str = __name__) -> logging.Logger:
        """
        定义为类方法，
        可以通过Logger().setup_logger()来设置日志等级和输出格式。
        - level: 日志等级，默认为INFO， 定义在Logger中
        - format_type: 日志格式，默认为'asctime' | 'levelname' | 'name' | 'message'，定义在Logger中。
        - fileposition: 日志文件位置，定义在setup_logger中。
        返回logger对象。
        """

        # 设置日志等级和格式
        logging.basicConfig(level=cls.level, format=cls.format_type)
        logger = logging.getLogger(fileposition)

        # 设置日志颜色
        # handler = logging.StreamHandler()
        # formatter = colorlog.ColoredFormatter(
        #     "%(log_color)s%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        #     datefmt=None,
        #     reset=True,
        #     log_colors={
        #         'DEBUG': 'cyan',
        #         'INFO': 'green',
        #         'WARNING': 'yellow',
        #         'ERROR': 'red',
        #         'CRITICAL': 'red,bg_white',
        #     },
        #     secondary_log_colors={},
        #     style='%')
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)

        # 返回logger对象
        return logger
