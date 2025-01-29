# WARN: TTS almost done, Now ASR
# TODO: 尝试在读取聊天记录那里实现缓存机制，以及当新增聊天记录多到某个数值时才写入文件，降低空间复杂度
from functions import CtrlBoard


if __name__ == "__main__":
    CtrlBoard().run()
