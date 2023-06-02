from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', index, name='index'),  # 127.0.0.1:8000
    path('accounts/signup/', registration, name='registration'),

    path('home/videochat/', videochat, name="createroom"),
    path('home/timetable/', timetable, name="timetable"),
    path('home/homework/', homework, name="homework"),
    path('home/groups/', groups, name="groups"),

    path('home/admin-groups/', adm_groups, name="adm-groups"),
    path('home/admin-groups/<int:group_id>', adm_groups),
    path('home/admin-groups/add-new', add_new_group, name="add-new-group"),

    path('home/admin-teachers/', adm_teachers, name="admin-groups"),

    path('home/admin-courses/', adm_courses, name="admin-groups"),
]