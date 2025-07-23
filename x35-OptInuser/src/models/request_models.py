# src/models/request_models.py
from pydantic import BaseModel
from typing import Optional, List

class RecordType(BaseModel):
    Name: str

class CustomerAccount(BaseModel):
    RecordType: RecordType
    PersonEmail: str
    Preferred_Language__c: Optional[str] = None
    Ecometry_Migration__c: bool = True
    Primary_Digital_Customer_ID__c: str
    MC_Send_Flag__c: bool = True
    LastName: Optional[str] = None
    FirstName: Optional[str] = None
    PersonMobilePhone: Optional[str] = None

class Email(BaseModel):
    Email_Address__c: str
    Current_Email__c: str = "true"
    MC_Send_Flag__c: bool = True

class Site(BaseModel):
    Site_ID__c: str
    Website_Site_ID__c: str
    Marketing_Eligible__c: bool = True
    MC_Send_Flag__c: bool = True
    Email_preference__c: bool = True
    Email_Preference_Date__c: str
    Email_Preference_Source__c: str
    SMS_preference__c: Optional[bool] = None
    SMS_Preference_Date__c: Optional[str] = None
    SMS_Preference_Source__c: Optional[str] = None
    Content_Preference: Optional[str] = None
    Content_Preference_Value__c: Optional[str] = None
    Content_Preference_Date__c: Optional[str] = None

class SalesforceCustomerPayload(BaseModel):
    customerAccount: CustomerAccount
    Emails: List[Email]
    Sites: List[Site]

class EmailSub(BaseModel):
    brand: Optional[str] = None
    currentEmailId: str
    signUpFlag: Optional[str] = None
    sendEmailCode: Optional[str] = None
    action: Optional[str] = None
    source: Optional[str] = None
    listName: Optional[str] = None
    languageCode: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    siteId: Optional[str] = None
    channelCode: Optional[str] = None
    version: Optional[str] = None
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    phone: Optional[str] = None
    contentPreference: Optional[str] = None
    contentPreferenceCodes: Optional[List[str]] = None
    contentPreferenceValue: Optional[str] = None

class LoyaltyEmailATG(BaseModel):
    emailSub: EmailSub

class InputRoot(BaseModel):
    loyaltyEmailATG: LoyaltyEmailATG