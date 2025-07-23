from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class SFTokenSettings(BaseSettings):
    """
    Configuration for Salesforce token settings.
    Automatically loads values from environment variables with the `SF_TOKEN_` prefix.
    """
    model_config = SettingsConfigDict(
        env_prefix="SF_TOKEN_",
        validate_assignment=True,
        extra="forbid",
    )

    client_id: str = Field(
        default="3MVG9y08DauEe.80Y.NnMFYaE0hzhfj6Jd5UjCRhZFY_sb5TYBho674lobm9tsLtVHj9cOORyeB0YaRxT04y1",
        description="Client ID for SF Token",
    )
    client_secret: str = Field(
        default="0FEADEB0FE7390F28DFBB45D029CD4A3EF556F465D4FD8B66D2A8BD29697AF39",
        description="Client Secret for SF Token",
    )
    refresh_token: str = Field(
        default="5Aep861MFU2WGGolEZWzo1m5lk4bqSB_JUXOscpKzPY6fZfw45saL3qdBKC5R.qUDmeOP4wJGIbtqNGMCXTRiDM",
        description="Refresh Token for SF Token",
    )
    salesforce_host: str = Field(
        default="urbn--staging.sandbox.my.salesforce.com",
        description="Salesforce host URL",
    )
    salesforce_create_customer_uri: str = Field(
        default="/services/apexrest/Customers",
        description="Salesforce create customer endpoint URI",
    )
    token_url: str = Field(
        default="https://urbn--staging.sandbox.my.salesforce.com/services/oauth2/token",
        description="Token URL for authentication",
    )
    salesforce_timeout: int = Field(
        default=30,
        description="Salesforce timeout in seconds",
    )