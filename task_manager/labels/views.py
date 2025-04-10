from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.tasks.models import Task

from .forms import LabelCreateForm
from .models import Label


# Create your views here.
class LabelListView(ListView):
    model = Label
    template_name = 'label_list.html'
    context_object_name = 'labels'


class LabelCreateView(SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = 'label_create.html'
    success_url = reverse_lazy('labels:label_list')
    success_message = 'Метка успешно создана'


class LabelUpdateView(SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelCreateForm
    template_name = 'label_update.html'
    success_url = reverse_lazy('labels:label_list')
    success_message = 'Метка успешно изменена'


class LabelDeleteView(SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'label_delete.html'
    success_url = reverse_lazy('labels:label_list')
    success_message = 'Метка успешно удалена'

    def form_valid(self, form):
        labels = self.get_object()
        if Task.objects.filter(labels=labels).exists():
            messages.warning(
                self.request,
                'Невозможно удалить метку, потому что она используется',
            )
            return redirect(self.success_url)
        return super().form_valid(form)
