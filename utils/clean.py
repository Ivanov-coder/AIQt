import os

CACHE_PATH = "./cache/"
LOG_PATH = "./log/data.log"

def clean() -> None:
    """
    清除缓存和聊天记录.
    这部分稍微有点bug，多协程挂起后data.log还是处在被访问的状态。会导致报错。
    """     

    if os.path.exists(CACHE_PATH):
        for file in os.listdir(CACHE_PATH):
            os.remove(os.path.join(CACHE_PATH, file))
    
    # TODO: 这玩意等Qt出来了再做 要求用户断掉AI的连接再调用
    # if os.path.exists(LOG_PATH):
    #     os.remove(LOG_PATH)