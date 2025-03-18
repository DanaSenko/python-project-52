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
    self_tasks = django_filters.BooleanFilter(method='filter_self_tasks', label="Только мои задачи",)
    
    class Meta:
        fields = ["status", "worker", "label", "author", "self_tasks"]


    def filter_self_tasks(self, queryset, reqeust, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
