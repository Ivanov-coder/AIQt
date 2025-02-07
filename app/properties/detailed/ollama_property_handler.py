from app.properties.properties_handler import PropertiesHandler


class GetOllamaProperties(PropertiesHandler):
    r"""
    Get Ollama Properties
    """

    application = "ollama"

    def get_property(self):
        return super().get_properties()