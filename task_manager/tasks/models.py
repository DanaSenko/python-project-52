from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.users.models import User

# Create your models here.
User = get_user_model()

class Task(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, blank=False, null=False, verbose_name="Статус")
    worker = models.ForeignKey(User, on_delete=models.PROTECT, related_name="assigned_tasks", verbose_name="Исполнитель")
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="authored_tasks", verbose_name="Автор")
    point = models.CharField(max_length=255, blank=True, null=True, verbose_name="Метка")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name