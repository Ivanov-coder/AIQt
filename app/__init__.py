def get_socket(choice: str = "ollama"):
    r"""
    The function of it is to get the socket of AI applications
    :param choice: the choice of socket
    """
    if choice == "ollama":
        from .ollamallm import CallOllamaAI

        return CallOllamaAI

    elif choice == "other":
        from .other import CallOtherAI

        return CallOtherAI

    elif choice == "spark":
        from .spark import CallSparkAI

        return CallSparkAI

    else:
        raise ValueError("The choice of socket must be ollama, other or spark")
