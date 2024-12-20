import os

CACHE_PATH = "./cache/"
AUDIO_PATH = "./audio"


# FIXME: 一个终端只能删自己的聊天记录！！！ 不要全删了！！！
# TODO: Qt信号槽事件 需要更改模型之后重新生成聊天记录文件 => 也就是当选择框改变字段时，重新调用get_id()方法
# def clean(filename: str) -> None:
def clean():
    """
    清除聊天记录/音频。
    """

    if os.path.exists(CACHE_PATH):
        for file in os.listdir(CACHE_PATH):
            # if filename in file:
                os.remove(os.path.join(CACHE_PATH, file))

    if os.path.exists(AUDIO_PATH):
        for file in os.listdir(AUDIO_PATH):
            # if filename in file:
                os.remove(os.path.join(AUDIO_PATH, file))
