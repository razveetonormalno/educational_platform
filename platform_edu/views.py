from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseServerError

import platform_edu.models
from .forms import UserForm, GroupAdd, HomeWork
from .models import *
from django.contrib.auth.models import Group
from .custom import *
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from .creator import *


def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
            return False

    return user_passes_test(in_groups)

@group_required('Teachers', 'Students')
@login_required
def timetable(request):
    user = User.objects.get(username=request.user.username)
    group = user.groups.all()

    title = "Расписание"
    data = {}
    content = tuple()
    if "Students" in str(group):
        print("This is a student!")
        data = get_data("Students")

        student = Student.objects.get(login=request.user.username)
        students_group = Groups.objects.in_bulk()

        group_number = None
        for group in students_group:
            if str(student.pk) in students_group[group].student_list:
                group_number = students_group[group].description
                data['roomId'] = get_room_(group_number)
                break

        table_content = get_for_student(group_number)
        data['table'] = table_content

        content = ("Добрый вечер", "Я Студент!", f"Группа {group_number}")
    elif "Teachers" in str(group):
        print("This is a teacher!")
        data = get_data("Teachers")

        teacher = Teacher.objects.get(login=request.user.username)
        table_content, group_now = get_for_teacher(str(teacher.pk))
        data['table'] = table_content
        data['ready'] = group_now

        content = ("Добрый вечер", "Я Учитель!")

    data['title'] = title
    data['content'] = content

    return render(request, 'timetable.html', context=data)

@group_required('Teachers', 'Students')
@login_required
def homework(request):
    user = User.objects.get(username=request.user.username)
    group = user.groups.all()

    if "Students" in str(group):
        print("This is a student!")
        data = get_data("Students")

    else:
        print("This is a teacher!")
        data = get_data("Teachers")

        teacher = Teacher.objects.get(login=request.user.username)
        lessons = Lesson.objects.filter(id_teacher_id=teacher.pk)

        group_list = []

        for less in lessons:
            gr = Groups.objects.get(id=less.id_group_id)
            if gr.description not in [i[0] for i in group_list]:
                group_list.append((gr.description, gr.pk))

        data['group_list'] = group_list

    data['title'] = "Домашние задания"

    return render(request, 'teacher/group_homework.html', context=data)

@group_required('Teachers')
@login_required
def view_homework(request, group_id):
    lessons = Lesson.objects.filter(id_group_id=group_id)

    data = get_data("Teachers")
    data['title'] = "Д/з"
    data['homeworks'] = []

    for lesson in lessons:
        home_work = Homework.objects.get(id=lesson.id_homework_id)
        data['homeworks'].append((home_work.pk, home_work.discipline, home_work.date))

    return render(request, "teacher/view_homework.html", context=data)

@group_required('Teachers')
@login_required
def choose_homework(request, group_id, homework_id):
    data = get_data("Teachers")
    data['title'] = "Д/з"
    data['homeworks'] = []

    group = Groups.objects.get(id=group_id)
    for i in group.student_list:
        stud = Student.objects.get(id=i)
        name = f"{stud.surname} {stud.name} {stud.patronymic}"
        data['homeworks'].append((i, name))

    return render(request, "teacher/choose.html")


@group_required('Teachers')
@login_required
def open_homework(request, group_id, homework_id, student_id):
    data = get_data("Teachers")
    data['title'] = "Д/з"
    data['homeworks'] = []
    pass
    # return render(request, "teacher/choose.html", context=data)

@group_required('Teachers')
@login_required
def add_homework(request, group_id=None):
    data = get_data("Teachers")
    data['title'] = "Задать домашнее задание"
    print(str(request.path).split('/')[-1])
    if request.method == "POST":
        group_id = str(request.path).split('/')[-1]
        print("IN POST >>>", request.GET)
        data['form'] = HomeWork(request.POST, request.FILES)
        if data['form'].is_valid():
            if request.POST.get('discipline') and request.POST.get('description') and request.FILES:
                discipline = request.POST.get('discipline')
                description = request.POST.get('description')
                task = request.FILES['task']
                print(">>>>>>>>", discipline)
                print(">>>>>>>>", description)
                print(">>>>>>>>", task)
                try:
                    home_work = Homework(discipline=discipline, description=description, task=task)
                    home_work.save()
                except Exception as e:
                    print(e)
                    home_work.delete()
                    raise e

                gr = Groups.objects.get(description=group_id)
                teacher = Teacher.objects.get(login=request.user.username)

                try:
                    less = Lesson(id_group_id=gr.pk, id_homework_id=home_work.pk,
                                  description=description, discipine=discipline,
                                  id_teacher_id=teacher.pk, status=True)
                    less.save()
                    data['succes'] = 1
                except Exception as e:
                    print(e)
                    less.delete()
                    raise e
    else:
        data['form'] = HomeWork()

    return render(request, "homework.html", context=data)

@group_required('Teachers', 'Students')
@login_required
def groups(request, group_id=None):
    def get_students_2(stud_dict: dict):
        res = []
        for i in stud_dict:
            st = Student.objects.get(id=i)
            res.append((f"{st.surname} {st.name} {st.patronymic}", st.phone, st.mail))
        return res

    user = User.objects.get(username=request.user.username)
    group = user.groups.all()

    if "Students" in str(group):
        print("This is a student!")
        data = get_data("Students")
        data['title'] = "Моя группа"

        student = Student.objects.get(login=request.user.username)
        all_groups = Groups.objects.all()
        for gr in all_groups:
            if str(student.pk) in gr.student_list:
                data['students'] = get_students_2(gr.student_list)

        return render(request, "studtable.html", context=data)
    else:
        print("This is a teacher!")
        data = get_data("Teachers")
        data['title'] = "Мои группы"

        teacher = Teacher.objects.get(login=request.user.username)
        all_groups = Groups.objects.all()

        data['content'] = []
        for gr in all_groups:
            if str(teacher.pk) in gr.teachers_list:
                if group_id:
                    if group_id == gr.pk:
                        data['group_id'] = group_id
                        data['students'] = get_students_2(gr.student_list)

                data['content'].append((gr.description, gr.pk))

        print(data['content'])

    return render(request, 'studtable.html', context=data)

@group_required('Administrators')
@login_required
def adm_teachers(request, teacher_id=None):
    title = 'Список учителей'
    data = get_data('Administrators')
    data['title'] = title

    adm = Administrator.objects.get(login=request.user.username)
    ei = EducationalInstitution.objects.get(id=adm.ei_id)
    if teacher_id:
        teacher = Teacher.objects.get(id=teacher_id)
        if ei.teachers_list:
            teacher_data = (teacher.surname, teacher.name, teacher.patronymic,
                            teacher.phone, teacher.mail)
            data['show'] = True
            data['teacher_id'] = str(teacher_id)
            data['teacher'] = teacher_data

            data['content'] = []
            for teach_id, username in ei.teachers_list.items():
                teacher_ = Teacher.objects.get(id=teach_id)
                data['content'].append((teach_id, f"{teacher_.surname} {teacher_.name[0]}. "))
        else:
            return redirect('home/admin-teachers')
    else:
        if ei.teachers_list:
            data['content'] = []
            for teach_id, username in ei.teachers_list.items():
                teacher = Teacher.objects.get(id=teach_id)
                data['content'].append((teach_id, f"{teacher.surname} {teacher.name[0]}. "))
        else:
            data['content'] = None
    return render(request, "administrator/teachers.html", context=data)

@group_required('Administrators')
@login_required
def add_new_teacher(request):
    title = 'Добавление учителей'
    data = get_data("Administrators")
    data['title'] = title

    if request.method == "POST":
        if request.FILES:
            a = request.FILES.get('file').chunks()
            a = list(map(lambda x: x.decode('utf-8'), a))
            b = "".join(a)
            try:
                teachers_json = dict(json.loads(b))

                data['accounts'] = []
                for key, val in teachers_json.items():
                    print(f"{key} >>> {val}")
                    new_user, created = User.objects.get_or_create(username=key, email=val['content'][4],)
                    data['account'] = 0
                    try:
                        if not created:
                            data['account'] = 1
                            data['accounts'].append(key)
                        else:
                            new_user.set_password(val['password'])
                            new_user.save()

                            group = Group.objects.get(name="Teachers")
                            teacher = Teacher(login=key,
                                              password=val['password'],
                                              surname=val['content'][0],
                                              name=val['content'][1],
                                              patronymic=val['content'][2],
                                              phone=val['content'][3],
                                              mail=val['content'][4],
                                              teach_id=new_user.id)
                            teacher.save()
                            new_user.groups.add(group)

                            adm = Administrator.objects.get(login=request.user.username)
                            ei = EducationalInstitution.objects.get(id=adm.ei_id)

                            old_teacher_list = ei.teachers_list
                            old_teacher_list[teacher.pk] = teacher.login
                            ei.teachers_list = old_teacher_list
                            ei.save()
                    except Exception as e:
                        print(e)
                        new_user.delete()
                        raise e
                        return HttpResponseServerError("<h1>505<br>Internal server error<h1>")

                if data['accounts']:
                    data['accounts'] = ", ".join(data['accounts'])

            except json.decoder.JSONDecodeError:
                data['check'] = True
        data['form'] = GroupAdd(request.FILES)
    else:
        print("NEW TEACHER >>> GET")
        data['form'] = GroupAdd()

    return render(request, 'registration/signup.html', context=data)

@group_required('Administrators')
@login_required
def add_new_student(request):
    title = 'Добавление студентов'
    data = get_data("Administrators")
    data['title'] = title

    if request.method == "POST":
        if request.FILES:
            a = request.FILES.get('file').chunks()
            a = list(map(lambda x: x.decode('utf-8'), a))
            b = "".join(a)
            try:
                students_json = dict(json.loads(b))
                for group_num, items in students_json.items():
                    gr = Groups.objects.get(description=group_num)
                    for st_id in items:
                        stud = Student.objects.get(id=st_id)
                        old_studs = gr.student_list
                        old_studs[st_id] = stud.login
                        gr.student_list = old_studs
                    gr.save()
            except platform_edu.models.Student.DoesNotExist:
                data['account'] = 2
            except json.decoder.JSONDecodeError:
                data['check'] = True
        data['form'] = GroupAdd(request.FILES)
    else:
        data['form'] = GroupAdd()

    return render(request, 'registration/signup.html', context=data)


@group_required('Administrators')
@login_required
def adm_groups(request, group_id=None):
    def get_students(stud_dict: dict):
        return tuple(stud_dict.values())

    title = 'Список групп'
    data = get_data('Administrators')
    data['title'] = title
    data['show'] = False

    adm = Administrator.objects.get(login=request.user.username)
    ei = EducationalInstitution.objects.get(id=adm.ei_id)
    if group_id:
        if ei.groups_list:
            data['show'] = True
            group = Groups.objects.get(id=group_id)
            data['group_id'] = group_id
            data['students'] = get_students(group.student_list)

            data['content'] = []
            for number, grp_id in ei.groups_list.items():
                data['content'].append((number, grp_id))
            print(f"Check the {group_id} group")
        else:
            return redirect('home/admin-groups')
    else:
        if ei.groups_list:
            data['content'] = []
            for number, grp_id in ei.groups_list.items():
                data['content'].append((number, grp_id))
        else:
            data['content'] = None

        print(f"Where is the groups?")

    return render(request, "administrator/groups.html", context=data)

@group_required('Administrators')
@login_required
def add_new_group(request):
    title = 'Добавление групп'
    data = get_data("Administrators")
    data['title'] = title

    if request.method == "POST":
        if request.FILES:
            a = request.FILES.get('file').chunks()
            a = list(map(lambda x: x.decode('utf-8'), a))
            b = "".join(a)
            try:
                courses_json = dict(json.loads(b))
                try:
                    data['accounts'] = []
                    data['account'] = 0
                    for group_num, items in courses_json.items():
                        print(items)
                        student_list = {}
                        for stud in items['student_list']:
                            new_user, created_user = User.objects.get_or_create(username=stud,
                                                                                email=items['student_list'][stud][5],)
                            try:
                                if not created_user:
                                    data['account'] = 1
                                    data['accounts'].append(stud)
                                else:
                                    new_user.set_password(items['student_list'][stud][0])
                                    new_user.save()

                                    group = Group.objects.get(name="Students")
                                    stud_data = [i for i in items['student_list'][stud]]
                                    stud_data.insert(0, stud)
                                    stud_data.append(new_user.pk)

                                    student = create_student(*stud_data)
                                    student.save()
                                    new_user.groups.add(group)

                                    student_list[student.pk] = student.login
                            except Exception as e:
                                print(e)
                                new_user.delete()
                                raise e
                                return HttpResponseServerError("<h1>505<br>Internal server error<h1>")

                        students_group = Groups(courses_list=items['courses_list'],
                                                student_list=student_list,
                                                description=group_num)
                        students_group.save()
                        for cours_id in items['courses_list']:
                            group_course = GroupCourse(id_course_id=cours_id, id_group_id=students_group.pk)
                            group_course.save()

                        adm = Administrator.objects.get(login=request.user.username)
                        ei = EducationalInstitution.objects.get(id=adm.ei_id)
                        old_groups_list = ei.groups_list
                        old_groups_list[students_group.description] = students_group.pk
                        ei.groups_list = old_groups_list
                        ei.save()

                except Exception as e:
                    print(e)
                    raise e
                    return HttpResponseServerError("<h1>505<br>Internal server error<h1>")

                if data['accounts']:
                    data['accounts'] = ", ".join(data['accounts'])

            except json.decoder.JSONDecodeError:
                data['check'] = True

        data['form'] = GroupAdd(request.FILES)
    else:
        data['form'] = GroupAdd()

    return render(request, 'registration/signup.html', context=data)

@group_required('Administrators')
@login_required
def adm_courses(request, course_id=None):
    def get_teachers(teachers: dict):
        res = []
        for i in teachers:
            res.append(Teacher.objects.get(id=i).name)
        return 'Авторы: ' + ', '.join(res)

    title = 'Список курсов'
    data = get_data('Administrators')
    data['title'] = title

    adm = Administrator.objects.get(login=request.user.username)
    ei = EducationalInstitution.objects.get(id=adm.ei_id)
    if course_id:
        course = Course.objects.get(id=course_id)
        if ei.courses_list:
            course_data = (get_teachers(course.teachers_list), 'Дисциплины: ' + ', '.join(course.subject_list),
                           'Название: ' + course.name, 'Описание: ' + course.description)
            data['course_id'] = str(course_id)
            data['course'] = course_data

            data['content'] = []
            for crs_id, name in ei.courses_list.items():
                data['content'].append((crs_id, name))
        else:
            return redirect('home/admin-courses')
    else:
        if ei.courses_list:
            data['content'] = []
            for crs_id in ei.courses_list:
                course = Course.objects.get(id=crs_id)
                data['content'].append((crs_id, course.name))
        else:
            data['content'] = None
    return render(request, "administrator/courses.html", context=data)

@group_required('Administrators')
@login_required
def add_new_course(request):
    title = 'Добавление курсов'
    data = get_data("Administrators")
    data['title'] = title
    if request.method == "POST":
        if request.FILES:
            a = request.FILES.get('file').chunks()
            a = list(map(lambda x: x.decode('utf-8'), a))
            b = "".join(a)
            try:
                courses_json = dict(json.loads(b))
                try:
                    data['accounts'] = []
                    data['account'] = 0
                    for i in courses_json:
                        print(courses_json[i])
                        course, created = Course.objects.get_or_create(teachers_list=courses_json[i]['teachers_list'],
                                                                       subject_list=courses_json[i]['subject_list'],
                                                                       name=courses_json[i]['name'],
                                                                       description=courses_json[i]['description'],)
                        if not created:
                            data['account'] = 1
                            data['accounts'].append(courses_json[i]['name'])
                        else:
                            course.save()
                except Exception as e:
                    print(e)
                    raise e
                    return HttpResponseServerError("<h1>505<br>Internal server error<h1>")

                if data['accounts']:
                    data['accounts'] = ", ".join(data['accounts'])
            except json.decoder.JSONDecodeError:
                data['check'] = True

        data['form'] = GroupAdd(request.FILES)
    else:
        data['form'] = GroupAdd()

    return render(request, 'registration/signup.html', context=data)


def home_page(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        group = user.groups.all()
        print(group)
        print(user.id)
        title = "Главная"
        data = {}
        content = tuple()
        if "Students" in str(group):
            print("This is a student!")
            data = get_data("Students")

            content = ("Добрый вечер", "Я Студент!")
        elif "Teachers" in str(group):
            print("This is a teacher!")
            data = get_data("Teachers")

            content = ("Добрый вечер", "Я Учитель!")
        elif "Administrators" in str(group):
            print("This is a admninistratos")
            data = get_data("Administrators")

            content = ("Добрый вечер", "Я Администратор!")

        data['title'] = title
        data['content'] = content

        return render(request, "student/main_page.html", context=data)
    else:
        return render(request, "index.html")

def registration(request):
    if request.method == "POST":
        print("Registration >>> POST")
        userform = UserForm(request.POST)
        if userform.is_valid():
            print(userform.cleaned_data)
            phone = request.POST.get("phone")
            phone = phone if phone[0] != '+' else '8' + phone[2:]

            user_data = {
                "login": request.POST.get("login"),
                "password": request.POST.get("password"),
                "surname": request.POST.get("surname"),
                "name": request.POST.get("name"),
                "patronymic": request.POST.get("patronymic"),
                "phone": phone,
                "mail": request.POST.get("mail"),
                "user_group": request.POST.get("user_group"),
            }
            print("PASSWORD >>> ", user_data['password'])
            new_user, created = User.objects.get_or_create(username=user_data['login'],
                                                           email=user_data['mail'],)
            try:
                if not created:
                    print("Account has already created")
                    return render(request, 'registration/signup.html', {'form': userform})
                else:
                    new_user.set_password(user_data['password'])
                    new_user.save()

                    if user_data['user_group'] == '1':
                        group = Group.objects.get(name="Students")
                        student = Student(login=user_data['login'],
                                          password=user_data['password'],
                                          surname=user_data['surname'],
                                          name=user_data['name'],
                                          patronymic=user_data['patronymic'],
                                          phone=user_data['phone'],
                                          mail=user_data['mail'],
                                          stud_id=new_user.id)
                        student.save()
                    else:
                        group = Group.objects.get(name="Teachers")
                        teacher = Teacher(login=user_data['login'],
                                          password=user_data['password'],
                                          surname=user_data['surname'],
                                          name=user_data['name'],
                                          patronymic=user_data['patronymic'],
                                          phone=user_data['phone'],
                                          mail=user_data['mail'],
                                          teach_id=new_user.id,)
                        teacher.save()

                    new_user.groups.add(group)
                    print(f"ID >>> {new_user.id}")
                    print(new_user)
                    print(new_user.groups.all())
                    return redirect('home')
            except Exception as e:
                print(e)
                new_user.delete()
                raise e
        else:
            print(">>> Form is not valid")
            userform = UserForm()
            return render(request, 'registration/signup.html', {'form': userform})

    elif request.method == "GET":
        print("Registration >>> GET")
        userform = UserForm()
        return render(request, 'registration/signup.html', {'form': userform})

def videochat(request):
    pass

@group_required('Teachers')
def create_videochat(request, group_num):
    response = create_room(group_num)
    print(response)
    return redirect(f"/home/videochat/?room_id={response['_id']}&group_id={group_num}")

@group_required('Teachers', "Students")
def join_room(request):
    print(request.GET)
    if request.GET['room_id']:
        with open('platform_edu/static/json/rooms.json') as file:
            rooms = json.loads(file.read())
            if request.GET['room_id'] in rooms:
                url = f"https://easyedu.metered.live/{rooms[request.GET['room_id']]['roomName']}"
                user = User.objects.get(username=request.user.username)
                group = user.groups.all()

                if "Students" in str(group):
                    path = "student/join_room.html"
                    return render(request, path, context={"url": url, "title": "Урок"})
                elif "Teachers" in str(group):
                    path = "teacher/new_room.html"
                    return render(request, path, context={"url": url, "title": "Урок", "group_id": request.GET['group_id']})
            else:
                return HttpResponseNotFound("<h1>Room does not exist</h1>")
    else:
        return HttpResponseNotFound("<h1>Need a room's id</h1>")

@group_required('Teachers')
def delete_room(request):
    print("DEL")
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        delete_room_req(data['room_name'])
        return JsonResponse({"res": True})
    else:
        print("DELETE GET >>>", request.GET)
        return HttpResponseNotFound()

@login_required
def get_courses(request, courses_id):
    def get_teachers(teachers: dict):
        res = []
        for i in teachers:
            res.append(Teacher.objects.get(id=i).name)
        return 'Авторы: ' + ', '.join(res)

    title = 'Список курсов'
    data = get_data('Administrators')
    data['title'] = title

    adm = Administrator.objects.get(login=request.user.username)
    ei = EducationalInstitution.objects.get(id=adm.ei_id)
    if course_id:
        course = Course.objects.get(id=course_id)
        if ei.courses_list:
            course_data = (get_teachers(course.teachers_list), 'Дисциплины: ' + ', '.join(course.subject_list),
                           'Название: ' + course.name, 'Описание: ' + course.description)
            data['course_id'] = str(course_id)
            data['course'] = course_data

            data['content'] = []
            for crs_id, name in ei.courses_list.items():
                data['content'].append((crs_id, name))
        else:
            return redirect('home/admin-courses')
    else:
        if ei.courses_list:
            data['content'] = []
            for crs_id in ei.courses_list:
                course = Course.objects.get(id=crs_id)
                data['content'].append((crs_id, course.name))
        else:
            data['content'] = None
    return render(request, "administrator/courses.html", context=data)

def index(request):
    return redirect('home')