from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# print(Group.objects.get(name="Students"))

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class EducationalInstitution(models.Model):
    teachers_list = models.JSONField()
    admins_list = models.JSONField()
    groups_list = models.JSONField()
    courses_list = models.JSONField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    director = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)


class Teacher(models.Model):
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    mail = models.CharField(max_length=255)


class Administrator(models.Model):
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    mail = models.CharField(max_length=255)


class Groups(models.Model):
    courses_list = models.JSONField()
    student_list = models.JSONField()
    description = models.TextField()


class Course(models.Model):
    teachers_list = models.JSONField()
    subject_list = models.JSONField()
    name = models.CharField(max_length=200)
    description = models.TextField()


class Homework(models.Model):
    date = models.DateField(auto_now_add=True)
    discipline = models.CharField(200)
    description = models.TextField()
    task = models.FileField()

class Lesson(models.Model):
    id_homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Student(models.Model):
    marks_list = models.JSONField(default=dict)
    login = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    mail = models.CharField(max_length=255)

class Mark(models.Model):
    id_homework = models.JSONField()
    mark = models.IntegerField()
    description = models.TextField()


class Subject(models.Model):
    name = models.CharField(max_length=255)
    content = models.FileField()


class GroupCourse(models.Model):
    id_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE)
