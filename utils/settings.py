import os
import yaml
from . import logs

# 初始化日志
logger = logs.Logger.setup_logger(fileposition=__name__)
# 初始化cache文件夹
if not os.path.exists("./cache"):
    os.mkdir("./cache")


class SetYaml:

    def create_yaml(self):
        """
        如果没有配置文件，则创建一个
        """

        # 写入yaml文件的标准格式
        fmt = {
            "other": [{
                "Key": None
            }, {
                "Link": "https://aihubmix.com/v1/chat/completions"
            }],
            "spark": [
                {
                    "Spark_Link":
                    "https://spark-api-open.xf-yun.com/v1/chat/completions"
                },
                {
                    "lite_Key": None
                },
                {
                    "generalv3_Key": None
                },
                {
                    "pro-128k_Key": None
                },
                {
                    "max-32_Key": None
                },
                {
                    "4.0Ultra_Key": None
                },
                {
                    "generalv3.5_Key": None
                },
            ]
        }

        # 不存在就创建目录并写入
        if not os.path.exists("./config/conf.yaml"):
            os.mkdir("./config")
            with open("./config/conf.yaml", "w", encoding="utf-8") as f:
                yaml.dump(fmt, f, allow_unicode=True, sort_keys=False)

    def read_yaml(self) -> dict:
        """
        读取配置问价
        """
        # 存在直接开，不存在先写入再开
        if os.path.exists("./config/conf.yaml"):
            with open("./config/conf.yaml", "r", encoding="utf-8") as f:
                conf = yaml.safe_load(f)
            return conf

        else:
            self.create_yaml()
            return self.read_yaml()

    def check_if_none(self,
                      conf: str,
                      choice: int,
                      model: str = None) -> (str | tuple[str, str]):
        """
        **检查conf.yaml中是否含有API KEY.**
        如果有，直接返回，没有，写入文件后再返回。
        ### conf是必传参数！
        ## 1表示Spark AI，2表示其他AI
        >>>  _check_if_none(conf, 1, "lite") # 检查Spark AI的lite模型有没有API KEY
        >>>  _check_if_none(conf, 2, "qwen-long") # 检查qwen-long模型有没有API KEY
        如果choice是1 那么模型参数是必传的；如果是2，那就可以不传。
        ## choice为1时只返回key， choice为2是返回key和link
        """
        # 这一部分是为了Spark AI设置的
        match choice:
            case 1:
                # 将可能出现的情况建立字典映射 避免一堆if...elif...else...
                match_idx_dict = {
                    "lite_Key": 1,
                    "generalv3_Key": 2,
                    "pro-128k_Key": 3,
                    "max-32k_Key": 4,
                    "4.0Ultra_Key": 5,
                    "generalv3.5_Key": 6,
                }

                common = f"{model}_Key"
                idx = match_idx_dict.get(common)
                if not conf["spark"][idx][common]:
                    logger.warning(
                        f"API KEY for {model} is not set in conf.yaml")
                    # TODO: 在Qt中需要以输入框的形式存在
                    API_KEY = input("Please enter your API KEY here: ")

                    with open("./config/conf.yaml", "w",
                              encoding="utf-8") as f:
                        # 判断是否输入了"Bearer "前缀 没有就补上
                        if "Bearer " not in API_KEY:
                            conf["spark"][idx][common] = "Bearer " + API_KEY
                        else:
                            conf["spark"][idx][common] = API_KEY

                        yaml.safe_dump(conf, f)

                return conf["spark"][idx][common]

            # 以下是为了其他AI设置的 由于不强行要求使用aihubmix网站，所以还需要判断是否存在接口网址
            case 2:
                if not conf["other"][0]["Key"]:
                    logger.warning(
                        f"API KEY for {model} is not set in conf.yaml")
                    # TODO: 在Qt中需要以输入框的形式存在
                    API_KEY = input("Please enter your API KEY here: ")

                    with open("./config/conf.yaml", "w",
                              encoding="utf-8") as f:
                        conf["other"][0]["Key"] = API_KEY
                        yaml.safe_dump(conf, f)

                if not conf["other"][1]["Link"]:
                    logger.warning(
                        f"API LINK for {model} is not set in conf.yaml")
                    # TODO: 在Qt中需要以输入框的形式存在
                    API_LINK = input("Please enter your API LINK here: ")

                    with open("./config/conf.yaml", "w",
                              encoding="utf-8") as f:
                        conf["other"][1]["Link"] = API_LINK
                        yaml.safe_dump(conf, f)

                return conf["other"][0]["Key"], conf["other"][1]["Link"]
