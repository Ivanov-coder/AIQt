from utils import read_properties_from_yaml


class PropertiesHandler:
    r"""
    Get Properties for AI
    This is the base class, used to register the factory pattern
    """

    # Place it in get_properties if possible
    application: str  # The app to be used, please assign it in the subclass
    step_in: str

    @classmethod
    def get_chat_model(cls) -> dict:
        r"""
        Get chat model from conf file.
        :returns:
            dict: Selected APP and chat model
        """
        properties = read_properties_from_yaml()
        return properties.get("using_chat_model", None)

    @classmethod
    def get_properties(cls) -> dict:
        r"""
        Get properties from conf file.
        :returns:
            dict: Properties
        """
        # TODO: Here actually need validation, to check if BASE_URL and API_KEY exists.
        properties = read_properties_from_yaml()
        return properties.get(f"{cls.application}_conf", None)

    @classmethod
    def write_properties(cls, properties: dict) -> None:
        r"""
        Write properties to conf file.
        :param properties:
            dict: Properties
        """
        
        
    
    def _write_url(cls, properties: dict) -> dict:
        r"""
        When url doesn't exist, write url to properties
        :param properties:
            dict: Properties
        
        :returns:
            dict: Properties
        """
        pass

    def _write_key(cls, properties: dict, model: str) -> dict:
        r"""
        When key doesn't exist, write key to properties

        :param properties:
            dict: Properties
        :param model:
            str: Model
        
        :returns:
            dict: Properties
        """
        pass
