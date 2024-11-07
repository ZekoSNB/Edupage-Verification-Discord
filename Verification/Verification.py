from Verification.Qrcode import Qrcode
from Verification.Edu import Edu
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re, os, json

 
# A class to handle the verification of student data using QR codes and Edupage API.
# Attributes:
# -----------
# BASE_DIR : str
#     The base directory path of the project.
# edu_data : dict
#     The educational data containing login credentials.
# edu : Edu
#     An instance of the Edu class used to interact with the Edupage API.
# Methods:
# --------
# __init__() -> None
#     Initializes the Verification class, sets the base directory, retrieves educational data, and initializes the Edu instance.
# verify(image: str) -> dict
#     Verifies the student data by reading a QR code from the given image and checking it against the Edupage system.
# verify_web(url: str) -> dict
#     Verifies the student data by fetching information from the provided URL.


class Verification():

    def __init__(self) -> None:
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.edu_data = self.get_data()
        self.edu = Edu(self.edu_data['EDU_LOGIN'], self.edu_data['EDU_PASSWORD'])

    def verify(self, image: str) -> None:
        Qr = Qrcode()
        image_path = os.path.join(self.BASE_DIR, 'images', image)
        Qr_data = Qr.read(image_path)
        if Qr_data:
            student_data = self.verify_web(Qr_data)

            if student_data is None:
                return {
                    "STATUS": False,
                    "ERROR": "Invalid URL"
                }
            
            return self.edu.check(student_data)
        else:
            return {
                "STATUS": False,
                "ERROR": "QR Code not found"
            } 
    
    def verify_web(self, url: str) -> dict:
        try:
            user_data = {
                "NAME": "",
                "YEAR": ""
            }
            options = Options()
            options.add_argument('--headless=new')
            chrome_driver = os.path.join(self.BASE_DIR, 'data', 'chromedriver')
            service = Service(chrome_driver)
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)
            user_data['NAME'] = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[1]/div[6]/div[2]').get_attribute('innerHTML')
            year = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[1]/div[11]').get_attribute('innerHTML')
            user_data['YEAR'] = re.sub(r'[\t\n\.]', '', year).split(' ')[::-1][0]
            driver.quit()
            
            return user_data
        except Exception as e:
            return None

    def get_data(self) -> dict:
        with open(os.path.join(self.BASE_DIR, 'data', 'data.json'), 'r') as f:
            return json.load(f)
