from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', index, name='index'),  # 127.0.0.1:8000
    path('accounts/signup/', registration, name='registration'),

    path('home/videochat/create', create_videochat, name="createroom"),
    path('home/videochat/<int:room_id>', join_room, name='join-room'),
    # path('home/videochat/create/new', videochat_new, name="createroom"),

    path('home/timetable/', timetable, name="timetable"),
    path('home/homework/', homework, name="homework"),
    path('home/groups/', groups, name="groups"),

    path('home/admin-groups/', adm_groups, name="adm-groups"),
    path('home/admin-groups/<int:group_id>', adm_groups),
    path('home/admin-groups/add-new', add_new_group, name="add-new-group"),

    path('home/admin-teachers/', adm_teachers, name="admin-groups"),
    path('home/admin-teachers/<int:teacher_id>', adm_teachers),
    path('home/admin-teachers/add-new', add_new_teacher, name="add-new-teacher"),

    path('home/admin-courses/', adm_courses, name="admin-groups"),
    path('home/admin-courses/<int:course_id>', adm_courses),
    path('home/admin-courses/add-new', add_new_course, name="add-new-course"),
]