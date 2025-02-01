from app.properties.properties_handler import PropertiesHandler


class GetSparkProperties(PropertiesHandler):
    r"""
    Get Spark Properties
    """

    application = "spark"

    @classmethod
    def get_properties(cls) -> dict:
        return cls._store_property()
