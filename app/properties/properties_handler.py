from utils import read_properties_from_yaml, set_frcolor
from utils.conf_handler.yaml_handler import YamlWriter


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
        # Default is without checking URL and API Key, but subclass should better overload this method
        properties = read_properties_from_yaml()
        return properties.get(f"{cls.application}_conf", None)

    @classmethod
    def write_properties(
        cls, properties: dict, key: str, text: str, color: str = "yellow"
    ) -> dict:
        r"""
        This method is for writing the properties of settings
        :params:
        properties (dict): the properties of whole settings
        key (str): the key of property dict
        text (str): the parameter for set_frcolor to handle, finally shows in the terminal
        color (str): the color of the text finally shows
        """
        assert key in properties[cls.step_in].keys(), KeyError("Key not in properties")

        value = input(set_frcolor(text=text, color=color))
        return YamlWriter().write_yaml(cls.step_in)(properties, key, value)
