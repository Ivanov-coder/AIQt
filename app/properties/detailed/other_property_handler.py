from utils import logger
from app.properties.properties_handler import PropertiesHandler
from utils.conf_handler.yaml_handler import read_properties_from_yaml


class GetOtherProperties(PropertiesHandler):
    r"""
    Get Other Properties
    """

    application = "other"
    # step_in is used in the key of property dict YamlWriter.write_yaml
    step_in = f"{application}_conf"

    @classmethod
    def get_properties(cls) -> dict | None:
        properties = read_properties_from_yaml()

        # These two codes are used to check if url and key exist.
        properties = cls._handle_url(properties)
        properties = cls._handle_api_key(properties)

        return properties.get(cls.step_in, None)

    @classmethod
    def _handle_api_key(cls, properties: dict) -> dict:
        if properties[cls.step_in].get("key", None) is None:
            logger.warning("API key of your AI apps is not set")
            properties = cls.write_properties(
                properties, key="key", text="Please input the API key of your AI apps: "
            )

        return properties

    @classmethod
    def _handle_url(cls, properties: dict) -> dict:
        if properties[cls.step_in].get("link", None) is None:
            logger.warning("API Link of your AI apps is not set")
            properties = cls.write_properties(
                properties, key="link", text="Please input the Link of your AI apps: "
            )

        return properties
