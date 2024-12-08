# 正在开发TTS和ASR

from utils import os
from utils import clean
from utils import asyncio
from utils import GenerateID
from utils.settings import logger

randID = GenerateID.get_id()


def switch(choice: str) -> None:
    """
    做选择用的，后面估计得做到Qt选择框里面。
    """
    # TODO: 这里的实例化需要做成选择框给用户选择模型
    if choice == "web-spark":
        from webAI import spark
        return spark.CallSparkAI(model="lite").callByhttpx(random_id=randID)
    elif choice == "web-other":
        from webAI import other
        return other.CallOtherAI(model="qwen-long").callByhttpx(
            random_id=randID)

    elif choice == "local":
        import localAI
        # TODO: 这里的实例化需要做成选择框给用户选择模型
        return localAI.ollamallm.CallOllamaAI(model="llama3.1").callByOllama(
            random_id=randID)


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
        # TODO: Qt信号槽事件 需要更改模型之后重新生成聊天记录文件
        # TODO: 也就是当选择框改变字段时，重新调用get_id()方法
        except KeyboardInterrupt:
            clean.clean()
            break

        except ModuleNotFoundError as e:
            logger.warning(e)
            logger.info("Installing requirements...")
            stdstatus = os.system("pip install -r requirements.txt")

            if stdstatus == 0:
                logger.info("Requirements installed successfully.")
            else:
                logger.error("Failed to install requirements.")
                break

        # except Exception as e:
        #     logger.error(e)
        #     logger.info("Restarted")
