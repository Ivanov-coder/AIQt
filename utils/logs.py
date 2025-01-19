import logging
import colorlog


class Logger:
    r"""
    A class of Logger
    - level: the level of Logs, default to be Logger.INFO
    - format_type: the format of Logs, default to be 'asctime' | 'levelname' | 'name' | 'message'
    """

    level: int = logging.INFO
    format_type: str = "%(asctime)s %(log_color)s| [%(levelname)s] | %(message)s"

    @classmethod
    def setup_logger(cls) -> logging.Logger:
        r"""
        Set level and format_type by `Logger().setup_logger()`
        :params:
        - level: default to be Logger.INFO
        - format_type: default to be 'asctime' | 'levelname' | 'name' | 'message'，定义在Logger中。
        :return:
        logging.Logger
        """
        logger = logging.getLogger()  # 设置日志等级和格式
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
        for h in logger.handlers:
            # 去除原本的handler
            logger.removeHandler(h)
        logger.addHandler(handler)  # 添加自己的handler
        return logger
