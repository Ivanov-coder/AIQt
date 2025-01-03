import os
import yaml
from . import dcl
from . import logs

# 初始化日志
logger = logs.Logger.setup_logger()


@dcl.dataclass
class SetYaml:

    BASIC: str = "./config"

    @classmethod
    def create_yaml(cls):
        """
        如果没有配置文件，则创建一个
        """
        # "https://aihubmix.com/v1/chat/completions"    AihubMix 的聊天对接
        FMT = {
            "other": [
                {"Key": None},
                {"Link": None},
            ],
            "spark": [
                {"Spark_Link": "https://spark-api-open.xf-yun.com/v1/chat/completions"},
                {"lite_Key": None},
                {"generalv3_Key": None},
                {"pro-128k_Key": None},
                {"max-32_Key": None},
                {"4.0Ultra_Key": None},
                {"generalv3.5_Key": None},
            ],
        }

        PERSONA = {
            "PERSONA": "You are the sarcastic AI VTuber Neuro-sama. You are super confident about yourself.You have a lot of knowledge and you are willing to help others. You like using emojis very much.",
            "LANG": "en",
        }

        # TODO: 新开个 conf.yaml来配置语音的语言设置等
        with open(f"{cls.BASIC}/api.yaml", "w", encoding="utf-8") as f:
            yaml.dump(FMT, f, allow_unicode=True, sort_keys=False)

        with open(f"{cls.BASIC}/ollamapersona.yaml", "w", encoding="utf-8") as f:
            yaml.dump(PERSONA, f, allow_unicode=True, sort_keys=False)

        with open(f"{cls.BASIC}/otherpersona.yaml", "w", encoding="utf-8") as f:
            yaml.dump(PERSONA, f, allow_unicode=True, sort_keys=False)

    @classmethod
    def read_yaml(cls, filename: str) -> dict:
        """
        读取配置文件
        """
        # 存在直接开，不存在先写入再开
        if os.path.exists(f"{cls.BASIC}/{filename}"):
            with open(f"{cls.BASIC}/{filename}", "r", encoding="utf-8") as f:
                api = yaml.safe_load(f)
            return api

        else:
            cls.create_yaml()
            return cls.read_yaml(filename)

    @classmethod
    def check_if_none(
        cls, api: str, choice: int, model: str = None
    ) -> str | tuple[str, str]:
        """
        **检查api.yaml中是否含有API KEY.**
        如果有，直接返回，没有，写入文件后再返回。
        ### api是必传参数！
        ## 1表示Spark AI，2表示其他AI
        >>>  check_if_none(api, 1, "lite") # 检查Spark AI的lite模型有没有API KEY
        >>>  check_if_none(api, 2, "qwen-long") # 检查qwen-long模型有没有API KEY
        如果choice是1 那么模型参数是必传的；如果是2，那就可以不传。
        ## choice为1时只返回key， choice为2是返回key和link
        """
        # 这一部分是为了Spark AI设置的
        match choice:
            case 1:
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
                if not api["spark"][idx][common]:
                    logger.warning(f"API KEY for {model} is not set in api.yaml")
                    # TODO: 在Qt中需要以输入框的形式存在
                    API_KEY = input("Please enter your API KEY here: ")

                    with open(f"{cls.BASIC}/api.yaml", "w", encoding="utf-8") as f:
                        # 判断是否输入了"Bearer "前缀 没有就补上
                        if "Bearer " not in API_KEY:
                            api["spark"][idx][common] = "Bearer " + API_KEY
                        else:
                            api["spark"][idx][common] = API_KEY

                        yaml.safe_dump(api, f)

                return api["spark"][idx][common]

            # 以下是为了其他AI设置的 由于不强行要求使用aihubmix网站，所以还需要判断是否存在接口网址
            case 2:
                if not api["other"][0]["Key"]:
                    logger.warning(f"API KEY for {model} is not set in api.yaml")
                    # TODO: 在Qt中需要以输入框的形式存在
                    API_KEY = input("Please enter your API KEY here: ")

                    with open(f"{cls.BASIC}/api.yaml", "w", encoding="utf-8") as f:
                        api["other"][0]["Key"] = API_KEY
                        yaml.safe_dump(api, f)

                if not api["other"][1]["Link"]:
                    logger.warning(f"API LINK for {model} is not set in api.yaml")
                    # TODO: 在Qt中需要以输入框的形式存在
                    API_LINK = input("Please enter your API LINK here: ")

                    with open(f"{cls.BASIC}/api.yaml", "w", encoding="utf-8") as f:
                        api["other"][1]["Link"] = API_LINK
                        yaml.safe_dump(api, f)

                return api["other"][0]["Key"], api["other"][1]["Link"]

            # TODO: 这部分是为了ollama的人格设置的
            case 3:
                pass
