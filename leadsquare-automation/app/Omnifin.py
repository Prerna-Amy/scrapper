from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException,NoAlertPresentException,InvalidSessionIdException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from models import OmnifinReport
import datetime
from pathlib import Path
from selenium.webdriver.chrome.options import Options  
from dotenv import load_dotenv
chrome_options = Options()  
chrome_options.add_argument("--headless")  
#options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'`

chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--test-type")
chrome_options.add_argument("--start-maximized")

#driver = webdriver.Chrome(ChromeDriverManager().install())

chrome_driver_file_path = '/home/prerna/Documents/tmp/chromedriver'

class OMNIScrapper():

    

    def __init__(self, omnifinReport: OmnifinReport):
        self.driver = webdriver.Chrome(executable_path = chrome_driver_file_path, chrome_options=chrome_options)
        # self.driver = webdriver.Chrome(executable_path = chrome_driver_file_path)
        self.driver.get("http://uat.staragrifinance.in:8080/OmniFin/loadLMS.do")
        self.omnifinReport = omnifinReport
        # self.driver.maximize_window()

    def OMNILogin(self):
        user_name = "60038"
        password = "a"
        email = self.driver.find_element_by_id("userName")
        passwd = self.driver.find_element_by_id("userPassword")
        email.send_keys(user_name)
        passwd.send_keys(password)
        signIn = self.driver.find_element_by_id("loginForm").submit()   
        print("sign in clicked")
        time.sleep(12)
        # self.GenerateReport()

    def acceptAlert(self, alertText):
        try:
            alert = self.driver.switch_to_alert()
            alert.accept()
            return True

        # except (NoAlertPresentException, TimeoutException) as py_ex:
        #     isrunning = 0
        #     print("Alert not present")
        #     self.driver.close()
        #finally:
        #    self.driver.quit()
        except Exception as e:
           return False
    
    def logOutOmni(self):
        # self.driver.find_element_by_partial_link_text('Logout').click()
        # time.sleep(random.randint(5,15))
        self.driver.close()


    def GenerateReport(self):
        try:
            credit_mgmt = self.driver.find_element_by_link_text("CREDIT MANAGEMENT").click()
            print("credit management selected")
            time.sleep(10)
            
            print("start working on reports")
            # report_part = self.driver.find_element_by_xpath("//a[contains(text(),'REPORTS')]")
            
            frame_sets = self.driver.find_elements_by_xpath('.//frame')
            # print("frame_sets=============", len(frame_sets))
            # for i in frame_sets:
            #     print("src=======", i.get_attribute('src'))
            self.driver.switch_to_frame("leftContant")
            print("switched to left content frame")
            #report_elements = self.driver.find_elements_by_tag_name('li h3')
            report_option = self.driver.find_elements_by_tag_name('li h3 a')
            print("report_elements=============", len(report_option))
            for i in report_option:
                print("element details===========", i.get_attribute('innerText'))
                if 'REPORTS' in i.get_attribute('innerText'):
                    print("tag found===========", i)

                    i.click()

                    
                    break
            time.sleep(10)
            print("Reports clicked")  
        except InvalidSessionIdException as e:
            # pass
            print("exception report=============", e)
        # Find your dropdown element by the following, finds the element in the dropdown named BRA

    def Dropdown_Element(self):
        #WebDriverWait(self.driver, 12).until(EC.element_to_be_clickable(By.LINK_TEXT, "Reports")).click()
        #time.sleep(2)
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Reports")))
            element.click()
            #time.sleep(20)
        except TimeoutException as e:
            isrunning = 0
            print("element timeout==========",str(e))
            self.driver.close()

    def Report_selection(self):
        try:
            self.driver.switch_to_default_content()
            # frame_sets = self.driver.find_elements_by_xpath('.//frame')
            # print("number of frames=============",len(frame_sets))
            # for i in frame_sets:
            #     print(i)
            #self.driver.implicitly_wait(10)
            #self.driver.switch_to_frame('content')
            #self.driver.implicitly_wait(10)
            #self.driver.find_element(By.TAG_NAME("select"))
        #li_element = self.driver.find_element(By.NAME("reportName"))
            WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"content")))
            li_element = Select(self.driver.find_element_by_name('reportName'))
            for opt in li_element.options:
                li_element.select_by_visible_text('Statement of Account')
            #time.sleep(20)
        except TimeoutException as e:
            isrunning=0
            print("Exception thrown.......",str(e))
            self.driver.close()
        except Exception as e:
            print("resport selection exception",e)


    def datevaluefrom(self):
        try:
            self.driver.switch_to_default_content()
            # frame_sets = self.driver.find_elements_by_xpath('.//frame')
            # print("number of frames=============",len(frame_sets))
            # for i in frame_sets:
            #     print(i)
        #self.driver.implicitly_wait(10)
            #WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name='content']")))
            self.driver.switch_to_frame('content')
        #driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe")
        #driver.get("https://demoqa.com/automation-practice-form")
            datefield = self.driver.find_element_by_id("dateFromD")
            datefield.click()
            select = Select(self.driver.find_element_by_class_name("ui-datepicker-month"))
        # months.click()
        # D-M-Y 01-03-2010
            from_date = datetime.datetime.strptime(self.omnifinReport.from_date, '%d-%m-%Y')
            for op in select.options:
                print("options from month =============", op.text)
                if op.text == from_date.strftime('%b'):
                    select.select_by_visible_text(op.text)
                    #time.sleep(5)
                    break
            #self.driver.implicitly_wait(10)

            select1 = Select(self.driver.find_element_by_class_name("ui-datepicker-year"))
        # months.click()
        # D-M-Y 01-03-2010
            from_date = datetime.datetime.strptime(self.omnifinReport.from_date, '%d-%m-%Y')
            for op in select1.options:
                print("options from year=============", op.text)
                if op.text == from_date.strftime('%Y'):
                    select1.select_by_visible_text(op.text)
                    #time.sleep(5)
                    break
                    #time.sleep(10)
        #months = self.driver.find_element_by_class_name("ui-datepicker-month")
        #months.click()
        #months.send_keys(self.omnifinReport.from_date)
        #years = self.driver.find_element_by_class_name("ui-datepicker-year")
        #years.click()
        #years.send_keys(self.omnifinReport.from_date)
        #select1 = Select(self.driver.find_element_by_class_name('ui-datepicker-year'))
        #days = self.driver.find_elements_by_css_selector("a[class*='ui-state-default']")
        #days.click()
        #days.send_keys(self.omnifinReport.from_date)
        #for day in days:
        #    if day.text == from_date.strftime('%d'):
        #        day.click()
        #        break
            days = self.driver.find_element_by_css_selector("a[class*='ui-state-default']")
        #days = self.driver.find_element_by_class_name('ui-datepicker-calendar')
            days.click()
            from_date = datetime.datetime.strptime(self.omnifinReport.from_date, '%d-%m-%Y')
            days.send_keys(self.omnifinReport.from_date)
            return True
        except TimeoutException as e:
            isrunning=0
            print("from time out==========",str(e))
            return False
        except Exception as e:
            print("Exception=============", e)
            return False


    def datevalueTo(self):
        try:

            self.driver.switch_to_default_content()
            #WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name='content']")))
            self.driver.switch_to_frame('content')
            datefield = self.driver.find_element_by_id("dateToD")
            datefield.click()
        # months = self.driver.find_element_by_class_name("ui-datepicker-month")
            select1 = Select(self.driver.find_element_by_class_name("ui-datepicker-month"))
        # months.click()
        # D-M-Y 01-03-2010
            to_date = datetime.datetime.strptime(self.omnifinReport.to_date, '%d-%m-%Y')
            for op in select1.options:
                print("options months=============", op.text)
                if op.text == to_date.strftime('%b'):
                    select1.select_by_visible_text(op.text)
                    print("selected month")
                    #time.sleep(5)
                    break
            #time.sleep(10)



        #months = self.driver.find_element_by_xpath("//select[@class='ui-datepicker-month']").click()

        #months.send_keys(self.omnifinReport.to_date)
        #years = self.driver.find_element_by_xpath("//select[@class='ui-datepicker-year']").click()
            select2 = Select(self.driver.find_element_by_class_name("ui-datepicker-year"))
            to_date = datetime.datetime.strptime(self.omnifinReport.to_date, '%d-%m-%Y')
            for op in select2.options:
                print("options years=============", op.text)
                if op.text == to_date.strftime('%Y'):
                    select2.select_by_visible_text(op.text)
                    print("selected year")
                    #time.sleep(5)
                    break
            #time.sleep(10)
        #years.click()
        #years.send_keys(self.omnifinReport.to_date)

        #select = Select(self.driver.find_element_by_class_name("ui-datepicker-month"))
        #for op in select.options:
        #    select.select_by_value(self.omnifinReport.to_date)
        #    time.sleep(5)
        #    break
        
    
        #select1 = Select(self.driver.find_element_by_class_name("ui-datepicker-year")).send_keys(self.omnifinReport.to_date)
        #for opt in select1.options:
        #        select1.select_by_value(self.omnifinReport.to_date)
        #        time.sleep(5)
        #        break
        #days = self.driver.find_elements_by_css_selector("a[class*='ui-state-default']")
        #to_date = datetime.datetime.strptime(self.omnifinReport.to_date, '%d-%m-%Y')
        #days.click()
            days = self.driver.find_element_by_css_selector("a[class*='ui-state-default']")
        #days = self.driver.find_element_by_class_name('ui-datepicker-calendar')
            days.click()
            to_date = datetime.datetime.strptime(self.omnifinReport.to_date, '%d-%m-%Y')
            days.send_keys(self.omnifinReport.to_date)

        #for day in days:
        #    if day.text == to_date.strftime('%d'):
        #        day.click()
        #        break
            return True
        except TimeoutException as e:
            isrunning = 0
            print("to date time out======",str(e))
            return False
        except Exception as e:
            print("Exception=============", e)
            return False
    

    def LoanDetails(self):
        try:
            main_window = self.driver.current_window_handle
            element1 = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "sp_loan2")))
            element1.click()

            # elements =  WebDriverWait(self.driver, 20).until(
            #         EC.visibility_of_all_elements_located((By.NAME,"specificLoanButton")))
            

            for handle in self.driver.window_handles: 
                if handle != main_window: 
                    loan_details_page = handle
                    print("loan details page found=============")

            if loan_details_page:
                self.driver.switch_to.window(loan_details_page) 
                #loan_number = "LXWRHMUM0000001"
                #loan_number = loannumber
                # element1 = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.NAME, "lovDesc")))
                # element1.send_keys(loan_number)
                time.sleep(15)
                self.driver.find_element_by_id('lovCode').send_keys(self.omnifinReport.loan_number)
                print("loan number added=============")
                #self.driver.find_element_by_class_name('searchLovButton').click()
                element1 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "searchLovButton")))
                element1.click()
                print("clicked search button=========")
                element2 = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "selectRadioBtn")))
                element2.click()
                #time.sleep(10)
                self.driver.switch_to.window(main_window)


            #elements = Select(self.driver.find_elements_by_id('p1'))


            #expected_value = "LXWRHMUM0000001"

            # for element in elements:
            #     if element.text == "LXWRHMUM0000001":
            #         element.click()
            #         time.sleep(20)
            #         break
            return True
        except TimeoutException as e:
            isrunning = 0
            print("Timeout.....",str(e))
            return False
        except Exception as e:
            print("Exception=============", e)
            return False

    

    def Generate_PDF(self):

        
            #element1 = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.NAME, "mybutton")))
            #element1.click()


        self.driver.find_element_by_name(" mybutton").click()
        #ele = self.driver.find_element(By.CLASS_NAME,'topformbutton3').click()
        #searchBar = self.driver.find_elements_by_css_selector('.button.first-in-line').click()
        #except TimeoutException as e:
            #isrunning = 0
            #print("generate pdf timeout==========",str(e))



    def Send_Mail(self):
        mail_content = '''Loan details file
        '''

        sender_address = 'prerna26may@gmail.com'
        sender_pass = 'Amy 123$%'
        receiver_address = self.omnifinReport.receiver_mail_id
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Statement of account'
        message.attach(MIMEText(mail_content, 'plain'))
        attach_file_name = 'statement_of_account.pdf'
        attach_file = open(attach_file_name, 'rb') 
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) 
        payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        message.attach(payload)
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(sender_address, sender_pass) 
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')
        return True
  



        
        

#loannumber = 'LSLAPMUM0000002'
# omnifinReport = OmnifinReport(from_date="01-01-2010", to_date="03-02-2020", loan_number="LXWRHMUM0000001", receiver_mail_id="prerna26may@gmail.com")

# obj = OMNIScrapper(omnifinReport)
# obj.OMNILogin()
# alertShown = obj.acceptAlert('Your Last Session was not Properly Terminated. Do you wish to Login Again ?')
# print("alertShown============", alertShown)
# if alertShown == True:
#     obj.acceptAlert('Your Last Session was not Properly Terminated. Do you wish to Login Again ?')
#     # time.sleep(5)
#     # obj.OMNILogin()

# time.sleep(15)
# obj.GenerateReport()
# obj.Dropdown_Element()
# obj.Report_selection()
#obj.LoanDetails()
#obj.datevaluefrom()
#obj.datevalueTo()
#obj.Generate_PDF()
#obj.Send_Mail()
#obj.from_date_picker()
#obj.to_date_picker()
#obj.ReportSelection()
# time.sleep(5)

# obj.logOutOmni()



