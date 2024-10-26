from Qrcode import Qrcode
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re


class Verification():
        
    def verify(self, image):
        Qr = Qrcode()
        Qr_data = Qr.read(image)
        if Qr_data:
            self.verify_web(Qr_data)
    
    def verify_web(self, url):
        user_data = {
            "name": "",
            "year": ""
        }
        options = Options()
        options.add_argument('--headless=new')
        service = Service('/home/zeko/Documents/Edupage-Verification-Discord/data/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        name = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[1]/div[6]/div[2]').get_attribute('innerHTML')
        year = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/div[1]/div[11]').get_attribute('innerHTML')
        user_data['name'] = name
        user_data['year'] = re.sub(r'[\t\n\.]', '', year).split(' ')[::-1][0]
        print(user_data)
        driver.quit()


if __name__ == '__main__':
    V = Verification()
    V.verify('/home/zeko/Documents/Edupage-Verification-Discord/data/download.png')
    V.verify('/home/zeko/Documents/Edupage-Verification-Discord/data/qrcodetest.png')
    V.verify('/home/zeko/Documents/Edupage-Verification-Discord/data/samkotest.jpeg')
    V.verify('/home/zeko/Documents/Edupage-Verification-Discord/data/radko.jpeg')