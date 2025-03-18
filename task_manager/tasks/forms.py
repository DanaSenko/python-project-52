from django import forms
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label

User = get_user_model()


class TaskCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Имя")
    description = forms.CharField(widget=forms.Textarea, label="Описание")
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(), label="Статус", to_field_name="name"
    )
    worker = forms.ModelChoiceField(
        queryset=User.objects.all(), label="Исполнитель", to_field_name="username"
    )
    label = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
        label="Метка",
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "worker", "label"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].queryset = Status.objects.all()
        self.fields["worker"].queryset = User.objects.all()
