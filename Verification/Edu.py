from edupage_api import Edupage
from edupage_api.exceptions import BadCredentialsException, CaptchaException
import json

# edupage = Edupage()

# with open('/home/zeko/Documents/Edupage-Verification-Discord/data/data.json', 'r') as file:
#     data = json.load(file)

# try:
#     edupage.login(data["EDU_LOGIN"], data["EDU_PASSWORD"], "gympd")
#     print(edupage)
#     print(edupage.get_students())
# except BadCredentialsException:
#     print("Wrong username or password!")
# except CaptchaException:
#     print("Captcha required!")

class Edu:
    def __init__(self, user, passw) -> None:
        self.edupage = Edupage()
        self.edupage.login(user, passw, "gympd")

    def check(self, data):
        if data['year'] != '2024/2025':
            return False
        students = self.edupage.get_students()
        
