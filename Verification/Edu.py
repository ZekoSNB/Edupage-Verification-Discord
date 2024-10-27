from edupage_api import Edupage


# A class to interact with the Edupage API for student verification and class retrieval.
# Attributes:
# -----------
# edupage : Edupage
#     An instance of the Edupage class used to interact with the Edupage API.
# Methods:
# --------
# __init__(user: str, passw: str) -> None
#     Initializes the Edu class with user credentials and logs into Edupage.
# check(data: dict) -> dict
#     Checks if the provided student data matches a student in the Edupage system.
# get_class(student: dict) -> str
#     Retrieves the class name for a given student based on their class ID.

class Edu:
    def __init__(self, user: str, passw: str) -> None:
        self.edupage = Edupage()
        self.edupage.login(user, passw, "gympd")

    def check(self, data: dict) -> dict:
        if data['YEAR'] != '2024/2025':
            return {
                "STATUS": False,
                "ERROR": "Školský rok sa nezhoduje"
            }
        students = self.edupage.get_students()
        for student in students:

            if student.name == data['NAME']:
                return {
                    "STATUS": True,
                    'NAME': student.name,
                    "ID": student.person_id,
                    "CLASS_ID": student.class_id,
                    "CLASS": self.get_class(student.class_id)
                }
        return {
            "STATUS": False,
            "ERROR": "Meno sa nenašlo"
        }

    def get_class(self, student_class_id: int) -> str:
        classes = self.edupage.get_classes()
        for class_ in classes:
            if class_.class_id == student_class_id:
                return class_.name
            

    
