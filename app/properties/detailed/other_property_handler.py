from app.properties.properties_handler import PropertiesHandler


class GetOtherProperties(PropertiesHandler):
    r"""
    Get Other Properties
    """

    application = "other"

    @classmethod
    def get_properties(cls) -> dict:
        return cls._store_property()
