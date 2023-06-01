from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .forms import UserForm
from .models import *


def home_page(request):
    return render(request, "main.html")

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

            new_user, created = User.objects.get_or_create(username=user_data['login'],
                                                           email=user_data['mail'],
                                                           password=user_data['password'])
            try:
                if not created:
                    print("Account has already created")
                    return render(request, 'registration/signup.html', {'form': userform})
                else:
                    if user_data['user_group'] == '1':
                        group = Group.objects.get(name="Students")
                        student = Student(login=user_data['login'],
                                          password=user_data['password'],
                                          surname=user_data['surname'],
                                          name=user_data['name'],
                                          patronymic=user_data['patronymic'],
                                          phone=user_data['phone'],
                                          mail=user_data['mail'],)
                        student.save()
                    else:
                        group = Group.objects.get(name="Teachers")
                        teacher = Teacher(login=user_data['login'],
                                          password=user_data['password'],
                                          surname=user_data['surname'],
                                          name=user_data['name'],
                                          patronymic=user_data['patronymic'],
                                          phone=user_data['phone'],
                                          mail=user_data['mail'],)
                        teacher.save()

                    new_user.groups.add(group)

                    print(new_user)
                    print(new_user.groups.all())
                    return render(request, 'main.html')
            except Exception as e:
                print(e)
                new_user.delete()
                raise e
                # return render(request, 'registration/signup.html', {'form': userform})
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