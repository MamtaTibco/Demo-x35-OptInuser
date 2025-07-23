from fastapi import APIRouter, HTTPException, Path, status
from pydantic import ValidationError
import logging
import json
from src.models.request_models import InputRoot
from src.services.optin_user_service import format_salesforce_customer_v1, format_salesforce_customer_v2
from src.repositories.lookup_repository import get_lookup_values
from src.services.salesforce_service import call_salesforce_api

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/optin-user/{version}")
async def optin_user(
        version: str = Path(..., description="API version (e.g., V4)"),
        input_data: InputRoot = None
):
    if version.upper() not in ["V4"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "INVALID_VERSION", "code": "400"}
        )

    try:
        if not input_data or not input_data.loyaltyEmailATG or not input_data.loyaltyEmailATG.emailSub:
            raise HTTPException(status_code=400, detail="Invalid input data")

        email_sub = input_data.loyaltyEmailATG.emailSub
        email_sub.version = version

        # Ensure required fields have defaults
        email_sub.brand = email_sub.brand or "TR"
        email_sub.country = email_sub.country or "US"
        email_sub.source = email_sub.source or "Signup"

        lookup = get_lookup_values(email_sub)

        if version.upper() == "V4":
            payload = format_salesforce_customer_v1(email_sub, lookup)
        else:
            payload = format_salesforce_customer_v2(input_data.loyaltyEmailATG, lookup)

        payload_dict = payload.dict()
        logger.info(f"Formatted payload: {json.dumps(payload_dict)}")

        response = await call_salesforce_api(payload_dict)
        return {"status": "OK"}

    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "VALIDATION_ERROR", "code": "400", "details": str(e)}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "OPTINUSER_FAILED", "code": "500", "details": str(e)}
        )