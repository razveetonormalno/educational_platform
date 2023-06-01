from django import forms


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
    phone = forms.RegexField(label="Телефон", regex="^(([\+7|8])+([0-9]){10})$")
    mail = forms.EmailField(max_length=100, label="Почта")
    user_group = forms.ChoiceField(label="Должность", choices=groups)
