import utils
from callAI import *

logger = utils.logs.Logger.setup_logger(fileposition=__name__)


# TODO: 在Qt中可能会存在开了Spark之后又开其它的情况，所以这里我们可能需要当窗口焦点改变时，做个挂起操作。
async def run():
    # TODO: 这里的实例化需要做成选择框给用户选择模型
    await spark.CallSparkAI().callByhttpx()
    # await httpx.CallOherAI().callByhttpx()


async def main():
    await run()


if __name__ == "__main__":
    while True:
        try:
            utils.asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("聊天记录已被删除")
            utils.os.remove("./cache/chat.json")
            break
        except Exception as e:
            logger.error(e)
            logger.info("你可以再次启动程序，聊天记录已经保存了")
            break
