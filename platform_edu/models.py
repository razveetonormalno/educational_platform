from django.db import models
from django.contrib.auth.models import User


def create_new_ei(id_adm, name_adm, name_ei, phone_ei):
    admin = {
        id_adm: name_adm,
    }
    new_ei = EducationalInstitution.objects.create(admins_list=admin,
                                                   name=name_ei,
                                                   phone=phone_ei,)
    new_ei.save()
    id_ei = new_ei.pk
    adm = Administrator.objects.get(login=name_adm)
    adm.ei_id = id_ei
    adm.save()
    return new_ei, adm

def create_new_adm(login, password, surname, name, patronymic, phone, mail, adm):
    new_adm = Administrator.objects.create(login=login, password=password, surname=surname, name=name,
                                           patronymic=patronymic, phone=phone, mail=mail, adm_id=adm)
    new_adm.save()
    id_adm = new_adm.pk
    return id_adm, login

def create_ei():
    adm_data = ('some_adm', '12345edu', 'some', 'some', 'some',
                '89649643213', 'renwok22@gmail.com', 3)
    new_admin = create_new_adm(*adm_data)
    create_new_ei(*new_admin, "First EI", '89649793937')

class EducationalInstitution(models.Model):
    teachers_list = models.JSONField(default=dict)
    admins_list = models.JSONField()
    groups_list = models.JSONField(default=dict)
    courses_list = models.JSONField(default=dict)
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    director = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=11)


class Teacher(models.Model):
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    mail = models.CharField(max_length=255)

    teach = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

class Administrator(models.Model):
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    mail = models.CharField(max_length=255)

    ei_id = models.IntegerField(default=-1)
    adm = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

class Groups(models.Model):
    courses_list = models.JSONField(default=dict)
    student_list = models.JSONField()
    teachers_list = models.JSONField(default=dict)
    description = models.CharField(unique=True)

class Course(models.Model):
    teachers_list = models.JSONField()
    subject_list = models.JSONField()
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

class Homework(models.Model):
    date = models.DateField(auto_now_add=True)
    discipline = models.CharField(max_length=200)
    description = models.TextField()
    task = models.FileField()

class Lesson(models.Model):
    id_homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    id_group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    id_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    status = models.BooleanField()
    discipine = models.CharField(max_length=100)
    description = models.TextField()

class Student(models.Model):
    marks_list = models.JSONField(default=dict)
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    mail = models.CharField(max_length=255)

    stud = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

class Mark(models.Model):
    id_homework = models.JSONField()
    mark = models.IntegerField()
    description = models.TextField()

class Subject(models.Model):
    name = models.CharField(max_length=255)
    content = models.FileField()

class GroupCourse(models.Model):
    id_group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE)
