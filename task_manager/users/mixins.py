from django.contrib import messages
from django.shortcuts import redirect

from task_manager.tasks.models import Task


class UserPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            messages.warning(request, "Вы не авторизованы! Пожалуйста, выполните вход.")
            return redirect("login")  # Перенаправление на страницу входа

        # Проверяем, пытается ли пользователь редактировать свой профиль
        user_to_edit = self.get_object()
        if user_to_edit != request.user:
            messages.warning(
                request, "У вас нет прав для изменения другого пользователя."
            )
            return redirect("users_list")
        return super().dispatch(request, *args, **kwargs)
