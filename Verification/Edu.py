from edupage_api import Edupage
import json


class Edu:
    def __init__(self, user, passw) -> None:
        self.edupage = Edupage()
        self.edupage.login(user, passw, "gympd")

    def check(self, data):
        if data['year'] != '2024/2025':
            return False
        students = self.edupage.get_students()
        for student in students:
            if student.name == data['name']:
                print(student.name)
                return True
            
if __name__ == "__main__":
    with open('/home/zekousek/Documents/Edupage-Verification-Discord/data/data.json', 'r') as file:
        data = json.load(file)
    edu = Edu(data["EDU_LOGIN"], data["EDU_PASSWORD"])
    print(edu.check({
        "name": "Test Test",
        "year": "2024/2025"
    }))
    print(edu.check({
        "name": "Test Test",
        "year": "2023/2024"
    }))
        
