# src/services/salesforce_service.py
import logging
from datetime import datetime
import httpx
from fastapi import HTTPException, status
from typing import Dict
from src.settings.config import Config

logger = logging.getLogger(__name__)

# Token cache
token_cache = {
    "token": None,
    "expires_at": None
}

async def get_salesforce_token() -> str:
    if token_cache["token"] and token_cache["expires_at"] and token_cache["expires_at"] > datetime.now().timestamp():
        return token_cache["token"]

    payload = {
        "grant_type": "refresh_token",
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
        "refresh_token": Config.REFRESH_TOKEN
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(Config.TOKEN_URL, data=payload)
            response.raise_for_status()

            token_data = response.json()
            token_cache["token"] = token_data["access_token"]
            token_cache["expires_at"] = datetime.now().timestamp() + 3600
            return token_data["access_token"]
    except Exception as e:
        logger.error(f"Failed to refresh Salesforce token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "TOKEN_REFRESH_FAILED",
                "code": "500",
                "details": str(e)
            }
        )

async def call_salesforce_api(payload: Dict):
    token = await get_salesforce_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"https://{Config.SALESFORCE_HOST}{Config.SALESFORCE_CREATE_CUSTOMER_URI}"

    async with httpx.AsyncClient(timeout=Config.SALESFORCE_TIMEOUT) as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code >= 400:
        logger.error(response.text)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "error": "SALESFORCE_API_ERROR",
                "code": "502",
                "details": response.text
            }
        )

    return response.json()