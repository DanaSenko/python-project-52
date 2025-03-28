from django import forms
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task

User = get_user_model()


class TaskCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # отображение исполнителя
        self.fields["executor"].label_from_instance = (
            lambda obj: f"{obj.first_name} {obj.last_name}"
        )

    name = forms.CharField(max_length=100, label="Имя", required=True)
    description = forms.CharField(
        widget=forms.Textarea, label="Описание", required=False
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.get_queryset(),
        label="Статус",
        required=True,
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Исполнитель",
        widget=forms.Select,
        required=False,
    )

    label = forms.ModelMultipleChoiceField(
        queryset=Label.objects.get_queryset(),
        widget=forms.SelectMultiple,
        required=False,
        label="Метки",
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "label"]
