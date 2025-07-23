from . import settings

class Config:
    SALESFORCE_HOST = settings.sf_token.salesforce_host
    SALESFORCE_CREATE_CUSTOMER_URI = settings.sf_token.salesforce_create_customer_uri
    SALESFORCE_TIMEOUT = settings.sf_token.salesforce_timeout
    CLIENT_ID = settings.sf_token.client_id
    CLIENT_SECRET = settings.sf_token.client_secret
    REFRESH_TOKEN = settings.sf_token.refresh_token
    TOKEN_URL = settings.sf_token.token_url
