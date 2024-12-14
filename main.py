# WARN: TTS almost done, Now ASR

from utils import os
from utils import clean
from utils import asyncio
from utils import GenerateID
from utils.settings import logger

randID = GenerateID.get_id()
count = 0 # 当生成wav时记录音频编号

def switch(choice: str):
    """
    做选择用的，后面估计得做到Qt选择框里面。
    """
    # TODO: 这里的实例化需要做成选择框给用户选择模型
    if choice == "web-spark":
        from webAI import spark

        return spark.CallSparkAI(model="lite").callByhttpx(random_id=randID)
    elif choice == "web-other":
        from webAI import other

        return other.CallOtherAI(model="qwen-long").callByhttpx(random_id=randID)

    elif choice == "local":
        import localAI

        global count    # 没法子了 不然每次进入循环都会被重新调用
        count += 1

        # TODO: 这里的实例化需要做成选择框给用户选择模型
        return localAI.ollamallm.CallOllamaAI(model="llama3.1").callByOllama(
            random_id=randID,
            isTTS=True,    # TODO: 做出来
            count=count
        )


# TODO: 在Qt中可能会存在开了Spark之后又开其它的情况，所以这里我们可能需要当窗口焦点改变时，做个挂起操作。
async def run():
    # TODO: 这里的实例化需要做成选择框给用户选择模型
    choice = "local"
    await switch(choice)


async def main():
    await run()


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        # TODO: Qt信号槽事件 需要更改模型之后重新生成聊天记录文件 => 也就是当选择框改变字段时，重新调用get_id()方法
        except KeyboardInterrupt:
            clean.clean()
            break
        
        # XXX: 这是本地情况
        except ModuleNotFoundError as e:
            logger.warning(e)
            logger.info("Installing requirements...")
            stdstatus = os.system("pip install -r requirements.txt")

            if stdstatus == 0:
                logger.info("Requirements installed successfully.")
            else:
                logger.error("Failed to install requirements.")
                break
        # PS 如果出了什么bug需要调试，请直接注释掉下面那一段
        # except Exception as e:
        #     logger.error(e)
        #     logger.info("Restarted")
