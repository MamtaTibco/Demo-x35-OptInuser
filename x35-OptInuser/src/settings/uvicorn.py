from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class UvicornSettings(BaseSettings):
    """
    Configuration for Uvicorn server settings.

    Automatically loads values from environment variables with the `UVICORN_` prefix.
    Defaults are provided for all settings, ensuring that the server runs even if
    no environment variables are explicitly set.
    """

    model_config = SettingsConfigDict(
        env_prefix="UVICORN_",
        validate_assignment=True,
        extra="forbid",
    )

    access_log: bool = Field(
        default=True,
        description="Enable or disable Uvicorn's access logs.",
    )
    backlog: int = Field(
        default=2048,
        description="Maximum number of connections that can be queued by the server.",
    )
    http: str = Field(
        default="auto",
        description="HTTP protocol implementation to use. 'auto' selects the best available.",
    )
    keep_alive: int = Field(
        default=5, description="Keep-alive timeout in seconds for HTTP connections."
    )
    log_level: str = Field(
        default="info",
        description="Logging level for Uvicorn (e.g., 'info', 'debug', 'warning').",
    )
    loop: str = Field(
        default="auto",
        description="Event loop implementation. 'auto' selects the best available.",
    )
    max_concurrency: int = Field(
        default=1000,
        description="Maximum number of concurrent requests handled by Uvicorn.",
    )
    port: int = Field(
        default=8080, description="Port number on which the Uvicorn server will listen."
    )
    proxy_headers: bool = Field(
        default=True,
        description="Enable or disable the handling of proxy headers (e.g., X-Forwarded-For).",
    )
    reload: bool = Field(
        default=False,
        description="Enable or disable auto-reloading when code changes. Recommended only in development.",
    )
    server_header: bool = Field(
        default=False,
        description="Include or exclude the 'Server' header in HTTP responses.",
    )
    workers: int = Field(
        default=1,
        description=(
            "Number of worker processes. Use 1 in containerized environments like Kubernetes "
            "where horizontal scaling is preferred."
        ),
    )
