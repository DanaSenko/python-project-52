import rollbar
from django.contrib import messages
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from task_manager.users.forms import CustomAuthenticationForm


class LoginView(DjangoLoginView):
    form_class = CustomAuthenticationForm
    template_name = "login.html"
    next_page = reverse_lazy("index")

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)


class IndexView(TemplateView):
    template_name = "index.html"


def test_rollbar(request):
    try:
        # Генерация тестовой ошибки
        raise ValueError("This is a test error for Rollbar")
    except Exception as e:
        # Отправка ошибки в Rollbar
        rollbar.report_exc_info()
        return HttpResponse("An error occurred, but it's been reported to Rollbar.")
