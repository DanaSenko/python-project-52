from django.views.generic import TemplateView
from django.http import HttpResponse
import rollbar
from task_manager.users.forms import CustomAuthenticationForm
from django.views import View
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages


class LoginView(DjangoLoginView):
    form_class = CustomAuthenticationForm
    template_name = "login.html"
    next_page = reverse_lazy("index")

    def form_valid(self, form):
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
