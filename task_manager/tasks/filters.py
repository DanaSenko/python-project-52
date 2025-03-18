import django_filters
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(), label="Статус",)
    worker = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label="Испольнитель",)
    label = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all(),
        label="Метки",)

    class Meta:
        fields = ["status", "worker", "label", "author"]

