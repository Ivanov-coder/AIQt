# from .properties_handler import *

# __all__ = [
#     "get_socket",
#     "GetOllamaProperties",
#     "GetSparkProperties",
#     "GetOtherProperties",
# ]


def get_app_socket(choice: str = "ollama"):
    r"""
    The function of it is to get the socket of AI applications
    :param choice: the choice of socket
    """
    if choice == "ollama":
        from .llms.detailed.ollama_handler import CallOllamaAI

        return CallOllamaAI

    elif choice == "other":
        from .llms.detailed.other_handler import CallOtherAI

        return CallOtherAI

    elif choice == "spark":
        from .llms.detailed.spark_handler import CallSparkAI

        return CallSparkAI

    else:
        raise ValueError("The choice of socket must be ollama, other or spark")
