from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Label
from .forms import LabelCreateForm
from django.contrib import messages


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

    def delete(self, request, *args, **kwargs):
        label = self.get_object()
        if label.task_set.exists():
            messages.error(
                request, "Невозможно удалить метку, так как она связана с задачами"
            )
            return redirect("labels:label_list")
        massages.success(request, "Метка успешно удалена")
        return super().delete(request, *args, **kwargs)
