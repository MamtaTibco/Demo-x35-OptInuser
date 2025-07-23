from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class FastAPISettings(BaseSettings):
    """
    Configuration for FastAPI application settings.

    Automatically loads values from environment variables with the `FASTAPI_` prefix.
    Defaults are provided for all settings, ensuring functionality even if
    no environment variables are explicitly set.
    """

    model_config = SettingsConfigDict(
        env_prefix="FASTAPI_",
        validate_assignment=True,
        extra="forbid",
    )

    enable_docs: bool = Field(
        default=True,
        description="Enable or disable FastAPI documentation endpoints (/docs and /redoc).",
    )
