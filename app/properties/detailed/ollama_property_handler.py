from app.properties.properties_handler import PropertiesHandler


class GetOllamaProperties(PropertiesHandler):
    r"""
    Get Ollama Properties
    """

    application = "ollama"

    @classmethod
    def get_properties(cls) -> dict:
        return cls._store_property()
