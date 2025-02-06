from pydantic import BaseModel, Field
from typing import Optional

class VerifyPanRequestBody(BaseModel):
    pan: str 
    consent: str 
    reason: str 

class RedirectionConfig(BaseModel):
    redirectUrl: str
    timeout: int

class AdditionalData(BaseModel):
    acno: str
    ifsc: str

class VerifyBankRequestBody(BaseModel):
    redirectionConfig: RedirectionConfig
    additionalData: AdditionalData