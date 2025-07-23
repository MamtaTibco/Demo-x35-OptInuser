# src/repositories/lookup_repository.py
from sqlmodel import select
from src.models.salesforce_models import BrandNameXref, SterlingA15Brand, OptinTableSource
from lookup.database import get_lookup_session
from lookup.cache_service import run_select_and_cache


def get_lookup_values(email_sub):
    with get_lookup_session() as session:
        brand_xrefs = session.exec(select(BrandNameXref)).all()
        brand_map = {item.BRAND_NAME: item.STERLING_BRAND_CODE for item in brand_xrefs}

        a15_brands = session.exec(select(SterlingA15Brand)).all()
        site_map = {item.A15_SITEID: item.A15_SITE_GROUP for item in a15_brands}

        optin_data = session.exec(select(OptinTableSource)).all()
        optin_data = [item.dict() for item in optin_data]

        brand_code = brand_map.get(email_sub.brand, "UNKNOWN")
        site_id = f"{brand_code.lower()}-{email_sub.country.lower()}"

        return {
            "STERLING_BRAND_CODE": brand_code,
            "TR_US": site_id,
            "OPTIN_DATA": optin_data,
            "STERLING_A15_BRAND": [{"A15_SITEID": k, "A15_SITE_GROUP": v} for k, v in site_map.items()],
            "BRAND_NAME_XREF": [{"BRAND_NAME": k, "STERLING_BRAND_CODE": v} for k, v in brand_map.items()]
        }