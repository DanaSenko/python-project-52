from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, FormView
from django.views.generic.edit import CreateView
from .forms import UserCreateForm, UserUpdateForm
from .mixins import UserPermissionMixin
from django.contrib import messages


class UserListView(ListView):  # shows all users
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class CreateUserView(CreateView):  # user registaration and redirect to login page
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = 'users/create_user.html'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
        return render(request, "users/create_user.html", {"form": form})



class UpdateUserView(UserPermissionMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update_user.html"
    success_url = reverse_lazy("users_list")
    login_url = "login"

    def form_valid(self, form):
        if form.cleaned_data["password"]:
            self.object.set_password(form.cleaned_data["password"])
        messages.success(self.request, "Пользователь успешно изменен")
        return super().form_valid(form)


class DeleteUserView(UserPermissionMixin, LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/delete_user.html"
    success_url = reverse_lazy("users_list")
    login_url = "login"


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
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
