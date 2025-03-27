from django import forms
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task

User = get_user_model()


class TaskCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Имя", required=True)
    description = forms.CharField(
        widget=forms.Textarea, label="Описание", required=False
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label="Статус",
        to_field_name="name",
        required=True,
    )
    worker = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Исполнитель",
        widget=forms.Select,
        to_field_name="username",
        required=False,
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
