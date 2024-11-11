import httpx
import utils
import lib.data.aiData as AI


def callSparkAI() -> None:
    """
    调用Spark AI.
    [官方文档](https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html#_1-%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E)
    """
    # 日志 确保只有执行callSparkAI函数时才被执行 而不是导包后就被执行
    logger = utils.logs.Logger.setup_logger(fileposition= __name__)

    # TODO: 需要把这个做出来到Qt中，成为滚动条去选择
    model = "lite"  # 如果有需要 请自行修改参数 默认为lite
    BASE_URL, API_KEY  = AI.start("1", model)
    # 这里只支持调用Spark AI 请不要在这里调用其他AI

    # TODO: 需要把这个做出来到Qt中，成为输入框
    content = input("请输入您的问题：")
    url = BASE_URL
    data = {
        "model": model,  # 指定请求的模型
        "messages": [{
            "role": "user",
            "content": content
        }],
    }
    header = {
        "Authorization": API_KEY  # 注意此处替换自己的APIPassword
    }
    response = httpx.post(url, headers=header, json=data)
    answer = response.json()["choices"]["message"]["content"] # 获取回答 请自行查阅API文档
    print(answer)