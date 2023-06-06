from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),  # 127.0.0.1:8000
    path('accounts/signup', registration, name='registration'),

    path('home/videochat/create/<str:group_num>', create_videochat, name="createroom"),
    path('home/videochat/delete/', delete_room, name='delete-room'),
    path('home/videochat/', join_room, name='join-room'),
    path('home/courses/', get_courses, name="courses"),
    path('home/courses/<int:course_id>', get_courses),
    # path('home/videochat/create/new', videochat_new, name="createroom"),

    path('home/timetable/', timetable, name="timetable"),
    path('home/homework/', homework, name="homework"),
    path('home/homework/new/<str:group_id>', add_homework, name="add-homework"),
    path('home/homework/view/<str:group_id>/', view_homework, name="view-homework"),
    path('home/homework/view/<str:group_id>/<str:homework_id>/', choose_homework, name="choose-homework"),
    path('home/homework/view/<str:group_id>/<str:homework_id>/<str:student_id>/', open_homework, name="open-homework"),

    path('home/groups/', groups, name="groups"),
    path('home/groups/<int:group_id>', groups),

    path('home/admin-groups/', adm_groups, name="adm-groups"),
    path('home/admin-groups/<int:group_id>', adm_groups),
    path('home/admin-groups/add-new', add_new_group, name="add-new-group"),
    path('home/admin-groups/add-new-stud', add_new_student, name="add-new-stud"),

    path('home/admin-teachers/', adm_teachers, name="admin-groups"),
    path('home/admin-teachers/<int:teacher_id>', adm_teachers),
    path('home/admin-teachers/add-new', add_new_teacher, name="add-new-teacher"),

    path('home/admin-courses/', adm_courses, name="admin-groups"),
    path('home/admin-courses/<int:course_id>', adm_courses),
    path('home/admin-courses/add-new', add_new_course, name="add-new-course"),
]