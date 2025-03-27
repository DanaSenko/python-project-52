from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.tasks.models import Task

from .forms import StatusCreateForm
from .models import Status


# Create your views here.
class StatusListView(ListView):
    model = Status
    template_name = "status_list.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusCreateForm
    template_name = "status_create.html"
    success_url = reverse_lazy("statuses:status_list")

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusCreateForm
    success_url = reverse_lazy("statuses:status_list")
    template_name = "status_update.html"
    login_url = "login"

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменен")
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "status_delete.html"
    success_url = reverse_lazy("statuses:status_list")
    login_url = "login"

    def form_valid(self, form):
        status = self.get_object()
        if Task.objects.filter(status=status).exists():
            messages.warning(
                self.request, "Невозможно удалить статус, потому что он используется"
            )
            return redirect(self.success_url)
        return super().form_valid(form)
