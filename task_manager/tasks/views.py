from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskCreateForm
from .models import Task


# Create your views here.
class TaskListView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = "task_list.html"
    context_object_name = "tasks"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "task_details.html"
    login_url = "login"


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task_create.html"
    success_message = "Задача успешно создана"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("tasks:task_list")
    success_message = "Задача успешно изменена"
    template_name = "task_update.html"
    login_url = "login"


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "task_delete.html"
    success_url = reverse_lazy("tasks:task_list")
    success_message = "Задача успешно удалена"
    login_url = "login"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.warning(request, "Задачу может удалить только ее автор")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
