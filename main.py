from utils import os
from utils import clean
from utils import asyncio
from utils.settings import logger

def switch(choice: str) -> None:
    """
    做选择用的，后面估计得做到Qt选择框里面。
    """
    if choice == "web":
        import webAI
        # TODO: 这里的实例化需要做成选择框给用户选择模型
        return webAI.sparkllm.CallSparkAI("lite").callByhttpx()
        # return other.CallOherAI("qwen-long").callByhttpx()

    elif choice == "local":
        import localAI
        # TODO: 这里的实例化需要做成选择框给用户选择模型
        return localAI.ollamallm.CallOllamaAI(model="gemma").callByOllama()

# TODO: 在Qt中可能会存在开了Spark之后又开其它的情况，所以这里我们可能需要当窗口焦点改变时，做个挂起操作。
async def run():
    # TODO: 这里的实例化需要做成选择框给用户选择模型
    await switch("local")

async def main():
    await run()


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            # TODO: Qt信号槽事件 是否清除缓存
            clean.clean()
            break

        except ModuleNotFoundError as e:
            logger.warning(e)
            logger.info("Installing requirements...")
            os.system("pip install -r requirements.txt")

        except Exception as e:
            logger.error(e)
            logger.info("Restarted")