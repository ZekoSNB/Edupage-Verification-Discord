from edupage_api import Edupage
import json, os, datetime

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
                print(student.class_id)
                return {
                    "STATUS": True,
                    "ID": student.person_id,
                    "CLASS_ID": student.class_id
                }
        return False

    def get_class(self, student):
        classes = self.edupage.get_classes()
        for class_ in classes:
            if class_.class_id == student['CLASS_ID']:
                return class_.name
            

if __name__ == "__main__":
    file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'data', 'data.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    edu = Edu(data["EDU_LOGIN"], data["EDU_PASSWORD"])
    
