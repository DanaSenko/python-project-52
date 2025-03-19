from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import TaskFilter
from .models import Task
from .forms import TaskCreateForm
from django.contrib import messages


# Create your views here.
class TaskListView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = "task_list.html"
    context_object_name = "tasks"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_create.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("tasks:task_list")
    template_name = "task_update.html"
    login_url = "login"

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = reverse_lazy("tasks:task_list")
    login_url = "login"

    def delete(self, request, *args, **kwargs):
        task_to_delete = self.get_object()
        if task_to_delete.author != request.user:
            messages.error(
                request,
                "Вы не можете удалить эту задачу, так как вы не являетесь ее автором.",
            )
            return redirect(
                "tasks:task_list"
            )  # Перенаправление на страницу списка пользователей
        messages.success(request, "Задача успешно удалена.")
        return super().dispatch(request, *args, **kwargs)
