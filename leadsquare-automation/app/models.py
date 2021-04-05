from fastapi import HTTPException
from typing import Optional
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel, Field, validator
from fastapi import Query

class OmnifinReport(BaseModel):
    # from_date: str = Query(..., regex=r"\d{1,2}-\d{1,2}-\d{4}", format="date")
    # to_date: str = Query(..., regex=r"\d{1,2}-\d{1,2}-\d{4}", format="date")
    from_date: str
    to_date: str
    loan_number: str
    receiver_mail_id: str


    @validator('from_date')
    def validateFromDate(cls,v):
        if not v:
            raise HTTPException(status_code=400, detail="From date is missing")

        return v

    @validator('to_date')
    def validateToDate(cls,v):
        if not v:
            raise HTTPException(status_code=400, detail="To date is missing")

        return v

    @validator('loan_number')
    def validatelan(cls,v):
        if not v:
            raise HTTPException(status_code=400, detail="Invalid Loan Number")

        return v

    


class Lead(BaseModel):
    ProspectID: str
    ProspectAutoId: int
    OwnerIdName: str
    mx_Applicant_Type: Optional[str] = ""
    FirstName: str
    LastName: str

    EmailAddress: Optional[str]
    Phone: Optional[str] = ""
    Mobile: Optional[str] = ""
    Latitude: Optional[str] = ""
    Longitude: Optional[str] = ""
    mx_Loan_Amount: Optional[float] = ""
    mx_Loan_Purpose: str
    mx_PAN_No: Optional[str] = ""
    mx_Type_of_Business: Optional[str] = ""
    
    mx_Street1: Optional[str] = ""
    mx_Street2: Optional[str] = ""
    mx_Branch: Optional[str] = ""
    mx_City: Optional[str] = ""
    mx_State: Optional[str] = ""
    mx_Country: Optional[str] = "India"
    mx_Customer_Status: Optional[str] = ""
    mx_DPD: Optional[str] = ""
    mx_NPA_Flag: Optional[str] = ""
    mx_EMI_Amount: Optional[float] = 0
    mx_Balance_Installment: Optional[float] = 0
    mx_Principal_Outstanding: Optional[float] = 0
    mx_Product: Optional[str] = ""
    Notes: Optional[str] = ""
    Origin: Optional[str] = ""
    Source: Optional[str] = ""
    ProspectStage: Optional[str] = ""
    CreatedOn: Optional[str] = ""
    LeadConversionDate: Optional[str] = ""
    mx_Disbursement_Date: Optional[str] = ""
