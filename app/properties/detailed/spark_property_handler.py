from utils import logger, set_frcolor
from app.properties.properties_handler import PropertiesHandler
from utils.conf_handler.yaml_handler import YamlWriter, read_properties_from_yaml


class GetSparkProperties(PropertiesHandler):
    r"""
    Get Spark Properties
    """

    application = "spark"
    # step_in is used in the key of property dict YamlWriter.write_yaml
    step_in = f"{application}_conf"

    @classmethod
    def get_properties(cls, model: str):
        properties = read_properties_from_yaml()
        # Since URL is initialized, here needn't validation.

        if properties[cls.step_in]["key"].get(model, None) is None:
            properties = cls._write_key(properties, model)

        return properties.get(cls.step_in, None)

    @classmethod
    def _write_key(cls, properties: dict, model: str) -> dict:
        r"""
        When key doesn't exist, write key to properties

        :param properties:
                dict: Properties
        :param model:
                str: Model
        """
        logger.warning("No API KEY detected!")
        value = input(
            set_frcolor(text="Please enter your API KEY here: ", color="yellow")
        )
        # Specified since Spark shares a different key with other applications
        if "Bearer " not in value:
            value = "Bearer " + value

        return YamlWriter().write_yaml(cls.step_in)(properties, "key", value, model)

    @classmethod
    def write_properties(
        cls, properties: dict, key: str, text: str, color: str = "yellow"
    ) -> dict:
        assert key != "key", ValueError(
            "This method isn't for setting API Key, go use <cls._write_key>"
        )
        return super().write_properties(properties, key, text, color)
