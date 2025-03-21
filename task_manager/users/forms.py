from django import forms
from django.contrib.auth.models import User
from django.contrib import messages


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"plaseholder": "Введите пароль"}),
        label="Пароль",
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"}),
        label="Подтверждение пароля",
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
        labels = {
            "username": "Имя пользователя",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            messages.error(request, "Пароли не совпадают")

        return cleaned_data


class UserUpdateForm(UserCreateForm):
    pass
