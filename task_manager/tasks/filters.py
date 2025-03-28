import django_filters
from django import forms
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # отображение для выбора исполнителя
        if "executor" in self.form.fields:
            self.form.fields["executor"].label_from_instance = lambda obj: (
                f"{obj.first_name} {obj.last_name}".strip() or obj.username
            )

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Статус",
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Исполнитель",
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(),
        label="Метка",
    )
    self_tasks = django_filters.BooleanFilter(
        method="filter_self_tasks",
        label="Только свои задачи",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        fields = ["status", "executor", "labels", "self_tasks"]

    def filter_self_tasks(self, queryset, request, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
