from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from .forms import UserForm, GroupAdd
from .models import *
from django.contrib.auth.models import Group
from .custom import *
from django.contrib.auth.decorators import login_required, user_passes_test
import json


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
        print(table_content)
        data['table'] = table_content

        content = ("Добрый вечер", "Я Студент!", f"Группа {group_number}")
    elif "Teachers" in str(group):
        print("This is a teacher!")

        teacher = Teacher.objects.get(login=request.user.username)
        table_content = get_for_teacher(str(teacher.pk))

        data = get_data("Teachers")
        content = ("Добрый вечер", "Я Учитель!")

    data['title'] = title
    data['content'] = content

    return render(request, 'timetable.html', context=data)

@group_required('Teachers', 'Students')
@login_required
def homework(request):
    pass

@group_required('Teachers', 'Students')
@login_required
def groups(request):
    pass

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

    add_group = GroupAdd(data)
    return render(request, "administrator/add-group.html", {"form": add_group})

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

    add_group = GroupAdd(data)
    return render(request, "administrator/add-group.html", {"form": add_group})

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
                data['content'].append((crs_id, course.name))
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

    add_group = GroupAdd(data)
    return render(request, "administrator/add-group.html", {"form": add_group})


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
def create_videochat(request):
    response = create_room()
    print(response)
    return redirect(f"/home/videochat/{response['_id']}")

@group_required('Teachers', "Students")
def join_room(request, room_id=None):
    if room_id:
        with open('platform_edu/static/json/rooms.json') as file:
            rooms = json.loads(file.read())
            if room_id in rooms:
                url = f"https://easyedu.metered.live/{rooms[room_id]['roomName']}"
                user = User.objects.get(username=request.user.username)
                group = user.groups.all()

                if "Students" in str(group):
                    path = "student/join_room.html"
                elif "Teachers" in str(group):
                    path = "teacher/new_room.html"

                return render(request, path, context={"url": url, "title": "Урок"})
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
        delete_room(data['room_name'])
        return JsonResponse({"res": True})
    else:
        print("DELETE GET >>>", request.GET)
        return HttpResponseNotFound()

def index(request):
    return redirect('home')