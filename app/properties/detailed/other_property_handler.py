from app.properties.properties_handler import PropertiesHandler
from utils.conf_handler.yaml_handler import read_properties_from_yaml


class GetOtherProperties(PropertiesHandler):
    r"""
    Get Other Properties
    """

    application = "other"
    # step_in is used in the key of property dict YamlWriter.write_yaml
    step_in = f"{application}_conf"

    def get_properties(self):
        properties = read_properties_from_yaml()

    def _write_key(cls, properties: dict):
        pass

    def _write_url(cls, properties: dict):
        pass
