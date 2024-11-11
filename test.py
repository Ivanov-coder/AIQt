import logging
import colorlog

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
def log(level: str) -> logging.Logger:
    logger = logging.getLogger()
    console = logging.StreamHandler()
    logger.setLevel(level)
    color = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s: %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    console.setFormatter(color)
    for handler in logger.handlers:
        logger.removeHandler(handler)

    logger.addHandler(console)
    return logger

if __name__ == '__main__':
    logger = log(logging.DEBUG)
    logger.debug('This is a debug message')
    logger.info('Hello World')
    logger.error('This is an error message')
    logger.warning('This is a warning message')
    logger.critical('This is a critical message')
