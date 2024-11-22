import utils
from callAI import *

logger = utils.logs.Logger.setup_logger(fileposition=__name__)

CACHE_PATH = "./cache/chat.json"
LOG_PATH = "./log/data.log"

# TODO: 在Qt中可能会存在开了Spark之后又开其它的情况，所以这里我们可能需要当窗口焦点改变时，做个挂起操作。
async def run():
    # TODO: 这里的实例化需要做成选择框给用户选择模型
    await sparkllm.CallSparkAI("lite").callByhttpx()
    # await other.CallOherAI("qwen-long").callByhttpx()


async def main():
    await run()


if __name__ == "__main__":
    while True:
        try:
            utils.asyncio.run(main())
        except KeyboardInterrupt:
            # TODO: Qt信号槽事件 是否清除缓存
            # 草 暂时想不到报错的解决方案
            utils.clean.clean()
            break
        except Exception as e:
            logger.error(e)
            logger.info("Restarted")
