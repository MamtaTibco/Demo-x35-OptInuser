# src/models/salesforce_models.py
from sqlmodel import SQLModel, Field

class BrandNameXref(SQLModel, table=True):
    __tablename__ = "BRAND_NAME_XREF"
    __table_args__ = {'extend_existing': True}
    BRAND_NAME: str = Field(primary_key=True)
    STERLING_BRAND_CODE: str

class SterlingA15Brand(SQLModel, table=True):
    __tablename__ = "STERLING_A15_BRAND"
    __table_args__ = {'extend_existing': True}
    A15_SITEID: str = Field(primary_key=True)
    A15_SITE_GROUP: str

class OptinTableSource(SQLModel, table=True):
    __tablename__ = "OPTINTABLE_SOURCE"
    __table_args__ = {'extend_existing': True}
    BRAND: str = Field(primary_key=True)
    SOURCE: str = Field(primary_key=True)
    SITEID: str
    SOURCE_EMS: str
    DOUBLEOPTINFLAG: str