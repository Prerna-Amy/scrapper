OmnifinScrapperPrerequisites

python 3.6

Selenium

FastAPI

Objective

We want to scrape the data of an online Omnifin site : http://uat.staragrifinance.in:8080/OmniFin/loadLMS.do

LoginPage: get the content of the page

First let’s pass the username and password to login the site

for UserName

admin

for Password

admin@123

After Login we have to click the Credit Management link

Note the structure of  code:

Inside credit management we have to click Report, Inside Report we have to choose 

Inside report type we have to choose Statement of account option.

Provide Loan Number(mandatory field to pass)

From Date(mandatory field to pass)

To Date(mandatory field to pass)

Generate Loan details Report

To click view generate

FastAPI(In fastAPI we have to pass mandatory field)

FromDate---  Date formate(DD-MM-YYYY)
ToDate ---DateFormat(DD-MM-YYYY)
LOAN NUMBER