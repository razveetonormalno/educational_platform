from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .forms import UserForm, GroupAdd
from .models import *
from django.contrib.auth.models import Group
from .custom import *
from django.contrib.auth.decorators import login_required, user_passes_test


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
        student = Student.objects.get(login=request.user.username)
        data = get_data("Students")

        content = ("Добрый вечер", "Я Студент!")
    elif "Teachers" in str(group):
        print("This is a teacher!")
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
def adm_teachers(request):
    pass

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
def adm_courses(request):
    pass


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
            return Http404(request)

    elif request.method == "GET":
        print("Registration >>> GET")
        userform = UserForm()
        return render(request, 'registration/signup.html', {'form': userform})

def videochat(request):
    pass

def index(request):
    return HttpResponse("Страница приложения EasyEdu.")