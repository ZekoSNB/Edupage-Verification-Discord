from Qrcode import Qrcode
from Edu import Edu
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re, os, json


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
            edu_data = self.edu.check(student_data)
            if edu_data['STATUS']:
                print(edu_data)
                print(self.edu.get_class(edu_data))
            else:
                print(edu_data)
        else:
            print('No data found in the QR code')
    
    def verify_web(self, url: str) -> dict:
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
        name = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[1]/div[6]/div[2]').get_attribute('innerHTML')
        year = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[1]/div[11]').get_attribute('innerHTML')
        user_data['NAME'] = name
        user_data['YEAR'] = re.sub(r'[\t\n\.]', '', year).split(' ')[::-1][0]
        driver.quit()
        return user_data

    def get_data(self) -> dict:
        with open(os.path.join(self.BASE_DIR, 'data', 'data.json'), 'r') as f:
            return json.load(f)
        
if __name__ == '__main__':
    V = Verification()
    V.verify('qrcodetest.jpeg')

