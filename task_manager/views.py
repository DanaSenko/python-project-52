from django.views.generic import TemplateView
from django.http import HttpResponse
import rollbar
from task_manager.users.forms import CustomAuthenticationForm
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages


class LoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Вы разлогинены")
        return redirect("index")


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
