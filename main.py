# 5. 数据库可以使用mysql：
# 6. 预设表的字段是: id[int]=>, model[varchar], prompt[varchar]=>给llm预设的人格/提示词等, filepath[varchar]=> 聊天记录的文件路径, time[datetime], user[varchar]=> 用户(将成为btree主键)

from utils import os
from utils import clean
from utils import asyncio
from utils import GenerateID
from utils.settings import logger

randKey, randID = GenerateID.get_id()

def switch(choice: str) -> None:
    """
    做选择用的，后面估计得做到Qt选择框里面。
    """
    if choice == "web":
        import webAI
        # TODO: 这里的实例化需要做成选择框给用户选择模型
        return webAI.spark.CallSparkAI("lite").callByhttpx()
        # return other.CallOherAI("qwen-long").callByhttpx()

    elif choice == "local":
        import localAI
        # TODO: 这里的实例化需要做成选择框给用户选择模型
        return localAI.ollamallm.CallOllamaAI(
            model="llama3.1",
            random_key=randKey).callByOllama(random_id=randID)


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
