from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class UserCreateForm(forms.ModelForm):
    password1= forms.CharField(
        widget=forms.PasswordInput(attrs={"plaseholder": "Введите пароль"}),
        label="Пароль",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"}),
        label="Подтверждение пароля",
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",]
        labels = {
            "username": "Имя пользователя",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password_confirm", "Пароли не совпадают")
        return cleaned_data


class UserUpdateForm(UserCreateForm):
    pass


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Имя пользователя"
        self.fields["password"].label = "Пароль"
