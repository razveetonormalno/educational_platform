import json
from .models import *

def create_student(login, password, surname, name, patronymic, phone, mail, stud_id):
    student = Student(login=login, password=password, surname=surname, name=name,
                      patronymic=patronymic, phone=phone, mail=mail, stud_id=stud_id)
    return student