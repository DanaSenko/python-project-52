from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import DeleteView, ListView, UpdateView
from django.views.generic.edit import CreateView
from task_manager.tasks.models import Task

from .forms import UserCreateForm, UserUpdateForm
from .mixins import UserPermissionMixin


class UserListView(ListView):  # shows all users
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class CreateUserView(CreateView):  # user registaration and redirect to login page
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "users/create_user.html"
    success_message = "Пользователь успешно зарегистрирован"

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.success(self.request, "Пользователь успешно зарегистрирован")
            return redirect("login")
        return render(request, "users/create_user.html", {"form": form})


class UpdateUserView(UserPermissionMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/update_user.html"
    success_url = reverse_lazy("users_list")
    login_url = "login"

    def form_valid(self, form):
        if form.cleaned_data["password1"]:
            self.object.set_password(form.cleaned_data["password1"])
        messages.success(self.request, "Пользователь успешно изменен")
        return super().form_valid(form)


class DeleteUserView(
    UserPermissionMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = User
    template_name = "users/delete_user.html"
    success_url = reverse_lazy("users_list")
    success_message = "Пользователь успешно удален"
    login_url = "login"

    def post(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if Task.objects.filter(Q(author=user_to_delete) | Q(worker=user_to_delete)).exists():
            messages.warning(
                request, "Невозможно удалить пользователя, потому что он используется"
            )
            return redirect("users_list")
        return super().post(request, *args, **kwargs)
