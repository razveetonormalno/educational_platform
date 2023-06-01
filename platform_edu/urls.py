from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', index, name='index'),  # 127.0.0.1:8000
    path('accounts/signup/', registration, name='registration'),
    path('home/videochat/', videochat, name="createroom"),
]