from .fastapi import FastAPISettings
from .uvicorn import UvicornSettings
from .sf_token_settings import SFTokenSettings

class Settings:
    """
    Unified settings class combining Base, FastAPI, and Uvicorn settings.
    Provides a single point of access to all configuration.
    """
    def __init__(self):
        self.fastapi = FastAPISettings()
        self.uvicorn = UvicornSettings()
        self.sf_token = SFTokenSettings()

settings = Settings()

__all__ = [
    "settings",
    "Settings",
    "FastAPISettings",
    "UvicornSettings",
    "DBSettings",
    "SFTokenSettings"
]