from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.tasks.models import Task

from .forms import LabelCreateForm
from .models import Label


# Create your views here.
class LabelListView(ListView):
    model = Label
    template_name = "label_list.html"
    context_object_name = "labels"


class LabelCreateView(CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "label_create.html"
    success_url = reverse_lazy("labels:label_list")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class LabelUpdateView(UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "label_update.html"
    success_url = reverse_lazy("labels:label_list")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно изменена")
        return super().form_valid(form)


class LabelDeleteView(DeleteView):
    model = Label
    template_name = "label_delete.html"
    success_url = reverse_lazy("labels:label_list")
    # нельзя удалить метку если она прикреплена хотя бы к одной задаче

    def form_valid(self, form):
        label = self.get_object()
        if Task.objects.filter(label=label).exists():
            messages.error(
                self.request, "Невозможно удалить метку, потому что она используется"
            )
            return redirect(self.success_url)
        return super().form_valid(form)
