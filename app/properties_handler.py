from utils import logger
from utils import handle_yaml


# TODO: 以后试试注册表模式
class GetProperties:
    r"""
    Get Properties for AI
    This is the base class, used to register the factory pattern
    """

    application: str  # The app to be used, please assign it in the subclass

    # FIXME: Due to the inf loop, the _cache_pool seems to be useless
    @classmethod
    def _store_property(cls) -> dict:
        r"""
        Get Properties in configuration
        """
        _cache_pool = {}  # Store properties that have been requested.

        # TODO: If users changed the conf, we need to update.
        if not _cache_pool:
            # This step will directly load the whole configurations
            _cache_pool.update(handle_yaml())
            # print("Executed!")    # Each loop executed this part :/

        properties = _cache_pool.get(f"{cls.application}_conf", None)
        return properties

    @classmethod
    def get_properties(cls) -> dict:
        r"""
        Get properties from conf file.
        :returns:
            dict: Properties
        """
        raise NotImplementedError(
            f"Subclass <{cls.__class__.__name__}> must override the method <get_properties>"
        )


class GetSparkProperties(GetProperties):
    r"""
    Get Spark Properties
    """

    application = "spark"

    @classmethod
    def get_properties(cls) -> dict:
        return cls._store_property()


class GetOtherProperties(GetProperties):
    r"""
    Get Other Properties
    """

    application = "other"

    @classmethod
    def get_properties(cls) -> dict:
        return cls._store_property()


class GetOllamaProperties(GetProperties):
    r"""
    Get Ollama Properties
    """

    application = "ollama"

    @classmethod
    def get_properties(cls) -> dict:
        return cls._store_property()
