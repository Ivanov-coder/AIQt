import utils
from callAI import *

logger = utils.logs.Logger.setup_logger(fileposition=__name__)

async def run():
    await spark.CallSparkAI().callByhttpx()   # default is "lite"
    # await httpx.CallOherAI().callByhttpx()

async def main():
    await run()


if __name__ == '__main__':
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
            