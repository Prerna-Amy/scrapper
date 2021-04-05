from typing import Optional,Dict
from pydantic import BaseModel,Field
from fastapi import FastAPI, Query, File, UploadFile,status,Response,Request,HTTPException
from uuid import UUID
import uvicorn
from datetime import date,datetime
from fastapi import HTTPException,Query
#from app_Omnifinn import OMNIScrapper
from Omnifin import OMNIScrapper
from datetime import date
from uuid import UUID
from selenium.webdriver.chrome.options import Options  
import time
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse


app = FastAPI()



class OmnifinReport():
    def __init__(self, from_date, to_date, loan_number, receiver_mail_id):
        self.from_date = from_date
        self.to_date = to_date
        self.loan_number = loan_number
        self.receiver_mail_id = receiver_mail_id



@app.get("/omnifin/soa")
async def DefineAccount(from_date: str, to_date: str, loan_number: str, receiver_mail_id: str):
    try:

        message = ""
    

                
        omnifinReport = OmnifinReport(from_date=from_date, to_date=to_date, loan_number=loan_number, receiver_mail_id=receiver_mail_id)
    # print("omnifinreport obj=============", omnifinReport)


        obj = OMNIScrapper(omnifinReport)
        obj.OMNILogin()
        alertShown = obj.acceptAlert('Your Last Session was not Properly Terminated. Do you wish to Login Again ?')
        print("alertShown============", alertShown)
        if alertShown == True:
            obj.acceptAlert('Your Last Session was not Properly Terminated. Do you wish to Login Again ?')
        time.sleep(15)
        obj.GenerateReport()
        print("generate report============")
        obj.Dropdown_Element()
        print("drop down element============")
        obj.Report_selection()
        print("report selection============")
        loandata = obj.LoanDetails()
        if loandata == False:
            message = "Invalid loan number"
            print("invalid loan details=======") 
            raise HTTPException(status_code=404,detail=message)
        # return {"loan data": loandata}
        fromdate = obj.datevaluefrom()
        if fromdate == False:
            message = "Invalid From date"
            print("invalid from date============")
            raise HTTPException(status_code=404,detail=message)
        # return {"fromdate": fromdate}
        todate = obj.datevalueTo()
        if todate == False:
            message = "Invalid To Date"
            print("Invalid to date============")
            raise HTTPException(status_code=404,detail=message)
        # return {"todate": todate}
        obj.Generate_PDF()
        print("pdf generated==========")
        sendmail = obj.Send_Mail()   
        if sendmail == True:
            message = "mail sent"
            print("mail sent successfully============")  
            raise HTTPException(status_code=200,detail=message)


    except:
        raise HTTPException(status_code=404,detail=message)



    




 



