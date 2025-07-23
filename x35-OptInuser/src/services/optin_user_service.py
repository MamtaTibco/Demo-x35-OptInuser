# src/services/optin_user_service.py
import logging
from datetime import datetime
from typing import Dict, List
from src.models.request_models import SalesforceCustomerPayload, LoyaltyEmailATG, EmailSub, CustomerAccount, Email, Site, RecordType

logger = logging.getLogger(__name__)

def trim(value: str) -> str:
    """Trim whitespace from string values."""
    return value.strip() if value else ""

def format_salesforce_customer_v1(email_sub: EmailSub, lookup_data: Dict) -> SalesforceCustomerPayload:
    """Format customer data for Salesforce API (Version 1)."""
    email = email_sub.currentEmailId
    now_iso = datetime.utcnow().isoformat()

    # Customer Account
    customer_account = CustomerAccount(
        RecordType=RecordType(Name=lookup_data["STERLING_BRAND_CODE"]),
        PersonEmail=email,
        Preferred_Language__c=email_sub.languageCode,
        Primary_Digital_Customer_ID__c=f"{email_sub.brand}{email}",
        LastName=email_sub.lastName,
        FirstName=email_sub.firstName
    )

    # Add phone if channel code is SMS or Both
    if email_sub.channelCode and email_sub.channelCode.upper() in ("S", "B") and email_sub.phone:
        customer_account.PersonMobilePhone = email_sub.phone

    # Email preferences
    emails = [Email(Email_Address__c=email)]

    # Site preferences
    sites = [Site(
        Site_ID__c=lookup_data["TR_US"],
        Website_Site_ID__c=email_sub.siteId or "terrain",
        Email_Preference_Date__c=now_iso,
        Email_Preference_Source__c=f"{email_sub.source} - {email_sub.country}"
    )]

    # SMS preferences
    if email_sub.channelCode and email_sub.channelCode.upper() in ("S", "B"):
        sites[0].SMS_preference__c = False
        sites[0].SMS_Preference_Date__c = now_iso
        sites[0].SMS_Preference_Source__c = f"{email_sub.source} - {email_sub.country}"

    # Content preferences
    if email_sub.contentPreference:
        sites[0].Content_Preference = email_sub.contentPreference

    if email_sub.contentPreferenceCodes and email_sub.contentPreferenceCodes[0]:
        sites[0].Content_Preference_Value__c = email_sub.contentPreferenceCodes[0]
    elif email_sub.contentPreferenceValue:
        sites[0].Content_Preference_Value__c = email_sub.contentPreferenceValue

    return SalesforceCustomerPayload(
        customerAccount=customer_account,
        Emails=emails,
        Sites=sites
    )

def format_salesforce_customer_v2(request: LoyaltyEmailATG, common_data: Dict) -> SalesforceCustomerPayload:
    """Format customer data for Salesforce API (Version 2)."""
    email_sub = request.emailSub
    var_brand_upper = trim(email_sub.brand).upper() if email_sub.brand else ""
    var_source_upper = trim(email_sub.source).upper() if email_sub.source else ""
    var_siteId_upper = trim(email_sub.siteId).upper() if email_sub.siteId else ""

    # Get data from cached lookups
    sterling_a15_brand = common_data.get("STERLING_A15_BRAND", [])
    optin_table_source = common_data.get("OPTIN_DATA", [])
    brand_name_xref = common_data.get("BRAND_NAME_XREF", [])

    # Process RecordType
    optin_site_id = next(
        (item["SITEID"] for item in optin_table_source
         if trim(item["BRAND"]).upper() == var_brand_upper
         and trim(item["SOURCE"]).upper() == var_source_upper),
        email_sub.siteId
    )

    brand_name_xref_item = next(
        (item for item in brand_name_xref
         if trim(item["BRAND_NAME"]).upper() == var_brand_upper),
        None
    )

    if brand_name_xref_item:
        site_id = brand_name_xref_item["STERLING_BRAND_CODE"]
        brand = brand_name_xref_item["STERLING_BRAND_CODE"]
    else:
        site_id = optin_site_id[:2].upper() if optin_site_id else var_brand_upper
        brand = var_brand_upper

    # Get brand name from lookup
    brand_name = next(
        (item["A15_SITE_GROUP"] for item in sterling_a15_brand
         if trim(item["A15_SITEID"]) == site_id),
        brand
    )

    # Customer Account
    customer_account = CustomerAccount(
        RecordType=RecordType(Name=brand_name),
        PersonEmail=email_sub.currentEmailId,
        Preferred_Language__c=email_sub.languageCode,
        Primary_Digital_Customer_ID__c=f"{brand}{email_sub.currentEmailId}",
        LastName=email_sub.lastName,
        FirstName=email_sub.firstName
    )

    # Add phone if channel code is SMS or Both
    if email_sub.channelCode and email_sub.channelCode.upper() in ("S", "B") and email_sub.phone:
        customer_account.PersonMobilePhone = email_sub.phone

    # Emails
    emails = [Email(Email_Address__c=email_sub.currentEmailId)] if email_sub.currentEmailId else []

    # Process Sites
    a15_site_group = next(
        (item["A15_SITE_GROUP"] for item in sterling_a15_brand
         if trim(item["A15_SITEID"]).upper() == var_siteId_upper),
        None
    )

    double_optin_flag = None
    if a15_site_group:
        double_optin_flag = next(
            (item["DOUBLEOPTINFLAG"] for item in optin_table_source
             if trim(item["BRAND"]).upper() == var_brand_upper
             and trim(item["SOURCE"]).upper() == var_source_upper
             and trim(item["SITEID"]).upper() == var_siteId_upper),
            ""
        )
    else:
        double_optin_flag = next(
            (item["DOUBLEOPTINFLAG"] for item in optin_table_source
             if trim(item["BRAND"]).upper() == var_brand_upper
             and trim(item["SOURCE"]).upper() == var_source_upper),
            ""
        )

    site_id = a15_site_group if a15_site_group else next(
        (item["A15_SITE_GROUP"] for item in sterling_a15_brand
         if trim(item["A15_SITEID"]).upper() == trim(optin_site_id).upper()),
        None
    )

    now_iso = datetime.utcnow().isoformat()
    site_data = Site(
        Site_ID__c=site_id,
        Website_Site_ID__c=email_sub.siteId or "terrain",
        Marketing_Eligible__c=True,
        MC_Send_Flag__c=True,
        Email_preference__c=(email_sub.action.upper() == "SUB" and double_optin_flag != "Y")
        if email_sub.channelCode != "S" else None,
        Email_Preference_Date__c=now_iso if email_sub.channelCode in ("B", "E") or not email_sub.channelCode else None
    )

    # Set email preference source
    source_ems = None
    if a15_site_group:
        source_ems = next(
            (item["SOURCE_EMS"] for item in optin_table_source
             if trim(item["BRAND"]).upper() == var_brand_upper
             and trim(item["SOURCE"]).upper() == var_source_upper
             and trim(item["SITEID"]).upper() == var_siteId_upper),
            None
        )
    else:
        source_ems = next(
            (item["SOURCE_EMS"] for item in optin_table_source
             if trim(item["BRAND"]).upper() == var_brand_upper
             and trim(item["SOURCE"]).upper() == var_source_upper),
            None
        )

    if source_ems:
        site_data.Email_Preference_Source__c = source_ems

    # SMS preferences
    if email_sub.channelCode and email_sub.channelCode.upper() in ("S", "B"):
        site_data.SMS_preference__c = False
        site_data.SMS_Preference_Date__c = now_iso
        if source_ems:
            site_data.SMS_Preference_Source__c = source_ems

    # Content preferences
    if email_sub.contentPreference:
        site_data.Content_Preference = email_sub.contentPreference

    if email_sub.contentPreferenceCodes and email_sub.contentPreferenceCodes[0]:
        site_data.Content_Preference_Value__c = email_sub.contentPreferenceCodes[0]
    elif email_sub.contentPreferenceValue:
        site_data.Content_Preference_Value__c = email_sub.contentPreferenceValue

    if (email_sub.channelCode in ("B", "E") or not email_sub.channelCode) and email_sub.contentPreferenceValue:
        site_data.Content_Preference_Date__c = now_iso

    return SalesforceCustomerPayload(
        customerAccount=customer_account,
        Emails=emails,
        Sites=[site_data]
    )