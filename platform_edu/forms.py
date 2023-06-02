from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_file(value):
    print(f'FILE >>> {value}')
    if value:
        raise ValidationError("Неправильный формат!")


class UserForm(forms.Form):
    groups = (
        (1, 'Ученик'),
        (2, 'Учитель'),
    )

    login = forms.SlugField(max_length=32, label="Логин:")
    password = forms.CharField(max_length=32, label="Пароль")
    surname = forms.CharField(max_length=100, label="Фамилия")
    name = forms.CharField(max_length=100, label="Имя")
    patronymic = forms.CharField(max_length=100, label="Отчество")
    phone = forms.RegexField(label="Телефон", regex=r"^(([\+7|8])+([0-9]){10})$", help_text="+71234567890 или 81234567890 ")
    mail = forms.EmailField(max_length=100, label="Почта")
    user_group = forms.ChoiceField(label="Должность", choices=groups)

class GroupAdd(forms.Form):
    file = forms.FileField(help_text=".json файл", validators=[validate_file])
